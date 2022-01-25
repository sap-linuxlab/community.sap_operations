# sap_pyrfc Ansible Role

The sap_pyrfc Ansible Role uses the open-source [`PyRFC`](https://github.com/SAP/PyRFC) bindings for the proprietary [`SAP NWRFC SDK`](https://support.sap.com/en/product/connectors/nwrfcsdk.html).

## Ansible Role Overview

This Ansible Role executes SAP RFCs, by downloading the SAP NWRFC SDK and using PyRFC.

Appropriate SAP User ID with download privileges, and target SAP System user authorizations are required.

Examples are given, however the Ansible Role does not contain any system-altering RFCs by default when executed. The actions must be defined in the Ansible Task variables.

## Ansible Role Requirements and Dependencies

### Dependencies on other Ansible Roles

To execute successfully, this Ansible Role is dependant on the Ansible Collection `community.sap_launchpad` on first run. Subsequent runs on the same host will re-use the Python altinstall with PyRFC enabled.

### Operating System

This role has been tested with RHEL, and is designed for Linux operating systems.

This role has not been tested and amended for SAP NetWeaver Application Server instantiations on IBM AIX or Windows Server.

Assumptions for executing this role include:
- Instances of SAP NetWeaver Application Server are installed to the target host
- Relevent OS Packages for SAP are installed
- Registered OS License and OS Package repositories are available (from the relevant content delivery network of the OS vendor)

## Ansible Tasks using PyRFC for different RFC parameter’s data types

RFC parameters _(IMPORTING, EXPORTING, CHANGING)_ can accept the following data types:
- Data elements (string, integer etc.)
- ABAP Structure
- ABAP Table

### Examples of Ansible Task variables for different RFC parameters

**RFC parameter requires a data element:**
- Commonly string or integer
- For this input type the PyRFC module requires a Python string or integer
- Ansible Task must declare the parameter name and use a YAML variable - `see example format below:`
```yaml
parameters:
  VAR: 'ECHO'
```

**RFC parameter requires an ABAP Structure:**
- For this input type the PyRFC module requires a Python Dictionary.
- Ansible Task must declare the parameter name and use a YAML dictionary (key:value) - `see example format below:`
```yaml
parameters:
  IMPORTSTRUCT:
    RFCFLOAT: 1.1
    RFCCHAR1: 'A'
```

**RFC requires an ABAP Table:**
- For this input type the PyRFC module requires a Python List.
- The Ansible Task must declare the parameter name and use a YAML list - `see example format below:`
```yaml
parameters:
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
