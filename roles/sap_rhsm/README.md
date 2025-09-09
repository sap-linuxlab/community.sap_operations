<!-- BEGIN Title -->
# sap_rhsm Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_rhsm` is used to register managed node with Red Hat Operating System. 
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:
- Supported Operating System: Red Hat
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->
### Example
<!-- BEGIN Execution Example -->
Register operating system.
```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Register operating system
      ansible.builtin.include_role:
        name: community.sap_operations.sap_rhsm
      vars:
        sap_rhsm_function: "register"
        sap_rhsm_username: "my_rhel_user"
        sap_rhsm_password: "my_rhel_password"
        sap_rhsm_pool_id: "8x8x8x8x8x88x8x8x8x8x8x8x8x"
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
```

Refresh operating system.
```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Register operating system
      ansible.builtin.include_role:
        name: community.sap_operations.sap_rhsm
      vars:
        sap_rhsm_function: "refresh"
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- SAP LinuxLab
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### sap_rhsm_function
- **Required**<br>
- _Type:_ `string`<br>

Select function to execute. Options: 'register', 'refresh'.<br>

### sap_rhsm_username
- _Type:_ `string`<br>

The username for registration.<br>
Mandatory for execution with `sap_rhsm_function` set to `register`.<br>

### sap_rhsm_password
- _Type:_ `string`<br>

The password for user defined in `sap_rhsm_username`.<br>
Mandatory for execution with `sap_rhsm_function` set to `register`.<br>

### sap_rhsm_pool_id
- _Type:_ `string`<br>

The pool ID to attach to during registration.<br>
Mandatory for execution with `sap_rhsm_function` set to `register`.<br>

### sap_rhsm_repos
- _Type:_ `list`<br>

The optional list of repositories to enable.<br>r>

### sap_rhsm_packages
- _Type:_ `list`<br>

The optional list of packages to install.<br>
<!-- END Role Variables -->
