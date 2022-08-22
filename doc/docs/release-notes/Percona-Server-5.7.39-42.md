# *Percona Server for MySQL* 5.7.39-42 (2022-08-15)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.39-42
includes all the features and bug fixes available in [MySQL 5.7.39 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-39.html) in addition to enterprise-grade features developed by Percona.

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open
source drop-in replacement for any *MySQL* database. It provides superior
performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide
better performance and concurrency for their most demanding workloads. It
delivers more value to *MySQL* server users with optimized performance,
greater performance scalability and availability, enhanced backups, and
increased visibility. [Commercial support contracts are available](https://www.percona.com/services/support/mysql-support).

## Release Highlights

Improvements and bug fixes provided by Oracle for *MySQL* 5.7.39 and included in Percona Server for MySQL are the following:

* To provide process information, the `SHOW PROCESSLIST` statement collects thread data from all active threads. Since the implementation iterates across active threads from within the thread manager while holding a global mutex, it has a negative impact on performance, particularly on busy systems.

Now, an alternative `SHOW PROCESSLIST` implementation is available based on the new Performance Schema processlist table. This implementation queries active thread data from the Performance Schema rather than the thread manager and does not require a mutex:

* To enable the alternative implementation, enable the `performance_schema_show_processlist` system variable.

    !!! note
        For new installations of MySQL 5.7.39, or higher, the processlist table is automatically created in the Performance Schema. It is not created automatically by an upgrade. If you are upgrading from an earlier version of MySQL 5.7, and want to use the Performance Schema implementation of processlist, create the table manually.

Find more information in the [Creating the processlist table](https://dev.mysql.com/doc/refman/5.7/en/performance-schema-processlist-table.html#performance-schema-processlist-table-creating).

* The alternative implementation of `SHOW PROCESSLIST` also applies to the *mysqladmin* processlist command.

* The alternative implementation does not apply to the `INFORMATION_SCHEMA PROCESSLIST` table or the `COM_PROCESS_INFO` command of the MySQL client/server protocol.

* To ensure that the default and alternative implementations give the same information, check the configuration requirements in [The processlist Table](https://dev.mysql.com/doc/refman/5.7/en/performance-schema-processlist-table.html#performance-schema-processlist-table-creating).

* MySQL removes a 4GB tablespace file size limit on Windows 32-bit systems. The limit was set because of an incorrect calculation performed while extending the tablespace.

* When, during a session, an incorrect value for the `binlog_checksum` system variable is set, a `COM_BINLOG_DUMP` command ran in the same session to request a binary log stream from a source fails. Now, the server validates the specified checksum value before starting the checksum algorithm setup process.

Find the full list of bug fixes and changes in the [MySQL 5.7.39 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-39.html).

## Deprecation and removal

* The `myisam_repair_threads` system variable has been removed.

* **myisamchk** `--parallel-recover` option has been removed.

## Improvements

The `SHOW PROCESSLIST` statement now displays an extra field `TIME_MS`. The `TIME_MS` field provides the information about the time in milliseconds that the thread has been in its current state.

## Bugs Fixed

* [PS-8205](https://jira.percona.com/browse/PS-8205): `DICT_TF2_FLAG_SET` was used instead of `DICT_TF2_FLAG_IS_SET`.

* [PS-8174](https://jira.percona.com/browse/PS-8174): MySQL crashed at shutdown with `buf0flu.cc:3567:UT_LIST_GET_LEN(buf_pool->flush_list) == 0` assertion.

## Useful links

* The [Percona Server for MySQL installation instructions](https://www.percona.com/doc/percona-server/5.7/installation.html)

* The [Percona Server In-Place Upgrading Guide: From 5.6 to 5.7](https://www.percona.com/doc/percona-server/5.7/upgrading_guide_56_57.html)

* The [Percona Software downloads](https://www.percona.com/downloads/)

* The [Percona Server for MySQL GitHub location](https://github.com/percona/percona-server)

* To contribute to the documentation, review the [Documentation Contribution Guide](https://github.com/percona/percona-server/blob/8.0/doc/source/contributing.md)
