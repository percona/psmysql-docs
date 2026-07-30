# Audit Log Filter file naming conventions

## Name qualities

An audit log path has:

* Optional directory prefix

* Base file name

* Optional suffix from compression or encryption

[Compression](audit-log-filter-compression-encryption.md) and [encryption](audit-log-filter-compression-encryption.md) append suffixes:

* Compression adds `.gz`.

* Encryption adds `.pwd_id.enc`.

`pwd_id` identifies the keyring entry for the password. The component stores keys in the keyring.

With both features enabled, both suffixes appear, for example on `audit_filter.log`.

Example names:

| Default name            | Enabled feature              |
| ----------------------- | ---------------------------- |
| `audit_filter.log`             | No compression or encryption |
| `audit_filter.log.gz`          | Compression                  |
| `audit_filter.log.pwd_id.enc`  | Encryption                   |
| `audit_filter.log.gz.pwd_id.enc` | Compression and encryption |

### Encryption ID format

Each `pwd_id` contains:

* UTC creation time as `YYYYMMDDThhmmss`.

* A sequence that starts at `1` and increments when several passwords share one timestamp.

Examples:

```text
20230417T082215-1
20230301T061400-1
20230301T061400-2
```

Example encrypted file names:

```text
audit_filter.log.20230417T082215-1.enc
audit_filter.log.20230301T061400-1.enc
audit_filter.log.20230301T061400-2.enc
```

The password with the highest sequence for a given timestamp is the current password.

## Rotation sequence suffix

Multiple rotations in the same second append `-N` so the server never overwrites a prior file:

```text
audit_filter.20250401T120000.log      -- first rotation at 12:00:00
audit_filter.20250401T120000-1.log    -- second rotation at 12:00:00
```

Update parsers to accept the optional `-N` suffix.

## Renaming operations

At startup, when the target path already has a file, the component renames the existing file and opens a new empty file.

At shutdown, the component renames the active log file.

## Additional reading

* [Manage the Audit Log Filter files](manage-audit-log-filter.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.file`

* [Audit Log Filter file format overview](audit-log-filter-formats.md)

* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)

* [Audit Log Filter overview](audit-log-filter-overview.md)
