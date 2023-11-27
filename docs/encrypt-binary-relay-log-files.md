# Encrypt binary log files and relay log files

Encrypt the binary log files and the relay log files to protect them from unauthorized viewing. The encryption uses the Advanced Encryption Standard (AES) symmetric block cipher algorithm. Instead of bits, this algorithm works on bytes.

Any supported encryption keyring plugin or component must be installed and configured to use encryption.

Enabling binary log encryption at system start, the server generates a binary log encryption key before iniatializing the binary log and relay logs. The key encrypts a file password for each binary log, if binary logging is enabled, and relay log. Keys generated from the file passwords encrypt the data in the files.

When used by the server, the binary log encryption key is called the binary log master key. This key can be rotated as needed and only the file password for each file is re-encrypted. 

The binary log index file and relay log index file is never encrypted. Relay log files are encrypted for all channels.

To review if a binary log file is encrypted or not, use the `SHOW BINARY LOGS` statement.

If the server is running, the `BINLOG_ENCRYPTION_ADMIN` privilege is required to enable or disable encryption.

## `binlog_encryption`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | `--binlog-encryption[= {ON \| OFF}]` |
| Scope        | Global                    |
| Dynamic      | Yes                       |
| Data type    | Boolean                   |
| Default      | OFF                       |

This system variable enables binary log file encryption and relay log file encryption on the server. The default value is `OFF`. You can enable encryption for relay log files on a replica without a binary log.

If you set the `binlog_encryption` to `OFF`, the server immediately rotates the binary log file and relay log files and all logging is not encrypted. For any previously encrypted files, the server can still read them and they are not decrypted. 











