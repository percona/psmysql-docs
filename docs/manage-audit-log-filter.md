# Manage the Audit Log Filter files

Audit log files can fill disks and grow without bound unless you cap them.

Use rotation to rename the active file and start a fresh one with the original name—manually with a UDF or automatically by size.

With automatic rotation enabled, prune old files by age, total size, or both.

## Manual log rotation

[`audit_log_filter.rotate_on_size`](audit-log-filter-variables.md#audit_log_filterrotate_on_size) defaults to 1 GB. Set it to `0` to disable automatic rotation; you must rotate by hand.

Run `SELECT audit_log_rotate();` to rotate immediately. Requires `AUDIT_ADMIN`.

Starting in Percona Server for MySQL 8.4.9-9, rotation finishes immediately in `ASYNCHRONOUS` and `PERFORMANCE` strategies instead of waiting on the background flush thread. Several rotations in the same second add a numeric suffix (for example `audit_filter.20250401T120000-1.log`) so files are not overwritten.

Pruning runs when `audit_log_filter.max_size` or `audit_log_filter.prune_seconds` is greater than zero. The server prunes immediately when you set either variable, and again on rotation (automatic when `rotate_on_size` &gt; 0, or manual via `audit_log_rotate()`). There is no background timer — with automatic rotation disabled, schedule manual rotations or rely on the prune that runs when you set the variable.

After rotation, delete archived files you no longer need yourself. [`audit_log_read()`](audit-log-filter-variables.md#audit_log_read) can read renamed files only if their names still match the active naming pattern.

## Additional reading

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — rotation, size, and pruning options
* [Audit Log Filter naming conventions](audit-log-filter-naming.md)
* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
* [Audit Log Filter security](audit-log-filter-security.md)
* [Audit Log Filter overview](audit-log-filter-overview.md)
