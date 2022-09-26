# List of variables introduced in Percona Server for MySQL 8.0

## System Variables

| Name | Cmd-Line | Option File | Var Scope | Dynamic |
| --- | --- | --- | --- | --- |
| audit_log_buffer_size | Yes | Yes | Global | No |
| audit_log_file | Yes | Yes | Global | No |
| audit_log_flush | Yes | Yes | Global | Yes |
| audit_log_format | Yes | Yes | Global | No |
| audit_log_handler | Yes | Yes | Global | No |
| audit_log_policy | Yes | Yes | Global | Yes |
| audit_log_rotate_on_size | Yes | Yes | Global | No |
| audit_log_rotations | Yes | Yes | Global | No |
| audit_log_strategy | Yes | Yes | Global | No |
| audit_log_syslog_facility | Yes | Yes | Global | No |
| audit_log_syslog_ident | Yes | Yes | Global | No |
| audit_log_syslog_priority | Yes | Yes | Global | No |
| csv_mode | Yes | Yes | Both | Yes |
| enforce_storage_engine | Yes | Yes | Global | No |
| expand_fast_index_creation | Yes | No | Both | Yes |
| extra_max_connections | Yes | Yes | Global | Yes |
| extra_port | Yes | Yes | Global | No |
| have_backup_locks | Yes | No | Global | No |
| have_backup_safe_binlog_info | Yes | No | Global | No |
| have_snapshot_cloning | Yes | No | Global | No |
| innodb_cleaner_lsn_age_factor | Yes | Yes | Global | Yes |
| innodb_corrupt_table_action | Yes | Yes | Global | Yes |
| innodb_empty_free_list_algorithm | Yes | Yes | Global | Yes |
| innodb_encrypt_online_alter_logs | Yes | Yes | Global | Yes |
| innodb_encrypt_tables | Yes | Yes | Global | Yes |
| innodb_kill_idle_transaction | Yes | Yes | Global | Yes |
| innodb_max_bitmap_file_size | Yes | Yes | Global | Yes |
| innodb_max_changed_pages | Yes | Yes | Global | Yes |
| innodb_print_lock_wait_timeout_info | Yes | Yes | Global | Yes |
| innodb_show_locks_held | Yes | Yes | Global | Yes |
| innodb_temp_tablespace_encrypt | Yes | Yes | Global | No |
| innodb_track_changed_pages | Yes | Yes | Global | No |
| keyring_vault_config | Yes | Yes | Global | Yes |
| keyring_vault_timeout | Yes | Yes | Global | Yes |
| log_slow_filter | Yes | Yes | Both | Yes |
| log_slow_rate_limit | Yes | Yes | Both | Yes |
| log_slow_rate_type | Yes | Yes | Global | Yes |
| log_slow_sp_statements | Yes | Yes | Global | Yes |
| log_slow_verbosity | Yes | Yes | Both | Yes |
| log_warnings_suppress | Yes | Yes | Global | Yes |
| proxy_protocol_networks | Yes | Yes | Global | No |
| query_response_time_flush | Yes | No | Global | No |
| query_response_time_range_base | Yes | Yes | Global | Yes |
| query_response_time_stats | Yes | Yes | Global | Yes |
| slow_query_log_always_write_time | Yes | Yes | Global | Yes |
| slow_query_log_use_global_control | Yes | Yes | Global | Yes |
| thread_pool_high_prio_mode | Yes | Yes | Both | Yes |
| thread_pool_high_prio_tickets | Yes | Yes | Both | Yes |
| thread_pool_idle_timeout | Yes | Yes | Global | Yes |
| thread_pool_max_threads | Yes | Yes | Global | Yes |
| thread_pool_oversubscribe | Yes | Yes | Global | Yes |
| thread_pool_size | Yes | Yes | Global | Yes |
| thread_pool_stall_limit | Yes | Yes | Global | No |
| thread_statistics | Yes | Yes | Global | Yes |
| tokudb_alter_print_error |  |  |  |  |
| tokudb_analyze_delete_fractionref |  |  |  |  |
| tokudb_analyze_in_background | Yes | Yes | Both | Yes |
| tokudb_analyze_mode | Yes | Yes | Both | Yes |
| tokudb_analyze_throttle | Yes | Yes | Both | Yes |
| tokudb_analyze_time | Yes | Yes | Both | Yes |
| tokudb_auto_analyze | Yes | Yes | Both | Yes |
| tokudb_block_size |  |  |  |  |
| tokudb_bulk_fetch |  |  |  |  |
| tokudb_cache_size |  |  |  |  |
| tokudb_cachetable_pool_threads | Yes | Yes | Global | No |
| tokudb_cardinality_scale_percent |  |  |  |  |
| tokudb_check_jemalloc |  |  |  |  |
| tokudb_checkpoint_lock |  |  |  |  |
| tokudb_checkpoint_on_flush_logs |  |  |  |  |
| tokudb_checkpoint_pool_threads | Yes | Yes | Global | No |
| tokudb_checkpointing_period |  |  |  |  |
| tokudb_cleaner_iterations |  |  |  |  |
| tokudb_cleaner_period |  |  |  |  |
| tokudb_client_pool_threads | Yes | Yes | Global | No |
| tokudb_commit_sync |  |  |  |  |
| tokudb_compress_buffers_before_eviction | Yes | Yes | Global | No |
| tokudb_create_index_online |  |  |  |  |
| tokudb_data_dir |  |  |  |  |
| tokudb_debug |  |  |  |  |
| tokudb_directio |  |  |  |  |
| tokudb_disable_hot_alter |  |  |  |  |
| tokudb_disable_prefetching |  |  |  |  |
| tokudb_disable_slow_alter |  |  |  |  |
| tokudb_empty_scan |  |  |  |  |
| tokudb_enable_partial_eviction | Yes | Yes | Global | No |
| tokudb_fanout | Yes | Yes | Both | Yes |
| tokudb_fs_reserve_percent |  |  |  |  |
| tokudb_fsync_log_period |  |  |  |  |
| tokudb_hide_default_row_format |  |  |  |  |
| tokudb_killed_time |  |  |  |  |
| tokudb_last_lock_timeout |  |  |  |  |
| tokudb_load_save_space |  |  |  |  |
| tokudb_loader_memory_size |  |  |  |  |
| tokudb_lock_timeout |  |  |  |  |
| tokudb_lock_timeout_debug |  |  |  |  |
| tokudb_log_dir |  |  |  |  |
| tokudb_max_lock_memory |  |  |  |  |
| tokudb_optimize_index_fraction |  |  |  |  |
| tokudb_optimize_index_name |  |  |  |  |
| tokudb_optimize_throttle |  |  |  |  |
| tokudb_pk_insert_mode |  |  |  |  |
| tokudb_prelock_empty |  |  |  |  |
| tokudb_read_block_size |  |  |  |  |
| tokudb_read_buf_size |  |  |  |  |
| tokudb_read_status_frequency |  |  |  |  |
| tokudb_row_format |  |  |  |  |
| tokudb_rpl_check_readonly |  |  |  |  |
| tokudb_rpl_lookup_rows |  |  |  |  |
| tokudb_rpl_lookup_rows_delay |  |  |  |  |
| tokudb_rpl_unique_checks |  |  |  |  |
| tokudb_rpl_unique_checks_delay |  |  |  |  |
| tokudb_strip_frm_data | Yes | Yes | Global | No |
| tokudb_support_xa |  |  |  |  |
| tokudb_tmp_dir |  |  |  |  |
| tokudb_version |  |  |  |  |
| tokudb_write_status_frequency |  |  |  |  |
| userstat | Yes | Yes | Global | Yes |
| version_comment | Yes | Yes | Global | Yes |
| version_suffix | Yes | Yes | Global | Yes |




## Status Variables

| Name | Var Type | Var Scope |
| --- | --- | --- |
| Binlog_snapshot_file | String | Global |
| Binlog_snapshot_position | Numeric | Global |
| Com_lock_binlog_for_backup | Numeric | Both |
| Com_lock_tables_for_backup | Numeric | Both |
| Com_show_client_statistics | Numeric | Both |
| Com_show_index_statistics | Numeric | Both |
| Com_show_table_statistics | Numeric | Both |
| Com_show_thread_statistics | Numeric | Both |
| Com_show_user_statistics | Numeric | Both |
| Com_unlock_binlog | Numeric | Both |
| Innodb_background_log_sync | Numeric | Global |
| Innodb_buffer_pool_pages_LRU_flushed | Numeric | Global |
| Innodb_buffer_pool_pages_made_not_young | Numeric | Global |
| Innodb_buffer_pool_pages_made_young | Numeric | Global |
| Innodb_buffer_pool_pages_old | Numeric | Global |
| Innodb_checkpoint_age | Numeric | Global |
| Innodb_checkpoint_max_age | Numeric | Global |
| Innodb_ibuf_free_list | Numeric | Global |
| Innodb_ibuf_segment_size | Numeric | Global |
| Innodb_lsn_current | Numeric | Global |
| Innodb_lsn_flushed | Numeric | Global |
| Innodb_lsn_last_checkpoint | Numeric | Global |
| Innodb_master_thread_active_loops | Numeric | Global |
| Innodb_master_thread_idle_loops | Numeric | Global |
| Innodb_max_trx_id | Numeric | Global |
| Innodb_mem_adaptive_hash | Numeric | Global |
| Innodb_mem_dictionary | Numeric | Global |
| Innodb_oldest_view_low_limit_trx_id | Numeric | Global |
| Innodb_purge_trx_id | Numeric | Global |
| Innodb_purge_undo_no | Numeric | Global |
| Threadpool_idle_threads | Numeric | Global |
| Threadpool_threads | Numeric | Global |
| Tokudb_DB_OPENS |  |  |
| Tokudb_DB_CLOSES |  |  |
| Tokudb_DB_OPEN_CURRENT |  |  |
| Tokudb_DB_OPEN_MAX |  |  |
| Tokudb_LEAF_ENTRY_MAX_COMMITTED_XR |  |  |
| Tokudb_LEAF_ENTRY_MAX_PROVISIONAL_XR |  |  |
| Tokudb_LEAF_ENTRY_EXPANDED |  |  |
| Tokudb_LEAF_ENTRY_MAX_MEMSIZE |  |  |
| Tokudb_LEAF_ENTRY_APPLY_GC_BYTES_IN |  |  |
| Tokudb_LEAF_ENTRY_APPLY_GC_BYTES_OUT |  |  |
| Tokudb_LEAF_ENTRY_NORMAL_GC_BYTES_IN |  |  |
| Tokudb_LEAF_ENTRY_NORMAL_GC_BYTES_OUT |  |  |
| Tokudb_CHECKPOINT_PERIOD |  |  |
| Tokudb_CHECKPOINT_FOOTPRINT |  |  |
| Tokudb_CHECKPOINT_LAST_BEGAN |  |  |
| Tokudb_CHECKPOINT_LAST_COMPLETE_BEGAN |  |  |
| Tokudb_CHECKPOINT_LAST_COMPLETE_ENDED |  |  |
| Tokudb_CHECKPOINT_DURATION |  |  |
| Tokudb_CHECKPOINT_DURATION_LAST |  |  |
| Tokudb_CHECKPOINT_LAST_LSN |  |  |
| Tokudb_CHECKPOINT_TAKEN |  |  |
| Tokudb_CHECKPOINT_FAILED |  |  |
| Tokudb_CHECKPOINT_WAITERS_NOW |  |  |
| Tokudb_CHECKPOINT_WAITERS_MAX |  |  |
| Tokudb_CHECKPOINT_CLIENT_WAIT_ON_MO |  |  |
| Tokudb_CHECKPOINT_CLIENT_WAIT_ON_CS |  |  |
| Tokudb_CHECKPOINT_BEGIN_TIME |  |  |
| Tokudb_CHECKPOINT_LONG_BEGIN_TIME |  |  |
| Tokudb_CHECKPOINT_LONG_BEGIN_COUNT |  |  |
| Tokudb_CHECKPOINT_END_TIME |  |  |
| Tokudb_CHECKPOINT_LONG_END_TIME |  |  |
| Tokudb_CHECKPOINT_LONG_END_COUNT |  |  |
| Tokudb_CACHETABLE_MISS |  |  |
| Tokudb_CACHETABLE_MISS_TIME |  |  |
| Tokudb_CACHETABLE_PREFETCHES |  |  |
| Tokudb_CACHETABLE_SIZE_CURRENT |  |  |
| Tokudb_CACHETABLE_SIZE_LIMIT |  |  |
| Tokudb_CACHETABLE_SIZE_WRITING |  |  |
| Tokudb_CACHETABLE_SIZE_NONLEAF |  |  |
| Tokudb_CACHETABLE_SIZE_LEAF |  |  |
| Tokudb_CACHETABLE_SIZE_ROLLBACK |  |  |
| Tokudb_CACHETABLE_SIZE_CACHEPRESSURE |  |  |
| Tokudb_CACHETABLE_SIZE_CLONED |  |  |
| Tokudb_CACHETABLE_EVICTIONS |  |  |
| Tokudb_CACHETABLE_CLEANER_EXECUTIONS |  |  |
| Tokudb_CACHETABLE_CLEANER_PERIOD |  |  |
| Tokudb_CACHETABLE_CLEANER_ITERATIONS |  |  |
| Tokudb_CACHETABLE_WAIT_PRESSURE_COUNT |  |  |
| Tokudb_CACHETABLE_WAIT_PRESSURE_TIME |  |  |
| Tokudb_CACHETABLE_LONG_WAIT_PRESSURE_COUNT |  |  |
| Tokudb_CACHETABLE_LONG_WAIT_PRESSURE_TIME |  |  |
| Tokudb_CACHETABLE_POOL_CLIENT_NUM_THREADS |  |  |
| Tokudb_CACHETABLE_POOL_CLIENT_NUM_THREADS_ACTIVE |  |  |
| Tokudb_CACHETABLE_POOL_CLIENT_QUEUE_SIZE |  |  |
| Tokudb_CACHETABLE_POOL_CLIENT_MAX_QUEUE_SIZE |  |  |
| Tokudb_CACHETABLE_POOL_CLIENT_TOTAL_ITEMS_PROCESSED |  |  |
| Tokudb_CACHETABLE_POOL_CLIENT_TOTAL_EXECUTION_TIME |  |  |
| Tokudb_CACHETABLE_POOL_CACHETABLE_NUM_THREADS |  |  |
| Tokudb_CACHETABLE_POOL_CACHETABLE_NUM_THREADS_ACTIVE |  |  |
| Tokudb_CACHETABLE_POOL_CACHETABLE_QUEUE_SIZE |  |  |
| Tokudb_CACHETABLE_POOL_CACHETABLE_MAX_QUEUE_SIZE |  |  |
| Tokudb_CACHETABLE_POOL_CACHETABLE_TOTAL_ITEMS_PROCESSED |  |  |
| Tokudb_CACHETABLE_POOL_CACHETABLE_TOTAL_EXECUTION_TIME |  |  |
| Tokudb_CACHETABLE_POOL_CHECKPOINT_NUM_THREADS |  |  |
| Tokudb_CACHETABLE_POOL_CHECKPOINT_NUM_THREADS_ACTIVE |  |  |
| Tokudb_CACHETABLE_POOL_CHECKPOINT_QUEUE_SIZE |  |  |
| Tokudb_CACHETABLE_POOL_CHECKPOINT_MAX_QUEUE_SIZE |  |  |
| Tokudb_CACHETABLE_POOL_CHECKPOINT_TOTAL_ITEMS_PROCESSED |  |  |
| Tokudb_CACHETABLE_POOL_CHECKPOINT_TOTAL_EXECUTION_TIME |  |  |
| Tokudb_LOCKTREE_MEMORY_SIZE |  |  |
| Tokudb_LOCKTREE_MEMORY_SIZE_LIMIT |  |  |
| Tokudb_LOCKTREE_ESCALATION_NUM |  |  |
| Tokudb_LOCKTREE_ESCALATION_SECONDS |  |  |
| Tokudb_LOCKTREE_LATEST_POST_ESCALATION_MEMORY_SIZE |  |  |
| Tokudb_LOCKTREE_OPEN_CURRENT |  |  |
| Tokudb_LOCKTREE_PENDING_LOCK_REQUESTS |  |  |
| Tokudb_LOCKTREE_STO_ELIGIBLE_NUM |  |  |
| Tokudb_LOCKTREE_STO_ENDED_NUM |  |  |
| Tokudb_LOCKTREE_STO_ENDED_SECONDS |  |  |
| Tokudb_LOCKTREE_WAIT_COUNT |  |  |
| Tokudb_LOCKTREE_WAIT_TIME |  |  |
| Tokudb_LOCKTREE_LONG_WAIT_COUNT |  |  |
| Tokudb_LOCKTREE_LONG_WAIT_TIME |  |  |
| Tokudb_LOCKTREE_TIMEOUT_COUNT |  |  |
| Tokudb_LOCKTREE_WAIT_ESCALATION_COUNT |  |  |
| Tokudb_LOCKTREE_WAIT_ESCALATION_TIME |  |  |
| Tokudb_LOCKTREE_LONG_WAIT_ESCALATION_COUNT |  |  |
| Tokudb_LOCKTREE_LONG_WAIT_ESCALATION_TIME |  |  |
| Tokudb_DICTIONARY_UPDATES |  |  |
| Tokudb_DICTIONARY_BROADCAST_UPDATES |  |  |
| Tokudb_DESCRIPTOR_SET |  |  |
| Tokudb_MESSAGES_IGNORED_BY_LEAF_DUE_TO_MSN |  |  |
| Tokudb_TOTAL_SEARCH_RETRIES |  |  |
| Tokudb_SEARCH_TRIES_GT_HEIGHT |  |  |
| Tokudb_SEARCH_TRIES_GT_HEIGHTPLUS3 |  |  |
| Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT |  |  |
| Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_BYTES |  |  |
| Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_UNCOMPRESSED_BYTES |  |  |
| Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_SECONDS |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_BYTES |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_UNCOMPRESSE |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_SECONDS |  |  |
| Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT |  |  |
| Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_BYTES |  |  |
| Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_UNCOMPRESSED_BYTES |  |  |
| Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_SECONDS |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_BYTES |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_UNCOMPRESSED_BY |  |  |
| Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_SECONDS |  |  |
| Tokudb_LEAF_NODE_COMPRESSION_RATIO |  |  |
| Tokudb_NONLEAF_NODE_COMPRESSION_RATIO |  |  |
| Tokudb_OVERALL_NODE_COMPRESSION_RATIO |  |  |
| Tokudb_NONLEAF_NODE_PARTIAL_EVICTIONS |  |  |
| Tokudb_NONLEAF_NODE_PARTIAL_EVICTIONS_BYTES |  |  |
| Tokudb_LEAF_NODE_PARTIAL_EVICTIONS |  |  |
| Tokudb_LEAF_NODE_PARTIAL_EVICTIONS_BYTES |  |  |
| Tokudb_LEAF_NODE_FULL_EVICTIONS |  |  |
| Tokudb_LEAF_NODE_FULL_EVICTIONS_BYTES |  |  |
| Tokudb_NONLEAF_NODE_FULL_EVICTIONS |  |  |
| Tokudb_NONLEAF_NODE_FULL_EVICTIONS_BYTES |  |  |
| Tokudb_LEAF_NODES_CREATED |  |  |
| Tokudb_NONLEAF_NODES_CREATED |  |  |
| Tokudb_LEAF_NODES_DESTROYED |  |  |
| Tokudb_NONLEAF_NODES_DESTROYED |  |  |
| Tokudb_MESSAGES_INJECTED_AT_ROOT_BYTES |  |  |
| Tokudb_MESSAGES_FLUSHED_FROM_H1_TO_LEAVES_BYTES |  |  |
| Tokudb_MESSAGES_IN_TREES_ESTIMATE_BYTES |  |  |
| Tokudb_MESSAGES_INJECTED_AT_ROOT |  |  |
| Tokudb_BROADCASE_MESSAGES_INJECTED_AT_ROOT |  |  |
| Tokudb_BASEMENTS_DECOMPRESSED_TARGET_QUERY |  |  |
| Tokudb_BASEMENTS_DECOMPRESSED_PRELOCKED_RANGE |  |  |
| Tokudb_BASEMENTS_DECOMPRESSED_PREFETCH |  |  |
| Tokudb_BASEMENTS_DECOMPRESSED_FOR_WRITE |  |  |
| Tokudb_BUFFERS_DECOMPRESSED_TARGET_QUERY |  |  |
| Tokudb_BUFFERS_DECOMPRESSED_PRELOCKED_RANGE |  |  |
| Tokudb_BUFFERS_DECOMPRESSED_PREFETCH |  |  |
| Tokudb_BUFFERS_DECOMPRESSED_FOR_WRITE |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_QUERY |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_QUERY_BYTES |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_QUERY_SECONDS |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_PREFETCH |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_PREFETCH_BYTES |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_PREFETCH_SECONDS |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_WRITE |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_WRITE_BYTES |  |  |
| Tokudb_PIVOTS_FETCHED_FOR_WRITE_SECONDS |  |  |
| Tokudb_BASEMENTS_FETCHED_TARGET_QUERY |  |  |
| Tokudb_BASEMENTS_FETCHED_TARGET_QUERY_BYTES |  |  |
| Tokudb_BASEMENTS_FETCHED_TARGET_QUERY_SECONDS |  |  |
| Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE |  |  |
| Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE_BYTES |  |  |
| Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE_SECONDS |  |  |
| Tokudb_BASEMENTS_FETCHED_PREFETCH |  |  |
| Tokudb_BASEMENTS_FETCHED_PREFETCH_BYTES |  |  |
| Tokudb_BASEMENTS_FETCHED_PREFETCH_SECONDS |  |  |
| Tokudb_BASEMENTS_FETCHED_FOR_WRITE |  |  |
| Tokudb_BASEMENTS_FETCHED_FOR_WRITE_BYTES |  |  |
| Tokudb_BASEMENTS_FETCHED_FOR_WRITE_SECONDS |  |  |
| Tokudb_BUFFERS_FETCHED_TARGET_QUERY |  |  |
| Tokudb_BUFFERS_FETCHED_TARGET_QUERY_BYTES |  |  |
| Tokudb_BUFFERS_FETCHED_TARGET_QUERY_SECONDS |  |  |
| Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE |  |  |
| Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE_BYTES |  |  |
| Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE_SECONDS |  |  |
| Tokudb_BUFFERS_FETCHED_PREFETCH |  |  |
| Tokudb_BUFFERS_FETCHED_PREFETCH_BYTES |  |  |
| Tokudb_BUFFERS_FETCHED_PREFETCH_SECONDS |  |  |
| Tokudb_BUFFERS_FETCHED_FOR_WRITE |  |  |
| Tokudb_BUFFERS_FETCHED_FOR_WRITE_BYTES |  |  |
| Tokudb_BUFFERS_FETCHED_FOR_WRITE_SECONDS |  |  |
| Tokudb_LEAF_COMPRESSION_TO_MEMORY_SECONDS |  |  |
| Tokudb_LEAF_SERIALIZATION_TO_MEMORY_SECONDS |  |  |
| Tokudb_LEAF_DECOMPRESSION_TO_MEMORY_SECONDS |  |  |
| Tokudb_LEAF_DESERIALIZATION_TO_MEMORY_SECONDS |  |  |
| Tokudb_NONLEAF_COMPRESSION_TO_MEMORY_SECONDS |  |  |
| Tokudb_NONLEAF_SERIALIZATION_TO_MEMORY_SECONDS |  |  |
| Tokudb_NONLEAF_DECOMPRESSION_TO_MEMORY_SECONDS |  |  |
| Tokudb_NONLEAF_DESERIALIZATION_TO_MEMORY_SECONDS |  |  |
| Tokudb_PROMOTION_ROOTS_SPLIT |  |  |
| Tokudb_PROMOTION_LEAF_ROOTS_INJECTED_INTO |  |  |
| Tokudb_PROMOTION_H1_ROOTS_INJECTED_INTO |  |  |
| Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_0 |  |  |
| Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_1 |  |  |
| Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_2 |  |  |
| Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_3 |  |  |
| Tokudb_PROMOTION_INJECTIONS_LOWER_THAN_DEPTH_3 |  |  |
| Tokudb_PROMOTION_STOPPED_NONEMPTY_BUFFER |  |  |
| Tokudb_PROMOTION_STOPPED_AT_HEIGHT_1 |  |  |
| Tokudb_PROMOTION_STOPPED_CHILD_LOCKED_OR_NOT_IN_MEMORY |  |  |
| Tokudb_PROMOTION_STOPPED_CHILD_NOT_FULLY_IN_MEMORY |  |  |
| Tokudb_PROMOTION_STOPPED_AFTER_LOCKING_CHILD |  |  |
| Tokudb_BASEMENT_DESERIALIZATION_FIXED_KEY |  |  |
| Tokudb_BASEMENT_DESERIALIZATION_VARIABLE_KEY |  |  |
| Tokudb_PRO_RIGHTMOST_LEAF_SHORTCUT_SUCCESS |  |  |
| Tokudb_PRO_RIGHTMOST_LEAF_SHORTCUT_FAIL_POS |  |  |
| Tokudb_RIGHTMOST_LEAF_SHORTCUT_FAIL_REACTIVE |  |  |
| Tokudb_CURSOR_SKIP_DELETED_LEAF_ENTRY |  |  |
| Tokudb_FLUSHER_CLEANER_TOTAL_NODES |  |  |
| Tokudb_FLUSHER_CLEANER_H1_NODES |  |  |
| Tokudb_FLUSHER_CLEANER_HGT1_NODES |  |  |
| Tokudb_FLUSHER_CLEANER_EMPTY_NODES |  |  |
| Tokudb_FLUSHER_CLEANER_NODES_DIRTIED |  |  |
| Tokudb_FLUSHER_CLEANER_MAX_BUFFER_SIZE |  |  |
| Tokudb_FLUSHER_CLEANER_MIN_BUFFER_SIZE |  |  |
| Tokudb_FLUSHER_CLEANER_TOTAL_BUFFER_SIZE |  |  |
| Tokudb_FLUSHER_CLEANER_MAX_BUFFER_WORKDONE |  |  |
| Tokudb_FLUSHER_CLEANER_MIN_BUFFER_WORKDONE |  |  |
| Tokudb_FLUSHER_CLEANER_TOTAL_BUFFER_WORKDONE |  |  |
| Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_STARTED |  |  |
| Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_RUNNING |  |  |
| Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_COMPLETED |  |  |
| Tokudb_FLUSHER_CLEANER_NUM_DIRTIED_FOR_LEAF_MERGE |  |  |
| Tokudb_FLUSHER_FLUSH_TOTAL |  |  |
| Tokudb_FLUSHER_FLUSH_IN_MEMORY |  |  |
| Tokudb_FLUSHER_FLUSH_NEEDED_IO |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES_1 |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES_2 |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES_3 |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES_4 |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES_5 |  |  |
| Tokudb_FLUSHER_FLUSH_CASCADES_GT_5 |  |  |
| Tokudb_FLUSHER_SPLIT_LEAF |  |  |
| Tokudb_FLUSHER_SPLIT_NONLEAF |  |  |
| Tokudb_FLUSHER_MERGE_LEAF |  |  |
| Tokudb_FLUSHER_MERGE_NONLEAF |  |  |
| Tokudb_FLUSHER_BALANCE_LEAF |  |  |
| Tokudb_HOT_NUM_STARTED |  |  |
| Tokudb_HOT_NUM_COMPLETED |  |  |
| Tokudb_HOT_NUM_ABORTED |  |  |
| Tokudb_HOT_MAX_ROOT_FLUSH_COUNT |  |  |
| Tokudb_TXN_BEGIN |  |  |
| Tokudb_TXN_BEGIN_READ_ONLY |  |  |
| Tokudb_TXN_COMMITS |  |  |
| Tokudb_TXN_ABORTS |  |  |
| Tokudb_LOGGER_NEXT_LSN |  |  |
| Tokudb_LOGGER_WRITES |  |  |
| Tokudb_LOGGER_WRITES_BYTES |  |  |
| Tokudb_LOGGER_WRITES_UNCOMPRESSED_BYTES |  |  |
| Tokudb_LOGGER_WRITES_SECONDS |  |  |
| Tokudb_LOGGER_WAIT_LONG |  |  |
| Tokudb_LOADER_NUM_CREATED |  |  |
| Tokudb_LOADER_NUM_CURRENT |  |  |
| Tokudb_LOADER_NUM_MAX |  |  |
| Tokudb_MEMORY_MALLOC_COUNT |  |  |
| Tokudb_MEMORY_FREE_COUNT |  |  |
| Tokudb_MEMORY_REALLOC_COUNT |  |  |
| Tokudb_MEMORY_MALLOC_FAIL |  |  |
| Tokudb_MEMORY_REALLOC_FAIL |  |  |
| Tokudb_MEMORY_REQUESTED |  |  |
| Tokudb_MEMORY_USED |  |  |
| Tokudb_MEMORY_FREED |  |  |
| Tokudb_MEMORY_MAX_REQUESTED_SIZE |  |  |
| Tokudb_MEMORY_LAST_FAILED_SIZE |  |  |
| Tokudb_MEM_ESTIMATED_MAXIMUM_MEMORY_FOOTPRINT |  |  |
| Tokudb_MEMORY_MALLOCATOR_VERSION |  |  |
| Tokudb_MEMORY_MMAP_THRESHOLD |  |  |
| Tokudb_FILESYSTEM_THREADS_BLOCKED_BY_FULL_DISK |  |  |
| Tokudb_FILESYSTEM_FSYNC_TIME |  |  |
| Tokudb_FILESYSTEM_FSYNC_NUM |  |  |
| Tokudb_FILESYSTEM_LONG_FSYNC_TIME |  |  |
| Tokudb_FILESYSTEM_LONG_FSYNC_NUM |  |  |
