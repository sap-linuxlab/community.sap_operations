# sap_monitor Ansible Module

Ansible modules for SAP healthcheck / monitoring

- Modules for SAP healthcheck / monitoring
- Please check the documentaion here [SAP Check Documentation](/docs/sap_monitor)
- For technical details, please check the individual `.sh` files here [SAP Check](/plugins/modules)


- **sap_monitor_hana_status**            
    - Checks the status of SAP HANA system
    - Returns 'GREEN' 'YELLOW' 'RED' 'GRAY' as returned by `sapcontrol`
    - Full list of outputs:
        | **Output**            | **Info**                                                  | **Return Variable**                 |
        | :---                  | :---                                                      | :---                                |
        | sap_status            | 'GREEN' 'YELLOW' 'RED' 'GRAY' as returned by `sapcontrol` | `<register_variable>.sap_status`    |
    - Sample output:
        ```yaml
        "changed": false,
        "sap_status": "GREEN",
        "failed": false,
        "item": {
            "InstanceNumber": "90",
            "InstanceType": "HANA",
            "SID": "HDX",
            "Type": "hana"
        },
        "msg": "SAP Check Successful"
        ```

- **sap_monitor_nw_status**            
    - Checks the status of SAP Netweaver system
    - Returns 'GREEN' 'YELLOW' 'RED' 'GRAY' as returned by `sapcontrol`
    - Full list of outputs:
        | **Output**            | **Info**                                                  | **Return Variable**                 |
        | :---                  | :---                                                      | :---                                |
        | sap_status            | 'GREEN' 'YELLOW' 'RED' 'GRAY' as returned by `sapcontrol` | `<register_variable>.sap_status`    |
    - Sample output:   
        ```yaml
        {
            "ansible_loop_var": "item",
            "changed": false,
            "sap_status": "GREEN",
            "failed": false,
            "item": {
                "InstanceNumber": "92",
                "InstanceType": "ASCS",
                "SID": "S4X",
                "Type": "nw"
            },
            "msg": "SAP Check Successful"
        },
        {
            "ansible_loop_var": "item",
            "changed": false,
            "sap_status": "GREEN",
            "failed": false,
            "item": {
                "InstanceNumber": "91",
                "InstanceType": "PAS",
                "SID": "S4X",
                "Type": "nw"
            },
            "msg": "SAP Check Successful"
        }
        ```


- **sap_monitor_nw_perf**            
    - Checks performance metrics of an SAP Netweaver ABAP system
    - > **_Note:_**  The current checklist only contains 4 items at this early stage of development but can be easily improved later
    - Current scope:
        - Heap Memory
        - Extended Memory
        - CPU Utilization
        - Program Buffer Swap
        - (more can be added)
    - Full list of outputs:
        | **Output**            | **Info**                          | **Return Variable**                       |
        | :---                  | :---                              | :---                                      |
        | heap_memory           | Heap memory                       | `<register_variable>.heap_memory`         |
        | extended_memory       | Extended memory                   | `<register_variable>.extended_memory`     |
        | cpu_util              | CPU utilization                   | `<register_variable>.cpu_util`            |
        | program_swap          | Program buffer swap               | `<register_variable>.program_swap`        |
    - Sample output:
        ```yaml
        "changed": false,
        "cpu_util": "7",
        "extended_memory": "19",
        "failed": false,
        "heap_memory": "0",
        "item": {
            "InstanceNumber": "91",
            "InstanceType": "PAS",
            "SID": "S4X",
            "Type": "nw"
        },
        "msg": "SAP Check Successful",
        "program_swap": "0.0
        ```

- **sap_monitor_nw_response**            
    - Checks response times of an SAP Netweaver ABAP system
    - > **_Note:_**  The current checklist only contains 4 items at this early stage of development but can be easily improved later
    - Current scope:
        - Dialog Response Time
        - Database Response Time
        - Front End Response Time
        - Program Buffer Swap
        - (more can be added)
    - Full list of outputs:
        | **Output**                | **Info**                              | **Return Variable**                           |
        | :---                      | :---                                  | :---                                          |
        | dialog_response_time      | Dialog response time                  | `<register_variable>.dialog_response_time`    |
        | database_response_time    | Database respone time                 | `<register_variable>.database_response_time`  |
        | frontend_response_time    | Front end response time               | `<register_variable>.frontend_response_time`  |
        | number_users              | Current number of logged in users     | `<register_variable>.number_users`            |
    - Sample output:     
        ```yaml
        "changed": false,
        "database_response_time": "177",
        "dialog_response_time": "542",
        "failed": false,
        "frontend_response_time": "211",
        "item": {
            "InstanceNumber": "91",
            "InstanceType": "PAS",
            "SID": "S4X",
            "Type": "nw"
        },
        "msg": "SAP Check Successful",
        "number_users": "19"
       ```