# Trigger updates

In MySQL, the system efficiently handles multiple client queries to the same table by opening separate table instances for each query. This prevents delays and conflicts. The use of a "Table Cache" speeds up access by reducing the need to repeatedly open and close tables, improving overall performance.

The [table_open_cache] system variable controls the number of tables MySQL can keep open simultaneously across all threads. By increasing this setting, MySQL can handle more open files, although this requires more file descriptors. Despite a soft limit, MySQL can temporarily exceed it if queries demand more open tables. Upon query completion, MySQL automatically manages the cache by closing the least recently used tables.

The [table_open_cache_instances] system variable controls the number of open table cache instances in MySQL. By splitting the open tables cache into smaller segments (table_open_cache divided by table_open_cache_instances), sessions can access only one instance at a time for DML operations, reducing contention and improving performance when many sessions are running. For systems with 16 or more CPU cores, a value of 8 or 16 is recommended. However, if many large triggers are causing high memory usage, setting this variable to 1 can help limit memory consumption.

When a table with triggers is opened in the Table Cache, it also reads the trigger definitions and links the open table instance to its specific trigger instances. When a connection executes a Data Manipulation Language (DML) statement that activates a trigger, that connection uses its own instance of the trigger body for that particular table instance. This method of caching both the open table instances and their associated trigger bodies can unexpectedly use a significant amount of memory.

Percona Server for MySQL has the following abilities:

* Avoid using table instances with fully-loaded and parsed triggers by read-only queries

* Show trigger CREATE statements even if the statement is unparseable

The additional system variable reduces the Table Cache memory consumption on the server when tables that contain trigger definitions also are part of a significant read-only workload.

## System variables

### table_open_cache_triggers

<table width="100%">
    <col style="width:20%">
    <col style="width:80%">
</table>

| Option         | Description                 |
|----------------|-----------------------------|
| Command-line   | `--table-open-cache-triggers` |
| Dynamic        | Yes                         |
| Scope          | Global                      |
| Data type      | Integer                     |
| Default        | 524288                      |
| Minimum value  | 1                           |
| Maximum value  | 524288                      |

This variable sets a soft limit on the maximum number of open tables in the Table Cache, which holds fully loaded triggers. By default, this value is set to the maximum to prevent any changes in behavior for existing users. If the number of open table instances with fully loaded triggers exceeds this limit, the system removes the least recently used unused table instances. You can set this value as a start-up option or change it dynamically while the system runs.

## Status variables

The following status variables are available:
<style>
    table th:first-of-type { width: 40%;
    }
    table th:nth-of-type(2) { width: 60%;
    }
</style>

| Variable name                         | Description |
|---------------------------------------|-------------|
| `table_open_cache_triggers_hits`      |  A hit means the statement required an open table instance with fully-loaded triggers and was able to get one from the `table_open_cache`.            |
| `table_open_cache_triggers_misses`    |  A miss means the statement requiring an open table instance with fully-loaded triggers was not found one in the `table_open_cache`. The statement may find a table instance without fully-loaded triggers and finalized their loading for it.            |
| `table_open_cache_triggers_overflows` |   An overflow indicates the number of unused table instances with triggers that were expelled from the `table_open_cache` due to the `table_open_cache_triggers` soft limit. This variable may demonstrate that the `table_open_cache_triggers` value should be increased.          |

## SHOW CREATE TRIGGER statment changes

The `SHOW CREATE TRIGGER` statement displays the SQL command that created a trigger, including definitions that may no longer be understandable. For example, if a trigger was created before a server upgrade that changed the trigger syntax, this statement will still show its definition.

## Additional resources

For more information, see [How MySQL opens and closes tables].

[table_open_cache]: https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-variables.html#sysvar_table_open_cache
[table_open_cache_instances]: https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-variables.html#sysvar_table_open_cache_instances

[How MySQL opens and closes tables]: https://dev.mysql.com/doc/refman/{{vers}}/en/table-cache.html