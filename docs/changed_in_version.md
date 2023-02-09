# Changed in Percona Server 8.0

*Percona Server for MySQL* 8.0 is based on *MySQL* 8.0 and incorporates many of the
improvements found in *Percona Server for MySQL* 5.7.

## Features ported to *Percona Server for MySQL* 8.0 from *Percona Server for MySQL* 5.7

The features are listed within the following sections:

### SHOW ENGINE INNODB STATUS Extensions


* The Redo Log state


* Specifying the InnoDB buffer pool sizes in bytes


* `innodb_print_lock_wait_timeout_info` system variable

### Performance


* [Prefix Index Queries Optimization](performance/prefix_index_queries_optimization.md#prefix-index-queries-optimization)


* [Multiple page asynchronous I/O requests](performance/aio_page_requests.md#aio-page-requests)


* [Thread Pool](performance/threadpool.md#threadpool)


* [Priority refill for the buffer pool free list](performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.md#ps-buffer-pool-free-list-priority-refill)


* [Multi-threaded LRU flusher](performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.md#lru-manager-threads)

### Flexibility


* [InnoDB Full-Text Search Improvements](flexibility/innodb_fts_improvements.md#innodb-fts-improvements)


* [Improved MEMORY Storage Engine](flexibility/improved_memory_engine.md#improved-memory-engine)


* [Extended mysqldump](flexibility/extended_mysqldump.md#extended-mysqldump)


* [Extended SELECT INTO OUTFILE/DUMPFILE](flexibility/extended_select_into_outfile.md#extended-select-into-outfile)


* [Support for PROXY protocol](flexibility/proxy_protocol_support.md#proxy-protocol-support)


* [Compressed columns with dictionaries](flexibility/compressed_columns.md#compressed-columns)

### Management


* [Percona Toolkit UDFs](management/udf_percona_toolkit.md#udf-percona-toolkit)


* [Kill Idle Transactions](management/kill_idle_trx.md)


* [XtraDB changed page tracking](management/changed_page_tracking.md)


* [PAM Authentication Plugin](./security/pam_plugin.md)


* [Expanded Fast Index Creation](management/innodb_expanded_fast_index_creation.md)


* [Backup Locks](management/backup_locks.md)


* [Audit Log Plugin](management/audit_log_plugin.md)


* [Start transaction with consistent snapshot](management/start_transaction_with_consistent_snapshot.md)


* [Extended SHOW GRANTS](management/extended_show_grants.md)


* [Data at Rest Encryption](security/data-at-rest-encryption.md#data-at-rest-encryption)

### Reliability


* [Handle Corrupted Tables](reliability/innodb_corrupt_table_action.md)


* [Too Many Connections Warning](reliability/log_connection_error.md)

### Diagnostics


* [User Statistics](diagnostics/user_stats.md)


* [Slow Query Log](diagnostics/slow_extended.md#slow-extended)


* [Show Storage Engines](diagnostics/show_engines.md)


* [Process List](diagnostics/process_list.md)


* [INFORMATION_SCHEMA.[GLOBAL_]TEMP_TABLES](diagnostics/misc_info_schema_tables.md)


* [Thread Based Profiling](diagnostics/thread_based_profiling.md)


* [InnoDB Page Fragmentation Counters](diagnostics/innodb_fragmentation_count.md)

#### Features Removed from *Percona Server for MySQL* 8.0

Some features, that were present in *Percona Server for MySQL* 5.7, are removed from
*Percona Server for MySQL* 8.0:

##### Removed Features


* [Slow Query Log Rotation and Expiration](https://docs.percona.com/percona-server/5.7/flexibility/slowlog_rotation.html)


* [CSV engine mode for standard-compliant quote and comma parsing](https://docs.percona.com/percona-server/5.7/flexibility/csv_engine_mode.html)


* [Expanded program option modifiers](https://docs.percona.com/percona-server/5.7/management/expanded_program_option_modifiers.html)


* [The ALL_O_DIRECT InnoDB flush method: it is not compatible with the new
redo logging implementation](https://docs.percona.com/percona-server/5.7/scalability/innodb_io.html)


* [XTRADB_RSEG table from INFORMATION_SCHEMA](https://docs.percona.com/percona-server/5.7/diagnostics/misc_info_schema_tables.html)


* [InnoDB memory size information from SHOW ENGINE INNODB STATUS; the same
information is available from Performance Schema memory summary tables](https://docs.percona.com/percona-server/5.7/diagnostics/innodb_show_status.html)


* [Query cache enhancements](https://docs.percona.com/percona-server/5.7/performance/query_cache_enhance.html#query-cache-enhancements)

##### Removed Syntax


* The `SET STATEMENT ... FOR ...` statement that enabled setting a
variable for a single query. For more information see
Replacing SET STATEMENT FOR with the Upstream Equivalent.


* The `LOCK BINLOG FOR BACKUP` statement due to the introduction of the
`log_status` table in Performance Schema of *MySQL* 8.0.

##### Removed plugins

* `SCALABILITY_METRICS`

* `QUERY_RESPONSE_TIME` plugins

The `QUERY_RESPONSE_TIME` plugins have been removed from *Percona Server for MySQL* 8.0 as the Performance Schema of *MySQL* 8.0
provides histogram data for statement execution time.

##### Removed system variables

* The [innodb_use_global_flush_log_at_trx_commit](https://docs.percona.com/percona-server/5.7/scalability/innodb_io.html#innodb_use_global_flush_log_at_trx_commit)
system variable which enabled setting the global *MySQL* variable
[innodb_flush_log_at_trx_commit](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit)


* [pseudo_server_id](https://docs.percona.com/percona-server/5.7/flexibility/per_session_server-id.html#pseudo_server_id)


* [max_slowlog_files](https://docs.percona.com/percona-server/5.7/flexibility/slowlog_rotation.html#max_slowlog_files)


* [max_slowlog_size](https://docs.percona.com/percona-server/5.7/flexibility/slowlog_rotation.html#max_slowlog_size)


* [innodb_show_verbose_locks](https://docs.percona.com/percona-server/5.7/diagnostics/innodb_show_status.html#innodb_show_verbose_locks):
showed the records locked in `SHOW ENGINE INNODB STATUS`


* [NUMA support in mysqld_safe](https://docs.percona.com/percona-server/5.7/performance/innodb_numa_support.html#improved-numa-support)


* `innodb_kill_idle_trx` which was an alias to the `kill_idle_trx` system variable


* The [max_binlog_files](https://docs.percona.com/percona-server/5.7/flexibility/max_binlog_files.html#max_binlog_files) system variable

##### Deprecated storage engine


* The TokuDB Storage Engine was [declared as deprecated](https://docs.percona.com/percona-server/8.0/release-notes/Percona-Server-8.0.13-3.html) in Percona Server for MySQL 8.0 and will be disabled in upcoming 8.0 versions.

    We recommend migrating to the MyRocks Storage Engine.

    For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).
