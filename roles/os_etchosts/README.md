# os_etchosts Ansible Role

Ansible role for updating /etc/hosts

## Overview

### Variables

| **Variable**                  | **Info**                                                               | **Default**  | **Required** |
| :---                          | :---                                                                   | :---         | :---         |
| os_etchosts_entries           | List of ip addresses and hostnames (please see sample)                 | <none>       | yes          |
| os_etchosts_fqdn              | Fully qualified domain name                                            | <none>       | yes          |
| os_etchosts_delimiter         | Delimiter between the hosts entries                                    | "\t"         | no           |

### Input and Execution

- Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-etchosts-update.yml"
    ```

- Sample playbook

    ```yaml
    ---
    - hosts: all
      become: true
      vars:
        sap_os_tools_etchosts_entries:
          - "10.0.0.1 hana01-lb"
          - "10.0.0.2 hana02-lb"
          - "10.0.1.1 s4hana01-ci"
          - "10.0.1.2 s4hana01-app"
        sap_os_tools_etchosts_fqdn: "poc.cloud"
      roles:
        - { role: community.sap_operations.os_etchosts }
    ```

- Sample result

    ```console
    cat /etc/hosts
    10.0.0.1  hana01-lb.poc.cloud hana01-lb
    10.0.0.2  hana02-lb.poc.cloud hana02-lb
    10.0.1.1  s4hana01-ci.poc.cloud s4hana01-ci
    10.0.1.2  s4hana01-app.poc.cloud s4hana01-app
    ```
