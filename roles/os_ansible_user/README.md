# os_ansible_user Ansible Role

Ansible role for creating an ansible user for your managed systems

## Prerequisites

- Create your Ansible user in your Ansible command host
- Generate a key via `ssh-keygen`
- > **_Note:_**  Highly recommended that you do this manually and not be part of the automation for security reasons
- A userid that has sudo privileges (or direct root) to create the Ansible user
  -   Provide the user in your `vars`  
        ```yaml
        ansible_user: admin_user
        ansible_password: your_password
        ansible_sudo_pass: your_password
        ```

## Overview

### Variables

| **Variable**                    | **Info**                                                               | **Default**      | **Required** |
| :---                            | :---                                                                   | :---             | :---         |
| os_ansible_user_userid          | Ansible user to be created                                             | <none>           | yes          |
| os_ansible_user_password        | Password of the Ansible user to be created                             | <none>           | yes          |
| os_ansible_user_uid             | Ansible user Unix user id                                              | <none>           | yes          |
| os_ansible_user_gid             | Ansible user Unix group id                                             | <none>           | yes          |
| os_ansible_user_keyfile         | Key filename found in `~./ssh/`                                        | "id_ecdsa.pub"   | yes          |
| os_ansible_user_force_recreate  | Forcefully recreate user by deleting existing user first               | "yes"            | no           |

### Input and Execution

- Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," os-create-ansible-user.yml"
    ```

- Sample playbook

    ```yaml
    ---
    - hosts: all
      become: true
      vars:
        ansible_user: admin_user
        ansible_password: your_password
        ansible_sudo_pass: your_password
        os_ansible_user_userid: ansadm
        os_ansible_user_password: 'my_password'
        os_ansible_user_uid: 1010
        os_ansible_user_gid: 1010
        os_ansible_user_keyfile: id_ecdsa.pub 
      roles:
        - { role: community.sap_operations.os_ansible_user }
    ```
