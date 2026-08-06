# Audit Log Filter security

The Audit Log Filter component writes audit files. Restrict the log directory to trusted operators and ensure the server can write there.

Logs are plaintext by default and may hold credentials, SQL text, and other sensitive data.

The default file under the data directory is `audit_filter.log`. Override location with `audit_log_filter.file` at startup.

Starting in Percona Server for MySQL 8.4.9-9, if the parent directory is missing the component errors and the server starts without Audit Log Filter active.

Rotation leaves multiple files on disk—protect every generation.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
* [Manage the Audit Log Filter files](manage-audit-log-filter.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.file`, `audit_log_filter.handler`
* [Install the audit log filter](install-audit-log-filter.md)
