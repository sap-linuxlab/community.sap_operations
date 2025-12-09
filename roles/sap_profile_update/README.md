<!-- BEGIN Title -->
# sap_profile_update Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_profile_update` manages parameters in SAP profile files.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- BEGIN Execution -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert all variables.
2. Validate all variables against target host and its profiles.
3. Manage parameters in profiles.
4. Add audit comment in profile file if change occurred.

#### Examples of audit comments
```bassh
# 2025-12-09 09:58:34 'rdisp/wp_no_btc' added with value '6' by Ansible Role community.sap_operations.sap_profile_update.
# 2025-12-09 10:00:25 'rdisp/wp_no_btc' changed from '6' to '7' by Ansible Role community.sap_operations.sap_profile_update.
# 2025-12-09 10:01:04 'rdisp/wp_no_btc' commented out by Ansible Role community.sap_operations.sap_profile_update.
```

<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of changing the parameter `rdisp/wp_no_btc` for one System `B01`.
```yaml
- name: Ansible Play for SAP Profile update
  hosts: host
  become: true
  tasks:
    - name: Execute Ansible Role sap_profile_update
      ansible.builtin.include_role:
        name: community.sap_operations.sap_profile_update
      vars:
        sap_profile_update_definitions:
          - sid: 'B01'
            profiles:
              - type: 'instance'
                instance_number: '01'
                parameters:
                  - name: 'rdisp/wp_no_btc'
                    value: '10'
```

Example of resizing instances for multiple Systems on one host with custom path to profiles.
```yaml
- name: Ansible Play for SAP Profile update
  hosts: host
  become: true
  tasks:
    - name: Execute Ansible Role sap_profile_update
      ansible.builtin.include_role:
        name: community.sap_operations.sap_profile_update
      vars:
        sap_profile_update_definitions:
          - sid: 'B01'
            profiles:
              - type: 'instance'
                instance_number: '10'
                path: '/usr/sap/B01/SYS/profile/B01_D10_b01hana_custom'
                parameters:
                  - name: 'PHYS_MEMSIZE'
                    value: '12880'
          - sid: 'B02'
            profiles:
              - type: 'instance'
                instance_number: '20'
                path: '/sapmnt/B02/profile/B02_D20_b02hana_custom'
                parameters:
                  - name: 'PHYS_MEMSIZE'
                    value: '12880'
```

Example of removing obsolete parameter for one System `B01`.
```yaml
- name: Ansible Play for SAP Profile update
  hosts: host
  become: true
  tasks:
    - name: Execute Ansible Role sap_profile_update
      ansible.builtin.include_role:
        name: community.sap_operations.sap_profile_update
      vars:
        sap_profile_update_definitions:
          - sid: 'B01'
            profiles:
              - type: 'default'
                parameters:
                  - name: 'icf/user_recheck'
                    state: 'absent'
```
<!-- END Execution Example -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### sap_profile_update_definitions
- _Type:_ `list` of type `list` of type `dict`

This variable defines all SAP systems, profiles, and parameters to be managed or updated on the current host.</br>
It is structured as a list of dictionaries, where each top-level dictionary defines a specific SAP System ID (SID). </br>

Key fields:
* `sid`: The 3-letter SAP System ID (e.g., 'PRD', 'QAS').
* `profiles`: A list of profile files to manage for this SID.
  * `type`: `default` or `instance`. Used for dynamic path calculation.
  * `instance_number`: Required if type is `instance` (e.g., '00', '10').
  * `path`: (Optional) Explicit file path to the profile. If omitted, the path
          will be constructed based on 'sid', 'type', and discovered facts.
  * `parameters`: The list of parameters to apply to this profile file.
    * `name`: Parameter name to update (e.g., `ssl/ciphersuites`).
    * `value`: New value for the parameter. Not required if state is `absent`.
    * `state`: (Optional) `present` (default) or `absent`.

Example:
```yaml
sap_profile_update_definitions:
  - sid: 'B01'
    profiles:
      - type: 'default'
        parameters:
          - name: 'ssl/ciphersuites'
            value: '135:PFS:HIGH::EC_P256:EC_HIGH'
          - name: 'rdisp/TRACE_LOGGING'
            state: 'absent'
      - type: 'instance'
        instance_number: '10'
        path: '/usr/sap/B01/SYS/profile/B01_D10_b01hana_custom'
        parameters:
          - name: 'rdisp/wp_no_btc'
            value: '6'
          - name: 'rdisp/wp_no_vb2'
            value: '2'
  - sid: 'B02'
    profiles:
      - type: 'default'
        path: '/sapmnt/B02/profile/DEFAULT.PFL'
        parameters:
          - name: 'ssl/ciphersuites'
            value: '135:PFS:HIGH::EC_P256:EC_HIGH'
```

### sap_profile_update_restart_sapstartsrv
- _Type:_ `bool`<br>
- _Default:_ `false`<br>

Enable this variable to restart sapstartsrv service after updating parameters.</br>
This is applicable only for 'instance' type profiles as DEFAULT.PFL does not have sapstartsrv.</br>
This role does not manage restart of complete SAP System,
and this parameter is limited to `sapcontrol -nr XX -function RestartService` only.</br>
<!-- END Role Variables -->
