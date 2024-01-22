#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2022 Red Hat, Project Atmosphere
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: hana_backup

author:
  - Ondra Machacek (@machacekondra)

short_description: Create SAP HANA database file backup

description: |
  Create backup of SAP HANA database to files or using BACKINT interface
  Full Backup: complete SAP HANA database backup.
  Differential Backup: the data changed since the last full data backup.
  Incremental Backup: the data changed since the last full data backup or the last delta backup.
  https://help.sap.com/docs/SAP_HANA_PLATFORM/6b94445c94ae495c83a19646e7c3fd56/15b4aa82ae7544f78f809e35add006ce.html

version_added: 1.1.0

seealso:
  - module: sap.sap_operations.hana_backup

options:
  binary_path:
    description: |
      Path to hdbsql binary.
    type: str
  host:
    description:
      - Name of the host on which the database instance is running.
    type: str
  instance_number:
    description:
      - Instance number of the database engine.
    type: str
  database_user_password:
    description:
      - Password for HANA SYSTEM database user. Or a user specified in C(database_user) parameter.
    type: str
  database_user:
    description:
      - A user which to be used to connect to database. SYSTEM user is used if no user is specified.
    type: str
  hdbsqluserstore_key:
    description:
      - hdbuserstore record to be used to connect to database.
    type: str
  type:
    description:
      - Backup type.
      - Delta backups can only be created after a data backup has been created.
    choices: [INCREMENTAL, DIFFERENTIAL, FULL]
    default: FULL
    type: str
  database_name:
    description: |
      SAP HANA system tenant or SYSTEMDB to backup. If not provided SYSTEMDB is default value.
      From SYSTEMDB other tenatns can be backed up. From tenant only itself can be backed up.
    type: str
    default: "SYSTEMDB"
  comment:
    description:
      - Comment to be included into backup.
    type: str
  destination:
    description: |
      Directory where where backup data are stored for file backups.
      <hanasid>adm user should have write permissions to that directory.
    type: str
  prefix:
    description:
      - The data backup files are prepended with the prefix.
      - Previous backup files will be overwritten if prefix was already
        used before (for file backups).
    type: str
  wait:
    description:
      - Wait for the operation to complete before returning.
      - If set to C(true), module will wait on backup task to complete.
      - If set to C(false), module will schedule the backup task and return
        immediately.
      - Please be aware you cannot run two backups in parallel for one SAP HANA database.
    type: bool
    default: true
  backend:
    description:
      - Create the backup in the file or using the third-party backup tool with BACKINT interface.
    type: str
    choices: [FILE, BACKINT]
    default: FILE
  tooloption:
    description:
      - String that is forwarded to the third-party backup tool.
      - This parameter is used only in case C(type) is I(BACKINT).
    type: str
"""

EXAMPLES = r"""
- name: Fetch the binary path of the hdbsql
  sap.sap_operations.parameter_info:
    instance_number: "00"
    name: DIR_INSTANCE
  register: dir_instance

- name: Create a full HANA backup for SYSTEMDB
  sap.sap_operations.hana_backup:
    database_user_password: CHANGEME
    prefix: MONDAY
    database_name: SYSTEMDB
    binary_path: "{{ dir_instance.parameter_value | first }}"

- name: Create a full HANA backup for RHE tenant
  sap.sap_operations.hana_backup:
    database_user_password: CHANGEME
    prefix: MONDAY
    binary_path: "{{ dir_instance.parameter_value | first }}"

- name: Create a full HANA backup for RHE tenant - all options used
  sap.sap_operations.hana_backup:
    database_user_password: CHANGEME
    database_name: RHE
    prefix: MONDAY
    destination: /backups
    comment: Created with ansible
    binary_path: "/my/custom/path"
    wait: false
"""

RETURN = r""" # """


import os

from ansible.module_utils.basic import AnsibleModule


def get_sql(module):
    sql_wait = "" if module.params.get("wait") else "ASYNCHRONOUS"
    backup_type = (
        "" if module.params.get("type") == "FULL" else module.params.get("type")
    )
    sql_comment = (
        "COMMENT '{0}'".format(module.params.get("comment"))
        if module.params.get("comment")
        else ""
    )
    sql_for_tenant = (
        ""
        if module.params.get("database_name") == "SYSTEMDB"
        else "FOR {0}".format(module.params["database_name"])
    )

    sql_tooloption = ""
    if module.params.get("backend") == "BACKINT":
        sql_tooloption = (
            "TOOLOPTION '{0}'".format(module.params.get("tooloption"))
            if module.params.get("tooloption")
            else ""
        )

    sql_prefix_destination = os.path.join(
        module.params.get("destination"), module.params.get("prefix")
    )
    sql_command = "BACKUP DATA {0} {1} USING {2}('{3}') {4} {5} {6}".format(
        backup_type,
        sql_for_tenant,
        module.params.get("backend"),
        sql_prefix_destination,
        sql_tooloption,
        sql_wait,
        sql_comment,
    )

    binary_path = os.path.join(module.params.get("binary_path"), "hdbsql")
    args = [binary_path]

    if module.params.get("host"):
        args.extend(["-n", module.params.get("host")])

    if module.params.get("instance_number"):
        args.extend(["-i", module.params.get("instance_number")])

    if module.params.get("hdbsqluserstore_key"):
        args.extend(["-U", module.params.get("hdbsqluserstore_key")])
    elif module.params.get("database_user_password"):
        user = (
            module.params.get("database_user")
            if module.params.get("database_user")
            else "SYSTEM"
        )
        args.extend(["-u", user, "-p", module.params.get("database_user_password")])

    args.append(sql_command.strip())
    return args


def run_command(module, args):
    return module.run_command(args=args)


def ensure_backup_created(module):
    if module.check_mode:
        return True, "", ""

    args = get_sql(module)
    rc, stdout, err = run_command(module, args)
    if rc != 0:
        module.fail_json(cmd=args, rc=rc, stdout=stdout, msg=err)

    return True, stdout, err, args


def main():
    module_args = dict(
        host=dict(type="str"),
        instance_number=dict(type="str"),
        database_user_password=dict(type="str", no_log=True),
        database_user=dict(type="str"),
        hdbsqluserstore_key=dict(type="str", no_log=False),
        database_name=dict(type="str", default="SYSTEMDB"),
        type=dict(
            type="str", choices=["INCREMENTAL", "DIFFERENTIAL", "FULL"], default="FULL"
        ),
        destination=dict(type="str", default=""),
        prefix=dict(type="str", default=""),
        comment=dict(type="str", default=""),
        wait=dict(type="bool", default=True),
        binary_path=dict(type="str", default=""),
        backend=dict(type="str", choices=["FILE", "BACKINT"], default="FILE"),
        tooloption=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[["database_user_password", "hdbsqluserstore_key"]],
    )
    changed, out, err, args = ensure_backup_created(module)
    module.exit_json(changed=changed, stdout=out, stderr=err, cmd=args)


if __name__ == "__main__":
    main()
