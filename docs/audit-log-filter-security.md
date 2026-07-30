# Audit Log Filter security

The Audit Log Filter component writes audit files. Restrict the log directory to trusted operators and ensure that the server can write to the directory.

Logs are plaintext by default and may hold credentials, SQL text, and other sensitive data.

The default file under the data directory is `audit_filter.log`. Override the location with `audit_log_filter.file` at startup.

When the parent directory is missing, the component errors and the server starts without Audit Log Filter active.

Rotation leaves multiple files on disk. Protect every generation.

## Bypassing the OS page cache

Audit log writes pass through the OS page cache by default. On busy servers with high audit throughput, recently written events can persist in kernel buffer memory until the page cache flushes them to disk. Other processes on the same host with read access to `/proc/<pid>/pagemap` or `/dev/mem` may observe those buffers.

Enable [`audit_log_filter.direct_io`](audit-log-filter-variables.md#audit_log_filterdirect_io) to open the audit log file with `O_DIRECT` and bypass the OS page cache. The component falls back to buffered I/O with a warning when the file system does not support `O_DIRECT` or when a direct write fails at runtime. The variable is a tech preview and requires a server restart to change.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)

* [Manage the Audit Log Filter files](manage-audit-log-filter.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.file` and `audit_log_filter.handler`

* [Install the audit log filter](install-audit-log-filter.md)
