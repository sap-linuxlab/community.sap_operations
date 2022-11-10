#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: rolling_kernel_switch

author:
  - Ondra Machacek (@machacekondra)

short_description: Manage Rolling kernel switch

description:
  - Rolling kernel switch
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
  wait:
    description:
      - Wait for the operation to complete before returning.
      - If set to C(true), module will wait for system update to finish.
      - If set to C(false), module will not wait for system update to finish.
        immediatelly.
    type: bool
    default: true
  wait_timeout:
    description:
      - Wait timeout for the operation to complete before returning.
    type: int
    default: 600
  soft_timeout:
    description:
      - Wait timeout for the operation to complete before returning.
    type: int
  force:
    description:
      - If C(true) don't enforce some minor update checks.
    type: bool
    default: false
"""

EXAMPLES = r"""
- name: Run the system update
  sap.sap_operations.rolling_kernel_switch:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    instance_number: "0"
"""

RETURN = r""" # """


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sap.sap_operations.plugins.module_utils import soap


def soap_client(
    hostname, username, password, ca_file, secure, instance, wait, wait_timeout
):
    return soap.SystemClient(
        hostname, username, password, ca_file, secure, instance, wait, wait_timeout
    )


def update_system(client, check_mode, soft_timeout, force):
    client.wait_for_system_transition()

    if check_mode:
        return True, client.get_system_instance_list()

    client.update_system(soft_timeout, force)
    return True, client.get_system_instance_list()


def main():
    module_args = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        hostname=dict(type="str"),
        soft_timeout=dict(type="int"),
        force=dict(type="bool", default=False),
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
    wait = module.params.get("wait")
    wait_timeout = module.params.get("wait_timeout")
    force = module.params.get("force")
    soft_timeout = module.params.get("soft_timeout")

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

    result["changed"], result["system"] = update_system(
        client, module.check_mode, soft_timeout, force
    )
    module.exit_json(**result)


if __name__ == "__main__":
    main()
