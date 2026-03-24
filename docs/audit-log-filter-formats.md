# Audit Log Filter file format overview

When an auditable event occurs, the component writes a record to the log file.

After the component starts, the first record marks audit logging start. With `audit_log_filter.format=NEW`, from Percona Server for MySQL 8.4.8-8 onward on the {{vers}} line (this docs build: {{release}}), that record’s `<NAME>` is `Startup` and the record includes `SERVER_ID` and `COMMAND_CLASS` (among the mandatory elements). Later records cover connections, disconnections, SQL statements executed, and so on. Statements within stored procedures or triggers are not logged, only the top-level statements. See [XML (new style)](audit-log-filter-new.md) for the full field list.

If files are referenced by `LOAD_DATA`, the contents are not logged.

Set with the `audit_log_filter.format` system variable at startup. The available format types are the following;

| Format Type | Command | Description |
|---|---|---|
| [XML (new style)](audit-log-filter-new.md) | `audit_log_filter.format=NEW` | The default format |
| [XML (old style)](audit-log-filter-old.md) | `audit_log_filter.format=OLD` | The original version of the XML format |
| [JSON](audit-log-filter-json.md) | `audit_log_filter.format=JSON` | Files written as a JSON array |

By default, the file contents in the new-style XML format are not compressed or encrypted.

Changing the `audit_log_filter.format`, you should also change 
the `audit_log_filter.file` name. For example, changing the `audit_log_filter.format` 
to JSON, change the `audit_log_filter.file` to `audit.json`. If you don't change 
the `audit_log_filter.file` name, then all audit log filter files have the same 
base name and you won't be able to easily find when the format changed.

