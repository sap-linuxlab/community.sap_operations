#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2022 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: system_info

author:
  - Ondra Machacek (@machacekondra)
  - Kirill Satarin (@kksat)

short_description: SAP system information

description:
  - Fetch the info about SAP systme
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
  secure:
    description:
      - "I(secure) specify if secure communication should be enforced."
      - "By default system CA store is used. User can pass custom CA by I(ca_file) parameter."
    choices: [ strict,insecure,none ]
    default: strict
    type: str
  instance_number:
    description:
      - The instance number of the managed service.
      - Must be between "00" and "99".
    type: str
    required: true
  status:
    description:
      - Return only instances with the I(status).
    type: str
  feature:
    description:
      - Return only instances with the I(feature).
    type: str
requirements:
  - python >= 3.6
  - suds >= 1.1.2
"""

EXAMPLES = r"""
- name: Fetch system info
  sap.sap_operations.system_info:
    username: "npladm"
    password: "secret123!"
    hostname: "sap.system.example.com"
    instance_number: "0"
    state: started
"""

RETURN = r"""
system_info:
    description: System info
    type: list
    returned: always
    sample: [{
        'hostname': vhcalnplcs,
        'instanceNr': 1,
        'httpPort': 50113,
        'httpsPort': 50114,
        'startPriority': 1,
        'features': MESSAGESERVER|ENQUE,
        'dispstatus': SAPControl-GREEN
    }]
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.sap.sap_operations.plugins.module_utils import soap


def soap_client(hostname, username, password, ca_file, secure, instance):
    return soap.SystemClient(hostname, username, password, ca_file, secure, instance)


def parse(instance_list, status, feature):
    if status is None and feature is None:
        return instance_list

    r = []
    for i in instance_list:
        if status and i["dispstatus"] == status:
            r.append(i)
        if feature and feature in i["features"].split("|"):
            r.append(i)

    return r


def main():
    module_args = dict(
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        hostname=dict(type="str"),
        ca_file=dict(type="str"),
        instance_number=dict(type="str", required=True),
        secure=dict(
            choices=["strict", "insecure", "none"], default="strict", type="str"
        ),
        status=dict(type="str"),
        feature=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )
    soap.check_sdk(module)

    hostname = module.params.get("hostname")
    username = module.params.get("username")
    password = module.params.get("password")
    ca_file = module.params.get("ca_file")
    secure = module.params.get("secure")
    instance_number = module.params.get("instance_number")
    status = module.params.get("status")
    feature = module.params.get("feature")

    result = dict(system_info={})
    client = soap_client(hostname, username, password, ca_file, secure, instance_number)
    try:
        client.connect()
    except Exception as err:
        module.fail_json(msg=(str(err)))

    result["system_info"] = parse(client.get_system_instance_list(), status, feature)

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
