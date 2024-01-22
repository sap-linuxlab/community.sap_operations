#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: service

author:
  - Ondra Machacek (@machacekondra)

short_description: Manage SAP HANA services

description:
  - Start and stop SAP HANA services
version_added: 1.0.0

options:
  username:
    description:
      - "I(username) of the SAP system"
    type: str
  password:
    description:
      - "I(password) of the SAP system"
    type: str
  hostname:
    description:
      - "I(hostname) of the SAP system"
    type: str
  ca_file:
    description:
      - "I(ca_file) use CA certificate to secure the communication. By default system CA store is used."
    type: str
  instance_number:
    description:
      - "I(instance_number) is the instance number to be managed."
    type: str
    required: true
  secure:
    description:
      - "I(secure) specify if secure communication should be enforced."
      - "By default system CA store is used. User can pass custom CA by I(ca_file) parameter."
    choices: [ strict,insecure,none ]
    default: strict
    type: str
  state:
    description:
      - State of the managed service.
    type: str
    choices: [ started, stopped ]
    default: started
  wait:
    description:
      - Wait for the operation to complete before returning.
      - If set to C(true), module will wait for service to start/ or stop.
      - If set to C(false), module will schedule the right operation and return
        immediatelly.
    type: bool
    default: true
  wait_timeout:
    description:
      - Wait timeout for the operation to complete before returning.
    type: int
    default: 600
requirements:
  - python >= 3.6
  - suds >= 1.1.2
"""

EXAMPLES = r"""
- name: Start the service and wait for service to be available using unix socket
  sap.sap_operations.service:
    instance_number: "0"

- name: Start the service and wait for service to be available using username/password
  sap.sap_operations.service:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"

- name: Start the service and do not wait for service to be up and running
  sap.sap_operations.service:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    instance_number: "0"
    state: started
    wait: false

- name: Stop the service and wait for termination
  sap.sap_operations.service:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    state: stopped

- name: Stop the service and do not wait
  sap.sap_operations.service:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    state: stopped
    wait: false
"""

RETURN = r"""
instances:
    description: Instance parameters
    type: dict
    returned: always
    sample: {
        'hostname': vhcalnplcs,
        'instanceNr': 1,
        'httpPort': 50113,
        'httpsPort': 50114,
        'startPriority': 1,
        'features': MESSAGESERVER|ENQUE,
        'dispstatus': SAPControl-GREEN
    }
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sap.sap_operations.plugins.module_utils import soap


def soap_client(
    hostname, username, password, ca_file, secure, instance, wait, wait_timeout
):
    return soap.ServiceClient(
        hostname, username, password, ca_file, secure, instance, wait, wait_timeout
    )


def ensure_started(client, check_mode):
    client.wait_for_service_transition()

    if client.is_service_running():
        return False, client.get_proccess_list()

    if check_mode:
        return True, client.get_proccess_list()

    client.start()
    return True, client.get_proccess_list()


def ensure_stopped(client, check_mode):
    client.wait_for_service_transition()

    if client.is_service_stopped():
        return False, client.get_proccess_list()

    if check_mode:
        return True, client.get_proccess_list()

    client.stop()
    return True, client.get_proccess_list()


def main():
    module_args = dict(
        state=dict(
            type="str",
            choices=[
                "started",
                "stopped",
            ],
            default="started",
        ),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        hostname=dict(type="str"),
        ca_file=dict(type="str"),
        instance_number=dict(type="str", required=True),
        secure=dict(
            choices=["strict", "insecure", "none"], default="strict", type="str"
        ),
        wait=dict(type="bool", default=True),
        wait_timeout=dict(type="int", default=600),
    )

    result = dict(changed=False, processes={}, error="")
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_together=[["username", "password", "hostname"]],
    )
    soap.check_sdk(module)

    hostname = module.params.get("hostname")
    username = module.params.get("username")
    password = module.params.get("password")
    ca_file = module.params.get("ca_file")
    secure = module.params.get("secure")
    instance_number = module.params.get("instance_number")
    wait = module.params.get("wait")
    wait_timeout = module.params.get("wait_timeout")

    client = soap_client(
        hostname,
        username,
        password,
        ca_file,
        secure,
        instance_number,
        wait,
        wait_timeout,
    )
    try:
        client.connect()
    except Exception as err:
        module.fail_json(msg=(str(err)))

    if module.params["state"] == "started":
        result["changed"], result["processes"] = ensure_started(
            client, module.check_mode
        )
    else:
        result["changed"], result["processes"] = ensure_stopped(
            client, module.check_mode
        )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
