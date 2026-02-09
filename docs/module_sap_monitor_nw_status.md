# sap_monitor_nw_status Ansible Module

## Description

This Ansible Module returns status of SAP Netweaver instance using `sapcontrol` function `GetSystemInstanceList`.

## Parameters

| Parameter | Required | Default | Details |
| --- | --- | --- | --- |
| nw_sid | Yes | | SAP Netweaver SID |
| nw_instance_number | Yes | | SAP Netweaver Instance Number |
| nw_instance_type | Yes | | Instance type for filtering results |

Available options for `nw_instance_type`:

- `ASCS` which filters by `MESSAGE`
- `SCS` which filters by `MESSAGE`
- `ERS` which filters by `ENQUE`
- `PAS` which filters by `ABAP`
- `WebDisp` which filters by `WEBDISP`
- `Java` which filters by `J2EE`


## Returned Values
Each returned parameter can be retrieved from registered variable.

| Parameter | Details |
| --- | --- |
| sap_status | Status determined by `sapcontrol`: `GREEN`, `YELLOW`, `RED` or `GRAY` |

**NOTE:**

- Returned message `msg` does not represent status, but rather if module was executed. Status is visible only in `sap_status`.

### Example
Example of getting status of SAP Netweaver with SID `B01` and Instance Number `01` of Type `PAS`. 

```yaml
---
- name: Ansible Play
  hosts: bw
  become: true

  tasks:

    - name: Execute Ansible Module sap_monitor_nw_status
      community.sap_operations.sap_monitor_nw_status:
        nw_sid: B01
        nw_instance_number: '01'
        nw_instance_type: PAS
      register: __sap_monitor_nw_status

    - name: Show returned values from sap_monitor_nw_status
      ansible.builtin.debug:
        var: __sap_monitor_nw_status
```

Example of returned values.
```console
ok: [b01hana] =>
    __sap_monitor_nw_status:
        changed: false
        failed: false
        msg: SAP Check Successful
        sap_status: GREEN
```
