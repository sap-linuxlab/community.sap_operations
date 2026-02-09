# sap_monitor_hana_status Ansible Module

## Description

This Ansible Module returns status of SAP HANA instance using `sapcontrol` function `GetSystemInstanceList`.

## Parameters

| Parameter | Required | Default | Details |
| --- | --- | --- | --- |
| hana_sid | Yes | | SAP HANA SID |
| hana_instance_number | Yes | | SAP HANA Instance Number |


## Returned Values
Each returned parameter can be retrieved from registered variable.

| Parameter | Details |
| --- | --- |
| sap_status | Status determined by `sapcontrol`: `GREEN`, `YELLOW`, `RED` or `GRAY` |

**NOTE:**

- Returned message `msg` does not represent status, but rather if module was executed. Status is visible only in `sap_status`.

### Example
Example of getting status of SAP HANA with SID `H02` and Instance Number `90`. 

```yaml
---
- name: Ansible Play
  hosts: hana
  become: true

  tasks:

    - name: Execute Ansible Module sap_monitor_hana_status
      community.sap_operations.sap_monitor_hana_status:
        hana_sid: H02
        hana_instance_number: '90'
      register: __sap_monitor_hana_status

    - name: Show returned values from sap_monitor_hana_status
      ansible.builtin.debug:
        var: __sap_monitor_hana_status
```

Example of returned values.
```console
ok: [b01hana] =>
    __sap_monitor_hana_status:
        changed: false
        failed: false
        msg: SAP Check Successful
        sap_status: GREEN
```

