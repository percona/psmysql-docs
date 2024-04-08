# Percona Server for MySQL 8.0.28-19 (2022-05-12)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.28-19
includes all the features and bug fixes available in the
[MySQL 8.0.28 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-28.html)
in addition to enterprise-grade features developed by Percona.

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open
source drop-in replacement for any *MySQL* database. It provides superior
performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide
better performance and concurrency for their most demanding workloads. It
delivers more value to *MySQL* server users with optimized performance,
greater performance scalability and availability, enhanced backups, and
increased visibility. [Commercial support contracts are available](https://www.percona.com/services/support/mysql-support).

## Release highlights

Improvements and bug fixes introduced by Oracle for *MySQL* 8.0.28 and included in Percona Server for MySQL are the following:


* The `ASCII` shortcut for `CHARACTER SET latin1` and `UNICODE` shortcut for `CHARACTER SET ucs2` are deprecated and raise a warning to use `CHARACTER SET` instead. The shortcuts will be removed in a future version.


* A stored function and a loadable function with the same name can share the same namespace. Add the schema name when invoking a stored function in the shared namespace. The server generates a warning when function names collide.


* InnoDB supports `ALTER TABLE ... RENAME COLUMN` operations when using `ALGORITHM=INSTANT`.


* The limit for `innodb_open_files` now includes temporary tablespace files. The temporary tablespace files were not counted in the `innodb_open_files` in previous versions.

Find the full list of bug fixes and changes in the [MySQL 8.0.28 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-28.html).

## Deprecation and removal

Starting with **Percona Server for MySQL** 8.0.28-19, the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and the storage engine is disabled in our binary builds.

## Improvement


* [PS-7871](https://jira.percona.com/browse/PS-7871): Using the `SET_VAR` syntax, MyRocks variables can be set dynamically.


* [PS-8064](https://jira.percona.com/browse/PS-8064): The ability to change log file locations dynamically is restricted.

## Bugs fixed


* [PS-7999](https://jira.percona.com/browse/PS-7999): The `FEDERATED` storage engine would not reconnect when a `wait_timeout` was exceeded. (Thanks to Sami Ahlroos for reporting this issue) (Upstream [#105878](http://bugs.mysql.com/bug.php?id=105878))


* [PS-7856](https://jira.percona.com/browse/PS-7856): Fixed for a sever exit caused by an update query on a partition tables.


* [PS-8032](https://jira.percona.com/browse/PS-8032): An Inplace index build with `lock=exclusive` did not generate an `MLOG_ADD_INDEX` redo.


* [PS-8050](https://jira.percona.com/browse/PS-8050): An upgrade from *Percona Server for MySQL* 5.7 to *MySQL* 8.0.26, caused a server exit with an assertion failure.

## Useful links


* The [Percona Server for MySQL installation instructions](https://www.percona.com/doc/percona-server/LATEST/installation.html)


* [Download Percona Server for MySQL 8.0](https://www.percona.com/downloads/Percona-Server-LATEST/)


* The [Percona Server for MySQL GitHub location](https://github.com/percona/percona-server)


* To contribute to the documentation, review the [Documentation Contribution Guide](https://github.com/percona/psmysql-docs/blob/8.0/contributing.md)
