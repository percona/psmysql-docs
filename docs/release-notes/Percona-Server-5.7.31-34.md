# Percona Server for MySQL 5.7.31-34 (2020-08-24)

* **Installation**  [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/5.7/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.31-34
includes all the features and bug fixes available in
[MySQL 5.7.31 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-31.html)
in addition to enterprise-grade features developed by Percona.

## New Features

* [PS-7128](https://jira.percona.com/browse/PS-7128): Document RocksDB variables: `rocksdb_max_background_compactions`, `rocksdb_max_background_flushes`, and `rocksdb_max_bottom_pri_background_compactions`

## Improvements

* [PS-7132](https://jira.percona.com/browse/PS-7132): Make default value of `rocksdb_wal_recovery_mode` compatible with InnoDB

* [PS-7199](https://jira.percona.com/browse/PS-7199): Add Coredumper functionality

* [PS-7114](https://jira.percona.com/browse/PS-7114): Enhance crash artifacts (core dumps and stack traces) to provide additional information to the operator

## Bugs Fixed

* [PS-7203](https://jira.percona.com/browse/PS-7203): Fixed audit plugin memory leak on replicas when opening tables

* [PS-7043](https://jira.percona.com/browse/PS-7043): Correct constant equality expression is used in LEFT JOIN condition by setting the ‘const_table’ flag together with setting the row as a NULL-row. (Upstream [#99499](http://bugs.mysql.com/bug.php?id=99499))

* [PS-7212](https://jira.percona.com/browse/PS-7212): Modify processing to binary compare in order to do native JSON comparison (Upstream [#100307](http://bugs.mysql.com/bug.php?id=100307))

* [PS-7076](https://jira.percona.com/browse/PS-7076): Modify to not update Cardinality after setting `tokudb_cardinality_scale_percent`

* [PS-7025](https://jira.percona.com/browse/PS-7025): Fix reading ahead of insert buffer pages by dispatching of buffered AIO transfers (Upstream [#100086](http://bugs.mysql.com/bug.php?id=100086))

* [PS-7010](https://jira.percona.com/browse/PS-7010): Modify to Lock buffer blocks before sanity check in btr_cur_latch_leaves

* [PS-6995](https://jira.percona.com/browse/PS-6995): Introduce a new optimizer switch to allow the user to reduce the cost of a range scan to determine best execution plan for Primary Key lookup

* [PS-5978](https://jira.percona.com/browse/PS-5978): Remove unneeded check of variable to allow mysqld_safe support –numa-interleave (Thanks to user springlin for reporting this issue)

* [PS-7220](https://jira.percona.com/browse/PS-7220): Fix activity counter update in purge coordinator and workers

* [PS-7234](https://jira.percona.com/browse/PS-7234): Modify PS minimal tarballs to remove COPYING.AGPLv3

* [PS-7204](https://jira.percona.com/browse/PS-7204): Add checks to linkingscript to correct failures in patchelf

* [PS-7075](https://jira.percona.com/browse/PS-7075): Provide binary tarball with shared libs and glibc suffix

* [PS-7062](https://jira.percona.com/browse/PS-7062): Modify ALTER INSTANCE ROTATE INNODB MASTER KEY to skip writing of redo for compressed encrypted temporary table.

* [PS-5263](https://jira.percona.com/browse/PS-5263): Update handle_binlog_flush_or_sync_error() to set my_ok(thd) after thd->clear_error() to correct assert in THD::send_statement_status (Upstream [#93770](http://bugs.mysql.com/bug.php?id=93770))

* [PS-4530](https://jira.percona.com/browse/PS-4530): Add documentation that `ps-admin` removes jemalloc and THP settings on TokuDB uninstall
