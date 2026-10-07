# Audit Log Filter format - JSON and JSONL

JSON and JSONL emit the same key-value pairs per event. Required keys appear in every record; optional keys depend on event type and settings. Key order is not guaranteed; long values may be truncated.

Only the file layout differs:

| Format | File structure | Set with |
|---|---|---|
| JSON | One top-level JSON array. Each event is a pretty-printed JSON object spanning multiple lines. | `audit_log_filter.format=JSON` |
| JSONL | One top-level JSON array. Each event is a single compact JSON object on its own line, separated by commas. | `audit_log_filter.format=JSONL` |

Percona Server for MySQL 8.4.9-9 introduced JSONL. JSONL is the usual shorthand for JSON Lines: one complete JSON value on each line, with nothing wrapping the file. Percona Server uses that name because each event is one line, and writes a different layout: a JSON array of compact event objects, one object per line, with commas between them. [Standard JSONL and Percona JSONL](#standard-jsonl-and-percona-jsonl) covers how that layout differs from JSON Lines, why Percona JSONL exists, and when to choose Percona JSONL instead of JSON.

Compression and encryption behave like JSON. `audit_log_read()` and `audit_log_read_bookmark()` read both formats.

JSON and JSONL alone expose some statistics (for example, query timing and size)—use them to flag outliers in workload analysis.

## Standard JSONL and Percona JSONL

### What standard JSONL represents

Standard JSONL ([JSON Lines](https://jsonlines.org/), also called newline-delimited JSON) stores a sequence of independent records:

* Each line is one complete JSON value. The specification permits any JSON value, including scalars and arrays, not only objects.
* A newline separates lines. Nothing else does.
* The file has no opening `[`, no closing `]`, and no commas between records.
* A file containing multiple records is not one JSON document. A reader parses and handles each line independently.

That layout fits data that arrives as a stream of separate records: large exports, application logs, event feeds, and bulk loads. A process can append one line, split the file on newlines, or hand each line to a worker without reading the rest of the file.

### How Percona JSONL differs

Percona JSONL uses a JSON array containing one compact event object per line, with commas between objects. The array is a valid JSON document only after the writer closes the file, either at shutdown or on rotation. The active file has no closing `]`. If the server stops without closing the file, for example after a crash, that file never receives the closing `]` and is not valid JSON. 

`audit_log_read()` supports both JSON and JSONL, but a general-purpose JSON parser needs the complete array. Line tools can inspect the event records, but `wc -l` counts the wrapper lines: a completed file that is neither compressed nor encrypted and contains N events has N+2 lines, so `wc -l` is not directly an event count.

| | Standard JSONL | Percona JSONL (`format=JSONL`) |
|---|---|---|
| Valid JSON document | A one-record file can itself be a valid JSON document. Multiple top-level records cannot. | Only after the writer closes the file, at shutdown or on rotation. The active file has no closing bracket. |
| Wrapper | None | `[` and `]` |
| Between events | Newline only | Comma, then newline. The last event in a completed file has no comma. |
| Event layout | One JSON value per line, including a scalar or an array, not only an object | One compact JSON object per line |
| A middle line parses on its own | Yes | No. The line ends with a comma, and the `[` and `]` lines are not events. |
| Typical reader | A JSONL parser, one line at a time | A JSON parser, or a line tool that removes the comma and the wrapper |

A strict JSON Lines parser cannot read a Percona JSONL file directly because the wrapper lines and comma-terminated event lines are not standalone JSON values. To convert a completed, uncompressed, and unencrypted file into standard JSON Lines, use the following command. It reads the complete array into memory, so use a line-oriented conversion or a streaming JSON parser for very large files. Do not use this command on the active file or as a live tailing pipeline.

```bash
jq -c '.[]' audit.jsonl
```

To parse one event line in place, delete a trailing comma first, and skip the `[` and `]` lines. The [JSONL example](#jsonl-example) shows the layout.

### Why Percona JSONL exists

Pretty-printed JSON is easy to open in an editor, and each event spans many lines. That layout is a poor fit for a large log or for a pipeline that handles one event at a time. Line tools cut a single event into pieces; the file is larger, and a consumer has to reassemble the lines before the tool can parse.

Percona JSONL keeps the JSON array, so existing JSON consumers can read a file after the writer closes it, including on rotation, and places each event on one line, so the file can be followed, filtered, counted, and shipped like a log. JSONL is the line-delimited format, with the same event fields as JSON. See [Migrate from audit plugins](migrate-to-audit-log-filter-component.md).

The benefit is both properties at once: a closed file is valid JSON, and each audit event is one line.

### When to choose JSONL

Choose JSONL when another system reads the log, or when you work with the file as a stream of events. Choose JSON when a person reads the file. The event fields are the same either way.

Prefer JSONL over JSON in these situations:

| Situation | Why JSONL |
|---|---|
| Large data sets | Compact lines take less space than pretty-printed objects, so rotation, copy, and retention cost less. A job can split the file into line ranges and process each range on its own. |
| Streaming records | On GNU/Linux, `tail -F` follows the log pathname across rotation. For ingestion, use a rotation-aware consumer that handles the array wrapper and commas. The newest event has no terminating newline until the next event is written or the file closes, so a line-oriented consumer may delay that event. |
| Logs and events | Audit data is a sequence of events. Collectors and SIEMs ingest that sequence more easily when each event is one line. `jq -c '.[]'` is an offline conversion of a completed plaintext file. |
| Bulk ingestion | A loader reads the array, or reads line by line after removing the wrapper and commas, and writes each event to a warehouse, an object store, or a search index. |
| Independent records | A worker takes one line, strips a trailing comma, and parses that object. It does not load the rest of the file, and a bad line stays on that line. |

Prefer JSON when people inspect the file directly. Pretty-printing makes nested objects such as `connection_data` and `startup_data` easier to scan.

Use JSONL if you are in any of these roles:

* You run a log pipeline (Filebeat, Fluent Bit, Vector, Logstash, or a similar shipper) that forwards audit events.
* You load audit events into a SIEM or a data lake for security or compliance.
* You grep or tail the audit file on the server.
* You used the audit log plugin's CSV format for line-delimited ingest.

Compression, encryption, and the SQL readers are the same for JSON and JSONL. Changing `audit_log_filter.format` requires a restart. Give JSONL its own [`audit_log_filter.file`](audit-log-filter-variables.md#audit_log_filterfile) name, for example, `audit.jsonl`. See [Audit Log Filter file format overview](audit-log-filter-formats.md).

## Version changes

### Percona Server for MySQL 8.4.9-9

* Component startup and shutdown events include the `event`, `connection_id`, `account`, `login`, and `startup_data` fields. The `startup_data` object holds `server_id`, `os_version`, `mysql_version`, and `args` (command-line arguments). Earlier releases exposed only `server_id` at the top level for those records.

* Lifecycle `event` values changed from the internal names `audit` / `noaudit` to `startup` / `shutdown`.

* On connection events, `connection_attributes` are nested inside the `connection_data` object.

* Message events: the `message_attributes` key is replaced by the `map` key; message events also include `account` and `login`.

## Attributes

Field sets match between JSON and JSONL. Only the file layout differs. See [How Percona JSONL differs](#how-percona-jsonl-differs).

Every event object includes at least:

* `timestamp`
* `id`
* `class`
* `event`

Other common keys:

| Name | Description |
|---|---|
| `account` | Database account for the event |
| `connection_data` | Client connection details. From 8.4.9-9, `connection_attributes` nest here on connection events. |
| `connection_id` | Client connection ID |
| `general_data` | Statement or command when `class` is `general` |
| `id` | Event ID |
| `login` | How the client attached to the server |
| `map` | 8.4.9-9+ Message payload (replaces `message_attributes`). Message events also carry `account` and `login`. |
| `query_statistics` | Optional metrics for outlier detection |
| `shutdown_data` | Component shutdown |
| `startup_data` | Component startup; from 8.4.9-9 includes `server_id`, `os_version`, `mysql_version`, `args` |
| `table_access_data` | Table access details |
| `time` | UNIX timestamp (integer) when present |
| `timestamp` | UTC time `YYYY-MM-DD hh:mm:ss` |

## JSON example

The following shows four event types recorded in `REDUCED` event mode: startup, connection, table access, and general status.

```json
[
  {
    "timestamp": "2026-04-03 10:43:52",
    "id": 0,
    "class": "audit",
    "event": "startup",
    "connection_id": 12,
    "account": { "user": "root", "host": "localhost" },
    "login": { "user": "root", "os": "", "ip": "", "proxy": "" },
    "startup_data": {
      "server_id": 1,
      "os_version": "x86_64-Linux",
      "mysql_version": "8.4.9-9",
      "args": [
        "/usr/sbin/mysqld",
        "--defaults-file=/etc/my.cnf",
        "--basedir=/usr",
        "--user=mysql",
        "--datadir=/var/lib/mysql",
        "--socket=/var/run/mysqld/mysqld.sock",
        "--port=3306"
      ]
    }
  },
  {
    "timestamp": "2026-04-03 10:43:53",
    "id": 1,
    "class": "connection",
    "event": "connect",
    "connection_id": 39,
    "account": { "user": "root", "host": "localhost" },
    "login": { "user": "root", "os": "", "ip": "", "proxy": "" },
    "connection_data": {
      "connection_type": "socket",
      "status": 0,
      "db": "test",
      "connection_attributes": {
        "_pid": "824388",
        "_platform": "x86_64",
        "_client_version": "8.0.45",
        "_os": "Linux",
        "_client_name": "libmysql"
      }
    }
  },
  {
    "timestamp": "2026-04-03 10:43:53",
    "id": 9,
    "class": "table_access",
    "event": "read",
    "connection_id": 40,
    "account": { "user": "root", "host": "localhost" },
    "login": { "user": "root", "os": "", "ip": "", "proxy": "" },
    "table_access_data": {
      "db": "test",
      "table": "sbtest2",
      "query": "SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099",
      "sql_command": "select"
    }
  },
  {
    "timestamp": "2026-04-03 10:43:53",
    "id": 11,
    "class": "general",
    "event": "status",
    "connection_id": 40,
    "account": { "user": "root", "host": "localhost" },
    "login": { "user": "root", "os": "", "ip": "", "proxy": "" },
    "general_data": {
      "command": "Query",
      "sql_command": "select",
      "query": "SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099",
      "status": 0
    }
  }
]
```

## JSONL example

In the JSONL format each event is a single compact JSON object on its own line, separated by commas inside a wrapping JSON array. The same events from the preceding JSON example look like this:

```json
[
{ "timestamp": "2026-04-03 10:43:52", "id": 0, "class": "audit", "event": "startup", "connection_id": 12, "account": { "user": "root", "host": "localhost" }, "login": { "user": "root", "os": "", "ip": "", "proxy": "" }, "startup_data": { "server_id": 1, "os_version": "x86_64-Linux", "mysql_version": "8.4.9-9", "args": ["/usr/sbin/mysqld", "--defaults-file=/etc/my.cnf", "--basedir=/usr", "--user=mysql", "--datadir=/var/lib/mysql", "--socket=/var/run/mysqld/mysqld.sock", "--port=3306"] } },
{ "timestamp": "2026-04-03 10:43:53", "id": 1, "class": "connection", "event": "connect", "connection_id": 39, "account": { "user": "root", "host": "localhost" }, "login": { "user": "root", "os": "", "ip": "", "proxy": "" }, "connection_data": { "connection_type": "socket", "status": 0, "db": "test", "connection_attributes": { "_pid": "824388", "_platform": "x86_64", "_client_version": "8.0.45", "_os": "Linux", "_client_name": "libmysql" } } },
{ "timestamp": "2026-04-03 10:43:53", "id": 9, "class": "table_access", "event": "read", "connection_id": 40, "account": { "user": "root", "host": "localhost" }, "login": { "user": "root", "os": "", "ip": "", "proxy": "" }, "table_access_data": { "db": "test", "table": "sbtest2", "query": "SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099", "sql_command": "select" } },
{ "timestamp": "2026-04-03 10:43:53", "id": 11, "class": "general", "event": "status", "connection_id": 40, "account": { "user": "root", "host": "localhost" }, "login": { "user": "root", "os": "", "ip": "", "proxy": "" }, "general_data": { "command": "Query", "sql_command": "select", "query": "SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099", "status": 0 } }
]
```

## Additional reading

* [Audit Log Filter file format overview](audit-log-filter-formats.md)
* [Audit Log Filter format - XML (new style)](audit-log-filter-new.md)
* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_read()`, `audit_log_read_bookmark()`, format options
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
* [Manage the Audit Log Filter files](manage-audit-log-filter.md)
