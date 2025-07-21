# Binary logs and replication improvements

Due to continuous development, Percona Server for MySQL incorporated a number of
improvements related to replication and binary logs handling. This resulted in replication specifics, which distinguishes it from MySQL.

## Statements with a `LIMIT` clause

In MySQL 8.0, any UPDATE/DELETE/INSERT ... SELECT statements that include a LIMIT clause are indeed considered unsafe for statement-based replication. These statements will cause MySQL to automatically switch from statement-based logging to row-based logging if binlog_format is set to MIXED.

Here's why:

* The LIMIT clause without an ORDER BY makes the result set non-deterministic

* The same statement might affect different rows on the primary and replicas

```{.bash data-prompt="mysql>"}
mysql> UPDATE table1 LIMIT 10 SET col1 = 'value';
mysql> DELETE FROM table1 LIMIT 5;
mysql> INSERT INTO table2 SELECT * FROM table1 LIMIT 3;
```

To make these statements safe for statement-based replication, you should do one of the following:

* Remove the LIMIT clause

* Add an ORDER BY clause to make the result set deterministic

```{.bash data-prompt="mysql>"}
mysql> UPDATE table1 SET col1 = 'value' ORDER BY id LIMIT 10;
mysql> DELETE FROM table1 ORDER BY id LIMIT 5;
mysql> INSERT INTO table2 SELECT * FROM table1 ORDER BY id LIMIT 3;
```

The exception is when the LIMIT is used with an ORDER BY clause that uses a unique key - in this case, the statement becomes deterministic and safe for statement-based replication.

Percona Server for MySQL acknowledges statements as safe when they include either an `ORDER BY PK` or `WHERE` 
condition. 


## Relay log position fix

*MySQL* always updated relay log position in multi-source replications setups
regardless of whether the committed transaction has already been executed or
not. Percona Server omits relay log position updates for the already logged
GTIDs.

## Relay log position details

Particularly, such unconditional relay log position updates caused additional
fsync operations in case of `relay-log-info-repository=TABLE`, and with the
higher number of channels transmitting such duplicate (already executed)
transactions the situation became proportionally worse. Bug fixed [#1786](https://jira.percona.com/browse/PS-1786), (upstream [#85141](https://bugs.mysql.com/bug.php?id=85141)).

## Source and connection status update fix

Replica nodes configured to update source status and connection information
only on log file rotation did not experience the expected reduction in load.
*MySQL* was additionally updating this information in case of multi-source
replication when replica had to skip the already executed GTID event.

## Write `FLUSH` commands to the binary log

`FLUSH` commands, such as `FLUSH SLOW LOGS`, are not written to the
binary log if the system variable [`binlog_skip_flush_commands`](#binlog_skip_flush_commands) is set
to `ON`.

In the context of MySQL, the `read_only` and `super_read_only` system variables control the ability to modify data in the database. The following changes were implemented in the behavior of `read_only` and `super_read_only` modes:

* When `read_only` is set to `ON`, any `FLUSH ...` command executed by a
normal user (without the `SUPER` privilege) are not written to the binary
log regardless of the value of the binlog_skip_flush_command variable.

* When `super_read_only` is set to `ON`, any `FLUSH ...` command executed by
any user (even by those with the `SUPER` privilege) are not written to the
binary log regardless of the value of the binlog_skip_flush_commands variable.

An attempt to run a `FLUSH` command without either [`SUPER`](https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_super) or [`RELOAD`](https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html#priv_reload)
privileges results in the `ER_SPECIFIC_ACCESS_DENIED_ERROR` exception
regardless of the value of the `binlog_skip_flush_commands` variable.

### binlog_skip_flush_commands

| Option | Description |
| --- | --- |
| Command-line | Yes |
| Config file | Yes |
| Scope | Global |
| Dynamic | Yes |
| Default | OFF |

When `binlog_skip_flush_commands` is set to ON, `FLUSH ...` commands are not written to the binary
log. 

The `binlog_skip_flush_commands` setting does not impact the following commands because they are never recorded in the binary log:

*	`FLUSH LOGS`
	
* `FLUSH BINARY LOGS`
	
* `FLUSH TABLES WITH READ LOCK`
	
* `FLUSH TABLES ... FOR EXPORT`


The `FLUSH` command is not recorded in the binary log and ignores the `binlog_skip_flush_commands` setting when executed with the `NO_WRITE_TO_BINLOG` keyword (or its alias `LOCAL`).

## Keep comments with DDL commands

When you run a DDL command, such as `DROP TABLE`, the server does the following in the binary log. 

| Actions  | Description   |
|---|---|
| Removes Comments   | The server deletes any comments in the original command. For example, if you use `DROP TABLE my_table /* This is a comment */;`, the binary log does not save the comment. |
| Adds Quotation Marks | The server puts quotation marks around the table name. So, if you run `DROP TABLE my_table;`, it logs it as `DROP TABLE "my_table";`.                               |

These actions simplify the logging format, but sometimes, you want the original format.

### binlog_ddl_skip_rewrite

| Option | Description |
| --- | --- |
| Command-line | Yes |
| Config file | Yes |
| Scope | Global |
| Dynamic | Yes |
| Default | OFF |

When disabled (default setting), the server removes comments and adds quotation marks to DDL statements.

When enabled, all single-table `DROP TABLE` DDL statements are logged in the binary log with the following characteristics:

* Comments are preserved, allowing any notes added to the command to remain in the binary log.

* Quotation marks are not added.

### Enable `binlog_ddl_skip_rewrite`

You can enable `binlog_ddl_skip_rewrite` at runtime:

```{.bash data-prompt="mysql>"}
-- Check current setting
mysql> SHOW VARIABLES LIKE 'binlog_ddl_skip_rewrite';

-- Enable feature
mysql> SET GLOBAL binlog_ddl_skip_rewrite = ON;

-- Disable feature
mysql> SET GLOBAL binlog_ddl_skip_rewrite = OFF;
```

to enable the variable permanently, add the following line to the `my.cnf` configuration file:

```ini
[mysqld]
binlog_ddl_skip_rewrite = ON
```

After making this change, restart the MySQL service for it to take effect.

!!! note

    Multi-table `DROP TABLE` DDL statements are not supported and return an error.

### Example usage

The following code block demonstrates how to enable `binlog_ddl_skip_rewrite` and shows the feature's effect on a `DROP TABLE` statement:

```{.bash data-prompt="mysql>"}
mysql> SET binlog_ddl_skip_rewrite = ON;
/*comment at start*/DROP TABLE t /*comment at end*/;
```

## Point-in-Time Recovery with `binlog_utils_udf`

Use the binlog_utils_udf component to assist with Point-in-Time Recovery (PiTR).
The component installs user-defined functions (UDFs) that help you map GTIDs to
binary log files and inspect the contents and timestamps of binlog files.

### Functions

| Function                                | Returns              | Description                                                             |
|-----------------------------------------|----------------------|-------------------------------------------------------------------------|
| get_binlog_by_gtid(gtid)                | STRING (binlog name) | Returns the binlog file that contains the specified GTID.               |
| get_last_gtid_from_binlog(binlog)       | STRING (GTID)        | Returns the last GTID found in the specified binlog.                    |
| get_gtid_set_by_binlog(binlog)          | STRING (GTID set)    | Returns all GTIDs found in the specified binlog.                        |
| get_binlog_by_gtid_set(gtid_set)        | STRING (binlog name) | Returns the first binlog file that contains at least one GTID from the specified set. |
| get_first_record_timestamp_by_binlog(binlog) | INTEGER (timestamp) | Returns the timestamp of the first event in the specified binlog.       |
| get_last_record_timestamp_by_binlog(binlog)  | INTEGER (timestamp) | Returns the timestamp of the last event in the specified binlog.        |

### Notes

* Timestamp-returning functions provide values with microsecond precision in
UNIX time. Each value represents the number of microseconds since
1970-01-01 00:00:00 UTC.

* Functions that accept a binlog name require a short file name only. Do not
include a path. If the input contains a path separator (/), the server
returns an error.

* The server reads binlogs from the current binlog directory defined by the
@@log_bin_basename system variable.

* Functions that return a binlog file name return the short name (no path).

### Install the component

Install the component once on each server where you want to use these UDFs.

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://component_binlog_utils_udf';
```

You can confirm installation by checking the list of registered functions:

```{.bash data-prompt="mysql>"}
mysql> SELECT ROUTINE_NAME FROM INFORMATION_SCHEMA.ROUTINES \G
```


### Usage examples

Replace the sample arguments with values from your environment. The examples
show the typical way to call each function. For clarity, results are aliased.

#### get_binlog_by_gtid()

Locate the binlog that contains a GTID:

```{.bash data-prompt="mysql>"}
mysql> SELECT get_binlog_by_gtid('UUID-GROUP:1') AS binlog;
```

#### get_last_gtid_from_binlog()

Return the last GTID in a binlog

```{.bash data-prompt="mysql>"}
mysql> SELECT get_last_gtid_from_binlog('binlog.000001') AS last_gtid;
```

#### get_gtid_set_by_binlog()

Return all GTIDs in a binlog

```{.bash data-prompt="mysql>"}
mysql> SELECT get_gtid_set_by_binlog('binlog.000001') AS gtid_set;
```

#### get_binlog_by_gtid_set()

Find a binlog that contains any GTID in a set

```{.bash data-prompt="mysql>"}
mysql> SELECT get_binlog_by_gtid_set('UUID1:7,UUID1:8') AS binlog;
```

#### get_first_record_timestamp_by_binlog() and get_last_record_timestamp_by_binlog(binlog)

Get the first event timestamp from a binlog. The function returns microseconds since the UNIX epoch. Use the tabs below to
see the raw numeric value or a human-readable timestamp.

=== "Raw Timestamp"
    ```{.bash data-prompt="mysql>"}
    mysql> SELECT get_first_record_timestamp_by_binlog('binlog.000001') AS raw_ts;
    ```

=== "Human-Readable"
    ```{.bash data-prompt="mysql>"}
    mysql> SELECT FROM_UNIXTIME(
        get_first_record_timestamp_by_binlog('binlog.000001') DIV 1000000
    ) AS first_event_ts;
    ```

Get the last event timestamp from a binlog

=== "Raw Timestamp"
    ```{.bash data-prompt="mysql>"}
    mysql> SELECT get_last_record_timestamp_by_binlog('binlog.000001') AS raw_ts;
    ```

=== "Human-Readable"
    ```{.bash data-prompt="mysql>"}
    mysql> SELECT FROM_UNIXTIME(
        get_last_record_timestamp_by_binlog('binlog.000001') DIV 1000000
    ) AS last_event_ts;
    ```


    ??? example "Expected output"

        ```{.text .no-copy}
        +---------------+
        | binlog        |
        +---------------+
        | binlog.000001 |
        +---------------+
        ```

Actual values depend on your server state and binlog contents.

### Uninstall the component

Remove the component and all associated UDFs:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_binlog_utils_udf';
```
	
## Limitations

For the following variables, do not define values with one or more dot (.) characters:

* [log_bin]

* [log_bin_index]

A value defined with the dot (.) character is handled differently in MySQL and Percona XtraBackup and can cause unpredictable behavior.

[@@log_bin_basename system variable]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#sysvar_log_bin_basename

[log_bin]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin

[log_bin_index]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin-index