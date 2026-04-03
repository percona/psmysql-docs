# Audit Log Filter format - JSON and JSONL

JSON and JSONL emit the same key-value pairs per event. Required keys appear in every record; optional keys depend on event type and settings. Key order is not guaranteed; long values may be truncated.

Only file layout differs:

| Format | File structure | Set with |
|---|---|---|
| JSON | One top-level JSON array. Each event is a pretty-printed JSON object spanning multiple lines. | `audit_log_filter.format=JSON` |
| JSONL | One top-level JSON array. Each event is a single compact JSON object on its own line, separated by commas. | `audit_log_filter.format=JSONL` |

JSONL arrived in Percona Server for MySQL 8.4.9-9. Unlike plain [JSON Lines](https://jsonlines.org/), Percona JSONL keeps a wrapping JSON array and commas between lines, so the file stays valid JSON while remaining line-friendly for `grep`, `jq`, `wc -l`, streams, and aggregators.

Compression and encryption behave like JSON. `audit_log_read()` and `audit_log_read_bookmark()` read both formats.

JSON and JSONL alone expose some statistics (for example query timing and size)—use them to flag outliers in workload analysis.

## Version changes

### Percona Server for MySQL 8.4.9-9

* Component startup and shutdown events include `event`, `connection_id`, `account`, `login`, and a `startup_data` object. The `startup_data` object holds `server_id`, `os_version`, `mysql_version`, and `args` (command-line arguments). Earlier releases exposed only `server_id` at the top level for those records.

* Lifecycle `event` values changed from the internal names `audit` / `noaudit` to `startup` / `shutdown`.

* On connection events, `connection_attributes` are nested inside the `connection_data` object.

* Message events: the `message_attributes` key is replaced by `map`; message events also include `account` and `login`.

## Attributes

Field sets match between JSON and JSONL; only wrapping differs. See the preceding table for details.

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
{"timestamp":"2026-04-03 10:43:52","id":0,"class":"audit","event":"startup","connection_id":12,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"startup_data":{"server_id":1,"os_version":"x86_64-Linux","mysql_version":"8.4.9-9","args":["/usr/sbin/mysqld","--defaults-file=/etc/my.cnf","--basedir=/usr","--user=mysql","--datadir=/var/lib/mysql","--socket=/var/run/mysqld/mysqld.sock","--port=3306"]}},
{"timestamp":"2026-04-03 10:43:53","id":1,"class":"connection","event":"connect","connection_id":39,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"connection_data":{"connection_type":"socket","status":0,"db":"test","connection_attributes":{"_pid":"824388","_platform":"x86_64","_client_version":"8.0.45","_os":"Linux","_client_name":"libmysql"}}},
{"timestamp":"2026-04-03 10:43:53","id":9,"class":"table_access","event":"read","connection_id":40,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"table_access_data":{"db":"test","table":"sbtest2","query":"SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099","sql_command":"select"}},
{"timestamp":"2026-04-03 10:43:53","id":11,"class":"general","event":"status","connection_id":40,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"general_data":{"command":"Query","sql_command":"select","query":"SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099","status":0}}
]
```

## Additional reading

* [Audit Log Filter file format overview](audit-log-filter-formats.md)
* [Audit Log Filter format - XML (new style)](audit-log-filter-new.md)
* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_read()`, `audit_log_read_bookmark()`, format options
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
* [Manage the Audit Log Filter files](manage-audit-log-filter.md)
