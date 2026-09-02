# Percona Server for MySQL {{vers}} variables

## System variables

!!! note "Version notice"

    The built-in thread pool variables apply to Percona Server for MySQL 9.7.1-1 and earlier 9.7 releases.

    Percona Server for MySQL 9.7.2-2 removes `thread_pool_high_prio_mode`, `thread_pool_high_prio_tickets`, `thread_pool_idle_timeout`, `thread_pool_max_threads`, and `thread_pool_oversubscribe`.

    The names `thread_pool_size` and `thread_pool_stall_limit` remain in the [MySQL thread pool plugin](mysql-thread-pool.md).

    The plugin does not keep the built-in defaults, units, or dynamic settings for `thread_pool_size` and `thread_pool_stall_limit`.

    `thread_pool_size` default: number of processors in the built-in pool, `16` in the plugin.

    `thread_pool_size` is dynamic in the built-in pool. The plugin does not permit runtime changes.

    `thread_pool_stall_limit` unit: milliseconds in the built-in pool, 10-millisecond intervals in the plugin.

    `thread_pool_stall_limit` default: `500` in the built-in pool, `6` in the plugin.

    See [Thread pool](threadpool.md) for the built-in variables.

    See [MySQL thread pool plugin](mysql-thread-pool.md) for the plugin variables.

| Name | Cmd-Line | Option File | Var Scope | Dynamic |
| --- | --- | --- | --- | --- |
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
| secure_log_path | Yes | Yes | Global | No |
| slow_query_log_always_write_time | Yes | Yes | Global | Yes |
| slow_query_log_use_global_control | Yes | Yes | Global | Yes |
| thread_pool_high_prio_mode (9.7.1-1 and earlier) | Yes | Yes | Both | Yes |
| thread_pool_high_prio_tickets (9.7.1-1 and earlier) | Yes | Yes | Both | Yes |
| thread_pool_idle_timeout (9.7.1-1 and earlier) | Yes | Yes | Global | Yes |
| thread_pool_max_threads (9.7.1-1 and earlier) | Yes | Yes | Global | Yes |
| thread_pool_oversubscribe (9.7.1-1 and earlier) | Yes | Yes | Global | Yes |
| thread_pool_size (name in both; behavior differs) | Yes | Yes | Global | Yes |
| thread_pool_stall_limit (name in both; behavior differs) | Yes | Yes | Global | No |
| thread_statistics | Yes | Yes | Global | Yes |
| userstat | Yes | Yes | Global | Yes |
| version_comment | Yes | Yes | Global | Yes |
| version_suffix | Yes | Yes | Global | Yes |

## Status variables

!!! note "Version notice"

    The `Threadpool_*` status variables belong to the built-in thread pool on Percona Server for MySQL 9.7.1-1 and earlier 9.7 releases.

    Percona Server for MySQL 9.7.2-2 removes all `Threadpool_*` status variables.

    The [MySQL thread pool plugin](mysql-thread-pool.md) reports state in the `performance_schema.tp_thread_group_state`, `performance_schema.tp_thread_group_stats`, and `performance_schema.tp_thread_state` tables.

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
| Innodb_max_trx_id | Numeric | Global |
| Innodb_mem_adaptive_hash | Numeric | Global |
| Innodb_mem_dictionary | Numeric | Global |
| Innodb_oldest_view_low_limit_trx_id | Numeric | Global |
| Innodb_purge_trx_id | Numeric | Global |
| Innodb_purge_undo_no | Numeric | Global |
| Threadpool_average_hp_queue_wait_us (9.7.1-1 and earlier) | String | Global |
| Threadpool_average_queue_wait_us (9.7.1-1 and earlier) | String | Global |
| Threadpool_idle_threads (9.7.1-1 and earlier) | Numeric | Global |
| Threadpool_requests_starved_in_queue (9.7.1-1 and earlier) | Numeric | Global |
| Threadpool_requests_waiting_in_hp_queue (9.7.1-1 and earlier) | Numeric | Global |
| Threadpool_requests_waiting_in_queue (9.7.1-1 and earlier) | Numeric | Global |
| Threadpool_threads (9.7.1-1 and earlier) | Numeric | Global |
