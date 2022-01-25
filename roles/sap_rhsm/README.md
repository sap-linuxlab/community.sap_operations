# sap_rhsm Ansible Role

Ansible role for RHEL registration / refresh

## Overview

### Variables

| **Variable**            | **Info**                                  | **Default**  | **Required** |
| :---                    | :---                                      | :---         | :---         |
| sap_rhsm_function       | 'register' or 'refresh'                   | 'register'   | yes          |
| sap_rhsm_username       | RHEL User for access.redhat.com           | <none>       | yes          |
| sap_rhsm_password       | Password for access.redhat.com            | <none>       | yes          |
| sap_rhsm_pool_id        | Subscription pool id                      | <none>       | yes          |
| sap_rhsm_repos          | List of repositories to enable            | <none>       | yes          |
| sap_rhsm_packages       | List of packages to install               | <none>       | yes          |

### Input and Execution

- Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-rhsm-register.yml"
    ```

- Sample playbook
  - Register
    ```yaml
    ---
    - hosts: all
      become: true
      vars:
        sap_rhsm_function: "register"
        sap_rhsm_username: "my_rhel_user"
        sap_rhsm_password: "my_rhel_password"
        sap_rhsm_pools_id: "8x8x8x8x8x88x8x8x8x8x8x8x8x"
        sap_rhsm_repos:
          - rhel-8-for-x86_64-baseos-e4s-rpms
          - rhel-8-for-x86_64-appstream-e4s-rpms
          - rhel-8-for-x86_64-sap-solutions-e4s-rpms
          - rhel-8-for-x86_64-sap-netweaver-e4s-rpms
          - rhel-8-for-x86_64-highavailability-e4s-rpms
          - ansible-2-for-rhel-8-x86_64-rpms
        sap_rhsm_packages:
          - yum-utils
          - nfs-utils
      roles:
        - { role: community.sap_operations.sap_rhsm }
    ```
  - Refresh
    ```yaml
    ---
    - hosts: all
      become: true
      vars:
        sap_rhsm_function: "refresh"
      roles:
        - { role: community.sap_operations.sap_rhsm }
    ```
- Sample result

    ```console
    cat /etc/hosts
    10.0.0.1  hana01-lb.poc.cloud hana01-lb
    10.0.0.2  hana02-lb.poc.cloud hana02-lb
    10.0.1.1  s4hana01-ci.poc.cloud s4hana01-ci
    10.0.1.2  s4hana01-app.poc.cloud s4hana01-app
    ```
