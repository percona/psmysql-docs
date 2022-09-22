# Percona Server for MySQL 8.0.20-11 (2020-07-21)


* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/8.0/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.20-11
includes all the features and bug fixes available in
[MySQL 8.0.20 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-20.html)
in addition to enterprise-grade features developed by Percona.

As of 8.0.20-11, the Percona Parallel Doublewrite buffer implementation has been removed and has been replaced with the Oracle MySQL implementation.

## New Features


* [PS-7128](https://jira.percona.com/browse/PS-7128): Add RocksDB variables: rocksdb_max_background_compactions, rocksdb_max_background_flushes, and rocksdb_max_bottom_pri_background_compactions


* [PS-7039](https://jira.percona.com/browse/PS-7039): Add RocksDB variable: rocksdb_validate_tables


* [PS-6951](https://jira.percona.com/browse/PS-6951): Add RocksDB variables: rocksdb_delete_cf, rocksdb_enable_iterate_bounds, and rocksdb_enable_remove_orphaned_dropped_cfs


* [PS-6926](https://jira.percona.com/browse/PS-6926): Add RocksDB variables: rocksdb_table_stats_recalc_threshold_pct, rocksdb_table_stats_recalc_threshold_count, rocksdb_table_stats_background_thread_nice_value, rocksdb_table_stats_max_num_rows_scanned, rocksdb_table_stats_use_table_scan.


* [PS-6910](https://jira.percona.com/browse/PS-6910): Add RocksDB variable: rocksdb_stats_level.


* [PS-6902](https://jira.percona.com/browse/PS-6902): Add RocksDB variable: rocksdb_enable_insert_with_update_caching.


* [PS-6901](https://jira.percona.com/browse/PS-6901): Add RocksDB variable: rocksdb_read_free_rpl.


* [PS-6891](https://jira.percona.com/browse/PS-6891): Add RocksDB variable: rocksdb_master_skip_tx_api.


* [PS-6890](https://jira.percona.com/browse/PS-6890): Add RocksDB variable: rocksdb_blind_delete_primary_key.


* [PS-6886](https://jira.percona.com/browse/PS-6886): Add RocksDB variable: rocksdb_cache_dump.


* [PS-6885](https://jira.percona.com/browse/PS-6885): Add RocksDB variable: rocksdb_rollback_on_timeout.

## Improvements


* [PS-6994](https://jira.percona.com/browse/PS-6994): Implement rocksdb_validate_tables functionality in Percona Server 8.X


* [PS-6984](https://jira.percona.com/browse/PS-6984): Update the zstd submodule to v1.4.4.


* [PS-5764](https://jira.percona.com/browse/PS-5764): Introduce SEQUENCE_TABLE() table-level SQL function

## Bugs Fixed


* [PS-7019](https://jira.percona.com/browse/PS-7019): Correct query results for LEFT JOIN with GROUP BY (Upstream [#99398](http://bugs.mysql.com/bug.php?id=99398))


* [PS-6979](https://jira.percona.com/browse/PS-6979): Modify the processing to call clean up functions to remove CREATE USER statement from the processlist after the statement has completed (Upstream [#99200](http://bugs.mysql.com/bug.php?id=99200))


* [PS-6860](https://jira.percona.com/browse/PS-6860): Merge innodb_buffer_pool_pages_LRU_flushed into buf_get_total_stat()


* [PS-7038](https://jira.percona.com/browse/PS-7038): Set innodb-parallel-read_threads=1 to prevent kill process from hanging (Thanks to user wavelet123 for reporting this issue)


* [PS-6945](https://jira.percona.com/browse/PS-6945): Correct tokubackup plugin process exported API to allow large file backups. (Thanks to user prohaska7 for reporting this issue)


* [PS-7000](https://jira.percona.com/browse/PS-7000): Fix newer collations for proper space padding in MyRocks


* [PS-6991](https://jira.percona.com/browse/PS-6991): Modify package to include missing development files (Thanks to user larrabee for reporting this issue)


* [PS-6946](https://jira.percona.com/browse/PS-6946): Correct tokubackup processing to free memory use from the address and thread sanitizers (Thanks to user prohaska7 for reporting this issue)


* [PS-5893](https://jira.percona.com/browse/PS-5893): Add support for running multiple instances with systemD on Debian. (Thanks to user sasha for reporting this issue)


* [PS-5620](https://jira.percona.com/browse/PS-5620): Modify Docker image to support supplying custom TLS certificates (Thanks to user agarner for reporting this issue)


* [PS-7168](https://jira.percona.com/browse/PS-7168): Determine if file per tablespace using table flags to prevent assertion


* [PS-7161](https://jira.percona.com/browse/PS-7161): Fixed ‘CreateTempFile’ gunit test to support both ‘HAVE_O_TMPFILE’-style


* [PS-7142](https://jira.percona.com/browse/PS-7142): Set ‘KEYRING_VAULT_PLUGIN_OPT’ value when required


* [PS-7138](https://jira.percona.com/browse/PS-7138): Correct file reference for ps-admin broken in tar.gz package


* [PS-7127](https://jira.percona.com/browse/PS-7127): Provide mechanism to grant dynamic privilege to the utility user.


* [PS-7118](https://jira.percona.com/browse/PS-7118): Add ability to set LOWER_CASE_TABLE_NAMES option before initializing data directory


* [PS-7116](https://jira.percona.com/browse/PS-7116): Port MyRocks fix of Index Condition Pushdown (ICP)


* [PS-7075](https://jira.percona.com/browse/PS-7075): Provide binary tarball with shared libs and glibc suffix


* [PS-6974](https://jira.percona.com/browse/PS-6974): Correct instability in the rocksdb.drop_cf_\* tests


* [PS-6969](https://jira.percona.com/browse/PS-6969): Correct instability in the rocksdb.index_stats_large_table


* [PS-6105](https://jira.percona.com/browse/PS-6105): Modify innodb.mysqld_core_dump_without_buffer_pool_dynamic test to move assertion to correct location


* [PS-5735](https://jira.percona.com/browse/PS-5735): Correct package to install the charsets on CentOS 7


* [PS-4757](https://jira.percona.com/browse/PS-4757): Remove CHECK_IF_CURL_DEPENDS_ON_RTMP to build keyring_vault for unconditional test


* [PS-7131](https://jira.percona.com/browse/PS-7131): Improve resume_encryption_cond conditional variable handling to avoid missed signals


* [PS-7100](https://jira.percona.com/browse/PS-7100): Fix rocksdb_read_free_rpl test to properly count rows corresponding to broken index entries


* [PS-7082](https://jira.percona.com/browse/PS-7082): Correct link displayed on help client command


* [PS-7169](https://jira.percona.com/browse/PS-7169): Set rocksdb_validate_tables to disabled RocksDB while upgrading the server from 5.7 to 8.0.20
