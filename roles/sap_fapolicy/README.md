# sap_fapolicy Ansible Role

Ansible role for updating fapolicy entries based on SAP instance numbers

- **Generic** - use the `generic` option to update entries directly by providing a list of users
- **SAP NW** - use the `nw` option to update SAP NW entries
- **SAP HANA** - use the `hana` option to update SAP HANA entries

## Overview

Fapolicy entries will be updated to allow access to the following directories 
  - "/hana/"
  - "/sapmnt/"
  - "/usr/sap/"
  - "/software/"
  - "/var/tmp/"
  - "/tmp/"

![](/docs/diagrams/sap_fapolicy_workflow.svg)

### Variables

| **Variable**        | **Info**                                    | **Default** | **Required**      |
| :---                | :---                                        | :---        | :---              |
| sap_fapolicy_type   | 'generic' / 'nw' / 'hana'                   | 'generic'   | yes               |
| sap_fapolicy_user   | Unix user to include in fapolicy entries    | <none>      | if 'generic'      |
| sap_fapolicy_sid    | SAP system SID                              | <none>      | if 'nw' / 'hana'  |

### Input and Execution

- Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-fapolicy-update.yml"
    ```

- Sample playbook using `generic` option

    ```yaml
    ---
    - hosts: all
      become: true
      
      vars:
        sap_fapolicy_user_generic_list:
          - "root"
          - "sapadm"
          - "uuidd"
      
      tasks:

      # Update fapolicy for generic users
      - name: Fapolicy Update - generic
        vars:
          sap_fapolicy_type: "generic"
        include_role: 
          name: community.sap_operations.sap_fapolicy
        loop: "{{ sap_fapolicy_user_generic_list }}"
        loop_control:
          loop_var: sap_fapolicy_user
    ```

- Sample playbook using `sap_facts` module to get all SAP systems in the host

    ```yaml
    ---
    - hosts: all
      become: true
      
      tasks:

      - name: Run sap_facts module to gather SAP facts
        community.sap_operations.sap_facts:
            param: "all"
        register: sap_facts_register

      # Update fapolicy for SAP users        
      - name: Fapolicy Update - SAP Users
        vars:
          sap_fapolicy_sid: "{{ item.Type }}"
          sap_fapolicy_type: "{{ item.Type }}"
        include_role: 
          name: community.sap_operations.sap_fapolicy
        loop: "{{ sap_facts_register.sap_facts }}"
    ```
