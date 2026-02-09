> **DEPRECATED (2026-01)**: PyRFC dependency deprecated — SAP discontinued development and maintenance of the PyRFC library in 2024.<br>
><br>
> The PyRFC library is a critical dependency for this role; it acts as a Python wrapper for the underlying SAP NWRFC SDK (C++ libraries).<br>
> Because SAP has archived the PyRFC project, it will no longer be updated to maintain compatibility with future security patches or version releases of the NWRFC SDK.<br>
><br>
> While PyRFC and the SAP NWRFC SDK are currently still available, their deprecation means they may be removed without notice.<br>
><br>
> Users should plan to migrate away from RFC-based automation toward supported OData/REST API integrations or SAP BTP connectors.<br>


# sap_rfc Ansible Role

The sap_rfc Ansible Role executes an SAP Remote Function Call (RFC) from a server-side host with connectivity to the SAP System host/s, and performs setup as necessary ([`PyRFC`](https://github.com/SAP/PyRFC) open source by SAP, and [`SAP NWRFC SDK`](https://support.sap.com/en/product/connectors/nwrfcsdk.html)).

## Ansible Role Overview

The sap_rfc Ansible Role uses:
- the Ansible Module `sap_pyrfc` from the Ansible Collection `sap_libs`, which leverages the open-source [`PyRFC`](https://github.com/SAP/PyRFC) bindings for the proprietary [`SAP NWRFC SDK`](https://support.sap.com/en/product/connectors/nwrfcsdk.html).
- the Ansible Module `software_center_download` from the Ansible Collection `sap_launchpad`, which on first-run is used to download the [`SAP NWRFC SDK`](https://support.sap.com/en/product/connectors/nwrfcsdk.html).

Appropriate target SAP System user authorizations are required for the execution of the RFCs, and on first-run to obtain the [`SAP NWRFC SDK`](https://support.sap.com/en/product/connectors/nwrfcsdk.html) an SAP User ID with download privileges is required.

The Ansible Role does not contain any system-altering RFCs by default when executed.

The Ansible Task variables define the RFC actions to be executed. Examples are given below.

## Ansible Role Requirements and Dependencies

### Dependencies on other Ansible Roles

To execute successfully, this Ansible Role is dependant on the Ansible Collections:
- `community.sap_launchpad` on first run
- `community.sap_libs` for every run

The first run will setup Python `altinstall`, subsequent runs on the same host will re-use the Python `altinstall` where PyRFC enabled. This is to protect the System default Python installation from additional or altered versions of Python Packages.

### Operating System

This role has been tested on target systems using RHEL 8.x, and is designed for Linux operating systems.

This role has not been tested and amended for SAP NetWeaver Application Server instantiations on IBM AIX or Windows Server.

Assumptions for executing this role include:

- The target host has access to the SAP System (i.e. the SAP NetWeaver Application Server instance)
- Registered OS License and OS Package repositories are available (from the relevant content delivery network of the OS vendor)

## Examples

The following example executes remote function `STFC_CONNECTION`.

```yaml
---
- name: Ansible Play
  hosts: all
  become: true
  tasks:

    - name: Execute Ansible Role sap_rfc
      ansible.builtin.include_role:
        name: community.sap_operations.sap_rfc
      vars:
        suser_id: 'My_S-User_ID'
        suser_password: 'My_S-User_Password'
        sap_nwrfc_sdk: nwrfc750P_10-70002752.zip
        target_connection:
          ashost: "My_SAP_System_Host"  # Example: s4hana.poc.cloud
          sysid: "My_SID"  # Example: TDT
          sysnr: "My_Instance_Number"  # Example: "01"
          client: "My_Client_ID"  # Example: "400"
          user: "My_Connection_User"  # Example: DDIC
          passwd: "My_Connection_User_Password"
          lang: EN
        target_function: STFC_CONNECTION
        target_parameters:
          REQUTEXT: 'Hello SAP!'
        pyrfc_first_run: yes
      register: sap_rfc_output

    - name: Show output of the variable 'sap_rfc_output'
      ansible.builtin.debug:
        msg: "{{ sap_rfc_output }}"
```


The Ansible Role is designed to provide for all different RFCs. Therefore, the RFC parameters _(IMPORTING, EXPORTING, CHANGING)_ can accept the following data types:

- Data elements (string, integer etc.)
- ABAP Structure
- ABAP Table

These RFC parameter data elements are mapped to the equivalent Python data type (e.g. string, integer, dictionary, list). Examples of these are shown below.

### Examples of Ansible Task variables for different RFC parameters

**RFC parameter requires a data element:**

- Commonly string or integer
- For this input type the PyRFC Python module requires a Python string or integer
- Ansible Task must declare the parameter name and use a YAML variable

`Ansible Task code example for data element:`
```yaml
sap_rfc_target_parameters:
  VAR: 'ECHO'
```

**RFC parameter requires an ABAP Structure:**

- For this input type the PyRFC Python module requires a Python Dictionary.
- Ansible Task must declare the parameter name and use a YAML dictionary (key:value)

`Ansible Task code example for ABAP Structure:`
```yaml
sap_rfc_target_parameters:
  IMPORTSTRUCT:
    RFCFLOAT: 1.1
    RFCCHAR1: 'A'
```

**RFC requires an ABAP Table:**

- For this input type the PyRFC Python module requires a Python List.
- The Ansible Task must declare the parameter name and use a YAML list

`Ansible Task code example for ABAP Table:`
```yaml
sap_rfc_target_parameters:
  RFCTABLE:
    - COLUMN0: SAP
    - COLUMN1: 1.23
```

## Supplementary information

The [Supplementary information](./SUPPLEMENTARY.md) provides:
- Context of SAP NWRFC SDK and PyRFC
  - Explanation of samples from SAP NWRFC SDK
- Brief explanation of SAP RFCs
- Security concerns with RFCs and SAP Systems
