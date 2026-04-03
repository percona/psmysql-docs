# Audit Log Filter format - JSON and JSONL

Both the JSON and JSONL formats write audit events as JSON objects with the same set of key-value pairs. Some pairs are listed in every audit record. The audit record type determines if other key-value pairs are listed. The order of the pairs within an audit record is not guaranteed. The value description may be truncated.

The two formats differ only in file-level structure:

| Format | File structure | Set with |
|---|---|---|
| JSON | One top-level JSON array. Each event is a pretty-printed JSON object spanning multiple lines. | `audit_log_filter.format=JSON` |
| JSONL | One top-level JSON array (the file is still valid JSON). Each event is a single compact JSON object on its own line. | `audit_log_filter.format=JSONL` |

The JSONL format was introduced in Percona Server for MySQL 8.4.9-9. Unlike the strict [JSON Lines](https://jsonlines.org/) specification, the Percona JSONL format retains the wrapping JSON array and trailing commas, so the output file is valid JSON and can be parsed by any JSON parser. The one-event-per-line layout still makes it easy to process with line-oriented tools (`grep`, `jq`, `wc -l`), streaming pipelines, and log aggregation systems. Encryption and compression work with JSONL just as they do with JSON. `audit_log_read()` and `audit_log_read_bookmark()` support both formats.

Percona Server for MySQL 8.4.9-9 introduces the following changes to the JSON and JSONL formats: the startup event now includes `event`, `connection_id`, `account`, `login`, and a `startup_data` object containing `server_id`, `os_version`, `mysql_version`, and `args` (previously only `server_id` was present at the top level). Shutdown events now also include `connection_id`, `account`, and `login` fields. The lifecycle `event` value changed from the internal names `audit`/`noaudit` to `startup`/`shutdown`. The `connection_data` object now nests `connection_attributes` on connection events. The `message_attributes` key is replaced by `map`, and message events also include `account` and `login` fields.

Certain statistics, such as query time and size, are only available in the JSON and JSONL formats and help detect activity outliers when analyzed.

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

In the JSONL format each event is a single compact JSON object on its own line. The file is still wrapped in a JSON array, so it remains valid JSON. The same events from the JSON example above look like this:

```json
[
{"timestamp":"2026-04-03 10:43:52","id":0,"class":"audit","event":"startup","connection_id":12,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"startup_data":{"server_id":1,"os_version":"x86_64-Linux","mysql_version":"8.4.9-9","args":["/usr/sbin/mysqld","--defaults-file=/etc/my.cnf","--basedir=/usr","--user=mysql","--datadir=/var/lib/mysql","--socket=/var/run/mysqld/mysqld.sock","--port=3306"]}},
{"timestamp":"2026-04-03 10:43:53","id":1,"class":"connection","event":"connect","connection_id":39,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"connection_data":{"connection_type":"socket","status":0,"db":"test","connection_attributes":{"_pid":"824388","_platform":"x86_64","_client_version":"8.0.45","_os":"Linux","_client_name":"libmysql"}}},
{"timestamp":"2026-04-03 10:43:53","id":9,"class":"table_access","event":"read","connection_id":40,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"table_access_data":{"db":"test","table":"sbtest2","query":"SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099","sql_command":"select"}},
{"timestamp":"2026-04-03 10:43:53","id":11,"class":"general","event":"status","connection_id":40,"account":{"user":"root","host":"localhost"},"login":{"user":"root","os":"","ip":"","proxy":""},"general_data":{"command":"Query","sql_command":"select","query":"SELECT c FROM sbtest2 WHERE id BETWEEN 83000 AND 83099","status":0}}
]
```

## Attributes

The order of the attributes within the JSON object can vary. Certain attributes are in every element. Other attributes are optional and depend on the type of event and the filter settings or component settings.

The following fields are contained in each object:

* `timestamp`
* `id`
* `class`
* `event`

The possible attributes in a JSON object are the following:

| Name | Description |
|---|---|
| `class` | Defines the type of event |
| `account` | Defines the MySQL account associated with the event. |
| `connection_data` | Defines the client connection. Starting from Percona Server for MySQL 8.4.9-9, on connection events, `connection_attributes` are nested inside this object. |
| `connection_id` | Defines the client connection identifier |
| `event` | Defines a subclass of the `event` class |
| `general_data` | Defines the executed statement or command when the audit record has a class value of `general`. |
| `id` | Defines the event ID |
| `login` | Defines how the client connected to the server |
| `map` | Introduced in Percona Server for MySQL 8.4.9-9. Contains message event payload data (replaces the former `message_attributes` key). Message events also include `account` and `login` fields. |
| `query_statistics` | Defines optional query statistics and is used for outlier detection |
| `shutdown_data` | Defines the audit log filter termination |
| `startup_data` | Defines the initialization of the audit log filter component. Starting from Percona Server for MySQL 8.4.9-9, contains `server_id`, `os_version`, `mysql_version`, and `args` (an array of command-line arguments). |
| `table_access_data` | Defines access to a table |
| `time` | Defines an integer that represents a UNIX timestamp |
| `timestamp` | Defines a UTC value in the `YYYY-MM-DD hh:mm:ss` format |

