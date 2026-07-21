# Audit Log Filter compression and encryption

## Compression

Enable compression for any [format](audit-log-filter-formats.md) with `audit_log_filter.compression` at server startup.

Allowed values:

* `NONE` — default, no compression
* `GZIP` — GNU zip compression

With both compression and encryption enabled, the component compresses first, then encrypts. To recover a file manually, decrypt, then decompress.

## Encryption

Encrypt any audit log format. The component generates the first password; you may rotate to custom passwords afterward. Passwords live in the keyring—enable a keyring first.

Set `audit_log_filter.encryption` at startup. Values:

* `NONE` — default, no encryption
* `AES` — AES-256-CBC

AES uses a 256-bit key.

Encryption-related functions:

| Function name     | Description          |
| ----------------- | -------------------- |
| audit_log_encryption_password_set() | Stores a password in the keyring. With encryption on, also rotates the log: renames the current file and starts a new file encrypted with the new password.                                           |
| audit_log_encryption_password_get() | With no argument, returns the active password. With a keyring ID, returns that archived or current password by ID. |

`audit_log_filter.password_history_keep_days` controls how long archived passwords stay available. When non-zero, calling `audit_log_encryption_password_set()` can expire older keyring entries.

On startup with encryption enabled, if no audit password exists the component generates one and stores it. Call `audit_log_encryption_password_get()` to inspect it.

## Manually uncompressing and decrypting audit log filter files

Decrypt with OpenSSL, for example:

```bash
openssl enc -d -aes-256-cbc -pass pass:password
    -iter iterations -md sha256
    -in audit.timestamp.log.pwd_id.enc
    -out audit.timestamp.log
```

You need the password and iteration count from `audit_log_encryption_password_get()`.

That function returns JSON, for example for file `audit.20190415T151322.log.20190414T223342-2.enc` with keyring ID `audit-log-20190414T223342-2`:

```sql
SELECT audit_log_encryption_password_get('audit-log-20190414T223342-2');
```

??? example "Expected output"

    ```{.text .no-copy}
    {"password":"{randomly-generated-alphanumeric-string}","iterations":568977}
    ```

## Additional reading

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — encryption and compression options
* [Audit Log Filter security](audit-log-filter-security.md)
* [Audit Log Filter file format overview](audit-log-filter-formats.md)
* [Manage the Audit Log Filter files](manage-audit-log-filter.md)
* [Keyring components and plugins overview](keyring-components-plugins-overview.md)
* [Quickstart component keyring](quickstart-component-keyring.md)
