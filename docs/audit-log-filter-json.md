# Audit Log Filter format - JSON

The feature is in [tech preview](glossary.md#tech-preview).

The JSON format has one top-level JSON array, which contain JSON objects with key-value pairs. These objects represent an event in the audit. Some pairs are listed in every audit record. The audit record type determines if other key-value pairs are listed. The order of the pairs within an audit record is not guaranteed. The value description may be truncated.

Certain statistics, such as query time and size, are only available in the JSON format and help detect activity outliers when analyzed. 

```json

[
  {
    "timestamp": "2023-03-29 11:17:03",
    "id": 0,
    "class": "audit",
    "server_id": 1
  },
  {
    "timestamp": "2023-03-29 11:17:05",
    "id": 1,
    "class": "command",
    "event": "command_start",
    "connection_id": 1,
    "command_data": {
      "name": "command_start",
      "status": 0,
      "command": "query"}
  },
  {
    "timestamp": "2023-03-29 11:17:05",
    "id": 2,
    "class": "general",
    "event": "log",
    "connection_id": 11,
    "account": { "user": "root[root] @ localhost []", "host": "localhost" },
    "login": { "user": "root[root] @ localhost []", "os": "", "ip": "", "proxy": "" },
    "general_data": {
      "command": "Query",
      "sql_command": "create_table",
      "query": "CREATE TABLE t1 (c1 INT)",
      "status": 0}
  },
  {
    "timestamp": "2023-03-29 11:17:05",
    "id": 3,
    "class": "query",
    "event": "query_start",
    "connection_id": 11,
    "query_data": {
      "query": "CREATE TABLE t1 (c1 INT)",
      "status": 0,
      "sql_command": "create_table"}
  },
  {
    "timestamp": "2023-03-29 11:17:05",
    "id": 4,
    "class": "query",
    "event": "query_status_end",
    "connection_id": 11,
    "query_data": {
      "query": "CREATE TABLE t1 (c1 INT)",
      "status": 0,
      "sql_command": "create_table"}
  },
  {
    "timestamp": "2023-03-29 11:17:05",
    "id": 5,
    "class": "general",
    "event": "status",
    "connection_id": 11,
    "account": { "user": "root[root] @ localhost []", "host": "localhost" },
    "login": { "user": "root[root] @ localhost []", "os": "", "ip": "", "proxy": "" },
    "general_data": {
      "command": "Query",
      "sql_command": "create_table",
      "query": "CREATE TABLE t1 (c1 INT)",
      "status": 0}
  },
  {
    "timestamp": "2023-03-29 11:17:05",
    "id": 6,
    "class": "command",
    "event": "command_end",
    "connection_id": 1,
    "command_data": {
      "name": "command_end",
      "status": 0,
      "command": "query"}
  }
]
```
The order of the attributes within the JSON object can vary. Certain attributes are in every element. Other attributes are optional and depend on the type of event and the filter settings or plugin settings.

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
| `connection_data` | Defines the client connection. |
| `connection_id` | Defines the client connection identifier |
| `event` | Defines a subclass of the `event` class |
| `general_data` | Defines the executed statement or command when the audit record has a class value of `general`. |
| `id` | Defines the event ID |
| `login` | Defines how the client connected to the server |
| `query_statistics` | Defines optional query statistics and is used for outlier detection |
| `shutdown_data` | Defines the audit log filter termination |
| `startup_data` | Defines the initialization of the audit log filter plugin |
| `table_access_data` | Defines access to a table |
| `time` | Defines an integer that represents a UNIX timestamp |
| `timestamp` | Defines a UTC value in the `YYYY-MM_DD hh:mm:ss` format |

