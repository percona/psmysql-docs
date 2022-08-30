# *Percona Server for MySQL* 5.7.38-41 (2022-06-02)

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

Improvements and bug fixes provided by Oracle for *MySQL* 5.7.38 and included in Percona Server for MySQL are the following:

* If a statement cannot be parsed, for example, if the statement contains syntax errors, that statement is not written to the slow query log.

* Loading an encrypted table failed if purge threads processed the undo records for that table.

* There was a memory leak when mysqldump was used on more than one table with the –order-by-primary option. The memory allocated to sort each row in a table is now released after every table.

Find the full list of bug fixes and changes in the [MySQL 5.7.38 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-38.html).

## Deprecation and removal

* The `myisam_repair_threads` system variable is deprecated. Values other than 1 (the default) for `myisam_repair_threads` throw a warning. Support for this variable may be removed in future versions.

* **myisamchk** `--parallel-recover` option is deprecated. Support for this option may be removed in future versions.

## Bugs Fixed

* [PS-6029](https://jira.percona.com/browse/PS-6029): The data masking gen_rnd_us_phone() function had a different format compared to MySQL upstream version.

* [PS-8129](https://jira.percona.com/browse/PS-8129): A fix for when mutex hangs in thread_pool_unix.

* [PS-8136](https://jira.percona.com/browse/PS-8136): `LOCK TABLES FOR BACKUP` did not prevent InnoDB key rotation. Due to this behavior, Percona Xtrabackup couldn’t fetch the key in case the key was rotated after starting the backup.

* [PS-8143](https://jira.percona.com/browse/PS-8143): Fixed the memory leak in `File_query_log::set_rotated_name()`.

* [PS-8204](https://jira.percona.com/browse/PS-8204): When the `audit_log_format` was set to XML, logged queries were truncated after a newline character.

## Useful links

* The [Percona Server for MySQL installation instructions](https://www.percona.com/doc/percona-server/5.7/installation.html)

* The [Percona Server In-Place Upgrading Guide: From 5.6 to 5.7](https://www.percona.com/doc/percona-server/5.7/upgrading_guide_56_57.html)

* The [Percona Software downloads](https://www.percona.com/downloads/)

* The [Percona Server for MySQL GitHub location](https://github.com/percona/percona-server)

* To contribute to the documentation, review the [Documentation Contribution Guide](https://github.com/percona/percona-server/blob/8.0/doc/source/contributing.md)
