# Audit Log Filter file naming conventions

## Name qualities

The audit log filter file name has the following qualities:

* Optional directory name
* Base name
* Optional suffix

Using either [compression](audit-log-filter-compression-encryption.md) or [encryption](audit-log-filter-compression-encryption.md) adds the following suffixes:

* Compression adds the `.gz` suffix
* Encryption adds the `pwd_id.enc` suffix

The `pwd_id` represents the password used for encrypting the log files. The audit log filter component stores passwords in the keyring.

You can combine compression and encryption, which adds both suffixes to the `audit_filter.log` name.

The following table displays the possible ways a file can be named:

| Default name            | Enabled feature                |
| ----------------------- | ------------------------------ |
| audit.log               | No compression or encryption   |
| audit.log.gz            | Compression                    |
| audit.log.pwd_id.enc    | Encryption                     |
| audit.log.gz.pwd_id.enc | Compression, encryption        |

### Encryption ID format

The format for `pwd_id` is the following:

* A UTC value in `YYYYMMDDThhmmss` format that represents when the password was created
* A sequence number that starts at `1` and increases if passwords have the same timestamp value

The following are examples of pwd_id values:

```text
20230417T082215-1
20230301T061400-1
20230301T061400-2
```

The following example is a list of the audit log filter files with the `pwd_id`:

```text
audit_filter.log.20230417T082215-1.enc
audit_filter.log.20230301T061400-1.enc
audit_filter.log.20230301T061400-2.enc
```

The current password has the largest sequence number.

## Renaming operations

During initialization, the component checks if a file with that name exists. 
If it does, the component renames the file. The component writes to an empty file.

During termination, the component renames the file.


