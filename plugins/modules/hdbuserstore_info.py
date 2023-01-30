#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Red Hat, Project Atmosphere
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: hdbuserstore_info

author:
  - Ondra Machacek (@machacekondra)

short_description: Get information from HANA user store (HANA command hdbsuserstore)

description: |
  Get information from HANA user store (HANA command hdbsuserstore)
  Key name is returned in case key exists (set previously)

version_added: 1.0.0

notes:
  - "See NOTE in documentation for I(hdbuserstore) module in regards to running ansible modules when becoming <hanasid>adm user with '-i'
     flag. Otherwise you might face issues with ansible module executions in SAP HANA environments."

options:
  binary_path:
    description:
      - "Custom path of the I(hdbuserstore) binary."
    type: str
    required: false
  key:
    description:
      - "Get info about the I(key)."
    type: str
requirements:
  - python >= 3.6
"""

EXAMPLES = r"""
- name: Get info about the key mykey from HDB user store
  sap.sap_operations.hdbuserstore_info:
    key: mykey
"""

RETURN = r"""
stdout:
    description: HDB key info
    type: str
    returned: always
"""

import os

from ansible.module_utils.basic import AnsibleModule


def main():
    module_args = dict(
        key=dict(type="str", no_log=False),
        binary_path=dict(type="str", default=""),
    )

    result = dict(changed=False, env={})
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    binary = os.path.join(module.params.get("binary_path"), "hdbuserstore")
    key = module.params.get("key", "")
    _rc, result["stdout"], _err = module.run_command(args=[binary, "List", key])

    module.exit_json(**result)


if __name__ == "__main__":
    main()
