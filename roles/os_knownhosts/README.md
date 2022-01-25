# os_knownhosts Ansible Role

Ansible role for updating known hosts file `/.ssh/known_hosts`. This is usually used on the Ansible control / central node.

## Overview


### Input and Execution

Just execute the role, no need to set vafriable inputs. Put the target host(s) in the inventory `-i` argument 

- Sample execution:

    ```bash
    ansible-playbook -i "host_you_want_to_update," sap-knownhosts-update.yml"
    ```

- Sample playbook

    ```yaml
    ---

    - name: Store known hosts of 'all' the hosts in the inventory file
      hosts: localhost
      connection: local
      roles:
        - { role: community.sap_operations.os_knownhosts }

    ```
