# MyRocks Server Variables

The MyRocks server variables expose configuration
of the underlying RocksDB engine.
There several ways to set these variables:


* For production deployments,
you should have all variables defined in the configuration file.


* *Dynamic* variables can be changed at runtime using the `SET` statement.


* If you want to test things out, you can set some of the variables
when starting `mysqld` using corresponding command-line options.

If a variable was not set in either the configuration file
or as a command-line option,
the default value is used.

Also, all variables can exist in one or both of the following scopes:


* *Global* scope defines how the variable affects overall server operation.


* *Session* scope defines how the variable affects operation
for individual client connections.

The following server variables are available:

| Variable Name                                                                                           |
|---------------------------------------------------------------------------------------------------------|
| [`rocksdb_access_hint_on_compaction_start`](#rocksdb_access_hint_on_compaction_start)                   |
| [`rocksdb_advise_random_on_open`](#rocksdb_advise_random_on_open)                                       |
| [`rocksdb_allow_concurrent_memtable_write`](#rocksdb_allow_concurrent_memtable_write)                   |
| [`rocksdb_allow_to_start_after_corruption`](#rocksdb_allow_to_start_after_corruption)                   |
| [`rocksdb_allow_mmap_reads`](#rocksdb_allow_mmap_reads)                                                 |
| [`rocksdb_allow_mmap_writes`](#rocksdb_allow_mmap_writes)                                               | 
| [`rocksdb_alter_column_default_inplace`](#rocksdb_alter_column_default_inplace)                         |
| [`rocksdb_base_background_compactions`](#rocksdb_base_background_compactions)                           |
| [`rocksdb_blind_delete_primary_key`](#rocksdb_blind_delete_primary_key)                                 |
| [`rocksdb_block_cache_size`](#rocksdb_block_cache_size)                                                 |
| [`rocksdb_block_restart_interval`](#rocksdb_block_restart_interval)                                     |
| [`rocksdb_block_size`](#rocksdb_block_size)                                                             |
| [`rocksdb_block_size_deviation`](#rocksdb_block_size_deviation)                                         |
| [`rocksdb_bulk_load`](#rocksdb_bulk_load)                                                               |
| [`rocksdb_bulk_load_allow_sk`](#rocksdb_bulk_load_allow_sk)                                             |
| [`rocksdb_bulk_load_allow_unsorted`](#rocksdb_bulk_load_allow_unsorted)                                 |
| [`rocksdb_bulk_load_size`](#rocksdb_bulk_load_size)                                                     |
| [`rocksdb_bytes_per_sync`](#rocksdb_bytes_per_sync)                                                     |
| [`rocksdb_cache_dump`](#rocksdb_cache_dump)                                                             |
| [`rocksdb_cache_index_and_filter_blocks`](#rocksdb_cache_index_and_filter_blocks)                       |
| [`rocksdb_checksums_pct`](#rocksdb_checksums_pct)                                                       |
| [`rocksdb_collect_sst_properties`](#rocksdb_collect_sst_properties)                                     |
| [`rocksdb_commit_in_the_middle`](#rocksdb_commit_in_the_middle)                                         |
| [`rocksdb_commit_time_batch_for_recovery`](#rocksdb_commit_time_batch_for_recovery)                     |
| [`rocksdb_compact_cf`](#rocksdb_compact_cf)                                                             |
| [`rocksdb_compaction_readahead_size`](#rocksdb_compaction_readahead_size)                               |
| [`rocksdb_compaction_sequential_deletes`](#rocksdb_compaction_sequential_deletes)                       |
| [`rocksdb_compaction_sequential_deletes_count_sd`](#rocksdb_compaction_sequential_deletes_count_sd)     |
| [`rocksdb_compaction_sequential_deletes_file_size`](#rocksdb_compaction_sequential_deletes_file_size)   |
| [`rocksdb_compaction_sequential_deletes_window`](#rocksdb_compaction_sequential_deletes_window)         |
| [`rocksdb_concurrent_prepare`](#rocksdb_concurrent_prepare)                                             |
| [`rocksdb_create_checkpoint`](#rocksdb_create_checkpoint)                                               |
| [`rocksdb_create_if_missing`](#rocksdb_create_if_missing)                                               |
| [`rocksdb_create_missing_column_families`](#rocksdb_create_missing_column_families)                     |
| [`rocksdb_datadir`](#rocksdb_datadir)                                                                   |
| [`rocksdb_db_write_buffer_size`](#rocksdb_db_write_buffer_size)                                         |
| [`rocksdb_deadlock_detect`](#rocksdb_deadlock_detect)                                                   |
| [`rocksdb_deadlock_detect_depth`](#rocksdb_deadlock_detect_depth)                                       |
| [`rocksdb_debug_optimizer_no_zero_cardinality`](#rocksdb_debug_optimizer_no_zero_cardinality)           |
| [`rocksdb_debug_ttl_ignore_pk`](#rocksdb_debug_ttl_ignore_pk)                                           |
| [`rocksdb_debug_ttl_read_filter_ts`](#rocksdb_debug_ttl_read_filter_ts)                                 |
| [`rocksdb_debug_ttl_rec_ts`](#rocksdb_debug_ttl_rec_ts)                                                 |
| [`rocksdb_debug_ttl_snapshot_ts`](#rocksdb_debug_ttl_snapshot_ts)                                       |
| [`rocksdb_default_cf_options`](#rocksdb_default_cf_options)                                             |
| [`rocksdb_delayed_write_rate`](#rocksdb_delayed_write_rate)                                             |
| [`rocksdb_delete_cf`](#rocksdb_delete_cf)                                                               |
| [`rocksdb_delete_obsolete_files_period_micros`](#rocksdb_delete_obsolete_files_period_micros)           |
| [`rocksdb_disable_file_deletions`](#rocksdb_disable_file_deletions)                                     |
| [`rocksdb_enable_bulk_load_api`](#rocksdb_enable_bulk_load_api)                                         |
| [`rocksdb_enable_insert_with_update_caching`](#rocksdb_enable_insert_with_update_caching)               |
| [`rocksdb_enable_iterate_bounds`](#rocksdb_enable_iterate_bounds)                                       |
| [`rocksdb_enable_native_partition`](#rocksdb_enable_native_partition)                                   |
| [`rocksdb_enable_pipelined_write`](#rocksdb_enable_pipelined_write)                                     |
| [`rocksdb_enable_remove_orphaned_dropped_cfs`](#rocksdb_enable_remove_orphaned_dropped_cfs)             |
| [`rocksdb_enable_ttl`](#rocksdb_enable_ttl)                                                             |
| [`rocksdb_enable_ttl_read_filtering`](#rocksdb_enable_ttl_read_filtering)                               |
| [`rocksdb_enable_thread_tracking`](#rocksdb_enable_thread_tracking)                                     |
| [`rocksdb_enable_write_thread_adaptive_yield`](#rocksdb_enable_write_thread_adaptive_yield)             |
| [`rocksdb_error_if_exists`](#rocksdb_error_if_exists)                                                   |
| [`rocksdb_error_on_suboptimal_collation`](#rocksdb_error_on_suboptimal_collation)                       |
| [`rocksdb_flush_log_at_trx_commit`](#rocksdb_flush_log_at_trx_commit)                                   |
| [`rocksdb_flush_memtable_on_analyze`](#rocksdb_flush_memtable_on_analyze)                               |
| [`rocksdb_force_compute_memtable_stats`](#rocksdb_force_compute_memtable_stats)                         |
| [`rocksdb_force_compute_memtable_stats_cachetime`](#rocksdb_force_compute_memtable_stats_cachetime)     |
| [`rocksdb_force_flush_memtable_and_lzero_now`](#rocksdb_force_flush_memtable_and_lzero_now)             |
| [`rocksdb_force_flush_memtable_now`](#rocksdb_force_flush_memtable_now)                                 |
| [`rocksdb_force_index_records_in_range`](#rocksdb_force_index_records_in_range)                         |
| [`rocksdb_hash_index_allow_collision`](#rocksdb_hash_index_allow_collision)                             |
| [`rocksdb_ignore_unknown_options`](#rocksdb_ignore_unknown_options)                                     |
| [`rocksdb_index_type`](#rocksdb_index_type)                                                             |
| [`rocksdb_info_log_level`](#rocksdb_info_log_level)                                                     |
| [`rocksdb_is_fd_close_on_exec`](#rocksdb_is_fd_close_on_exec)                                           |
| [`rocksdb_keep_log_file_num`](#rocksdb_keep_log_file_num)                                               |
| [`rocksdb_large_prefix`](#rocksdb_large_prefix)                                                         |
| [`rocksdb_lock_scanned_rows`](#rocksdb_lock_scanned_rows)                                               |
| [`rocksdb_lock_wait_timeout`](#rocksdb_lock_wait_timeout)                                               |
| [`rocksdb_log_file_time_to_roll`](#rocksdb_log_file_time_to_roll)                                       |
| [`rocksdb_manifest_preallocation_size`](#rocksdb_manifest_preallocation_size)                           |
| [`rocksdb_manual_compaction_bottommost_level`](#rocksdb_manual_compaction_bottommost_level)             |
| [`rocksdb_manual_wal_flush`](#rocksdb_manual_wal_flush)                                                 |
| [`rocksdb_master_skip_tx_api`](#rocksdb_master_skip_tx_api)                                             |
| [`rocksdb_max_background_compactions`](#rocksdb_max_background_compactions)                             |
| [`rocksdb_max_background_flushes`](#rocksdb_max_background_flushes)                                     |
| [`rocksdb_max_background_jobs`](#rocksdb_max_background_jobs)                                           |
| [`rocksdb_max_bottom_pri_background_compactions`](#rocksdb_max_bottom_pri_background_compactions)       |
| [`rocksdb_max_latest_deadlocks`](#rocksdb_max_latest_deadlocks)                                         |
| [`rocksdb_max_log_file_size`](#rocksdb_max_log_file_size)                                               |
| [`rocksdb_max_manifest_file_size`](#rocksdb_max_manifest_file_size)                                     |
| [`rocksdb_max_open_files`](#rocksdb_max_open_files)                                                     |
| [`rocksdb_max_row_locks`](#rocksdb_max_row_locks)                                                       |
| [`rocksdb_max_subcompactions`](#rocksdb_max_subcompactions)                                             |
| [`rocksdb_max_total_wal_size`](#rocksdb_max_total_wal_size)                                             |
| [`rocksdb_merge_buf_size`](#rocksdb_merge_buf_size)                                                     |
| [`rocksdb_merge_combine_read_size`](#rocksdb_merge_combine_read_size)                                   |
| [`rocksdb_merge_tmp_file_removal_delay_ms`](#rocksdb_merge_tmp_file_removal_delay_ms)                   |
| [`rocksdb_new_table_reader_for_compaction_inputs`](#rocksdb_new_table_reader_for_compaction_inputs)     |
| [`rocksdb_no_block_cache`](#rocksdb_no_block_cache)                                                     |
| [`rocksdb_no_create_column_family`](#rocksdb_no_create_column_family)                                   |
| [`rocksdb_override_cf_options`](#rocksdb_override_cf_options)                                           |
| [`rocksdb_paranoid_checks`](#rocksdb_paranoid_checks)                                                   |
| [`rocksdb_partial_index_sort_max_mem`](#rocksdb_partial_index_sort_max_mem)                             |
| [`rocksdb_pause_background_work`](#rocksdb_pause_background_work)                                       |
| [`rocksdb_perf_context_level`](#rocksdb_perf_context_level)                                             |
| [`rocksdb_persistent_cache_path`](#rocksdb_persistent_cache_path)                                       |
| [`rocksdb_persistent_cache_size_mb`](#rocksdb_persistent_cache_size_mb)                                 |
| [`rocksdb_pin_l0_filter_and_index_blocks_in_cache`](#rocksdb_pin_l0_filter_and_index_blocks_in_cache)   |
| [`rocksdb_print_snapshot_conflict_queries`](#rocksdb_print_snapshot_conflict_queries)                   |
| [`rocksdb_rate_limiter_bytes_per_sec`](#rocksdb_rate_limiter_bytes_per_sec)                             |
| [`rocksdb_read_free_rpl`](#rocksdb_read_free_rpl)                                                       |
| [`rocksdb_read_free_rpl_tables`](#rocksdb_read_free_rpl_tables)                                         |
| [`rocksdb_records_in_range`](#rocksdb_records_in_range)                                                 |
| [`rocksdb_reset_stats`](#rocksdb_reset_stats)                                                           |
| [`rocksdb_rollback_on_timeout`](#rocksdb_rollback_on_timeout)                                           |
| [`rocksdb_rpl_skip_tx_api`](#rocksdb_rpl_skip_tx_api)                                                   |
| [`rocksdb_seconds_between_stat_computes`](#rocksdb_seconds_between_stat_computes)                       |
| [`rocksdb_signal_drop_index_thread`](#rocksdb_signal_drop_index_thread)                                 |
| [`rocksdb_sim_cache_size`](#rocksdb_sim_cache_size)                                                     |
| [`rocksdb_skip_bloom_filter_on_read`](#rocksdb_skip_bloom_filter_on_read)                               |
| [`rocksdb_skip_fill_cache`](#rocksdb_skip_fill_cache)                                                   |
| [`rocksdb_skip_locks_if_skip_unique_check`](#rocksdb_skip_locks_if_skip_unique_check)                   |
| [`rocksdb_sst_mgr_rate_bytes_per_sec`](#rocksdb_sst_mgr_rate_bytes_per_sec)                             |
| [`rocksdb_stats_dump_period_sec`](#rocksdb_stats_dump_period_sec)                                       |
| [`rocksdb_stats_level`](#rocksdb_stats_level)                                                           |
| [`rocksdb_stats_recalc_rate`](#rocksdb_stats_recalc_rate)                                               |
| [`rocksdb_store_row_debug_checksums`](#rocksdb_store_row_debug_checksums)                               |
| [`rocksdb_strict_collation_check`](#rocksdb_strict_collation_check)                                     |
| [`rocksdb_strict_collation_exceptions`](#rocksdb_strict_collation_exceptions)                           |
| [`rocksdb_table_cache_numshardbits`](#rocksdb_table_cache_numshardbits)                                 |
| [`rocksdb_table_stats_background_thread_nice_value`](#rocksdb_table_stats_background_thread_nice_value) |
| [`rocksdb_table_stats_max_num_rows_scanned`](#rocksdb_table_stats_max_num_rows_scanned)                 |
| [`rocksdb_table_stats_recalc_threshold_count`](#rocksdb_table_stats_recalc_threshold_count)             |
| [`rocksdb_table_stats_recalc_threshold_pct`](#rocksdb_table_stats_recalc_threshold_pct)                 |
| [`rocksdb_table_stats_sampling_pct`](#rocksdb_table_stats_sampling_pct)                                 |
| [`rocksdb_table_stats_use_table_scan`](#rocksdb_table_stats_use_table_scan)                             |
| [`rocksdb_tmpdir`](#rocksdb_tmpdir)                                                                     |
| [`rocksdb_two_write_queues`](#rocksdb_two_write_queues)                                                 |
| [`rocksdb_trace_block_cache_access`](#rocksdb_trace_block_cache_access)                                 |
| [`rocksdb_trace_queries`](#rocksdb_trace_queries)                                                       |
| [`rocksdb_trace_sst_api`](#rocksdb_trace_sst_api)                                                       |
| [`rocksdb_track_and_verify_wals_in_manifest`](#rocksdb_track_and_verify_wals_in_manifest)               |
| [`rocksdb_unsafe_for_binlog`](#rocksdb_unsafe_for_binlog)                                               |
| [`rocksdb_update_cf_options`](#rocksdb_update_cf_options)                                               |
| [`rocksdb_use_adaptive_mutex`](#rocksdb_use_adaptive_mutex)                                             |
| [`rocksdb_use_default_sk_cf`](#rocksdb_use_default_sk_cf)                                               |
| [`rocksdb_use_direct_io_for_flush_and_compaction`](#rocksdb_use_direct_io_for_flush_and_compaction)     |
| [`rocksdb_use_direct_reads`](#rocksdb_use_direct_reads)                                                 |
| [`rocksdb_use_fsync`](#rocksdb_use_fsync)                                                               |
| [`rocksdb_validate_tables`](#rocksdb_validate_tables)                                                   |
| [`rocksdb_verify_row_debug_checksums`](#rocksdb_verify_row_debug_checksums)                             |
| [`rocksdb_wal_bytes_per_sync`](#rocksdb_wal_bytes_per_sync)                                             |
| [`rocksdb_wal_dir`](#rocksdb_wal_dir)                                                                   |
| [`rocksdb_wal_recovery_mode`](#rocksdb_wal_recovery_mode)                                               |
| [`rocksdb_wal_size_limit_mb`](#rocksdb_wal_size_limit_mb)                                               |
| [`rocksdb_wal_ttl_seconds`](#rocksdb_wal_ttl_seconds)                                                   |
| [`rocksdb_whole_key_filtering`](#rocksdb_whole_key_filtering)                                           |
| [`rocksdb_write_batch_max_bytes`](#rocksdb_write_batch_max_bytes)                                       |
| [`rocksdb_write_disable_wal`](#rocksdb_write_disable_wal)                                               |
| [`rocksdb_write_ignore_missing_column_families`](#rocksdb_write_ignore_missing_column_families)         |
| [`rocksdb_write_policy`](#rocksdb_write_policy)                                                         |

### `rocksdb_access_hint_on_compaction_start`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb-access-hint-on-compaction-start |
| Dynamic      | No                                        |
| Scope        | Global                                    |
| Data type    | String or numeric                         |
| Default      | NORMAL or 1                               |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the file access pattern once compaction is started, and applied to all input files of compaction.
Possible values are:


* `0` = `NONE`


* `1` = `NORMAL` (default)


* `2` = `SEQUENTIAL`


* `3` = `WILLNEED`

### `rocksdb_advise_random_on_open`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-advise-random-on-open |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | Boolean                         |
| Default      | ON                              |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to hint at the underlying file system
that the file access pattern is random,
when a data file is opened.
Enabled by default.

### `rocksdb_allow_concurrent_memtable_write`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb-allow-concurrent-memtable-write |
| Dynamic      | No                                        |
| Scope        | Global                                    |
| Data type    | Boolean                                   |
| Default      | OFF                                       |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to allow multiple writers to update memtables in parallel.
Disabled by default.

### `rocksdb_allow_to_start_after_corruption`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb_allow_to_start_after_corruption |
| Dynamic      | No                                        |
| Scope        | Global                                    |
| Data type    | Boolean                                   |
| Default      | OFF                                       |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to allow the server to restart once MyRocks reported data corruption. Disabled by default.

Once corruption is detected server writes a marker file (named
ROCKSDB_CORRUPTED) in the data directory and aborts. If a marker file exists,
then mysqld exits on startup with an error message. The restart failure will
continue until the problem is solved or until mysqld is started with this
variable turned on in the command line.

!!! note

    Not all memtables support concurrent writes.

### `rocksdb_allow_mmap_reads`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-allow-mmap-reads |
| Dynamic      | No                         |
| Scope        | Global                     |
| Data type    | Boolean                    |
| Default      | OFF                        |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to allow the OS to map a data file into memory for reads. Disabled by default. If you enable this, make sure that rocksdb_use_direct_reads is disabled.

### `rocksdb_allow_mmap_writes`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-allow-mmap-writes |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Boolean                     |
| Default      | OFF                         |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to allow the OS to map a data file into memory for writes. Disabled by default.

### `rocksdb_alter_column_default_inplace`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --rocksdb-alter-column-default-inplace |
| Dynamic      | Yes                                    |
| Scope        | Global                                 |
| Data type    | Boolean                                |
| Default      | ON                                     |


The variable has been implemented in Percona Server for MySQL 5.7.35-38. Allow inplace alter for the alter column default operation.

### `rocksdb_base_background_compactions`

| Option       | Description                           |
|--------------|---------------------------------------|
| Command-line | --rocksdb-base-background-compactions |
| Dynamic      | No                                    |
| Scope        | Global                                |
| Data type    | Numeric                               |
| Default      | 1                                     |


The variable has been implemented in Percona Server 5.7.19-17. This variable has been replaced in Percona Server 5.7.20-18
by rocksdb_max_background_jobs, which automatically decides how
many threads to allocate towards flush/compaction. Specifies the suggested number of concurrent background compaction jobs, submitted to the default LOW priority thread pool in RocksDB.
Default is `1`.
The allowed range of values is from `-1` to `64`.
Maximum depends on the rocksdb_max_background_compactions variable.

### `rocksdb_blind_delete_primary_key`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-blind-delete-primary-key |
| Dynamic      | Yes                                |
| Scope        | Global, Session                    |
| Data type    | Boolean                            |
| Default      | OFF                                |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Skips verifying if rows exist before executing deletes. The following conditions must be met:


* The variable is enabled


* Only a single table is listed in the `DELETE` statement


* The table has only a primary key with no secondary keys

### `rocksdb_block_cache_size`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-block-cache-size |
| Dynamic      | No                         |
| Scope        | Global                     |
| Data type    | Numeric                    |
| Default      | 536870912                  |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the size of the LRU block cache for RocksDB. This memory is reserved for the block cache, which is in addition to any filesystem caching that may occur.

The minimum value is `1024` because that’s the size of one block.

The default value is `536870912`.

The maximum value is `9223372036854775807`.

### `rocksdb_block_restart_interval`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-block-restart-interval |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Numeric                          |
| Default      | 16                               |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the number of keys for each set of delta encoded data.
The default value is `16`.
The allowed range is from `1` to `2147483647`.

### `rocksdb_block_size`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-block-size |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Numeric              |
| Default      | 4096                 |

The variable has been implemented in Percona Server 5.7.19-17. The minimum value has changed from `0` to `1024` in Percona Server 5.7.20-18. This variable specifies the size of the data block for reading RocksDB data files.
The default value is `4096`.
The allowed range is from `1024` to `18446744073709551615`.

### `rocksdb_block_size_deviation`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-block-size-deviation |
| Dynamic      | No                             |
| Scope        | Global                         |
| Data type    | Numeric                        |
| Default      | 10                             |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the threshold for free space allowed in a data block (see rocksdb_block_size).
If there is less space remaining,
close the block (and write to new block).
Default value is `10`, meaning that the block is not closed
until there is less than 10 bits of free space remaining.

The allowed range is from `1` to `2147483647`.

### `rocksdb_bulk_load_allow_sk`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-bulk-load-allow-sk |
| Dynamic      | Yes                          |
| Scope        | Global, Session              |
| Data type    | Boolean                      |
| Default      | OFF                          |


The variable has been implemented in Percona Server 5.7.23-23. Enabling this variable allows secondary keys to be added using the bulk loading
feature. This variable can be toggled only when the bulk load is disabled, for example,
when rocksdb_bulk_load is `OFF`.

### `rocksdb_bulk_load_allow_unsorted`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-bulk-load-allow-unsorted |
| Dynamic      | Yes                                |
| Scope        | Global, Session                    |
| Data type    | Boolean                            |
| Default      | OFF                                |


The variable has been implemented in Percona Server 5.7.20-18. By default, the bulk loader requires its input to be sorted in the primary key order. If enabled, unsorted inputs are allowed too, which are then
sorted by the bulkloader itself, at a performance penalty.

### `rocksdb_bulk_load`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb-bulk-load |
| Dynamic      | Yes                 |
| Scope        | Global, Session     |
| Data type    | Boolean             |
| Default      | OFF                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to use bulk load:
MyRocks will ignore checking keys for uniqueness
or acquiring locks during transactions.
Disabled by default.
Enable this only if you are certain that there are no row conflicts,
for example, when setting up a new MyRocks instance from a MySQL dump.

When the rocksdb_bulk_load variable is enabled, it behaves as if the variable rocksdb_commit_in_the_middle is enabled, even if the variable rocksdb_commit_in_the_middle is disabled.

### `rocksdb_bulk_load_size`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-bulk-load-size |
| Dynamic      | Yes                      |
| Scope        | Global, Session          |
| Data type    | Numeric                  |
| Default      | 1000                     |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the number of keys to accumulate
before committing them to the storage engine when the bulk load is enabled
(see rocksdb_bulk_load).
The default value is `1000`,
which means that a batch can contain up to 1000 records
before they are implicitly committed.
The allowed range is from `1` to `1073741824`.

### `rocksdb_bytes_per_sync`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-bytes-per-sync |
| Dynamic      | Yes                      |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 0                        |

The variable has been implemented in Percona Server 5.7.19-17 and changed to dynamic in Percona Server 5.7.21-20. Specifies how often should the OS sync files to disk
as they are being written, asynchronously, in the background.
This operation can be used to smooth out write I/O over time.
The default value is `0` meaning that files are never synced.
The allowed range is up to `18446744073709551615`.

### `rocksdb_cache_dump`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-cache-dump |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Boolean              |
| Default      | ON                   |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Includes RocksDB block cache content in a core dump. This variable is enabled by default.

### `rocksdb_cache_index_and_filter_blocks`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-cache-index-and-filter-blocks |
| Dynamic      | No                                      |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | ON                                      |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether RocksDB should use the block cache for caching the index and bloomfilter data blocks from each data file.
Enabled by default.
If you disable this feature, RocksDB will allocate additional memory to maintain these data blocks.

### `rocksdb_checksums_pct`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-checksums-pct |
| Dynamic      | Yes                     |
| Scope        | Global, Session         |
| Data type    | Numeric                 |
| Default      | 100                     |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the percentage of rows to be checksummed.
The default value is `100` (checksum all rows).
The allowed range is from `0` to `100`.

### `rocksdb_collect_sst_properties`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-collect-sst-properties |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | ON                               |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to collect statistics on each data file
to improve optimizer behavior.
Enabled by default.

### `rocksdb_commit_in_the_middle`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-commit-in-the-middle |
| Dynamic      | Yes                            |
| Scope        | Global                         |
| Data type    | Boolean                        |
| Default      | OFF                            |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to commit rows implicitly when a batch contains more than the value of rocksdb_bulk_load_size.

This variable is disabled by default.

When the rocksdb_bulk_load variable is enabled, it behaves as if the variable rocksdb_commit_in_the_middle is enabled, even if the variable rocksdb_commit_in_the_middle is disabled.

### `rocksdb_commit_time_batch_for_recovery`

| Option       | Description                              |
|--------------|------------------------------------------|
| Command-line | --rocksdb-commit-time-batch-for-recovery |
| Dynamic      | Yes                                      |
| Scope        | Global, Session                          |
| Data type    | Boolean                                  |
| Default      | OFF                                      |

The variable has been implemented in Percona Server 5.7.23-23. Specifies whether to write the commit time write batch into the database or not.

!!! note

    If the commit time write batch is only useful for recovery, then writing to WAL is enough.

### `rocksdb_compact_cf`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-compact-cf |
| Dynamic      | Yes                  |
| Scope        | Global               |
| Data type    | String               |
| Default      |                      |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the name of the column family to compact.

### `rocksdb_compaction_readahead_size`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-compaction-readahead-size |
| Dynamic      | Yes                                 |
| Scope        | Global                              |
| Data type    | Numeric                             |
| Default      | 0                                   |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the size of reads to perform ahead of compaction.
The default value is `0`.
Set this to at least 2 megabytes (`16777216`)
when using MyRocks with spinning disks
to ensure sequential reads instead of random.
The maximum allowed value is `18446744073709551615`.

!!! note

    If you set this variable to a non-zero value, rocksdb_new_table_reader_for_compaction_inputs is enabled.

### `rocksdb_compaction_sequential_deletes`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Numeric                                 |
| Default      | 0                                       |
                                                                                         
The variable has been implemented in Percona Server 5.7.19-17. Specifies the threshold to trigger compaction on a file
if it has more than this number of sequential delete markers.
The default value is `0` meaning that compaction is not triggered
regardless of the number of delete markers.
The maximum allowed value is `2000000` (two million delete markers).

!!! note

    Depending on workload patterns, MyRocks can potentially maintain large numbers of delete markers, which increases the latency of queries. This compaction feature will reduce latency, but may also increase the MyRocks write rate. Use this variable together with rocksdb_compaction_sequential_deletes_file_size to only perform compaction on large files.

### `rocksdb_compaction_sequential_deletes_count_sd`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes-count-sd |
| Dynamic      | Yes                                              |
| Scope        | Global                                           |
| Data type    | Boolean                                          |
| Default      | OFF                                              |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to count single deletes as delete markers recognized by rocksdb_compaction_sequential_deletes.
Disabled by default.

### `rocksdb_compaction_sequential_deletes_file_size`

| Option       | Description                                       |
|--------------|---------------------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes-file-size |
| Dynamic      | Yes                                               |
| Scope        | Global                                            |
| Data type    | Numeric                                           |
| Default      | 0                                                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the minimum file size required to trigger compaction on it by rocksdb_compaction_sequential_deletes.
The default value is `0`, meaning that compaction is triggered regardless of file size.
The allowed range is from `-1` to `9223372036854775807`.

### `rocksdb_compaction_sequential_deletes_window`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes-window |
| Dynamic      | Yes                                            |
| Scope        | Global                                         |
| Data type    | Numeric                                        |
| Default      | 0                                              |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the size of the window for counting delete markers by rocksdb_compaction_sequential_deletes.
The default value is `0`.
The allowed range is up to `2000000` (two million).

### `rocksdb_concurrent_prepare`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-concurrent_prepare |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Boolean                      |
| Default      | ON                           |

The variable has been deprecated in the *Percona Server for MySQL* 5.7.21-20, as it has been renamed upstream to `rocksdb_two_write_queues`.

The variable has been implemented in Percona Server 5.7.20-18. When enabled this variable allows/encourages threads that are using two-phase commit to `prepare` in parallel. 

### `rocksdb_create_checkpoint`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-create-checkpoint |
| Dynamic      | Yes                         |
| Scope        | Global                      |
| Data type    | String                      |
| Default      |                             |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the directory where MyRocks should create a checkpoint. Empty by default.

### `rocksdb_create_if_missing`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-create-if-missing |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Boolean                     |
| Default      | ON                          |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should create its database if it does not exist.
Enabled by default.

### `rocksdb_create_missing_column_families`

| Option       | Description                              |
|--------------|------------------------------------------|
| Command-line | --rocksdb-create-missing-column-families |
| Dynamic      | No                                       |
| Scope        | Global                                   |
| Data type    | Boolean                                  |
| Default      | OFF                                      |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should create new column families if they do not exist.
Disabled by default.

### `rocksdb_datadir`

| Option       | Description                              |
|--------------|------------------------------------------|
| Command-line | --rocksdb-datadir                        |
| Dynamic      | No                                       |
| Scope        | Global                                   |
| Data type    | Boolean                                  |
| Default      | OFF                                      |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the location of the MyRocks data directory.
By default, it is created in the current working directory.

### `rocksdb_db_write_buffer_size`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-db-write-buffer-size |
| Dynamic      | No                             |
| Scope        | Global                         |
| Data type    | Numeric                        |
| Default      | 0                              |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum size of all memtables used to store writes in MyRocks across all column families. When this size is reached, the data is flushed
to persistent media.
The default value is `0`.
The allowed range is up to `18446744073709551615`.

### `rocksdb_deadlock_detect`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-deadlock-detect |
| Dynamic      | Yes                       |
| Scope        | Global, Session           |
| Data type    | Boolean                   |
| Default      | OFF                       |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should detect deadlocks.
Disabled by default.

### `rocksdb_deadlock_detect_depth`

Implemented in Percona Server 5.7.20-18.

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-deadlock-detect-depth |
| Dynamic      | Yes                             |
| Scope        | Global, Session                 |
| Data type    | Numeric                         |
| Default      | 50                              |


The variable has been implemented in Percona Server 5.7.20-18. Specifies the number of transactions deadlock detection will traverse
through before assuming deadlock.

### `rocksdb_debug_optimizer_no_zero_cardinality`

| Option       | Description                                   |
|--------------|-----------------------------------------------|
| Command-line | --rocksdb-debug-optimizer-no-zero-cardinality |
| Dynamic      | Yes                                           |
| Scope        | Global                                        |
| Data type    | Boolean                                       |
| Default      | ON                                            |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should prevent zero cardinality
by always overriding it with some value.

### `rocksdb_debug_ttl_ignore_pk`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-debug-ttl-ignore-pk |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | OFF                           |

The variable has been implemented in Percona Server 5.7.20-18, for debugging purposes only. If true, compaction filtering will not occur on Primary Key TTL data. This variable is a no-op in non-debug builds.

### `rocksdb_debug_ttl_read_filter_ts`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb_debug-ttl-read-filter-ts |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 0                                  |

The variable has been implemented in Percona Server 5.7.20-18. For debugging purposes only.  Overrides the TTL read
filtering time to time + debug_ttl_read_filter_ts.
A value of `0` denotes that the variable is not set.
This variable is a no-op in non-debug builds.

### `rocksdb_debug_ttl_rec_ts`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-debug-ttl-rec-ts |
| Dynamic      | Yes                        |
| Scope        | Global                     |
| Data type    | Numeric                    |
| Default      | 0                          |

The variable has been implemented in Percona Server 5.7.20-18. For debugging purposes only.  Overrides the TTL of
records to `now()` + debug_ttl_rec_ts.
The value can be +/- to simulate a record inserted in the past vs a record
inserted in the “future”. A value of `0` denotes that the
variable is not set.
This variable is a no-op in non-debug builds.

### `rocksdb_debug_ttl_snapshot_ts`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-debug-ttl-snapshot-ts |
| Dynamic      | Yes                             |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 0                               |

The variable has been implemented in Percona Server 5.7.20-18. For debugging purposes only.  Sets the snapshot during
compaction to `now()` + rocksdb_debug_set_ttl_snapshot_ts.
The value can be +/- to simulate a snapshot in the past vs a
snapshot created in the “future”. A value of `0` denotes
that the variable is not set. This variable is a no-op in
non-debug builds.

### `rocksdb_default_cf_options`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-default-cf-options |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | String                       |
| Default      |                              |



The variable has been implemented in Percona Server 5.7.19-17. Specifies the default column family options for MyRocks.
Empty by default.

### `rocksdb_delayed_write_rate`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-delayed-write-rate |
| Dynamic      | Yes                          |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 16777216                     |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the write rate in bytes per second, which should be used if MyRocks hits a soft limit or threshold for writes.
Default value is `16777216` (16 MB/sec).
The allowed range is from `0` to `18446744073709551615`.

### `rocksdb_delete_cf`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb-delete-cf |
| Dynamic      | Yes                 |
| Scope        | Global              |
| Data type    | String              |
| Default      | “”                  |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Deletes the column family by name. The default value is “”, an empty string.

For example:

```sql
SET @@global.ROCKSDB_DELETE_CF = 'cf_primary_key';
```

### `rocksdb_delete_obsolete_files_period_micros`

| Option       | Description                                   |
|--------------|-----------------------------------------------|
| Command-line | --rocksdb-delete-obsolete-files-period-micros |
| Dynamic      | No                                            |
| Scope        | Global                                        |
| Data type    | Numeric                                       |
| Default      | 21600000000                                   |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the period in microseconds to delete obsolete files regardless of files removed during compaction.
Default value is `21600000000` (6 hours).
Allowed range is up to `9223372036854775807`.

### `rocksdb_enable_bulk_load_api`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-enable-bulk-load-api |
| Dynamic      | No                             |
| Scope        | Global                         |
| Data type    | Boolean                        |
| Default      | ON                             |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to use the `SSTFileWriter` feature for bulk loading. This feature bypasses the memtable, but requires keys to be inserted into the table in either ascending or descending order.
Enabled by default.
If disabled, bulk loading uses the normal write path via the memtable
and does not require keys to be inserted in any order.

### `rocksdb_enable_insert_with_update_caching`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --rocksdb-enable-insert-with-update-caching |
| Dynamic      | Yes                                         |
| Scope        | Global                                      |
| Data type    | Boolean                                     |
| Default      | ON                                          |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Specifies whether to enable optimization where the read is cached from a failed insertion attempt in INSERT ON DUPLICATE KEY UPDATE.

### `rocksdb_enable_iterate_bounds`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-enable-iterate-bounds |
| Dynamic      | Yes                             |
| Scope        | Global, Local                   |
| Data type    | Boolean                         |
| Default      | TRUE                            |


The variable has been implemented in Percona Server for MySQL 5.7.30-33. Enables the rocksdb iterator upper bounds and lower bounds in read options.

Implemented in Percona Server for MySQL 5.7.35-38.

### `rocksdb_enable_native_partition`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-enable-native-partition |
| Dynamic      | No                                |
| Scope        | Global                            |
| Data type    | Boolean                           |
| Default      | OFF                               |


This variable is **experimental** and should not be used in production.

This variable enables native partitioning and may be used when upgrading to 8.0.

### `rocksdb_enable_pipelined_write`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-enable-pipelined-write |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | OFF                              |

DBOptions::enable_pipelined_write for RocksDB.

The variable has been implemented in Percona Server for MySQL 5.7.35-38.

If `enable_pipelined_write` is `true`, a separate write thread is maintained for WAL write and memtable write. A write thread first enters the WAL writer queue and then the memtable writer queue. A pending thread on the WAL writer queue only waits for the previous WAL write operations but does not wait for memtable write operations. Enabling the feature may improve write throughput and reduce latency of the prepare phase of a two-phase commit.

### `rocksdb_enable_remove_orphaned_dropped_cfs`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-enable-remove-orphaned-dropped-cfs |
| Dynamic      | Yes                                          |
| Scope        | Global                                       |
| Data type    | Boolean                                      |
| Default      | TRUE                                         |


The variable has been implemented in Percona Server for MySQL 5.7.30-33. Enables the removal of dropped column families (cfs) from metadata if the cfs do not exist in the cf manager.

The default value is `TRUE`.

### `rocksdb_enable_ttl`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-enable-ttl |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Boolean              |
| Default      | ON                   |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to keep expired TTL records during compaction. Enabled by default. If disabled, expired TTL records will be dropped during compaction.

### `rocksdb_enable_ttl_read_filtering`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-enable-ttl-read-filtering |
| Dynamic      | Yes                                 |
| Scope        | Global                              |
| Data type    | Boolean                             |
| Default      | ON                                  |


The variable has been implemented in Percona Server 5.7.20-18. For tables with TTL, expired records are skipped/filtered
out during processing and in query results. Disabling
this will allow these records to be seen, but as a result,
rows may disappear in the middle of transactions as they
are dropped during compaction. **Use with caution.**

### `rocksdb_enable_thread_tracking`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-enable-thread-tracking |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | OFF                              |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to enable tracking the status of threads accessing the database.
Disabled by default.
If enabled, thread status will be available via `GetThreadList()`.

### `rocksdb_enable_write_thread_adaptive_yield`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-enable-write-thread-adaptive-yield |
| Dynamic      | No                                           |
| Scope        | Global                                       |
| Data type    | Boolean                                      |
| Default      | OFF                                          |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether the MyRocks write batch group leader
should wait up to the maximum allowed time before blocking on a mutex.
Disabled by default.
Enable it to increase throughput for concurrent workloads.

### `rocksdb_error_if_exists`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-error-if-exists |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | OFF                       |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to report an error when a database already exists.
Disabled by default.

### `rocksdb_error_on_suboptimal_collation`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-error-on-suboptimal-collation |
| Dynamic      | No                                      |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | ON                                      |

The variable has been implemented in Percona Server 5.7.23-23. Specifies whether to report an error instead of a warning if an index is created on a char field where the table has a sub-optimal collation (case
insensitive). Enabled by default.

### `rocksdb_flush_log_at_trx_commit`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-flush-log-at-trx-commit |
| Dynamic      | Yes                               |
| Scope        | Global, Session                   |
| Data type    | Numeric                           |
| Default      | 1                                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to sync on every transaction commit,
similar to [innodb_flush_log_at_trx_commit](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit).
Enabled by default, which ensures ACID compliance.

Possible values:

* `0`: Do not sync on transaction commit.
This provides better performance but may lead to data inconsistency
in case of a crash.

* `1`: Sync on every transaction commit.
This is set by default and recommended
as it ensures data consistency,
but reduces performance.

* `2`: Sync every second.

### `rocksdb_flush_memtable_on_analyze`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-flush-memtable-on-analyze |
| Dynamic      | Yes                                 |
| Scope        | Global, Session                     |
| Data type    | Boolean                             |
| Default      | ON                                  |


The variable has been implemented in Percona Server 5.7.19-17 and removed in Percona Server 5.7.21-20. Specifies whether to flush the memtable when running `ANALYZE` on a table.
Enabled by default.
This ensures accurate cardinality
by including data in the memtable for calculating stats.

### `rocksdb_force_compute_memtable_stats`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --rocksdb-force-compute-memtable-stats |
| Dynamic      | Yes                                    |
| Scope        | Global                                 |
| Data type    | Boolean                                |
| Default      | ON                                     |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether data in the memtables should be included for calculating index statistics used by the query optimizer.
Enabled by default.
This provides better accuracy but may reduce performance.

### `rocksdb_force_compute_memtable_stats_cachetime`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-force-compute-memtable-stats-cachetime |
| Dynamic      | Yes                                              |
| Scope        | Global                                           |
| Data type    | Numeric                                          |
| Default      | 60000000                                         |


The variable has been implemented in Percona Server 5.7.20-18. Specifies for how long the cached value of memtable statistics should be used instead of computing it every time during the query plan analysis.

### `rocksdb_force_flush_memtable_and_lzero_now`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-force-flush-memtable-and-lzero-now |
| Dynamic      | Yes                                          |
| Scope        | Global                                       |
| Data type    | Boolean                                      |
| Default      | OFF                                          |


The variable has been implemented in Percona Server 5.7.19-17. Works similar to force_flush_memtable_now
but also flushes all L0 files.

### `rocksdb_force_flush_memtable_now`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-force-flush-memtable-now |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Boolean                            |
| Default      | OFF                                |


The variable has been implemented in Percona Server 5.7.19-17. Forces MyRocks to immediately flush all memtables out to data files.

!!! warning

    Use with caution! Write requests will be blocked until all memtables are flushed.

### `rocksdb_force_index_records_in_range`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --rocksdb-force-index-records-in-range |
| Dynamic      | Yes                                    |
| Scope        | Global, Session                        |
| Data type    | Numeric                                |
| Default      | 1                                      |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the value used to override the number of rows
returned to query optimizer when `FORCE INDEX` is used.
The default value is `1`.
The allowed range is from `0` to `2147483647`.
Set to `0` if you do not want to override the returned value.

### `rocksdb_hash_index_allow_collision`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-hash-index-allow-collision |
| Dynamic      | No                                   |
| Scope        | Global                               |
| Data type    | Boolean                              |
| Default      | ON                                   |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether hash collisions are allowed.
Enabled by default, which uses less memory.
If disabled, the full prefix is stored to prevent hash collisions.

### `rocksdb_ignore_unknown_options`

| Option       | Description |
|--------------|-------------|
| Command-line |
| Dynamic      | No          |
| Scope        | Global      |
| Data type    | Boolean     |
| Default      | ON          |

The variable has been implemented in Percona Server 5.7.20-18. When enabled, it allows RocksDB to receive unknown options and not exit.

### `rocksdb_index_type`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-index-type |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Enum                 |
| Default      | kBinarySearch        |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the type of indexing used by MyRocks:

* `kBinarySearch`: Binary search (default).

* `kHashSearch`: Hash search.

### `rocksdb_info_log_level`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-info-log-level |
| Dynamic      | Yes                      |
| Scope        | Global                   |
| Data type    | Enum                     |
| Default      | error_level              |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the level for filtering messages written by MyRocks to the `mysqld` log.

* `debug_level`: Maximum logging (everything including debugging
log messages)

* `info_level`

* `warn_level`

* `error_level` (default)

* `fatal_level`: Minimum logging (only fatal error messages logged)

### `rocksdb_is_fd_close_on_exec`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-is-fd-close-on-exec |
| Dynamic      | No                            |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | ON                            |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether child processes should inherit open file handles.
Enabled by default.

### `rocksdb_large_prefix`

| Option       | Description            |
|--------------|------------------------|
| Command-line | --rocksdb-large-prefix |
| Dynamic      | Yes                    |
| Scope        | Global                 |
| Data type    | Boolean                |
| Default      | OFF                    |

The variable has been implemented in Percona Server 5.7.20-18. When enabled, this option allows index key prefixes longer than 767 bytes
(up to 3072 bytes). This option mirrors the [innodb_large_prefix](https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_large_prefix)
The values for rocksdb_large_prefix should be the same between
source and replica.

### `rocksdb_keep_log_file_num`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-keep-log-file-num |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 1000                        |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum number of info log files to keep.
The default value is `1000`.
The allowed range is from `1` to `18446744073709551615`.

### `rocksdb_lock_scanned_rows`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-lock-scanned-rows |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Boolean                     |
| Default      | OFF                         |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to hold the lock on rows that are scanned during `UPDATE` and not actually updated.
Disabled by default.

### `rocksdb_lock_wait_timeout`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-lock-wait-timeout |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Numeric                     |
| Default      | 1                           |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the number of seconds MyRocks should wait to acquire a row loc before aborting the request.
The default value is `1`.
The allowed range is up to `1073741824`.

### `rocksdb_log_file_time_to_roll`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-log-file-time-to-roll |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 0                               |



The variable has been implemented in Percona Server 5.7.19-17. Specifies the period (in seconds) for rotating the info log files.
The default value is `0`, meaning that the log file is not rotated.
The allowed range is up to `18446744073709551615`.

### `rocksdb_manifest_preallocation_size`

| Option       | Description                           |
|--------------|---------------------------------------|
| Command-line | --rocksdb-manifest-preallocation-size |
| Dynamic      | No                                    |
| Scope        | Global                                |
| Data type    | Numeric                               |
| Default      | 0                                     |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the number of bytes to preallocate for the MANIFEST file used by MyRocks to store information about column families, levels, active files, etc.
The default value is `0`.
The allowed range is up to `18446744073709551615`.

!!! note

    A value of `4194304` (4 MB) is reasonable to reduce random I/O on XFS.

### `rocksdb_manual_compaction_bottommost_level`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-manual-compaction-bottommost-level |
| Dynamic      | Yes                                          |
| Scope        | Global, Session                              |
| Data type    | Enum                                         |
| Default      | kForceOptimized                              |

The variable has been implemented in Percona Server for MySQL 5.7.35-38.

Option for skipping bottommost level compaction during manual compaction. The values are the following:


* `kSkip` - Skip bottommost level compaction


* `kIfHaveCompactionFilter` - Only compact the bottommost level if there is a compaction filter


* `kForce` - Always compact the bottommost level


* `kForceOptimized` - The default value. Always compact the bottommost level but in the bottommost level avoid double-compacting files created

### `rocksdb_manual_wal_flush`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-manual-wal-flush |
| Dynamic      | No                         |
| Scope        | Global                     |
| Data type    | Boolean                    |
| Default      | ON                         |

The variable has been implemented in Percona Server 5.7.20-18. This variable can be used to disable automatic/timed WAL flushing and instead rely on the application to do the flushing.

### `rocksdb_master_skip_tx_api`

| Option       | Description     |
|--------------|-----------------|
| Command-line |
| Dynamic      | Yes             |
| Scope        | Global, Session |
| Data type    | Boolean         |
| Default      | OFF             |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. When enabled, uses the WriteBatch API, which is faster. The session does not hold any lock-on-row access. This variable is not effective on replicas.

!!! note

    Due to the disabled row locks, improper use of the variable can cause data corruption or inconsistency.

### `rocksdb_max_background_compactions`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-max-background-compactions |
| Dynamic      | Yes                                  |
| Scope        | Global                               |
| Data type    | Numeric                              |
| Default      | -1                                   |

The variable has been implemented in Percona Server 5.7.19-17. This variable has been replaced in Percona Server 5.7.20-18
by rocksdb_max_background_jobs, which automatically decides how many threads to allocate towards flush/compaction. This variable has been re-implemented in Percona Server for MySQL 5.7.31-34.

Sets DBOptions:: max_background_compactions for RocksDB.
The default value is `-1`. The allowed range is up to `64`.

### `rocksdb_max_background_flushes`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-max-background-flushes |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Numeric                          |
| Default      | -1                               |

The variable has been implemented in Percona Server 5.7.19-17. This variable has been replaced in Percona Server 5.7.20-18
by rocksdb_max_background_jobs, which automatically decides how many threads to allocate towards flush/compaction. This variable has been re-implemented in Percona Server for MySQL 5.7.31-34.

Sets DBOptions:: max_background_flushes for RocksDB.
The default value is `-1`. The allowed range is up to `64`.

### `rocksdb_max_background_jobs`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-max-background-jobs |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Numeric                       |
| Default      | 2                             |

This variable has been implemented in Percona Server 5.7.20-18 to replace rocksdb_base_background_compactions,
rocksdb_max_background_compactions, and
rocksdb_max_background_flushes variables. This variable specifies
the maximum number of background jobs. It automatically decides
how many threads to allocate towards flush/compaction. It was implemented to
reduce the number of (confusing) options for users and can tweak and push the
responsibility down to RocksDB level.

### `rocksdb_max_bottom_pri_background_compactions`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --rocksdb_max_bottom_pri_background_compactions |
| Dynamic      | No                                              |
| Data type    | Unsigned integer                                |
| Default      | 0                                               |

This variable has been implemented in Percona Server for MySQL 5.7.31-34. Creates a specified number of threads, sets a lower CPU priority, and lets compactions use them. The maximum compaction concurrency is capped by `rocksdb_max_background_compactions` or `rocksdb_max_background_jobs`

The minimum value is `0` and the maximum value is `64`.

### `rocksdb_max_latest_deadlocks`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-max-latest-deadlocks |
| Dynamic      | Yes                            |
| Scope        | Global                         |
| Data type    | Numeric                        |
| Default      | 5                              |

This variable has been implemented in Percona Server 5.7.20-18. Specifies the maximum number of recent deadlocks to store.

### `rocksdb_max_log_file_size`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-max-log-file-size |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 0                           |

This variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum size for info log files,
after which the log is rotated.
The default value is `0`, meaning that only one log file is used.
The allowed range is up to `18446744073709551615`.

Also see rocksdb_log_file_time_to_roll.

### `rocksdb_max_manifest_file_size`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-manifest-log-file-size |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Numeric                          |
| Default      | 18446744073709551615             |

This variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum size of the MANIFEST data file,
after which it is rotated.
The default value is also the maximum, making it practically unlimited:
only one manifest file is used.

### `rocksdb_max_open_files`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-max-open-files |
| Dynamic      | No                       |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 1000                     |

This variable has been implemented in Percona Server 5.7.19-17. Default value has changed to `1000` in Percona Server 5.7.19-17. Specifies the maximum number of file handles opened by MyRocks.
Values in the range between `0` and `open_files_limit`
are taken as they are. If rocksdb_max_open_files value is
greater than `open_files_limit`, it will be reset to 1/2 of
`open_files_limit`, and a warning will be emitted to the `mysqld`
error log. A value of `-2` denotes auto-tuning: just sets
rocksdb_max_open_files value to 1/2 of `open_files_limit`.
Finally, `-1` means no limit, i.e. an infinite number of file handles.

!!! warning

    Setting rocksdb_max_open_files to `-1` is dangerous, as the server may quickly run out of file handles in this case.

### `rocksdb_max_row_locks`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-max-row-locks |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | Numeric                 |
| Default      | 1048576                 |

This variable has been implemented in Percona Server 5.7.19-17. The default value has changed from `1073741824` to `1048576` in Percona Server 5.7.21-21. The scope has changed to `Global` in Percona Server for MySQL 5.7.32-35. Specifies the limit on the maximum number of row locks a transaction can have before it fails.
The default value is also the maximum, making it practically unlimited:
transactions never fail due to row locks.

### `rocksdb_max_subcompactions`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-max-subcompactions |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 1                            |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum number of threads allowed for each compaction job.
A default value of `1` means no subcompactions (one thread per compaction job).
The allowed range is up to `64`.

### `rocksdb_max_total_wal_size`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-max-total-wal-size |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 0                            |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum total size of WAL (write-ahead log) files, after which memtables are flushed.
The default value is `0`: the WAL size limit is chosen dynamically.
The allowed range is up to `9223372036854775807`.

### `rocksdb_merge_buf_size`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-merge-buf-size |
| Dynamic      | Yes                      |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 67108864                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the size (in bytes) of the merge-sort buffers
used to accumulate data during secondary key creation.
New entries are written directly to the lowest level in the database,
instead of updating indexes through the memtable and L0.
These values are sorted using merge-sort,
with buffers set to 64 MB by default (`67108864`).
The allowed range is from `100` to `18446744073709551615`.

### `rocksdb_merge_combine_read_size`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-merge-combine-read-size |
| Dynamic      | Yes                               |
| Scope        | Global                            |
| Data type    | Numeric                           |
| Default      | 1073741824                        |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the size (in bytes) of the merge-combine buffer
used for the merge-sort algorithm as described in rocksdb_merge_buf_size.
The default size is 1 GB (`1073741824`).
The allowed range is from `100` to `18446744073709551615`.

### `rocksdb_merge_tmp_file_removal_delay_ms`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb_merge_tmp_file_removal_delay_ms |
| Dynamic      | Yes                                       |
| Scope        | Global, Session                           |
| Data type    | Numeric                                   |
| Default      | 0                                         |

The variable has been implemented in Percona Server 5.7.20-18. Fast secondary index creation creates merge files when needed. After finishing secondary index creation, merge files are removed. By default, the file removal
is done without any sleep, so removing GBs of merge files within <1s may
happen, which will cause trim stalls on Flash. This variable can be used to
rate limit the delay in milliseconds.

### `rocksdb_new_table_reader_for_compaction_inputs`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-new-table-reader-for-compaction-inputs |
| Dynamic      | No                                               |
| Scope        | Global                                           |
| Data type    | Boolean                                          |
| Default      | OFF                                              |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should create a new file descriptor and table reader for each compaction input.
Disabled by default.
Enabling this may increase memory consumption,
but will also allow pre-fetch options to be specified for compaction
input files without impacting table readers used for user queries.

### `rocksdb_no_block_cache`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-no-block-cache |
| Dynamic      | No                       |
| Scope        | Global                   |
| Data type    | Boolean                  |
| Default      | OFF                      |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to disable the block cache for column families.
Variable is disabled by default,
meaning that using the block cache is allowed.

### `rocksdb_no_create_column_family`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-no-create-column-family |
| Dynamic      | No                                |
| Scope        | Global                            |
| Data type    | Boolean                           |
| Default      | OFF                               |

The variable has been implemented in Percona Server 5.7.23-24. Specifies whether column families can be created implicitly via an index comment.
If this variable is set to `ON`, then column families must already exist or
must be present within the rocksdb_override_cf_options for a user to
assign and index to a column family.

### `rocksdb_override_cf_options`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-override-cf-options |
| Dynamic      | No                            |
| Scope        | Global                        |
| Data type    | String                        |
| Default      |                               |

The variable has been implemented in Percona Server 5.7.19-17. Specifies option overrides for each column family.
Empty by default.

### `rocksdb_paranoid_checks`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-paranoid-checks |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | ON                        |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should re-read the data file
as soon as it is created to verify correctness.
Enabled by default.

### `rocksdb_pause_background_work`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-pause-background-work |
| Dynamic      | Yes                             |
| Scope        | Global                          |
| Data type    | Boolean                         |
| Default      | OFF                             |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should pause all background operations.
Disabled by default. There is no practical reason for a user to ever
use this variable because it is intended as a test synchronization tool
for the MyRocks MTR test suites.

!!! warning

    If someone were to set a rocksdb_force_flush_memtable_now to
    `1` while rocksdb_pause_background_work is set to `1`,
    the client that issued the `rocksdb_force_flush_memtable_now=1` will be
    blocked indefinitely until rocksdb_pause_background_work
    is set to `0`.

### `rocksdb_perf_context_level`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-perf-context-level |
| Dynamic      | Yes                          |
| Scope        | Global, Session              |
| Data type    | Numeric                      |
| Default      | 0                            |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the level of information to capture with the Perf Context plugins.
The default value is `0`.
The allowed range is up to `5`.

| Value | Description                                                                  |
|-------|------------------------------------------------------------------------------|
| 0     | Unknown setting                                                              |
| 1     | Disable perf stats                                                           |
| 2     | Enable only count stats                                                      |
| 3     | Enable count stats and time stats except for mutexes                         |
| 4     | Enable count stats, time stats, except for wall time or CPU time for mutexes |
| 5     | Enable count and time stats                                                  |

### `rocksdb_persistent_cache_path`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-persistent-cache-path |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | String                          |
| Default      |                                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the path to the persistent cache.
Set this together with rocksdb_persistent_cache_size_mb.

### `rocksdb_persistent_cache_size_mb`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-persistent-cache-size-mb |
| Dynamic      | No                                 |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 0                                  |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the size of the persistent cache in megabytes.
Default is `0` (persistent cache disabled).
The allowed range is up to `18446744073709551615`.
Set this together with rocksdb_persistent_cache_path.

### `rocksdb_pin_l0_filter_and_index_blocks_in_cache`

| Option       | Description                                       |
|--------------|---------------------------------------------------|
| Command-line | --rocksdb-pin-l0-filter-and-index-blocks-in-cache |
| Dynamic      | No                                                |
| Scope        | Global                                            |
| Data type    | Boolean                                           |
| Default      | ON                                                |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks pins the filter and index blocks in the cache
if rocksdb_cache_index_and_filter_blocks is enabled.
Enabled by default.

### `rocksdb_print_snapshot_conflict_queries`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb-print-snapshot-conflict-queries |
| Dynamic      | Yes                                       |
| Scope        | Global                                    |
| Data type    | Boolean                                   |
| Default      | OFF                                       |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether queries that generate snapshot conflicts
should be logged to the error log.
Disabled by default.

### `rocksdb_rate_limiter_bytes_per_sec`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-rate-limiter-bytes-per-sec |
| Dynamic      | Yes                                  |
| Scope        | Global                               |
| Data type    | Numeric                              |
| Default      | 0                                    |


The variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum rate at which MyRocks can write to media via memtable flushes and compaction.
The default value is `0` (the write rate is not limited).
The allowed range is up to `9223372036854775807`.

### `rocksdb_read_free_rpl`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-read-free-rpl |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | Enum                    |
| Default      | OFF                     |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. se read-free replication, which allows no row lookup during replication, on the replica.

The options are the following:


* OFF - Disables the variable


* PK_SK - Enables the variable on all tables with a primary key


* PK_ONLY - Enables the variable on tables where the only key is the primary key

### `rocksdb_read_free_rpl_tables`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-read-free-rpl-tables |
| Dynamic      | Yes                            |
| Scope        | Global, Session                |
| Data type    | String                         |
| Default      |                                |

This variable is disabled in *Percona Server for MySQL* 5.7.30-33. We recommend
that you use `rocksdb_read_free_rpl` instead of this variable.

The variable has been implemented in Percona Server 5.7.19-17 and disabled in Percona Server for MySQL 5.7.30-33. Lists tables (as a regular expression) that should use read-free replication on the replica (that is, replication without row lookups).
Empty by default.

### `rocksdb_records_in_range`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-records-in-range |
| Dynamic      | Yes                        |
| Scope        | Global, Session            |
| Data type    | Numeric                    |
| Default      | 0                          |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the value to override the result of `records_in_range()`.
The default value is `0`.
The allowed range is up to `2147483647`.

### `rocksdb_reset_stats`

| Option       | Description           |
|--------------|-----------------------|
| Command-line | --rocksdb-reset-stats |
| Dynamic      | Yes                   |
| Scope        | Global                |
| Data type    | Boolean               |
| Default      | OFF                   |

The variable has been implemented in Percona Server 5.7.19-17. Resets MyRocks internal statistics dynamically (without restarting the server).

### `rocksdb_rollback_on_timeout`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-rollback-on-timeout |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | OFF                           |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. By default, only the last statement on a transaction is rolled back. If `--rocksdb-rollback-on-timeout=ON`, a transaction timeout causes a rollback of
the entire transaction.

### `rocksdb_rpl_skip_tx_api`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-rpl-skip-tx-api |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | OFF                       |

The variable has been implemented in Percona Server 5.7.19-17 and removed in Percona Server 5.7.20-19. The variable has been re-implemented in Percona Server 5.7.21-21. Specifies whether write batches should be used for replication thread
instead of the transaction API.
Disabled by default.

There are two conditions that are necessary to
use it: row replication format and replica
operating in super read-only mode.

### `rocksdb_seconds_between_stat_computes`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-seconds-between-stat-computes |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Numeric                                 |
| Default      | 3600                                    |
                                                                                                                                
The variable has been implemented in Percona Server 5.7.19-17. Specifies the number of seconds to wait
between recomputation of table statistics for the optimizer.
During that time, only changed indexes are updated.
The default value is `3600`.
The allowed value is from `0` to `4294967295`.

### `rocksdb_signal_drop_index_thread`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-signal-drop-index-thread |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Boolean                            |
| Default      | OFF                                |

The variable has been implemented in Percona Server 5.7.19-17. Signals the MyRocks drop index thread to wake up.

### `rocksdb_sim_cache_size`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-sim-cache-size |
| Dynamic      | No                       |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 0                        |

The variable has been implemented in Percona Server 5.7.20-18. Enables the simulated cache, which allows us to figure out the hit/miss rate with a specific cache size without changing the real block cache.

### `rocksdb_skip_bloom_filter_on_read`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-skip-bloom-filter-on_read |
| Dynamic      | Yes                                 |
| Scope        | Global, Session                     |
| Data type    | Boolean                             |
| Default      | OFF                                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether bloom filters should be skipped on reads.
Disabled by default (bloom filters are not skipped).

### `rocksdb_skip_fill_cache`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-skip-fill-cache |
| Dynamic      | Yes                       |
| Scope        | Global, Session           |
| Data type    | Boolean                   |
| Default      | OFF`                      |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to skip caching data on the read requests.
Disabled by default (caching is not skipped).

### `rocksdb_skip_locks_if_skip_unique_check`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | rocksdb_skip_locks_if_skip_unique_check |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | OFF                                     |

The variable has been implemented in Percona Server for MySQL 5.7.35-38. Skips row locking when unique checks are disabled.

### `rocksdb_sst_mgr_rate_bytes_per_sec`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-sst-mgr-rate-bytes-per-sec |
| Dynamic      | Yes                                  |
| Scope        | Global                               |
| Data type    | Numeric                              |
| Default      | 0                                    |

The variable has been implemented in Percona Server 5.7.19-17. The default value has changed from `67108864` to `0` in Percona Server 5.7.20-18. Specifies the maximum rate for writing to data files.
The default value is `0`. This option is not effective on HDD.
The allowed range is from `0` to `18446744073709551615`.

### `rocksdb_stats_dump_period_sec`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-stats-dump-period-sec |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 600                             |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the period in seconds for performing a dump of the MyRocks statistics to the info log.
The default value is `600`.
The allowed range is up to `2147483647`.

### `rocksdb_stats_level`

| Option       | Description           |
|--------------|-----------------------|
| Command-line | --rocksdb-stats-level |
| Dynamic      | Yes                   |
| Scope        | Global                |
| Data type    | Numeric               |
| Default      | 0                     |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Controls the RocksDB statistics level. The default value is “0” (kExceptHistogramOrTimers), which is the fastest level. The maximum value is “4”.

### `rocksdb_stats_recalc_rate`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-stats-recalc-rate |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 0                           |

The variable has been implemented in Percona Server 5.7.23-23. Specifies the number of indexes to recalculate per second. Recalculating index statistics periodically ensures it matches the actual sum from SST files.
The default value is `0`. The allowed range is up to `4294967295`.

### `rocksdb_store_row_debug_checksums`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-store-row-debug-checksums |
| Dynamic      | Yes                                 |
| Scope        | Global                              |
| Data type    | Boolean                             |
| Default      | OFF                                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to include checksums when writing index or table records.
Disabled by default.

### `rocksdb_strict_collation_check`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-strict-collation-check |
| Dynamic      | Yes                              |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | ON                               |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to check and verify
that table indexes have proper collation settings.
Enabled by default.

### `rocksdb_strict_collation_exceptions`

| Option       | Description                           |
|--------------|---------------------------------------|
| Command-line | --rocksdb-strict-collation-exceptions |
| Dynamic      | Yes                                   |
| Scope        | Global                                |
| Data type    | String                                |
| Default      |                                       |

The variable has been implemented in Percona Server 5.7.19-17. Lists tables (as a regular expression) that should be excluded from verifying case-sensitive collation enforced by rocksdb_strict_collation_check.
Empty by default.

### `rocksdb_table_cache_numshardbits`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-table-cache-numshardbits |
| Dynamic      | No                                 |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 6                                  |

The variable has been implemented in Percona Server 5.7.19-17. Max value has been changed from `2147483647` to `19` in Percona Server 5.7.20-18. Specifies the number of table caches.
The default value is `6`.
The allowed range is from `0` to `19`.

### `rocksdb_table_stats_background_thread_nice_value`

| Option       | Description                                        |
|--------------|----------------------------------------------------|
| Command-line | --rocksdb-table-stats-background-thread-nice-value |
| Dynamic      | Yes                                                |
| Scope        | Global                                             |
| Data type    | Numeric                                            |
| Default      | 19                                                 |

The variable has been implemented in Percona Server for MySQL 5.7.30-33.
The nice value for index stats.
The minimum = -20 (THREAD_PRIO_MIN)
The maximum = 19 (THREAD_PRIO_MAX)

### `rocksdb_table_stats_max_num_rows_scanned`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --rocksdb-table-stats-max-num-rows-scanned |
| Dynamic      | Yes                                        |
| Scope        | Global                                     |
| Data type    | Numeric                                    |
| Default      | 0                                          |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. The maximum number of rows to scan in a table scan is based on a cardinality calculation.
The minimum is `0` (every modification triggers a stats recalculation).
The maximum is `18,446,744,073,709,551,615`.

### `rocksdb_table_stats_recalc_threshold_count`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-table-stats-recalc-threshold-count |
| Dynamic      | Yes                                          |
| Scope        | Global                                       |
| Data type    | Numeric                                      |
| Default      | 100                                          |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. The number of modified rows to trigger a stats recalculation. This is a dependent variable for stats recalculation.
The minimum is `0`.
The maximum is `18,446,744,073,709,551,615`.

### `rocksdb_table_stats_recalc_threshold_pct`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --rocksdb-table-stats-recalc-threshold-pct |
| Dynamic      | Yes                                        |
| Scope        | Global                                     |
| Data type    | Numeric                                    |
| Default      | 10                                         |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. The percentage of the number of modified rows over the total number of rows to trigger stats recalculations. This is a dependent variable for stats
recalculation.
The minimum value is `0`
The maximum value is `100` (RDB_TBL_STATS_RECALC_THRESHOLD_PCT_MAX).

### `rocksdb_table_stats_sampling_pct`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-table-stats-sampling-pct |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 10                                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the percentage of entries to sample
when collecting statistics about table properties.
The default value is `10`.
The allowed range is from `0` to `100`.

### `rocksdb_table_stats_use_table_scan`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-table-stats-use-table-scan |
| Dynamic      | Yes                                  |
| Scope        | Global                               |
| Data type    | Boolean                              |
| Default      | FALSE                                |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Enables table-scan-based index calculations.
The default value is `FALSE`.

### `rocksdb_tmpdir`

| Option       | Description      |
|--------------|------------------|
| Command-line | --rocksdb-tmpdir |
| Dynamic      | Yes              |
| Scope        | Global, Session  |
| Data type    | String           |
| Default      |                  |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the path to the directory for temporary files during DDL operations.

### `rocksdb_trace_block_cache_access`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-trace-block-cache-access |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | String                             |
| Default      | &quot;&quot;                       |

The variable has been implemented in Percona Server for MySQL 5.7.30-33. Defines the block cache trace option string. The format is “sampling frequency: max_trace_file_size:trace_file_name.” The
sampling frequency value and max_trace_file_size value
are positive integers. The block accesses are saved to
the `rocksdb_datadir/block_cache_traces/trace_file_name`.
The default value is an empty string (&quot;&quot;).

### `rocksdb_trace_queries`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-trace-queries |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | String                  |
| Default      | &quot;&quot;            |


The variable has been implemented in Percona Server for MySQL 5.7.35-38. This variable is a trace option string. The format is `sampling_frequency:max_trace_file_size:trace_file_name`. The `sampling_frequency` value and `max_trace_file_size` value are positive integers. The queries are saved to the rocksdb_datadir/queries_traces/trace_file_name.

The file size unit is measured in bytes.

The sampling frequency specifies that one request is sampled from `sampling_frequency` requests. If the request is `1`, all the requests are traced. If the request is `5`, then for every five requests, one request is traced.

### `rocksdb_trace_sst_api`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-trace-sst-api |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | Boolean                 |
| Default      | OFF                     |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to generate trace output in the log
for each call to `SstFileWriter`.
Disabled by default.

### `rocksdb_track_and_verify_wals_in_manifest`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --rocksdb-track-and-verify-wals-in-manifest |
| Dynamic      | No                                          |
| Scope        | Global                                      |
| Data type    | Boolean                                     |
| Default      | ON                                          |

The variable has been implemented in Percona Server for MySQL 5.7.35-38.

DBOptions::track_and_verify_wals_in_manifest for RocksDB

If true, the log numbers and sizes of the synced WALs are tracked in Manifest, then, during a DB recovery, if a synced WAL is missing from the disk, or the size of the WAL does not match the recorded size in Manifest, an error is reported adn the recovery is aborted.

!!! note

    This option does not work with a secondary instance.

### `rocksdb_two_write_queues`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --rocksdb-track-and-verify-wals-in-manifest |
| Dynamic      | No                                          |
| Scope        | Global                                      |
| Data type    | Boolean                                     |
| Default      | ON                                          |

The variable has been implemented in Percona Server 5.7.21-20. When enabled this variable allows/encourages threads that are using two-phase commit to `prepare` in parallel.

### `rocksdb_unsafe_for_binlog`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-unsafe-for-binlog |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Boolean                     |
| Default      | OFF                         |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to allow statement-based binary logging
which may break consistency.
Disabled by default.

### `rocksdb_update_cf_options`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-update-cf-options |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | String                      |
| Default      |                             |

The variable has been implemented in Percona Server 5.7.19-17. Specifies option updates for each column family.
Empty by default.

### `rocksdb_use_adaptive_mutex`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-use-adaptive-mutex |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Boolean                      |
| Default      | OFF                          |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to use an adaptive mutex
which spins in user space before resorting to the kernel.
Disabled by default.

### `rocksdb_use_default_sk_cf`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-use-default-sk-cf |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Boolean                     |
| Default      | OFF                         |

The variable has been implemented in Percona Server for MySQL 5.7.32-35. Use `default_sk` column family for secondary keys.

### `rocksdb_use_direct_io_for_flush_and_compaction`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-use-direct-io-for-flush-and-compaction |
| Dynamic      | No                                               |
| Scope        | Global                                           |
| Data type    | Boolean                                          |
| Default      | OFF                                              |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to write to data files directly,
without caches or buffers.
Disabled by default.

### `rocksdb_use_direct_reads`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-use-direct-reads |
| Dynamic      | No                         |
| Scope        | Global                     |
| Data type    | Boolean                    |
| Default      | OFF                        |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to read data files directly,
without caches or buffers.
Disabled by default.
If you enable this,
make sure that rocksdb_allow_mmap_reads is disabled.

### `rocksdb_use_fsync`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb-use-fsync |
| Dynamic      | No                  |
| Scope        | Global              |
| Data type    | Boolean             |
| Default      | OFF                 |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether MyRocks should use `fsync` instead of `fdatasync` when requesting a sync of a data file.
Disabled by default.

### `rocksdb_validate_tables`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-validate-tables |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Numeric                   |
| Default      | 1                         |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to verify that MySQL `.frm` files match MyRocks tables.

* `0`: do not verify.

* `1`: verify and fail on error (default).

* `2`: verify and continue with the error.

### `rocksdb_verify_row_debug_checksums`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-verify-row-debug-checksums |
| Dynamic      | Yes                                  |
| Scope        | Global, Session                      |
| Data type    | Boolean                              |
| Default      | OFF                                  |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to verify checksums when reading index or table records.
Disabled by default.

### `rocksdb_wal_bytes_per_sync`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-wal-bytes-per-sync |
| Dynamic      | Yes                          |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 0                            |

The variable has been implemented in Percona Server 5.7.19-17. The variable has been changed to dynamic in Percona Server 5.7.21-20. Specifies how often should the OS sync WAL (write-ahead log) files to the disk
as they are being written, asynchronously, in the background.
This operation can be used to smooth out write I/O over time.
The default value is `0`, meaning that files are never synced.
The allowed range is up to `18446744073709551615`.

### `rocksdb_wal_dir`

| Option       | Description       |
|--------------|-------------------|
| Command-line | --rocksdb-wal-dir |
| Dynamic      | No                |
| Scope        | Global            |
| Data type    | String            |
| Default      |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the path to the directory where MyRocks stores WAL files.

### `rocksdb_wal_recovery_mode`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-wal-recovery-mode |
| Dynamic      | Yes                         |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 2                           |

!!! note

    In version 5.7.31-34 and later, the default is changed from `1` to `2`.

The variable has been implemented in Percona Server 5.7.19-17. Specifies the level of tolerance when recovering write-ahead logs (WAL) files
after a system crash.

The following are the options:

* `0`: if the last WAL entry is corrupted, truncate the entry and either start the server normally or refuse to start.

* `1`: if a WAL entry is corrupted, the server fails to start and does not recover from the crash.

* `2` (default): if a corrupted WAL entry is detected, truncate all entries after the detected corrupted entry. You can select this setting for replication replicas.
 
* `3`: If a corrupted WAL entry is detected, skip only the corrupted entry and continue the apply WAL entries. This option can be dangerous.

### `rocksdb_wal_size_limit_mb`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-wal-size-limit-mb |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 0                           |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the maximum size of all WAL files in megabytes
before attempting to flush memtables and delete the oldest files.
The default value is `0` (never rotated).
The allowed range is up to `9223372036854775807`.

### `rocksdb_wal_ttl_seconds`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-wal-ttl-seconds |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Numeric                   |
| Default      | 0                         |

The variable has been implemented in Percona Server 5.7.19-17. Specifies the timeout in seconds before deleting archived WAL files.
The default is `0` (WAL files are not archived).
The allowed range is up to `9223372036854775807`.

### `rocksdb_whole_key_filtering`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-whole-key-filtering |
| Dynamic      | No                            |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | ON                            |


The variable has been implemented in Percona Server 5.7.19-17. Specifies whether the bloomfilter should use the whole key for filtering instead of just the prefix.
Enabled by default.
Make sure that lookups use the whole key for matching.

### `rocksdb_write_batch_max_bytes`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-write-batch-max-bytes |
| Dynamic      | Yes                             |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 0                               |

The variable has been implemented in Percona Server 5.7.20-18. Specifies the maximum size of a RocksDB write batch in bytes. `0` means no limit. In case the user exceeds the limit following error is shown:

`ERROR HY000: Status error 10 received from RocksDB: Operation aborted: Memory
limit reached`.

### `rocksdb_write_disable_wal`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-write-disable-wal |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Boolean                     |
| Default      | OFF                         |

The variable has been implemented in Percona Server 5.7.19-17. Lets you temporarily disable the writes to WAL files,
which can be useful for bulk loading.

### `rocksdb_write_ignore_missing_column_families`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --rocksdb-write-ignore-missing-column-families |
| Dynamic      | Yes                                            |
| Scope        | Global, Session                                |
| Data type    | Boolean                                        |
| Default      | OFF                                            |

The variable has been implemented in Percona Server 5.7.19-17. Specifies whether to ignore writes to column families that do not exist.
Disabled by default (writes to non-existent column families are not ignored).

### `rocksdb_write_policy`

| Option       | Description            |
|--------------|------------------------|
| Command-line | --rocksdb-write-policy |
| Dynamic      | No                     |
| Scope        | Global                 |
| Data type    | String                 |
| Default      | write_committed        |

The variable has been implemented in Percona Server 5.7.23-23. Specifies when two-phase commit data are actually written into the database.
Allowed values are `write_committed`, `write_prepared`, and
`write_unprepared`.

Default value is `write_committed` which means data are written at commit
time. If the value is set to `write_prepared`, then data are written after
the prepare phase of a two-phase transaction. If the value is set to
`write_unprepared`, then data are written before the prepare phase.
