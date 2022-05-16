#!/usr/bin/python
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from pyrfc import (ABAPApplicationError, ABAPRuntimeError, CommunicationError,
                   Connection, LogonError)

from ..module_utils.pyrfc_handler import get_connection

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sap_pyrfc
short_description: Execute RFC calls
version_added: "0.1.0"
description: This module executes RFC calls.
options:
    function:
        description: The system ID.
        type: str
        required: true
    parameters:
        description: The parameters for the function.
        type: dict
        required: true
    connection:
        description: The connection parameters.
        type: dict
        required: true
'''

EXAMPLES = '''
sap_pyrfc:
  function: STFC_CONNECTION
  parameters:
    REQUTEXT: "Hello SAP!"
  connection:
    ashost: s4hana.poc.cloud
    sysid: TDT
    sysnr: "01"
    client: "400"
    user: DDIC
    passwd: Password1
    lang: EN
'''


def main():
    argument_spec = dict(function=dict(required=True, type='str'),
                         parameters=dict(required=True, type='dict'),
                         connection=dict(required=True, type='dict'),
                         )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    function = module.params.get('function')
    func_params = module.params.get('parameters')
    conn_params = module.params.get('connection')

    # Validate connection fields
    required_conn_fields = ['ashost', 'sysnr', 'client', 'user', 'passwd']
    missing = [f for f in required_conn_fields if f not in conn_params]
    if missing:
        msg = 'Missing required login fields: %s' % ', '.join(missing)
        module.fail_json(msg=msg)

    # Check mode
    if module.check_mode:
        msg = "function: %s; params: %s; login: %s" % (function, func_params, conn_params)
        module.exit_json(msg=msg, changed=True)

    try:
        conn = get_connection(module, conn_params)
        result = conn.call(function, **func_params)
        module.exit_json(changed=True, result=result)
    except CommunicationError as e:
        msg = "Could not connect to server: %s" % e.message
        module.exit_json(failed=True, msg=msg)
    except LogonError as e:
        msg = "Could not log in: %s" % e.message
        module.exit_json(failed=True, msg=msg)
    except (ABAPApplicationError, ABAPRuntimeError) as e:
        msg = "ABAP error occurred: %s" % e.message
        module.exit_json(failed=True, msg=msg)

    module.exit_json(failed=False)


if __name__ == '__main__':
    main()
