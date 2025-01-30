# Filter the Audit Log Filter logs

The audit filter log filtering is based on rules. The filter rule definition has the ability to include or exclude events based on the following attributes:

* User account
* Audit event class
* Audit event subclass
* Audit event fields (for example, `COMMAND_CLASS` or `STATUS`)

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

The function, `audit_log_filter_flush()`, forces reloading all filters and should only be invoked when modifying the audit tables. This function affects all users. Users in current sessions must either execute change-user or disconnect and reconnect.

## Constraints

The `component_audit_log_filter` component must be enabled and the audit tables must exist to use the audit log filter functions. The user account must have the required privileges. 

## Using the audit log filter functions

With a new connection, the audit log filter component finds the user account name in the filter assignments. If a filter has been assigned, the component uses that filter. If no filter has been assigned, but there is a default account filter, the component uses that filter. If there is no filter assigned, and there is no default account filter, then the component does not process any event.

The default account is represented by `%` as the account name.

You can assign filters to a specific user account or disassociate a user account from a filter. To disassociate a user account, either unassign a filter or assign a different filter. If you remove a filter, that filter is unassigned from all users, including current users in current sessions.

## set_filter options and available filters

| Filter           | Available options                                                                 |
|------------------|-----------------------------------------------------------------------------------|
| class Filter     | `general`: Logs general server events                                             |
|                  | `connection`: Tracks connection-related activities                                |
|                  | `table_access`: Monitors database table interactions                              |
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

### Examples

Create simple filters

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_set_filter('log_general', '{
  "filter": {
    "class": {
      "name": "general"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_connection', '{
  "filter": {
    "class": {
      "name": "connection"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_table_access', '{
  "filter": {
    "class": {
      "name": "table_access"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_global_variable', '{
  "filter": {
    "class": {
      "name": "global_variable"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_command', '{
  "filter": {
    "class": {
      "name": "command"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_query', '{
  "filter": {
    "class": {
      "name": "query"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_stored_program', '{
  "filter": {
    "class": {
      "name": "stored_program"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_authentication', '{
  "filter": {
    "class": {
      "name": "authentication"
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_message', '{
  "filter": {
    "class": {
      "name": "message"
    }
  }
}');
```

Add filter_update_on_user_change.

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_set_filter('log_connect', '{
  "filter": {
    "class": {
      "name": "connection",
      "event": {
        "name": "connect"
      }
    }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_disconnect', '{
  "filter": {
    "class": {
      "name": "connection",
      "event": {
        "name": "disconnect"
      }
    }
  }
}');
```

| Option      | Filters                                      | Example                        | Event                                     |
|-------------|---------------------------------------------|--------------------------------|-------------------------------------------|
| class       | general, connection, table_access           | N/A                            | general: Server-wide events, query processing<br>connection: Login, logout, connection attempts<br>table_access: Database and table-level interactions |
| user        | Filters by MySQL user accounts              | ["admin", "readonly_user"]     | All actions performed by specified users |
| database    | Filters by database name                    | ["sales", "inventory"]         | Operations within specified databases     |
| table       | Filters by table name                       | ["customers", "orders"]        | Interactions with specific tables         |
| operation   | For table_access: read, insert, update, delete<br>For connection: connect, disconnect | N/A                            | Specific types of database operations     |
| status      | 0: Successful queries<br>1: Failed queries   | N/A                            | Query execution result filtering          |
| thread_id   | Filters by specific MySQL thread identifiers | ["12345", "67890"]             | Actions within a particular database thread |
| query_time  | Filters based on query execution duration   | N/A                            | Long-running or quick queries             |

