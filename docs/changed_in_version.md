# Changed in Percona Server 8.0

*Percona Server for MySQL* 8.0 is based on *MySQL* 8.0 and incorporates many of the
improvements found in *Percona Server for MySQL* 5.7.

## Features Ported to *Percona Server for MySQL* 8.0 from *Percona Server for MySQL* 5.7

The features are listed within the following sections:

### SHOW ENGINE INNODB STATUS Extensions


* The Redo Log state


* Specifying the InnoDB buffer pool sizes in bytes


* `innodb_print_lock_wait_timeout_info` system variable

### Performance


* Prefix Index Queries Optimization


* Multiple page asynchronous I/O requests


* Thread Pool


* Priority refill for the buffer pool free list


* Multi-threaded LRU flusher

### Flexibility


* InnoDB Full-Text Search Improvements


* Improved MEMORY Storage Engine


* Extended mysqldump


* Extended SELECT INTO OUTFILE/DUMPFILE


* Support for PROXY protocol


* Compressed columns with dictionaries

### Management


* Percona Toolkit UDFs


* Kill Idle Transactions


* XtraDB changed page tracking


* PAM Authentication Plugin


* Expanded Fast Index Creation


* Backup Locks


* Audit Log Plugin


* Start transaction with consistent snapshot


* Extended SHOW GRANTS


* Data at Rest Encryption

### Reliability


* Handle Corrupted Tables


* Too Many Connections Warning

### Diagnostics


* User Statistics


* Slow Query Log


* Show Storage Engines


* Process List


* INFORMATION_SCHEMA.[GLOBAL_]TEMP_TABLES


* Thread Based Profiling


* InnoDB Page Fragmentation Counters

#### Features Removed from *Percona Server for MySQL* 8.0

Some features, that were present in *Percona Server for MySQL* 5.7, are removed from
*Percona Server for MySQL* 8.0:

##### Removed Features


* [Slow Query Log Rotation and Expiration](https://www.percona.com/doc/percona-server/5.7/flexibility/slowlog_rotation.html)


* [CSV engine mode for standard-compliant quote and comma parsing](https://www.percona.com/doc/percona-server/5.7/flexibility/csv_engine_mode.html)


* [Expanded program option modifiers](https://www.percona.com/doc/percona-server/5.7/management/expanded_program_option_modifiers.html)


* [The ALL_O_DIRECT InnoDB flush method: it is not compatible with the new
redo logging implementation](https://www.percona.com/doc/percona-server/5.7/scalability/innodb_io.html)


* [XTRADB_RSEG table from INFORMATION_SCHEMA](https://www.percona.com/doc/percona-server/5.7/diagnostics/misc_info_schema_tables.html)


* [InnoDB memory size information from SHOW ENGINE INNODB STATUS; the same
information is available from Performance Schema memory summary tables](https://www.percona.com/doc/percona-server/5.7/diagnostics/innodb_show_status.html)


* [Query cache enhancements](https://www.percona.com/doc/percona-server/5.7/performance/query_cache_enhance.html#query-cache-enhancements)

##### Removed Syntax


* The `SET STATEMENT ... FOR ...` statement that enabled setting a
variable for a single query. For more information see
Replacing SET STATEMENT FOR with the Upstream Equivalent.


* The `LOCK BINLOG FOR BACKUP` statement due to the introduction of the
`log_status` table in Performance Schema of *MySQL* 8.0.

##### Removed Plugins


* `SCALABILITY_METRICS`


* `QUERY_RESPONSE_TIME` plugins

The `QUERY_RESPONSE_TIME` plugins have been removed from *Percona Server for MySQL* 8.0 as the Performance Schema of *MySQL* 8.0
provides histogram data for statement execution time.

##### Removed System variables


* The [innodb_use_global_flush_log_at_trx_commit](https://www.percona.com/doc/percona-server/5.7/scalability/innodb_io.html#innodb_use_global_flush_log_at_trx_commit)
system variable which enabled setting the global *MySQL* variable
[innodb_flush_log_at_trx_commit](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit)


* [pseudo_server_id](https://www.percona.com/doc/percona-server/5.7/flexibility/per_session_server-id.html#pseudo_server_id)


* [max_slowlog_files](https://www.percona.com/doc/percona-server/5.7/flexibility/slowlog_rotation.html#max_slowlog_files)


* [max_slowlog_size](https://www.percona.com/doc/percona-server/5.7/flexibility/slowlog_rotation.html#max_slowlog_size)


* [innodb_show_verbose_locks](https://www.percona.com/doc/percona-server/5.7/diagnostics/innodb_show_status.html#innodb_show_verbose_locks):
showed the records locked in `SHOW ENGINE INNODB STATUS`


* [NUMA support in mysqld_safe](https://www.percona.com/doc/percona-server/5.7/performance/innodb_numa_support.html#improved-numa-support)


* [innodb_kill_idle_trx](https://www.percona.com/doc/percona-server/LATEST/management/innodb_kill_idle_trx.html)
which was an alias to the `kill_idle_trx` system variable


* The [max_binlog_files](https://www.percona.com/doc/percona-server/5.7/flexibility/max_binlog_files.html#max_binlog_files) system variable

##### Deprecated Storage engine


* The TokuDB Storage Engine was [declared as deprecated](https://www.percona.com/doc/percona-server/8.0/release-notes/Percona-Server-8.0.13-3.html) in Percona Server for MySQL 8.0 and will be disabled in upcoming 8.0 versions.

> We recommend migrating to the MyRocks Storage Engine.

> For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).
