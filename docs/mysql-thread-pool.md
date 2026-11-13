# MySQL thread pool plugin

The plugin applies to Percona Server for MySQL 9.7.2-2 and later releases and the MySQL thread pool plugin implementation.

!!! note "You cannot implement multiple thread pools"

    Percona Server for MySQL 9.7.2-2 is the first release that includes the MySQL thread pool plugin. The Percona thread pool implementation is also available.
    
    If you try to implement multiple thread pools, the MySQL thread pool does not load. If the Percona thread pool is configured, the MySQL thread_pool plugin refuses to load.
    
    This page covers the MySQL thread pool plugin. For the Percona thread pool implementation, see [Thread pool](threadpool.md).

## Version changes

Percona Server for MySQL 9.7.2-2 provides thread pooling as the `thread_pool` plugin.

## Thread pool operation

When a transaction begins, its initial statement is placed in the low-priority queue; subsequent statements from the active transaction receive high-priority treatment. A high session count increases context switches and lock contention. The plugin shares a limited set of worker threads across many sessions. The plugin caps the number of workers that run at the same time.

The plugin creates thread groups. The plugin assigns each session to a group in repeating cycle order. Each group holds a high-priority queue and a low-priority queue.

The first statement of a transaction enters the low-priority queue. Later statements of that open transaction enter the high-priority queue.

Each group takes work from the high-priority queue first.

For upstream plugin behavior, see [MySQL Thread Pool](https://dev.mysql.com/doc/refman/26.7/en/thread-pool.html) in the MySQL Reference Manual.

## Prerequisites

Complete the following requirements before you install the plugin:

* Percona Server for MySQL 9.7.2-2 or a later version runs on the host.

* Your operating system account can edit `my.cnf` and restart the server.

* Your MySQL account can query `INFORMATION_SCHEMA` and `performance_schema`.

* The plugin library file `thread_pool.so` exists in the plugin directory.

* The server is not configured to use the Percona thread pool. If any Percona thread pool variable is set in my.cnf, the MySQL plugin refuses to load. See [Migrate from the Percona thread pool](#migrate-from-the-percona-server).

## Install the thread pool plugin

1. Find the plugin directory:

    ```sql
    SHOW VARIABLES LIKE 'plugin_dir';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +---------------+--------------------------+
        | Variable_name | Value                    |
        +---------------+--------------------------+
        | plugin_dir    | /usr/lib64/mysql/plugin/ |
        +---------------+--------------------------+
        ```

    The `Value` column depends on the operating system and the package layout.

2. Confirm that the plugin library file exists in the plugin directory. Replace `<plugin_dir>` with the value from step 1:

    ```bash
    ls <plugin_dir>/thread_pool.so
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        /usr/lib64/mysql/plugin/thread_pool.so
        ```

3. Add the following lines to `my.cnf`:

    ```ini
    [mysqld]
    plugin-load-add=thread_pool.so
    ```

4. Restart the server. On Red Hat Enterprise Linux and derivatives, the service name is `mysqld`:

    ```shell
    sudo systemctl restart mysql
    ```

    The command returns nothing when the service restarts.

## Verify the installation

1. Confirm the plugin status:

    ```sql
    SELECT PLUGIN_NAME, PLUGIN_STATUS
    FROM INFORMATION_SCHEMA.PLUGINS
    WHERE PLUGIN_NAME LIKE 'thread%';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +-------------+---------------+
        | PLUGIN_NAME | PLUGIN_STATUS |
        +-------------+---------------+
        | thread_pool | ACTIVE        |
        +-------------+---------------+
        ```

2. Confirm the thread handling model:

    ```sql
    SHOW VARIABLES LIKE 'thread_handling';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +-----------------+--------------------+
        | Variable_name   | Value              |
        +-----------------+--------------------+
        | thread_handling | loaded-dynamically |
        +-----------------+--------------------+
        ```

    A successful plugin load sets `thread_handling` to `loaded-dynamically`.

3. Confirm the monitoring tables:

    ```sql
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'performance_schema'
    AND TABLE_NAME LIKE 'tp%';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +-----------------------+
        | TABLE_NAME            |
        +-----------------------+
        | tp_thread_group_state |
        | tp_thread_group_stats |
        | tp_thread_state       |
        +-----------------------+
        ```

The error log records a plugin initialization failure.

## Migrate from the Percona Server

The Percona thread pool and the MySQL thread_pool plugin cannot run at the same time. If any of the following variables are still set in `my.cnf`, the thread_pool plugin refuses to load:

* `thread_handling`

* `thread_pool_high_prio_mode`

* `thread_pool_high_prio_tickets`

* `thread_pool_idle_timeout`

* `thread_pool_max_threads`

* `thread_pool_oversubscribe`

Do not keep `thread_handling=pool-of-threads`. A successful plugin load sets `thread_handling` to `loaded-dynamically`.

1. Record the current thread pool configuration before the upgrade:

    ```sql
    SHOW VARIABLES LIKE 'thread%';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +-------------------------------+-------------+
        | Variable_name                 | Value       |
        +-------------------------------+-------------+
        | thread_handling               | pool-of-threads |
        | thread_pool_high_prio_mode    | transactions |
        | thread_pool_high_prio_tickets | 4294967295  |
        | thread_pool_idle_timeout      | 60          |
        | thread_pool_max_threads       | 100000      |
        | thread_pool_oversubscribe     | 3           |
        | thread_pool_size              | 16          |
        | thread_pool_stall_limit       | 500         |
        +-------------------------------+-------------+
        ```

    The result can include other variables that match `thread%`. Record every `thread_pool_%` value and `thread_handling`.

2. Upgrade the server to Percona Server for MySQL 9.7.2-2 or later. See [Upgrade procedures](upgrade-procedures.md).

3. Stop the server:

    ```shell
    sudo systemctl stop mysql
    ```

    Keep the server stopped during the `my.cnf` edits. The `plugin-load-add` only takes effect when the server starts. 

3. Remove the following variables from `my.cnf`: `thread_handling`, `thread_pool_high_prio_mode`, `thread_pool_high_prio_tickets`, `thread_pool_idle_timeout`, `thread_pool_max_threads`, and `thread_pool_oversubscribe`.

4. Add the plugin to `my.cnf`:

    ```ini
    [mysqld]
    plugin-load-add=thread_pool.so
    ```

5. Convert the values recorded in step 1 using the [System variable mapping table](#system-variable-mapping). Add the converted variables to the `[mysqld]` section of `my.cnf`.

6. Restart the server:

    ```bash
    sudo systemctl restart mysql
    ```

    The command returns nothing when the service restarts.

7. Complete the steps in [Verify the installation](#verify-the-installation).

### System variable mapping

| Removed variable | Replacement | Migration action |
|------------------|-------------|------------------|
| `thread_handling=pool-of-threads` | `plugin-load-add=thread_pool.so` | Remove the variable. A successful plugin load sets `thread_handling` to `loaded-dynamically`. |
| `thread_pool_size` | `thread_pool_size` | Keep the value. The default value changes from the number of processors to 16. |
| `thread_pool_stall_limit` | `thread_pool_stall_limit` | Divide the recorded value by 10. The unit changes from milliseconds to 10-millisecond intervals. A recorded value of `500` converts to `50`. |
| `thread_pool_high_prio_mode` | `thread_pool_high_priority_connection` | Set `thread_pool_high_priority_connection` to `1` for a session that requires the high-priority queue. The default value `0` matches the `transactions` mode. |
| `thread_pool_high_prio_tickets` | `thread_pool_prio_kickup_timer` | Set the number of milliseconds before the thread pool moves a statement to the high-priority queue. The default value is `1000`. |
| `thread_pool_oversubscribe` | `thread_pool_query_threads_per_group` and `thread_pool_max_active_query_threads` | Set `thread_pool_query_threads_per_group` to `2` as a starting value. Set `thread_pool_max_active_query_threads` to limit the active threads per group. |
| `thread_pool_idle_timeout` | `thread_pool_max_unused_threads` | Set the number of idle workers that the plugin keeps. The value `0` permits an unlimited number of idle workers. |
| `thread_pool_max_threads` | `thread_pool_max_transactions_limit` | Set the maximum number of concurrent transactions. The sum of `max_connections` and `thread_pool_size` defines the maximum number of threads. |

### Example `my.cnf` changes

The following fragment loads the plugin and the converted replacements. Place the fragment in the `[mysqld]` section:

```ini
[mysqld]
plugin-load-add=thread_pool.so
thread_pool_size=16
thread_pool_stall_limit=50
thread_pool_prio_kickup_timer=1000
thread_pool_query_threads_per_group=2
thread_pool_max_unused_threads=0
thread_pool_max_transactions_limit=0
```

The example converts `thread_pool_stall_limit` from `500` milliseconds to `50` intervals of 10 milliseconds.

The example omits `thread_pool_high_priority_connection`. The default value `0` matches `thread_pool_high_prio_mode=transactions`.

Set `thread_pool_high_priority_connection=1` in a session that requires the high-priority queue.

`thread_pool_max_unused_threads=0` permits an unlimited number of idle workers.

`thread_pool_max_transactions_limit=0` does not cap concurrent transactions. Adjust the value after you record `max_connections` and the expected concurrency.

The `Threadpool_*` status variables are not `my.cnf` settings. Point monitoring at the Performance Schema tables in [Status variable mapping](#status-variable-mapping).

### Status variable mapping

The MySQL thread pool plugin does not expose the `Threadpool_average_hp_queue_wait_us`, `Threadpool_average_queue_wait_us`, `Threadpool_idle_threads`, `Threadpool_requests_starved_in_queue`, `Threadpool_requests_waiting_in_hp_queue`, `Threadpool_requests_waiting_in_queue`, and `Threadpool_threads` status variables. Replace monitoring queries and alerts that read these status variables with queries against the following Performance Schema tables:

* `performance_schema.tp_thread_group_state`: reports the state of each thread group.

* `performance_schema.tp_thread_group_stats`: reports statistics per thread group.

* `performance_schema.tp_thread_state`: reports the state of each thread in a thread group.

The `tp_*` tables appear when the plugin is active. The tables disappear when the plugin is not loaded.

## System variables

The thread pool plugin exposes the following system variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `thread_pool_algorithm` | `0` | Selects the scheduler. Value `1` targets high concurrency. |
| `thread_pool_dedicated_listeners` | `OFF` | Assigns each group a listener that only accepts incoming statements. |
| `thread_pool_high_priority_connection` | `0` | Sends every statement of a session to the high-priority queue when the value is `1`. |
| `thread_pool_max_active_query_threads` | `0` | Caps active workers in a group. Value `0` uses the plugin default rule. |
| `thread_pool_max_transactions_limit` | `0` | Caps concurrent transactions. |
| `thread_pool_max_unused_threads` | `0` | Caps idle workers that remain in the pool. |
| `thread_pool_prio_kickup_timer` | `1000` | Wait time in milliseconds before a low-priority statement moves to the high-priority queue. |
| `thread_pool_query_threads_per_group` | `1` | Sets the number of query workers per group. |
| `thread_pool_size` | `16` | Sets the number of thread groups. |
| `thread_pool_stall_limit` | `6` | Stall timeout. Each unit equals 10 milliseconds. The maximum value is `600`. |
| `thread_pool_transaction_delay` | `0` | Wait time in milliseconds before a worker starts a transaction. |

## Tuning

Keep the plugin defaults as a baseline. Change one variable at a time. Measure throughput after each change.

Set `thread_pool_size` in `my.cnf`. The plugin does not apply a runtime change to `thread_pool_size`.

`thread_pool_stall_limit` uses 10-millisecond units. The default `6` equals 60 milliseconds. The maximum `600` equals six seconds.

Inspect stall counts in `performance_schema.tp_thread_group_stats`:

```sql
SELECT STALLED_QUERIES_EXECUTED, QUERIES_EXECUTED
FROM performance_schema.tp_thread_group_stats;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------------+-------------------+
    | STALLED_QUERIES_EXECUTED | QUERIES_EXECUTED  |
    +--------------------------+-------------------+
    |                        0 |                 0 |
    |                        0 |                 0 |
    +--------------------------+-------------------+
    ```

The result contains one row per thread group. A high `STALLED_QUERIES_EXECUTED` value means statements exceed `thread_pool_stall_limit`. Raise `thread_pool_stall_limit` to reduce stall events.


## Privileged connections

`thread_pool_max_transactions_limit` can block ordinary sessions when the cap is reached. A session with `TP_CONNECTION_ADMIN` bypasses that cap. Use that session to raise the cap, clear the cap, or run `KILL` on a blocked session.

Issue an explicit `GRANT` for `TP_CONNECTION_ADMIN`. The server does not add this privilege to accounts by default:

```sql
GRANT TP_CONNECTION_ADMIN ON *.* TO 'admin_user'@'localhost';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

The plugin places that session in the `Admin` thread group.

The last row of `performance_schema.tp_thread_group_stats` reports the `Admin` thread group.
