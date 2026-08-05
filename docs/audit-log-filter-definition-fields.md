# Audit Log Filter definition fields

Canonical class, event, and field names for [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) validation. The names align with the Percona Server source [filter_definition_fields.md](https://github.com/percona/percona-server/blob/9.7/components/audit_log_filter/filter_definition_fields.md).

For SQL command values (`create_db`, `select`, `grant`, and so on), typical event sequences for DDL/DCL/TCL operations, and the mapping between filter names and log output, see [Event classes, log output, and SQL commands](write-filter-definitions.md#event-classes-log-output-and-sql-commands).

[`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) decides which sections apply. The following notes contrast `REDUCED` and `FULL`.

## Notes

* Names on this page are filter-definition names. They may differ from JSON log output keys.

* Field type reflects the current server validator (`get_event_field_value_type()`).

* Some numeric-looking fields validate as `string` when the server leaves them untyped.

* Only documented class names pass validation.

* When [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) is `REDUCED` (the default), only the following events are tracked and accepted by filter-definition validation:

    * `general`: `status`

    * `connection`: `connect`, `disconnect`, `change_user`

    * `table_access`: `read`, `insert`, `update`, `delete`

    * `message`: `internal`, `user`

    In `REDUCED` mode, class names that exist only for extended auditing (`global_variable`, `command`, `query`, `stored_program`, `authentication`, and `parse`) are rejected entirely. Subclass names that are not in the preceding list (for example, `general/log` and `connection/pre_authenticate`) are also rejected during filter validation. At runtime, events outside the `REDUCED` set are silently skipped. With `FULL`, those six classes and their subclasses are valid filter targets.

* Lifecycle-related records with class names `audit`, `server_startup`, and `server_shutdown` are not valid filter-definition targets. The audit log filter ignores startup and shutdown lifecycle events when they arrive.

* For `connection.connection_type`, the validator accepts numeric values `0`–`5` and the pseudo-constants `::undefined`, `::tcp/ip`, `::socket`, `::named_pipe`, `::ssl`, and `::shared_memory`.

## `general`

Supported events: `log`, `error`, `result`, and `status`.

REDUCED mode: only `status`.

| Field name | Field type | Description |
| --- | --- | --- |
| `general_error_code` | integer | Event error code. |
| `general_thread_id` | unsigned integer | Event thread ID. Aliased to `general_connection_id`. |
| `general_connection_id` | unsigned integer | Event connection ID. |
| `general_user.str` | string | User name recorded for the general event. |
| `general_user.length` | unsigned integer | User name length. |
| `general_command.str` | string | General command text, for example `Query`. |
| `general_command.length` | unsigned integer | General command text length. |
| `general_query.str` | string | SQL statement text associated with the event. |
| `general_query.length` | unsigned integer | SQL statement text length. |
| `general_host.str` | string | Client host name. |
| `general_host.length` | unsigned integer | Client host name length. |
| `general_sql_command.str` | string | SQL command name associated with the statement, for example `select`. |
| `general_sql_command.length` | unsigned integer | SQL command name length. |
| `general_external_user.str` | string | External user or OS login associated with the event. |
| `general_external_user.length` | unsigned integer | External user or OS login length. |
| `general_ip.str` | string | Client IP address. |
| `general_ip.length` | unsigned integer | Client IP address length. |

## `connection`

Supported events: `connect`, `disconnect`, `change_user`, and `pre_authenticate`.

REDUCED mode: `connect`, `disconnect`, and `change_user`.

| Field name | Field type | Description |
| --- | --- | --- |
| `status` | integer | Current connection event status. |
| `connection_id` | unsigned integer | Connection ID. |
| `user.str` | string | User name of this connection. |
| `user.length` | unsigned integer | User name length. |
| `priv_user.str` | string | Privileged user name. |
| `priv_user.length` | unsigned integer | Privileged user name length. |
| `external_user.str` | string | External user name or OS login. |
| `external_user.length` | unsigned integer | External user name length. |
| `proxy_user.str` | string | Proxy user used for the connection. |
| `proxy_user.length` | unsigned integer | Proxy user name length. |
| `host.str` | string | Connection host name. |
| `host.length` | unsigned integer | Connection host name length. |
| `ip.str` | string | Connection IP address. |
| `ip.length` | unsigned integer | Connection IP address length. |
| `database.str` | string | Default database specified at connection time. |
| `database.length` | unsigned integer | Default database name length. |
| `connection_type` | integer | Connection type code: numeric `0`–`5` or pseudo-constant. See [Connection type constants](#connection-type-constants). |

### Connection type constants

`connection_type` values:

| Value | Meaning |
| --- | --- |
| `0` or `::undefined` | Undefined |
| `1` or `::tcp/ip` | TCP/IP |
| `2` or `::socket` | Socket |
| `3` or `::named_pipe` | Named pipe |
| `4` or `::ssl` | TCP/IP with encryption |
| `5` or `::shared_memory` | Shared memory |

## `table_access`

Supported events: `read`, `insert`, `update`, and `delete`.

REDUCED mode: all events.

| Field name | Field type | Description |
| --- | --- | --- |
| `connection_id` | unsigned integer | Event connection ID. |
| `sql_command_id` | integer | SQL command ID. |
| `query.str` | string | SQL statement text. |
| `query.length` | unsigned integer | SQL statement text length. |
| `table_database.str` | string | Database name associated with event. |
| `table_database.length` | unsigned integer | Database name length. |
| `table_name.str` | string | Table name associated with event. |
| `table_name.length` | unsigned integer | Table name length. |

## `global_variable` *(FULL mode only)*

Supported events: `get` and `set`.

| Field name | Field type | Description |
| --- | --- | --- |
| `connection_id` | string | Event connection ID. |
| `variable_name.str` | string | Variable name. |
| `variable_name.length` | string | Variable name length. |
| `variable_value.str` | string | Variable value. |
| `variable_value.length` | string | Variable value length. |

## `command` *(FULL mode only)*

Supported events: `start` and `end`.

| Field name | Field type | Description |
| --- | --- | --- |
| `status` | string | Command event status code. |
| `connection_id` | string | Event connection ID. |
| `command.str` | string | Command text. |
| `command.length` | string | Command text length. |

## `query` *(FULL mode only)*

Supported events: `start`, `nested_start`, `status_end`, and `nested_status_end`.

| Field name | Field type | Description |
| --- | --- | --- |
| `status` | string | Query event status code. |
| `connection_id` | string | Event connection ID. |
| `sql_command_id` | string | SQL command string associated with the query event. The field name is retained as `sql_command_id` for compatibility. |
| `query.str` | string | SQL query text. |
| `query.length` | string | SQL query text length. |
| `query_charset` | string | SQL query character set name. |

## `stored_program` *(FULL mode only)*

Supported events: `execute`.

| Field name | Field type | Description |
| --- | --- | --- |
| `connection_id` | string | Event connection ID. |
| `database.str` | string | Database where the stored program is defined. |
| `database.length` | string | Database name length. |
| `name.str` | string | Stored program name. |
| `name.length` | string | Stored program name length. |

## `authentication` *(FULL mode only)*

Supported events: `flush`, `authid_create`, `credential_change`, `authid_rename`, and `authid_drop`.

| Field name | Field type | Description |
| --- | --- | --- |
| `status` | string | Authentication event status. |
| `connection_id` | string | Event connection ID. |
| `user.str` | string | User name. |
| `user.length` | string | User name length. |
| `host.str` | string | Host name. |
| `host.length` | string | Host name length. |

## `message`

Supported events: `internal` and `user`.

REDUCED mode: all events.

| Field name | Field type | Description |
| --- | --- | --- |
| `connection_id` | string | Event connection ID. |
| `component.str` | string | Component name. |
| `component.length` | string | Component name length. |
| `producer.str` | string | Message producer name. |
| `producer.length` | string | Message producer name length. |
| `message.str` | string | Message text. |
| `message.length` | string | Message text length. |

## `parse` *(FULL mode only)*

Supported events: `preparse` and `postparse`.

| Field name | Field type | Description |
| --- | --- | --- |
| `connection_id` | string | Event connection ID. |
| `flags` | string | Parse rewrite flags value. |
| `query.str` | string | Original SQL query text. |
| `query.length` | string | Original SQL query text length. |
| `rewritten_query.str` | string | Rewritten SQL query text. |
| `rewritten_query.length` | string | Rewritten SQL query text length. |

## Abortability

Not every class or event supports execution blocking. The following table lists which filter-definition targets accept an `abort` item. When a filter tries to abort a non-abortable event, the server writes a warning to the error log and lets the statement through. See [Block statements with an audit log filter](block-statements-with-audit-filter.md).

| Class | Event subclass | Can be aborted |
|---|---|---|
| `table_access` | `read`, `insert`, `update`, `delete` | Yes |
| `message` | `internal`, `user` | Yes |
| `query` | `start`, `status_end`, `nested_start`, `nested_status_end` | Yes (`FULL` mode only) |
| `stored_program` | `execute` | Yes (`FULL` mode only) |
| `connection` | all subclasses | No |
| `general` | all subclasses | No |
| `command` | all subclasses | No |
| `parse` | all subclasses | No |
| `global_variable` | all subclasses | No |
| `authentication` | all subclasses | No |

## Additional reading

* [Write audit_log_filter definitions](write-filter-definitions.md)

* [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)

* [Audit Log Filter restrictions](audit-log-filter-restrictions.md)

* [Audit Log Filter file format overview](audit-log-filter-formats.md)

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Install the audit log filter](install-audit-log-filter.md)
