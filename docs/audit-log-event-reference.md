# Audit Log Filter Event Reference

This page provides a reference for actual audit events and fields recorded by Percona Server for MySQL's audit subsystem and explains how they relate to the Audit Log Filter filter definitions documented elsewhere. The official filter documentation shows how to construct filters and lists a limited set of event classes and subclasses, but does not enumerate every real event type or internal field value that may be present in Audit Log Filters. This reference bridges that gap with observed audit output and filtering guidance.

Examples on this page are observed output examples captured from test runs and are not a complete list of all possible events in every environment.

Some examples in this page were captured on earlier 8.4 builds (for example, 8.4.6-6). On newer 8.4 releases, event naming and lifecycle fields can differ. For current baseline behavior, see [Audit Log Filter overview](audit-log-filter-overview.md).

## Audit Log Filter output fields

Audit entries (in XML or JSON formats) include a structured set of fields. Common fields seen in Audit Log Filters:



| Field        | Description                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------------|
| NAME        | Descriptive event name (e.g., Command Start, Result).                                                 |
| RECORD_ID   | Unique identifier for the audit record.                                                               |
| TIMESTAMP   | When the event occurred.                                                                              |
| COMMAND_CLASS | Internal classification used by the audit plugin.                                                   |
| SQLTEXT     | The SQL statement text, if applicable.                                                                |
| STATUS      | Execution result (usually 0 for success).                                                             |
| HOST, USER, IP | Client connection context.                                                                         |
| Other fields | Additional context such as STARTUP_OPTIONS and SERVER_ID for lifecycle events.                       |


These fields are essential for interpreting audit entries and for writing filters that match them.

## Observed COMMAND_CLASS values

In real Audit Log Filters, the COMMAND_CLASS field often contains values not listed in the documented filter class table. Common observed values include:



| `COMMAND_CLASS`                     | Typical Context |
|-------------------------------------|-----------------|
| `Query`                             | General SQL query processing. |
| `Parse`                             | SQL parsing phase before execution. |
| `select`                            | Data retrieval. |
| `insert`                            | INSERT DML. |
| `create_db`, `drop_db`              | Database DDL operations. |
| `create_table`, `drop_table`        | Table DDL. |
| `alter_table`                       | ALTER TABLE. |
| `create_index`, `drop_index`        | Index creation/deletion. |
| `show_fields`                       | DESCRIBE or SHOW FIELDS. |
| `optimize`                          | OPTIMIZE TABLE. |
| `alter_tablespace`                  | CREATE/DROP TABLESPACE. |
| `set_option`                        | SET session options. |
| `create_compression_dictionary`     | Create compression dictionary. |
| `drop_compression_dictionary`       | Drop compression dictionary. |
| `create_user`, `drop_user`          | User management. |
| `grant`                             | Grant privileges. |
| `begin`                             | START TRANSACTION. |
| `commit`                            | COMMIT. |
| `savepoint`                         | SAVEPOINT. |
| `rollback`                          | ROLLBACK. |
| `shutdown`                          | Server shutdown invocation. |
| `Server Startup`                    | Server initialization event. |
| `Authentication`, `Auth Flush`      | Authentication or plugin events. |
| `Audit`                             | Audit plugin startup. |


These values represent the internal classification of operations that the audit subsystem records.

## Filterable classes vs. recorded event values

The official Write audit_log_filter definitions documentation lists the following filterable classes and their subclasses:


| Class name   | Event subclass | Description                     |
|--------------|----------------|---------------------------------|
| connection   | connect        | Connection initiated.           |
| connection   | change_user    | In‑session user change.         |
| connection   | disconnect     | Disconnection.                  |
| general      | status         | General server status events.   |
| general      | command        | SQL command details.            |
| table_access | read           | SELECT or similar reads.        |
| table_access | insert         | INSERT operations.              |
| table_access | update         | UPDATE operations.              |
| table_access | delete         | DELETE operations.              |

This set is the official documented event hierarchy that appears in JSON filter definitions. However, many internal event values such as `create_table`, `drop_db`, or other server lifecycle events do not appear explicitly here.

The audit subsystem still records them, so you may need field‑level filters (e.g., matching on COMMAND_CLASS or SQLTEXT) when writing broader filters.

## Practical mapping of events to filters

Because not all audit events map to documented filter classes, administrators often use field-level matching in JSON filters.

### Quick mapping from observed output to filter fields

Use this table as a starting point when converting observed log output to JSON filter rules.

| Observed output value | Typical filter field | Example value |
|-----------------------|----------------------|---------------|
| `COMMAND_CLASS=create_table` | `general_sql_command.str` | `create_table` |
| `COMMAND_CLASS=drop_table` | `general_sql_command.str` | `drop_table` |
| `COMMAND_CLASS=create_db` | `general_sql_command.str` | `create_db` |
| `COMMAND_CLASS=drop_db` | `general_sql_command.str` | `drop_db` |
| `COMMAND_CLASS=shutdown` | `general_sql_command.str` | `shutdown` |
| `SQLTEXT=CREATE ...` | `SQLTEXT` pattern match | `(CREATE|ALTER|DROP)\\s` |

### Example: Filtering specific DDL operations

To log events such as `create_db`, `drop_table`, and `alter_table`, match on the command field used in JSON filter definitions:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "or": [
            { "field": { "name": "general_sql_command.str", "value": "create_db" } },
            { "field": { "name": "general_sql_command.str", "value": "drop_db" } },
            { "field": { "name": "general_sql_command.str", "value": "create_table" } },
            { "field": { "name": "general_sql_command.str", "value": "drop_table" } },
            { "field": { "name": "general_sql_command.str", "value": "alter_table" } }
          ]
        }
      }
    }
  }
}
```

!!! note

     The `COMMAND_CLASS` field values in audit log output (such as `alter_table` and `create_db`) correspond to the `general_sql_command.str` field in JSON filter definitions when matching `general` class events with `status` subclass. For DDL operations that appear in `Query Start` events, you may need to match on multiple event types or use SQL text pattern matching.

### Example: Matching by SQL text pattern

To log all DDL statements using SQL text:

```json
{
  "filter": {
    "field": [
      { "name": "SQLTEXT", "pattern": "(CREATE|ALTER|DROP)\\s" }
    ]
  }
}
```

This filter selects events based on the SQL command text itself.

## Server lifecycle and plugin events

The audit subsystem logs lifecycle and plugin events that are useful for broad auditing:

### Server startup example

```xml
<AUDIT_RECORD>
  <NAME>Startup</NAME>
  <COMMAND_CLASS>Server Startup</COMMAND_CLASS>
  …
</AUDIT_RECORD>
```

### Authentication or audit activity

```xml
<AUDIT_RECORD>
  <NAME>Auth Flush</NAME>
  <COMMAND_CLASS>Authentication</COMMAND_CLASS>
  …
</AUDIT_RECORD>
```

### Savepoint (transaction control)

<AUDIT_RECORD>
  <NAME>Query Start</NAME>
  <RECORD_ID>4506_2025-10-15T09:08:48</RECORD_ID>
  <TIMESTAMP>2025-10-15T09:08:48</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>226</CONNECTION_ID>
  <COMMAND_CLASS>savepoint</COMMAND_CLASS>
  <SQLTEXT>SAVEPOINT save1</SQLTEXT>
</AUDIT_RECORD>
<AUDIT_RECORD>
  <NAME>Query Status End</NAME>
  <RECORD_ID>4507_2025-10-15T09:08:48</RECORD_ID>
  <TIMESTAMP>2025-10-15T09:08:48</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>226</CONNECTION_ID>
  <COMMAND_CLASS>savepoint</COMMAND_CLASS>
  <SQLTEXT>SAVEPOINT save1</SQLTEXT>
</AUDIT_RECORD>

### Rollback (transactional control)

<AUDIT_RECORD>
  <NAME>Query Start</NAME>
  <RECORD_ID>4515_2025-10-15T09:13:29</RECORD_ID>
  <TIMESTAMP>2025-10-15T09:13:29</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>226</CONNECTION_ID>
  <COMMAND_CLASS>rollback</COMMAND_CLASS>
  <SQLTEXT>ROLLBACK</SQLTEXT>
</AUDIT_RECORD>
<AUDIT_RECORD>
  <NAME>Query Status End</NAME>
  <RECORD_ID>4516_2025-10-15T09:13:29</RECORD_ID>
  <TIMESTAMP>2025-10-15T09:13:29</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>226</CONNECTION_ID>
  <COMMAND_CLASS>rollback</COMMAND_CLASS>
  <SQLTEXT>ROLLBACK</SQLTEXT>
</AUDIT_RECORD>

### Shutdown events

```xml
<AUDIT_RECORD>
  <NAME>Query Start</NAME>
  <COMMAND_CLASS>shutdown</COMMAND_CLASS>
  …
</AUDIT_RECORD>
```

These events represent activities beyond SQL queries and connections. Because they are not enumerated in the documented filter classes, administrators must use field filters if they want to include or exclude them.

## How to use this reference

Use this page as a companion to the Audit Log Filter filter definitions documentation, which explains how to construct JSON filters using documented classes and subclasses.

- The Write `audit_log_filter` definitions page explains filter syntax and documented classes and subclasses.
- This Audit Log Filter Event Reference helps interpret observed Audit Log Filter output and extend filters with field-based matching.

