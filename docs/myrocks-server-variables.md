# MyRocks server variables

The MyRocks server variables expose configuration of the underlying RocksDB engine. There several ways to set these variables:

* For production deployments, you should have all variables defined in the configuration file.

* *Dynamic* variables can be changed at runtime using the `SET` statement.

* If you want to test things out, you can set some of the variables when starting `mysqld` using corresponding command-line options.

If a variable was not set in either the configuration file or as a command-line option, the default value is used.

Also, all variables can exist in one or both of the following scopes:

* *Global* scope defines how the variable affects overall server operation.

* *Session* scope defines how the variable affects operation for individual client connections.

## Variable table

| Variable Name                                                                                        |
|----------------------------------------------------------------------------------------------------------|
| [`rocksdb_access_hint_on_compaction_start`](#rocksdb_access_hint_on_compaction_start)                                                                        |
| [`rocksdb_advise_random_on_open`](#rocksdb_advise_random_on_open)                                                                        |
| [`rocksdb_allow_concurrent_memtable_write`](#rocksdb_allow_concurrent_memtable_write)                                                                        |
| [`rocksdb_allow_mmap_reads`](#rocksdb_allow_mmap_reads)                                                                        |
| [`rocksdb_allow_mmap_writes`](#rocksdb_allow_mmap_writes)                                                                        |
| [`rocksdb_allow_to_start_after_corruption`](#rocksdb_allow_to_start_after_corruption)                                                                        |
| [`rocksdb_allow_unsafe_alter`](#rocksdb_allow_unsafe_alter)                                                                        |
| [`rocksdb_alter_column_default_inplace`](#rocksdb_alter_column_default_inplace)                                                                        |
| [`rocksdb_alter_table_comment_inplace`](#rocksdb_alter_table_comment_inplace)                                                                        |
| [`rocksdb_base_background_compactions`](#rocksdb_base_background_compactions)                                                                        |
| [`rocksdb_blind_delete_primary_key`](#rocksdb_blind_delete_primary_key)                                                                        |
| [`rocksdb_block_cache_numshardbits`](#rocksdb_block_cache_numshardbits)                                                                        |
| [`rocksdb_block_cache_size`](#rocksdb_block_cache_size)                                                                        |
| [`rocksdb_block_restart_interval`](#rocksdb_block_restart_interval)                                                                        |
| [`rocksdb_block_size`](#rocksdb_block_size)                                                                        |
| [`rocksdb_block_size_deviation`](#rocksdb_block_size_deviation)                                                                        |
| [`rocksdb_bulk_load`](#rocksdb_bulk_load)                                                                        |
| [`rocksdb_bulk_load_allow_sk`](#rocksdb_bulk_load_allow_sk)                                                                        |
| [`rocksdb_bulk_load_allow_unsorted`](#rocksdb_bulk_load_allow_unsorted)                                                                        |
| [`rocksdb_bulk_load_compression_parallel_threads`](#rocksdb_bulk_load_compression_parallel_threads)                                                                        |
| [`rocksdb_bulk_load_enable_unique_key_check`](#rocksdb_bulk_load_enable_unique_key_check)                                                                        |
| [`rocksdb_bulk_load_fail_if_not_bottommost_level`](#rocksdb_bulk_load_fail_if_not_bottommost_level)                                                                        |
| [`rocksdb_bulk_load_partial_index`](#rocksdb_bulk_load_partial_index)                                                                        |
| [`rocksdb_bulk_load_size`](#rocksdb_bulk_load_size)                                                                        |
| [`rocksdb_bulk_load_use_sst_partitioner`](#rocksdb_bulk_load_use_sst_partitioner)                                                                        |
| [`rocksdb_bytes_per_sync`](#rocksdb_bytes_per_sync)                                                                        |
| [`rocksdb_cache_dump`](#rocksdb_cache_dump)                                                                        |
| [`rocksdb_cache_high_pri_pool_ratio`](#rocksdb_cache_high_pri_pool_ratio)                                                                        |
| [`rocksdb_cache_index_and_filter_blocks`](#rocksdb_cache_index_and_filter_blocks)                                                                        |
| [`rocksdb_cache_index_and_filter_with_high_priority`](#rocksdb_cache_index_and_filter_with_high_priority)                                                                        |
| [`rocksdb_cancel_manual_compactions`](#rocksdb_cancel_manual_compactions)                                                                        |
| [`rocksdb_charge_memory`](#rocksdb_charge_memory)                                                                        |
| [`rocksdb_check_iterate_bounds`](#rocksdb_check_iterate_bounds)                                                                        |
| [`rocksdb_checksums_pct`](#rocksdb_checksums_pct)                                                                        |
| [`rocksdb_collect_sst_properties`](#rocksdb_collect_sst_properties)                                                                        |
| [`rocksdb_column_default_value_as_expression`](#rocksdb_column_default_value_as_expression)                                                                        |
| [`rocksdb_commit_in_the_middle`](#rocksdb_commit_in_the_middle)                                                                        |
| [`rocksdb_commit_time_batch_for_recovery`](#rocksdb_commit_time_batch_for_recovery)                                                                        |
| [`rocksdb_compact_cf`](#rocksdb_compact_cf)                                                                        |
| [`rocksdb_compact_lzero_now`](#rocksdb_compact_lzero_now)                                                                        |
| [`rocksdb_compaction_readahead_size`](#rocksdb_compaction_readahead_size)                                                                        |
| [`rocksdb_compaction_sequential_deletes`](#rocksdb_compaction_sequential_deletes)                                                                        |
| [`rocksdb_compaction_sequential_deletes_count_sd`](#rocksdb_compaction_sequential_deletes_count_sd)                                                                        |
| [`rocksdb_compaction_sequential_deletes_file_size`](#rocksdb_compaction_sequential_deletes_file_size)                                                                        |
| [`rocksdb_compaction_sequential_deletes_window`](#rocksdb_compaction_sequential_deletes_window)                                                                        |
| [`rocksdb_concurrent_prepare`](#rocksdb_concurrent_prepare)                                                                        |
| [`rocksdb_converter_record_cached_length`](#rocksdb_converter_record_cached_length)                                                                        |
| [`rocksdb_corrupt_data_action`](#rocksdb_corrupt_data_action)                                                                        |
| [`rocksdb_create_checkpoint`](#rocksdb_create_checkpoint)                                                                        |
| [`rocksdb_create_if_missing`](#rocksdb_create_if_missing)                                                                        |
| [`rocksdb_create_missing_column_families`](#rocksdb_create_missing_column_families)                                                                        |
| [`rocksdb_create_temporary_checkpoint`](#rocksdb_create_temporary_checkpoint)                                                                        |
| [`rocksdb_datadir`](#rocksdb_datadir)                                                                        |
| [`rocksdb_db_write_buffer_size`](#rocksdb_db_write_buffer_size)                                                                        |
| [`rocksdb_deadlock_detect`](#rocksdb_deadlock_detect)                                                                        |
| [`rocksdb_deadlock_detect_depth`](#rocksdb_deadlock_detect_depth)                                                                        |
| [`rocksdb_debug_cardinality_multiplier`](#rocksdb_debug_cardinality_multiplier)                                                                        |
| [`rocksdb_debug_manual_compaction_delay`](#rocksdb_debug_manual_compaction_delay)                                                                        |
| [`rocksdb_debug_optimizer_no_zero_cardinality`](#rocksdb_debug_optimizer_no_zero_cardinality)                                                                        |
| [`rocksdb_debug_skip_bloom_filter_check_on_iterator_bounds`](#rocksdb_debug_skip_bloom_filter_check_on_iterator_bounds)                                                                        |
| [`rocksdb_debug_ttl_ignore_pk`](#rocksdb_debug_ttl_ignore_pk)                                                                        |
| [`rocksdb_debug_ttl_read_filter_ts`](#rocksdb_debug_ttl_read_filter_ts)                                                                        |
| [`rocksdb_debug_ttl_rec_ts`](#rocksdb_debug_ttl_rec_ts)                                                                        |
| [`rocksdb_debug_ttl_snapshot_ts`](#rocksdb_debug_ttl_snapshot_ts)                                                                        |
| [`rocksdb_default_cf_options`](#rocksdb_default_cf_options)                                                                        |
| [`rocksdb_delayed_write_rate`](#rocksdb_delayed_write_rate)                                                                        |
| [`rocksdb_delete_cf`](#rocksdb_delete_cf)                                                                        |
| [`rocksdb_delete_obsolete_files_period_micros`](#rocksdb_delete_obsolete_files_period_micros)                                                                        |
| [`rocksdb_disable_file_deletions`](#rocksdb_disable_file_deletions)                                                                        |
| [`rocksdb_disable_instant_ddl`](#rocksdb_disable_instant_ddl)                                                                        |
| [`rocksdb_enable_bulk_load_api`](#rocksdb_enable_bulk_load_api)                                                                        |
| [`rocksdb_enable_delete_range_for_drop_index`](#rocksdb_enable_delete_range_for_drop_index)                                                                        |
| [`rocksdb_enable_insert_with_update_caching`](#rocksdb_enable_insert_with_update_caching)                                                                        |
| [`rocksdb_enable_instant_ddl`](#rocksdb_enable_instant_ddl)                                                                        |
| [`rocksdb_enable_instant_ddl_for_append_column`](#rocksdb_enable_instant_ddl_for_append_column)                                                                        |
| [`rocksdb_enable_instant_ddl_for_column_default_changes`](#rocksdb_enable_instant_ddl_for_column_default_changes)                                                                        |
| [`rocksdb_enable_instant_ddl_for_drop_index_changes`](#rocksdb_enable_instant_ddl_for_drop_index_changes)                                                                        |
| [`rocksdb_enable_instant_ddl_for_table_comment_changes`](#rocksdb_enable_instant_ddl_for_table_comment_changes)                                                                        |
| [`rocksdb_enable_iterate_bounds`](#rocksdb_enable_iterate_bounds)                                                                        |
| [`rocksdb_enable_pipelined_write`](#rocksdb_enable_pipelined_write)                                                                        |
| [`rocksdb_enable_remove_orphaned_dropped_cfs`](#rocksdb_enable_remove_orphaned_dropped_cfs)                                                                        |
| [`rocksdb_enable_thread_tracking`](#rocksdb_enable_thread_tracking)                                                                        |
| [`rocksdb_enable_ttl`](#rocksdb_enable_ttl)                                                                        |
| [`rocksdb_enable_ttl_read_filtering`](#rocksdb_enable_ttl_read_filtering)                                                                        |
| [`rocksdb_enable_udt_in_mem`](#rocksdb_enable_udt_in_mem)                                                                        |
| [`rocksdb_enable_write_thread_adaptive_yield`](#rocksdb_enable_write_thread_adaptive_yield)                                                                        |
| [`rocksdb_error_if_exists`](#rocksdb_error_if_exists)                                                                        |
| [`rocksdb_error_on_suboptimal_collation`](#rocksdb_error_on_suboptimal_collation)                                                                        |
| [`rocksdb_file_checksums`](#rocksdb_file_checksums)                                                                        |
| [`rocksdb_flush_log_at_trx_commit`](#rocksdb_flush_log_at_trx_commit)                                                                        |
| [`rocksdb_flush_memtable_on_analyze`](#rocksdb_flush_memtable_on_analyze)                                                                        |
| [`rocksdb_force_compute_memtable_stats`](#rocksdb_force_compute_memtable_stats)                                                                        |
| [`rocksdb_force_compute_memtable_stats_cachetime`](#rocksdb_force_compute_memtable_stats_cachetime)                                                                        |
| [`rocksdb_force_flush_memtable_and_lzero_now`](#rocksdb_force_flush_memtable_and_lzero_now)                                                                        |
| [`rocksdb_force_flush_memtable_now`](#rocksdb_force_flush_memtable_now)                                                                        |
| [`rocksdb_force_index_records_in_range`](#rocksdb_force_index_records_in_range)                                                                        |
| [`rocksdb_hash_index_allow_collision`](#rocksdb_hash_index_allow_collision)                                                                        |
| [`rocksdb_ignore_unknown_options`](#rocksdb_ignore_unknown_options)                                                                        |
| [`rocksdb_index_type`](#rocksdb_index_type)                                                                        |
| [`rocksdb_info_log_level`](#rocksdb_info_log_level)                                                                        |
| [`rocksdb_invalid_create_option_action`](#rocksdb_invalid_create_option_action)                                                                        |
| [`rocksdb_io_error_action`](#rocksdb_io_error_action)                                                                        |
| [`rocksdb_is_fd_close_on_exec`](#rocksdb_is_fd_close_on_exec)                                                                        |
| [`rocksdb_keep_log_file_num`](#rocksdb_keep_log_file_num)                                                                        |
| [`rocksdb_large_prefix`](#rocksdb_large_prefix)                                                                        |
| [`rocksdb_lock_scanned_rows`](#rocksdb_lock_scanned_rows)                                                                        |
| [`rocksdb_lock_wait_timeout`](#rocksdb_lock_wait_timeout)                                                                        |
| [`rocksdb_log_file_time_to_roll`](#rocksdb_log_file_time_to_roll)                                                                        |
| [`rocksdb_manifest_preallocation_size`](#rocksdb_manifest_preallocation_size)                                                                        |
| [`rocksdb_manual_compaction_bottommost_level`](#rocksdb_manual_compaction_bottommost_level)                                                                        |
| [`rocksdb_manual_compaction_threads`](#rocksdb_manual_compaction_threads)                                                                        |
| [`rocksdb_manual_wal_flush`](#rocksdb_manual_wal_flush)                                                                        |
| [`rocksdb_master_skip_tx_api`](#rocksdb_master_skip_tx_api)                                                                        |
| [`rocksdb_max_background_compactions`](#rocksdb_max_background_compactions)                                                                        |
| [`rocksdb_max_background_flushes`](#rocksdb_max_background_flushes)                                                                        |
| [`rocksdb_max_background_jobs`](#rocksdb_max_background_jobs)                                                                        |
| [`rocksdb_max_bottom_pri_background_compactions`](#rocksdb_max_bottom_pri_background_compactions)                                                                        |
| [`rocksdb_max_compaction_history`](#rocksdb_max_compaction_history)                                                                        |
| [`rocksdb_max_file_opening_threads`](#rocksdb_max_file_opening_threads)                                                                        |
| [`rocksdb_max_latest_deadlocks`](#rocksdb_max_latest_deadlocks)                                                                        |
| [`rocksdb_max_log_file_size`](#rocksdb_max_log_file_size)                                                                        |
| [`rocksdb_max_manifest_file_size`](#rocksdb_max_manifest_file_size)                                                                        |
| [`rocksdb_max_manual_compactions`](#rocksdb_max_manual_compactions)                                                                        |
| [`rocksdb_max_open_files`](#rocksdb_max_open_files)                                                                        |
| [`rocksdb_max_row_locks`](#rocksdb_max_row_locks)                                                                        |
| [`rocksdb_max_subcompactions`](#rocksdb_max_subcompactions)                                                                        |
| [`rocksdb_max_total_wal_size`](#rocksdb_max_total_wal_size)                                                                        |
| [`rocksdb_merge_buf_size`](#rocksdb_merge_buf_size)                                                                        |
| [`rocksdb_merge_combine_read_size`](#rocksdb_merge_combine_read_size)                                                                        |
| [`rocksdb_merge_tmp_file_removal_delay_ms`](#rocksdb_merge_tmp_file_removal_delay_ms)                                                                        |
| [`rocksdb_new_table_reader_for_compaction_inputs`](#rocksdb_new_table_reader_for_compaction_inputs)                                                                        |
| [`rocksdb_no_block_cache`](#rocksdb_no_block_cache)                                                                        |
| [`rocksdb_no_create_column_family`](#rocksdb_no_create_column_family)                                                                        |
| [`rocksdb_override_cf_options`](#rocksdb_override_cf_options)                                                                        |
| [`rocksdb_paranoid_checks`](#rocksdb_paranoid_checks)                                                                        |
| [`rocksdb_partial_index_blind_delete`](#rocksdb_partial_index_blind_delete)                                                                        |
| [`rocksdb_partial_index_ignore_killed`](#rocksdb_partial_index_ignore_killed)                                                                        |
| [`rocksdb_partial_index_sort_max_mem`](#rocksdb_partial_index_sort_max_mem)                                                                        |
| [`rocksdb_pause_background_work`](#rocksdb_pause_background_work)                                                                        |
| [`rocksdb_perf_context_level`](#rocksdb_perf_context_level)                                                                        |
| [`rocksdb_persistent_cache_path`](#rocksdb_persistent_cache_path)                                                                        |
| [`rocksdb_persistent_cache_size_mb`](#rocksdb_persistent_cache_size_mb)                                                                        |
| [`rocksdb_pin_l0_filter_and_index_blocks_in_cache`](#rocksdb_pin_l0_filter_and_index_blocks_in_cache)                                                                        |
| [`rocksdb_print_snapshot_conflict_queries`](#rocksdb_print_snapshot_conflict_queries)                                                                        |
| [`rocksdb_protection_bytes_per_key`](#rocksdb_protection_bytes_per_key)                                                                        |
| [`rocksdb_rate_limiter_bytes_per_sec`](#rocksdb_rate_limiter_bytes_per_sec)                                                                        |
| [`rocksdb_read_free_rpl`](#rocksdb_read_free_rpl)                                                                        |
| [`rocksdb_read_free_rpl_tables`](#rocksdb_read_free_rpl_tables)                                                                        |
| [`rocksdb_records_in_range`](#rocksdb_records_in_range)                                                                        |
| [`rocksdb_reset_stats`](#rocksdb_reset_stats)                                                                        |
| [`rocksdb_rollback_on_timeout`](#rocksdb_rollback_on_timeout)                                                                        |
| [`rocksdb_rpl_skip_tx_api`](#rocksdb_rpl_skip_tx_api)                                                                        |
| [`rocksdb_seconds_between_stat_computes`](#rocksdb_seconds_between_stat_computes)                                                                        |
| [`rocksdb_signal_drop_index_thread`](#rocksdb_signal_drop_index_thread)                                                                        |
| [`rocksdb_sim_cache_size`](#rocksdb_sim_cache_size)                                                                        |
| [`rocksdb_skip_bloom_filter_on_read`](#rocksdb_skip_bloom_filter_on_read)                                                                        |
| [`rocksdb_skip_fill_cache`](#rocksdb_skip_fill_cache)                                                                        |
| [`rocksdb_skip_locks_if_skip_unique_check`](#rocksdb_skip_locks_if_skip_unique_check)                                                                        |
| [`rocksdb_sst_mgr_rate_bytes_per_sec`](#rocksdb_sst_mgr_rate_bytes_per_sec)                                                                        |
| [`rocksdb_stats_dump_period_sec`](#rocksdb_stats_dump_period_sec)                                                                        |
| [`rocksdb_stats_level`](#rocksdb_stats_level)                                                                        |
| [`rocksdb_stats_recalc_rate`](#rocksdb_stats_recalc_rate)                                                                        |
| [`rocksdb_store_row_debug_checksums`](#rocksdb_store_row_debug_checksums)                                                                        |
| [`rocksdb_strict_collation_check`](#rocksdb_strict_collation_check)                                                                        |
| [`rocksdb_strict_collation_exceptions`](#rocksdb_strict_collation_exceptions)                                                                        |
| [`rocksdb_table_cache_numshardbits`](#rocksdb_table_cache_numshardbits)                                                                        |
| [`rocksdb_table_stats_background_thread_nice_value`](#rocksdb_table_stats_background_thread_nice_value)                                                                        |
| [`rocksdb_table_stats_max_num_rows_scanned`](#rocksdb_table_stats_max_num_rows_scanned)                                                                        |
| [`rocksdb_table_stats_recalc_threshold_count`](#rocksdb_table_stats_recalc_threshold_count)                                                                        |
| [`rocksdb_table_stats_recalc_threshold_pct`](#rocksdb_table_stats_recalc_threshold_pct)                                                                        |
| [`rocksdb_table_stats_sampling_pct`](#rocksdb_table_stats_sampling_pct)                                                                        |
| [`rocksdb_table_stats_skip_system_cf`](#rocksdb_table_stats_skip_system_cf)                                                                        |
| [`rocksdb_table_stats_use_table_scan`](#rocksdb_table_stats_use_table_scan)                                                                        |
| [`rocksdb_tmpdir`](#rocksdb_tmpdir)                                                                        |
| [`rocksdb_trace_block_cache_access`](#rocksdb_trace_block_cache_access)                                                                        |
| [`rocksdb_trace_queries`](#rocksdb_trace_queries)                                                                        |
| [`rocksdb_trace_sst_api`](#rocksdb_trace_sst_api)                                                                        |
| [`rocksdb_track_and_verify_wals_in_manifest`](#rocksdb_track_and_verify_wals_in_manifest)                                                                        |
| [`rocksdb_two_write_queues`](#rocksdb_two_write_queues)                                                                        |
| [`rocksdb_unsafe_for_binlog`](#rocksdb_unsafe_for_binlog)                                                                        |
| [`rocksdb_update_cf_options`](#rocksdb_update_cf_options)                                                                        |
| [`rocksdb_use_adaptive_mutex`](#rocksdb_use_adaptive_mutex)                                                                        |
| [`rocksdb_use_default_sk_cf`](#rocksdb_use_default_sk_cf)                                                                        |
| [`rocksdb_use_direct_io_for_flush_and_compaction`](#rocksdb_use_direct_io_for_flush_and_compaction)                                                                        |
| [`rocksdb_use_direct_reads`](#rocksdb_use_direct_reads)                                                                        |
| [`rocksdb_use_fsync`](#rocksdb_use_fsync)                                                                        |
| [`rocksdb_use_hyper_clock_cache`](#rocksdb_use_hyper_clock_cache)                                                                        |
| [`rocksdb_use_io_uring`](#rocksdb_use_io_uring)                                                                        |
| [`rocksdb_use_write_buffer_manager`](#rocksdb_use_write_buffer_manager)                                                                        |
| [`rocksdb_validate_tables`](#rocksdb_validate_tables)                                                                        |
| [`rocksdb_verify_row_debug_checksums`](#rocksdb_verify_row_debug_checksums)                                                                        |
| [`rocksdb_wal_bytes_per_sync`](#rocksdb_wal_bytes_per_sync)                                                                        |
| [`rocksdb_wal_dir`](#rocksdb_wal_dir)                                                                        |
| [`rocksdb_wal_recovery_mode`](#rocksdb_wal_recovery_mode)                                                                        |
| [`rocksdb_wal_size_limit_mb`](#rocksdb_wal_size_limit_mb)                                                                        |
| [`rocksdb_wal_ttl_seconds`](#rocksdb_wal_ttl_seconds)                                                                        |
| [`rocksdb_whole_key_filtering`](#rocksdb_whole_key_filtering)                                                                        |
| [`rocksdb_write_batch_flush_threshold`](#rocksdb_write_batch_flush_threshold)                                                                        |
| [`rocksdb_write_batch_max_bytes`](#rocksdb_write_batch_max_bytes)                                                                        |
| [`rocksdb_write_disable_wal`](#rocksdb_write_disable_wal)                                                                        |
| [`rocksdb_write_ignore_missing_column_families`](#rocksdb_write_ignore_missing_column_families)                                                                        |
| [`rocksdb_write_policy`](#rocksdb_write_policy)                                                                        |

## Variable definitions

### `rocksdb_access_hint_on_compaction_start`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb-access-hint-on-compaction-start |
| Dynamic      | No                                        |
| Scope        | Global                                    |
| Data type    | String or numeric                         |
| Default      | NORMAL or 1                               |

**[Removed: 8.4.5-5]** As of Percona Server for MySQL 8.4.5-5, the `rocksdb-access-hint-on-compaction-start` variable has been removed.

Specifies the file access pattern once a compaction is started,
applied to all input files of a compaction.
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

Specifies whether to hint the underlying file system
that the file access pattern is random,
when a data file is opened.
Enabled by default.




### `rocksdb_allow_concurrent_memtable_write`

| Option                            | Description                                                                           |
|-----------------------------------|---------------------------------------------------------------------------------------|
| Command-line                      | --rocksdb-allow-concurrent-memtable-write                                               |
| Dynamic                           | No                                                                                    |
| Scope                             | Global                                                                                |
| Data type                         | Boolean                                                                               |
| Default                           | OFF                                                                                   |

Specifies whether to allow multiple writers to update memtables in parallel. Disabled by default.


### `rocksdb_allow_mmap_reads`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-allow-mmap-reads |
| Dynamic      | No                         |
| Scope        | Global                     |
| Data type    | Boolean                    |
| Default      | OFF                        |

Specifies whether to allow the OS to map a data file into memory for reads.
Disabled by default.
If you enable this, make sure that rocksdb_use_direct_reads is disabled.




### `rocksdb_allow_mmap_writes`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-allow-mmap-writes |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Boolean                     |
| Default      | OFF                         |

Specifies whether to allow the OS to map a data file into memory for writes.
Disabled by default.




### `rocksdb_allow_to_start_after_corruption`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb_allow_to_start_after_corruption |
| Dynamic      | No                                        |
| Scope        | Global                                    |
| Data type    | Boolean                                   |
| Default      | OFF                                       |

Specifies whether to allow server to restart once MyRocks reported data
corruption. Disabled by default.

Once corruption is detected server writes marker file (named
ROCKSDB_CORRUPTED) in the data directory and aborts. If marker file exists,
then mysqld exits on startup with an error message. The restart failure will
continue until the problem is solved or until mysqld is started with this
variable turned on in the command line.

!!! note

    Not all memtables support concurrent writes.




### `rocksdb_allow_unsafe_alter`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --rocksdb-allow-unsafe-alter           |
| Dynamic      | No                                     |
| Scope        | Global                                 |
| Data type    | Boolean                                |
| Default      | OFF                                    |

Controls crash-unsafe `INPLACE` `ADD PARTITION` and `DROP PARTITION` on partitioned MyRocks tables. The default value is `OFF`. The variable is not dynamic.

Take a verified backup before you enable `rocksdb_allow_unsafe_alter` or run `INPLACE` partition alters.

| Value | Behavior |
|-------|----------|
| `OFF` | Blocks explicit `ALGORITHM=INPLACE` for those partition operations. Without an explicit algorithm, MySQL may select a `COPY` algorithm. |
| `ON` | Permits `INPLACE` `ADD PARTITION` and `DROP PARTITION` on partitioned MyRocks tables. |

Set the variable at server startup. Add `--rocksdb-allow-unsafe-alter` on the server command line, or set `rocksdb_allow_unsafe_alter=ON` under the `[mysqld]` group in the server configuration file. Restart the server to apply the change.

Crash-unsafe does not mean the setting causes crashes. Crash-unsafe means the operation lacks atomic recovery if the server or host stops mid-operation.

Leave `rocksdb_allow_unsafe_alter` at `OFF` unless operators understand the recovery risk and hold a tested backup. Enable the variable only under the following conditions:

* The workload requires `INPLACE` `ADD PARTITION` or `DROP PARTITION` without a full table rebuild

* A tested backup exists before the alter

* Operators accept the recovery risk for the DDL window

For partition `INPLACE` limits and `DROP PARTITION` data handling, see [Partition management support](myrocks-limitations.md#partition-management-support). To recover after an interrupted `INPLACE` partition alter, see [Recover mismatched partition metadata](myrocks-limitations.md#recover-mismatched-partition-metadata).



### `rocksdb_alter_column_default_inplace`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --rocksdb-alter-column-default-inplace |
| Dynamic      | Yes                                    |
| Scope        | Global                                 |
| Data type    | Boolean                                |
| Default      | ON                                     |

Allows an inplace alter for the `ALTER COLUMN` default operation.




### `rocksdb_alter_table_comment_inplace`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --rocksdb_alter_table_comment_inplace  |
| Dynamic      | Yes                                    |
| Scope        | Global                                 |
| Data type    | Boolean                                |
| Default      | OFF                                    |

Allows changing `ALTER TABLE COMMENT` inplace.

This variable is disabled (OFF) by default.




### `rocksdb_base_background_compactions`

| Option       | Description                           |
|--------------|---------------------------------------|
| Command-line | --rocksdb-base-background-compactions |
| Dynamic      | No                                    |
| Scope        | Global                                |
| Data type    | Numeric                               |
| Default      | 1                                     |

Specifies the suggested number of concurrent background compaction jobs,
submitted to the default LOW priority thread pool in RocksDB. The default is `1`.
The allowed range of values is from `-1` to `64`. The maximum value depends on the
[rocksdb_max_background_compactions](#rocksdb_max_background_compactions) variable. This variable was
replaced with [rocksdb_max_background_jobs](#rocksdb_max_background_jobs), which automatically
decides how many threads to allocate toward flush/compaction.




### `rocksdb_blind_delete_primary_key`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-blind-delete-primary-key |
| Dynamic      | Yes                                |
| Scope        | Global, Session                    |
| Data type    | Boolean                            |
| Default      | OFF                                |

Skips verifying if rows exists before executing deletes. The following conditions must be met:

* The variable is enabled

* Only a single table listed in the `DELETE` statement

* The table has only a primary key with no secondary keys




### `rocksdb_block_cache_numshardbits`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-block-cache-numshardbits |
| Dynamic      | No                                 |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | -1                                 |

This variable specifies the number of shards ,`numShardBits`, for the block cache in RocksDB. The cache is sharded into `2^numShardBits` shards by the key hash.

The default value is `-1`. The `-1` value means that RocksDB automatically determines the number of shards for the block cache based on the cache capacity.

The minimum value is `-1` and the maximum value is `8`.




### `rocksdb_block_cache_size`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-block-cache-size |
| Dynamic      | Yes                         |
| Scope        | Global                     |
| Data type    | Numeric                    |
| Default      | 536870912                  |

Sets the RocksDB block cache size in bytes. The block cache holds uncompressed Sorted String Table (SST) data blocks in memory. Index and filter blocks also enter the cache when [`rocksdb_cache_index_and_filter_blocks`](#rocksdb_cache_index_and_filter_blocks) equals `ON`.

The operating-system page cache stores compressed SST file pages when RocksDB uses buffered reads. A miss in the block cache can still hit compressed data in the page cache. Enable [`rocksdb_use_direct_reads`](#rocksdb_use_direct_reads) to bypass the page cache. Direct reads send every block-cache miss to storage. Size the block cache larger when direct reads are enabled.

The default value is `536870912` bytes, which equals 512 megabytes (MB). The minimum value is `1024` bytes, and the maximum value is `9223372036854775807` bytes.

When the cache reaches the configured size, RocksDB evicts the blocks that queries read least recently. This policy is Least Recently Used (LRU). Enable [`rocksdb_use_hyper_clock_cache`](#rocksdb_use_hyper_clock_cache) to replace the LRU policy with HyperClockCache.

Set the size at server startup or at runtime. At startup, add `--rocksdb-block-cache-size` on the server command line, or set `rocksdb_block_cache_size` under the `[mysqld]` group in the server configuration file. The following statement sets the cache to 1073741824 bytes, which equals 1 gigabyte (GB):

```sql
SET GLOBAL rocksdb_block_cache_size = 1073741824;
```

A runtime increase raises the cache capacity. RocksDB then allocates memory as it inserts blocks. That extra allocation can exhaust host memory. A runtime decrease lowers the capacity. RocksDB then evicts entries until usage fits the new limit. The `SET GLOBAL` statement can block for several seconds during that eviction. Persist the value in the configuration file so the size remains after restart.

A small cache increases SST file reads. A large cache can exhaust host memory. On a server that also runs InnoDB, the block cache competes with `innodb_buffer_pool_size` for RAM. Keep the sum of the following allocations below physical RAM:

* `rocksdb_block_cache_size`

* `innodb_buffer_pool_size` on hybrid InnoDB and MyRocks servers

* RocksDB memtables and write buffers

* Other `mysqld` buffers and connection memory

* Operating-system page cache for compressed SST files when [`rocksdb_use_direct_reads`](#rocksdb_use_direct_reads) is `OFF`

Reduce `rocksdb_block_cache_size` or `innodb_buffer_pool_size` when that sum approaches host RAM. Disable the cache with [`rocksdb_no_block_cache`](#rocksdb_no_block_cache) when the workload does not benefit from cached blocks.

Inspect cache efficiency with [`rocksdb_block_cache_hit`](myrocks-status-variables.md#rocksdb_block_cache_hit) and [`rocksdb_block_cache_miss`](myrocks-status-variables.md#rocksdb_block_cache_miss). The following query reports current block cache usage:

```sql
SELECT STAT_TYPE, VALUE
  FROM INFORMATION_SCHEMA.ROCKSDB_DBSTATS
 WHERE STAT_TYPE = 'DB_BLOCK_CACHE_USAGE';
```

Related variables include the following:

* [`rocksdb_block_cache_numshardbits`](#rocksdb_block_cache_numshardbits)

* [`rocksdb_cache_index_and_filter_blocks`](#rocksdb_cache_index_and_filter_blocks)

* [`rocksdb_no_block_cache`](#rocksdb_no_block_cache)

* [`rocksdb_use_hyper_clock_cache`](#rocksdb_use_hyper_clock_cache)




### `rocksdb_block_restart_interval`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-block-restart-interval |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Numeric                          |
| Default      | 16                               |

Specifies the number of keys for each set of delta encoded data.
Default value is `16`.
Allowed range is from `1` to `2147483647`.




### `rocksdb_block_size`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-block-size |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Numeric              |
| Default      | 16 KB                |

Specifies the size of the data block for reading RocksDB data files.
The default value is `16 KB`.
The allowed range is from `1024` to `18446744073709551615` bytes.

#### Version changes

In Percona Server for MySQL 8.4.7-7, the maximum value remains `18446744073709551615` bytes.




### `rocksdb_block_size_deviation`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-block-size-deviation |
| Dynamic      | No                             |
| Scope        | Global                         |
| Data type    | Numeric                        |
| Default      | 10                             |

Specifies the threshold for free space allowed in a data block
(see rocksdb_block_size).
If there is less space remaining,
close the block (and write to new block).
Default value is `10`, meaning that the block is not closed
until there is less than 10 bits of free space remaining.

Allowed range is from `1` to `2147483647`.




### `rocksdb_bulk_load`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb-bulk-load |
| Dynamic      | Yes                 |
| Scope        | Global, Session     |
| Data type    | Boolean             |
| Default      | OFF                 |

Specifies whether to use bulk load:
MyRocks will ignore checking keys for uniqueness
or acquiring locks during transactions.
Disabled by default.
Enable this only if you are certain that there are no row conflicts,
for example, when setting up a new MyRocks instance from a MySQL dump.

When the `rocksdb_bulk_load` variable is enabled, it behaves as if the variable `rocksdb_commit_in_the_middle` is enabled, even if the variable `rocksdb_commit_in_the_middle` is disabled.




### `rocksdb_bulk_load_allow_sk`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-bulk-load-allow-sk |
| Dynamic      | Yes                          |
| Scope        | Global, Session              |
| Data type    | Boolean                      |
| Default      | OFF                          |

Enabling this variable allows secondary keys to be added using the bulk loading
feature. This variable can be enabled or disabled only when the rocksdb_bulk_load is `OFF`.




### `rocksdb_bulk_load_allow_unsorted`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-bulk-load-allow-unsorted |
| Dynamic      | Yes                                |
| Scope        | Global, Session                    |
| Data type    | Boolean                            |
| Default      | OFF                                |

By default, the bulk loader requires its input to be sorted in the primary
key order. If enabled, unsorted inputs are allowed too, which are then
sorted by the bulkloader itself, at a performance penalty.




### `rocksdb_bulk_load_compression_parallel_threads`

| Option         | Description                                                                |
|-----------------|----------------------------------------------------------------------------|
| Dynamic      | Yes                                                                        |
| Scope        | Global, Session                                                            |
| Data type    | Numeric                                                                    |
| Default      | 1                                                                          |
| Minimum      | 1                                                                          |
| Maximum      | 1024                                                                       |

Added in Percona Server for MySQL 8.4.5-5

Specifies the number of parallel worker threads used to compress SST data blocks during bulk load.




### `rocksdb_bulk_load_enable_unique_key_check`

| Option         | Description                                                              |
|-----------------|--------------------------------------------------------------------------|
| Dynamic      | Yes                                                                      |
| Scope        | Global, Session                                                          |
| Data type    | Bool                                                                     |
| Default      | OFF                                                                      |

Added in Percona Server for MySQL 8.4.5-5.

Controls whether the unique key constraint is checked during bulk loading.
This setting can only be changed when bulk loading is disabled.





### `rocksdb_bulk_load_fail_if_not_bottommost_level`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb_bulk_load_fail_if_not_bottommost_level |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Boolean                     |
| Default      | OFF                         |

When this variable is enabled, the bulk load fails if an sst file created during bulk load cannot be placed to the bottommost level in the rocksdb. 

This variable can be enabled or disabled only when the [`rocksdb_bulk_load`](#rocksdb_bulk_load) is `OFF`.

This variable is disabled (OFF) by default.

!!! warning

    When `rocksdb_bulk_load_fail_if_not_bottommost_level` is disabled, it may cause severe performance impact.




### `rocksdb_bulk_load_partial_index`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb-bulk-load-partial-index |
| Dynamic      | Yes                 |
| Scope        | Local               |
| Data type    | Boolean             |
| Default      | ON                  |

Materializes partial index during bulk load instead of leaving the index empty.




### `rocksdb_bulk_load_size`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-bulk-load-size |
| Dynamic      | Yes                      |
| Scope        | Global, Session          |
| Data type    | Numeric                  |
| Default      | 1000                     |

Specifies the number of keys to accumulate
before committing them to the storage engine when bulk load is enabled
(see rocksdb_bulk_load).
Default value is `1000`,
which means that a batch can contain up to 1000 records
before they are implicitly committed.
Allowed range is from `1` to `1073741824`.




### `rocksdb_bulk_load_use_sst_partitioner`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb_bulk_load_use_sst_partitioner |
| Dynamic      | Yes                 |
| Scope        | Global, Session     |
| Data type    | Boolean             |
| Default      | OFF                 |

If enabled, this variable uses sst partitioner to split sst files to ensure bulk load sst files can be ingested to bottommost level.

This variable is disabled (OFF) by default.




### `rocksdb_bytes_per_sync`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-bytes-per-sync |
| Dynamic      | Yes                      |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 0                        |

Specifies how often should the OS sync files to disk
as they are being written, asynchronously, in the background.
This operation can be used to smooth out write I/O over time.
Default value is `0` meaning that files are never synced.
Allowed range is up to `18446744073709551615`.




### `rocksdb_cache_dump`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-cache-dump |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Boolean              |
| Default      | ON                   |

Includes RocksDB block cache content in core dump. This variable is enabled by default.




### `rocksdb_cache_high_pri_pool_ratio`

| Option | Description |
|---|---|
| Command-line | --rocksdb-cache-high-pri-pool-ratio |
| Dynamic | No |
| Scope | Global |
| Data type | Double |
| Default | 0.0 |

This variable specifies the size of the block cache high-pri pool. The default value and minimum value is 0.0. The maximum value is 1.0.




### `rocksdb_cache_index_and_filter_blocks`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-cache-index-and-filter-blocks |
| Dynamic      | No                                      |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | ON                                      |

Specifies whether RocksDB should use the block cache for caching the index
and bloomfilter data blocks from each data file.
Enabled by default.
If you disable this feature, RocksDB allocates additional memory to maintain these data blocks.




### `rocksdb_cache_index_and_filter_with_high_priority`

| Option | Description |
|---|---|
| Command-line | --rocksdb-cache-index-and-filter-with-high-priority |
| Dynamic | No |
| Scope | Global |
| Data type | Boolean |
| Default | ON |

Specifies whether RocksDB should use the block cache with high priority for caching the index
and bloomfilter data blocks from each data file.
Enabled by default.
If you disable this feature, RocksDB allocates additional memory to maintain these data blocks.




### `rocksdb_cancel_manual_compactions`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-cancel-manual-compactions     |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | OFF                                     |

Cancels all ongoing manual compactions.




### `rocksdb_charge_memory`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb_charge_memory                 |
| Dynamic      | No                                      |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | OFF                                     |

This variable is [tech preview](glossary.md) and may be removed in the future releases.

Turns on RocksDB memory-charging related features (BlockBasedTableOptions::cache_usage_options.options.charged) from `cnf` files. This variable is related to [`rocksdb_use_write_buffer_manager`](#rocksdb_use_write_buffer_manager).

This variable is disabled (OFF) by default.




### `rocksdb_check_iterate_bounds`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-check-iterate-bounds |
| Dynamic      | Yes                     |
| Scope        | Global, Session         |
| Data type    | Boolean                 |
| Default      | ON                      |


This variable enables checking the upper and lower bounds of the RocksDB iterator during iteration. The default value in `ON` which means this variable is enabled.




### `rocksdb_checksums_pct`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-checksums-pct |
| Dynamic      | Yes                     |
| Scope        | Global, Session         |
| Data type    | Numeric                 |
| Default      | 100                     |

Specifies the percentage of rows to be checksummed.
Default value is `100` (checksum all rows).
Allowed range is from `0` to `100`.




### `rocksdb_collect_sst_properties`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-collect-sst-properties |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | ON                               |

Specifies whether to collect statistics on each data file
to improve optimizer behavior.
Enabled by default.




### `rocksdb_column_default_value_as_expression`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb_column_default_value_as_expression |
| Dynamic      | Yes                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | ON                               |

Allows to set a function as the default value for a column.

This variable is enabled (ON) by default.




### `rocksdb_commit_in_the_middle`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-commit-in-the-middle |
| Dynamic      | Yes                            |
| Scope        | Global                         |
| Data type    | Boolean                        |
| Default      | OFF                            |

Specifies whether to commit rows implicitly
when a batch contains more than the value of
rocksdb_bulk_load_size.

This option should only be enabled at the time of data import because it may cause locking errors.


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

Specifies whether to write the commit time write batch into the database or
not.

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

Specifies the name of the column family to compact.




### `rocksdb_compact_lzero_now`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-compact-lzero-now |
| Dynamic      | Yes                  |
| Scope        | Global               |
| Data type    | Boolean              |
| Default      | OFF                  |

This variable acts as a trigger. Set the variable to `ON`, `rocksdb-compact-lzero-now=ON`, to immediately compact all the `Level 0` (L0) files. After all the `L0` files are compacted, the variable value automatically switches to `OFF`.




### `rocksdb_compaction_readahead_size`

**[Changed in 8.4.5-5]** The default value of `rocksdb_compaction_readahead_size` has changed from `0` to `2097152`.

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-compaction-readahead-size |
| Dynamic      | Yes                                 |
| Scope        | Global                              |
| Data type    | Numeric                             |
| Default      | 2097152 (Prior to 8.4.5-5, the default was 0)                                   |

Specifies the size of reads to perform ahead of compaction.
The default value is now `2097152`.
Set this to at least 2 megabytes (`16777216`)
when using MyRocks with spinning disks
to ensure sequential reads instead of random.
Maximum allowed value is `18446744073709551615`.

!!! note

    If you set this variable to a non-zero value, rocksdb_new_table_reader_for_compaction_inputs is enabled.




### `rocksdb_compaction_sequential_deletes`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Numeric                                 |
| Default      | 149999                                  |

Specifies the threshold to trigger compaction on a file if it has more than this number of sequential delete markers.

The default value is `149999`.

Maximum allowed value is `2000000` (two million delete markers).

!!! note

    Depending on workload patterns, MyRocks can potentially maintain large
    numbers of delete markers, which increases latency of queries.  This
    compaction feature will reduce latency, but may also increase the MyRocks
    write rate.  Use this variable together with
    rocksdb_compaction_sequential_deletes_file_size to only perform
    compaction on large files.




### `rocksdb_compaction_sequential_deletes_count_sd`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes-count-sd |
| Dynamic      | Yes                                              |
| Scope        | Global                                           |
| Data type    | Boolean                                          |
| Default      | ON                                              |

Specifies whether to count single deletes as delete markers recognized by `rocksdb_compaction_sequential_deletes`.

The default value is `ON` which means the variable is enabled.




### `rocksdb_compaction_sequential_deletes_file_size`

| Option       | Description                                       |
|--------------|---------------------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes-file-size |
| Dynamic      | Yes                                               |
| Scope        | Global                                            |
| Data type    | Numeric                                           |
| Default      | 0                                                 |

Specifies the minimum file size required to trigger compaction on it
by rocksdb_compaction_sequential_deletes.
Default value is `0`,
meaning that compaction is triggered regardless of file size.
Allowed range is from `-1` to `9223372036854775807`.




### `rocksdb_compaction_sequential_deletes_window`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --rocksdb-compaction-sequential-deletes-window |
| Dynamic      | Yes                                            |
| Scope        | Global                                         |
| Data type    | Numeric                                        |
| Default      | 150000                                              |

Specifies the size of the window for counting delete markers by `rocksdb_compaction_sequential_deletes`. Default value is `150000`.

Allowed range is up to `2000000` (two million).




### `rocksdb_concurrent_prepare`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-concurrent_prepare |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Boolean                      |
| Default      | ON                           |

When enabled this variable allows/encourages threads that are using
two-phase commit to `prepare` in parallel. This variable was
renamed in upstream to rocksdb_two_write_queues.




### `rocksdb_converter_record_cached_length`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb_converter_record_cached_length |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Numeric                       |
| Default      | 0                             |

Specifies the maximum number of bytes to cache on table handler for encoding table record data. 

If the used memory exceeds `rocksdb_converter_record_cached_length`, the memory is released when the handler is returned to the table handler cache.

The minimum value is `0` (zero) that means there is no limit.
The maximum value is `UINT64_MAX (0xffffffffffffffff)`.

The default value is `0`(zero) that means there is no limit.




### `rocksdb_corrupt_data_action`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb_corrupt_data_action  |
| Dynamic      | Yes                            |
| Scope        | Global                         |
| Data type    | enum { ERROR = 0, ABORT_SERVER, WARNING }; |
| Default      | ERROR                          |

This variable controls the behavior when hitting the data corruption in MyRocks. 

You can select one of the following actions:

* `ERROR` - fail the query with the error `HA_ERR_ROCKSDB_CORRUPT_DATA`

* `ABORT_SERVER` - crash the server

* `WARNING` - pass the query with warning

The default value is `ERROR` that means the query fails with the error `HA_ERR_ROCKSDB_CORRUPT_DATA`.




### `rocksdb_create_checkpoint`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-create-checkpoint |
| Dynamic      | Yes                         |
| Scope        | Global                      |
| Data type    | String                      |
| Default      |                             |

Specifies the directory where MyRocks should create a checkpoint.
Empty by default.




### `rocksdb_create_if_missing`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-create-if-missing |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Boolean                     |
| Default      | ON                          |

Specifies whether MyRocks should create its database if it does not exist.
Enabled by default.




### `rocksdb_create_missing_column_families`

| Option       | Description                              |
|--------------|------------------------------------------|
| Command-line | --rocksdb-create-missing-column-families |
| Dynamic      | No                                       |
| Scope        | Global                                   |
| Data type    | Boolean                                  |
| Default      | OFF                                      |

Specifies whether MyRocks should create new column families
if they do not exist.
Disabled by default.




### `rocksdb_create_temporary_checkpoint`

| Option       | Description                              |
|--------------|------------------------------------------|
| Command-line | --rocksdb-create-temporary-checkpoint    |
| Dynamic      | Yes                                      |
| Scope        | Session                                  |
| Data type    | String                                   |

When specified it will create a temporary RocksDB ‘checkpoint’ or
‘snapshot’ in the datadir. If the session ends with an existing
checkpoint, or if the variable is reset to another value, the checkpoint
will get removed. This variable should be used by backup tools. Prolonged
use or other misuse can have serious side effects to the server instance.




### `rocksdb_datadir`

| Option       | Description                              |
|--------------|------------------------------------------|
| Command-line | --rocksdb-datadir                        |
| Dynamic      | No                                       |
| Scope        | Global                                   |
| Data type    | String                                   |
| Default      | `./.rocksdb`                             |

Specifies the location of the MyRocks data directory.
By default, it is created in the current working directory.




### `rocksdb_db_write_buffer_size`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-db-write-buffer-size |
| Dynamic      | No                             |
| Scope        | Global                         |
| Data type    | Numeric                        |
| Default      | 0                              |

Specifies the maximum size of all memtables used to store writes in MyRocks
across all column families. When this size is reached, the data is flushed
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

Specifies whether MyRocks should detect deadlocks.
Disabled by default.




### `rocksdb_deadlock_detect_depth`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-deadlock-detect-depth |
| Dynamic      | Yes                             |
| Scope        | Global, Session                 |
| Data type    | Numeric                         |
| Default      | 50                              |

Specifies the number of transactions deadlock detection will traverse
through before assuming deadlock.




### `rocksdb_debug_cardinality_multiplier`

| Option | Description |
|---|---|
| Command-line | --rocksdb-debug-cardinality-multiplier |
| Dynamic | Yes |
| Scope | Global |
| Data type | UINT |
| Default | 2 |

The cardinality multiplier used in tests. The minimum value is 0. The maximum value is 2147483647 (INT_MAX).

#### Version changes

In Percona Server for MySQL 8.4.7-7, the minimum value was changed to `1`.




### `rocksdb_debug_manual_compaction_delay`

| Option | Description |
|---|---|
| Command-line | --rocksdb-debug-manual-compaction-delay |
| Dynamic | Yes |
| Scope | Global |
| Data type | UINT |
| Default | 0 |

Only use this variable when debugging.

This variable specifies a sleep, in seconds, to simulate long-running compactions. The minimum value is 0. The maximum value is 4292967295 (UINT_MAX).




### `rocksdb_debug_optimizer_no_zero_cardinality`

| Option       | Description                                   |
|--------------|-----------------------------------------------|
| Command-line | --rocksdb-debug-optimizer-no-zero-cardinality |
| Dynamic      | Yes                                           |
| Scope        | Global                                        |
| Data type    | Boolean                                       |
| Default      | ON                                            |

Specifies whether MyRocks should prevent zero cardinality
by always overriding it with some value.



### `rocksdb_debug_skip_bloom_filter_check_on_iterator_bounds`

| Option                                        | Description                                                                           |
|-----------------------------------------------|---------------------------------------------------------------------------------------|
| Command-line                                  | --rocksdb-debug-skip-bloom-filter-check-on-iterator-bounds                                |
| Dynamic                                       | Yes                                                                                   |
| Scope                                         | Global                                                                                |
| Data type                                     | Boolean                                                                               |
| Default                                       | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5

Allows setting iterator bounds in RocksDB even when the query range conditions would normally enable Bloom filter usage.


### `rocksdb_debug_ttl_ignore_pk`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-debug-ttl-ignore-pk |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | OFF                           |

For debugging purposes only. If true, compaction filtering will not occur
on Primary Key TTL data. This variable is a no-op in non-debug builds.




### `rocksdb_debug_ttl_read_filter_ts`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb_debug-ttl-read-filter-ts |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 0                                  |

For debugging purposes only.  Overrides the TTL read
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

For debugging purposes only.  Overrides the TTL of
records to `now()` + debug_ttl_rec_ts.
The value can be +/- to simulate a record inserted in the past vs a record
inserted in the  future . A value of `0` denotes that the
variable is not set.
This variable is a no-op in non-debug builds.




### `rocksdb_debug_ttl_snapshot_ts`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-debug-ttl-snapshot-ts |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Numeric                       |
| Default      | 0                             |

For debugging purposes only. Sets the snapshot during
compaction to `now()` + rocksdb_debug_set_ttl_snapshot_ts.

The value can be +/- to simulate a snapshot in the past vs a
snapshot created in the  future . A value of `0` denotes
that the variable is not set. This variable is a no-op in
non-debug builds.




### `rocksdb_default_cf_options`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-default-cf-options |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | String                       |

The `rocksdb_default_cf_options` variable defines the settings for the default
column family. MyRocks stores data in this column family unless a table or
index uses a dedicated one.

#### How the option works

MyRocks does not expose every RocksDB tuning knob as a separate MySQL
variable. Instead, the server accepts a semicolon-separated list of parameters
in RocksDB shorthand and passes them to the engine.

These settings apply to every table that uses the default column family. For
example, `write_buffer_size=64M;target_file_size_base=32M` configures memtable
size and SST file size.

On startup, the server applies this option to all existing column families.
The option is read-only at runtime.

#### Which parameters are commonly tuned

The following parameters control memory, compaction, and storage behavior:

* `block_based_table_factory` — Nested settings for blocks, including Bloom
  filters, index types, and block cache behavior.

* `compression_per_level` — Compression algorithm per level, such as LZ4 or
  ZSTD, to balance CPU and disk space.

* `level0_file_num_compaction_trigger` — Number of L0 (level 0) files that
  trigger a compaction.

* `max_bytes_for_level_base` — Total size limit for level 1 of the LSM
  (Log-Structured Merge) tree. The level-1 limit influences how large
  subsequent levels become.

* `max_write_buffer_number` — Maximum number of memtables that can accumulate
  in memory, with one active and the others waiting to flush. Raising
  `max_write_buffer_number` helps absorb bursts of writes.

* `target_file_size_base` — Target size for a single SST file at level 1.
  Combined with level size limits, `target_file_size_base` affects how many
  files exist per level.

* `write_buffer_size` — Size of a single memtable. When the limit is reached,
  MyRocks freezes the memtable and schedules a flush to an SST (Sorted String
  Table) file.

#### When to tune the option

Adjusting the `rocksdb_default_cf_options` string for the hardware, such as
SSD versus HDD, is the primary way to optimize MyRocks throughput. The string
provides centralized control over compaction style, memory, and I/O
(input/output) parallelism.

The default varies by MyRocks version but balances LZ4 compression with
moderate buffer sizes, such as 64 MB memtables. The default value is:

```default
block_based_table_factory={cache_index_and_filter_blocks=1;filter_policy=bloomfilter:10:false;whole_key_filtering=1};level_compaction_dynamic_level_bytes=true;optimize_filters_for_hits=true;compaction_pri=kMinOverlappingRatio;compression=kLZ4Compression;bottommost_compression=kLZ4Compression;
```

#### What each component of the default value does

The default value combines four groups of settings:

1. Block-based table options control how data is laid out and cached inside
   SST (Sorted String Table) files:

    * `cache_index_and_filter_blocks=1` forces the index and Bloom filter
      data into the RocksDB block cache instead of pinning them outside the
      cache, for better control of total memory.

    * `filter_policy=bloomfilter:10:false` configures a Bloom filter with 10
      bits per key. The `false` value refers to `use_block_based_builder` and
      selects the modern, more efficient Full Filter format.

    * `whole_key_filtering=1` hashes the entire key in the Bloom filter for
      the fastest performance on point lookups.

2. Compaction and layout settings shape how levels grow.
   `level_compaction_dynamic_level_bytes=true` adjusts per-level byte limits
   from the bottom level, reducing space amplification and making sizing more
   self-tuning. `compaction_pri=kMinOverlappingRatio` prefers compactions that
   free the most space relative to bytes written.

3. Read optimization reduces CPU work on lookups.
   `optimize_filters_for_hits=true` skips Bloom filter checks on the
   bottommost level where hits are statistically more likely, saving CPU
   (central processing unit) time.

4. Compression settings reduce disk usage.
   `compression=kLZ4Compression` and `bottommost_compression=kLZ4Compression`
   use LZ4 for low CPU overhead and solid general-purpose compression.




### `rocksdb_delayed_write_rate`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-delayed-write-rate |
| Dynamic      | Yes                          |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 16777216                     |

Specifies the write rate in bytes per second, which should be used
if MyRocks hits a soft limit or threshold for writes.
Default value is `16777216` (16 MB/sec).
Allowed range is from `0` to `18446744073709551615`.




### `rocksdb_delete_cf`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb-delete-cf |
| Dynamic      | Yes                 |
| Scope        | Global              |
| Data type    | String              |
| Default      | “”                  |

Deletes the column family by name. The default value is “” , an empty string.

For example:

```default
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

Specifies the period in microseconds to delete obsolete files
regardless of files removed during compaction.
Default value is `21600000000` (6 hours).
Allowed range is up to `9223372036854775807`.




### `rocksdb_disable_file_deletions`

| Option       | Description                                   |
|--------------|-----------------------------------------------|
| Command-line | --rocksdb-disable-file-deletions              |
| Dynamic      | Yes                                           |
| Scope        | Session                                       |
| Data type    | Boolean                                       |
| Default      | OFF                                           |

It allows a client to temporarily disable RocksDB deletion
of old `WAL` and `.sst` files for the purposes of making a consistent
backup. If the client session terminates for any reason after disabling
deletions and has not re-enabled deletions, they will be explicitly
re-enabled. This variable should be used by backup tools. Prolonged
use or other misuse can have serious side effects to the server instance.




### `rocksdb_disable_instant_ddl`

| Option       | Description                                   |
|--------------|-----------------------------------------------|
| Command-line | --rocksdb_disable_instant_ddl                 |
| Dynamic      | Yes                                           |
| Scope        | Global                                       |
| Data type    | Boolean                                       |
| Default      | OFF                                            |

**[Deprecated: 8.4.5-5]** The `rocksdb_disable_instant_ddl` variable is deprecated and will be removed in a future version. Its default value has changed to `OFF` as of this version.

Disables Instant DDL during `ALTER TABLE` operations.

Prior to Percona Server for MySQL 8.4.5-5, this variable was enabled (`ON`) by default.




### `rocksdb_enable_bulk_load_api`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-enable-bulk-load-api |
| Dynamic      | No                             |
| Scope        | Global                         |
| Data type    | Boolean                        |
| Default      | ON                             |

Specifies whether to use the `SSTFileWriter` feature for bulk loading,
This feature bypasses the memtable,
but requires keys to be inserted into the table
in either ascending or descending order.
Enabled by default.
If disabled, bulk loading uses the normal write path via the memtable
and does not require keys to be inserted in any order.




### `rocksdb_enable_delete_range_for_drop_index`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --rocksdb_enable_delete_range_for_drop_index|
| Dynamic      | Yes                                         |
| Scope        | Global                                      |
| Data type    | Boolean                                     |
| Default      | OFF                                         |

Enables drop table / index by calling the DeleteRange.

This option is disabled (OFF) by default.




### `rocksdb_enable_insert_with_update_caching`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --rocksdb-enable-insert-with-update-caching |
| Dynamic      | Yes                                         |
| Scope        | Global                                      |
| Data type    | Boolean                                     |
| Default      | ON                                          |

Specifies whether to enable optimization where the read is cached from a failed insertion attempt in INSERT ON DUPLICATE KEY UPDATE.



### `rocksdb_enable_instant_ddl`

| Option                      | Description                                                                           |
|-----------------------------|---------------------------------------------------------------------------------------|
| Command-line                | --rocksdb-enable-instant-ddl                                                          |
| Dynamic                     | Yes                                                                                   |
| Scope                       | Global                                                                                |
| Data type                   | Boolean                                                                               |
| Default                     | ON                                                                                    |

Added in Percona Server for MySQL 8.4.5-5.

Enables Instant DDL during `ALTER TABLE` operations when possible. If set
to `OFF`, no DDL operations can be executed as instant.


### `rocksdb_enable_instant_ddl_for_append_column`

| Option                                   | Description                                                                           |
|------------------------------------------|---------------------------------------------------------------------------------------|
| Command-line                             | --rocksdb-enable-instant-ddl-for-append-column                                        |
| Dynamic                                  | Yes                                                                                   |
| Scope                                    | Global                                                                                |
| Data type                                | Boolean                                                                               |
| Default                                  | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Enables Instant DDL specifically for appending columns during `ALTER TABLE`
operations.


### `rocksdb_enable_instant_ddl_for_column_default_changes`

| Option                                        | Description                                                                           |
|-----------------------------------------------|---------------------------------------------------------------------------------------|
| Command-line                                  | --rocksdb-enable-instant-ddl-for-column-default-changes                               |
| Dynamic                                       | Yes                                                                                   |
| Scope                                         | Global                                                                                |
| Data type                                     | Boolean                                                                               |
| Default                                       | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Enables Instant DDL for changes to column defaults during `ALTER TABLE`
operations.


### `rocksdb_enable_instant_ddl_for_drop_index_changes`

| Option                                       | Description                                                                           |
|----------------------------------------------|---------------------------------------------------------------------------------------|
| Command-line                                 | --rocksdb-enable-instant-ddl-for-drop-index-changes                                   |
| Dynamic                                      | Yes                                                                                   |
| Scope                                        | Global                                                                                |
| Data type                                    | Boolean                                                                               |
| Default                                      | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Enables Instant DDL for dropping indexes during `ALTER TABLE` operations.


### `rocksdb_enable_instant_ddl_for_table_comment_changes`

| Option                                         | Description                                                                           |
|------------------------------------------------|---------------------------------------------------------------------------------------|
| Command-line                                   | --rocksdb-enable-instant-ddl-for-table-comment-changes                                |
| Dynamic                                        | Yes                                                                                   |
| Scope                                          | Global                                                                                |
| Data type                                      | Boolean                                                                               |
| Default                                        | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Enables Instant DDL for changes to table comments during `ALTER TABLE`
operations.


### `rocksdb_enable_iterate_bounds`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-enable-iterate-bounds |
| Dynamic      | Yes                             |
| Scope        | Global, Local                   |
| Data type    | Boolean                         |
| Default      | ON                              |

Enables the rocksdb iterator upper bounds and lower bounds in read options.




### `rocksdb_enable_pipelined_write`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-enable-pipelined-write |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | OFF                              |

DBOptions::enable_pipelined_write for RocksDB.

If `enable_pipelined_write` is `ON`, a separate write thread is maintained for WAL write and memtable write. A write thread first enters the WAL writer queue and then the memtable writer queue. A pending thread on the WAL writer queue only waits for the previous WAL write operations but does not wait for memtable write operations. Enabling the feature may improve write throughput and reduce latency of the prepare phase of a two-phase commit.




### `rocksdb_enable_remove_orphaned_dropped_cfs`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-enable-remove-orphaned-dropped-cfs |
| Dynamic      | Yes                                          |
| Scope        | Global                                       |
| Data type    | Boolean                                      |
| Default      | ON                                         |

Enables the removal of dropped column families (cfs) from metadata if the cfs do not exist in the cf manager.

The default value is `ON`.




### `rocksdb_enable_thread_tracking`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-enable-thread-tracking |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | OFF                              |

Specifies whether to enable tracking the status of threads
accessing the database.
Disabled by default.
If enabled, thread status will be available via `GetThreadList()`.




### `rocksdb_enable_ttl`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-enable-ttl |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Boolean              |
| Default      | ON                   |

Specifies whether to keep expired TTL records during compaction.
Enabled by default.
If disabled, expired TTL records will be dropped during compaction.




### `rocksdb_enable_ttl_read_filtering`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-enable-ttl-read-filtering |
| Dynamic      | Yes                                 |
| Scope        | Global                              |
| Data type    | Boolean                             |
| Default      | ON                                  |

For tables with TTL, expired records are skipped/filtered
out during processing and in query results. Disabling
this will allow these records to be seen, but as a result
rows may disappear in the middle of transactions as they
are dropped during compaction. **Use with caution.**



### `rocksdb_enable_udt_in_mem`

| Option                            | Description                                                                           |
|-----------------------------------|---------------------------------------------------------------------------------------|
| Command-line                      | --rocksdb-enable-udt-in-mem                                                             |
| Dynamic                           | Yes                                                                                   |
| Scope                             | Global                                                                                |
| Data type                         | Boolean                                                                               |
| Default                           | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

**[Not yet implemented.]**

Enables the user-defined timestamp in memtable feature to support Hybrid
Logical Clock (HLC) snapshot reads in MyRocks.


### `rocksdb_enable_write_thread_adaptive_yield`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-enable-write-thread-adaptive-yield |
| Dynamic      | No                                           |
| Scope        | Global                                       |
| Data type    | Boolean                                      |
| Default      | OFF                                          |

Specifies whether the MyRocks write batch group leader
should wait up to the maximum allowed time
before blocking on a mutex.
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

Specifies whether to report an error when a database already exists.
Disabled by default.




### `rocksdb_error_on_suboptimal_collation`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-error-on-suboptimal-collation |
| Dynamic      | No                                      |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | ON                                      |

Specifies whether to report an error instead of a warning if an index is
created on a char field where the table has a sub-optimal collation (case
insensitive). Enabled by default.




### `rocksdb_file_checksums`

**[Changed in 8.4.5-5]** The `rocksdb_file_checksums` variable's default value changed from `OFF` to `CHECKSUMS_OFF`, and its data type changed to `Enum= CHECKSUMS_OFF, CHECKSUMS_WRITE_ONLY, CHECKSUMS_WRITE_AND_VERIFY`.

| Option        | Description                                                                                                                               |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Command-line  | --rocksdb-file-checksums                                                                                                                  |
| Dynamic       | No                                                                                                                                        |
| Scope         | Global                                                                                                                                    |
| Data type     | Enum= CHECKSUMS_OFF, CHECKSUMS_WRITE_ONLY, CHECKSUMS_WRITE_AND_VERIFY                                                                       |
| Default       | CHECKSUMS_OFF (Prior to 8.4.5-5, the default was OFF)                                                                                      |


This variable controls whether to write and check RocksDB file-level checksums. The possible values are:

* `CHECKSUMS_OFF`: Disables checksums.

* `CHECKSUMS_WRITE_ONLY`: Writes checksums but skips verification on database open.

* `CHECKSUMS_WRITE_AND_VERIFY`: Writes checksums and verifies them when the database is opened.

Prior to Percona Server for MySQL 8.4.5-5, the default value was `OFF`, and the data type was a Boolean (where `OFF` equated to disabled).




### `rocksdb_flush_log_at_trx_commit`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-flush-log-at-trx-commit |
| Dynamic      | Yes                               |
| Scope        | Global, Session                   |
| Data type    | Numeric                           |
| Default      | 1                                 |

This variable controls whether the RocksDB Write-Ahead Log (WAL) is
synchronized to disk on every transaction commit. The behavior is similar to
[innodb_flush_log_at_trx_commit :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit).

The default value is `1`, which ensures ACID compliance. Committed
transactions remain durable after a crash. Less strict values improve
performance at the cost of durability.

#### Which value should you choose

The variable accepts the values `0`, `1`, or `2`. The following sections
describe each value, the trade-offs, and the operational outcomes.

##### Value `0`: do not sync on commit

Setting `0` does not flush or sync the WAL on commit. The setting removes
commit-time I/O, so throughput is highest and commit latency is lowest. The
trade-off is the weakest durability of the three values. After a crash,
recently committed work may be missing or the database may be inconsistent.
The risk window is wider than the roughly one-second window associated with
`2` and far beyond what `1` allows.

The setting produces the following outcomes:

* Leaves the WAL unflushed and unsynced on transaction commit.

* Minimizes commit-time I/O relative to `1` and `2`.

* Risks extensive data loss or inconsistency after a crash compared with
  stricter settings.

##### Value `1`: sync on every commit (default)

Setting `1` requires every commit to wait until the WAL is durably on disk
before the commit returns. The sync is typically a full sync such as `fsync`.
Use this value when a successful commit must survive a crash. The setting
provides the strongest durability and ACID guarantees of the three values.
The trade-off is the most synchronous disk work per commit, so commit latency
and sustained write throughput are lower than with `0` or `2` when commits
are frequent or disk sync is slow.

The setting produces the following outcomes:

* Writes and syncs the WAL to disk at each transaction commit.

* Ensures full durability and ACID compliance for committed work.

* Incurs the highest per-commit I/O and the slowest commits of the three
  values.

##### Value `2`: sync in background, typically once per second

Setting `2` writes the WAL on each commit, but the session does not wait for
the durable sync. A background thread performs syncs on a schedule, for
example about once per second. Individual commits return faster than with
`1` because they skip the per-commit sync wait. The trade-off is the possible
loss of up to one second of commits after a crash.

The setting produces the following outcomes:

* Records each commit in the WAL without blocking the commit on a full
  durable sync.

* Balances performance and durability.

* Risks the loss of up to about one second of committed transactions after a
  crash.




### `rocksdb_flush_memtable_on_analyze`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-flush-memtable-on-analyze |
| Dynamic      | Yes                                 |
| Scope        | Global, Session                     |
| Data type    | Boolean                             |
| Default      | ON                                  |

Specifies whether to flush the memtable when running `ANALYZE` on a table.
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

Specifies whether data in the memtables should be included
for calculating index statistics
used by the query optimizer.
Enabled by default.
This provides better accuracy, but may reduce performance.




### `rocksdb_force_compute_memtable_stats_cachetime`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-force-compute-memtable-stats-cachetime |
| Dynamic      | Yes                                              |
| Scope        | Global                                           |
| Data type    | Numeric                                          |
| Default      | 60000000 (60 seconds)                            |

This variable controls how long, in microseconds, MyRocks caches memtable
statistics for the query optimizer. The optimizer needs row-count estimates
to plan queries. Data not yet flushed to disk requires scanning memtables for
accurate statistics.

#### How the cache works

To avoid the CPU cost of rescanning memtables for every query, MyRocks stores
the statistics in a cache. This variable defines the expiration time for the
cached value. The default is `60000000` microseconds, or 60 seconds.

The cached value is reused on every query plan analysis until the timer
expires.

#### When to raise or lower the value

A higher value, such as several minutes, improves performance in
high-query-rate environments by reducing how often statistics collection
runs. The optimizer may use stale data if the table changes rapidly.

A lower value, such as one second, gives the optimizer a near-real-time view
of the data. The setting can yield better plans on volatile workloads, at
the cost of more CPU use during query optimization.




### `rocksdb_force_flush_memtable_and_lzero_now`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-force-flush-memtable-and-lzero-now |
| Dynamic      | Yes                                          |
| Scope        | Global                                       |
| Data type    | Boolean                                      |
| Default      | OFF                                          |

Works similar to `rocksdb_force_flush_memtable_now` but also flushes all L0 files.




### `rocksdb_force_flush_memtable_now`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-force-flush-memtable-now |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Boolean                            |
| Default      | OFF                                |

Forces MyRocks to immediately flush all memtables out to data files.

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

Specifies the value used to override the number of rows
returned to query optimizer when `FORCE INDEX` is used.
Default value is `1`.
Allowed range is from `0` to `2147483647`.
Set to `0` if you do not want to override the returned value.




### `rocksdb_hash_index_allow_collision`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-hash-index-allow-collision |
| Dynamic      | No                                   |
| Scope        | Global                               |
| Data type    | Boolean                              |
| Default      | ON                                   |

Specifies whether hash collisions are allowed.
Enabled by default, which uses less memory.
If disabled, full prefix is stored to prevent hash collisions.




### `rocksdb_ignore_unknown_options`

| Option       | Description |
|--------------|-------------|
| Command-line |             |
| Dynamic      | No          |
| Scope        | Global      |
| Data type    | Boolean     |
| Default      | ON          |

When enabled, it allows RocksDB to receive unknown options and not exit.




### `rocksdb_index_type`

| Option       | Description          |
|--------------|----------------------|
| Command-line | --rocksdb-index-type |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Enum                 |
| Default      | kBinarySearch        |

Specifies the type of indexing used by MyRocks:

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

Specifies the level for filtering messages written by MyRocks
to the `mysqld` log.

* `debug_level`: Maximum logging (everything including debugging
log messages)

* `info_level`

* `warn_level`

* `error_level` (default)

* `fatal_level`: Minimum logging (only fatal error messages logged)



### `rocksdb_invalid_create_option_action`

| Option                                | Description                                                                           |
|---------------------------------------|---------------------------------------------------------------------------------------|
| Command-line                          | --rocksdb-invalid-create-option-action                                                |
| Dynamic                               | Yes                                                                                   |
| Scope                                 | Global                                                                                |
| Data type                             | Enum: LOG, PUSH_WARNING, PUSH_ERROR                                                   |
| Default                               | LOG                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Controls the behavior when creating a table encounters an error related to
RocksDB options. You can choose to only log the error, pass the query and
give users a warning, or fail the query.


### `rocksdb_io_error_action`

| Option                      | Description                                                                           |
|-----------------------------|---------------------------------------------------------------------------------------|
| Command-line                | --rocksdb-io-error-action                                                           |
| Dynamic                     | Yes                                                                                   |
| Scope                       | Global                                                                                |
| Data type                   | Enum: ABORT_SERVER, IGNORE_ERROR                                                      |
| Default                     | ABORT_SERVER                                                                        |

Added in Percona Server for MySQL 8.4.5-5.

Controls the behavior when an I/O error occurs within RocksDB. By default,
MyRocks aborts the server and refuses to start. Setting this option to
`IGNORE_ERROR` suppresses the error instead.


### `rocksdb_is_fd_close_on_exec`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-is-fd-close-on-exec |
| Dynamic      | No                            |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | ON                            |

Specifies whether child processes should inherit open file jandles.
Enabled by default.




### `rocksdb_keep_log_file_num`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-keep-log-file-num |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 1000                        |

Specifies the maximum number of info log files to keep.
Default value is `1000`.
Allowed range is from `1` to `18446744073709551615`.




### `rocksdb_large_prefix`

| Option       | Description            |
|--------------|------------------------|
| Command-line | --rocksdb-large-prefix |
| Dynamic      | Yes                    |
| Scope        | Global                 |
| Data type    | Boolean                |
| Default      | ON                     |

**[Removed: 8.4.5-5]** As of Percona Server for MySQL 8.4.5-5, the `rocksdb_large_prefix` variable has been removed.

This variable is deprecated in `Percona Server for MySQL 8.3.0-1` and will be removed in a future release.

When enabled, this option allows index key prefixes longer than 767 bytes (up to 3072 bytes). The values for `rocksdb_large_prefix` should be the same between source and replica.


### `rocksdb_lock_scanned_rows`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-lock-scanned-rows |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Boolean                     |
| Default      | OFF                         |

Specifies whether to hold the lock on rows that are scanned during `UPDATE`
and not actually updated.
Disabled by default.




### `rocksdb_lock_wait_timeout`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-lock-wait-timeout |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Numeric                     |
| Default      | 1                           |

Specifies the number of seconds MyRocks should wait to acquire a row lock
before aborting the request.
Default value is `1`.
Allowed range is up to `1073741824`.




### `rocksdb_log_file_time_to_roll`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-log-file-time-to-roll |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 0                               |

Specifies the period (in seconds) for rotating the info log files.
Default value is `0`, meaning that the log file is not rotated.
Allowed range is up to `18446744073709551615`.




### `rocksdb_manifest_preallocation_size`

| Option       | Description                           |
|--------------|---------------------------------------|
| Command-line | --rocksdb-manifest-preallocation-size |
| Dynamic      | No                                    |
| Scope        | Global                                |
| Data type    | Numeric                               |
| Default      | 0                                     |

Specifies the number of bytes to preallocate for the MANIFEST file
used by MyRocks to store information
about column families, levels, active files, etc.
Default value is `0`.
Allowed range is up to `18446744073709551615`.

!!! note

    A value of `4194304` (4 MB) is reasonable to reduce random I/O on XFS.




### `rocksdb_manual_compaction_bottommost_level`

| Option       | Description                                  |
|--------------|----------------------------------------------|
| Command-line | --rocksdb-manual-compaction-bottommost-level |
| Dynamic      | Yes                                          |
| Scope        | Local                                        |
| Data type    | Enum                                         |
| Default      | kForceOptimized                              |

Option for bottommost level compaction during manual compaction:

* kSkip - Skip bottommost level compaction

* kIfHaveCompactionFilter - Only compact bottommost level if there is a compaction filter

* kForce - Always compact bottommost level

* kForceOptimized -  Always compact bottommost level but in bottommost level avoid double-compacting files created in the same compaction
  
### `rocksdb_manual_compaction_threads`

| Option        | Description                         |
| ------------- | ----------------------------------- |
| Command-line  | --rocksdb-manual-compaction-threads |
| Dynamic       | Yes                                 |
| Scope         | Local                               |
| Data type     | INT                                 |
| Default       | 0                                   |

The variable defines the number of RocksDB threads to run for a manual compaction. The minimum value is 0. The maximum value is 120. 




### `rocksdb_manual_wal_flush`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-manual-wal-flush |
| Dynamic      | No                         |
| Scope        | Global                     |
| Data type    | Boolean                    |
| Default      | ON                         |

This variable can be used to disable automatic/timed WAL flushing and instead
rely on the application to do the flushing.




### `rocksdb_master_skip_tx_api`

| Option       | Description     |
|--------------|-----------------|
| Command-line |                 |
| Dynamic      | Yes             |
| Scope        | Global, Session |
| Data type    | Boolean         |
| Default      | OFF             |

When enabled, uses the WriteBatch API, which is faster. The session does not hold any lock on row access. This variable is not effective on replica.

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

Sets DBOptions:: max_background_compactions for RocksDB.
The default value is `-1` The allowed range is `-1` to `64`.
This variable was replaced
by rocksdb_max_background_jobs, which automatically decides how
many threads to allocate towards flush/compaction.




### `rocksdb_max_background_flushes`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-max-background-flushes |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Numeric                          |
| Default      | -1                               |

Sets DBOptions:: max_background_flushes for RocksDB.
The default value is `-1`. The allowed range is `-1` to `64`.
This variable has been replaced
by rocksdb_max_background_jobs, which automatically decides how
many threads to allocate towards flush/compaction.




### `rocksdb_max_background_jobs`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-max-background-jobs |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Numeric                       |
| Default      | 2                             |

Limits concurrent RocksDB background jobs for memtable flushes and Sorted String Table (SST) compaction. A memtable flush writes in-memory rows to an SST file. Compaction merges SST files to reclaim space and reduce read amplification.

The default value is `2`. The minimum value is `-1`. The maximum value is `64`.

#### Slot distribution between flushes and compaction

RocksDB divides the configured jobs into flush slots and compaction slots. Flush jobs run in the HIGH-priority thread pool. Compaction jobs run in the LOW-priority thread pool. RocksDB applies the following calculation:

* Flush slots equal `rocksdb_max_background_jobs` divided by four, with a minimum of one slot. The division discards any remainder.

* Compaction slots equal `rocksdb_max_background_jobs` minus the flush slots, with a minimum of one slot.

The following table shows the resulting slots:

| `rocksdb_max_background_jobs` | Flush slots | Compaction slots |
|-------------------------------|-------------|------------------|
| `2` (default)                 | 1           | 1                |
| `4`                           | 1           | 3                |
| `8`                           | 2           | 6                |
| `16`                          | 4           | 12               |
| `32`                          | 8           | 24               |

RocksDB limits compaction to one concurrent job while write pressure remains low. RocksDB raises compaction concurrency to the full compaction slot count when the write controller detects a need to speed up compaction. A server under a light write load can therefore show a single compaction thread even with a high job limit.

#### Interaction with the replaced variables

`rocksdb_max_background_jobs` replaced [`rocksdb_base_background_compactions`](#rocksdb_base_background_compactions), [`rocksdb_max_background_compactions`](#rocksdb_max_background_compactions), and [`rocksdb_max_background_flushes`](#rocksdb_max_background_flushes). RocksDB ignores `rocksdb_base_background_compactions`.

The automatic distribution applies only when [`rocksdb_max_background_flushes`](#rocksdb_max_background_flushes) and [`rocksdb_max_background_compactions`](#rocksdb_max_background_compactions) both equal `-1`. A value other than `-1` in either variable disables the automatic distribution. RocksDB then derives the slots as follows:

* Flush slots equal `rocksdb_max_background_flushes`, with a minimum of one slot.

* Compaction slots equal `rocksdb_max_background_compactions`, with a minimum of one slot.

* The effective job total equals the sum of both variables. RocksDB substitutes one for a variable that remains at `-1`.

A value other than `-1` in either replaced variable makes `rocksdb_max_background_jobs` ineffective. Leave both replaced variables at `-1` so `rocksdb_max_background_jobs` controls the slots.

#### Configure the variable

Set the value at server startup or at runtime. At startup, add `--rocksdb-max-background-jobs` on the server command line. Or set `rocksdb_max_background_jobs` under the `[mysqld]` group in the server configuration file. The following statement sets the limit to eight jobs:

```sql
SET GLOBAL rocksdb_max_background_jobs = 8;
```

RocksDB resizes the HIGH-priority and LOW-priority thread pools after a runtime change. Persist the value in the configuration file so the limit remains after restart.

#### Size the value for the host

A low value can stall writes when memtables fill or compaction falls behind. A high value can consume CPU and storage bandwidth that query threads need.

Background jobs and client connections draw from the same CPU cores. Reserve cores for foreground queries. Keep `rocksdb_max_background_jobs` below the core count of the host. Compaction receives roughly three quarters of the jobs. Compare the compaction slot count against the intended core budget.

Select a starting value from the workload table in [Size MyRocks background jobs](myrocks-background-jobs.md). Keep the sum of client threads and `rocksdb_max_background_jobs` at or below the logical CPU thread count.

On a server that also runs InnoDB, MyRocks background jobs compete with InnoDB background threads for CPU and storage bandwidth. Size `rocksdb_max_background_jobs` together with InnoDB purge threads and page-cleaner threads.

Raise the value when write stalls persist and the host retains spare CPU and storage bandwidth. [`rocksdb_max_bottom_pri_background_compactions`](#rocksdb_max_bottom_pri_background_compactions) can add lower-priority compaction threads. RocksDB still caps total compaction concurrency with `rocksdb_max_background_jobs`. Limit flush and compaction write rate with [`rocksdb_rate_limiter_bytes_per_sec`](#rocksdb_rate_limiter_bytes_per_sec).




### `rocksdb_max_bottom_pri_background_compactions`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --rocksdb_max_bottom_pri_background_compactions |
| Dynamic      | No                                              |
| Data type    | Unsigned integer                                |
| Default      | 0                                               |

Creates a specified number of threads, sets a lower CPU priority, and letting compactions use them. The maximum compaction concurrency is capped by `rocksdb_max_background_compactions` or `rocksdb_max_background_jobs`

The minimum value is `0` and the maximum value is `64`.




### `rocksdb_max_compaction_history`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --rocksdb-max-compaction-history                |
| Dynamic      | Yes                                             |
| Scope        | Global                                          |
| Data type    | Unsigned integer                                |
| Default      | 64                                              |

The minimum value is `0` and the maximum value is `UINT64_MAX`.

Tracks the history for at most `rockdb_mx_compaction_history` completed compactions. The history is in the INFORMATION_SCHEMA.ROCKSDB_COMPACTION_HISTORY table.




### `rocksdb_max_file_opening_threads`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --rocksdb-max-file-opening-threads              |
| Dynamic      | No                                              |
| Scope        | Global                                          |
| Data type    | Numeric                                         |
| Default      | 16                                              |


This variable sets `DBOptions::max_file_opening_threads` for RocksDB. The default value is `16`. The minimum value is `1` and the maximum value is 2147483647 (`INT_MAX`).

#### Version changes

In Percona Server for MySQL 8.4.7-7, the maximum value was changed to `262144`.




### `rocksdb_max_latest_deadlocks`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | --rocksdb-max-latest-deadlocks |
| Dynamic      | Yes                            |
| Scope        | Global                         |
| Data type    | Numeric                        |
| Default      | 5                              |

Specifies the maximum number of recent deadlocks to store.




### `rocksdb_max_log_file_size`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-max-log-file-size |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 0                           |

Specifies the maximum size for info log files,
after which the log is rotated.
Default value is `0`, meaning that only one log file is used.
Allowed range is up to `18446744073709551615`.

Also see rocksdb_log_file_time_to_roll.




### `rocksdb_max_manifest_file_size`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-manifest-log-file-size |
| Dynamic      | No                               |
| Scope        | Global                           |
| Data type    | Numeric                          |
| Default      | 18446744073709551615             |

Specifies the maximum size of the MANIFEST data file,
after which it is rotated.
Default value is also the maximum, making it practically unlimited:
only one manifest file is used.




### `rocksdb_max_manual_compactions`

| Option       | Description                      |
| ------------ | -------------------------------- |
| Command-line | --rocksdb-max-manual-compactions |
| Dynamic      | Yes                              |
| Scope        | Global                           |
| Data type    | UINT                             |
| Default      | 10                               |

The variable defines the maximum number of pending plus ongoing manual compactions. The default value and the minimum value is 0. The maximum value is 4294967295 (UNIT_MAX).




### `rocksdb_max_open_files`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-max-open-files |
| Dynamic      | No                       |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 1000                     |

Specifies the maximum number of file handles opened by MyRocks.
Values in the range between `0` and `open_files_limit`
are taken as they are. If rocksdb_max_open_files value is
greater than `open_files_limit`, it will be reset to 1/2 of
`open_files_limit`, and a warning will be emitted to the `mysqld`
error log. A value of `-2` denotes auto tuning: just sets
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

Specifies the limit on the maximum number of row locks a transaction can have
before it fails.
Default value is also the maximum, making it practically unlimited:
transactions never fail due to row locks.




### `rocksdb_max_subcompactions`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-max-subcompactions |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 1                            |

Specifies the maximum number of threads allowed for each compaction job.
Default value of `1` means no subcompactions (one thread per compaction job).
Allowed range is up to `64`.




### `rocksdb_max_total_wal_size`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-max-total-wal-size |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 2 GB                         |

This variable limits the total disk space consumed by Write-Ahead Log (WAL)
files across all column families. The limit helps prevent log files from
exhausting disk capacity. When the combined size exceeds the threshold,
MyRocks flushes memtables to SST (Sorted String Table) files.

The default value is `2 GB`. The allowed range is up to
`9223372036854775807`.

#### How the limit works

When the combined size of all WAL files exceeds the threshold, RocksDB
identifies the oldest logs. RocksDB then forces a flush of their associated
memtables to SST files.

After the data is in an SST file, RocksDB deletes or archives the
corresponding WAL files. Total usage returns under the limit.

#### When to raise or lower the limit

A higher limit improves write performance by allowing larger, less frequent
flushes. Disk usage increases and recovery time after a crash lengthens,
because more log data must be replayed.

A lower limit keeps the disk footprint small and recovery fast. The setting
may cause frequent forced flushes, which can throttle write throughput.




### `rocksdb_merge_buf_size`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-merge-buf-size |
| Dynamic      | Yes                      |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 67108864                 |

Specifies the size (in bytes) of the merge-sort buffers
used to accumulate data during secondary key creation.
New entries are written directly to the lowest level in the database,
instead of updating indexes through the memtable and L0.
These values are sorted using merge-sort,
with buffers set to 64 MB by default (`67108864`).
Allowed range is from `100` to `18446744073709551615`.




### `rocksdb_merge_combine_read_size`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-merge-combine-read-size |
| Dynamic      | Yes                               |
| Scope        | Global                            |
| Data type    | Numeric                           |
| Default      | 1073741824                        |

Specifies the size (in bytes) of the merge-combine buffer
used for the merge-sort algorithm
as described in rocksdb_merge_buf_size.
Default size is 1 GB (`1073741824`).
Allowed range is from `100` to `18446744073709551615`.




### `rocksdb_merge_tmp_file_removal_delay_ms`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb_merge_tmp_file_removal_delay_ms |
| Dynamic      | Yes                                       |
| Scope        | Global, Session                           |
| Data type    | Numeric                                   |
| Default      | 0                                         |

Fast secondary index creation creates merge files when needed. After finishing
secondary index creation, merge files are removed. By default, the file removal
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

Specifies whether MyRocks should create a new file descriptor and table reader
for each compaction input.
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

Specifies whether to disable the block cache for column families.
Variable is disabled by default,
meaning that using the block cache is allowed.




### `rocksdb_no_create_column_family`

| Option       | Description                       |
|--------------|-----------------------------------|
| Command-line | --rocksdb-no-create-column-family |
| Dynamic      | No                                |
| Scope        | Global                            |
| Data type    | Boolean                           |
| Default      | ON                                |

Controls the processing of the column family name given in the `COMMENT`
clause in the `CREATE TABLE` or `ALTER TABLE` statement in case the column family
name does not refer to an existing column family.

If rocksdb_no_create_column_family is set to NO, a new column family will be created and the new index will
be placed into it.

If rocksdb_no_create_column_family is set to YES, no new column family will be created and the index will be
placed into the default column family. A warning is issued in this case informing that
the specified column family does not exist and cannot be created.




### `rocksdb_override_cf_options`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-override-cf-options |
| Dynamic      | No                            |
| Scope        | Global                        |
| Data type    | String                        |
| Default      |                               |

Specifies option overrides for each column family.
Empty by default.




### `rocksdb_paranoid_checks`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-paranoid-checks |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | ON                        |

Specifies whether MyRocks should re-read the data file
as soon as it is created to verify correctness.
Enabled by default.




### `rocksdb_partial_index_blind_delete`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb_partial_index_blind_delete |
| Dynamic      | Yes                          |
| Scope        | Global                       |
| Data type    | Boolean                      |
| Default      | ON                           |

If enabled, the server does not read from the partial index to check if the key exists before 
deleting the partial index and the delete marker is unconditionally written.

If the variable is disabled (OFF), the server always reads from partial index to check if key exists before 
deleting the partial index. 

This variable is enabled (ON) by default.




### `rocksdb_partial_index_ignore_killed`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-partial-index-ignore-killed |
| Dynamic      | Yes                       |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | ON                        |

If this variable is set to `ON`, the partial index materialization ignores the killed flag and continues materialization until completion. If queries are killed during materialization due to timeout, the work done so far is wasted, and the killed query will likely be retried later, hitting the same issue.

The default value is `ON` which means this variable is enabled.




### `rocksdb_partial_index_sort_max_mem`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-partial-index-sort-max-mem |
| Dynamic      | Yes                      |
| Scope        | Local                    |
| Data type    | Unsigned Integer         |
| Default      | 0                        |

This variable sets the memory threshold, in bytes, for MyRocks to perform an
in-memory sort when a query is only partially satisfied by an index.

#### How the default behaves

The default value is `0`, which removes the memory limit. MyRocks may use as
much RAM (random-access memory) as needed to perform the sort in memory.

The default produces the following effects:

* Delivers maximum performance for partial index scans by avoiding slow
  disk-based filesorts.

* Risks consuming all available system memory when a single large query, or
  many concurrent queries, run at once. The condition can lead to an
  out-of-memory (OOM) crash.

#### When to set a memory cap

A non-zero value, such as `16777216` for 16 MB, introduces a safety governor.

The cap produces the following effects:

* Enables MyRocks to use the optimized in-memory sort path only when the
  result set fits within the defined memory budget.

* Forces a fallback to a standard filesort when a sort requires more than
  the cap. The fallback avoids unbounded memory use and protects server
  stability. Affected queries take longer to complete because sorting uses
  disk or temporary files instead of memory.




### `rocksdb_pause_background_work`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-pause-background-work |
| Dynamic      | Yes                             |
| Scope        | Global                          |
| Data type    | Boolean                         |
| Default      | OFF                             |

Specifies whether MyRocks should pause all background operations.
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

Specifies the level of information to capture with the Perf Context plugins.
The default value is `0`.
The allowed range is up to `5`.

| Value | Description |
|---|---|
| 1 | Disable perf stats |
| 2 | Enable only count stats |
| 3 | Enable count stats and time stats except for mutexes |
| 4 | Enable count stats and time stats, except for wall time or CPU time for mutexes |
| 5 | Enable all count stats and time stats |




### `rocksdb_persistent_cache_path`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-persistent-cache-path |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | String                          |
| Default      |                                 |

Specifies the path to the persistent cache.
Set this together with rocksdb_persistent_cache_size_mb.




### `rocksdb_persistent_cache_size_mb`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-persistent-cache-size-mb |
| Dynamic      | No                                 |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 0                                  |

Specifies the size of the persisten cache in megabytes.
Default is `0` (persistent cache disabled).
Allowed range is up to `18446744073709551615`.
Set this together with rocksdb_persistent_cache_path.




### `rocksdb_pin_l0_filter_and_index_blocks_in_cache`

| Option       | Description                                       |
|--------------|---------------------------------------------------|
| Command-line | --rocksdb-pin-l0-filter-and-index-blocks-in-cache |
| Dynamic      | No                                                |
| Scope        | Global                                            |
| Data type    | Boolean                                           |
| Default      | ON                                                |

Specifies whether MyRocks pins the filter and index blocks in the cache
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

Specifies whether queries that generate snapshot conflicts
should be logged to the error log.
Disabled by default.




### `rocksdb_protection_bytes_per_key`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --rocksdb_protection_bytes_per_key        |
| Dynamic      | Yes                                       |
| Scope        | Global, Session                           |
| Data type    | Numeric                                   |
| Default      | 0                                         |

This variable is used to configure `WriteOptions::protection_bytes_per_key`. The default value is 0 (disabled). When this variable is set to 1, 2, 4, or 8, it uses that number of bytes per key value to protect entries in the WriteBatch.

The minimum value is `0`.

The maximum value is `ULONG_MAX (0xFFFFFFFF)`.




### `rocksdb_rate_limiter_bytes_per_sec`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-rate-limiter-bytes-per-sec |
| Dynamic      | Yes                                  |
| Scope        | Global                               |
| Data type    | Numeric                              |
| Default      | 0                                    |

Limits the combined write rate of memtable flushes and Sorted String Table (SST) compaction. The unit is bytes per second. The limiter does not throttle client writes to memtables. The limiter does not throttle Write-Ahead Log (WAL) writes.

The default value is `0` and disables the rate limiter. The allowed range is `0` to `9223372036854775807`.

A runtime `SET GLOBAL` can change a non-zero rate only if startup created the limiter. Shut down the server to enable or disable the limiter. Then set the value in the configuration file and restart.

At startup, add `--rocksdb-rate-limiter-bytes-per-sec` on the server command line. Or set `rocksdb_rate_limiter_bytes_per_sec` under the `[mysqld]` group in the server configuration file. After the limiter is active, run the following statement. The statement sets the rate to 104857600 bytes per second. That rate equals 100 megabytes (MB) per second:

```sql
SET GLOBAL rocksdb_rate_limiter_bytes_per_sec = 104857600;
```

Persist the value in the configuration file so the rate remains after restart.

MyRocks creates a GenericRateLimiter with a 100 millisecond refill period. RocksDB assigns high I/O priority to flush writes. RocksDB assigns low I/O priority to compaction writes. The limiter still grants compaction tokens so flush traffic does not starve compaction.

The limiter applies to the following write paths:

| Write path | Rate limiter |
|------------|--------------|
| Client transactions that write memtables | Not throttled |
| Write-Ahead Log (WAL) writes | Not throttled |
| Memtable flush writes to SST files | Throttled |
| Compaction writes to SST files | Throttled |
| SST file deletion | Not throttled. Use [`rocksdb_sst_mgr_rate_bytes_per_sec`](#rocksdb_sst_mgr_rate_bytes_per_sec). |

A low limit delays flush and compaction I/O. Delayed flushes let memtables accumulate. Delayed compaction lets Level 0 (L0) files and pending compaction bytes grow. MyRocks then slows or stops client writes. A high limit can saturate storage and raise read latency. On a server that also runs InnoDB, include InnoDB write I/O in the same storage budget.

Watch the following status variables after you enable the limiter:

* [`rocksdb_flush_write_bytes`](myrocks-status-variables.md#rocksdb_flush_write_bytes) counts flush write volume.

* [`rocksdb_compact_write_bytes`](myrocks-status-variables.md#rocksdb_compact_write_bytes) counts compaction write volume.

* [`rocksdb_bytes_written`](myrocks-status-variables.md#rocksdb_bytes_written) counts uncompressed client write volume. The limiter does not cap this counter.

* [`rocksdb_wal_bytes`](myrocks-status-variables.md#rocksdb_wal_bytes) counts WAL write volume. The limiter does not cap this counter.

* [`rocksdb_memtable_unflushed`](myrocks-status-variables.md#rocksdb_memtable_unflushed) shows unflushed memtable memory.

* [`rocksdb_stall_memtable_limit_slowdowns`](myrocks-status-variables.md#rocksdb_stall_memtable_limit_slowdowns) and [`rocksdb_stall_memtable_limit_stops`](myrocks-status-variables.md#rocksdb_stall_memtable_limit_stops) rise when memtable count nears or hits the limit.

* [`rocksdb_stall_l0_file_count_limit_slowdowns`](myrocks-status-variables.md#rocksdb_stall_l0_file_count_limit_slowdowns) and [`rocksdb_stall_l0_file_count_limit_stops`](myrocks-status-variables.md#rocksdb_stall_l0_file_count_limit_stops) rise when L0 file count nears or hits the limit.

* [`rocksdb_stall_pending_compaction_limit_slowdowns`](myrocks-status-variables.md#rocksdb_stall_pending_compaction_limit_slowdowns) and [`rocksdb_stall_pending_compaction_limit_stops`](myrocks-status-variables.md#rocksdb_stall_pending_compaction_limit_stops) rise when pending compaction bytes near or hit the limit.

* [`rocksdb_stall_total_slowdowns`](myrocks-status-variables.md#rocksdb_stall_total_slowdowns), [`rocksdb_stall_total_stops`](myrocks-status-variables.md#rocksdb_stall_total_stops), and [`rocksdb_stall_micros`](myrocks-status-variables.md#rocksdb_stall_micros) summarize write slowdowns, stops, and wait time.

Related variables include the following:

* [`rocksdb_delayed_write_rate`](#rocksdb_delayed_write_rate) throttles client writes after MyRocks hits a soft write limit.

* [`rocksdb_max_background_jobs`](#rocksdb_max_background_jobs) sets how many flush and compaction jobs can run.

* [`rocksdb_sst_mgr_rate_bytes_per_sec`](#rocksdb_sst_mgr_rate_bytes_per_sec) limits SST file deletion rate.




### `rocksdb_read_free_rpl`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-read-free-rpl |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | Enum                    |
| Default      | OFF                     |

Uses read-free replication, which allows no row lookup during replication, on the replica.

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

We recommend that you use `rocksdb_read_free_rpl` instead of this variable.

This variable lists tables (as a regular expression)
that should use read-free replication on the replica
(that is, replication without row lookups).
Empty by default.




### `rocksdb_records_in_range`

| Option       | Description                |
|--------------|----------------------------|
| Command-line | --rocksdb-records-in-range |
| Dynamic      | Yes                        |
| Scope        | Global, Session            |
| Data type    | Numeric                    |
| Default      | 0                          |

Specifies the value to override the result of `records_in_range()`.
Default value is `0`.
Allowed range is up to `2147483647`.




### `rocksdb_reset_stats`

| Option       | Description           |
|--------------|-----------------------|
| Command-line | --rocksdb-reset-stats |
| Dynamic      | Yes                   |
| Scope        | Global                |
| Data type    | Boolean               |
| Default      | OFF                   |

Resets MyRocks internal statistics dynamically
(without restarting the server).




### `rocksdb_rollback_on_timeout`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-rollback-on-timeout |
| Dynamic      | Yes                           |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | OFF                           |

By default, only the last statement on a transaction is rolled back. If `--rocksdb-rollback-on-timeout=ON`, a transaction timeout causes a rollback of the entire transaction.




### `rocksdb_rpl_skip_tx_api`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-rpl-skip-tx-api |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | OFF                       |

Specifies whether write batches should be used for replication thread
instead of the transaction API.
Disabled by default.

There are two conditions which are necessary to
use it: row replication format and replica
operating in super read only mode.




### `rocksdb_seconds_between_stat_computes`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | --rocksdb-seconds-between-stat-computes |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Numeric                                 |
| Default      | 3600                                    |

Specifies the number of seconds to wait
between recomputation of table statistics for the optimizer.
During that time, only changed indexes are updated.
Default value is `3600`.
Allowed is from `0` to `4294967295`.




### `rocksdb_signal_drop_index_thread`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-signal-drop-index-thread |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | Boolean                            |
| Default      | OFF                                |

Signals the MyRocks drop index thread to wake up.




### `rocksdb_sim_cache_size`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --rocksdb-sim-cache-size |
| Dynamic      | No                       |
| Scope        | Global                   |
| Data type    | Numeric                  |
| Default      | 0                        |

Enables the simulated cache, which allows us to figure out the hit/miss rate
with a specific cache size without changing the real block cache.




### `rocksdb_skip_bloom_filter_on_read`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-skip-bloom-filter-on_read |
| Dynamic      | Yes                                 |
| Scope        | Global, Session                     |
| Data type    | Boolean                             |
| Default      | OFF                                 |

Specifies whether bloom filters should be skipped on reads.
Disabled by default (bloom filters are not skipped).




### `rocksdb_skip_fill_cache`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-skip-fill-cache |
| Dynamic      | Yes                       |
| Scope        | Global, Session           |
| Data type    | Boolean                   |
| Default      | OFF                       |

Specifies whether to skip caching data on read requests.
Disabled by default (caching is not skipped).




### `rocksdb_skip_locks_if_skip_unique_check`

| Option       | Description                             |
|--------------|-----------------------------------------|
| Command-line | rocksdb_skip_locks_if_skip_unique_check |
| Dynamic      | Yes                                     |
| Scope        | Global                                  |
| Data type    | Boolean                                 |
| Default      | OFF                                     |

Skip row locking when unique checks are disabled.




### `rocksdb_sst_mgr_rate_bytes_per_sec`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-sst-mgr-rate-bytes-per-sec |
| Dynamic      | Yes                                  |
| Scope        | Global, Session                      |
| Data type    | Numeric                              |
| Default      | 0                                    |

Specifies the maximum rate for writing to data files.
Default value is `0`. This option is not effective on HDD.
Allowed range is from `0` to `18446744073709551615`.




### `rocksdb_stats_dump_period_sec`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-stats-dump-period-sec |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 600                             |

Specifies the period in seconds for performing a dump of the MyRocks statistics
to the info log.
Default value is `600`.
Allowed range is up to `2147483647`.




### `rocksdb_stats_level`

| Option       | Description           |
|--------------|-----------------------|
| Command-line | --rocksdb-stats-level |
| Dynamic      | Yes                   |
| Scope        | Global                |
| Data type    | Numeric               |
| Default      | 0                     |

Controls the RocksDB statistics level. The default value is “0” (kExceptHistogramOrTimers), which is the fastest level. The maximum value is “4”.




### `rocksdb_stats_recalc_rate`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-stats-recalc-rate |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 0                           |

Specifies the number of indexes to recalculate per second. Recalculating index statistics periodically ensures it to match the actual sum from SST files.
Default value is `0`. Allowed range is up to `4294967295`.




### `rocksdb_store_row_debug_checksums`

| Option       | Description                         |
|--------------|-------------------------------------|
| Command-line | --rocksdb-store-row-debug-checksums |
| Dynamic      | Yes                                 |
| Scope        | Global                              |
| Data type    | Boolean                             |
| Default      | OFF                                 |

Specifies whether to include checksums when writing index or table records.
Disabled by default.




### `rocksdb_strict_collation_check`

| Option       | Description                      |
|--------------|----------------------------------|
| Command-line | --rocksdb-strict-collation-check |
| Dynamic      | Yes                              |
| Scope        | Global                           |
| Data type    | Boolean                          |
| Default      | ON                               |

**[Removed: 8.4.5-5]** As of Percona Server for MySQL 8.4.5-5, the `rocksdb_strict_collation_check` variable has been removed.

Specifies whether to check and verify
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

**[Removed: 8.4.5-5]** As of Percona Server for MySQL 8.4.5-5, the `rocksdb_strict_collation_exceptions` variable has been removed.

Lists tables (as a regular expression) that should be excluded
from verifying case-sensitive collation
enforced by rocksdb_strict_collation_check.
Empty by default.




### `rocksdb_table_cache_numshardbits`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-table-cache-numshardbits |
| Dynamic      | No                                 |
| Scope        | Global                             |
| Data type    | Numeric                            |
| Default      | 6                                  |

Specifies the number if table caches.
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

The maximum number of rows to scan in a table scan based on
a cardinality calculation.
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

The number of modified rows to trigger a stats recalculation. This is a
dependent variable for stats recalculation.
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

The percentage of the number of modified rows over the total number of rows
to trigger stats recalculations. This is a dependent variable for stats
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

Specifies the percentage of entries to sample
when collecting statistics about table properties.
Default value is `10`.
Allowed range is from `0` to `100`.



### `rocksdb_table_stats_skip_system_cf`

| Option                            | Description                                                                           |
|-----------------------------------|---------------------------------------------------------------------------------------|
| Command-line                      | --rocksdb-table-stats-skip-system-cf                                                  |
| Dynamic                           | Yes                                                                                   |
| Scope                             | Global                                                                                |
| Data type                         | Boolean                                                                               |
| Default                           | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Determines whether to skip recording table statistics for the system column
family.


### `rocksdb_table_stats_use_table_scan`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-table-stats-use-table-scan |
| Dynamic      | Yes                                  |
| Scope        | Global                               |
| Data type    | Boolean                              |
| Default      | OFF.                                 |

Enables table-scan-based index calculations. The default value is `OFF`.




### `rocksdb_tmpdir`

| Option       | Description      |
|--------------|------------------|
| Command-line | --rocksdb-tmpdir |
| Dynamic      | Yes              |
| Scope        | Global, Session  |
| Data type    | String           |
| Default      |                  |

Specifies the path to the directory for temporary files during DDL operations.




### `rocksdb_trace_block_cache_access`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --rocksdb-trace-block-cache-access |
| Dynamic      | Yes                                |
| Scope        | Global                             |
| Data type    | String                             |
| Default      | &quot;&quot;                       |

Defines the block cache trace option string. The format is sampling frequency: max_trace_file_size:trace_file_name. The sampling frequency value and max_trace_file_size value are positive integers. The block accesses are saved to the `rocksdb_datadir/block_cache_traces/trace_file_name`. The default value is an empty string.




### `rocksdb_trace_queries`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-trace-queries |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | String                  |
| Default      | &quot;&quot;            |

This variable is a trace option string. The format is sampling_frequency:max_trace_file_size:trace_file_name. The sampling_frequency and max_trace_file_size are positive integers. The queries are saved to the rocksdb_datadir/queries_traces/trace_file_name.




### `rocksdb_trace_sst_api`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --rocksdb-trace-sst-api |
| Dynamic      | Yes                     |
| Scope        | Global                  |
| Data type    | Boolean                 |
| Default      | OFF                     |

Specifies whether to generate trace output in the log
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

DBOptions::track_and_verify_wals_in_manifest for RocksDB.




### `rocksdb_two_write_queues`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --rocksdb-track-and-verify-wals-in-manifest |
| Dynamic      | No                                          |
| Scope        | Global                                      |
| Data type    | Boolean                                     |
| Default      | ON                                          |

When enabled this variable allows/encourages threads that are using
two-phase commit to `prepare` in parallel.




### `rocksdb_unsafe_for_binlog`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-unsafe-for-binlog |
| Dynamic      | Yes                         |
| Scope        | Global, Session             |
| Data type    | Boolean                     |
| Default      | OFF                         |

Specifies whether to allow statement-based binary logging
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

Specifies option updates for each column family.
Empty by default.




### `rocksdb_use_adaptive_mutex`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-use-adaptive-mutex |
| Dynamic      | No                           |
| Scope        | Global                       |
| Data type    | Boolean                      |
| Default      | OFF                          |

Specifies whether to use adaptive mutex which spins in user space before
resorting to the kernel. Disabled by default.




### `rocksdb_use_default_sk_cf`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-use-default-sk-cf |
| Dynamic      | No                          |
| Scope        | Global                      |
| Data type    | Boolean                     |
| Default      | OFF                         |

Use `default_sk` column family for secondary keys.




### `rocksdb_use_direct_io_for_flush_and_compaction`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --rocksdb-use-direct-io-for-flush-and-compaction |
| Dynamic      | No                                               |
| Scope        | Global                                           |
| Data type    | Boolean                                          |
| Default      | OFF                                              |

Specifies whether to write to data files directly,
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

Specifies whether to read data files directly,
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

Specifies whether MyRocks should use `fsync` instead of `fdatasync`
when requesting a sync of a data file.
Disabled by default.




### `rocksdb_use_hyper_clock_cache`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb_use_hyper_clock_cache |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Boolean                   |
| Default      | OFF                       |

This variable replaces the standard LRU (Least Recently Used) block cache
with a lock-free HyperClockCache implementation. When enabled, MyRocks uses
HyperClockCache instead of the default LRUCache for RocksDB. The default
value is `OFF`.

#### Key benefits

The HyperClockCache provides the following benefits:

* High concurrency on many-core systems with 16 or more cores. The cache
  reduces the global lock bottleneck found in traditional LRU caches.

* CPU efficiency through a clock algorithm rather than a linked list. The
  algorithm avoids expensive memory writes and synchronization on every
  cache hit.

#### Trade-offs

Enabling HyperClockCache produces the following trade-offs:

* Memory overhead. The cache uses a fixed-size hash table, which has
  slightly higher per-entry memory overhead than a standard LRU cache.

* Approximate LRU ordering. Eviction precision is lower than with a
  traditional LRU cache, but faster to maintain.

* Throughput improvement. Heavy read or scan workloads can see
  significantly higher throughput.

#### When to enable HyperClockCache

Enable HyperClockCache when CPU profiling shows high mutex contention within
the RocksDB block cache, or when running on high core-count servers.



### `rocksdb_use_io_uring`

| Option                  | Description                                                                           |
|-------------------------|---------------------------------------------------------------------------------------|
| Command-line            | --rocksdb-use-io-uring                                                                |
| Dynamic                 | Yes                                                                                   |
| Scope                   | Global                                                                                |
| Data type               | Boolean                                                                               |
| Default                 | OFF                                                                                   |

Added in Percona Server for MySQL 8.4.5-5.

Enables the use of `io_uring` for RocksDB.


### `rocksdb_use_write_buffer_manager`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --rocksdb_use_write_buffer_manager |
| Dynamic      | No                   |
| Scope        | Global               |
| Data type    | Boolean              |
| Default      | OFF                  |

This variable is [tech preview](./glossary.md#tech-preview) and may be removed in the future releases.

Allows to turn on the write buffer manager (WriteBufferManager) from `cnf` files. This variable is related to [`rocksdb_charge_memory`](#rocksdb_charge_memory).




### `rocksdb_validate_tables`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-validate-tables |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Numeric                   |
| Default      | 1                         |

Specifies whether to verify that MySQL data dictionary is equal to the MyRocks data dictionary.


* `0`: do not verify.


* `1`: verify and fail on error (default).


* `2`: verify and continue with error.




### `rocksdb_verify_row_debug_checksums`

| Option       | Description                          |
|--------------|--------------------------------------|
| Command-line | --rocksdb-verify-row-debug-checksums |
| Dynamic      | Yes                                  |
| Scope        | Global, Session                      |
| Data type    | Boolean                              |
| Default      | OFF                                  |

Specifies whether to verify checksums when reading index or table records.
Disabled by default.




### `rocksdb_wal_bytes_per_sync`

| Option       | Description                  |
|--------------|------------------------------|
| Command-line | --rocksdb-wal-bytes-per-sync |
| Dynamic      | Yes                          |
| Scope        | Global                       |
| Data type    | Numeric                      |
| Default      | 0                            |

Specifies how often should the OS sync WAL (write-ahead log) files to disk
as they are being written, asynchronously, in the background.
This operation can be used to smooth out write I/O over time.
Default value is `0`, meaning that files are never synced.
Allowed range is up to `18446744073709551615`.




### `rocksdb_wal_dir`

| Option       | Description       |
|--------------|-------------------|
| Command-line | --rocksdb-wal-dir |
| Dynamic      | No                |
| Scope        | Global            |
| Data type    | String            |
| Default      |                   |

Specifies the path to the directory where MyRocks stores WAL files.




### `rocksdb_wal_recovery_mode`

| Option       | Description                 |
|--------------|-----------------------------|
| Command-line | --rocksdb-wal-recovery-mode |
| Dynamic      | Yes                         |
| Scope        | Global                      |
| Data type    | Numeric                     |
| Default      | 2                           |

Specifies the level of tolerance when recovering write-ahead logs (WAL) files
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

Specifies the maximum size of all WAL files in megabytes
before attempting to flush memtables and delete the oldest files.
Default value is `0` (never rotated).
Allowed range is up to `9223372036854775807`.




### `rocksdb_wal_ttl_seconds`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --rocksdb-wal-ttl-seconds |
| Dynamic      | No                        |
| Scope        | Global                    |
| Data type    | Numeric                   |
| Default      | 0                         |

Specifies the timeout in seconds before deleting archived WAL files.
Default is `0` (archived WAL files are never deleted).
Allowed range is up to `9223372036854775807`.




### `rocksdb_whole_key_filtering`

| Option       | Description                   |
|--------------|-------------------------------|
| Command-line | --rocksdb-whole-key-filtering |
| Dynamic      | No                            |
| Scope        | Global                        |
| Data type    | Boolean                       |
| Default      | ON                            |

The `rocksdb_whole_key_filtering` variable controls whether the Bloom filter
stores a hash of the entire key or only the prefix. The option is part of
RocksDB `BlockBasedTableOptions`. The default value is `ON`.

When the variable is enabled, ensure that lookups use the whole key for
matching.

#### How the filter behaves

The two states produce the following behavior:

* Enabled (default): MyRocks adds both the whole key and the prefix to the
  Bloom filter. Storing both yields the most accurate filtering for point
  lookups, such as `WHERE pk = 10`. The engine can skip SST (Sorted String
  Table) files that do not contain the key.

* Disabled: MyRocks adds only the prefix to the Bloom filter. Because fewer
  unique prefixes exist than unique keys, Bloom filters are smaller and save
  significant memory.

#### When to disable whole-key filtering

Disabling whole-key filtering suits memory-constrained environments or
workloads dominated by prefix scans. Point lookups see a higher
false-positive rate. The database may read from disk because the prefix
matched, even though the full key did not.




### `rocksdb_write_batch_flush_threshold`

| Option       | Description                           |
|--------------|---------------------------------------|
| Command-line | --rocksdb-write-batch-flush-threshold |
| Dynamic      | Yes                                   |
| Scope        | Local                                 |
| Data type    | Integer                               |
| Default      | 0                                     |

This variable specifies the maximum size of the write batch in bytes before flushing. Only valid if `rockdb_write_policy` is WRITE_UNPREPARED. There is no limit if the variable is set to the default setting.




### `rocksdb_write_batch_max_bytes`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --rocksdb-write-batch-max-bytes |
| Dynamic      | Yes                             |
| Scope        | Global                          |
| Data type    | Numeric                         |
| Default      | 0                               |

Specifies the maximum size of a RocksDB write batch in bytes. `0` means no
limit. In case user exceeds the limit following error will be shown:
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

Lets you temporarily disable writes to WAL files,
which can be useful for bulk loading.




### `rocksdb_write_ignore_missing_column_families`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --rocksdb-write-ignore-missing-column-families |
| Dynamic      | Yes                                            |
| Scope        | Global, Session                                |
| Data type    | Boolean                                        |
| Default      | OFF                                            |

Specifies whether to ignore writes to column families that do not exist.
Disabled by default (writes to non-existent column families are not ignored).




### `rocksdb_write_policy`

| Option       | Description            |
|--------------|------------------------|
| Command-line | --rocksdb-write-policy |
| Dynamic      | No                     |
| Scope        | Global                 |
| Data type    | String                 |
| Default      | write_committed        |

Specifies when two-phase commit data are written into the database.
Allowed values are `write_committed`, `write_prepared`, and
`write_unprepared`.

| Value                 | Description                                                      |
| --------------------- | ---------------------------------------------------------------- |
| `write_committed`     | Data written at commit time                                      |
| `write_prepared`      | Data written after the prepare phase of a two-phase transaction  |
| `write_unprepared`    | Data written before the prepare phase of a two-phase transaction |

<!-- RocksDB options: Each is defined with and without the rocksdb
prefix. Some have the abbreviated syntax -->
