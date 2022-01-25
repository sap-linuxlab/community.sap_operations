# sap_facts Ansible Module

- The equivalent of Ansible's `gather_facts`, but for gathering SAP facts
- Scans the host and populates a dictionary list `sap_facts` containing `SID` `Type` `InstanceNumber` `InstanceType`
- This is the foundation of every modules / roles / tasks not just for this Ansbile collection but for any other collections related to SAP
- ![](/docs/diagrams/workflow_module_sap_facts.svg)
- Full list of outputs:
    | **Output**            | **Info**                                  | **Return Variable**                 |
    | :---                  | :---                                      | :---                                |
    | sap_nw_sid            | List of all SAP NW SIDs                   | `<register_variable>.sap_nw_sid`    |
    | sap_hana_sid          | List of all SAP HANA SIDs                 | `<register_variable>.sap_hana_sid`  |
    | sap_nw_nr             | List of all SAP NW instance numbers       | `<register_variable>.sap_nw_nr`     |
    | sap_hana_nr           | List of all SAP HANA instance numbers     | `<register_variable>.sap_hana_nr`   |
    | **sap_facts**         | Dictionary list of all the details        | `<register_variable>.sap_facts`     |

- Sample `sap_facts` dictionary list generated:
            
    ```yaml
    [
            {
                "InstanceNumber": "00",
                "InstanceType": "HANA",
                "SID": "H20",
                "Type": "hana"
            },
            {
                "InstanceNumber": "02",
                "InstanceType": "ASCS",
                "SID": "S4H",
                "Type": "nw"
            },
            {
                "InstanceNumber": "01",
                "InstanceType": "PAS",
                "SID": "S4H",
                "Type": "nw"
            },
            {
                "InstanceNumber": "03",
                "InstanceType": "WebDisp",
                "SID": "WD1",
                "Type": "nw"
            }
    ]
    ```

