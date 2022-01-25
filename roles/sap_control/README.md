# sap_control Ansible Role

This Ansible Role executes basic SAP administration tasks on Linux operating systems.

## Ansible Role Overview

This Ansible Role executes basic SAP administration tasks on Linux operating systems, including:
- Start/Stop/Restart of SAP HANA Database Server
- Start/Stop/Restart of SAP NetWeaver Application Server
- Multiple Automatic discovery and Start/Stop/Restart of SAP HANA Database Server or SAP NetWeaver Application Server

## Example execution

### Example Playbook

```yaml
- hosts: sap_servers
  roles:
    - { role: community.sap_operations.sap_control }
```

### Example Inputs

- Using restart all
  ```yaml
  sap_control_function: "restart_all_sap"
  ```
- Using a specific SAP SID
  ```yaml
  sap_control_function: "stop_sap_hana"
  sap_sid: "HDB"
  ```

## Ansible Role Requirements and Dependencies

### Operating System

This role has been tested with RHEL, and is designed for Linux operating systems.

This role has not been tested and amended for SAP NetWeaver Application Server instantiations on IBM AIX or Windows Server.

Assumptions for executing this role include:
- Instances of either SAP HANA Database Server or SAP NetWeaver Application Server are installed to the target host
- Relevent OS Packages for SAP are installed
- Registered OS License and OS Package repositories are available (from the relevant content delivery network of the OS vendor)

### SAP software instances

This role has been tested with SAP NetWeaver Application Server 7.53 and SAP HANA Database Server 2.0 SPS04 rev 20.

This role has not been tested with other versions of SAP NetWeaver Application Server, however it should work for all versions above SAP NetWeaver Application Server 7.50.

This role has not been tested with other versions of SAP HANA Database Server, however it should work for all versions above SAP HANA 2.0 SPS00.

Assumptions for executing this role include:
- Installations used default `/usr/sap` and `/sapmnt` directories
- Installations for SAP HANA used default `/hana/shared` directory

## Ansible Role Variables

| **variable** | **info** | **required** |
| :--- |:--- | :--- |
| `SID` | SAP system SID | no, only if you are targetting a single SAP system|
| `nowait` | Default: `false` | no, use only when absolutely sure! This will bypass all waiting and ignore all necessary steps for a graceful stop / start|
| `sap_control_function` | Function to execute:<br/><ul><li>`restart_all_sap`</li><li>`restart_all_nw`</li><li>`restart_all_hana`</li><li>`restart_sap_nw`</li><li>`restart_sap_hana`</li><li>`stop_all_sap`</li><li>`start_all_sap`</li><li>`stop_all_nw`</li><li>`start_all_nw`</li><li>`stop_all_hana`</li><li>`start_all_hana`</li><li>`stop_sap_nw`</li><li>`start_sap_nw`</li><li>`stop_sap_hana`</li><li>`start_sap_hana`</li></ul> | yes, only this is required to detect the Instance Number which is used with SAP Host Agent `sapcontrol` CLI<br/><br/><br/>_Note: Executions using `all` will automatically detect any System IDs and corresponding Instance Numbers_ |

## Ansible Role workflow and structure

The following diagram demonstrates the Ansible Role workflow, where the variable `sap_control_function` is set with different values (such as **"restart_all"**) and will perform different sequence of SAP Host Agent `sapcontrol` CLI functions.

![sap_control](/docs/diagrams/workflow_role_sap_control.svg)
