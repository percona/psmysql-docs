# *Percona Server for MySQL* 5.7.30-33 ((2020-05-20)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/5.7/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.30-33
includes all the features and bug fixes available in
[MySQL 5.7.30 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-30.html)
in addition to enterprise-grade features developed by Percona.

Merged MyRocks/RocksDB up to Facebook MySQL production tag fb-prod201907.

## New Features

* [PS-6951](https://jira.percona.com/browse/PS-6951): Document new RocksDB variables: rocksdb_delete_cf, rocksdb_enable_iterate_bounds, and rocksdb_enable_remove_orphaned_dropped_cfs

* [PS-4464](https://jira.percona.com/browse/PS-4464): Expose the last global transaction identifier (GTID) executed for a CONSISTENT SNAPSHOT.

* [PS-6926](https://jira.percona.com/browse/PS-6926): Document RocksDB variables: rocksdb_table_stats_recalc_threshold_pct, rocksdb_table_stats_recalc_threshold_count, rocksdb_table_stats_background_thread_nice_value, rocksdb_table_stats_max_num_rows_scanned, rocksdb_table_stats_use_table_scan. rocksdb_table_stats_background_thread_nice_value,  rocksdb_table_stats_max_num_rows_scanned,  rocksdb_table_stats_use_table_scan, and rocksdb_trace_block_cache_access.

* [PS-6901](https://jira.percona.com/browse/PS-6901): Document RocksDB variable: rocksdb_read_free_rpl.

* [PS-6890](https://jira.percona.com/browse/PS-6890): Document RocksDB variable: rocksdb_blind_delete_primary_key.

* [PS-6885](https://jira.percona.com/browse/PS-6885): Document the new variable rocksdb_rollback_on_timeout which allows the rollback of an entire transaction on timeout.

* [PS-6891](https://jira.percona.com/browse/PS-6891): Document RocksDB variable: rocksdb_master_skip_tx_api.

* [PS-6886](https://jira.percona.com/browse/PS-6886): Document variable rocksdb_cache_dump which includes RocksDB block cache content in a core dump.

* [PS-6910](https://jira.percona.com/browse/PS-6910): Document RocksDB variable: rocksdb_stats_level.

## Improvements

* [PS-6984](https://jira.percona.com/browse/PS-6984): Update the zstd submodule to v1.4.4.

## Bugs Fixed

* [PS-6979](https://jira.percona.com/browse/PS-6979): Modify the processing to call clean up functions to remove CREATE USER statement from the processlist after the statement has completed (Upstream [#99200](http://bugs.mysql.com/bug.php?id=99200))

* [PS-6860](https://jira.percona.com/browse/PS-6860): Merge innodb_buffer_pool_pages_LRU_flushed into buf_get_total_stat()

* [PS-6811](https://jira.percona.com/browse/PS-6811): Correct service failure of asserting ACL_PROXY_USER when skip-name-resolve=1 and there is a Proxy user (Upstream [#98908](http://bugs.mysql.com/bug.php?id=98908))

* [PS-6112](https://jira.percona.com/browse/PS-6112): Correct Binlog_snapshot_gtid inconsistency when mysqldump was used with –single-transaction.

* [PS-6945](https://jira.percona.com/browse/PS-6945): Correct tokubackup plugin process exported API to allow large file backups.

* [PS-6856](https://jira.percona.com/browse/PS-6856): Correct binlogs corruptions in PS 5.7.28 and 5.7.29 (Upstream [#97531](http://bugs.mysql.com/bug.php?id=97531))

* [PS-6946](https://jira.percona.com/browse/PS-6946): Correct tokubackup processing to free memory use from the address and thread sanitizers

* [PS-5893](https://jira.percona.com/browse/PS-5893): Add support for running multiple instances with systemD on Debian.

* [PS-5620](https://jira.percona.com/browse/PS-5620): Modify Docker image to support supplying custom TLS certificates

* [PS-4573](https://jira.percona.com/browse/PS-4573): Implement use of a single config file - mysqld.cnf file.

* [PS-7041](https://jira.percona.com/browse/PS-7041): Correct Compilation error when -DWITH_EDITLINE=bundled is used

* [PS-7020](https://jira.percona.com/browse/PS-7020): Modify MTR tests for Ubuntu 20.04 to include python2 (python 2.6 or higher) and python3

* [PS-6974](https://jira.percona.com/browse/PS-6974): Correct instability in the rocksdb.drop_cf_\* tests

* [PS-6969](https://jira.percona.com/browse/PS-6969): Correct instability in the rocksdb.index_stats_large_table

* [PS-6954](https://jira.percona.com/browse/PS-6954): Correct tokudb-backup-plugin to avoid collision between -std=c++11 and -std=gnu++03.

* [PS-6925](https://jira.percona.com/browse/PS-6925): Correct mismatched default socket values for mysqld and mysqld_safe

* [PS-6899](https://jira.percona.com/browse/PS-6899): Correct main.events_bugs and main.events_1 to interpret date 01-01-2020 properly (Upstream [#98860](http://bugs.mysql.com/bug.php?id=98860))

* [PS-6796](https://jira.percona.com/browse/PS-6796): Correct instability in percona_changed_page_bmp_shutdown_thread

* [PS-6773](https://jira.percona.com/browse/PS-6773): Initialize values in sha256_password_authenticate (Upstream [#98223](http://bugs.mysql.com/bug.php?id=98223))

* [PS-5844](https://jira.percona.com/browse/PS-5844): Fix a memory leak after ‘innodb.alter_crash’ in ‘prepare_inplace_alter_table_dict()’ (Upstream [#96472](http://bugs.mysql.com/bug.php?id=96472))

* [PS-5735](https://jira.percona.com/browse/PS-5735): Correct 5.7 package to install the charsets on CentOS 7

* [PS-4757](https://jira.percona.com/browse/PS-4757): Remove CHECK_IF_CURL_DEPENDS_ON_RTMP to build keyring_vault for unconditional test

* [PS-4649](https://jira.percona.com/browse/PS-4649): Document PerconaFT in TokuDB which is fractal tree indexing to enhance the B-tree data structure