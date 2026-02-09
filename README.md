# community.sap_operations Ansible Collection

![Ansible Lint](https://github.com/sap-linuxlab/community.sap_operations/actions/workflows/ansible-lint.yml/badge.svg?branch=main)

## Description

This Ansible Collection executes various SAP Systems operational tasks, including:

- Start, Stop and Restart of SAP Systems consisting of SAP Netweaver and SAP HANA.
- Configuration of firewall with predefined ports for SAP products.
- Configuration of SAP HANA Backint backups and their execution and cleanup.
- Manages parameters in SAP profile files.
- Execution of SAP HANA Replication takeover action in replicated environment.

## Requirements

| Component | Control Node | Managed Node |
| --- | --- | --- |
| Operating System | Any OS | Red Hat Enterprise Linux for SAP Solutions 8.x, 9.x and 10.x<br>SUSE Linux Enterprise Server for SAP applications 15 SP5, 15 SP6, 15 SP7 and 16.0 |
| Python | 3.11 or higher | 3.9 or higher |
| Ansible-Core | 2.18 or higher | N/A |
| Ansible | 12 or higher | N/A |

> **Managed Node Registration**<br>
> Operating system needs to have access to required package repositories either directly or via subscription registration.

**Additional notes:**

- **Version Compatibility:** For a detailed mapping of supported Python versions and Ansible-Core life cycles, refer to the official [Ansible-Core Support Matrix](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix).
- **Control Node Permissions:** Ensure the user executing the playbooks has the necessary SSH keys and sudo privileges configured for the target environment.

## Installation Instructions

### Installation
Install this collection with Ansible Galaxy command:
```console
ansible-galaxy collection install community.sap_operations
```

### Upgrade
Installed Ansible Collection will not be upgraded automatically when Ansible package is upgraded.

To upgrade the collection to the latest available version, run the following command:
```console
ansible-galaxy collection install community.sap_operations --upgrade
```

You can also install a specific version of the collection, when you encounter issues with latest version. Please report these issues in affected Role repository if that happens.
Example of downgrading collection to version 1.0.0:
```
ansible-galaxy collection install community.sap_operations:==1.0.0
```

See [Installing collections](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html) for more details on installation methods.

## Use Cases

### Ansible Roles
| Name | Summary |
| --- | --- |
| [sap_control](https://github.com/sap-linuxlab/community.sap_operations/tree/main/roles/sap_control) | Executes predefined sapcontrol operations |
| [sap_firewall](https://github.com/sap-linuxlab/community.sap_operations/tree/main/roles/sap_firewall) | Configures firewall with recommended rules for SAP Systems or custom ports |
| [sap_hana_backint](https://github.com/sap-linuxlab/community.sap_operations/tree/main/roles/sap_hana_backint) | Executes range of actions to operate SAP HANA Backint Agents across different Cloud platforms |
| [sap_hana_sr_takeover](https://github.com/sap-linuxlab/community.sap_operations/tree/main/roles/sap_hana_sr_takeover) | Executes Takeover operation on SAP HANA System with configured SAP HANA System Replication (HSR) |
| [sap_profile_update](https://github.com/sap-linuxlab/community.sap_operations/tree/main/roles/sap_profile_update) | Manages parameters in SAP profile files |

#### Deprecated Roles
| Name | Summary |
| --- | --- |
| os_ansible_user | Removed in favor of built in Ansible Module `ansible.builtin.user` |
| os_etchosts | Removed in favor of Ansible Role [community.sap_install.sap_maintain_etc_hosts](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_maintain_etc_hosts) |
| os_knownhosts | Removed in favor of built in Ansible Module `ansible.builtin.known_hosts` |
| sap_fapolicy | Removed in favor of Ansible Role [linux_system_roles.fapolicyd](https://github.com/linux-system-roles/fapolicyd) |
| sap_rfc | Deprecated because of SAP discontinued development and maintenance of the PyRFC library in 2024 |
| sap_rhsm | Removed in favor of Ansible Role [linux_system_roles.rhc](https://github.com/linux-system-roles/rhc) |

### Ansible Modules

> **NOTE: All included modules are currently not maintained or tested.**<br>
> They should be used with caution.<br>

| Name | Summary |
| --- | --- |
| [sap_operations.sap_facts](/docs/module_sap_facts.md) | Gather facts about SAP Systems on host |
| [sap_operations.sap_monitor_hana_status](/docs/module_sap_monitor_hana_status.md) | Checks status of running SAP HANA databases on host |
| [sap_operations.sap_monitor_nw_status](/docs/module_sap_monitor_nw_status.md) | Check status of running SAP NetWeaver applications on host |
| [sap_operations.sap_monitor_nw_perf](/docs/module_sap_monitor_nw_perf.md) | Checks host performance metrics from SAP NetWeaver Primary Application Server (PAS) instance |
| [sap_operations.sap_monitor_nw_response](/docs/module_sap_monitor_nw_response.md) | Checks system response time metrics from SAP NetWeaver Primary Application Server (PAS) instance |

## Testing
This Ansible Collection was tested across different Operating Systems, SAP products and scenarios. You can find examples of some of them below.

Operating systems:

- Red Hat Enterprise Linux for SAP Solutions 8.x, 9.x and 10.x
- SUSE Linux Enterprise Server for SAP applications 15 SP7 and 16.0

SAP Products:

- SAP S/4HANA AnyPremise 2023
- SAP BW/4HANA 2023
- SAP HANA 2.0 SPS08

## Contributing
For information on how to contribute, please see our [contribution guidelines](https://sap-linuxlab.github.io/initiative_contributions/).

## Contributors
We welcome contributions to this collection. For a list of all contributors and information on how you can get involved, please see our [CONTRIBUTORS document](./CONTRIBUTORS.md).

## Support
You can report any issues using [Issues](https://github.com/sap-linuxlab/community.sap_operations/issues) section.

## Release Notes and Roadmap
You can find the release notes of this collection in [Changelog file](https://github.com/sap-linuxlab/community.sap_operations/blob/main/CHANGELOG.rst)

## Further Information

### Variable Precedence Rules
Please follow [Ansible Precedence guidelines](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) on how to pass variables when using this collection.

## License
[Apache 2.0](https://github.com/sap-linuxlab/community.sap_install/blob/main/LICENSE) 
