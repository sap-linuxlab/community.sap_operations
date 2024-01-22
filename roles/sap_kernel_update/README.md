# sap_kernel_update Ansible Role

Role updates SAP kernel.

## Functionality

A newer SAP kernel is provided in two SAR files - SAPEXE_\*.SAR and SAPEXEDB_\*.SAR.
Role extracts each SAR file, creates directory with new SAP kernel and replaces old kernel with new kernel.
SAP system is stopped before kernel replacement and started afterwards.

Backup of old SAP kernel is created if revert would be needed.
Backup directory (for example `/usr/sap/RHE/SYS/exe/uc/linuxx86_64-backup-20220329T144751/`)
should be removed manually.

## Requirements

- Most role tasks must be executed under root account.
  Some tasks are executed under sidadm account.
- SAPCAR binary must be installed on the host

<!-- BEGIN: Role Input Parameters -->

## Role Variables

Required parameters:

- [sap_kernel_update_instance](#sap_kernel_update_instance)

- [sap_kernel_update_kernel_path](#sap_kernel_update_kernel_path)

- [sap_kernel_update_new_kernel_path](#sap_kernel_update_new_kernel_path)

- [sap_kernel_update_sid](#sap_kernel_update_sid)

### sap_kernel_update_instance

- _Type:_ `str`
- _Required:_ `True`

The instance number to be managed.

### sap_kernel_update_kernel_path

- _Type:_ `str`
- _Required:_ `True`

Path to directory with installed SAP kernel.

### sap_kernel_update_new_kernel_path

- _Type:_ `str`
- _Required:_ `True`

Path to new kernel.

### sap_kernel_update_sid

- _Type:_ `str`
- _Required:_ `True`

SAP System ID.

### sap_force_update

- _Type:_ `str`
- _Default:_ `False`
- _Required:_ `False`

Update the system if rolling updgrade can't be used. Stop and start the system, so there is downtime.

### sap_kernel_update_backup

- _Type:_ `str`
- _Default:_ `True`
- _Required:_ `False`

Backup previous kernel.

<!-- END: Role Input Parameters -->
