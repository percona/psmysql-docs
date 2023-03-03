# Data at Rest Encryption

The following system variables, status variables, and options have been removed in Percona Server for MySQL 8.0.31-23.

| Variable name                                    |
|--------------------------------------------------|
| `innodb_encryption_rotation_pages_read_from_cache` |
| `innodb_encryption_rotation_pages_read_from_disk`  |
| `innodb_encryption_rotation_pages_modified`        |
| `innodb_encryption_rotation_pages_flushed`         |
| `innodb_encryption_rotation_estimated_iops`        |
| `innodb_encryption_rotation_list_length`           |
| `innodb_num_pages_encrypted`                       |
| `innodb_num_pages_decrypted`                       |
| `innodb_encryption_threads`                        |
| `innodb_encryption_rotate_key_age`                 |
| `innodb_encryption_rotation_loops`                 |
| `innodb_default_encryption_key_id`                 |
| `rotate_system_key and any dependencies`           |


The following system variable options have been changed in Percona Server for MySQL 8.0.31-23.

| Variable name                                    | Changed              |
|--------------------------------------------------|-----------------------------------|
| `default_table_encryption`                         | Changed to two options: ON or OFF |
| `innodb_sys_tablespace_encrypt`                    | Changed to Boolean                |

Data security is a concern for institutions and organizations. `Transparent
Data Encryption (TDE)` or `Data at Rest Encryption` encrypts
data files. Data at rest is
any data that is not accessed or changed frequently, stored on different
types of storage devices. Encryption ensures that if an unauthorized user
accesses the data files from the file system, the user cannot read the contents.

If the user uses master key encryption, the MySQL keyring plugin stores the
InnoDB master key, used for the master key encryption implemented by *MySQL*.
The master key is also used to encrypt redo logs, and undo logs, along with the
tablespaces.

The InnoDB tablespace encryption has the following components:

* The database instance has a master key for tablespaces and a master key
for binary log encryption.

* Each tablespace has a tablespace key. The key is used to encrypt the
Tablespace data pages. Encrypted tablespace keys are written on
the tablespace header. In the master key implementation, the tablespace key
cannot be changed unless you rebuild the table.

Two separate keys allow the master key to be rotated in a minimal operation.
When the master key is rotated, each tablespace key is decrypted and
re-encrypted with the new master key. The key rotation only reads and writes to the first page of each tablespace file (.ibd).

An InnoDB tablespace file is comprised of multiple logical and physical pages.
Page 0 is the tablespace header page and keeps the metadata for the tablespace.
The encryption information is stored on page 0 and the tablespace key is
encrypted.

An encrypted page is decrypted at the I/O
layer, added to the buffer pool, and used to access the data. A buffer pool page is not encrypted. The page is encrypted by the I/O layer before the page is flushed to disk.

## Percona XtraBackup support

Percona XtraBackup version 8 supports the backup of encrypted general tablespaces. 

Percona XtraBackup only supports features that are [Generally Available (GA)](../glossary.md#general-availability-ga) in Percona Server for MySQL. Due to time constraints, GA features may be supported in a later Percona XtraBackup release. Review the [Percona XtraBackup release notes](https://docs.percona.com/percona-xtrabackup/8.0/release-notes.html) for more information.
