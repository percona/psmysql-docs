# Percona Server for MySQL 8.0.27-18 (2022-03-02)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/8.0/installation.html)


[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.27-18
includes all the features and bug fixes available in the
[MySQL 8.0.27 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-27.html).
in addition to enterprise-grade features developed by Percona.

*Percona Server for MySQL* is a free, fully compatible, enhanced and open
source drop-in replacement for any *MySQL* database. It provides superior
performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide
better performance and concurrency for their most demanding workloads, and
delivers greater value to *MySQL* server users with optimized performance,
greater performance scalability and availability, enhanced backups and
increased visibility. [Commercial support contracts are available](https://www.percona.com/services/support/mysql-support).

## Release highlights

The following lists a number of the bug fixes for *MySQL* 8.0.27, provided by Oracle, and included in Percona Server for MySQL:


* The `default_authentication_plugin` is deprecated. Support for this plugin may be removed in future versions. Use the `authentication_policy` variable.


* The `binary` operator is deprecated. Support for this operator may be removed in future versions. Use `CAST(... AS BINARY)`.


* Fix for when a parent table initiates a cascading `SET NULL` operation on the child table, the virtual column can be set to NULL instead of the value derived from the parent table.

Find the full list of bug fixes and changes in the [MySQL 8.0.27 Release Notes](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-27.html).

## New features


* [PS-7960](https://jira.percona.com/browse/PS-7960): Documented the `rocksdb_partial_index_sort_max_mem` variable, the `rocksdb_bulk_load_partial_index` variable, and the `rocksdb_cancel_manual_compactions` variable.


* [PS-2346](https://jira.percona.com/browse/PS-2346): LP #720547: Implemented an option to allow queries with specific error codes to add entries to the Slow Query Log.

## Improvements


* [PS-7955](https://jira.percona.com/browse/PS-7955): Enabled ZenFS functionality on standard Percona Server packages on Debian 11 and Ubuntu 20.04.


* [PS-7931](https://jira.percona.com/browse/PS-7931): Implemented a Slow Query Log Rotation and Expiration in Percona Server for MySQL 8.0.


* [PS-6730](https://jira.percona.com/browse/PS-6730): The ‘Last_errno:’ field in the Slow Query Log contains only error information.


* [PS-8076](https://jira.percona.com/browse/PS-8076): Added a deprecation warning when using XtraDB changed page tracking.

## Bugs fixed


* [PS-7883](https://jira.percona.com/browse/PS-7883): An `ALTER` query caused a server exit when `--rocksdb_write_disable_wal` was enabled.


* [PS-8007](https://jira.percona.com/browse/PS-8007): *Percona Server for MySQL* can fail to start if the server starts before the network mounts the datadir or a local mount of the datadir.


* [PS-7977](https://jira.percona.com/browse/PS-7977): The AppArmor profile is broken after an 8.0.22-13 to 8.0.23-14 upgrade. (Thanks to Alex Kompel for reporting this issue)


* [PS-7958](https://jira.percona.com/browse/PS-7958): A `SELECT` statement using a Full-Text Search index with a special character caused a server exit.


* [PS-7940](https://jira.percona.com/browse/PS-7940): The initialization of a virtual column template if a child table had a virtual column caused a restart loop. This initialization prevented a server exit when there was an `ON DELETE CASCADE` statement in the parent table and the child table had virtual columns. (Upstream [#105290](http://bugs.mysql.com/bug.php?id=105290))


* [PS-5654](https://jira.percona.com/browse/PS-5654): On a view, the query digest for each SELECT statement is now based on the SELECT statement and not the view definition, which was the case for earlier versions (Upstream [#89559](http://bugs.mysql.com/bug.php?id=89559))


* [PS-7975](https://jira.percona.com/browse/PS-7975): Fix to allow test main.mtr_unit_tests to complete successfully (Thanks to Thomas Deutschmann for reporting this issue)


* [PS-7873](https://jira.percona.com/browse/PS-7873): Fix for when the log_status table reported an incorrect executed_gtid (Thanks to zhujzhuo for reporting this issue) (Upstream [#102175](http://bugs.mysql.com/bug.php?id=102175))


* [PS-5168](https://jira.percona.com/browse/PS-5168) Fix for when the Slow Query Log reports `tmp_table_size:0`.


* Normalized the `zenfs` utility backup and restore requirements for the `--path` command line option, the `--backup_path` command-lne option, and the `restore_path` command-line option. For more information, see Installing and configuring Percona Server for MySQL with ZenFS support.

## Packaging notes


* Red Hat Enterprise Linux 6 (and derivative Linux distributions) are no longer supported.

## Known issues

The RPM packages for Red Hat Enterprise Linux 7 (and compatible derivatives) do not support TLSv1.3, as it requires OpenSSL 1.1.1, which is currently not available on this platform.

## Contact us

The [Documentation Contribution Guide](https://github.com/percona/psmysql-docs/blob/8.0/contributing.md) describes the methods available to contribute to the Percona Server for MySQL documentation.

For free technical help, visit the Percona [Community Forum](https://forums.percona.com/c/mysql-mariadb/percona-server-for-mysql-8-0/20).

To report bugs or submit feature requests, open a [JIRA](https://jira.percona.com/projects/PS/issues) ticket.

For paid [support](https://www.percona.com/services/support) and [managed services](https://www.percona.com/services/managed-services) or [consulting services](https://www.percona.com/services/consulting), contact [Percona Sales](https://www.percona.com/about-percona/contact).
