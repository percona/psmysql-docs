# Binary logs and replication improvements

Due to continuous development, Percona Server for MySQL incorporated a number of
improvements related to replication and binary logs handling. This resulted in replication specifics, which distinguishes it from MySQL.

## Statements with a `LIMIT` clause

In MySQL 8.0, any UPDATE/DELETE/INSERT ... SELECT statements that include a LIMIT clause are indeed considered unsafe for statement-based replication. These statements will cause MySQL to automatically switch from statement-based logging to row-based logging if binlog_format is set to MIXED.

Here's why:

* The LIMIT clause without an ORDER BY makes the result set non-deterministic

* The same statement might affect different rows on the primary and replicas

```{.bash}
UPDATE table1 LIMIT 10 SET col1 = 'value';
DELETE FROM table1 LIMIT 5;
INSERT INTO table2 SELECT * FROM table1 LIMIT 3;
```

To make these statements safe for statement-based replication, you should do one of the following:

* Remove the LIMIT clause

* Add an ORDER BY clause to make the result set deterministic

```{.bash}
UPDATE table1 SET col1 = 'value' ORDER BY id LIMIT 10;
DELETE FROM table1 ORDER BY id LIMIT 5;
INSERT INTO table2 SELECT * FROM table1 ORDER BY id LIMIT 3;
```

The exception is when the LIMIT is used with an ORDER BY clause that uses a unique key - in this case, the statement becomes deterministic and safe for statement-based replication.

Percona Server for MySQL acknowledges statements as safe when they include either an `ORDER BY PK` or `WHERE` 
condition. 


## Relay log position fix

*MySQL* always updated relay log position in multi-source replications setups
regardless of whether the committed transaction has already been executed or
not. Percona Server omits relay log position updates for the already logged
GTIDs.

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

```{.bash}
-- Check current setting
SHOW VARIABLES LIKE 'binlog_ddl_skip_rewrite';

-- Enable feature
SET GLOBAL binlog_ddl_skip_rewrite = ON;

-- Disable feature
SET GLOBAL binlog_ddl_skip_rewrite = OFF;
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

```{.bash}
SET binlog_ddl_skip_rewrite = ON;
/*comment at start*/DROP TABLE t /*comment at end*/;
```

## Point-in-Time Recovery with `binlog_utils_udf`

Point-in-Time Recovery (PiTR) allows you to restore a database to any specific moment in time using binary logs. The `binlog_utils_udf` component provides user-defined functions (UDFs) that simplify PiTR operations by helping you:

* Map Global Transaction Identifiers (GTIDs) to specific binary log files
* Inspect binary log contents and timestamps
* Locate the exact binary log files needed for recovery operations

These functions are particularly useful when you need to determine which binary log files contain specific transactions or events during recovery planning.

### Prerequisites

Before using the `binlog_utils_udf` component, ensure the following requirements are met:

* Percona Server for MySQL: The component is only available in Percona Server for MySQL, not in standard MySQL

* Binary logging enabled: The server must have binary logging enabled (`log_bin` system variable set to `ON`)

* GTID enabled: For GTID-related functions, GTID must be enabled (`gtid_mode` set to `ON`)

* MySQL privileges: You need `SYSTEM_VARIABLES_ADMIN` privilege to install components. For binary log operations, `BINLOG_ADMIN` privilege may also be required. The `SUPER` privilege is deprecated in MySQL 8.0+ and should be replaced with specific dynamic privileges

#### Install the component

Install the component on each server where you plan to use these functions:

```{.bash}
INSTALL COMPONENT 'file://component_binlog_utils_udf';
```

#### Verify installation

```{.bash}
SELECT * FROM mysql.component WHERE component_urn = 'file://component_binlog_utils_udf';
```

```{.bash}
SELECT ROUTINE_NAME FROM INFORMATION_SCHEMA.ROUTINES 
    -> WHERE ROUTINE_NAME LIKE 'get_%' AND ROUTINE_TYPE = 'FUNCTION';
```

### Available functions

The `binlog_utils_udf` component provides six functions for binary log analysis and GTID mapping:

| Function                                | Returns              | Description                                                             | Use Case |
|-----------------------------------------|----------------------|-------------------------------------------------------------------------|----------|
| [`get_binlog_by_gtid(gtid)`](#find-binary-log-by-gtid)              | STRING (binlog name) | Returns the binary log file that contains the specified GTID.           | Find which binary log contains a specific transaction |
| [`get_last_gtid_from_binlog(binlog)`](#get-last-gtid-from-binary-log)     | STRING (GTID)        | Returns the last GTID found in the specified binary log.               | Identify the final transaction in a binary log file |
| [`get_gtid_set_by_binlog(binlog)`](#get-all-gtids-from-binary-log)        | STRING (GTID set)    | Returns all GTIDs found in the specified binary log.                   | Get complete list of transactions in a binary log |
| [`get_binlog_by_gtid_set(gtid_set)`](#find-binary-log-by-gtid-set)      | STRING (binlog name) | Returns the first binary log file that contains at least one GTID from the specified set. | Find binary log containing any transaction from a GTID set |
| [`get_first_record_timestamp_by_binlog(binlog)`](#get-first-event-timestamp) | INTEGER (timestamp) | Returns the timestamp of the first event in the specified binary log.  | Determine when a binary log file started |
| [`get_last_record_timestamp_by_binlog(binlog)`](#get-last-event-timestamp)  | INTEGER (timestamp) | Returns the timestamp of the last event in the specified binary log.   | Determine when a binary log file ended |

### Important notes

* CAST requirement: When using these user-defined functions, you must use CAST to return a result. String functions require `CAST(...AS CHAR)` and timestamp functions require `CAST(...AS UNSIGNED)`.

* Timestamp precision: Timestamp-returning functions provide values with microsecond precision in UNIX time format. Each value represents the number of microseconds since 1970-01-01 00:00:00 UTC.

* Binary log file names: Functions that accept a binary log name require only the short file name (for example, `binlog.000001`). Do not include the full path. If the input contains a path separator (`/`), the server returns an error.

* Binary log directory: The server reads binary logs from the directory defined by the `@@log_bin_basename` system variable.

* Return values: Functions that return binary log file names return only the short name without the path.

* Performance considerations: These functions read binary log files directly from disk. For large binary log files, the functions may take several seconds to complete.

### Simplifying UDF usage without CAST()

While CAST() is required for proper function execution, you can configure your MySQL client to handle data type conversions automatically, reducing the need to use CAST() explicitly in your queries.

#### Configure the MySQL client

You can set the appropriate client character set and collation to simplify UDF usage:

```{.bash}
-- Set client character set
SET character_set_client = 'utf8mb4';

-- Set client collation
SET collation_connection = 'utf8mb4_general_ci';
```

Alternatively, you can configure these settings in your MySQL client configuration file (e.g., `~/.my.cnf` or `/etc/mysql/my.cnf`):

```ini
[client]
default-character-set=utf8mb4
default-collation=utf8mb4_general_ci
```

By configuring these settings, the MySQL client can handle data type conversions more effectively, allowing you to use the UDF functions without explicit CAST() statements in many cases.

!!! note

    While client configuration can simplify usage, CAST() will still work and may be necessary in some scenarios. The choice between using CAST() explicitly or relying on client configuration depends on your specific use case and preferences.



### Usage examples

The following examples demonstrate how to use each function. Replace the sample arguments with values from your environment. All examples include CAST statements for proper function execution, though these may be optional if you've configured your MySQL client as described in the [Simplifying UDF usage without CAST()](#simplifying-udf-usage-without-cast) section.

#### Find binary log by GTID

Use `get_binlog_by_gtid()` to locate which binary log file contains a specific transaction:

```{.bash}
SELECT CAST(get_binlog_by_gtid('550e8400-e29b-41d4-a716-446655440000:123') AS CHAR) AS binlog;
```

Use case: When you know a specific GTID and need to find which binary log file contains that transaction for recovery purposes.

#### Get last GTID from binary log

Use `get_last_gtid_from_binlog()` to find the final transaction in a specific binary log file:

```{.bash}
SELECT CAST(get_last_gtid_from_binlog('binlog.000001') AS CHAR) AS last_gtid;
```

Use case: Determine the last transaction processed in a binary log file before rotating to the next file.

#### Get all GTIDs from binary log

Use `get_gtid_set_by_binlog()` to retrieve all GTIDs contained in a specific binary log file:

```{.bash}
SELECT CAST(get_gtid_set_by_binlog('binlog.000001') AS CHAR) AS gtid_set;
```

Use case: Get a complete list of all transactions in a binary log file for analysis or replication setup.

#### Find binary log by GTID set

Use `get_binlog_by_gtid_set()` to find the first binary log file that contains any GTID from a specified set:

```{.bash}
SELECT CAST(get_binlog_by_gtid_set('550e8400-e29b-41d4-a716-446655440000:7,550e8400-e29b-41d4-a716-446655440000:8') AS CHAR) AS binlog;
```

Use case: When you have a set of GTIDs and need to find which binary log file contains at least one of those transactions.

#### Get binary log timestamps

Use timestamp functions to determine when events occurred in binary log files. These functions return microsecond-precision timestamps in UNIX time format.

##### Get first event timestamp

Find when the first event was written to a binary log file:

=== "Raw Timestamp (Microseconds)"
    ```{.bash}
    SELECT CAST(get_first_record_timestamp_by_binlog('binlog.000001') AS UNSIGNED) AS raw_ts;
    ```

=== "Human-Readable Format"
    ```{.bash}
    SELECT FROM_UNIXTIME(
        CAST(get_first_record_timestamp_by_binlog('binlog.000001') AS UNSIGNED) DIV 1000000
    ) AS first_event_ts;
    ```

Use case: Determine when a binary log file started receiving events, useful for recovery planning.

##### Get last event timestamp

Find when the last event was written to a binary log file:

=== "Raw Timestamp (Microseconds)"
    ```{.bash}
    SELECT CAST(get_last_record_timestamp_by_binlog('binlog.000001') AS UNSIGNED) AS raw_ts;
    ```

=== "Human-Readable Format"
    ```{.bash}
    SELECT FROM_UNIXTIME(
        CAST(get_last_record_timestamp_by_binlog('binlog.000001') AS UNSIGNED) DIV 1000000
    ) AS last_event_ts;
    ```

Use case: Determine when a binary log file stopped receiving events, useful for understanding binary log rotation timing.


### Troubleshooting

#### Common issues

Function returns NULL: This usually indicates that the specified GTID or binary log file does not exist. Verify that:

* The GTID format is correct (UUID:transaction_id)

* The binary log file exists in the binary log directory

* GTID is enabled on the server

Error: "Unknown function": The component is not installed. Install the component using the `INSTALL COMPONENT` command.

Error: "Access denied": You need `SYSTEM_VARIABLES_ADMIN` privilege to install the component and `BINLOG_ADMIN` privilege for binary log operations. The `SUPER` privilege is deprecated in MySQL 8.0+.

Performance issues: These functions read binary log files directly from disk. For large binary log files, expect execution times of several seconds.

#### Verify binary log files

Check which binary log files are available:

```{.bash}
SHOW BINARY LOGS;
```

#### Check GTID status

Verify GTID is enabled:

```{.bash}
SHOW VARIABLES LIKE 'gtid_mode';
```

### Uninstall the component

Remove the component and all associated functions:

```{.bash}
UNINSTALL COMPONENT 'file://component_binlog_utils_udf';
```

Verify removal:

```{.bash}
SELECT * FROM mysql.component WHERE component_urn = 'file://component_binlog_utils_udf';
```

The query should return no rows if the component is successfully uninstalled.
	
## Limitations

For the following variables, do not define values with one or more dot (.) characters:

* [log_bin]

* [log_bin_index]

A value defined with the dot (.) character is handled differently in MySQL and Percona XtraBackup and can cause unpredictable behavior.

[@@log_bin_basename system variable]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#sysvar_log_bin_basename

[log_bin]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin

[log_bin_index]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin-index