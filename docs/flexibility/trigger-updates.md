# Trigger updates

Clients can issue simultaneous queries for a table. To avoid scalability problems, each thread-handling query has its own table instance. The server uses a special cache, called the Table Cache, which contains open table instanances. The use of the cache avoids paying the penalty in resources for opening and closing tables for each statement.

The `[table_open_cache`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_table_open_cache) system variable sets soft limits on the cache size. This limit can be temporarily exceeded if the currently executing queries require more open tables than specified. However, when these queries complete, the server closes the unused table instances from this cache using the least recently used (LRU) algorithm.

The [`table_open_cache_instances`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_table_open_cache_instances) system variable shows the number of open tables cache instances.

For more information, see [How MySQL opens and closes tables](https://dev.mysql.com/doc/refman/8.0/en/table-cache.html).

Opening a table with triggers in Table Cache also parses the trigger definitions and associates the open table instance with its own instances of the defined trigger bodies. When a connection executes a DML statement and must run a trigger, that connection gets its own instance of the trigger body for that specific open table instance. As a result of this approach, caching open table instances and also caching an associated trigger body for each trigger can consume a surprising amount of memory.

## Version changes

Percona Server for MySQL 8.0.31 adds the following abilities:

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

This variable allows you to set a soft limit on the maximum of open tables in the Table Cache, which contains fully-loaded triggers. By default, the value is the maximum value to avoid existing users observing a change in behavior.

If the number of open table instances with fully-loaded triggers exceeds the value, then unused table instances with fully-loaded triggers are removed. This operation uses the least recently used (LRU) method for managing storage areas.

The value can be a start-up option or changed dynamically.

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

The `SHOW CREATE TRIGGER` statement shows the CREATE statement used to create
the trigger. The statement also shows definitions which can no longer be
parsed. For example, you can show the definition of a trigger created before
a server upgrade which changed the trigger syntax.