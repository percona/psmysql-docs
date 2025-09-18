# Reading Audit Log Filter files

The Audit Log Filter functions can provide a SQL interface to read JSON-format audit log files. The functions cannot read log files in other formats. Configuring the plugin for JSON logging lets the functions use the directory that contains the current audit log filter file and search in that location for readable files. The value of the `audit_log_filter_file` system variable provides the file location, base name, and the suffix and then searches for names that match the pattern.

If the file is renamed and no longer fits the pattern, the file is ignored.

## Functions used for reading the files

The following functions read the files in the JSON-format:

* [`audit_log_read`](audit-log-filter-variables.md#audit_log_read) - reads audit log filter events
* [`audit_log_read_bookmark()](audit-log-filter-variables.md#audit_log_read_bookmark) - for the most recently read event, returns a bookmark. The bookmark can be passed to `audit_log_read()`.

Initialize a read sequence by using a bookmark or an argument that specifies the start position:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read(audit_log_read_bookmark());
```

The following example continues reading from the current position:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read();
```

Reading a file is closed when the session ends or calling `audit_log_read()` with another argument.

## Using jq to process JSON audit logs

The `jq` utility is a command-line JSON processor that provides an alternative way to read and analyze JSON-format audit log files. This is useful for filtering, searching, and formatting audit log data from the command line.

!!! note "Important"
    `jq` can only parse audit log files that are closed, meaning they are not currently being used by the MySQL server. If you run `jq` commands on an open file (one that the server is actively writing to), `jq` will not be able to parse that file.

### Installing jq

=== "RHEL/CentOS"

    ```bash
    sudo yum install jq
    ```

=== "Debian/Ubuntu"

    ```bash
    sudo apt install jq
    ```

### Example usage

Extract all connection events:

```bash
cat audit_filter.log | jq '.[]|select(.class=="connection")'
```

Find all events for a specific user:

```bash
cat data/audit_filter.20251007T121752.log.json | jq '.[] | select((.account.user // "") | contains("root"))'
{
  "timestamp": "2025-10-07 11:15:27",
  "id": 4,
  "class": "general",
  "event": "log",
  "connection_id": 11,
  "account": {
    "user": "[root] @ localhost []",
    "host": "localhost"
  },
  "login": {
    "user": "[root] @ localhost []",
    "ip": "",
    "proxy": ""
  },
  "general_data": {
    "status": 0
  }
}
```

Filter events by SQL command type:

```bash
cat data/audit_filter.20251007T121752.log.json| jq '.[]|select(.query_data.sql_command=="select")'
{
  "timestamp": "2025-10-07 11:15:27",
  "id": 10,
  "class": "query",
  "event": "query_start",
  "connection_id": 11,
  "query_data": {
    "query": "select @@version_comment limit 1",
    "status": 0,
    "sql_command": "select"
  }
}
```

Extract only INSERT operations on specific tables:

```bash
cat data/audit_filter.20260109T131132.log | jq '.[]|select(.class=="table_access" and .event=="insert" or (.table_access_data.table_database // "")=="test")'
{
  "timestamp": "2026-01-09 13:10:59",
  "id": 80,
  "class": "table_access",
  "event": "insert",
  "connection_id": 12,
  "table_access_data": {
    "db": "test",
    "table": "t1",
    "query": "INSERT INTO t1 VALUES (1)",
    "sql_command": "insert"
  }
}
```

Pretty-print the entire audit log:

```bash
cat audit_filter.log.20251007T121752.log.json | jq '.' | less
```

For more `jq` examples and syntax, see the [jq documentation](https://stedolan.github.io/jq/manual/).
