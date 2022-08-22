# *Percona Server for MySQL* 5.7.29-32 (2020-02-05)

* **Installation**:  [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/5.7/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.29-32
includes all the features and bug fixes available in
[MySQL 5.7.29 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-29.html)
in addition to enterprise-grade features developed by Percona.

## Bugs Fixed

* [PS-1469](https://jira.percona.com/browse/PS-1469): The Memory storage engine detected an incorrect “is full” condition when the space contained reusable memory chunks that could be reused.

* [PS-6113](https://jira.percona.com/browse/PS-6113): If `ANALYZE TABLE` with persistent statistics ran more than 600 seconds the execution of a diagnostic query may cause a server exit. (Upstream [#97828](http://bugs.mysql.com/bug.php?id=97828))

* [PS-5813](https://jira.percona.com/browse/PS-5813): To set the `slow_query_log_use_global_control` to “none” could cause an error.

* [PS-6150](https://jira.percona.com/browse/PS-6150): The execution of SHOW ENGINE INNODB STATUS to show locked mutexes could cause a server exit.

* [PS-6750](https://jira.percona.com/browse/PS-6750): The installation of client packages could cause a file conflict in Red Hat Enterprise Linux 8.

* [PS-5940](https://jira.percona.com/browse/PS-5940): When a temporary table was dropped, the server exited. (Upstream [#96766](http://bugs.mysql.com/bug.php?id=96766))

* [PS-5675](https://jira.percona.com/browse/PS-5675): Concurrent INSERT … ON DUPLICATE KEY UPDATE statements could cause a failure with a unique index violation. (Upstream [#96578](http://bugs.mysql.com/bug.php?id=96578))

* [PS-5421](https://jira.percona.com/browse/PS-5421): MyRocks: Corrected documentation for `rocksdb_db_write_buffer_size`.

* [PS-4794](https://jira.percona.com/browse/PS-4794): Documented that using ps-admin to enable MyRocks does not disable Transparent Huge Pages.

* [PS-6093](https://jira.percona.com/browse/PS-6093): The execution of SHOW ENGINE INNODB STATUS to show locked mutexes with simultaneous access to a compressed table could cause a server exit.

* [PS-6148](https://jira.percona.com/browse/PS-6148): If ANALYZE TABLE with transient statistics ran more than 600 seconds the execution of a diagnostic query may cause a server exit. (Upstream [#97828](http://bugs.mysql.com/bug.php?id=97828))

* [PS-6125](https://jira.percona.com/browse/PS-6125): MyRocks: To set `rocksdb_update_cf_options` with a non-existant column family created a partially-defined column family which could cause a server exit.

* [PS-6123](https://jira.percona.com/browse/PS-6123): A Debian/Ubuntu init script used an incorrect comparison which could cause the service command to return before the server start.

* [PS-5956](https://jira.percona.com/browse/PS-5956): Root session could kill Utility user session.

* [PS-5952](https://jira.percona.com/browse/PS-5952): Utility user was visible in performance_schema.threads.

* [PS-5843](https://jira.percona.com/browse/PS-5843): A memory leak could occur after “group_replication.gr_majority_loss_restart”. (Upstream [#96471](http://bugs.mysql.com/bug.php?id=96471))

* [PS-5325](https://jira.percona.com/browse/PS-5325): Conditional jump or move depended on uninitialized value on innodb_zip.wl5522_zip or innodb.alter_missing_tablespace.
