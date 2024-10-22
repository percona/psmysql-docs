# Binary logs and replication improvements

Due to continuous development, Percona Server for MySQL incorporated a number of
improvements related to replication and binary logs handling. This resulted in replication specifics, which distinguishes it from MySQL.

## Statements with a `LIMIT` clause

In MySQL 8.0, any UPDATE/DELETE/INSERT ... SELECT statements that include a LIMIT clause are indeed considered unsafe for statement-based replication. These statements will cause MySQL to automatically switch from statement-based logging to row-based logging if binlog_format is set to MIXED.

Here's why:

* The LIMIT clause without an ORDER BY makes the result set non-deterministic

* The same statement might affect different rows on the primary and replicas

```sql
UPDATE table1 LIMIT 10 SET col1 = 'value';
DELETE FROM table1 LIMIT 5;
INSERT INTO table2 SELECT * FROM table1 LIMIT 3;
```

To make these statements safe for statement-based replication, you should do one of the following:

* Remove the LIMIT clause

* Add an ORDER BY clause to make the result set deterministic

```sql
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
binary log if the system variable `binlog_skip_flush_commands` is set
to **ON**.

In addition, the following changes were implemented in the behavior of
`read_only` and super_read_only modes:

* When `read_only` is set to **ON**, any `FLUSH ...` command executed by a
normal user (without the `SUPER` privilege) are not written to the binary
log regardless of the value of the binlog_skip_flush_command variable.

* When super_read_only is set to **ON**, any `FLUSH ...` command executed by
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

When `binlog_skip_flush_commands` is set to **ON**, `FLUSH ...` commands are not written to the binary
log. 

The `binlog_skip_flush_commands` setting does not affect the following commands because they are not written to binary log:

	•	`FLUSH LOGS`
	
	•	`FLUSH BINARY LOGS`
	
	•	`FLUSH TABLES WITH READ LOCK`
	
	•	`FLUSH TABLES ... FOR EXPORT`


The `FLUSH` command does not record to the binary log, and it ignores the `binlog_skip_flush_commands` value when you run it with the `NO_WRITE_TO_BINLOG` keyword (or its alias `LOCAL`).

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

When disabled (default setting), the server removes comments and adds quotation marks.

If the variable is enabled, all single table `DROP TABLE` DDL statements are logged in the binary log with the following:

•	Comments are preserved, so any notes you add to the command stay in the binary log.

•	Quotation marks are not added.


You can enable `binlog_ddl_skip_rewrite` at runtime:

```sql
-- Check current setting
SHOW VARIABLES LIKE 'binlog_ddl_skip_rewrite';

-- Enable feature
SET GLOBAL binlog_ddl_skip_rewrite = ON;

-- Disable feature
SET GLOBAL binlog_ddl_skip_rewrite = OFF;
```

You can enable it permanently by adding it to the my.cnf configuration file:

```text
[mysqld]
binlog_ddl_skip_rewrite = ON
```

After adding the statement to the configuration file, restart the MySQL service.

Multi-table `DROP TABLE` DDL statements are not supported and return an error.

```sql
SET binlog_ddl_skip_rewrite = ON;
/*comment at start*/DROP TABLE t /*comment at end*/;
```

## Binary log user defined functions

To implement Point in Time recovery, we have added the `binlog_utils_udf`. The following user-defined functions are included:

| Name | Returns | Description |
| --- | --- | --- |
| get_binlog_by_gtid() | Binlog file name as STRING | Returns the binlog file name that contains the specified GTID |
| get_last_gtid_from_binlog() | GTID as STRING | Returns the last GTID found in the specified binlog |
| get_gtid_set_by_binlog() | GTID set as STRING | Returns all GTIDs found in the specified binlog |
| get_binlog_by_gtid_set() | Binlog file name as STRING | Returns the file name of the binlog which contains at least one GTID from the specified set. |
| get_first_record_timestamp_by_binlog() | Timestamp as INTEGER | Returns the timestamp of the first event in the specified binlog |
| get_last_record_timestamp_by_binlog() | Timestamp as INTEGER | Returns the timestamp of the last event in the specified binlog |

All functions returning timestamps return their values as microsecond precision UNIX time. In other words, they represent the number of microseconds since 1-JAN-1970.

All functions accepting a binlog name as the parameter accepts only short names, without a path component. If the path separator (‘/’) is found in the input, an error is returned. This serves the purpose of restricting the locations from where binlogs can be read. They are always read from the current binlog directory ([@@log_bin_basename system variable]).

All functions returning binlog file names return the name in short form, without a path component.

The basic syntax for `get_binlog_by_gtid()` is the following:

    * get_binlog_by_gtid(string) [AS] alias

Usage: SELECT get_binlog_by_gtid(string) [AS] alias

An example of using the `get_binlog_gtid` command:

```sql
CREATE FUNCTION get_binlog_by_gtid RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT get_binlog_by_gtid("F6F54186-8495-47B3-8D9F-011DDB1B65B3:1") AS result;
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

The basic syntax for `get_last_gtid_from_binlog()` is the following:

    * get_last_gtid_from_binlog(string) [AS] alias

Usage: SELECT get_last_gtid_from_binlog(string) [AS] alias

An example of using the `get_last_gtid_from_binlog` command:

```sql
CREATE FUNCTION get_last_gtid_from_binlog RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT get_last_gtid_from_binlog("binlog.00001") AS result;
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

The basic syntax for `get_gtid_set_by_binlog()` is the following:

    * get_gtid_set_by_binlog(string) [AS] alias

Usage: SELECT get_gtid_set_by_binlog(string) [AS] alias

An example of using the `get_gtid_set_by_binlog` command:

```sql
CREATE FUNCTION get_gtid_set_by_binlog RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT get_gtid_set_by_binlog("binlog.00001") AS result;
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

The basic syntax for `get_binlog_by_gtid_set()` is the following:


* get_binlog_by_gtid_set(string) [AS] alias

Usage: SELECT get_binlog_by_gtid_set(string) [AS] alias

An example of using the `get_binlog_by_gtid_set` command:

```sql
CREATE FUNCTION get_binlog_by_gtid_set RETURNS STRING SONAME 'binlog_utils_udf.so';
SELECT get_binlog_by_gtid_set("11ea-b9a7:7,11ea-b9a7:8") AS result;
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

The basic syntax for `get_first_record_timestamp_by_binlog()` is the following:

    * get_first_record_timestamp_by_binlog(TIMESTAMP) [AS] alias

Usage: SELECT get_first_record_timestamp_by_binlog(TIMESTAMP) [AS] alias

An example of using the `get_first_record_timestamp_by_binlog` command:

```sql
CREATE FUNCTION get_first_record_timestamp_by_binlog RETURNS INTEGER SONAME 'binlog_utils_udf.so';
SELECT FROM_UNIXTIME(get_first_record_timestamp_by_binlog("bin.00003") DIV 1000000) AS result;
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+
    | result              |
    +=====================+
    | 2020-12-03 09:10:40 |
    +---------------------+
    ```

```sql
DROP FUNCTION get_first_record_timestamp_by_binlog;
```

The basic syntax for `get_last_record_timestamp_by_binlog()` is the following:

    * get_last_record_timestamp_by_binlog(TIMESTAMP) [AS] alias

Usage: SELECT get_last_record_timestamp_by_binlog(TIMESTAMP) [AS] alias

An example of using the `get_last_record_timestamp_by_binlog` command:

```sql
CREATE FUNCTION get_last_record_timestamp_by_binlog RETURNS INTEGER SONAME 'binlog_utils_udf.so';
SELECT FROM_UNIXTIME(get_last_record_timestamp_by_binlog("bin.00003") DIV 1000000) AS result;
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+
    | result              |
    +=====================+
    | 2020-12-04 04:18:56 |
    +---------------------+
    ```

```sql
DROP FUNCTION get_last_record_timestamp_by_binlog;
```

## Limitations

For the following variables, do not define values with one or more dot (.) characters:

* [log_bin]

* [log_bin_index]

A value defined with the dot (.) character is handled differently in MySQL and Percona XtraBackup and can cause unpredictable behavior.

[@@log_bin_basename system variable]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#sysvar_log_bin_basename

[log_bin]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin

[log_bin_index]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin-index