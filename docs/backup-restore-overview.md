# Backup and restore overview

Backups are data snapshots that are taken at a specific time and are stored in a common location in a common 
format. A backup is only useful for a defined time. 

The following scenarios require a backup to recover:

| **Reason**         | **Description**                                                                                                     |
|--------------------|---------------------------------------------------------------------------------------------------------------------|
| Hardware or host failure       | Issues with disks, such as stalls or broken disks. With cloud services, the instance can be unaccessible or broken. |
| Corrupted data     | This issue can be caused by power outages, the database failed to write correctly and close the file.               |
| User mistake | Deleting data or an update overwriting good data with bad data          |
| Natural disaster or data center failure | Power outage, flooding, or internet issues                                                                                   |
| Compliance         | Required to comply with regulations and standards                                                                   |

## Strategies

Define a backup and restore strategy for each of your databases. The strategies should have the following practices:

| Practice | Description |
|---|--- |
| Retention | How long should you keep the backups. This decision should be based on the organization's data governance policies and the expense of storing the backups. The schedule for backups should match the retention schedule. |
| Document | Document the strategy and any related policies. The documents should include information about the process and any tools used during backup or restore. |
| Encrypt | Encrypt the backup and secure the storage locations |
| Test | Test the backups on a timely basis. |

The backup strategy defines type and the backup frequency,
the hardware required, how the backups are verified, and storing the backups, which also 
includes the backup security. The strategy uses the following metrics:

| **Metric**               | **Description**                          |
|--------------------------|------------------------------------------|
| Recovery Time Objective (RTO)  | How long can the system be down?         |
| Recovery Point Objective (RPO) | How much data can the organization lose? |

The restore strategy defines which user account has the restore responsibility and how and frequency 
of testing the restore process.

These strategies require planning, implementation, and rigorous testing. You must test your
restore process with each type of backup used to validate the backup and measure the recovery time. Automate this testing
as much as possible. You should also document the process. In case of disaster, you can follow the procedures in the
document without wasting time.

If you are using replication, consider using a dedicated replica for backups because the operation can cause a high CPU load.

## Physical backup or logical backup

A backup can be either a physical backup or a logical backup.

### Physical backups

A physical backup copies the files needed to store and recover the database. They can be data files, configuration files,
logs, and other types of files. The physical database can be stored in the cloud, in offline storage, on disc, or tape.

[Percona XtraBackup] takes a physical backup. You can also 
use RDS/LVM Snapshots or the MySQL Enterprise Backup. 

If the server is stopped or down, you can copy the datadir with the `cp` command or the `rsync` command.

### Logical backups

A logical backup contains the structural details. This type of backup contains tables, views, procedures, and functions. 

Tools like [`mysqldump`], 
[`mydumper`], 
[`mysqlpump`], and 
[`mysql shell`] take a logical backup.

### Comparison

| **Comparison** | **Physical backup**                               | **Logical backup**                                            |
|----------------|---------------------------------------------------|---------------------------------------------------------------|
| Content        | The physical database files                       | The tables, users, procedures, and functions                  |
| Restore speed  | Restore can be quick                              | Restore can be slower and does not include file information.  |
| Storage        | Can take more space                               | Based on what is selected, the backup can be smaller          |

[`mysqldump`]: https://dev.mysql.com/doc/refman/{{vers}}/en/mysqldump.html
[`mydumper`]: https://github.com/mydumper/mydumper
[`mysqlpump`]: https://dev.mysql.com/doc/refman/{{vers}}/en/mysqlpump.html
[`mysql shell`]: https://dev.mysql.com/doc/mysql-shell/{{vers}}/en/mysql-shell-utilities-dump-instance-schema.html
[Percona XtraBackup]: https://docs.percona.com/percona-xtrabackup/innovation-release/index.html