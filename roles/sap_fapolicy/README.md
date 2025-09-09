<!-- BEGIN Title -->
# sap_fapolicy Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_rhsm` is used to update fapolicy configuration for SAP Systems. 
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
Configuration with `sap_fapolicy_type` set to `generic`.
```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Configure fapolicy
      ansible.builtin.include_role:
        name: community.sap_operations.sap_fapolicy
      vars:
        sap_fapolicy_type: "generic"
```

Configuration for all SAP Systems on managed node.
```yaml
---
- hosts: all
  become: true
  tasks:
    - name: Run sap_facts module to gather SAP facts
      community.sap_operations.sap_facts:
        param: "all"
      register: sap_facts_register

    - name: Fapolicy Update - SAP Users
      vars:
        sap_fapolicy_sid: "{{ item.Type }}"
        sap_fapolicy_type: "{{ item.Type }}"
      ansible.builtin.include_role:
        name: community.sap_operations.sap_fapolicy
      loop: "{{ sap_facts_register.sap_facts }}"
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
### sap_fapolicy_type
- **Required**<br>
- _Type:_ `string`<br>
- _Default:_ `generic`<br>

Select fapolicy type to configure. Options: `generic`, `nw`, `hana`.<br>

### sap_fapolicy_user
- _Type:_ `string`<br>

The user for fapolicy configuration.<br>
Mandatory when `sap_fapolicy_type` is set to `generic`.<br>
Automatically set as `sap_fapolicy_sid` + 'adm' if `sap_fapolicy_type` is `nw` or `hana`.<br>

### sap_fapolicy_uid
- _Type:_ `string`<br>

The User ID of provided user `sap_fapolicy_user`.<br>
Automatically set if `sap_fapolicy_user` or `sap_fapolicy_sid` is provided.<br>

### sap_fapolicy_sid
- _Type:_ `string`<br>

The SAP System ID (3 letter String).<br>
Mandatory when `sap_fapolicy_type` is set to `nw` or `hana`.<br>

### sap_fapolicy_directory_list
- _Type:_ `list`<br>
- _Default:_ `['/hana/', '/sapmnt/', '/usr/sap/', '/software/', '/var/tmp/', '/tmp/']`<br>

The list of directories for fapolicy configuration.<br>

### sap_fapolicy_rules_header
- _Type:_ `string`<br>
- _Default:_ `# Allow rules for SAP directories`<br>

The header line to add to fapolicy rules.<br>
<!-- END Role Variables -->
