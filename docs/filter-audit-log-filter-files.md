# Filter the Audit Log Filter logs

The audit filter log filtering is based on rules. The filter rule definition has the ability to include or exclude events based on the following attributes:

* User account
* Audit event class
* Audit event subclass
* Audit event fields (for example, `COMMAND_CLASS` or `STATUS`)

From Percona Server for MySQL 8.4.8-8: The NEW XML formatter (`audit_log_filter.format=NEW`) behavior described here—including which `<NAME>` strings and child elements appear in each `<AUDIT_RECORD>`—was verified for that release on the {{vers}} line. This documentation build is {{release}}. If your server predates 8.4.8-8, or you use a build whose audit code differs, compare against a real log from your server.

When you inspect new-style XML logs for that line of releases, expect values such as `Startup`, `Shutdown`, `Disconnect`, `Query Start`, `Query Status End`, and `Connection` as the `COMMAND_CLASS` on connect and disconnect. For the full field list per event type, see [XML (new style)](audit-log-filter-new.md).

You can define multiple filters and assign any filter to multiple accounts. You can also create a default filter for specific user accounts. The filters are defined using function calls. After the filter is defined, the filter is stored in `mysql` system tables. 

## Audit Log Filter functions

The Audit Log filter functions require `AUDIT_ADMIN` or `SUPER` privilege. 

The following functions are used for rule-based filtering:

| Function | Description | Example |
|---|---|---|
| audit_log_filter_flush() | Manually flush the filter tables | `SELECT audit_log_filter_flush()`
| audit_log_filter_set_filter() | Defines a filter | `SELECT audit_log_filter_set_filter('log_connections','{ "filter":{}}'`')
| audit_log_filter_remove_filter() | Removes a filter |
| audit_log_filter_set_user() | Assigns a filter to a specific user account |
| audit_log_filter_remove_user() | Removes the filters from a specific user account |

Using a SQL interface, you can define, display, or modify audit log filters. The filters are stored in the `mysql` system database.

The [`audit_log_session_filter_id()`](audit-log-filter-variables.md#audit_log_session_filter_id) function returns the internal ID of the audit log filter in the current session.

Filter definitions are `JSON` values.

The function, `audit_log_filter_flush()`, forces reloading all filters and should only be invoked when modifying the audit tables. After a flush, existing sessions are detached from their filters and stop logging until they reconnect or execute `CHANGE_USER`, at which point the filter is re-resolved from the reloaded registry.

## Constraints

The `component_audit_log_filter` component must be enabled and the audit tables must exist to use the audit log filter functions. The user account must have the required privileges. 

## Event mode

The [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) variable controls which event classes and subclasses are processed. In `REDUCED` mode (the default), only a curated subset of events is available for filtering. In `FULL` mode, all event classes and subclasses are available.

In REDUCED mode, `audit_log_filter_set_filter()` rejects new filter definitions that reference disabled event classes or subclasses. Persisted filters created under FULL mode that reference disabled classes still load after a restart or flush — the disabled classes are silently skipped with a warning.

## Filter definition validation

Filter definitions are validated at parse time. The following are rejected with a descriptive error:

* Unknown field names (e.g., `"WRONG.str"`)
* Invalid class names or event subclass names
* Empty arrays (e.g., `"class": []`)
* Unknown JSON keys
* `print` rules referencing invalid fields for one of the classes in a multi-class array

An empty filter object `{}` is equivalent to `{"filter": {"log": true}}` and logs all events. If you want a filter that logs nothing, use `{"filter": {"log": false}}`.

Parse event subclass names must use `preparse` and `postparse`.

## Using the audit log filter functions

With a new connection, the audit log filter component finds the user account name in the filter assignments. If a filter has been assigned, the component uses that filter. If no filter has been assigned, but there is a default account filter, the component uses that filter. If there is no filter assigned, and there is no default account filter, then the component does not process any event.

The default account is represented by `%` as the account name.

You can assign filters to a specific user account or disassociate a user account from a filter. To disassociate a user account, either unassign a filter or assign a different filter. When you call `audit_log_filter_set_user()`, existing sessions keep their original filter until they reconnect or execute `CHANGE_USER`; only new connections pick up the new mapping. If you remove a filter with `audit_log_filter_remove_filter()`, only sessions using that filter are detached; sessions using other filters continue logging normally.

## set_filter options and available filters

| Filter           | Available options                                                                 |
|------------------|-----------------------------------------------------------------------------------|
| class Filter     | `general`: Logs general server events                                             |
|                  | `connection`: Tracks connection-related activities                                |
|                  | `table_access`: Monitors database table interactions                              |
|                  | `global_variable`: Global variable changes (requires `event_mode=FULL`)           |
|                  | `command`: Server commands (requires `event_mode=FULL`)                           |
|                  | `query`: Query events (requires `event_mode=FULL`)                                |
|                  | `stored_program`: Stored program events (requires `event_mode=FULL`)              |
|                  | `authentication`: Authentication events (requires `event_mode=FULL`)              |
|                  | `message`: Audit message events                                                  |
|                  | `parse`: Parse events with subclasses `preparse` and `postparse` (requires `event_mode=FULL`) |
| user Filter      | Accepts specific usernames as filter criteria                                     |
|                  | Can include multiple usernames                                                   |
|                  | Supports wildcard matching                                                       |
| database Filter  | Filters events by database name                                                  |
|                  | Accepts exact database names                                                     |
|                  | Supports wildcard matching for database selection                                |
| table Filter     | Specifies individual table names                                                 |
|                  | Allows filtering for specific tables within databases                            |
|                  | Supports wildcard matching                                                       |
| operation Filter | `read`: SELECT statements                                                       |
|                  | `write`: INSERT, UPDATE, DELETE statements                                       |
|                  | `ddl`: Data Definition Language operations                                       |
|                  | `dcl`: Data Control Language operations                                          |
| event Filter     | `status`: Tracks query execution status                                          |
|                  | `query`: Captures query details                                                  |
|                  | `connection`: Monitors connection events                                         |
| status Filter    | `0`: Successful operations                                                      |
|                  | `1`: Failed operations                                                          |

!!! note "Filter definition"
    Integer event fields (such as `error_code`, `connection_id`, `connection_type`) accept both integer and string values. For example, you can use `"value": 0` or `"value": "0"`. The `connection_type` field also accepts symbolic constants (`::undefined`, `::tcp/ip`, `::socket`, `::named_pipe`, `::ssl`, `::shared_memory`).

### Examples

Create simple filters

```sql
SELECT audit_log_filter_set_filter('log_general', '{
  "filter": {
    "class": {
      "name": "general"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_connection', '{
  "filter": {
    "class": {
      "name": "connection"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_table_access', '{
  "filter": {
    "class": {
      "name": "table_access"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_global_variable', '{
  "filter": {
    "class": {
      "name": "global_variable"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_command', '{
  "filter": {
    "class": {
      "name": "command"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_query', '{
  "filter": {
    "class": {
      "name": "query"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_stored_program', '{
  "filter": {
    "class": {
      "name": "stored_program"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_authentication', '{
  "filter": {
    "class": {
      "name": "authentication"
    }
  }
}');

SELECT audit_log_filter_set_filter('log_message', '{
  "filter": {
    "class": {
      "name": "message"
    }
  }
}');
```

Add filter_update_on_user_change.

```sql
SELECT audit_log_filter_set_filter('log_connect', '{
  "filter": {
    "class": { "name": "connection" },
    "event": { "name": "connect" }
  }
}');

SELECT audit_log_filter_set_filter('log_disconnect', '{
  "filter": {
    "class": { "name": "connection" },
    "event": { "name": "disconnect" }
  }
}');
```

| Option      | Filters                                      | Example                        | Event                                     |
|-------------|---------------------------------------------|--------------------------------|-------------------------------------------|
| class       | general, connection, table_access           | N/A                            | General: Server-wide events, query processing<br>connection: Login, logout, connection attempts<br>table_access: Database and table-level interactions |
| user        | Filters by MySQL user accounts              | ["admin", "readonly_user"]     | All actions performed by specified users |
| database    | Filters by database name                    | ["sales", "inventory"]         | Operations within specified databases     |
| table       | Filters by table name                       | ["customers", "orders"]        | Interactions with specific tables         |
| operation   | For table_access: read, insert, update, delete<br>For connection: connect, disconnect | N/A                            | Specific types of database operations     |
| status      | 0: Successful queries<br>1: Failed queries   | N/A                            | Query execution result filtering          |
| thread_id   | Filters by specific MySQL thread identifiers | ["12345", "67890"]             | Actions within a particular database thread |
| query_time  | Filters based on query execution duration   | N/A                            | Long-running or quick queries             |

!!! note "Filter definition"
    Integer event fields (such as `error_code`, `connection_id`, `connection_type`) accept both integer and string values. For example, you can use `"value": 0` or `"value": "0"` for numeric fields. The `connection_type` field also accepts symbolic constants.

