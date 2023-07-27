# Encrypting the Redo Log data

## Version changes

Percona Server for MySQL 8.0.30-22 changes the data type to Boolean and removes the `master_key` and `keyring_key` options.

Percona Server for MySQL 8.0.16-7 implements the options.

## Overview

MySQL uses the redo log files to apply changes during data recovery.

Writing the redo log data to disk encrypts the data and reading the redo log data from disk unencrypts the data. When the redo log data is in memory, the data is unencrypted. The Redo log data uses the tablespace encryption key.

!!! warning

    After the redo log is enabled, a MySQL 8.0.30 regression prevents disabling the redo log.

After starting the server, an attempt to encrypt the redo log files fails
if you have the following conditions:

* Server started with no keyring specified
* Server started with a keyring, but you specified a redo log encryption method that is different from the previously used method on the server.

Starting with MySQL 8.0.30, the most recent checkpoint and the redo log encryption metadata is stored in the redo log file header.

After enabling redo log encryption, attempting a normal restart without the keyring plugin or keyring component is not possible, since InnoDB scans the redo log pages during startup. Without the keyring plugin or keyring component, this operation is not possible when the redo log pages are encrypted. You can do a forced startup without the redo logs.

## System variable

### `innodb_redo_log_encrypt`

| Variable     | Description               |
|--------------|---------------------------|
| Command-line | --innodb-redo-log-encrypt |
| Dynamic      | Yes                       |
| Scope        | Global                    |
| Data type    | Boolean                      |
| Default      | OFF                       |

| Option | Description |
|---|---|
| ON | This option is a compatibility alias for the master_key. Any existing redo log pages remain unencrypted; new pages are encrypted when written to disk.  |
| OFF | Any existing encrypted pages remain encrypted; new pages are unencrypted. |
| master_key | Removed in Percona Server for MySQL 8.0.30-22 |
| keyring_key | Removed in Percona Server for MySQL 8.0.30-22 |

Determines the encryption for the table redo log data. The default option for the variable is `OFF`.

