> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Audit Log Filter security

The Audit Log Filter component writes audit files. Restrict the log directory to trusted operators and ensure the server can write there.

Logs are plaintext by default and may hold credentials, SQL text, and other sensitive data.

The default file under the data directory is `audit_filter.log`. Override location with `audit_log_filter.file` at startup.

Starting in Percona Server for MySQL 8.4.9-9, if the parent directory is missing the component errors and the server starts without Audit Log Filter active.

Rotation leaves multiple files on disk—protect every generation.

## Additional reading

- [Audit Log Filter overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.html)
- [Audit Log Filter compression and encryption](https://docs.percona.com/percona-server/8.4/audit-log-filter-compression-encryption.html)
- [Manage the Audit Log Filter files](https://docs.percona.com/percona-server/8.4/manage-audit-log-filter.html)
- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html) — `audit_log_filter.file`, `audit_log_filter.handler`
- [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html)
