# Binary logs and replication improvements

Due to continuous development, Percona Server for MySQL incorporated a number of
improvements related to replication and binary logs handling. This resulted in replication specifics, which distinguishes it from *MySQL*.

## Safety of statements with a `LIMIT` clause

### Summary of the fix

*MySQL* considers all `UPDATE/DELETE/INSERT ... SELECT` statements with
`LIMIT` clause to be unsafe, no matter wether they are really producing
non-deterministic result or not, and switches from statement-based logging
to row-based one. *Percona Server for MySQL* is more accurate, it acknowledges such
instructions as safe when they include `ORDER BY PK` or `WHERE`
condition. This fix has been ported from the upstream bug report
[#42415](https://bugs.mysql.com/bug.php?id=42415) ([#44](https://jira.percona.com/browse/PS-44)).

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
transactions the situation became proportionally worse. Bug fixed [#1786](https://jira.percona.com/browse/PS-1786), (upstream [#85141](https://bugs.mysql.com/bug.php?id=85141)).

## Performance improvement on source and connection status updates

### Source and connection status update fix

Replica nodes configured to update source status and connection information
only on log file rotation did not experience the expected reduction in load.
*MySQL* was additionally updating this information in case of multi-source
replication when replica had to skip the already executed GTID event.

## Write `FLUSH` commands to the binary log

`FLUSH` commands, such as `FLUSH SLOW LOGS`, are not written to the
binary log if the system variable binlog_skip_flush_commands is set
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

When binlog_skip_flush_commands is set to **ON**, `FLUSH ...` commands are not written to the binary
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

If the variable is enabled, single table `DROP TABLE` DDL statements are logged in the binary log with comments. Multi-table `DROP TABLE` DDL statements are not supported and return an error.

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

!!! note

    All functions returning timestamps return their values as microsecond precision UNIX time. In other words, they represent the number of microseconds since 1-JAN-1970.

All functions accepting a binlog name as the parameter accepts only short names, without a path component. If the path separator (‘/’) is found in the input, an error is returned. This serves the purpose of restricting the locations from where binlogs can be read. They are always read from the current binlog directory ([@@log_bin_basename system variable]).

All functions returning binlog file names return the name in short form, without a path component.

The basic syntax for `get_binlog_by_gtid()` is the following:

    * get_binlog_by_gtid(string) [AS] alias

Usage: SELECT get_binlog_by_gtid(string) [AS] alias

Example:

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

For example:

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

For example:

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

Example:

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

For example:

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

For example:

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

A value defined with these characters is handled differently in *MySQL* and Percona XtraBackup and can cause unpredictable behavior.

[@@log_bin_basename system variable]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#sysvar_log_bin_basename

[log_bin]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin

[log_bin_index]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#option_mysqld_log-bin-index