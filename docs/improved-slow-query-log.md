# Improved slow query log

This feature adds microsecond time resolution and additional statistics to the slow query log output. It lets you turn the slow query log on or off at runtime, adds logging for the replica SQL thread, and adds fine-grained control over what and how much to log into the slow query log.

You can use the Percona Toolkit [pt-query-digest](https://docs.percona.com/percona-toolkit/pt-query-digest.html) tool to aggregate similar queries together and report on those that consume the most execution time.

## Version specific information

* 8.0.12-1: The feature was ported from Percona Server for MySQL 5.7.

## Other information

### Changes to the log format

The feature adds more information to the slow log output.

??? example "Expected output"

    ```{.text .no-copy}
    # Time: 130601  8:01:06.058915
    # User@Host: root[root] @ localhost []  Id:    42
    # Schema: imdb  Last_errno: 0  Killed: 0
    # Query_time: 7.725616  Lock_time: 0.000328  Rows_sent: 4  Rows_examined: 1543720  Rows_affected: 0
    # Bytes_sent: 272  Tmp_tables: 0  Tmp_disk_tables: 0  Tmp_table_sizes: 0
    # Full_scan: Yes  Full_join: No  Tmp_table: No  Tmp_table_on_disk: No
    # Filesort: No  Filesort_on_disk: No  Merge_passes: 0
    SET timestamp=1370073666;
    SELECT id,title,production_year FROM title WHERE title = 'Bambi';
    ```

Another example (log_slow_verbosity `=profiling`):

??? example "Expected output"

    ```{.text .no-copy}
    # Time: 130601  8:03:20.700441
    # User@Host: root[root] @ localhost []  Id:    43
    # Schema: imdb  Last_errno: 0  Killed: 0
    # Query_time: 7.815071  Lock_time: 0.000261  Rows_sent: 4  Rows_examined: 1543720  Rows_affected: 0
    # Bytes_sent: 272
    # Profile_starting: 0.000125 Profile_starting_cpu: 0.000120
    Profile_checking_permissions: 0.000021 Profile_checking_permissions_cpu: 0.000021
    Profile_Opening_tables: 0.000049 Profile_Opening_tables_cpu: 0.000048 Profile_init: 0.000048
    Profile_init_cpu: 0.000049 Profile_System_lock: 0.000049 Profile_System_lock_cpu: 0.000048
    Profile_optimizing: 0.000024 Profile_optimizing_cpu: 0.000024 Profile_statistics: 0.000036 
    Profile_statistics_cpu: 0.000037 Profile_preparing: 0.000029 Profile_preparing_cpu: 0.000029
    Profile_executing: 0.000012 Profile_executing_cpu: 0.000012 Profile_Sending_data: 7.814583
    Profile_Sending_data_cpu: 7.811634 Profile_end: 0.000013 Profile_end_cpu: 0.000012
    Profile_query_end: 0.000014 Profile_query_end_cpu: 0.000014 Profile_closing_tables: 0.000023
    Profile_closing_tables_cpu: 0.000023 Profile_freeing_items: 0.000051
    Profile_freeing_items_cpu: 0.000050 Profile_logging_slow_query: 0.000006
    Profile_logging_slow_query_cpu: 0.000006
    # Profile_total: 7.815085 Profile_total_cpu: 7.812127
    SET timestamp=1370073800;
    SELECT id,title,production_year FROM title WHERE title = 'Bambi';
    ```

Notice that the `Killed:` keyword is followed by zero when the
query successfully completes. This keyword is followed by a number other than zero if the query is unsuccessful:

| Killed Numeric Code | Exception                                      |
|---------------------|------------------------------------------------|
| 0                   | NOT_KILLED                                     |
| 1                   | KILL_BAD_DATA                                  |
| 1053                | ER_SERVER_SHUTDOWN (see MySQL Documentation)   |
| 1317                | ER_QUERY_INTERRUPTED (see MySQL Documentation) |
| 3024                | ER_QUERY_TIMEOUT (see MySQL Documentation)     |
| Any other number    | KILLED_NO_VALUE (Catches all other cases)      |

### Connection and Schema Identifier

Each slow log entry now contains a connection identifier so you can trace all the queries from a single connection. This identifier is the same value shown in the Id column in `SHOW FULL PROCESSLIST` or returned from the `CONNECTION_ID()` function.

Each entry also contains a schema name to trace all the queries for a particular schema.

??? example "Expected output"

    ```{.text .no-copy}
    # Id: 43  Schema: imdb
    ```

### Microsecond time resolution and extra row information

This microsecond time resolution and extra row information are the 'microflow` feature's original functionality. `Query_time` and `Lock_time` are logged with microsecond resolution.

The feature also adds information about how many rows were examined for `SELECT` queries and how many were analyzed and affected for `UPDATE`, `DELETE`, and `INSERT` queries.

??? example "Expected output"

    ```{.text .no-copy}
    # Query_time: 0.962742  Lock_time: 0.000202  Rows_sent: 4  Rows_examined: 1543719  Rows_affected: 0
    ```

Values and context:

* `Rows_examined`: Number of rows scanned - `SELECT`

* `Rows_affected`: Number of rows changed - `UPDATE`, `DELETE`, `INSERT`

### Memory footprint

The feature provides information about the amount of bytes sent for the result of the query and the number of temporary tables created for its execution - differentiated by whether they were created on memory or on disk - with the total number of bytes used by them.

??? example "Expected output"

    ```{.text .no-copy}
    # Bytes_sent: 8053  Tmp_tables: 1  Tmp_disk_tables: 0  Tmp_table_sizes: 950528
    ```

Values and context:

* `Bytes_sent`: The amount of bytes sent for the result of the query

* `Tmp_tables`: Number of temporary tables created on memory for the query

* `Tmp_disk_tables`: Number of temporary tables created on disk for the query

* `Tmp_table_sizes`: Total Size in bytes for all temporary tables used in the query

### Query plan information

The database can execute a query using different methods:

* Using indexes

* Scanning the entire table

* Creating temporary tables

Each query can be executed in various ways. For example, it may use indexes or do a full table scan, or a temporary table may be needed. These are the things that you can usually see by running `EXPLAIN` on the query. The feature will now allow you to see the most important facts about the execution in the log file.

??? example "Expected output"

    ```{.text .no-copy}
    # Full_scan: Yes  Full_join: No  Tmp_table: No  Tmp_table_on_disk: No
    # Filesort: No  Filesort_on_disk: No  Merge_passes: 0
    ```

The values and their meanings are documented with the [`log_slow_filter`](slow-extended.md#log_slow_filter) option.

### InnoDB usage information

The final part of the output is the InnoDB usage statistics. MySQL currently shows many per-session statistics for operations with `SHOW SESSION STATUS`, but that does not include those of InnoDB, which are always global and shared by all threads. This feature lets you see those values for a given query.

??? example "Expected output"

    ```{.text .no-copy}
    #   InnoDB_IO_r_ops: 6415  InnoDB_IO_r_bytes: 105103360  InnoDB_IO_r_wait: 0.001279
    #   InnoDB_rec_lock_wait: 0.000000  InnoDB_queue_wait: 0.000000
    #   InnoDB_pages_distinct: 6430
    ```


| Value               | Description                                                                                                                                                                          |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| InnoDB_IO_r_ops       | Counts the planned page read operations. The actual number may differ due to asynchronous operations.                                                                                 |
| InnoDB_IO_r_bytes     | Similar to InnoDB_IO_r_ops but measures the operations in bytes instead of counts.                                                                                                   |
| InnoDB_IO_r_wait      | Shows how long (in seconds) InnoDB took to read data from storage.                                                                                                                   |
| InnoDB_rec_lock_wait  | Indicates how long (in seconds) the query waited for row locks.                                                                                                                      |
| InnoDB_queue_wait     | Measures how long (in seconds) the query waited to enter the InnoDB queue or waited inside the queue for execution.                                                                  |
| InnoDB_pages_distinct | Estimates the number of unique pages the query accessed. It uses a small hash array to represent the entire buffer pool, which may lead to inaccuracy for queries accessing many pages. |


If the query did not use *InnoDB* tables, that information is written into the log instead of the above statistics.
