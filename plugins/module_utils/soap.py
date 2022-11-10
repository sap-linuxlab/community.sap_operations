#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

import http.client
import socket
import ssl
import time
import traceback
import urllib.request

from ansible.module_utils.basic import missing_required_lib


try:
    from suds.client import Client
    from suds.transport.http import HttpAuthenticated, HttpTransport
except (ImportError, NameError):
    # To avoid import error
    HttpAuthenticated = object
    HttpTransport = object
    HAS_SUDS_LIBRARY = False
    SUDS_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_SUDS_LIBRARY = True


YELLOW = "SAPControl-YELLOW"  # In transition
GREEN = "SAPControl-GREEN"  # Running
RED = "SAPControl-RED"  # Failure
GRAY = "SAPControl-GRAY"  # Stopped


def check_sdk(module):
    if not HAS_SUDS_LIBRARY:
        module.fail_json(
            msg=missing_required_lib("suds"), exception=SUDS_LIBRARY_IMPORT_ERROR
        )


class LocalSocketHttpConnection(http.client.HTTPConnection):
    def __init__(
        self,
        host,
        port=None,
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
        source_address=None,
        socketpath=None,
    ):
        super().__init__(host, port, timeout, source_address)
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(socketpath)


class LocalSocketHandler(urllib.request.HTTPHandler):
    def __init__(
        self,
        debuglevel=0,
        socketpath=None,
    ):
        self._debuglevel = debuglevel
        self._socketpath = socketpath

    def http_open(self, req):
        return self.do_open(LocalSocketHttpConnection, req, socketpath=self._socketpath)


class LocalSocketHttpAuthenticated(HttpAuthenticated):
    def __init__(self, socketpath, **kwargs):
        HttpAuthenticated.__init__(self, **kwargs)
        self._socketpath = socketpath

    def u2handlers(self):
        handlers = HttpTransport.u2handlers(self)
        handlers.append(LocalSocketHandler(socketpath=self._socketpath))
        return handlers


class SAPClient(object):
    poll_interval = 3

    def __init__(
        self,
        hostname,
        username,
        password,
        ca_file,
        secure,
        instance,
        wait=True,
        wait_timeout=1200,
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ca_file = ca_file
        self.secure = secure
        self.instance = instance
        self.wait = wait
        self.wait_timeout = wait_timeout
        self.client = None

    def connect(self):
        if self.hostname is None or self.hostname == "localhost":
            return self._connect_local()

        return self._connect_http()

    def _connect_local(self):
        try:
            localsocket = LocalSocketHttpAuthenticated(
                "/tmp/.sapstream5{0}13".format(str(self.instance).zfill(2))
            )
            client = Client("http://localhost/sapcontrol?wsdl", transport=localsocket)
        except Exception as e:
            raise Exception(str(e))

        self.client = client.service

    def _connect_http(self):
        protocol = "http" if self.secure == "none" else "https"
        port = "5{0}1{1}".format(
            str(self.instance).zfill(2), "3" if self.secure == "none" else "4"
        )
        url = "{0}://{1}:{2}/sapcontrol?wsdl".format(protocol, self.hostname, port)

        if self.secure == "strict":
            if self.ca_file is not None:
                ssl._create_default_https_context = lambda: ssl.create_default_context(
                    cafile=self.ca_file
                )
        elif self.secure == "insecure":
            if self.ca_file is not None:
                ssl._create_default_https_context = (
                    lambda: ssl._create_unverified_context(cafile=self.ca_file)
                )

        try:
            client = Client(url, username=self.username, password=self.password)
        except Exception as e:
            raise Exception(str(e) + url)

        self.client = client.service

    def parameter_value(self, name=None):
        return self.client.ParameterValue(parameter=name).split("\n")

    def get_system_instance_list(self):
        return [dict(s) for s in self.client.GetSystemInstanceList()[0]]


class SystemClient(SAPClient):

    # TODO(kirill): What should we wait for in case of specific system definition?
    # features = 'MESSAGESERVER|ENQUE|ABAP|GATEWAY|ICMAN|IGS'
    instance_map = {
        "ALL": 0,
        "SCS": 1,
        "DIALOG": 2,
        "ABAP": 3,
        "J2EE": 4,
        "TREX": 5,
        "ENQREP": 6,
        "HDB": 7,
        "ALLNOHDB": 8,
        "LEVEL": 9,
    }
    features_map = {
        "ALL": ["ABAP", "MESSAGESERVER"],
        "SCS": ["MESSAGESERVER"],
        "DIALOG": ["ABAP"],
        "ABAP": ["ABAP"],
        "J2EE": [],  # Nothing is stoppped.
        "TREX": [],  # Don't work.
        "ENQREP": [],  # Nothing is stoppped.
        "HDB": [],  # Nothing is stoppped.
        "ALLNOHDB": [],
        "LEVEL": [],
    }

    def update_system(self, soft_timeout=None, force=None):
        self.client.UpdateSystem(
            softtimeout=soft_timeout, force=force, waittimeout=self.wait_timeout
        )

        if self.wait:
            # TODO: how to wait?
            pass

    def start_system(self, instance):
        self.client.StartSystem(
            options=self.instance_map.get(instance, 0), waittimeout=self.wait_timeout
        )

        if self.wait:
            self.wait_for_system_status(instance, GREEN)

    def stop_system(self, instance):
        self.client.StopSystem(
            options=self.instance_map.get(instance, 0),
            waittimeout=self.wait_timeout,
            softtimeout=1,
        )

        if self.wait:
            self.wait_for_system_status(instance, GRAY)

    def is_system_down(self):
        if all(GRAY == i["dispstatus"] for i in self.get_system_instance_list()):
            return True

    def is_system_running(self):
        if all(GREEN == i["dispstatus"] for i in self.get_system_instance_list()):
            return True

    def wait_for_system_status(self, name, status):
        # TODO(kiril): Remove?
        # No action needed, as nothing happens on our intance?
        if not self.features_map.get(name):
            return

        instances = {}
        features_map = self.features_map.get(name)
        for instance in self.get_system_instance_list():
            if [e in instance.get("features").split("|") for e in features_map]:
                instances[instance.get("instanceNr")] = False

        for _i in range(0, self.wait_timeout, self.poll_interval):
            if all(instances.values()):
                return

            for instance in self.get_system_instance_list():
                if [e in instance.get("features").split("|") for e in features_map]:
                    # Check state:
                    if instance.get("dispstatus") == status:
                        instances[instance.get("instanceNr")] = True

            time.sleep(self.poll_interval)

    def wait_for_system_transition(self):
        if all(YELLOW != i["dispstatus"] for i in self.get_system_instance_list()):
            return

        if not self.wait:
            raise Exception(
                "Instance is in transition and module is configured not to wait"
            )

        for _i in range(0, self.wait_timeout * self.poll_interval, self.poll_interval):
            time.sleep(self.poll_interval)
            if all(YELLOW != i["dispstatus"] for i in self.get_system_instance_list()):
                break
        else:
            raise Exception("Timeout: system is still not started or stopped")


class InstanceClient(SAPClient):
    def instance_start(self, instance_host, instance_number, wait=False):
        self.client.InstanceStart(host=instance_host, nr=instance_number)

        if wait:
            self.wait_for_instance_status(instance_host, instance_number, GREEN)

    def instance_stop(self, instance_host, instance_number, wait=False):
        self.client.InstanceStop(host=instance_host, nr=instance_number)

        if wait:
            self.wait_for_instance_status(instance_host, instance_number, GRAY)

    def is_instance_running(self, instance_host, instance_number):
        return GREEN == self.instance_dispstatus(instance_host, instance_number)

    def is_instance_stopped(self, instance_host, instance_number):
        return GRAY == self.instance_dispstatus(instance_host, instance_number)

    def system_instance_dispstatus(self, instance_host, instance_number):
        return self.get_system_instance(instance_host, instance_number).get(
            "dispstatus"
        )

    def get_system_instance(self, instance_host, instance_number):
        instance_list = self.get_system_instance_list()
        for inst in instance_list:
            if (
                inst["hostname"] == instance_host
                and inst["instanceNr"] == instance_number
            ):
                return inst
        return dict()

    def wait_for_instance_status(self, instance_host, instance_number, status):
        for i in range(0, self._wait_timeout, self.poll_interval):
            if all(
                p == status
                for p in self.system_instance_dispstatus(instance_host, instance_number)
            ):
                return
            else:
                time.sleep(self.poll_interval)

    def wait_for_instance_transition(self, instance_host, instance_number):
        if YELLOW != self.system_instance_dispstatus(instance_host, instance_number):
            return

        if not self.wait:
            raise Exception(
                "Instance is in transition and module is configured not to wait"
            )

        for _i in range(0, self.wait_timeout * self.poll_interval, self.poll_interval):
            time.sleep(self.poll_interval)
            if YELLOW != self.system_instance_dispstatus(
                instance_host, instance_number
            ):
                break
        else:
            raise Exception(
                "Timeout: instance host '{0}' / numbver {1} is still not started or stopped".format(
                    instance_host, instance_number
                )
            )


class ServiceClient(SAPClient):
    def start(self):
        self.client.Start()

        if self.wait:
            self.wait_for_proccesses_status(GREEN)

    def stop(self):
        self.client.Stop()

        if self.wait:
            self.wait_for_proccesses_status(GRAY)

    def is_service_running(self):
        return all(p == GREEN for p in self.proccess_dispstatus())

    def is_service_stopped(self):
        return all(p == GRAY for p in self.proccess_dispstatus())

    def wait_for_proccesses_status(self, status):
        for i in range(0, self.wait_timeout, self.poll_interval):
            if all(p == status for p in self.proccess_dispstatus()):
                return
            else:
                time.sleep(self.poll_interval)

    def proccess_dispstatus(self):
        return [p["dispstatus"] for p in self.get_proccess_list()]

    def any_proccess_dispstatus(self, status):
        return any(p == status for p in self.proccess_dispstatus())

    def get_proccess_list(self):
        r = self.client.GetProcessList()
        if len(r) > 0:
            return [dict(p) for p in r[0]]
        return []

    def wait_for_service_transition(self):
        if not self.any_proccess_dispstatus(YELLOW):
            return

        if not self.wait:
            raise Exception(
                "Service is in transition and module is configured not to wait"
            )

        for _i in range(0, self.wait_timeout * self.poll_interval, self.poll_interval):
            time.sleep(self.poll_interval)
            if not self.any_proccess_dispstatus(YELLOW):
                break
        else:
            raise Exception("Timeout: services are still not started or stopped")
