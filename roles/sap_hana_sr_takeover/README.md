<!-- BEGIN Title -->
# sap_hana_sr_takeover Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_hana_sr_takeover` executes Takeover operation on SAP HANA System with configured SAP HANA System Replication (HSR).
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

## Prerequisites
<!-- BEGIN Prerequisites -->
HSR must be configured correctly and `ACTIVE` when executing this Ansible Role.

- HSR can be configured using `community.sap_install.sap_ha_install_hana_hsr` role.

**NOTE:** This role will fail gracefully when invalid replication is detected, but it might not catch all irregularities.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert and validate all variables.
2. Detect if SAP HANA System is running. 
3. Detect existing replication and validate results
4. Execute Takeover operation on target Primary node.
5. Stop SAP HANA on the source Primary node, if it is running.
6. Register the source Primary as a new Secondary Node.
7. Start SAP HANA on the new Secondary Node and show summary.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of takeover operation from `h02hana0` in `hana_primary` group to `h02hana1` in `hana_secondary` group.

```yaml
- name: Ansible Play for SAP HANA SR Takeover
  hosts: hana_primary, hana_secondary
  become: true
  any_errors_fatal: true
  tasks:

    - name: Execute Ansible Role sap_hana_sr_takeover
      ansible.builtin.include_role:
        name: community.sap_operations.sap_hana_sr_takeover
      vars:
        sap_hana_sr_takeover_primary: 'h02hana1'
        sap_hana_sr_takeover_sid: 'H02'
        sap_hana_sr_takeover_instance_number: '90'
```
<!-- END Execution Example -->

## Testing
This Ansible Role has been tested in following scenarios.
Operating systems:

 - SUSE Linux Enterprise Server for SAP applications 16 (SLE4SAP)

SAP Products:

- SAP HANA 2.0 SP08

**NOTE:** SAP has introduced a new parameter in HANA 2.0 SPS07, that can fail takeover when replication is not ACTIVE.<br>
See SAP Note 3484530 - Takeover Fails With Error Message: not all volumes are replicated initially, cannot proceed.

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
### sap_hana_sr_takeover_primary
- _Type:_ `string`

Name of existing Secondary Node that will Takeover current Primary Node.<br>
This name must exist in playbook hosts.

### sap_hana_sr_takeover_sid
- _Type:_ `string`

SAP HANA Database System ID (SID) in capital letters.

### sap_hana_sr_takeover_instance_number
- _Type:_ `string`

SAP HANA Database Instance Number.

### sap_hana_sr_takeover_replication_mode
- _Type:_ `string`

SAP HANA System Replication mode that will be applied during registration.<br>
Available values: `sync`, `syncmem`, `async`

### sap_hana_sr_takeover_operation_mode
- _Type:_ `string`

SAP HANA System Replication Operation mode that will be applied during registration.<br>
Available values: `delta_datashipping`, `logreplay`, `logreplay_readaccess`
<!-- END Role Variables -->
