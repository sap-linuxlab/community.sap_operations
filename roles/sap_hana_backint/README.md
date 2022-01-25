# sap_hana_backint Ansible Role

`NOTE: Work in Progress`

Collection of Ansible roles to perform SAP HANA database server backups - the setup, execute, and cleanup - using an SAP HANA Backint Agent.

This Ansible Role works with:
- Amazon Simple Storage Service (S3).
- IBM Cloud Object Storage (COS), S3 protocol compatible
- Microsoft Azure Backup to Microsoft Azure Recovery Services Vault (RSV) [powered by Azure Blob Storage]
- SAP HANA 2.0 SPS06 and above

This Ansible Role uses the following:
- **SAP HANA Backint Agents:**
  - [SAP HANA Backint Agent for Amazon S3 - SAP Note 2935898](https://launchpad.support.sap.com/#/notes/2935898), supports AWS S3 and IBM COS. For CPU architectures x86_64 and ppc64le. See [SAP Note 2935898](https://launchpad.support.sap.com/#/notes/2935898).
  - [Microsoft Azure Backup Plugin for SAP HANA](https://docs.microsoft.com/en-us/azure/backup/sap-hana-db-about), to store backups with Microsoft Azure Recovery Services Vault (RSV) powered by Azure Blob Storage. For CPU architectures x86_64 only. See [SAP Note 2756788](https://launchpad.support.sap.com/#/notes/2756788).
  - [Google Cloud Storage Backint agent for SAP HANA](https://cloud.google.com/solutions/sap/docs/sap-hana-backint-overview), using Google Cloud Storage (GCS) Buckets. For CPU architectures x86_64 only. See [SAP Note 2705632](https://launchpad.support.sap.com/#/notes/2705632).
- **Scripts:**
  - [SAP Note 2399996 - How-To: Configuring automatic SAP HANA Cleanup with SAP HANACleaner](https://launchpad.support.sap.com/#/notes/2399996). An open-source project - https://github.com/chriselswede/hanachecker

## Functionality

The following functions are available:
- `backup_function: 'setup'`: setup of SAP HANA Backint for all SAP HANA SIDs and Tenants on the host, or for specified SID. This includes:
  - create hdbuserstore user and keys
  - create configuration files and install the agent
  - amend SAP HANA parameters in global.ini
- `backup_function: 'execute'`: run backup from SAP HANA Backint for all SAP HANA SIDs and Tenants on the host, or for specified SID.
- `backup_function: 'clean'`: run cleanup of SAP HANA Backint for all SAP HANA SIDs and Tenants on the host, or for specified SID.

The following target platforms are available:
- `target_platform: 'aws_s3'`
- `target_platform: 'azure_backup_rsv'`
- `target_platform: 'ibm_cos_s3'`
- `target_platform: 'gcs'`

## Requirements

- **SAP HANA Backint Agents:**
  - SAP HANA Backint Agent for Amazon S3, version 1.2.17 and above (bundled with SAP HANA 2.0 SPS06 and above)
    - Python 3.7, enabled with SSL. Cannot use System Python (default: Python 3.6), avoid SAP HANA Python (default: Python 3.7)
- **Object Storage platforms:**
  - AWS Simple Storage Service (S3); with object versioning enabled.
  - IBM Cloud Object Storage (COS); with object versioning enabled. Uses S3 protocol.

## Setup detailed information

### hdbuserstore keys

These users and keys will be created in hdbusertstore:
- SystemDB: `HDB_SYSTEM_BACKUP_USER`
- TenantDB: `HDB_TENANT_{SID}_BACKUP_USER`

### Directories and Files

- Backint Directory:      `/usr/sap/{SID}/SYS/global/hdb/opt`
- Executable File:        `/usr/sap/{SID}/SYS/global/hdb/opt/hdbbackint`
- Configuration File:     `/usr/sap/{SID}/SYS/global/hdb/opt/hdbbackint.cfg`
- Cleaner Script:         `/usr/sap/{SID}/SYS/global/hdb/opt/hanacleaner.py`

### SAP HANA parameters

| Description | SAP HANA global.ini parameter | default value set |
| --- | --- | --- |
| Data backup agent file | `data_backup_parameter_file` | hdbbackint agent path |
| - | | |
| Catalog backup using backint | `catalog_backup_using_backint` | `true` |
| Catalog backup agent file | `catalog_backup_parameter_file` | hdbbackint agent path |
| - | | |
| ***OPTIONAL, IF ENABLED:***<br/> Log backup using backint | `log_backup_using_backint` | ***OPTIONAL, IF ENABLED:***<br/> `true` |
| ***OPTIONAL, IF ENABLED:***<br/> Log backup agent file | `log_backup_parameter_file` | ***OPTIONAL, IF ENABLED:***<br/> hdbbackint agent path |

## Known Issues and Errors

### Microsoft Azure Backup agent

**Preregistration script:**
- RHEL 8.x with MS Azure Recovery Services Vault (RSV) attempts to run `yum install python-azure-agent` instead of `yum install WALinuxAgent`. Error appears to be due to `Package_WaAgent_RHEL="python-azure-agent"`.
- The Shell Function `Package.RequirePython()` does not have a case for RHEL, which means RHEL will always use Python 2.x. For RHEL 8.x, this will install Python 2.x (which was removed as the default of the OS Distribution).
- The Shell Function `Check.Waagent()` does not operate correctly because a command is commented out `#systemctl restart waagent.service`.
- The Shell Function `Check.Wireserver()`, `Check.IMDS()` and `Check.AadConnectivity()` assumes the host is running on Microsoft Azure platform, it blocks usage of Microsoft Azure Recovery Services Vault from on-premise hosts.
- The Shell Function `Plugin.CreateUser()` results in `Failed to create BACKUP_KEY_NAME: 'Operation succeed.'`
