# Encrypt system tablespace

## Version changes

Percona Server for MySQL 8.0.31-23 removes keyring encryption with advanced encryption key rotation and associated system variables, status variables, and options.

Keyring encryption is a **tech preview** feature.

## Overview

Percona Server for MySQL supports system tablespace encryption. The InnoDB system tablespace may be encrypted with the master key encryption. The limitation is the following:

* You cannot convert the system tablespace from the encrypted state to the
unencrypted state, or the unencrypted state to the encrypted state. If a
conversion is needed, create a new instance with the
system tablespace in the required state and transfer the user tables to that instance.

To enable system tablespace encryption, edit `my.cnf`, and set the `innodb_sys_tablespace_encrypt` =“ON”

System tablespace encryption can only be enabled with the `--initialize` option

You can create an encrypted table as follows:

```sql
mysql> CREATE TABLE table_name TABLESPACE=innodb_system ENCRYPTION='Y';
```

## System Variables

### `innodb_sys_tablespace_encrypt`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --innodb-sys-tablespace-encrypt |
| Scope        | Global                          |
| Dynamic      | No                              |
| Data type    | Boolean                         |
| Default      | OFF                             |

Enables the encryption of the InnoDB system tablespace.

## Re-Encrypt the System Tablespace

You can re-encrypt the system tablespace key with master key rotation. When
the master key is rotated, the tablespace key is decrypted and re-encrypt
with the new master key. Only the first page of the tablespace (.ibd) file is
read and written during the key rotation. The tables in the tablespace are not
re-encrypted.

```sql
mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY;
```
