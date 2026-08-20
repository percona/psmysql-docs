<!--  do we need this doc? -->

# List of features available in Percona Server for MySQL releases

The following table lists Percona features that differ between Percona Server for MySQL 8.4 and Percona Server for MySQL {{vers}}. Features with the same status in both versions are omitted. The {{vers}} column reflects the {{vers}} documentation set.

For plugin transition steps, read [Upgrade from plugins to components](upgrade-components.md).

| Feature | Percona Server for MySQL 8.4 | Percona Server for MySQL {{vers}} |
|---|---|---|
| [Audit Log Filter](audit-log-filter-overview.md) | `component_audit_log_filter`, `format=OLD` available | `component_audit_log_filter`, `format=OLD` removed, JSONL default output format |
| [Audit log plugin](audit-log-plugin.md) | Deprecated plugin | Removed. Use `component_audit_log_filter` |
| [Binary log user-defined functions](binlogging-replication-improvements.md) | `binlog_utils_udf` plugin | `component_binlog_utils_udf` |
| [Data masking](data-masking-overview.md) | `data_masking` plugin and component | `component_masking_functions` |
| [Keyring components](keyring-components-plugins-overview.md) | Keyring plugins and keyring components | Keyring components only, `keyring_file` plugin removed |
| [Percona Toolkit UDFs](udf-percona-toolkit.md) | Plugin | `component_percona_udf` |
| `SEQUENCE_TABLE()` function | Deprecated | Removed, replaced by [`PERCONA_SEQUENCE_TABLE(n)`](percona-sequence-table.md) |
| [Thread pool](threadpool.md) | Percona Server for MySQL thread pool plugin | Percona Server for MySQL thread pool plugin in 9.7.1. MySQL thread pool plugin as of 9.7.2 |


