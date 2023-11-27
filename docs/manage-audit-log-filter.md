# Manage the Audit Log Filter files

The Audit Log Filter files have the following potential results:

* Consume a large amount of disk space
* Grow large

You can manage the space by using log file rotation. This operation renames and then rotates the current log file and then uses the original name on a new current log file. You can rotate the file either manually or automatically.

If automatic rotation is enabled, you can prune the log file. This pruning operation can be based on either the log file age or combined log file size.

## Manual log rotation

The default setting for [`audit_log_filter.rotate_on_size`](audit-log-filter-variables.md#audit_log_filter_rotate_on_size) is 1GB. If this option is set to `0`, the audit log filter component does not do an automatic rotation of the log file. You must do the rotation manually with this setting.

The `SELECT audit_log_rotate()` command renames the file and creates a new audit log filter file with the original name. You must have the `AUDIT_ADMIN` privilege. 

The files are pruned if either `audit_log_filter.max_size` or `audit_log_filter.prune_seconds` have a value greater than 0 (zero) and `audit_log_filter.rotate_on_size` > 0.

After the files have been renamed, you must manually remove any archived audit log filter files. The renamed audit log filter files can be read by `audit_log_read()`. The `audit_log_read()` does not find the logs if the name pattern differs from the current pattern.
