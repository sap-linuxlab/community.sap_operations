<!-- BEGIN Title -->
# sap_hana_backint Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_hana_backint` executes range of actions to operate SAP HANA Backint Agents across different Cloud platforms.<br>
Actions:

- 'setup' - Installs and configures the SAP HANA Backint agent.
- 'backup' - Performs a backup operation using the configured Backint agent.
- 'clean' - Executes cleanup operation using hanacleaner.py.

Supported Cloud platforms solutions:

- Amazon Web Services S3 (`aws_s3`)
- Azure Backup to Microsoft Azure Recovery Services Vault powered by Azure Blob Storage (`azure_backup_rsv`)
- IBM Cloud Object Storage (COS), S3 protocol compatible (`ibm_cos_s3`)
- Google Cloud Storage (`gcs`)
<!-- END Description -->

## Prerequisites
<!-- BEGIN Prerequisites -->
> The Ansible execution user must have `sudo` privileges configured to allow running commands as the `<sid>adm` user of the target SAP system.

### Requirements for aws_s3
- AWS service account keys or IAM role attached to host.
- AWS S3 Bucket created with versioning enabled.
- Compatible Python3 version with Backint agent. See SAP Note 2935898 for more details.
    - Python 3.7 for agent version 1.2.20 and earlier
    - Python 3.11 for agent version 1.2.21 and later
- Python3 library `zstandard` installed, when compression is set to `zstd` (default).

### Requirements for azure_backup_rsv
> **This Ansible role does not configure complete Backint setup for Azure, only pre-registration!**<br>
> Manual post steps are required in Azure Cloud Console: Discovering the database instances and enabling the Backup Policy.

### Requirements for ibm_cos_s3
- IBM Cloud API key.
- IBM Cloud Object Storage (COS) Bucket created with versioning enabled.
- Compatible Python3 version with Backint agent. See SAP Note 2935898 for more details.
    - Python 3.7 for agent version 1.2.20 and earlier
    - Python 3.11 for agent version 1.2.21 and later
- Python3 library `zstandard` installed, when compression is set to `zstd` (default).

### Requirements for gcs
- Cloud Storage bucket created.
- Package `google-cloud-sap-agent` installed on host. This package is included in Google Cloud images.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

### Execution Flow
<!-- BEGIN Execution Flow -->
Action `setup`:

1. Assert and validate all variables for selected action and platform.
2. Detect existing SAP System IDs and Instances on host.
3. Configure platform-specific backint agent.
4. Configure SYSTEMDB backup user and `hdbuserstore`.
5. Detect tenant databases.
6. Configure tenant backup users and `hdbuserstore`.

Action `backup`:

1. Assert and validate all variables for selected action and platform.
2. Detect existing SAP System IDs and Instances on host.
3. Detect tenant databases.
4. Execute SYSTEMDB backup via `hdbbackint`.
5. Execute tenant databases backup via `hdbbackint`.

Action `clean`:

1. Assert and validate all variables for selected action and platform.
2. Detect existing SAP System IDs and Instances on host.
3. Detect tenant databases.
4. Check if `hanacleaner.py` script exists.
5. Execute `hanacleaner.py` for SYSTEMDB backup cleanup.
6. Execute `hanacleaner.py` for tenant databases backup cleanup.

<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of configuring Backint agent on `aws_s3` platform.

```yaml
---
- name: Ansible Play for SAP HANA Backint
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_backint
      ansible.builtin.include_role:
        name: community.sap_operations.sap_hana_backint
      vars:
        sap_hana_backint_action: 'setup'
        sap_hana_backint_platform: 'aws_s3'
        sap_hana_backint_sid: 'H01'
        sap_hana_backint_system_backup_password: 'my_system_password'
        sap_hana_backint_tenant_backup_password: 'my_tenant_password'
        sap_hana_backint_aws_s3_definition:
          auth: 'key'
          bucket: 'my_bucket'
          region: "my_aws_region"
          access_key: "my_access_key"
          secret_access_key: "my_secret_access_key"
          trace_default_level: 'info'
          trace_sdk_level: 'warning'
          compression_type: 'zstd'
          compression_level: '1'
          python_path: '/usr/bin/python3.11'
          agent_path: '/software/sap_hana_extracted/SAP_HANA_DATABASE/server/'
```

Example of executing backup on `gcs` platform:

```yaml
---
- name: Ansible Play for SAP HANA Backint
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_backint
      ansible.builtin.include_role:
        name: community.sap_operations.sap_hana_backint
      vars:
        sap_hana_backint_action: 'backup'
        sap_hana_backint_platform: 'gcs'
        sap_hana_backint_sid: 'H01'
        sap_hana_backint_gcs_definition:
          bucket: 'my_bucket'
```

Example of executing cleanup on `azure_backup_rsv` platform:

```yaml
---
- name: Ansible Play for SAP HANA Backint
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_backint
      ansible.builtin.include_role:
        name: community.sap_operations.sap_hana_backint
      vars:
        sap_hana_backint_action: 'clean'
        sap_hana_backint_platform: 'azure_backup_rsv'
        sap_hana_backint_sid: 'H01'
```

<!-- END Execution Example -->

## Testing
This Ansible Role has been tested in following scenarios.
Operating systems:

 - SUSE Linux Enterprise Server for SAP applications 15 SP6 and SP7 (SLE4SAP)

SAP Products:

- SAP HANA 2.0 SP08

<!-- BEGIN Further Information -->
## Further Information
Documentation sources that were used to configure this Ansible Role.

### SAP HANA Backint Agents
- [SAP HANA Backint Agent for Amazon S3 - SAP Note 2935898](https://launchpad.support.sap.com/#/notes/2935898), supports AWS S3 and IBM COS. For CPU architectures x86_64 and ppc64le.
- [Microsoft Azure Backup Plugin for SAP HANA](https://docs.microsoft.com/en-us/azure/backup/sap-hana-db-about), to store backups with Microsoft Azure Recovery Services Vault (RSV) powered by Azure Blob Storage. For CPU architectures x86_64 only. See [SAP Note 2756788](https://launchpad.support.sap.com/#/notes/2756788) and [blog post](https://docs.azure.cn/en-us/backup/backup-azure-sap-hana-database).
- [Google Cloud Storage Backint agent for SAP HANA](https://docs.cloud.google.com/sap/docs/agent-for-sap/latest/configure-backint-backup-recovery#enable_backint), using Google Cloud Storage (GCS) Buckets. For CPU architectures x86_64 only. See [SAP Note 2705632](https://launchpad.support.sap.com/#/notes/2705632).

### Scripts
- [SAP Note 2399996 - How-To: Configuring automatic SAP HANA Cleanup with SAP HANACleaner](https://launchpad.support.sap.com/#/notes/2399996). An open-source project - https://github.com/chriselswede/hanachecker

### Known Issues and Errors

####  Microsoft Azure Backup agent

**Pre-registration script:**

- RHEL 8.x with MS Azure Recovery Services Vault (RSV) attempts to run `yum install python-azure-agent` instead of `yum install WALinuxAgent`.<br>
  Error appears to be due to `Package_WaAgent_RHEL="python-azure-agent"`.
- The Shell Function `Package.RequirePython()` does not have a case for RHEL, which means RHEL will always use Python 2.x.<br>
  For RHEL 8.x, this will install Python 2.x (which was removed as the default of the OS Distribution).
- The Shell Function `Check.Waagent()` does not operate correctly because a command is commented out `#systemctl restart waagent.service`.
- The Shell Function `Check.Wireserver()`, `Check.IMDS()` and `Check.AadConnectivity()` assumes the host is running on Microsoft Azure platform,<br>
  it blocks usage of Microsoft Azure Recovery Services Vault from on-premise hosts.
- The Shell Function `Plugin.CreateUser()` results in `Failed to create BACKUP_KEY_NAME: 'Operation succeed.'`

<!-- END Further Information -->

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
### sap_hana_backint_action
- _Type:_ `string`

Sets the action to perform with this Ansible Role.<br>
Options:

- `setup` - Installs and configures the SAP HANA Backint agent.
- `backup` - Triggers a backup operation using the configured Backint agent.
- `clean` - Executes cleanup operation using hanacleaner.py.

### sap_hana_backint_platform
- _Type:_ `string`

Sets the target platform for Backint operations.<br>
Options:

- `aws_s3` - Use Amazon Web Services S3 as the storage backend.
- `azure_backup_rsv` - Use Azure Backup Recovery Services as the storage backend.
- `ibm_cos_s3` - Use IBM Cloud Object Storage S3 as the storage backend.
- `gcs` - Use Google Cloud Storage as the storage backend.

### sap_hana_backint_sid
- _Type:_ `string`

The SAP HANA System ID (SID).<br>

### sap_hana_backint_target_database
- _Type:_ `string`
- _Default:_ `all`

Specifies which database(s) to target for the backint action.<br>
Options:

- `all` - Target both SYSTEMDB and all specified tenant databases.
- `system` - Target only the SYSTEMDB.
- `tenant` - Target only the tenant databases.

### sap_hana_backint_tenants
- _Type:_ `list`

A list of SAP HANA Tenant SIDs to perform operations on.<br>
If left empty, tenant-specific tasks will be executed on all detected tenants.<br>
If listed tenant is not detected, it will be skipped.

### sap_hana_backint_hanacleaner
- _Type:_ `boolean`
- _Default:_ `true`

Enable integration with hanacleaner.py script for automatic cleanup.

### sap_hana_backint_system_backup_user
- _Type:_ `string`
- _Default:_ `HDB_SYSTEM_BACKUP_USER`

The name of database user for performing SYSTEM backup.

### sap_hana_backint_system_backup_password
- _Type:_ `string`

The password of database user defined in `sap_hana_backint_system_backup_user`.<br>
This is used only if existing hdbuserstore entry is not found during `setup` action.

### sap_hana_backint_tenant_backup_user
- _Type:_ `string`
- _Default:_ `HDB_TENANT_{{ sap_hana_backint_sid | upper }}_BACKUP_USER`

The name of database user for performing Tenant database backups.<br>
**NOTE:** This is used for all tenants, unless you restrict them with `sap_hana_backint_tenants` variable.

### sap_hana_backint_tenant_backup_password
- _Type:_ `string`

The password of database user defined in `sap_hana_backint_tenant_backup_user`.<br>
This is used only if existing hdbuserstore entry is not found during `setup` action.<br>
**NOTE:** This is used for all tenants, unless you restrict them with `sap_hana_backint_tenants` variable.

### sap_hana_backint_aws_s3_definition
- _Type:_ `dict`

Dictionary with platform specific variables when `sap_hana_backint_platform` is `aws_s3`.

- **auth** `Required`<br>
  _Type:_ `string`<br>
  Default method of authentication. Options: key, implicit, role.

- **bucket** `Required`<br>
  _Type:_ `string`<br>
  Name of the S3 bucket.

- **region** `Required`<br>
  _Type:_ `string`<br>
  Region of the S3 bucket.

- **access_key** `Required when auth: key`<br>
  _Type:_ `string`<br>
  AWS access key.

- **secret_access_key** `Required when auth: key`<br>
  _Type:_ `string`<br>
  AWS secret access key.

- **role_name** `Required when auth: role`<br>
  _Type:_ `string`<br>
  An IAM role that allows access to the S3 bucket.

- **trace_default_level**<br>
  _Type:_ `string`<br>
  _Default:_ `info`<br>
  Trace level.<br>
  Options: `critical`, `error`, `warning`, `info`, `debug`

- **trace_sdk_level**<br>
  _Type:_ `string`<br>
  _Default:_ `warning`<br>
  Trace level for the sdk.<br>
  Options: `critical`, `error`, `warning`, `info`, `debug`

- **compression_type**<br>
  _Type:_ `string`<br>
  _Default:_ `zstd`<br>
  Enables or disables compression.<br>
  Options: `zstd`, `none`

- **compression_level**<br>
  _Type:_ `string`<br>
  _Default:_ `1`<br>
  zstd compression level between 1 and 10.

- **python_path** `Required`<br>
  _Type:_ `string`<br>
  Python executable path, where compatible Python 3 is already installed.<br>
  This file must be executable by <sid>adm user. Example: `/usr/bin/python3.11`.

- **agent_path** `Required`<br>
  _Type:_ `string`<br>
  Path to aws-s3-backint-<version>-<platform>.tar.gz script or its directory.<br>
  Example: `/software/sap_hana_extracted/SAP_HANA_DATABASE/server/aws-s3-backint-1.2.32.tar.gz`.

- **agent_directory**<br>
  _Type:_ `string`<br>
  Path to custom backint directory, where agent will be extracted.

Example:
```yaml
sap_hana_backint_aws_s3_definition:
  auth: 'key'
  bucket: 'my_bucket'
  region: "my_aws_region"
  access_key: "my_access_key"
  secret_access_key: "my_secret_access_key"
  trace_default_level: 'info'
  trace_sdk_level: 'warning'
  compression_type: 'zstd'
  compression_level: '1'
  python_path: '/usr/bin/python3.11'
  agent_path: '/software/sap_hana_extracted/SAP_HANA_DATABASE/server/'
  agent_directory: /backint/
```

### sap_hana_backint_ibm_cos_s3_definition
- _Type:_ `dict`

Dictionary with platform specific variables when `sap_hana_backint_platform` is `ibm_cos_s3`.

- **bucket** `Required`<br>
  _Type:_ `string`<br>
  Name of the S3 bucket.

- **region** `Required`<br>
  _Type:_ `string`<br>
  Region of the S3 bucket.

- **api_key** `Required`<br>
  _Type:_ `string`<br>
  IBM Cloud API key.

- **resource_instance_id** `Required`<br>
  _Type:_ `string`<br>
  IBM Cloud Resource Instance ID.

- **endpoint_url** `Required`<br>
  _Type:_ `string`<br>
  Custom endpoint URL for IBM COS S3.

- **trace_default_level**<br>
  _Type:_ `string`<br>
  _Default:_ `info`<br>
  Trace level.<br>
  Options: `critical`, `error`, `warning`, `info`, `debug`

- **trace_sdk_level**<br>
  _Type:_ `string`<br>
  _Default:_ `warning`<br>
  Trace level for the sdk.<br>
  Options: `critical`, `error`, `warning`, `info`, `debug`

- **compression_type**<br>
  _Type:_ `string`<br>
  _Default:_ `zstd`<br>
  Enables or disables compression.<br>
  Options: `zstd`, `none`

- **compression_level**<br>
  _Type:_ `string`<br>
  _Default:_ `1`<br>
  zstd compression level between 1 and 10.

- **python_path** `Required`<br>
  _Type:_ `string`<br>
  Python executable path, where compatible Python 3 is already installed.<br>
  This file must be executable by <sid>adm user. Example: `/usr/bin/python3.11`.

- **agent_path** `Required`<br>
  _Type:_ `string`<br>
  Path to aws-s3-backint-<version>-<platform>.tar.gz script or its directory.<br>
  Example: `/software/sap_hana_extracted/SAP_HANA_DATABASE/server/aws-s3-backint-1.2.32.tar.gz`.

- **agent_directory**<br>
  _Type:_ `string`<br>
  Path to custom backint directory, where agent will be extracted.

Example:
```yaml
sap_hana_backint_ibm_cos_s3_definition:
  bucket: 'my_bucket'
  region: "my_aws_region"
  api_key: "my_api_key"
  resource_instance_id: "my_resource_instance_id"
  endpoint_url: "my_endpoint_url"
  trace_default_level: 'info'
  trace_sdk_level: 'warning'
  compression_type: 'zstd'
  compression_level: '1'
  python_path: '/usr/bin/python3.11'
  agent_path: '/software/sap_hana_extracted/SAP_HANA_DATABASE/server/'
  agent_directory: /backint/
```

### sap_hana_backint_gcs_definition
- _Type:_ `dict`

Dictionary with platform specific variables when `sap_hana_backint_platform` is `gcs`.

- **bucket** `Required`<br>
  _Type:_ `string`<br>
  Name of the Cloud Storage bucket.

- **compress**<br>
  _Type:_ `boolean`<br>
  _Default:_ `true`<br>
  Enables or disables compression.

```yaml
sap_hana_backint_gcs_definition:
  bucket: 'my_bucket'
  compress: true
```

### sap_hana_backint_instance_number
- _Type:_ `string`

The SAP HANA Instance Number.<br>
The default value is number of first instance found on the host.

### sap_hana_backint_setup_hostname
- _Type:_ `string`<br>
- _Default:_ `{{ ansible_hostname }}`

Specifies the hostname to be used in Backint configuration during `setup` action.

### sap_hana_backint_setup_log_backint
- _Type:_ `boolean`<br>
- _Default:_ `false`

Enables configuration of log backup with Backint during `setup` action.<br>
This will also set `log_mode` if `sap_hana_backint_setup_log_mode` is defined.

### sap_hana_backint_setup_log_mode
- _Type:_ `boolean`

Specifies the log mode to enable during `setup` action.<br>
This is applied to both SYSTEMDB and tenant databases if applicable.<br>
Options: `normal`, `overwrite`.

### sap_hana_backint_clean_retained_backups
- _Type:_ `boolean`<br>
- _Default:_ `4`

Specifies number of backups to retain when hanacleaner.py is executed during action `clean`.
<!-- END Role Variables -->
