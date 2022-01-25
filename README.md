# community.sap_operations Ansible Collection ![Ansible Lint](https://github.com/infrasap/community.sap_operations/workflows/Ansible%20Lint/badge.svg?branch=main)

This Ansible Collection executes various SAP Systems operational tasks, which can be used day-to-day individually or combined for more complex regular maintainance automation

## Functionality

This Ansible Collection executes various SAP Systems operational tasks, including:

- **OS configuration Post-install of SAP Software**
  - Create ansible user for managing systems
  - Update /etc/hosts file
  - Update SSH authorized known hosts file
  - Update fapolicy entries based on SAP System instance numbers
  - Update firewall port entries based on SAP System instance numbers
  - License registration and refresh for RHEL subscription manager
- **SAP administration tasks**
  - Start/Stop of SAP HANA and SAP NetWeaver (in any configuration)
  - Update SAP profile files

## Contents

An Ansible Playbook can call either an Ansible Role, or the individual Ansible Modules:
- **Ansible Roles** (runs multiple Ansible Modules)
- **Ansible Modules** (and adjoining Python/Bash Functions)

For further information regarding the development, code structure and execution workflow please read the [Development documentation](./docs/DEVELOPMENT.md).

Within this Ansible Collection, there are various Ansible Roles and Ansible Modules.

#### Ansible Roles

| Name &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; | Summary |
| :-- | :-- |
| [os_ansible_user](/roles/os_ansible_user) | creates Ansible user `ansadm` with ssh key |
| [os_etchosts](/roles/os_etchosts) | updates `/etc/hosts` |
| [os_knownhosts](/roles/os_knownhosts) | updates known hosts file `/.ssh/known_hosts` |
| [sap_control](/roles/sap_control) | starting and stopping SAP systems |
| [sap_fapolicy](/roles/sap_fapolicy) | update service `fapolicyd` for generic / sap nw / sap hana related uids |
| [sap_firewall](/roles/sap_firewall) | update service `firewalld` for generic / sap nw / sap hana related ports |
| [sap_profile_update](/roles/sap_profile_update) | update default and instance profiles |
| [sap_rhsm](/roles/sap_rhsm) | Red Hat subscription manager registration |

#### Ansible Modules

| Name &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; | Summary |
| :-- | :-- |
| [sap_operations.sap_facts](/docs/module_sap_facts.md) | gather SAP facts in a host (e.g. SAP System IDs and SAP System Instance Numbers of either SAP HANA database server or SAP NetWeaver application server) |
| [sap_operations.sap_monitor_hana_status](/docs/module_sap_monitor.md) | check status of running SAP HANA database server |
| [sap_operations.sap_monitor_nw_status](/docs/module_sap_monitor.md) | check status of running SAP NetWeaver application server |
| [sap_operations.sap_monitor_nw_perf](/docs/module_sap_monitor.md) | check host performance metrics from SAP NetWeaver Primary Application Server (PAS) instance |
| [sap_operations.sap_monitor_nw_response](/docs/module_sap_monitor.md) | check system response time metrics from SAP NetWeaver Primary Application Server (PAS) instance |

## Execution examples

There are various methods to execute the Ansible Collection, dependant on the use case. For more information, see [Execution examples with code samples](./docs/EXEC_EXAMPLES.md) and the summary below:

| Execution Scenario | Use Case | Target |
| --- | --- | --- |
| Ansible Playbook <br/>-> source Ansible Collection <br/>-> execute Ansible Task <br/>--> run Ansible Module <br/>---> run Python/Bash Functions | Simple executions with a few activities | Localhost or Remote |
| Ansible Playbook <br/>-> source Ansible Collection <br/>-> execute Ansible Task <br/>--> run Ansible Role <br/>---> run Ansible Module <br/>----> run Python/Bash Functions <br/>--> run Ansible Role<br/>---> ... | Complex executions with various interlinked activities;<br/> run in parallel or sequentially | Localhost or Remote |
| Python/Bash Functions | Simple testing or non-Ansible use cases | Localhost |

## Requirements, Dependencies and Testing

### Operating System requirements

Designed for Linux operating systems, e.g. RHEL and SLES.

This role has not been tested and amended for SAP NetWeaver Application Server instantiations on IBM AIX or Windows Server.

Assumptions for executing this role include:
- Registered OS License and OS Package repositories are available (from the relevant content delivery network of the OS vendor)

### Python requirements

Python 3 from the execution/controller host.

### Testing on execution/controller host

**Tests with Ansible Core release versions:**
- Ansible Core 2.11.5 community edition

**Tests with Python release versions:**
- Python 3.9.7 (i.e. CPython distribution)

**Tests with Operating System release versions:**
- RHEL 8.4
- macOS 11.6 (Big Sur), with Homebrew used for Python 3.x via PyEnv

### Testing on target/remote host

**Tests with Operating System release versions:**
- RHEL 8.2 for SAP

## License

- [Apache 2.0](./LICENSE)

## Contributors

Contributors to the Ansible Roles within this Ansible Collection, are shown within [/docs/contributors](./docs/CONTRIBUTORS.md).
