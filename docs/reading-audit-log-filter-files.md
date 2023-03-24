# Reading Audit Log Filter files

The feature is in [tech preview](glossary.md#tech-preview).

The Audit Log Filter functions can provide a SQL interface to read JSON-format audit log files. The functions cannot read log files in other formats. Configuring the plugin for JSON logging lets the functions use the directory that contains the current audit log filter file and search in that location for readable files. The value of the `audit_log_filter_file` system variable provides the file location, base name, and the suffix and then searches for names that match the pattern.

If the file is renamed and no longer fits the pattern, the file is ignored.

## Functions used for reading the files

The following functions read the files in the JSON-format:

* [`audit_log_read`](audit-log-filter-variables.md#audit_log_read) - reads audit log filter events
* [`audit_log_read_bookmark()](audit-log-filter-variables.md#audit_log_read_bookmark) - for the most recently read event, returns a bookmark. The bookmark can be passed to `audit_log_read()`.

Initialize a read sequence by using a bookmark or an argument that specifies the start position:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read(audit_log_read_bookmark());

The following example continues reading from the current position:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read();
```

Reading a file is closed when the session ends or calling `audit_log_read()` with another argument.

