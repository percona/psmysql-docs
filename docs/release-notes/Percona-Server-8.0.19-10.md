# Percona Server for MySQL 8.0.19-10 (2020-03-23)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/8.0/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.19-10
includes all the features and bug fixes available in
[MySQL 8.0.19 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-19.html)
in addition to enterprise-grade features developed by Percona.

## New Features


* [PS-5729](https://jira.percona.com/browse/PS-5729): Added server’s UUID to Percona system keys.


* [PS-5917](https://jira.percona.com/browse/PS-5917): Added Simplified LDAP authentication plugin.


* [PS-4464](https://jira.percona.com/browse/PS-4464): Exposed the last global transaction identifier (GTID) executed for a CONSISTENT SNAPSHOT.

## Improvements


* [PS-6775](https://jira.percona.com/browse/PS-6775): Removed the KEYRING_ON option from default_table_encryption.


* [PS-6733](https://jira.percona.com/browse/PS-6733): Added binary search to the Data masking plugin.

## Bugs Fixed


* [PS-6811](https://jira.percona.com/browse/PS-6811): Service failed to start asserting ACL_PROXY_USER::check_validity if –skip-name-resolve=1 and there is a Proxy user. (Upstream [#98908](http://bugs.mysql.com/bug.php?id=98908))


* [PS-6112](https://jira.percona.com/browse/PS-6112): Inconsistent `Binlog_snapshot_gtid` when mysqldump was used with –single-transaction.


* [PS-5923](https://jira.percona.com/browse/PS-5923): “SELECT … INTO var_name FOR UPDATE” was not working in MySQL 8.0. (Upstream [#96677](http://bugs.mysql.com/bug.php?id=96677))


* [PS-6150](https://jira.percona.com/browse/PS-6150): The execution of SHOW ENGINE INNODB STATUS to show locked mutexes could cause a server exit.


* [PS-5379](https://jira.percona.com/browse/PS-5379): Slow startup after an upgrade from MySQL 5.7 to MySQL 8. (Upstream [#96340](http://bugs.mysql.com/bug.php?id=96340))


* [PS-6750](https://jira.percona.com/browse/PS-6750): The installation of client packages could cause a file conflict in Red Hat Enterprise Linux 8.


* [PS-5675](https://jira.percona.com/browse/PS-5675): Concurrent INSERT … ON DUPLICATE KEY UPDATE statements could cause a failure with a unique index violation. (Upstream [#96578](http://bugs.mysql.com/bug.php?id=96578))


* [PS-6857](https://jira.percona.com/browse/PS-6857): New package naming broke dbdeployer.


* [PS-6767](https://jira.percona.com/browse/PS-6767): The execution of a stored function in a WHERE clause was skipped. (Upstream [#98160](http://bugs.mysql.com/bug.php?id=98160))


* [PS-5421](https://jira.percona.com/browse/PS-5421): MyRocks: Corrected documentation for rocksdb_db_write_buffer_size.


* [PS-6761](https://jira.percona.com/browse/PS-6761): MacOS error in threadpool_unix.cc: there was no matching member function for call to ‘compare_exchange_weak’.


* [PS-6900](https://jira.percona.com/browse/PS-6900): The test big-test required re-recording after explicit_encryption was re-added.


* [PS-6897](https://jira.percona.com/browse/PS-6897): The main.udf_myisam test and main.transactional_acl_tables test failed on trunk.


* [PS-6106](https://jira.percona.com/browse/PS-6106): ALTER TABLE without ENCRYPTION clause caused tables to be encrypted.


* [PS-6093](https://jira.percona.com/browse/PS-6093): The execution of SHOW ENGINE INNODB STATUS to show locked mutexes with simultaneous access to a compressed table could cause a server exit.


* [PS-5552](https://jira.percona.com/browse/PS-5552): Assertion ‘m_idx >= 0’ failed in plan_idx QEP_share d::idx() const. (Upstream [#98258](http://bugs.mysql.com/bug.php?id=98258))


* [PS-6899](https://jira.percona.com/browse/PS-6899): The tests, main.events_bugs and main.events_1, failed because 2020-01-01 was considered a future time. (Upstream [#98860](http://bugs.mysql.com/bug.php?id=98860))


* [PS-6881](https://jira.percona.com/browse/PS-6881): Documented that mysql 8.0 does not require mysql_upgrade.


* [PS-6796](https://jira.percona.com/browse/PS-6796): The test, percona_changed_page_bmp_shutdown_thread, was unstable.


* [PS-6773](https://jira.percona.com/browse/PS-6773): A conditional jump or move depended on uninitialized value(s) in sha256_password_authenticate. (Upstream [#98223](http://bugs.mysql.com/bug.php?id=98223))


* [PS-6125](https://jira.percona.com/browse/PS-6125): MyRocks: To set rocksdb_update_cf_options with a nonexistent column family created a partially-defined column family which could cause a server exit.


* [PS-6037](https://jira.percona.com/browse/PS-6037): When Extra Packages Enterprise Linux (EPEL) 8 repo was enabled on CentOS/RHEL 8, jemalloc v5 was installed.


* [PS-5956](https://jira.percona.com/browse/PS-5956): Root session could kill Utility user session.


* [PS-5952](https://jira.percona.com/browse/PS-5952): Utility user was visible in performance_schema.threads.


* [PS-5843](https://jira.percona.com/browse/PS-5843): A memory leak could occur after “group_replication.gr_majority_loss_restart”. (Upstream [#96471](http://bugs.mysql.com/bug.php?id=96471))


* [PS-5642](https://jira.percona.com/browse/PS-5642): The page tracker thread did not exit if the startup failed.


* [PS-5325](https://jira.percona.com/browse/PS-5325): A conditional jump or move depended on uninitialized value on innodb_zip.wl5522_zip or innodb.alter_missing_tablespace.


* [PS-4678](https://jira.percona.com/browse/PS-4678): MyRocks: Documented the generated columns limitation.


* [PS-4649](https://jira.percona.com/browse/PS-4649): TokuDB: Documented PerconaFT (fractal tree indexing).
