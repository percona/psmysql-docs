# Audit Log Filter file format overview

When an auditable event occurs, the component writes a record to the log file.

After the component starts, the first record lists the description of the server and the options at startup. After the first record, the auditable events are connections, disconnections, SQL statements executed, and so on. Statements within stored procedures or triggers are not logged, only the top-level statements.

If files are referenced by `LOAD_DATA`, the contents are not logged.

Set with the `audit_log_filter.format` system variable at startup. The available format types are the following;

| Format Type | Command | Description |
|---|---|---|
| [XML (new style)](audit-log-filter-new.md) | `audit_log_filter.format=NEW` | The default format |
| [XML (old style)](audit-log-filter-old.md) | `audit_log_filter.format=OLD` | The original version of the XML format |
| [JSON](audit-log-filter-json.md) | `audit_log_filter.format=JSON` | Files written as a JSON array |
| [JSONL](audit-log-filter-json.md) | `audit_log_filter.format=JSONL` | Introduced in Percona Server for MySQL 8.4.9-9. Each event is a single compact JSON object on its own line inside a wrapping JSON array (the file is still valid JSON). Easy to process with `grep`, `jq`, `wc -l`, streaming pipelines, and log aggregation systems. |

By default, the file contents in the new-style XML format are not compressed or encrypted.

Changing the `audit_log_filter.format`, you should also change 
the `audit_log_filter.file` name. For example, changing the `audit_log_filter.format` 
to JSON or JSONL, change the `audit_log_filter.file` to `audit.json` or `audit.jsonl` respectively. If you don't change 
the `audit_log_filter.file` name, then all audit log filter files have the same 
base name and you won't be able to easily find when the format changed.

