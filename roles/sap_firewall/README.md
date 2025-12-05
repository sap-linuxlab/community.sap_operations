<!-- BEGIN Title -->
# sap_firewall Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_firewall` configures `firewalld` with recommended rules for SAP Systems or custom ports.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `ansible.posix`
    - Modules:
        - `firewalld`
  - This collection is part of main Ansible package.
<!-- END Dependencies -->

## Prerequisites
<!-- BEGIN Prerequisites -->
This Ansible role installs Python libraries (bindings) for `firewalld` on operating systems where they are not included as a dependency of the `firewalld` package.
For example, the `python311-firewall` package might need to be installed on some OS versions, while on others it is included as a dependency of `firewalld`.

> **SUSE NOTE for SLES 15 and older**: Firewall bindings packages compatible with Python 3.11 (e.g., `python311-firewall`) are available only in SLES 15 SP6+.  
> Existing `python3-firewall` on SLES 15 SP5 or older is not compatible with Python 3.11.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
> **NOTE: Predefined presets contain recommended ports.**  
> You can design your own port openings using `sap_firewall_ports`, if none of presets suit your requirements.

### Available Presets
Following presets are defined by Ansible Role with ports below.
> `NN` specifies the SAP Instance Number defined in `sap_firewall_instance_number`.

#### Preset: netweaver
| Ports | Protocol | Reason |
| --- | --- | --- |
| 1128-1129 | TCP | SAP Host Agent ports for status and metrics communication. |
| 3200-3399 | TCP | Essential SAP Gateway (33NN) and SAP Dispatcher (32NN) communication for all instance numbers (00-99) |
| 36NN | TCP | SAP Message Server port (36NN). Used for internal communication between application servers. |
| 80NN | TCP | SAP Internet Communication Manager (ICM) HTTP port (80NN). Used for non-secure web client access. |
| 81NN | TCP | SAP Message Server HTTP port (81NN), configured via the `ms/http_port_<n>` profile parameter. |
| 443NN | TCP | SAP Internet Communication Manager (ICM) HTTPS port (443NN). Used for secure web client access. |
| 5NN13</br>5NN14<br>5NN16 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 620NN<br>621NN | TCP | JAVA ports (62NNN), commonly used for communication within the AS-Java stack, e.g., P4/P4S protocols. |

#### Preset: hana
| Ports | Protocol | Reason |
| --- | --- | --- |
| 1128-1129 | TCP | SAP Host Agent ports for status and metrics communication. |
| 5050 | TCP | SAP HANA Data Provisioning Agent (DP Agent) port for SDA/SDI connectivity. |
| 43NN | TCP | SAP HANA Web Dispatcher HTTPS port. |
| 3NN90 | TCP | SAP HANA SQL and internal communication range for the IndexServer and distributed nodes. |
| 30105<br>30107<br>30140 | TCP | SAP HANA System Replication (SR) and internal endpoint communication. |
| 4NN01</br>4NN02<br>4NN06<br>4NN12<br>4NN14<br>4NN40 | TCP | SAP HANA Extended Application Services (XS) and other key internal services. |
| 5NN13</br>5NN14<br>5NN16 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 51000-51500 | TCP | SAP HANA XSA runtime port range for the xscontroller-managed Web Dispatcher connection. |
| 64997 | TCP | Internal administration port for the SAP Web Dispatcher, used for local communication only. |

#### Preset: ha
| Ports | Protocol | Reason |
| --- | --- | --- |
| 5404-5405 | UDP | UDP ports used by Corosync for inter-node communication and cluster heartbeats. |
| 2224 | TCP | TCP port used by the Pacemaker Remote service to manage remote nodes or containerized resources. |

### Execution Flow
<!-- BEGIN Execution Flow -->
Execution with `sap_firewall_state` set to `present` (default):
1. Assert and validate all variables.
2. Install `firewalld` and bindings, if required.
3. Add new services based on presets defined in `sap_firewall_presets`.
  - Fail if existing service file is detected, unless `sap_firewall_service_force` is set to `true`.
4. Add new ports and services defined in `sap_firewall_ports`.
5. Reload `firewalld` configuration, if required.

Execution with `sap_firewall_state` set to `absent`:
1. Assert and validate all variables.
2. Install `firewalld` and bindings, if required.
  - This is required because `firewall-cmd` commands are executed in online mode.
3. Remove services from `firewall-cmd` based on presets defined in `sap_firewall_presets`.
4. Remove ports and services from `firewall-cmd` defined in `sap_firewall_ports`.
5. Reload `firewalld` configuration, if required.
6. Remove existing service files under `/etc/firewalld/services/` based on presets defined in `sap_firewall_presets`. 
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of enabling `netweaver` preset and custom TCP port `3700` into `public` zone.
```yaml
---
- name: Ansible Play for SAP Firewall
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_firewall
      ansible.builtin.include_role:
        name: community.sap_operations.sap_firewall
      vars:
        sap_firewall_state: present
        sap_firewall_presets:
          - preset: netweaver
            zone: public
        sap_firewall_instance_number: '90'
        sap_firewall_ports:
          - zone: public
            tcp:
              - '3700'
```

Example of enabling UDP port range `3700-3701` and existing service `ssh` in `internal` zone.
```yaml
---
- name: Ansible Play for SAP Firewall
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_firewall
      ansible.builtin.include_role:
        name: community.sap_operations.sap_firewall
      vars:
        sap_firewall_state: present
        sap_firewall_ports:
          - zone: internal
            udp:
              - '3700-3701'
            service:
              - ssh
```

Example of removing configured `hana` preset and custom TCP port `3700` into `public` zone.
```yaml
---
- name: Ansible Play for SAP Firewall
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_firewall
      ansible.builtin.include_role:
        name: community.sap_operations.sap_firewall
      vars:
        sap_firewall_state: absent
        sap_firewall_presets:
          - preset: hana
            zone: public
        sap_firewall_instance_number: '90'
        sap_firewall_ports:
          - zone: public
            tcp:
              - '3700'
```

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
### sap_firewall_state
- _Type:_ `string`
- _Default:_ `present`

Sets the desired state of the firewall configuration for SAP.  
`present` - Creates and enables the firewall services for SAP.  
`absent`  - Removes the firewall services for SAP.  

### sap_firewall_presets
- _Type:_ `list` of type `dict`

A list of SAP Firewall configuration presets to apply.  
Each item is a dictionary defining the preset and its zone.  
Preset options:  
- `hana`      - Use predefined ports for SAP HANA.  
- `netweaver` - Use predefined ports for SAP NetWeaver.  
- `ha`        - Use predefined ports for SAP High Availability.  
Example zone values: `block, dmz, drop, external, home, internal, public, trusted, work`.  
Example:  
```yaml
sap_firewall_presets:
  - preset: hana
    zone: public
  - preset: netweaver
    zone: internal
```

### sap_firewall_ports
- _Type:_ `list` of type `dict`

A list of custom firewall rules to apply.  
Each item in the list is a dictionary that defines a zone and the ports to open.  
Example zone values: `block, dmz, drop, external, home, internal, public, trusted, work`.  
Example:  
```yaml
sap_firewall_ports:
  - zone: public
    tcp:
      - "3200-3399"  # A range of ports
      - "3600"       # A single port
    udp:
      - "1234"
    service:
      - "ssh"
  - zone: internal
    tcp:
      - "8080"
```

### sap_firewall_instance_number
- _Type:_ `string`

The SAP Instance number.  
Required if sap_firewall_presets contains `hana` or `netweaver`.  

### sap_firewall_end_status
- _Type:_ `string`
- _Default:_ `enabled`

Status of firewall at the end of the playbook.  
This will be used only when `sap_firewall_presets` or `sap_firewall_ports` are not empty.  
- `enabled`  - Firewall will be enabled and started.
- `disabled` - Firewall will be disabled and stopped.  

### sap_firewall_service_name
- _Type:_ `string`

The name of the firewall service for SAP.  
If not provided, the service name is generated based on `sap_firewall_presets` and `sap_firewall_instance_number`.  
Example: `sap-netweaver-00` for `sap_firewall_presets: ['netweaver']` and `sap_firewall_instance_number: '00'`.
<!-- END Role Variables -->
