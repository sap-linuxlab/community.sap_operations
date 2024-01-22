#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: system

author:
  - Ondra Machacek (@machacekondra)
  - Kirill Satarin (@kksat)

short_description: Manage SAP system

description:
  - Start and stop SAP system.
version_added: 1.0.0

seealso:
  - name: How to use the SAPControl Web Service Interface
    description: How to use the SAPControl Web Service Interface
    link: https://assets.cdn.sap.com/sapcom/docs/2016/09/0a40e60d-8b7c-0010-82c7-eda71af511fa.pdf

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
  secure:
    description:
      - "I(secure) specify if secure communication should be enforced."
      - "By default system CA store is used. User can pass custom CA by I(ca_file) parameter."
    choices: [ strict,insecure,none ]
    default: strict
    type: str
  name:
    description:
      - "I(name) name of the feature to be managed."
    choices: [ALL, SCS, DIALOG, ABAP, J2EE, TREX, ENQREP, HDB, ALLNOHDB, LEVEL]
    default: ALL
    type: str
  state:
    description:
      - State of the managed system.
    type: str
    choices: [ started, stopped ]
    default: started
  instance_number:
    description:
      - The instance number of the managed service.
      - Must be between "0" and "99".
    type: str
    required: true
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
- name: Use module with local socket on target machine
  sap.sap_operations.system:
    instance_number: "0"

- name: Start system
  sap.sap_operations.system:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    instance_number: "0"
    state: started

- name: Stop system
  sap.sap_operations.system:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    instance_number: "0"
    state: stopped

"""

RETURN = r"""
system:
    description: System info
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
    return soap.SystemClient(
        hostname, username, password, ca_file, secure, instance, wait, wait_timeout
    )


def ensure_started(client, name, check_mode):
    client.wait_for_system_transition()

    if client.is_system_running():
        return False, client.get_system_instance_list()

    if check_mode:
        return True, client.get_system_instance_list()

    client.start_system(name)
    return True, client.get_system_instance_list()


def ensure_stopped(client, name, check_mode):
    client.wait_for_system_transition()

    if client.is_system_down():
        return False, client.get_system_instance_list()

    if check_mode:
        return True, client.get_system_instance_list()

    client.stop_system(name)
    return True, client.get_system_instance_list()


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
        name=dict(
            type="str",
            choices=[
                "ALL",
                "SCS",
                "DIALOG",
                "ABAP",
                "J2EE",
                "TREX",
                "ENQREP",
                "HDB",
                "ALLNOHDB",
                "LEVEL",
            ],
            default="ALL",
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
    name = module.params.get("name")
    wait = module.params.get("wait")
    wait_timeout = module.params.get("wait_timeout")

    result = dict(changed=False, system={})
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
        result["changed"], result["system"] = ensure_started(
            client, name, module.check_mode
        )
    else:
        result["changed"], result["system"] = ensure_stopped(
            client, name, module.check_mode
        )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
