# Binary logs and replication improvements

Due to continuous development, *Percona Server for MySQL* incorporated a number of
improvements related to replication and binary logs handling. This resulted in replication specifics, which distinguishes it from *MySQL*.

## Safety of statements with a `LIMIT` clause

### Summary of the fix

*MySQL* considers all `UPDATE/DELETE/INSERT ... SELECT` statements with
`LIMIT` clause to be unsafe, no matter wether they are really producing
non-deterministic result or not, and switches from statement-based logging
to row-based one. *Percona Server for MySQL* is more accurate, it acknowledges such
instructions as safe when they include `ORDER BY PK` or `WHERE`
condition. This fix has been ported from the upstream bug report
[#42415 :octicons-link-external-16:](https://bugs.mysql.com/bug.php?id=42415) ([#44 :octicons-link-external-16:](https://jira.percona.com/browse/PS-44)).

## Performance improvement on relay log position update

### Relay log position fix

*MySQL* always updated relay log position in multi-source replications setups
regardless of whether the committed transaction has already been executed or
not. Percona Server omits relay log position updates for the already logged
GTIDs.

### Relay log position details

Particularly, such unconditional relay log position updates caused additional
fsync operations in case of `relay-log-info-repository=TABLE`, and with the
higher number of channels transmitting such duplicate (already executed)
transactions the situation became proportionally worse. Bug fixed [#1786 :octicons-link-external-16:](https://jira.percona.com/browse/PS-1786)
(upstream [#85141 :octicons-link-external-16:](https://bugs.mysql.com/bug.php?id=85141)).

## Performance improvement on source and connection status updates

### Source and connection status update fix

Replica nodes configured to update source status and connection information
only on log file rotation did not experience the expected reduction in load.
*MySQL* was additionally updating this information in case of multi-source
replication when replica had to skip the already executed GTID event.

### Source and connection status details

The configuration with `master_info_repository=TABLE` and
`sync_master_info=0` makes replica to update source status and connection
information in this table on log file rotation and not after each
sync_master_info event, but it didn’t work on multi-source replication setups.
Heartbeats sent to the replica to skip GTID events which it had already executed
previously, were evaluated as relay log rotation events and reacted with
`mysql.slave_master_info` table sync. This inaccuracy could produce huge (up
to 5 times on some setups) increase in write load on the replica, before this
problem was fixed in *Percona Server for MySQL*. Bug fixed [#1812 :octicons-link-external-16:](https://jira.percona.com/browse/PS-1812) (upstream
[#85158 :octicons-link-external-16:](https://bugs.mysql.com/bug.php?id=85158)).

## Write `FLUSH` commands to the binary log

`FLUSH` commands, such as `FLUSH SLOW LOGS`, are not written to the
binary log if the system variable binlog_skip_flush_commands is set
to ON.

In addition, the following changes were implemented in the behavior of
`read_only` and super_read_only modes:

* When `read_only` is set to ON, any `FLUSH ...` command executed by a
normal user (without the `SUPER` privilege) are not written to the binary
log regardless of the value of the binlog_skip_flush_command variable.

* When super_read_only is set to ON, any `FLUSH ...` command executed by
any user (even by those with the `SUPER` privilege) are not written to the
binary log regardless of the value of the binlog_skip_flush_commands variable.

An attempt to run a `FLUSH` command without either `SUPER` or `RELOAD`
privileges results in the `ER_SPECIFIC_ACCESS_DENIED_ERROR` exception
regardless of the value of the binlog_skip_flush_commands variable.

### binlog_skip_flush_commands

| Option | Description |
| --- | --- |
| Command-line | Yes |
| Config file | Yes |
| Scope | Global |
| Dynamic | Yes |
| Default | OFF |

This variable was introduced in Percona Server for MySQL 8.0.15-5.

When binlog_skip_flush_commands is set to ON, `FLUSH ...` commands are not written to the binary
log. See Writing FLUSH Commands to the Binary Log for more information
about what else affects the writing of `FLUSH` commands to the binary log.

!!! note

    `FLUSH LOGS`, `FLUSH BINARY LOGS`, `FLUSH TABLES WITH READ LOCK`, and `FLUSH TABLES ... FOR EXPORT` are not written to the binary log no matter what value the binlog_skip_flush_commands variable contains. The `FLUSH` command is not recorded to the binary log and the value of binlog_skip_flush_commands is ignored if the `FLUSH` command is run with the `NO_WRITE_TO_BINLOG` keyword (or its alias `LOCAL`).

## Maintaining comments with DROP TABLE

When you issue a `DROP TABLE` command, the binary log stores the command but removes comments and encloses the table name in quotation marks. If you require the binary log to maintain the comments and not add quotation marks, enable `binlog_ddl_skip_rewrite`.

### binlog_ddl_skip_rewrite

| Option | Description |
| --- | --- |
| Command-line | Yes |
| Config file | Yes |
| Scope | Global |
| Dynamic | Yes |
| Default | OFF |

This variable was introduced in Percona Server for MySQL 8.0.26-16.

If the variable is enabled, single table `DROP TABLE` DDL statements are logged in the binary log with comments. Multi-table `DROP TABLE` DDL statements are not supported and return an error.

```sql
SET binlog_ddl_skip_rewrite = ON;
/*comment at start*/DROP TABLE t /*comment at end*/;
```

## Binary log user-defined functions

To implement Point in Time recovery, we have added the `binlog_utils_udf` plugin. These functions help you locate specific transactions in binary logs and determine which binary log files contain particular GTIDs, which is essential for precise point-in-time recovery operations.

### Prerequisites

Before using these functions, ensure that:

* Binary logging is enabled on your MySQL server

* You have the `SYSTEM_VARIABLES_ADMIN` and `SERVICE_CONNECTION_ADMIN` privileges to install plugins

  * `SYSTEM_VARIABLES_ADMIN`: Allows modification of system variables at runtime
  
  * `SERVICE_CONNECTION_ADMIN`: Allows management of service connections and administrative operations

* You have read access to the binary log directory

* GTID-based replication is configured (for GTID-related functions)

### Installation

Before using the user-defined functions, you must install the plugin:

```sql
INSTALL PLUGIN binlog_utils_udf SONAME 'binlog_utils_udf.so';
```

After installation, you can verify the plugin is loaded by checking the `INFORMATION_SCHEMA.PLUGINS` table:

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME = 'binlog_utils_udf';
```

To verify that the UDFs are available, you can check the `mysql.func` table or `performance_schema.user_defined_functions`:

```sql
SELECT * FROM mysql.func WHERE name LIKE 'get_%';
SELECT * FROM performance_schema.user_defined_functions WHERE name LIKE 'get_%';
```

### Understanding GTIDs

A Global Transaction Identifier (GTID) is a unique identifier for each transaction in a MySQL replication setup. GTIDs help ensure data consistency and enable precise point-in-time recovery. GTIDs follow the format `source_id:transaction_id`, where `source_id` is the server's UUID and `transaction_id` is a sequence number.

When using these user-defined functions, you must use CAST to return a result. For example:

```sql
SELECT CAST(get_last_gtid_from_binlog("binlog.0001") AS CHAR) as result;
```

### Available functions

The following user-defined functions are included:

| Function | Returns | Description | Use Case |
| --- | --- | --- | --- |
| [get_binlog_by_gtid(gtid)](#get_binlog_by_gtid) | STRING (binlog name) | Returns the binary log file that contains the specified GTID | Find which binary log contains a specific transaction |
| [get_last_gtid_from_binlog(binlog)](#get_last_gtid_from_binlog) | STRING (GTID) | Returns the last GTID found in the specified binary log | Identify the final transaction in a binary log file |
| [get_gtid_set_by_binlog(binlog)](#get_gtid_set_by_binlog) | STRING (GTID set) | Returns all GTIDs found in the specified binary log | Get complete list of transactions in a binary log |
| [get_binlog_by_gtid_set(gtid_set)](#get_binlog_by_gtid_set) | STRING (binlog name) | Returns the first binary log file that contains at least one GTID from the specified set | Find binary log containing any transaction from a GTID set |
| [get_first_record_timestamp_by_binlog(binlog)](#get_first_record_timestamp_by_binlog) | INTEGER (timestamp) | Returns the timestamp of the first event in the specified binary log | Determine when a binary log file started |
| [get_last_record_timestamp_by_binlog(binlog)](#get_last_record_timestamp_by_binlog) | INTEGER (timestamp) | Returns the timestamp of the last event in the specified binary log | Determine when a binary log file ended |

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

```sql
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

By configuring these settings, the MySQL client can handle data type conversions more effectively, allowing you to use the UDF functions without explicit CAST() statements in many cases. While client configuration can simplify usage, CAST() will still work and may be necessary in some scenarios. The choice between using CAST() explicitly or relying on client configuration depends on your specific use case and preferences.

All functions returning timestamps return their values as microsecond precision UNIX time. In other words, they represent the number of microseconds since 1-JAN-1970.

All functions accepting a binlog name as a parameter accept only short names, without a path component. If the path separator ('/') is found in the input, an error is returned. This restriction serves the purpose of limiting the locations from which binlogs can be read. They are always read from the current binlog directory ([@@log_bin_basename system variable :octicons-link-external-16:](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_log_bin_basename)).

All functions returning binlog file names return the name in short form, without a path component.

#### get_binlog_by_gtid

Syntax:

```
get_binlog_by_gtid(gtid_string)
```

Parameters:

- `gtid_string`: The GTID to search for (format: `source_id:transaction_id`)

Returns: Binary log file name as STRING

Example:

```sql
CREATE FUNCTION get_binlog_by_gtid RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT CAST(get_binlog_by_gtid("F6F54186-8495-47B3-8D9F-011DDB1B65B3:1") AS CHAR) AS result;
```
??? example "Expected output"

    ```{.text .no-copy}
    +--------------+
    | result       |
    +==============+
    | binlog.00001 |
    +--------------+
    ```

```sql
DROP FUNCTION get_binlog_by_gtid;
```

#### get_last_gtid_from_binlog

Syntax:

```
get_last_gtid_from_binlog(binlog_name)
```

Parameters:

- `binlog_name`: The binary log file name (without path)

Returns: GTID as STRING

Example:

```sql
CREATE FUNCTION get_last_gtid_from_binlog RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT CAST(get_last_gtid_from_binlog("binlog.00001") AS CHAR) AS result;
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------------+
    | result                                  |
    +=========================================+
    | F6F54186-8495-47B3-8D9F-011DDB1B65B3:10 |
    +-----------------------------------------+
    ```

```sql
DROP FUNCTION get_last_gtid_from_binlog;
```

#### get_gtid_set_by_binlog

Syntax:

```
get_gtid_set_by_binlog(binlog_name)
```

Parameters:

- `binlog_name`: The binary log file name (without path)

Returns: GTID set as STRING

Example:

```sql
CREATE FUNCTION get_gtid_set_by_binlog RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT CAST(get_gtid_set_by_binlog("binlog.00001") AS CHAR) AS result;
```
??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------+
    | result                  |
    +=========================+
    | 11ea-b9a7:7,11ea-b9a7:8 |
    +-------------------------+
    ```

```sql
DROP FUNCTION get_gtid_set_by_binlog;
```

#### get_binlog_by_gtid_set

Syntax:

```
get_binlog_by_gtid_set(gtid_set)
```

Parameters:

- `gtid_set`: Comma-separated list of GTIDs to search for

Returns: Binary log file name as STRING

Example:

```sql
CREATE FUNCTION get_binlog_by_gtid_set RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT CAST(get_binlog_by_gtid_set("11ea-b9a7:7,11ea-b9a7:8") AS CHAR) AS result;
```
??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------------------------------------------+
    | result                                                        |
    +===============================================================+
    | bin.000003                                                    |
    +---------------------------------------------------------------+
    ```

```sql
DROP FUNCTION get_binlog_by_gtid_set;
```

#### get_first_record_timestamp_by_binlog

Syntax:

```
get_first_record_timestamp_by_binlog(binlog_name)
```

Parameters:

- `binlog_name`: The binary log file name (without path)

Returns: Timestamp as INTEGER (microseconds since Unix epoch)

Example:

```sql
CREATE FUNCTION get_first_record_timestamp_by_binlog RETURNS INTEGER SONAME 'binlog_utils_udf.so';
SELECT FROM_UNIXTIME(CAST(get_first_record_timestamp_by_binlog("bin.00003") AS UNSIGNED) DIV 1000000) AS result;
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+
    | result              |
    +=====================+
    | 2024-12-03 09:10:40 |
    +---------------------+
    ```

```sql
DROP FUNCTION get_first_record_timestamp_by_binlog;
```

#### get_last_record_timestamp_by_binlog

Syntax:

```
get_last_record_timestamp_by_binlog(binlog_name)
```

Parameters:

- `binlog_name`: The binary log file name (without path)

Returns: Timestamp as INTEGER (microseconds since Unix epoch)

Example:

```sql
CREATE FUNCTION get_last_record_timestamp_by_binlog RETURNS INTEGER SONAME 'binlog_utils_udf.so';
SELECT FROM_UNIXTIME(CAST(get_last_record_timestamp_by_binlog("bin.00003") AS UNSIGNED) DIV 1000000) AS result;
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+
    | result              |
    +=====================+
    | 2024-12-04 04:18:56 |
    +---------------------+
    ```

```sql
DROP FUNCTION get_last_record_timestamp_by_binlog;
```

### Troubleshooting

#### Common issues

Function returns NULL: This usually indicates that the specified GTID or binary log file does not exist. Verify that:

* The GTID format is correct (UUID:transaction_id)
* The binary log file exists in the binary log directory
* GTID is enabled on the server

Error: "Unknown function": The plugin is not installed. Install the plugin using the `INSTALL PLUGIN` command.

Error: "Access denied": You need `SYSTEM_VARIABLES_ADMIN` and `SERVICE_CONNECTION_ADMIN` privileges to install the plugin and use the functions.

Performance issues: These functions read binary log files directly from disk. For large binary log files, expect execution times of several seconds.

#### Verify binary log files

Check which binary log files are available:

```sql
SHOW BINARY LOGS;
```

#### Check GTID status

Verify GTID is enabled:

```sql
SHOW VARIABLES LIKE 'gtid_mode';
```

Function returns NULL or error:

* Ensure the binary log file exists in the current binlog directory

* Verify you have read permissions on the binary log files

* Check that the binary log file name is correct and does not include a path

Plugin installation fails:

* Verify you have the `SYSTEM_VARIABLES_ADMIN` and `SERVICE_CONNECTION_ADMIN` privileges:

* Ensure the `binlog_utils_udf.so` file exists in the plugin directory

* Check that the plugin is compatible with your MySQL version

GTID format errors:

* Ensure GTIDs follow the correct format: `source_id:transaction_id`

* Verify that GTID-based replication is enabled on your server

Timestamp conversion issues:

* Remember that timestamps are returned in microseconds since Unix epoch

* Use `FROM_UNIXTIME()` with division by 1000000 to convert to readable format

Character set and display issues:

* This behavior is expected. UDFs developed before MySQL's UDF API character set enhancements did not specify character sets for STRING return values, which defaulted to "binary"

* The `--binary-as-hex` command line option is `TRUE` by default in interactive mode

* If you see unexpected hexadecimal output from UDF functions, start the mysql client with `--binary-as-hex=FALSE` or add this parameter to the `[client]` section of your MySQL config file (no server restart required). The change takes effect on the next client connection.

* The `--binary-as-hex=FALSE` option affects how binary data is displayed in the output

* CAST operations (for example, `CAST(function_name() AS CHAR)`) convert binary data to character strings

### Uninstalling the plugin

To uninstall the `binlog_utils_udf` plugin, use the following command:

```sql
UNINSTALL PLUGIN binlog_utils_udf;
```

The plugin cannot be disabled without uninstalling. When uninstalled, all user-defined functions provided by the plugin are automatically removed and become unavailable.

To verify removal, check the `INFORMATION_SCHEMA.PLUGINS` table:

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME = 'binlog_utils_udf';
```

The query should return no rows if the plugin is successfully uninstalled.

## Limitations

For the following variables, do not define values with one or more dot (.) characters:

* [log_bin :octicons-link-external-16:](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_log-bin)

* [log_bin_index :octicons-link-external-16:](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#option_mysqld_log-bin-index)

A value defined with these characters is handled differently in *MySQL* and Percona XtraBackup and can cause unpredictable behavior.
