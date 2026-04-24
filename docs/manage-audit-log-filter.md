# Manage the Audit Log Filter files

Audit log files can fill disks and grow without bound unless you cap them.

Use rotation to rename the active file and start a fresh file with the original name. Rotate manually with a UDF or automatically by size.

With automatic rotation enabled, prune old files by age, total size, or both.

## Manual log rotation

[`audit_log_filter.rotate_on_size`](audit-log-filter-variables.md#audit_log_filterrotate_on_size) defaults to 1 GB. Set the variable to `0` to disable automatic rotation. You must then rotate by hand.

Run `SELECT audit_log_rotate();` to rotate immediately. The call requires `AUDIT_ADMIN`.

Rotation finishes immediately in the `ASYNCHRONOUS` and `PERFORMANCE` strategies instead of waiting on the background flush thread. Several rotations in the same second add a numeric suffix, for example `audit_filter.20250401T120000-1.log`, so that files are not overwritten.

Pruning runs when `audit_log_filter.max_size` or `audit_log_filter.prune_seconds` is greater than zero and `audit_log_filter.rotate_on_size` is greater than zero.

After rotation, delete archived files you no longer need. [`audit_log_read()`](audit-log-filter-variables.md#audit_log_read) can read renamed files only when the file names still match the active naming pattern.

## Additional reading

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — rotation, size, and pruning options

* [Audit Log Filter naming conventions](audit-log-filter-naming.md)

* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)

* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)

* [Audit Log Filter security](audit-log-filter-security.md)

* [Audit Log Filter overview](audit-log-filter-overview.md)
