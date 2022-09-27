# Encrypting the Redo Log files

MySQL uses the redo log files to apply changes during data recovery.

Encrypt the redo log files by enabling the innodb_redo_log_encrypt
variable. The default value for the variable is `OFF`.

The Redo log files use the tablespace encryption key.

### `innodb_redo_log_encrypt`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --innodb-redo-log-encrypt |
| Dynamic      | Yes                       |
| Scope        | Global                    |
| Data type    | Text                      |
| Default      | OFF                       |

Determines the encryption for the table redo log data.

When you enable `innodb_redo_log_encrypt` any existing redo log pages stay
unencrypted, and new pages are encrypted when they are written to disk. If you
disable `innodb_redo_log_encrypt` after enabling the variable, any encrypted pages remain encrypted, but the new pages are unencrypted.

As implemented in Percona Server for MySQL 8.0.16-7, the supported values for
innodb_redo_log_encrypt are the following:

* ON

* OFF

* master_key

* keyring_key

!!! note

    **The `keyring_key` value is in tech preview.**

For `innodb_redo_log_encrypt`, the “ON” value is a compatibility alias for
master_key.

After starting the server, an attempt to encrypt the redo log files fails
if you have the following conditions:

* Server started with no keyring specified
* Server started with a keyring, but you specified a redo log encryption method that is different from the previously used method on the server.
