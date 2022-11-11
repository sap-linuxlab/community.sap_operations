sap_hana_sr_takeover
=====================

This role can be used to ensure, control and change SAP HANA System Replication

Requirements
------------

This role requires SAP HANA System Replication configure, e.g. using the community.sap_install.sap_ha_install_hana_hsr role

Role Variables
--------------

The follwoing variables are mandatory for running this role unless a default value is specified

| Variable Name                       | Description 		                                  |
|-------------------------------------|-----------------------------------------------------------|
| sap_hana_sr_takeover_primary        | Server to become the primary server                       |
| sap_hana_sr_takeover_secondary      | Server to register as secondary. The role can be run twice if more than one secondary is needed by looping over this variable |
| sap_hana_sr_takeover_sitename       | Name of the site being registered as secondary i          |
| sap_hana_sr_takeover_rep_mode       | HANA replication mode (defaults to sync if not set)       |
| sap_hana_sr_takeover_hsr_oper_mode  | HANA replication operation mpode (defaults to logreplay ) |
| sap_hana_sid                        | HANA SID                                                  |
| sap_hana_instance_number            | HANA instance number


Dependencies
------------

`sap_hana_sid` and `sap_hana_instance_number` may already be set or used in other roles

Example Playbook
----------------

If you have `hana1` and `hana2` configured for SAP HSR with SID RHE and instance 00 the following playbook
ensures that `hana1` is the primary and `hana2` is the secondary

The role will fail if `hana1` is not configured for system replication (mode: none in `hdbnsutil -sr_state`).
`hana1` needs to be primary or secondary in sync

The role will do nothing if `hana1` is the primary and `hana2` is the secondary.

It also ensures that the secondary HANA DB is started

```yaml
- name: Ensure hana1 is primary
  hosts: hanas
  become: true
  tasks:
    - name: Switch to hana1
      include_role:
        name: community.sap_operations.sap_hana_sr_takeover
      vars:
        sap_hana_sr_takeover_primary: hana2
        sap_hana_sr_takeover_secondary: hana1
        sap_hana_sr_takeover_sitename: DC01
        sap_hana_sid: "RHE"
        sap_hana_instance_number: "00"
```


License
-------
Apache-2.0
