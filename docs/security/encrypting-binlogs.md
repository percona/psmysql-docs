# Encrypt Binary Log Files and Relay Log Files

Binary log file and relay log file encryption at rest ensures the
server-generated binary logs are encrypted in persistent storage.

## Upgrade from Percona Server for MySQL 8.0.15-5 or later

As of 8.0.15-5, Percona Server for MySQL uses the upstream
implementation of the binary log file and relay log file encryption.

The encrypt-binlog variable is
removed, and the related command-line option `–encrypt-binlog` is not
supported. It is important to remove the encrypt-binlog variable from your
configuration file before you attempt to upgrade either from another release
in the Percona Server for MySQL 8.0 series or from Percona Server for MySQL 5.7.
Otherwise, a server boot error is generated and reports an unknown
variable.

The implemented binary log file encryption is compatible with the older
format. The encrypted binary log file used in a previous version of MySQL 8.0
series or Percona Server for MySQL series is supported.

## Architecture

The Binary log encryption uses the following tiers:

* File password

* Binary log file encryption key

The file password encrypts the content of a single binary file or relay log
file. The binary log encryption key encrypts the file password and the key
is stored in the keyring.

## Implementation

After you have enabled the `binlog_encryption` variable and the keyring is
available, you can encrypt the data content for new binary log files and relay
log files. Only the data content is encrypted. The server generates a MySQL error if you attempt to encrypt a binary log file or
relay log file without a keyring.

In replication, the source maintains the binary log and the replica maintains a binary
log copy called the relay log. The source uses SSL connections to encrypt the stream, and the events
are re-executed on the replica. The source and replicas can have separate
keyring storage and different keyring plugins.

The server rotates the binary log and relay log files if `binlog_encryption` = `OFF`. All new log files are unencrypted. Any encrypted files are not unencrypted.

When an encrypted binary log is dumped, and this operation involves decryption,
use `mysqlbinlog` with the `--read-from-remote-server` option.

!!! note

    The –read-from-remote-server option only applies to the binary logs. Encrypted relay logs can not be dumped or decrypted with this option.

## Enable binary log encryption

In Percona Server for MySQL 8.0.15-5 and later, set the binlog_encryption variable
to `ON` in a startup configuration file, such as `my.cnf`. The default is `OFF`.

```text
binlog_encryption=ON
```

## Verify the encryption

To verify that the binary log encryption option is enabled, run the following
statement:

```{.bash data-prompt="mysql>"}
mysql> SHOW BINARY LOGS;
```

The `SHOW BINARY LOGS` output displays the name, size, and if a binary log file is encrypted or unencrypted.

??? example "Expected output"

    ```text
    +-------------------+----------------+---------------+
    | Log_name          | File_size      | Encrypted     |
    +-------------------+----------------+---------------+
    | binlog.00011      | 72367          | No            |
    | binlog:00012      | 71503          | No            |
    | binlog:00013      | 73762          | Yes           |
    +-------------------+----------------+---------------+
    ```

## Binary log file variables

### `encrypt_binlog`

| Option       | Description      |
|--------------|------------------|
| Command-line | --encrypt-binlog |
| Dynamic      | No               |
| Scope        | Global           |
| Data type    | Boolean          |
| Default      | OFF              |

Percona Server for MySQL 8.0.15-5 removes this variable.

This variable enables or disables the binary log and relay log file encryption.
