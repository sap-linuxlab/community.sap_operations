# sap_kernel_update Ansible Role

Role updates SAP kernel.

# Functionality

A newer SAP kernel is provided in two SAR files - SAPEXE_*.SAR and SAPEXEDB_*.SAR.
Role extracts each SAR file, creates directory with new SAP kernel and replaces old kernel with new kernel.
SAP system is stopped before kernel replacement and started afterwards.

Backup of old SAP kernel is created if revert would be needed.
Backup directory (for example `/usr/sap/RHE/SYS/exe/uc/linuxx86_64-backup-20220329T144751/`)
should be removed manually.

# Requirements

- Most role tasks must be executed under root account.
  Some tasks are executed under sidadm account.
- SAPCAR binary must be installed on the host

# Parameters

See [argument_specs.yml](meta/argument_specs.yml).
