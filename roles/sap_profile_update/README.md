# sap_profile_update Ansible Role

Ansible role for updating SAP profiles

- **DEFAULT** profile
- **Instance** profile

## Overview

### Variables

| **Variable**                                  | **Info**                                             | **Default** | **Required** |
| :---                                          | :---                                                 | :---        | :---         |
| sap_update_profile_sid                        | SAP system SID                                       | <none>      | yes          |
| sap_update_profile_instance_nr                | SAP system instance number                           | <none>      | yes          |
| sap_update_profile_default_profile_params     | List of parameters to update in the default profile  | <none>      | no           |
| sap_update_profile_instance_profile_params    | List of parameters to update in the instance profile | <none>      | no           |

### Input and Execution

- Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-profile-update.yml -e "@input_file.yml"
    ```

- Sample direct input

    ```yaml
    sap_update_profile_sid: "S20"
    sap_update_profile_instance_nr: "00"
    sap_update_profile_default_profile_params:
      - sapgui/user_scripting = TRUE
      - ssl/ciphersuites = 135:PFS:HIGH::EC_P256:EC_HIGH
      - ssl/client_ciphersuites = 150:PFS:HIGH::EC_P256:EC_HIGH
    sap_update_profile_instance_profile_params:
      - PHYS_MEMSIZE = 32768
      - icm/server_port_0 = PROT=HTTP,PORT=80$$,PROCTIMEOUT=600,TIMEOUT=3600
      - icm/server_port_1 = PROT=HTTPS,PORT=443$$,PROCTIMEOUT=600,TIMEOUT=3600
      - icm/server_port_2 = PROT=SMTP,PORT=25$$,PROCTIMEOUT=120,TIMEOUT=120
    ```

- Sample playbook using `sap_facts` module to get all SAP systems in the host

    ```yaml
    ---
    - hosts: all
      become: true

      vars:

        sap_update_profile_default_profile_params:
            - sapgui/user_scripting = TRUE
            - ssl/ciphersuites = 135:PFS:HIGH::EC_P256:EC_HIGH
            - ssl/client_ciphersuites = 150:PFS:HIGH::EC_P256:EC_HIGH
        sap_update_profile_instance_profile_params:
            - PHYS_MEMSIZE = 32768
            - icm/server_port_0 = PROT=HTTP,PORT=80$$,PROCTIMEOUT=600,TIMEOUT=3600
            - icm/server_port_1 = PROT=HTTPS,PORT=443$$,PROCTIMEOUT=600,TIMEOUT=3600
            - icm/server_port_2 = PROT=SMTP,PORT=25$$,PROCTIMEOUT=120,TIMEOUT=120

      tasks:
        
        # Gather SAP facts of the host
        - name: Run sap_facts module to gather SAP facts
          community.sap_operations.sap_facts:
            param: "all"
          register: sap_facts_register

        # Update all the profiles of the SAP systems in the host      
        - name: Update all the profiles of the SAP systems in the host
          vars:
            sap_update_profile_sid: "{{ item.SID }}"
            sap_update_profile_instance_nr: "{{ item.InstanceNumber }}"
          include_role: 
            name: community.sap_operations.sap_profile_update
          loop: "{{ sap_facts_register.sap_facts }}"
          when:
            - item.Type == 'nw'
    ```
