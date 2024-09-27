# Slow query log variables

This feature adds microsecond time resolution and additional statistics to the slow query log output. It lets you enable or disable the slow query log at runtime, adds logging for the replica SQL thread, and adds fine-grained control over what and how much to log into the slow query log.

## System Variables

### `log_slow_filter`

| Option       | Description     |
|--------------|-----------------|
| Command-line | Yes             |
| Config file  | Yes             |
| Scope        | Global, Session |
| Dynamic      | Yes             |

Controls which slow queries are recorded in the slow query log based on any combination of the following values:

| Option            | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| `filesort`        | Logs when a query requires sorting.                               |
| `filesort_on_disk`| Records queries that sort results using temporary tables on disk. |
| `full_join`       | Records queries that join tables without using indexes.           |
| `full_scan`       | Records queries that scan the entire table.                       |
| `qc_miss`         | Logs queries that could not be served from the query cache.       |
| `tmp_table`       | Records queries that create temporary tables in memory.           |
| `tmp_table_on_disk`| Records queries that create temporary tables on disk.            |

Multiple values are separated by commas. For example: `full_scan,tmp_table_on_disk`

If no values are specified, the filter is disabled and all queries are logged.

### `log_slow_rate_type`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | yes         |
| Data type    | Enumerated  |
| Default      | session, query     |

Determines the context of `log_slow_rate_limit`.  

| Value   | Description                                                                                                                                           |
|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| session | The rate limit applies to the entire server session. The maximum number of slow queries allowed per second is counted across all queries executed within that session. |
| query   | The rate limit applies to each individual query. This means that each query can be logged as slow if it exceeds the specified limit, regardless of the overall session activity.       |

### `log_slow_rate_limit`

| Option       | Description     |
|--------------|-----------------|
| Command-line | Yes             |
| Config file  | Yes             |
| Scope        | Global, session |
| Dynamic      | yes             |
| Default      | 1               |
| Range        | 1-1000          |

The `log_slow_rate_limit` variable controls how often queries are logged in the slow query log. Instead of logging every query, it only logs one out of every `n` queries, where `n` is the value of `log_slow_rate_limit`. 

By default, `n` is 1, so all queries are logged. This setting helps reduce the amount of information in the slow query log, which is useful during debugging to avoid overwhelming the log file.

Please note: when log_slow_rate_type is `session` rate limiting is disabled for the replication thread.

Logging all queries might consume I/O bandwidth and cause the log file to grow large.

    
  * When log_slow_rate_type is `session`, this option lets you log full sessions, so you have complete records of sessions for later analysis; but you can rate-limit the number of sessions that are logged. Note that this feature will not work well if your application uses any type of connection pooling or persistent connections. Note that you change log_slow_rate_limit in `session` mode, you should reconnect for get effect.

  * When log_slow_rate_type is `query`, this option lets you log just some queries for later analysis. For example, if you set the value to 100, then one percent of queries will be logged.

Note that every query has global unique `query_id` and every connection can has it own (session) log_slow_rate_limit.
Decision “log or no” calculated in following manner:


* if `log_slow_rate_limit` = 1 - log every query

* If `log_slow_rate_limit` &gt; 1 - log every 1/`log_slow_rate_limit` query.

This allows flexible setup logging behavior.

For example, if you set the value to 100, then 1 query for every 100 queries of `sessions/queries` is logged. 

In Percona Server for MySQL information about the `log_slow_rate_limit` has been added to the slow query log. This means that if the `log_slow_rate_limit` is effective it will be reflected in the slow query log for each written query. 

??? example "Expected output"

    ```{.text .no-copy}
    Log_slow_rate_type: query  Log_slow_rate_limit: 10
    ```

### `log_slow_sp_statements`

| Option       | Description    |
|--------------|----------------|
| Command-line | Yes            |
| Config file  | Yes            |
| Scope        | Global         |
| Dynamic      | Yes            |
| Data type    | Enumerated     |
| Default      | session        |
| Range        | session, query |

If `TRUE`, statements executed by stored procedures are logged to the slow if it is open.

Percona Server for MySQL implemented improvements for logging of stored procedures to the slow query log:

* Each query from a stored procedure is now logged to the slow query log individually

* `CALL` itself isn’t logged to the slow query log anymore as this would be counting twice for the same query which would lead to incorrect results

* Queries that were called inside of stored procedures are annotated in the slow query log with the stored procedure name in which they run.

Example of the improved stored procedure slow query log entry:

```{.bash data-prompt="mysql"}
mysqlDELIMITER //
mysqlCREATE PROCEDURE improved_sp_log()
       BEGIN
        SELECT * FROM City;
        SELECT * FROM Country;
       END//
mysqlDELIMITER ;
mysqlCALL improved_sp_log();
```

When we check the slow query log after running the stored procedure, with `log_slow_sp_statements` set to `TRUE`, it should look like this:

??? example "Expected output"

    ```{.text .no-copy}
    # Time: 150109 11:38:55
    # User@Host: root[root] @ localhost []
    # Thread_id: 40  Schema: world  Last_errno: 0  Killed: 0
    # Query_time: 0.012989  Lock_time: 0.000033  Rows_sent: 4079  Rows_examined: 4079  Rows_affected: 0  Rows_read: 4079
    # Bytes_sent: 161085
    # Stored routine: world.improved_sp_log
    SET timestamp=1420803535;
    SELECT * FROM City;
    # User@Host: root[root] @ localhost []
    # Thread_id: 40  Schema: world  Last_errno: 0  Killed: 0
    # Query_time: 0.001413  Lock_time: 0.000017  Rows_sent: 4318  Rows_examined: 4318  Rows_affected: 0  Rows_read: 4318
    # Bytes_sent: 194601
    # Stored routine: world.improved_sp_log
    SET timestamp=1420803535;
    ```

If variable log_slow_sp_statements is set to `FALSE`:

* Entry is added to a slow-log for a `CALL` statement only and not for any of the individual statements run in that stored procedure

* Execution time is reported for the `CALL` statement as the total execution time of the `CALL` including all its statements

If we run the same stored procedure with the `log_slow_sp_statements` is set to `FALSE` slow query log should look like this:

??? example "Expected output"

    ```{.text .no-copy}
    # Time: 150109 11:51:42
    # User@Host: root[root] @ localhost []
    # Thread_id: 40  Schema: world  Last_errno: 0  Killed: 0
    # Query_time: 0.013947  Lock_time: 0.000000  Rows_sent: 4318  Rows_examined: 4318  Rows_affected: 0  Rows_read: 4318
    # Bytes_sent: 194612
    SET timestamp=1420804302;
    CALL improved_sp_log();
    ```

!!! note

    Support for logging stored procedures doesn’t involve triggers, so they won’t be logged even if this feature is enabled.

### `log_slow_verbosity`

| Option       | Description     |
|--------------|-----------------|
| Command-line | Yes             |
| Config file  | Yes             |
| Scope        | Global, session |
| Dynamic      | Yes             |

Specifies how much information to include in your slow log. The value is a comma-delimited string, and can contain any combination of the following values: 

* `microtime`: Log queries with microsecond precision.

* `query_plan`: Log information about the query’s execution plan.

* `innodb`: Log *InnoDB* statistics.

* `minimal`: Equivalent to enabling just `microtime`.

* `standard`: Equivalent to enabling `microtime,query_plan`.

* `full`: Equivalent to `microtime`,`query_plan`,`innodb`.

* `profiling`: Enables profiling of all queries in all connections.

* `profiling_use_getrusage`: Enables usage of the getrusage function.

* `query_info`: Enables printing `Query_tables` and `Query_digest` into the slow query log. These fields are disabled by default.


You can combine the options. For example, to enable microsecond query timing and InnoDB statistics, set this option to `microtime,innodb` or `standard`.

### `slow_query_log_use_global_control`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | Yes         |
| Default      | None        |

Specifies which variables have global scope instead of local. For such variables, the global variable value is used in the current session, but without copying this value to the session value. Value is a “flag” variable - you can specify multiple values separated by commas


* `none`: All variables use local scope


* `log_slow_filter`: Global variable log_slow_filter has effect (instead of local)


* `log_slow_rate_limit`: Global variable log_slow_rate_limit has effect (instead of local)


* `log_slow_verbosity`: Global variable log_slow_verbosity has effect (instead of local)


* `long_query_time`: Global variable long_query_time has effect (instead of local)


* `min_examined_row_limit`: Global variable `min_examined_row_limit` has effect (instead of local)


* `all` Global variables has effect (instead of local)

### `slow_query_log_always_write_time`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | Yes         |
| Default      | 10          |

This variable can be used to specify the query execution time after which the query will be written to the slow query log. It can be used to specify an additional execution time threshold for the slow query log, that, when exceeded, will cause a query to be logged unconditionally, that is, `log_slow_rate_limit` will not apply to it.



