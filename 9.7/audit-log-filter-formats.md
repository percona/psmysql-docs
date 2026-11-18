> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Audit Log Filter file format overview

On each auditable event, the component appends a record to the log. After startup, the first record describes the server and the startup options. Later records cover connections, disconnections, executed SQL, and other audit events.

[`audit_log_filter.event_mode`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html#audit_log_filterevent_mode) controls which server actions become audit records. The file format does not change that selection. See the variable reference for `REDUCED` versus `FULL` and for releases before the variable existed.

When `LOAD_DATA` references files, the component does not log file contents.

Set the format with `audit_log_filter.format` at startup. The available formats follow:

| Format type                                                                              | Command                         | Description                                                                                      |
| ---------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------ |
| [JSONL](https://docs.percona.com/percona-server/9.7/audit-log-filter-json.html)          | `audit_log_filter.format=JSONL` | Default. One compact JSON object per line inside a wrapping array. See the JSON and JSONL topic. |
| [JSON](https://docs.percona.com/percona-server/9.7/audit-log-filter-json.html)           | `audit_log_filter.format=JSON`  | One top-level JSON array of events.                                                              |
| [XML (new style)](https://docs.percona.com/percona-server/9.7/audit-log-filter-new.html) | `audit_log_filter.format=NEW`   | XML layout.                                                                                      |

By default, JSONL logs are neither compressed nor encrypted.

When you change `audit_log_filter.format`, rename `audit_log_filter.file` as well. For example, use `audit.json` or `audit.jsonl` for JSON or JSONL. Reusing one base name obscures format changes across rotated files.

## Additional reading

- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.html)
- [Audit Log Filter format - JSON and JSONL](https://docs.percona.com/percona-server/9.7/audit-log-filter-json.html)
- [Audit Log Filter format - XML (new style)](https://docs.percona.com/percona-server/9.7/audit-log-filter-new.html)
- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html) — `audit_log_filter.format` and `audit_log_filter.file`
- [Reading Audit Log Filter files](https://docs.percona.com/percona-server/9.7/reading-audit-log-filter-files.html)
- [Audit Log Filter compression and encryption](https://docs.percona.com/percona-server/9.7/audit-log-filter-compression-encryption.html)
