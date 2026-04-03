# Reading Audit Log Filter files

The Audit Log Filter functions can provide a SQL interface to read JSON-format and JSONL-format (introduced in Percona Server for MySQL 8.4.9-9) audit log files. The functions cannot read log files in other formats. JSON uses a JSON array file layout, while JSONL stores one compact JSON object per line, separated by commas inside a wrapping JSON array. Configuring the component for JSON or JSONL logging lets the functions use the directory that contains the current audit log filter file and search in that location for readable files. The value of the `audit_log_filter.file` system variable provides the file location, base name, and the suffix and then searches for names that match the pattern.

If the file is renamed and no longer fits the pattern, the file is ignored.

## Functions used for reading the files

The following functions read the files in JSON or JSONL format:

* [`audit_log_read`](audit-log-filter-variables.md#audit_log_read) - reads audit log filter events

* [`audit_log_read_bookmark`](audit-log-filter-variables.md#audit_log_read_bookmark) - for the most recently read event, returns a bookmark. This bookmark can be passed to `audit_log_read()`.

Initialize a read sequence by using a bookmark or an argument that specifies the start position:

```sql
SELECT audit_log_read(audit_log_read_bookmark());
```

The following example continues reading from the current position:

```sql
SELECT audit_log_read();
```

A read sequence is closed when the session ends or when you call `audit_log_read()` with another argument.

