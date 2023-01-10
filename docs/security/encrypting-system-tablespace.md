# Encrypt the system tablespace

*Percona Server for MySQL* supports system tablespace encryption. The InnoDB system tablespace may be encrypted with the master key encryption or the keyring encryption with advanced encryption key rotation.

Keyring encryption is a **tech preview** feature.

The limitation is the following:

* You cannot convert the system tablespace from the encrypted state to the
unencrypted state, or the unencrypted state to the encrypted state. If a
conversion is needed, create a new instance with the
system tablespace in the required state and transfer the user tables to that instance.

To enable system tablespace encryption, edit `my.cnf` with the following settings:

* Add the innodb_sys_tablespace_encrypt

* Change the innodb_sys_tablespace_encrypt value to “ON”

System tablespace encryption can only be enabled with the `--initialize`
option

You can create an encrypted table as follows:

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE table_name TABLESPACE=innodb_system ENCRYPTION='Y';
```

## System variables

### `innodb_sys_tablespace_encrypt`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --innodb-sys-tablespace-encrypt |
| Scope        | Global                          |
| Dynamic      | No                              |
| Data type    | Boolean                         |
| Default      | OFF                             |


Enables the encryption of the InnoDB system tablespace.

## Re-encrypt the system tablespace

You can re-encrypt the system tablespace key with master key rotation. When
the master key is rotated, the tablespace key is decrypted and re-encrypt
with the new master key. Only the first page of the tablespace (.ibd) file is
read and written during the key rotation. The tables in the tablespace are not
re-encrypted.

The command is as follows:

```{.bash data-prompt="mysql>"}
mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY;
```
