#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Red Hat, Project Atmosphere
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: hdbuserstore

author:
  - Ondra Machacek (@machacekondra)

short_description: Manage the HANA user store (HANA command hdbuserstore)

description: |
  Manage the HANA user store (HANA command hdbuserstore)
  Get and set HANA user store records.
version_added: 1.0.0

options:
  state:
    description:
      - "If I(present) the key will be created, removed otherwise."
    type: str
    choices: ['present', 'absent']
    default: 'present'
  binary_path:
    description: |
      Custom path of the I(hdbuserstore) binary.
      Variable I(binary_path) is required if hdbuserstore command cannot be found in PATH environment variable (with user running the module).
      See examples section to find several ways not to provide value for this variable.
    type: str
    required: false
  key:
    description:
      - "Manage the I(key)."
    type: str
    required: true
  env:
    description: |
      Database location (host:port).
      Required only if C(state=present)
    type: str
  username:
    description: |
      Username for the hdb store
      Required only if you set new key, C(state=present)
    type: str
  password:
    description: |
      Password for the hdb store username.
      Required only if you set new key, state=present
    type: str
  force:
    description: |
      If I(true) the key will be updated even if already exists. Used to update password.
      If set to I(false) (default value) module will return OK, but will not update the key, key will be created only if it does not exists
    type: bool
    default: false
requirements:
  - python >= 3.6
extends_documentation_fragment: action_common_attributes
attributes:
  check_mode:
    support: full
  diff_mode:
    support: none
  platform:
    platforms: posix
"""

EXAMPLES = r"""
- name: Set the key mykey
  sap.sap_operations.hdbuserstore:
    key: mykey
    env: "localhost:30113"
    username: myuser
    password: mypassword

# NOTES:
# Variable binary_path is required if hdbuserstore command cannot be found in PATH environment variable.
# If running ansible module using become directive with <hanasid>adm user and flag '-i' (interactive - meaning load all environment for the user)
# ansible modules fail. This is due to the fact that <hanasid>adm user sets environment variables PYTHONHOME and PYTHONPATH (to use HANA python,
# not platform python) that confuse ansible.
#
# In that case hdbuserstore command will not be in PATH environment variable for <hanasid>adm user and I(binary_path) has to be provided.
#
# There are several workaround around this unplesant situation. One is recommended.
#
# Workaround 1 (recommended)
#
# Run hdbsuserstore module with <hanasid>adm user with '-i' (interactive) flag like so
- name: Set the key mykey
  sap.sap_operations.hdbuserstore:
    key: mykey
    env: "localhost:30113"
    username: myuser
    password: mypassword
  become: true
  become_user: <hanasid>adm
  become_flags: -i
  vars:
    ansible_python_interpreter: "/usr/libexec/platform-python -E"

# Option '-E' for python interpreter will ignore all PYTHON\* environment variables, so ansible will run platform python without any problems.
# Variable I(ansible_python_interpreter) have to be set to value "/usr/libexec/platform-python -E" on all RHEL versions for any ansible module
# execution when becoming <hanasid>adm user with flag '-i'.
#
# ansible_python_interpreter: "/usr/libexec/platform-python -E" can be set at task level (as above), at play level like so
# Or be set as host variable either in inventory file or as task in playbook:
- name: Converge
  hosts: all
  gather_facts: false
  become: true
  become_user: hanadm
  become_flags: -i
  vars:
    ansible_python_interpreter: python -E

  tasks:
    - name: Environment for SAP HANA
      set_fact:
        ansible_python_interpreter: "/usr/libexec/platform-python -E"

# Workaround 2
#
# Do not use interactive flag when becoming <hanasid>adm user.
- name: Set the key mykey
  sap.sap_operations.hdbuserstore:
    key: mykey
    env: "localhost:30113"
    username: myuser
    password: mypassword
    binary_path: "/usr/sap/HAN/SYS/exe/hdb"
  become: true
  become_user: <hanasid>adm

# In that case hdbuserstore command will not be in PATH environment variable for <hanasid>adm user and I(binary_path) has to be provided.
#
# Workaround 3
#
# Do not use interactive flag when becoming <hanasid>adm user. But do not want to provide value for variable I(binary_path).
#
# In that case value for I(binary_path) can be extracted from HANA parameter DIR_EXECUTABLE that one can get with I(parameter_info) module:
- name: Get DIR_EXECUTABLE
  sap.sap_operations.parameter_info:
    instance_number: "00"
    name: DIR_EXECUTABLE
  become: true
  become_user: <hanasid>adm
  register: __DIR_EXECUTABLE

- name: Set the key mykey
  sap.sap_operations.hdbuserstore:
    key: mykey
    env: "localhost:30113"
    username: myuser
    password: mypassword
    binary_path: "{{ __DIR_EXECUTABLE.parameter_value[0] }}"
  become: true
  become_user: <hanasid>adm
"""

RETURN = r"""
key:
    description: HDB key name
    type: str
    returned: always
    sample: mykey
env:
    description: HDB env name
    type: str
    returned: When state is C(present)
    sample: myenv
username:
    description: HDB username for key
    type: str
    returned: When state is C(present)
    sample: myusername
"""

import os

from ansible.module_utils.basic import AnsibleModule


def ensure_created(module):
    binary = os.path.join(module.params.get("binary_path"), "hdbuserstore")
    key = module.params.get("key")
    env = module.params.get("env")
    username = module.params.get("username")
    password = module.params.get("password")
    force = module.params.get("force")
    return_key = {"key": key, "env": env, "username": username}

    # Fetch the key:
    rc, stdout, _err = module.run_command(args=[binary, "List", key])
    if rc not in [0, 100]:
        module.fail_json(msg="Failed to execute list: {0}".format(stdout))

    if rc == 0 and not force:
        return False, stdout, return_key

    # Store the key:
    if not module.check_mode:
        rc, stdout, _err = module.run_command(
            args=[binary, "Set", key, env, username, password]
        )
        if rc != 0:
            module.fail_json(msg="Failed to execute Set: {0}".format(stdout))

    return True, stdout, return_key


def ensure_absent(module):
    binary = os.path.join(module.params.get("binary_path"), "hdbuserstore")
    key = module.params.get("key")

    rc, stdout, _err = module.run_command(args=[binary, "List", key])
    if not module.check_mode and rc == 0:
        rc, _out, _err = module.run_command(args=[binary, "Delete", key])

    if rc not in [0, 100]:
        module.fail_json(msg="Failed to execute delete: {0}".format(stdout))

    return rc == 0, stdout, {"key": key}


def main():
    module_args = dict(
        state=dict(
            type="str",
            choices=[
                "present",
                "absent",
            ],
            default="present",
        ),
        key=dict(type="str", required=True, no_log=False),
        env=dict(type="str"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        binary_path=dict(type="str", default=""),
        force=dict(type="bool", default=False),
    )

    result = dict(changed=False)
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ["state", "present", ["env", "username", "password"]],
        ],
    )

    state = module.params.get("state")
    if state == "present":
        result["changed"], result["stdout"], return_key = ensure_created(module)
    else:
        result["changed"], result["stdout"], return_key = ensure_absent(module)

    result.update(return_key)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
