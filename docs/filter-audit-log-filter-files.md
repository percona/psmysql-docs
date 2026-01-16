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

## Function behavior and edge cases

### audit_log_filter_set_filter()

**Behavior when filter name already exists:**
* If a filter with the same name already exists, the function returns an error
* To update an existing filter, you must first remove it, then create a new one with the same name
* Alternatively, modify the filter directly in the `mysql.audit_log_filter` table and call `audit_log_filter_flush()`

**Example:**
```sql
-- First attempt creates the filter
SELECT audit_log_filter_set_filter('my_filter', '{"filter": {"log": true}}');
-- Returns: OK

-- Second attempt with same name fails
SELECT audit_log_filter_set_filter('my_filter', '{"filter": {"log": false}}');
-- Returns: ERROR: Filter 'my_filter' already exists
```

### audit_log_filter_set_user()

**Wildcard support (8.4.4+):**
Starting from Percona Server for MySQL 8.4.4, `audit_log_filter_set_user()` accepts wildcard characters (`%` and `_`) in the host part of user accounts.

**Examples:**
```sql
-- Match user from any host
SELECT audit_log_filter_set_user('admin@%', 'log_all');

-- Match user from specific IP subnet
SELECT audit_log_filter_set_user('user@192.168.0.%', 'log_all');

-- Match user from specific domain
SELECT audit_log_filter_set_user('user@%.example.com', 'log_all');

-- Match user with underscore in hostname
SELECT audit_log_filter_set_user('user@db_server_1', 'log_all');
```

**Behavior when assigning filter to non-existent user:**
* The function succeeds even if the user account doesn't exist
* The filter assignment is stored in `mysql.audit_log_user` table
* When the user connects, the filter is applied
* If the user never connects, the assignment remains but has no effect

**Behavior when user is in current session:**
* If a user is currently connected, changing their filter assignment does not affect their current session
* The new filter takes effect when:
  * The user disconnects and reconnects, or
  * The user executes `CHANGE_USER` command

### audit_log_filter_remove_filter()

**Behavior when filter is assigned to users:**
* When you remove a filter, it is automatically unassigned from all users (including the default `%` account)
* Current sessions are detached from the filter immediately
* New connections for affected users fall back to:
  * Default filter (if one exists), or
  * No filtering (if no default exists)

**Example:**
```sql
-- Remove filter that's assigned to multiple users
SELECT audit_log_filter_remove_filter('log_all');
-- All users assigned to 'log_all' are now unassigned
-- Current sessions continue without filter
-- New connections use default filter or no filtering
```

### audit_log_filter_remove_user()

**Behavior:**
* Removing a user's filter assignment does not affect their current session
* New sessions for the user will use:
  * Default filter (if one exists), or
  * No filtering (if no default exists)

**Removing default filter:**
* To remove the default filter, use: `SELECT audit_log_filter_remove_user('%');`
* This affects all users without specific filter assignments

## Modifying filters via tables vs functions

You can modify audit log filters in two ways: using functions or by directly modifying the audit tables.

### Using functions (recommended)

**Advantages:**
* Validation of filter definitions
* Immediate effect (no flush required)
* Error messages for invalid configurations
* Atomic operations

**Example:**
```sql
SELECT audit_log_filter_set_filter('my_filter', '{"filter": {"log": true}}');
-- Filter is immediately active
```

### Direct table modification

**When to use:**
* Bulk updates of multiple filters
* Script-based configuration management
* Replication scenarios (with caution)

**Important:**
* Changes to `mysql.audit_log_filter` or `mysql.audit_log_user` tables do not take effect automatically
* You must call `audit_log_filter_flush()` after making table changes
* No validation is performed on filter definitions
* Invalid JSON in filter definitions can cause errors

**Example:**
```sql
-- Direct table modification
INSERT INTO mysql.audit_log_filter (NAME, FILTER) 
VALUES ('my_filter', '{"filter": {"log": true}}');

-- Must flush to activate
SELECT audit_log_filter_flush();
```

### Replication implications

**Default behavior:**
* By default, `mysql.audit_log_filter` and `mysql.audit_log_user` tables are replicated
* Changes on the source server replicate to replica servers
* However, replicated table changes do not automatically activate filters on the replica

**What happens:**
1. Source server: Filter is created and activated
2. Replication: Table changes are replicated to replica
3. Replica server: Filter exists in table but is NOT active in memory
4. Replica server: Must call `audit_log_filter_flush()` or restart server to activate

**Recommendation:**
Configure replication to ignore audit log filter tables:
```ini
# In my.cnf
replicate-ignore-table=mysql.audit_log_filter
replicate-ignore-table=mysql.audit_log_user
```

This ensures:
* Each server has independent filter configuration
* No conflicts between source and replica filters
* Better control over audit logging on each server

## Translating 8.0 include/exclude variables to JSON filters

If you're migrating from Percona Server 8.0 plugin to 8.4 component, you need to convert old include/exclude variables to JSON filter definitions.

### Variable mapping table

| 8.0 Plugin Variable | 8.4 Component JSON Filter | Example |
|---------------------|---------------------------|---------|
| `audit_log_include_accounts` | `"user": ["user1", "user2"]` | Include specific users |
| `audit_log_exclude_accounts` | `"user": ["user1"], "negate": true` | Exclude specific users |
| `audit_log_include_commands` | `"class": {"name": "general"}, "event": {"name": "command"}` | Include specific commands |
| `audit_log_exclude_commands` | `"class": {"name": "general"}, "event": {"name": "command"}, "negate": true` | Exclude specific commands |
| `audit_log_include_databases` | `"database": ["db1", "db2"]` | Include specific databases |
| `audit_log_exclude_databases` | `"database": ["db1"], "negate": true` | Exclude specific databases |

### Migration examples

**8.0 Configuration:**
```ini
audit_log_include_accounts = admin@localhost, dba@%
audit_log_exclude_databases = test, temp
```

**8.4 JSON Filter:**
```json
{
  "filter": {
    "class": [
      {
        "name": "general",
        "user": ["admin", "dba"],
        "database": ["test", "temp"],
        "negate": true
      }
    ]
  }
}
```

**8.0 Configuration:**
```ini
audit_log_include_commands = SELECT, INSERT, UPDATE, DELETE
audit_log_exclude_accounts = readonly_user@%
```

**8.4 JSON Filter:**
```json
{
  "filter": {
    "class": [
      {
        "name": "general",
        "event": [{"name": "command"}],
        "user": ["readonly_user"],
        "negate": true
      }
    ]
  }
}
```

### Complete migration procedure

1. **Document current 8.0 configuration:**
   * List all `audit_log_include_*` and `audit_log_exclude_*` variables
   * Note their values

2. **Convert to JSON filters:**
   * Use the mapping table above
   * Create filter definitions for each include/exclude rule
   * Combine related rules into single filters where possible

3. **Test filters:**
   * Create filters in a test environment
   * Verify they match the behavior of old plugin configuration
   * Adjust as needed

4. **Deploy to production:**
   * Install 8.4 component
   * Create JSON filters
   * Assign filters to users
   * Verify functionality

For complete migration instructions, see [Migration Guide](audit-log-filter-migration.md).

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

!!! note "Filter definition"
    Status values must be specified as strings (for example, `"0"`, `"1"`). The audit log filter does not filter on integer values, only on string values. If you use integer values, you will see the error: `ERROR: Incorrect rule definition.`

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
    "class": { "name": "connection" },
    "event": { "name": "connect" }
  }
}');

mysql> SELECT audit_log_filter_set_filter('log_disconnect', '{
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
    Status, thread ID, and connection ID values must be specified as strings (for example, `"0"`, `"1"`, `"12345"`). The audit log filter does not filter on integer values, only on string values. If you use integer values, you will see the error: `ERROR: Incorrect rule definition.`

