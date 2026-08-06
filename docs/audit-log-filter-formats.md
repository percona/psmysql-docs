# Audit Log Filter file format overview

On each auditable event, the component appends a record to the log. After startup, the first record describes the server and startup options; later records cover connections, disconnections, executed SQL, and more.

Which server actions become audit records depends on [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode), not on the file format. See that variable for `REDUCED` versus `FULL` and for releases before it existed.

If `LOAD_DATA` references files, the component does not log file contents.

Set format with [`audit_log_filter.format`](audit-log-filter-variables.md#audit_log_filterformat) at startup. Options:

| Format Type | Command | Description |
|---|---|---|
| [XML (new style)](audit-log-filter-new.md) | `audit_log_filter.format=NEW` | New XML layout (default in Percona Server 8.4) |
| [XML (old style)](audit-log-filter-old.md) | `audit_log_filter.format=OLD` | Legacy XML layout. Deprecated and may be removed in a later version. |
| [JSON](audit-log-filter-json.md) | `audit_log_filter.format=JSON` | One top-level JSON array of events |
| [JSONL](audit-log-filter-json.md) | `audit_log_filter.format=JSONL` | Added in 8.4.9-9. One compact JSON object per line inside a wrapping array (see the JSON/JSONL topic). |

By default, new-style XML logs are neither compressed nor encrypted.

When you change `audit_log_filter.format`, rename `audit_log_filter.file` as well—for example use `audit.json` or `audit.jsonl` for JSON or JSONL. Reusing one base name obscures format changes across rotated files.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter format - XML (new style)](audit-log-filter-new.md)
* [Audit Log Filter format - XML (old style)](audit-log-filter-old.md)
* [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.format`, `audit_log_filter.file`
* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
