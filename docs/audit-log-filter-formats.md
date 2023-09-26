# Audit Log Filter file format overview

The feature is in [tech preview](glossary.md#tech-preview).

When an auditable event occurs, the plugin writes a record to the log file.

After the plugin starts, the first record lists the description of the server and the options at startup. After the first record, the auditable events are connections, disconnections, SQL statements executed, and so on. Statements within stored procedures or triggers are not logged, only the top-level statements.

If files are referenced by `LOAD_DATA`, the contents are not logged.

Set with the `audit_log_filter_format` system variable at startup. The available format types are the following;

| Format Type | Command | Description |
|---|---|---|
| [XML (new style)](audit-log-filter-new.md) | `audit_log_filter_format=NEW` | The default format |
| [XML (old style)](audit-log-filter-old.md) | `audit_log_filter_format=OLD` | The original version of the XML format |
| [JSON](audit-log-filter-json.md) | `audit_log_filter_format=JSON` | Files written as a JSON array |

By default, the file contents in the new-style XML format are not compressed or encrypted.

Changing the `audit_log_filter_format`, you should also change 
the `audit_log_filter_file` name. For example, changing the `audit_log_filter_format` 
to JSON, change the `audit_log_filter_file` to `audit.json`. If you don't change 
the `audit_log_filter_file` name, then all audit log filter files have the same 
base name and you won't be able to easily find when the format changed.

