
# Development of community.sap_operations Ansible Collection

This Ansible Collection is developed with several design principles and code practices.

## Code structure

This Ansible Collection directory tree structure is shown below:
```code
collection/
├── docs/
├── meta/
├── plugins/
│   └── modules/
│       ├── sap_facts.sh
│       ├── sap_monitor_hana_status.sh
│       ├── sap_monitor_nw_perf.sh
│       ├── sap_monitor_nw_response.sh
│       └── sap_monitor_nw_status.sh
├── roles/
│   ├── os_ansible_user
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       └── main.yml
│   ├── os_etchosts
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       ├── main.yml
│   │       └── update_etchosts.yml
│   ├── os_knownhosts
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       └── main.yml
│   ├── sap_control
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       ├── functions
│   │       │   ├── cleanipc.yml
│   │       │   ├── restart_sapstartsrv.yml
│   │       │   └── sapstartsrv.yml
│   │       ├── main.yml
│   │       ├── prepare.yml
│   │       └── sapcontrol.yml
│   ├── sap_fapolicy
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       ├── enable_fapolicy.yml
│   │       ├── get_sidadm_user.yml
│   │       ├── get_user_uid.yml
│   │       ├── main.yml
│   │       └── update_fapolicy.yml
│   ├── sap_firewall
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       ├── enable_firewall.yml
│   │       ├── generate_ports_generic.yml
│   │       ├── generate_ports_hana.yml
│   │       ├── generate_ports_nw.yml
│   │       ├── main.yml
│   │       └── update_firewall.yml
│   ├── sap_profile_update
│   │   ├── defaults
│   │   │   └── main.yml
│   │   └── tasks
│   │       ├── main.yml
│   │       └── update_parameter.yml
│   └── sap_rhsm
│       ├── defaults
│       │   └── main.yml
│       └── tasks
│           ├── main.yml
│           ├── rhsm_refresh.yml
│           └── rhsm_register.yml
├── playbooks/
│   ├── sample-os-yum-update.yml
│   ├── sample-sap-control-all-restart-nw.yml
│   ├── sample-sap-control-all-restart.yml
│   ├── sample-sap-control-single-restart.yml
│   ├── sample-sap-etchosts-update.yml
│   ├── sample-sap-facts.yml
│   ├── sample-sap-fapolicy-all-update.yml
│   ├── sample-sap-firewall-all-update.yml
│   ├── sample-sap-firewall-update.yml
│   ├── sample-sap-hana-status.yml
│   ├── sample-sap-knownhosts-update.yml
│   ├── sample-sap-nw-perf.yml
│   ├── sample-sap-nw-resp.yml
│   ├── sample-sap-nw-status.yml
│   └── sample-sap-profile-update.yml
├── tests/
├── galaxy.yml
└── README.md
```

## Execution logic

This Ansible Collection is designed to be heavily re-usable for various scenarios where SAP System operational tasks are performed, and avoid encapsulation of commands within Ansible's syntax; this ensures the scripts (and the sequence of commands) could be re-used manually or re-used by another automation framework.

It is important to understand the execution flow by an Ansible Playbook to either an Ansible Role (with or without embedded Playbooks), an Ansible Task, or an Ansible Module (and contained Script files). Alternatively it is possible to call the script files manually.

See examples below:

### Ansible Playbook to call many Ansible Roles (and the contained interlinked Ansible Tasks)
```code
# Produce outcome scenario, using many interlinked tasks
- Run: Ansible Playbook
  - Run: Ansible Role
    - Ansible Task
      - Ansible Playbook 1..n
        - Ansible Task
          - execute custom Ansible Module
            - execute specified Python Module Functions
              - call APIs or CLIs/binaries
    - Ansible Task
      - Ansible Playbook 1..n
        - Ansible Task
          - subsequent OS commands using output from APIs or CLIs/binaries
```

### Ansible Playbook to call single set of Ansible Tasks
```code
# Produce outcome scenario, with single set of tasks
- Run: Ansible Playbook
  - Ansible Task
    - execute custom Ansible Module
      - execute specified Python Module Functions
        - call APIs or CLIs/binaries
```

### Python Shell to call single Python Function
```code
# Produce outcome scenario manually with singular code execution
- Run: Python Shell
  - Import Python Module file for APIs or CLIs/binaries
  - Execute specificed Python Functions
```
