# Log encryption

Describes the redo log encryption and the undo log encryption.

## Redo Log encryption

Use the `innodb_redo_log_encrypt` option to enable or disable redo log data encryption. By default, the encryption of the redo log is disabled.

InnoDB uses the tablespace encryption key to encrypt the redo log data. If the encryption is enabled, when the server encrypts and writes the redo log data to the disk. When the server reads the redo log data from disk, the data is decrypted.

Changing the encryption does not change existing redo log pages. Setting the option to `ON`, any existing redo log pages remain unencrypted; writing new pages to disk encrypts them. Setting the option to `OFF`, any existing encrypted pages remain encrypted; writing new pages to disk are unencrypted.

The metadata for the redo log encryption includes the tablespace encryption key and is stored the in redo log file header. Removing the encryption metadata disables the redo log encryption.

Without the keyring plugin or component or the encryption key, a normal restart is not possible. InnoDB scans the redo log pages during startup. If the encryption options are not available, InnoDB cannot scan these pages. A forced startup without the redo logs is possible.

## Option

### `innodb_redo_log_encrypt`

| Variable     | Description               |
|--------------|---------------------------|
| Command-line | `--innodb-redo-log-encrypt[= {ON \| OFF}]` |
| Dynamic      | Yes                       |
| Scope        | Global                    |
| Data type    | Boolean                      |
| Default      | OFF                       |

| Option | Description |
|---|---|
| ON | This option is a compatibility alias for the master_key. Any existing redo log pages remain unencrypted; new pages are encrypted when written to disk.  |
| OFF | Any existing encrypted pages remain encrypted; new pages are unencrypted. |


Determines the encryption for the table redo log data. The default option for the variable is `OFF`.

## Undo Log encryption

Use the `innodb_undo_log_encrypt` option to enable or disable undo log data encryption. By default, the option to encrypt the undo log data is disabled.

InnoDB uses the tablespace encryption key to encrypt the undo log data. If the encryption is enabled, when the server encrypts and writes the undo log data to the disk. When the server reads the undo log data from disk, the data is decrypted.

Changing the encryption does not change existing undo log pages. Setting the option to `ON`, any existing pages remain unencrypted; writing new pages to disk encrypts them. Setting the option to `OFF`, any existing encrypted pages remain encrypted; writing new pages to disk are unencrypted.

The metadata for the redo log encryption includes the tablespace encryption key and is stored the in undo log file header.

The server requires the keyring plugin or keyring component used to encrypt log data until that data is truncated, even if the current option setting is `OFF`. When the undo tablespace is truncated, the encryption header is removed.


## `innodb_undo_log_encrypt`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | `--innodb-undo-log-encrypt[= {ON \| OFF}]` |
| Scope        | Global                    |
| Dynamic      | Yes                       |
| Data type    | Boolean                   |
| Default      | OFF                       |

This system variable defines the encryption status for the undo log data. The default setting is `OFF`, which disables the encryption.

