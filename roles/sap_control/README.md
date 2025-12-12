<!-- BEGIN Title -->
# sap_control Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_control` executes predefined that cover range of SAP administration tasks, including:
- Start/Stop/Restart of SAP HANA Database Server.
- Start/Stop/Restart of SAP NetWeaver Application Server.
- Start/Stop/Restart/Update of SAP Netweaver System.
<!-- END Description -->

<!-- BEGIN Disclaimer -->
## Disclaimer
> **IMPORTANT:** This role is designed to perform administrative actions on SAP systems, such as starting and stopping instances.  
> Misuse of this role, especially in production environments, can lead to system downtime and potential data loss.  
> It is crucial to understand the function you are executing and its impact on your SAP landscape.  
> Always test in non-production environments before applying to production systems. Use with caution.  
<!-- END Disclaimer -->

<!-- BEGIN Dependencies -->
## Dependencies
> This is optional dependency, active only when the variable `sap_control_use_sap_system_facts` is set to `true`.
- `community.sap_libs`
    - Modules:
        - `sap_system_facts`
  - This collection is part of main Ansible package.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
This Ansible Role assumes that SAP Netweaver and HANA are installed in standard locations.
- `/sapmnt` and `/usr/sap` for SAP Netweaver
- `/shared/hana/` and `/usr/sap` for SAP Netweaver
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
Primary variable is `sap_control_function` and it drives all logic of this role.  
The function names are constructed using the pattern: [`ACTION`]_[`SCOPE`]_[`TARGET`]

`ACTION`: The operation to perform.
- Process-level: `start`, `stop`, `restart`
- System-level (asynchronous): `startsystem`, `stopsystem`, `restartsystem`, `updatesystem`
> `system` functions leave everything to `sapcontrol` and check in asynchronous mode if it is completed.

`SCOPE`: The instances the action applies to.
- `all`: Applies to all detected instances of the target type.
- `sap`: Applies to a single instance specified by `sap_control_sid`.

`TARGET`: The type of SAP system.
- `hana`: SAP HANA instances.
- `nw`: SAP NetWeaver instances.
- `sap`: All SAP instances (both `hana` and `nw`).

Following functions are available:
| Target and Scope | Start | Stop | Restart | Other |
| --- | --- | --- | --- | --- |
| HANA | start_all_hana<br>start_sap_hana | stop_all_hana<br>stop_sap_hana | restart_all_hana<br>restart_sap_hana | | |
| Netweaver | start_all_nw<br>start_sap_nw | stop_all_nw<br>stop_sap_nw | restart_all_nw<br>restart_sap_nw | | |
| Combined | start_all_sap | stop_all_sap | restart_all_sap | | |
| System | startsystem_all_nw<br>startsystem_sap_nw | stopsystem_all_nw<br>stopsystem_sap_nw | restartsystem_all_nw<br>restartsystem_sap_nw | updatesystem_all_nw<br>updatesystem_sap_nw |
<!-- END Execution -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert and validate all variables.
2. Detect existing SAP System IDs and Instances on host.
   - Alternatively collection this information using `community.sap_libs.sap_system_facts` module if the variable `sap_control_use_sap_system_facts` is set to `true`.
3. Prepare list of commands for execution.
4. Check if `sapstartsrv` service is running.
   - Service is restarted when required, because it is required for `sapcontrol` commands.
5. Execute `sapcontrol` commands and wait for completion.
6. Execute `cleanipc` command unless the variable `sap_control_cleanipc` is set to `false`.
7. Show output message with current status of processes for each instance.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of starting all SAP Netweaver instances on host(s).
```yaml
---
- name: Ansible Play for SAP Control
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_control
      ansible.builtin.include_role:
        name: community.sap_operations.sap_control
      vars:
        sap_control_function: start_all_nw
```

Example of stopping `B01` SAP Netweaver and HANA instances on host(s) using `community.sap_libs.sap_system_facts`, without `cleanipc` execution.
```yaml
---
- name: Ansible Play for SAP Control
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_control
      ansible.builtin.include_role:
        name: community.sap_operations.sap_control
      vars:
        sap_control_function: stop_all_sap
        sap_control_sid: B01
        sap_control_use_sap_system_facts: true
        sap_control_cleanipc: false
```
<!-- END Execution Example -->

## Testing
This Ansible Role has been tested in following scenarios.
Operating systems:
 - SUSE Linux Enterprise Server for SAP applications 15 SP6 and SP7 (SLE4SAP)
 - SUSE Linux Enterprise Server for SAP applications 16 (SLE4SAP)

SAP Products:
- SAP Netweaver 7.50 and higher
- SAP HANA 2.0 SP04 and higher

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
### sap_control_function
- _Type:_ `string`

The sapcontrol function to execute on target host.  
These are predefined functions defined in variable `__sap_control_function_definitions`.

### sap_control_sid
- _Type:_ `string`

The 3-letter SAP System ID (e.g., 'PRD', 'QAS').  
This is required when executing a function that targets a specific SAP instance (e.g., `start_sap_nw`) instead of all instances on the host.

### sap_control_command_nowait
- _Type:_ `boolean`
- _Default:_ `false`

If set to `true`, the role will not wait for start/stop operations to complete.  
> **NOTE:** This option should be used with caution, as the role will not verify the final status of the instance.

### sap_control_cleanipc
- _Type:_ `boolean`
- _Default:_ `true`

If set to `false`, the `cleanipc` command will not be executed after stopping an SAP instance.

### sap_control_use_sap_system_facts
- _Type:_ `boolean`
- _Default:_ `false`

Enable this variable to use `community.sap_libs.sap_system_facts` to detect SAP instances.  
This can be useful if this role is part of a playbook that expects facts set by that module.  
> **NOTE:** This module will not detect instances with `sapstartsrv` stopped.
<!-- END Role Variables -->
