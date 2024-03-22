# TokuDB status variables

Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. For more information, see the [TokuDB Introduction](tokudb-intro.md) and [TokuDB version changes](tokudb-version-changes.md). 


*TokuDB* status variables provide details about the inner workings of *TokuDB*
storage engine and they can be useful in tuning the storage engine to a
particular environment.

You can view these variables and their values by running:

```sql
mysql> SHOW STATUS LIKE 'tokudb%';
```

## TokuDB Status Variables Summary

The following global status variables are available:

| Name                                                            | Var Type |
|-----------------------------------------------------------------|----------|
| [Tokudb_DB_OPENS](#tokudb_db_opens)                                                 | integer  |
| [Tokudb_DB_CLOSES](#tokudb_db_closes)                                                | integer  |
| [Tokudb_DB_OPEN_CURRENT](#tokudb_db_open_current)                                          | integer  |
| [Tokudb_DB_OPEN_MAX](#tokudb_db_open_max)                                              | integer  |
| [Tokudb_LEAF_ENTRY_MAX_COMMITTED_XR](#tokudb_leaf_entry_max_committed_xr)                              | integer  |
| [Tokudb_LEAF_ENTRY_MAX_PROVISIONAL_XR](#tokudb_leaf_entry_max_provisional_xr)                           | integer  |
| [Tokudb_LEAF_ENTRY_EXPANDED](#tokudb_leaf_entry_expanded)                                      | integer  |
| [Tokudb_LEAF_ENTRY_MAX_MEMSIZE](#tokudb_leaf_entry_max_memsize)                                   | integer  |
| [Tokudb_LEAF_ENTRY_APPLY_GC_BYTES_IN](#tokudb_leaf_entry_apply_gc_bytes_in)                             | integer  |
| [Tokudb_LEAF_ENTRY_APPLY_GC_BYTES_OUT](#tokudb_leaf_entry_apply_gc_bytes_out)                            | integer  |
| [Tokudb_LEAF_ENTRY_NORMAL_GC_BYTES_IN](#tokudb_leaf_entry_normal_gc_bytes_in)                            | integer  |
| [Tokudb_LEAF_ENTRY_NORMAL_GC_BYTES_OUT](#tokudb_leaf_entry_normal_gc_bytes_out)                           | integer  |
| [Tokudb_CHECKPOINT_PERIOD](#tokudb_checkpoint_period)                                        | integer  |
| [Tokudb_CHECKPOINT_FOOTPRINT](#tokudb_checkpoint_footprint)                                     | integer  |
| [Tokudb_CHECKPOINT_LAST_BEGAN](#tokudb_checkpoint_last_began)                                    | datetime |
| [Tokudb_CHECKPOINT_LAST_COMPLETE_BEGAN](#tokudb_checkpoint_last_complete_began)                           | datetime |
| [Tokudb_CHECKPOINT_LAST_COMPLETE_ENDED](#tokudb_checkpoint_last_complete_ended)                           | datetime |
| [Tokudb_CHECKPOINT_DURATION](#tokudb_checkpoint_duration)                                      | integer  |
| [Tokudb_CHECKPOINT_DURATION_LAST](#tokudb_checkpoint_duration_last)                                 | integer  |
| [Tokudb_CHECKPOINT_LAST_LSN](#tokudb_checkpoint_last_lsn)                                      | integer  |
| [Tokudb_CHECKPOINT_TAKEN](#tokudb_checkpoint_taken)                                         | integer  |
| [Tokudb_CHECKPOINT_FAILED](#tokudb_checkpoint_failed)                                        | integer  |
| [Tokudb_CHECKPOINT_WAITERS_NOW](#tokudb_checkpoint_waiters_now)                                   | integer  |
| [Tokudb_CHECKPOINT_WAITERS_MAX](#tokudb_checkpoint_waiters_max)                                   | integer  |
| [Tokudb_CHECKPOINT_CLIENT_WAIT_ON_MO](#tokudb_checkpoint_client_wait_on_mo)                             | integer  |
| [Tokudb_CHECKPOINT_CLIENT_WAIT_ON_CS](#tokudb_checkpoint_client_wait_on_cs)                             | integer  |
| [Tokudb_CHECKPOINT_BEGIN_TIME](#tokudb_checkpoint_begin_time)                                    | integer  |
| [Tokudb_CHECKPOINT_LONG_BEGIN_TIME](#tokudb_checkpoint_long_begin_time)                               | integer  |
| [Tokudb_CHECKPOINT_LONG_BEGIN_COUNT](#tokudb_checkpoint_long_begin_count)                              | integer  |
| [Tokudb_CHECKPOINT_END_TIME](#tokudb_checkpoint_end_time)                                      | integer  |
| [Tokudb_CHECKPOINT_LONG_END_TIME](#tokudb_checkpoint_long_end_time)                                 | integer  |
| [Tokudb_CHECKPOINT_LONG_END_COUNT](#tokudb_checkpoint_long_end_count)                                | integer  |
| [Tokudb_CACHETABLE_MISS](#tokudb_cachetable_miss)                                          | integer  |
| [Tokudb_CACHETABLE_MISS_TIME](#tokudb_cachetable_miss_time)                                     | integer  |
| [Tokudb_CACHETABLE_PREFETCHES](#tokudb_cachetable_prefetches)                                    | integer  |
| [Tokudb_CACHETABLE_SIZE_CURRENT](#tokudb_cachetable_size_current)                                  | integer  |
| [Tokudb_CACHETABLE_SIZE_LIMIT](#tokudb_cachetable_size_limit)                                    | integer  |
| [Tokudb_CACHETABLE_SIZE_WRITING](#tokudb_cachetable_size_writing)                                  | integer  |
| [Tokudb_CACHETABLE_SIZE_NONLEAF](#tokudb_cachetable_size_nonleaf)                                  | integer  |
| [Tokudb_CACHETABLE_SIZE_LEAF](#tokudb_cachetable_size_leaf)                                     | integer  |
| [Tokudb_CACHETABLE_SIZE_ROLLBACK](#tokudb_cachetable_size_rollback)                                 | integer  |
| [Tokudb_CACHETABLE_SIZE_CACHEPRESSURE](#tokudb_cachetable_size_cachepressure)                            | integer  |
| [Tokudb_CACHETABLE_SIZE_CLONED](#tokudb_cachetable_size_cloned)                                   | integer  |
| [Tokudb_CACHETABLE_EVICTIONS](#tokudb_cachetable_evictions)                                     | integer  |
| [Tokudb_CACHETABLE_CLEANER_EXECUTIONS](#tokudb_cachetable_cleaner_executions)                            | integer  |
| [Tokudb_CACHETABLE_CLEANER_PERIOD](#tokudb_cachetable_cleaner_period)                                | integer  |
| [Tokudb_CACHETABLE_CLEANER_ITERATIONS](#tokudb_cachetable_cleaner_iterations)                            | integer  |
| [Tokudb_CACHETABLE_WAIT_PRESSURE_COUNT](#tokudb_cachetable_wait_pressure_count)                           | integer  |
| [Tokudb_CACHETABLE_WAIT_PRESSURE_TIME](#tokudb_cachetable_wait_pressure_time)                            | integer  |
| [Tokudb_CACHETABLE_LONG_WAIT_PRESSURE_COUNT](#tokudb_cachetable_long_wait_pressure_count)                      | integer  |
| [Tokudb_CACHETABLE_LONG_WAIT_PRESSURE_TIME](#tokudb_cachetable_long_wait_pressure_time)                       | integer  |
| [Tokudb_CACHETABLE_POOL_CLIENT_NUM_THREADS](#tokudb_cachetable_pool_client_num_threads)                       | integer  |
| [Tokudb_CACHETABLE_POOL_CLIENT_NUM_THREADS_ACTIVE](#tokudb_cachetable_pool_client_num_threads_active)                | integer  |
| [Tokudb_CACHETABLE_POOL_CLIENT_QUEUE_SIZE](#tokudb_cachetable_pool_client_queue_size)                        | integer  |
| [Tokudb_CACHETABLE_POOL_CLIENT_MAX_QUEUE_SIZE](#tokudb_cachetable_pool_client_max_queue_size)                    | integer  |
| [Tokudb_CACHETABLE_POOL_CLIENT_TOTAL_ITEMS_PROCESSED](#tokudb_cachetable_pool_client_total_items_processed)             | integer  |
| [Tokudb_CACHETABLE_POOL_CLIENT_TOTAL_EXECUTION_TIME](#tokudb_cachetable_pool_client_total_execution_time)              | integer  |
| [Tokudb_CACHETABLE_POOL_CACHETABLE_NUM_THREADS](#tokudb_cachetable_pool_cachetable_num_threads)                   | integer  |
| [Tokudb_CACHETABLE_POOL_CACHETABLE_NUM_THREADS_ACTIVE](#tokudb_cachetable_pool_cachetable_num_threads_active)            | integer  |
| [Tokudb_CACHETABLE_POOL_CACHETABLE_QUEUE_SIZE](#tokudb_cachetable_pool_cachetable_queue_size)                    | integer  |
| [Tokudb_CACHETABLE_POOL_CACHETABLE_MAX_QUEUE_SIZE](#tokudb_cachetable_pool_cachetable_max_queue_size)                | integer  |
| [Tokudb_CACHETABLE_POOL_CACHETABLE_TOTAL_ITEMS_PROCESSED](#tokudb_cachetable_pool_cachetable_total_items_processed)         | integer  |
| [Tokudb_CACHETABLE_POOL_CACHETABLE_TOTAL_EXECUTION_TIME](#tokudb_cachetable_pool_cachetable_total_execution_time)          | integer  |
| [Tokudb_CACHETABLE_POOL_CHECKPOINT_NUM_THREADS](#tokudb_cachetable_pool_checkpoint_num_threads)                   | integer  |
| [Tokudb_CACHETABLE_POOL_CHECKPOINT_NUM_THREADS_ACTIVE](#tokudb_cachetable_pool_checkpoint_num_threads_active)            | integer  |
| [Tokudb_CACHETABLE_POOL_CHECKPOINT_QUEUE_SIZE](#tokudb_cachetable_pool_checkpoint_queue_size)                    | integer  |
| [Tokudb_CACHETABLE_POOL_CHECKPOINT_MAX_QUEUE_SIZE](#tokudb_cachetable_pool_checkpoint_max_queue_size)                | integer  |
| [Tokudb_CACHETABLE_POOL_CHECKPOINT_TOTAL_ITEMS_PROCESSED](#tokudb_cachetable_pool_checkpoint_total_items_processed)         | integer  |
| [Tokudb_CACHETABLE_POOL_CHECKPOINT_TOTAL_EXECUTION_TIME](#tokudb_cachetable_pool_checkpoint_total_execution_time)          | integer  |
| [Tokudb_LOCKTREE_MEMORY_SIZE](#tokudb_locktree_memory_size)                                     | integer  |
| [Tokudb_LOCKTREE_MEMORY_SIZE_LIMIT](#tokudb_locktree_memory_size_limit)                               | integer  |
| [Tokudb_LOCKTREE_ESCALATION_NUM](#tokudb_locktree_escalation_num)                                  | integer  |
| [Tokudb_LOCKTREE_ESCALATION_SECONDS](#tokudb_locktree_escalation_seconds)                              | numeric  |
| [Tokudb_LOCKTREE_LATEST_POST_ESCALATION_MEMORY_SIZE](#tokudb_locktree_latest_post_escalation_memory_size)              | integer  |
| [Tokudb_LOCKTREE_OPEN_CURRENT](#tokudb_locktree_open_current)                                    | integer  |
| [Tokudb_LOCKTREE_PENDING_LOCK_REQUESTS](#tokudb_locktree_pending_lock_requests)                           | integer  |
| [Tokudb_LOCKTREE_STO_ELIGIBLE_NUM](#tokudb_locktree_sto_eligible_num)                                | integer  |
| [Tokudb_LOCKTREE_STO_ENDED_NUM](#tokudb_locktree_sto_ended_num)                                   | integer  |
| [Tokudb_LOCKTREE_STO_ENDED_SECONDS](#tokudb_locktree_sto_ended_seconds)                               | numeric  |
| [Tokudb_LOCKTREE_WAIT_COUNT](#tokudb_locktree_wait_count)                                      | integer  |
| [Tokudb_LOCKTREE_WAIT_TIME](#tokudb_locktree_wait_time)                                       | integer  |
| [Tokudb_LOCKTREE_LONG_WAIT_COUNT](#tokudb_locktree_long_wait_count)                                 | integer  |
| [Tokudb_LOCKTREE_LONG_WAIT_TIME](#tokudb_locktree_long_wait_time)                                  | integer  |
| [Tokudb_LOCKTREE_TIMEOUT_COUNT](#tokudb_locktree_timeout_count)                                   | integer  |
| [Tokudb_LOCKTREE_WAIT_ESCALATION_COUNT](#tokudb_locktree_wait_escalation_count)                           | integer  |
| [Tokudb_LOCKTREE_WAIT_ESCALATION_TIME](#tokudb_locktree_wait_escalation_time)                            | integer  |
| [Tokudb_LOCKTREE_LONG_WAIT_ESCALATION_COUNT](#tokudb_locktree_long_wait_escalation_count)                      | integer  |
| [Tokudb_LOCKTREE_LONG_WAIT_ESCALATION_TIME](#tokudb_locktree_long_wait_escalation_time)                       | integer  |
| [Tokudb_DICTIONARY_UPDATES](#tokudb_dictionary_updates)                                       | integer  |
| [Tokudb_DICTIONARY_BROADCAST_UPDATES](#tokudb_dictionary_broadcast_updates)                             | integer  |
| [Tokudb_DESCRIPTOR_SET](#tokudb_descriptor_set)                                           | integer  |
| [Tokudb_MESSAGES_IGNORED_BY_LEAF_DUE_TO_MSN](#tokudb_messages_ignored_by_leaf_due_to_msn)                      | integer  |
| [Tokudb_TOTAL_SEARCH_RETRIES](#tokudb_total_search_retries)                                     | integer  |
| [Tokudb_SEARCH_TRIES_GT_HEIGHT](#tokudb_search_tries_gt_height)                                   | integer  |
| [Tokudb_SEARCH_TRIES_GT_HEIGHTPLUS3](#tokudb_search_tries_gt_heightplus3)                              | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT](#tokudb_leaf_nodes_flushed_not_checkpoint)                        | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_BYTES](#tokudb_leaf_nodes_flushed_not_checkpoint_bytes)                  | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_UNCOMPRESSED_BYTES](#tokudb_leaf_nodes_flushed_not_checkpoint_uncompressed_bytes)     | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_SECONDS](#tokudb_leaf_nodes_flushed_not_checkpoint_seconds)                | numeric  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT](#tokudb_nonleaf_nodes_flushed_to_disk_not_checkpoint)             | integer  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_BYTES](#tokudb_nonleaf_nodes_flushed_to_disk_not_checkpoint_bytes)       | integer  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_UNCOMPRESSE](#tokudb_nonleaf_nodes_flushed_to_disk_not_checkpoint_uncompresse) | integer  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_SECONDS](#tokudb_nonleaf_nodes_flushed_to_disk_not_checkpoint_seconds)     | numeric  |
| [Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT](#tokudb_leaf_nodes_flushed_checkpoint)                            | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_BYTES](#tokudb_leaf_nodes_flushed_checkpoint_bytes)                      | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_UNCOMPRESSED_BYTES](#tokudb_leaf_nodes_flushed_checkpoint_uncompressed_bytes)         | integer  |
| [Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_SECONDS](#tokudb_leaf_nodes_flushed_checkpoint_seconds)                    | numeric  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT](#tokudb_nonleaf_nodes_flushed_to_disk_checkpoint)                 | integer  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_BYTES](#tokudb_nonleaf_nodes_flushed_to_disk_checkpoint_bytes)           | integer  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_UNCOMPRESSED_BY](#tokudb_nonleaf_nodes_flushed_to_disk_checkpoint_uncompressed_by) | integer  |
| [Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_SECONDS](#tokudb_nonleaf_nodes_flushed_to_disk_checkpoint_seconds)         | numeric  |
| [Tokudb_LEAF_NODE_COMPRESSION_RATIO](#tokudb_leaf_node_compression_ratio)                              | numeric  |
| [Tokudb_NONLEAF_NODE_COMPRESSION_RATIO](#tokudb_nonleaf_node_compression_ratio)                           | numeric  |
| [Tokudb_OVERALL_NODE_COMPRESSION_RATIO](#tokudb_overall_node_compression_ratio)                           | numeric  |
| [Tokudb_NONLEAF_NODE_PARTIAL_EVICTIONS](#tokudb_nonleaf_node_partial_evictions)                           | numeric  |
| [Tokudb_NONLEAF_NODE_PARTIAL_EVICTIONS_BYTES](#tokudb_nonleaf_node_partial_evictions_bytes)                     | integer  |
| [Tokudb_LEAF_NODE_PARTIAL_EVICTIONS](#tokudb_leaf_node_partial_evictions)                              | integer  |
| [Tokudb_LEAF_NODE_PARTIAL_EVICTIONS_BYTES](#tokudb_leaf_node_partial_evictions_bytes)                        | integer  |
| [Tokudb_LEAF_NODE_FULL_EVICTIONS](#tokudb_leaf_node_full_evictions)                                 | integer  |
| [Tokudb_LEAF_NODE_FULL_EVICTIONS_BYTES](#tokudb_leaf_node_full_evictions)                           | integer  |
| [Tokudb_NONLEAF_NODE_FULL_EVICTIONS](#tokudb_leaf_node_full_evictions)                              | integer  |
| [Tokudb_NONLEAF_NODE_FULL_EVICTIONS_BYTES](#tokudb_leaf_node_full_evictions_bytes)                        | integer  |
| [Tokudb_LEAF_NODES_CREATED](#tokudb_leaf_nodes_created)                                       | integer  |
| [Tokudb_NONLEAF_NODES_CREATED](#tokudb_nonleaf_nodes_created)                                    | integer  |
| [Tokudb_LEAF_NODES_DESTROYED](#tokudb_leaf_nodes_destroyed)                                     | integer  |
| [Tokudb_NONLEAF_NODES_DESTROYED](#tokudb_nonleaf_nodes_destroyed)                                  | integer  |
| [Tokudb_MESSAGES_INJECTED_AT_ROOT_BYTES](#tokudb_messages_injected_at_root)                          | integer  |
| [Tokudb_MESSAGES_FLUSHED_FROM_H1_TO_LEAVES_BYTES](#tokudb_messages_flushed_from_h1_to_leaves_bytes)                 | integer  |
| [Tokudb_MESSAGES_IN_TREES_ESTIMATE_BYTES](#tokudb_messages_in_trees_estimate_bytes)                         | integer  |
| [Tokudb_MESSAGES_INJECTED_AT_ROOT](#tokudb_messages_injected_at_root)                                | integer  |
| [Tokudb_BROADCASE_MESSAGES_INJECTED_AT_ROOT](#tokudb_broadcase_messages_injected_at_root)                      | integer  |
| [Tokudb_BASEMENTS_DECOMPRESSED_TARGET_QUERY](#tokudb_basements_decompressed_target_query)                      | integer  |
| [Tokudb_BASEMENTS_DECOMPRESSED_PRELOCKED_RANGE](#tokudb_basements_decompressed_prelocked_range)                   | integer  |
| [Tokudb_BASEMENTS_DECOMPRESSED_PREFETCH](#tokudb_basements_decompressed_prefetch)                          | integer  |
| [Tokudb_BASEMENTS_DECOMPRESSED_FOR_WRITE](#tokudb_basements_decompressed_for_write)                         | integer  |
| [Tokudb_BUFFERS_DECOMPRESSED_TARGET_QUERY](#tokudb_buffers_decompressed_target_query)                        | integer  |
| [Tokudb_BUFFERS_DECOMPRESSED_PRELOCKED_RANGE](#tokudb_buffers_decompressed_prelocked_range)                     | integer  |
| [Tokudb_BUFFERS_DECOMPRESSED_PREFETCH](#tokudb_buffers_decompressed_prefetch)                            | integer  |
| [Tokudb_BUFFERS_DECOMPRESSED_FOR_WRITE](#tokudb_buffers_decompressed_for_write)                          | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_QUERY](#tokudb_pivots_fetched_for_query)                                 | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_QUERY_BYTES](#tokudb_pivots_fetched_for_query_bytes)                           | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_QUERY_SECONDS](#tokudb_pivots_fetched_for_query_seconds)                         | numeric  |
| [Tokudb_PIVOTS_FETCHED_FOR_PREFETCH](#tokudb_pivots_fetched_for_prefetch)                              | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_PREFETCH_BYTES](#tokudb_pivots_fetched_for_prefetch_bytes)                        | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_PREFETCH_SECONDS](#tokudb_pivots_fetched_for_prefetch_seconds)                      | numeric  |
| [Tokudb_PIVOTS_FETCHED_FOR_WRITE](#tokudb_pivots_fetched_for_write)                                 | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_WRITE_BYTES](#tokudb_pivots_fetched_for_write_bytes)                           | integer  |
| [Tokudb_PIVOTS_FETCHED_FOR_WRITE_SECONDS](#tokudb_pivots_fetched_for_write_seconds)                         | numeric  |
| [Tokudb_BASEMENTS_FETCHED_TARGET_QUERY](#tokudb_basements_fetched_target_query)                           | integer  |
| [Tokudb_BASEMENTS_FETCHED_TARGET_QUERY_BYTES](#tokudb_basements_fetched_target_query_bytes)                     | integer  |
| [Tokudb_BASEMENTS_FETCHED_TARGET_QUERY_SECONDS](#tokudb_basements_fetched_target_query_seconds)                   | numeric  |
| [Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE](#tokudb_basements_fetched_prelocked_range)                        | integer  |
| [Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE_BYTES](#tokudb_basements_fetched_prelocked_range_bytes)                  | integer  |
| [Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE_SECONDS](#tokudb_basements_fetched_prelocked_range_seconds)                | numeric  |
| [Tokudb_BASEMENTS_FETCHED_PREFETCH](#tokudb_basements_fetched_prefetch)                               | integer  |
| [Tokudb_BASEMENTS_FETCHED_PREFETCH_BYTES](#tokudb_basements_fetched_prefetch_bytes)                         | integer  |
| [Tokudb_BASEMENTS_FETCHED_PREFETCH_SECONDS](#tokudb_basements_fetched_prefetch_seconds)                       | numeric  |
| [Tokudb_BASEMENTS_FETCHED_FOR_WRITE](#tokudb_basements_fetched_for_write)                             | integer  |
| [Tokudb_BASEMENTS_FETCHED_FOR_WRITE_BYTES](#tokudb_basements_fetched_for_write_bytes)                        | integer  |
| [Tokudb_BASEMENTS_FETCHED_FOR_WRITE_SECONDS](#tokudb_basements_fetched_for_write_seconds)                      | numeric  |
| [Tokudb_BUFFERS_FETCHED_TARGET_QUERY](#tokudb_buffers_fetched_target_query)                             | integer  |
| [Tokudb_BUFFERS_FETCHED_TARGET_QUERY_BYTES](#tokudb_buffers_fetched_target_query_bytes)                       | integer  |
| [Tokudb_BUFFERS_FETCHED_TARGET_QUERY_SECONDS](#tokudb_buffers_fetched_target_query_seconds)                     | numeric  |
| [Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE](#tokudb_buffers_fetched_prelocked_range)                          | integer  |
| [Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE_BYTES](#tokudb_buffers_fetched_prelocked_range_bytes)                    | integer  |
| [Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE_SECONDS](#tokudb_buffers_fetched_prelocked_range_seconds)                  | numeric  |
| [Tokudb_BUFFERS_FETCHED_PREFETCH](#tokudb_buffers_fetched_prefetch)                                 | integer  |
| [Tokudb_BUFFERS_FETCHED_PREFETCH_BYTES](#tokudb_buffers_fetched_prefetch_bytes)                           | integer  |
| [Tokudb_BUFFERS_FETCHED_PREFETCH_SECONDS](#tokudb_buffers_fetched_prefetch_seconds)                         | numeric  |
| [Tokudb_BUFFERS_FETCHED_FOR_WRITE](#tokudb_buffers_fetched_for_write)                                | integer  |
| [Tokudb_BUFFERS_FETCHED_FOR_WRITE_BYTES](#tokudb_buffers_fetched_for_write_bytes)                          | integer  |
| [Tokudb_BUFFERS_FETCHED_FOR_WRITE_SECONDS](#tokudb_buffers_fetched_for_write_seconds)                        | integer  |
| [Tokudb_LEAF_COMPRESSION_TO_MEMORY_SECONDS](#tokudb_leaf_compression_to_memory_seconds)                       | numeric  |
| [Tokudb_LEAF_SERIALIZATION_TO_MEMORY_SECONDS](#tokudb_leaf_serialization_to_memory_seconds)                     | numeric  |
| [Tokudb_LEAF_DECOMPRESSION_TO_MEMORY_SECONDS](#tokudb_leaf_decompression_to_memory_seconds)                     | numeric  |
| [Tokudb_LEAF_DESERIALIZATION_TO_MEMORY_SECONDS](#tokudb_leaf_deserialization_to_memory_seconds)                   | numeric  |
| [Tokudb_NONLEAF_COMPRESSION_TO_MEMORY_SECONDS](#tokudb_nonleaf_compression_to_memory_seconds)                    | numeric  |
| [Tokudb_NONLEAF_SERIALIZATION_TO_MEMORY_SECONDS](#tokudb_nonleaf_serialization_to_memory_seconds)                  | numeric  |
| [Tokudb_NONLEAF_DECOMPRESSION_TO_MEMORY_SECONDS](#tokudb_nonleaf_decompression_to_memory_seconds)                  | numeric  |
| [Tokudb_NONLEAF_DESERIALIZATION_TO_MEMORY_SECONDS](#tokudb_nonleaf_deserialization_to_memory_seconds)                | numeric  |
| [Tokudb_PROMOTION_ROOTS_SPLIT](#tokudb_promotion_roots_split)                                    | integer  |
| [Tokudb_PROMOTION_LEAF_ROOTS_INJECTED_INTO](#tokudb_promotion_leaf_roots_injected_into)                       | integer  |
| [Tokudb_PROMOTION_H1_ROOTS_INJECTED_INTO](#tokudb_promotion_h1_roots_injected_into)                         | integer  |
| [Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_0](#tokudb_promotion_injections_at_depth_0)                          | integer  |
| [Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_1](#tokudb_promotion_injections_at_depth_1)                          | integer  |
| [Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_2](#tokudb_promotion_injections_at_depth_2)                          | integer  |
| [Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_3](#tokudb_promotion_injections_at_depth_3)                          | integer  |
| [Tokudb_PROMOTION_INJECTIONS_LOWER_THAN_DEPTH_3](#tokudb_promotion_injections_lower_than_depth_3)                  | integer  |
| [Tokudb_PROMOTION_STOPPED_NONEMPTY_BUFFER](#tokudb_promotion_stopped_nonempty_buffer)                        | integer  |
| [Tokudb_PROMOTION_STOPPED_AT_HEIGHT_1](#tokudb_promotion_stopped_at_height_1)                           | integer  |
| [Tokudb_PROMOTION_STOPPED_CHILD_LOCKED_OR_NOT_IN_MEMORY](#tokudb_promotion_stopped_child_locked_or_not_in_memory)          | integer  |
| [Tokudb_PROMOTION_STOPPED_CHILD_NOT_FULLY_IN_MEMORY](#tokudb_promotion_stopped_child_not_fully_in_memory)              | integer  |
| [Tokudb_PROMOTION_STOPPED_AFTER_LOCKING_CHILD](#tokudb_promotion_stopped_after_locking_child)                    | integer  |
| [Tokudb_BASEMENT_DESERIALIZATION_FIXED_KEY](#tokudb_basement_deserialization_fixed_key)                       | integer  |
| [Tokudb_BASEMENT_DESERIALIZATION_VARIABLE_KEY](#tokudb_basement_deserialization_variable_key)                    | integer  |
| [Tokudb_PRO_RIGHTMOST_LEAF_SHORTCUT_SUCCESS](#tokudb_pro_rightmost_leaf_shortcut_success)                      | integer  |
| [Tokudb_PRO_RIGHTMOST_LEAF_SHORTCUT_FAIL_POS](#tokudb_pro_rightmost_leaf_shortcut_fail_pos)                     | integer  |
| [Tokudb_RIGHTMOST_LEAF_SHORTCUT_FAIL_REACTIVE](#tokudb_rightmost_leaf_shortcut_fail_reactive)                    | integer  |
| [Tokudb_CURSOR_SKIP_DELETED_LEAF_ENTRY](#tokudb_cursor_skip_deleted_leaf_entry)                           | integer  |
| [Tokudb_FLUSHER_CLEANER_TOTAL_NODES](#tokudb_flusher_cleaner_total_nodes)                              | integer  |
| [Tokudb_FLUSHER_CLEANER_H1_NODES](#tokudb_flusher_cleaner_h1_nodes)                                 | integer  |
| [Tokudb_FLUSHER_CLEANER_HGT1_NODES](#tokudb_flusher_cleaner_hgt1_nodes)                               | integer  |
| [Tokudb_FLUSHER_CLEANER_EMPTY_NODES](#tokudb_flusher_cleaner_empty_nodes)                              | integer  |
| [Tokudb_FLUSHER_CLEANER_NODES_DIRTIED](#tokudb_flusher_cleaner_nodes_dirtied)                            | integer  |
| [Tokudb_FLUSHER_CLEANER_MAX_BUFFER_SIZE](#tokudb_flusher_cleaner_max_buffer_size)                          | integer  |
| [Tokudb_FLUSHER_CLEANER_MIN_BUFFER_SIZE](#tokudb_flusher_cleaner_min_buffer_size)                          | integer  |
| [Tokudb_FLUSHER_CLEANER_TOTAL_BUFFER_SIZE](#tokudb_flusher_cleaner_total_buffer_size)                        | integer  |
| [Tokudb_FLUSHER_CLEANER_MAX_BUFFER_WORKDONE](#tokudb_flusher_cleaner_max_buffer_workdone)                      | integer  |
| [Tokudb_FLUSHER_CLEANER_MIN_BUFFER_WORKDONE](#tokudb_flusher_cleaner_min_buffer_workdone)                      | integer  |
| [Tokudb_FLUSHER_CLEANER_TOTAL_BUFFER_WORKDONE](#tokudb_flusher_cleaner_total_buffer_workdone)                    | integer  |
| [Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_STARTED](#tokudb_flusher_cleaner_num_leaf_merges_started)                  | integer  |
| [Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_RUNNING](#tokudb_flusher_cleaner_num_leaf_merges_running)                  | integer  |
| [Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_COMPLETED](#tokudb_flusher_cleaner_num_leaf_merges_completed)                | integer  |
| [Tokudb_FLUSHER_CLEANER_NUM_DIRTIED_FOR_LEAF_MERGE](#tokudb_flusher_cleaner_num_dirtied_for_leaf_merge)               | integer  |
| [Tokudb_FLUSHER_FLUSH_TOTAL](#tokudb_flusher_flush_total)                                      | integer  |
| [Tokudb_FLUSHER_FLUSH_IN_MEMORY](#tokudb_flusher_flush_in_memory)                                  | integer  |
| [Tokudb_FLUSHER_FLUSH_NEEDED_IO](#tokudb_flusher_flush_needed_io)                                  | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES](#tokudb_flusher_flush_cascades)                                   | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES_1](#tokudb_flusher_flush_cascades_1)                                 | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES_2](#tokudb_flusher_flush_cascades_2)                                 | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES_3](#tokudb_flusher_flush_cascades_3)                                 | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES_4](#tokudb_flusher_flush_cascades_4)                                 | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES_5](#tokudb_flusher_flush_cascades_5)                                 | integer  |
| [Tokudb_FLUSHER_FLUSH_CASCADES_GT_5](#tokudb_flusher_flush_cascades_gt_5)                              | integer  |
| [Tokudb_FLUSHER_SPLIT_LEAF](#tokudb_flusher_split_leaf)                                       | integer  |
| [Tokudb_FLUSHER_SPLIT_NONLEAF](#tokudb_flusher_split_nonleaf)                                    | integer  |
| [Tokudb_FLUSHER_MERGE_LEAF](#tokudb_flusher_merge_leaf)                                       | integer  |
| [Tokudb_FLUSHER_MERGE_NONLEAF](#tokudb_flusher_merge_nonleaf)                                   | integer  |
| [Tokudb_FLUSHER_BALANCE_LEAF](#tokudb_flusher_balance_leaf)                                     | integer  |
| [Tokudb_HOT_NUM_STARTED](#tokudb_hot_num_started)                                          | integer  |
| [Tokudb_HOT_NUM_COMPLETED](#tokudb_hot_num_completed)                                        | integer  |
| [Tokudb_HOT_NUM_ABORTED](#tokudb_hot_num_aborted)                                          | integer  |
| [Tokudb_HOT_MAX_ROOT_FLUSH_COUNT](#tokudb_hot_max_root_flush_count)                                 | integer  |
| [Tokudb_TXN_BEGIN](#tokudb_txn_begin)                                                | integer  |
| [Tokudb_TXN_BEGIN_READ_ONLY](#tokudb_txn_begin_read_only)                                      | integer  |
| [Tokudb_TXN_COMMITS](#tokudb_txn_commits)                                              | integer  |
| [Tokudb_TXN_ABORTS](#tokudb_txn_aborts)                                               | integer  |
| [Tokudb_LOGGER_NEXT_LSN](#tokudb_logger_next_lsn)                                          | integer  |
| [Tokudb_LOGGER_WRITES](#tokudb_logger_writes)                                            | integer  |
| [Tokudb_LOGGER_WRITES_BYTES](#tokudb_logger_writes_bytes)                                      | integer  |
| [Tokudb_LOGGER_WRITES_UNCOMPRESSED_BYTES](#tokudb_logger_writes_uncompressed_bytes)                         | integer  |
| [Tokudb_LOGGER_WRITES_SECONDS](#tokudb_logger_writes_seconds)                                    | numeric  |
| [Tokudb_LOGGER_WAIT_LONG](#tokudb_logger_wait_long)                                         | integer  |
| [Tokudb_LOADER_NUM_CREATED](#tokudb_loader_num_created)                                       | integer  |
| [Tokudb_LOADER_NUM_CURRENT](#tokudb_loader_num_current)                                       | integer  |
| [Tokudb_LOADER_NUM_MAX](#tokudb_loader_num_max)                                           | integer  |
| [Tokudb_MEMORY_MALLOC_COUNT](#tokudb_memory_malloc_count)                                      | integer  |
| [Tokudb_MEMORY_FREE_COUNT](#tokudb_memory_free_count)                                        | integer  |
| [Tokudb_MEMORY_REALLOC_COUNT](#tokudb_memory_realloc_count)                                     | integer  |
| [Tokudb_MEMORY_MALLOC_FAIL](#tokudb_memory_malloc_fail)                                       | integer  |
| [Tokudb_MEMORY_REALLOC_FAIL](#tokudb_memory_realloc_fail)                                      | integer  |
| [Tokudb_MEMORY_REQUESTED](#tokudb_memory_requested)                                         | integer  |
| [Tokudb_MEMORY_USED](#tokudb_memory_used)                                             | integer  |
| [Tokudb_MEMORY_FREED](#tokudb_memory_freed)                                             | integer  |
| [Tokudb_MEMORY_MAX_REQUESTED_SIZE](#tokudb_memory_max_requested_size)                                | integer  |
| [Tokudb_MEMORY_LAST_FAILED_SIZE](#tokudb_memory_last_failed_size)                                  | integer  |
| [Tokudb_MEM_ESTIMATED_MAXIMUM_MEMORY_FOOTPRINT](#tokudb_mem_estimated_maximum_memory_footprint)                   | integer  |
| [Tokudb_MEMORY_MALLOCATOR_VERSION](#tokudb_memory_mallocator_version)                                | string   |
| [Tokudb_MEMORY_MMAP_THRESHOLD](#tokudb_memory_mmap_threshold)                                 | integer  |
| [Tokudb_FILESYSTEM_THREADS_BLOCKED_BY_FULL_DISK](#tokudb_filesystem_threads_blocked_by_full_disk)                  | integer  |
| [Tokudb_FILESYSTEM_FSYNC_TIME](#tokudb_filesystem_fsync_time)                                    | integer  |
| [Tokudb_FILESYSTEM_FSYNC_NUM](#tokudb_filesystem_fsync_num)                                     | integer  |
| [Tokudb_FILESYSTEM_LONG_FSYNC_TIME](#tokudb_filesystem_fsync_time)                               | integer  |
| [Tokudb_FILESYSTEM_LONG_FSYNC_NUM](#tokudb_filesystem_long_fsync_num)                                | integer  |

### `Tokudb_DB_OPENS`

This variable shows the number of times an individual PerconaFT dictionary file
was opened. This is a not a useful value for a regular user to use for any
purpose due to layers of open/close caching on top.

### `Tokudb_DB_CLOSES`

This variable shows the number of times an individual PerconaFT dictionary file
was closed. This is a not a useful value for a regular user to use for any
purpose due to layers of open/close caching on top.

### `Tokudb_DB_OPEN_CURRENT`

This variable shows the number of currently opened databases.

### `Tokudb_DB_OPEN_MAX`

This variable shows the maximum number of concurrently opened databases.

### `Tokudb_LEAF_ENTRY_MAX_COMMITTED_XR`

This variable shows the maximum number of committed transaction records that
were stored on disk in a new or modified row.

### `Tokudb_LEAF_ENTRY_MAX_PROVISIONAL_XR`

This variable shows the maximum number of provisional transaction records that
were stored on disk in a new or modified row.

### `Tokudb_LEAF_ENTRY_EXPANDED`

This variable shows the number of times that an expanded memory mechanism was
used to store a new or modified row on disk.

### `Tokudb_LEAF_ENTRY_MAX_MEMSIZE`

This variable shows the maximum number of bytes that were stored on disk as a
new or modified row. This is the maximum uncompressed size of any row stored in
*TokuDB* that was created or modified since the server started.

### `Tokudb_LEAF_ENTRY_APPLY_GC_BYTES_IN`

This variable shows the total number of bytes of leaf nodes data before
performing garbage collection for non-flush events.

### `Tokudb_LEAF_ENTRY_APPLY_GC_BYTES_OUT`

This variable shows the total number of bytes of leaf nodes data after
performing garbage collection for non-flush events.

### `Tokudb_LEAF_ENTRY_NORMAL_GC_BYTES_IN`

This variable shows the total number of bytes of leaf nodes data before
performing garbage collection for flush events.

### `Tokudb_LEAF_ENTRY_NORMAL_GC_BYTES_OUT`

This variable shows the total number of bytes of leaf nodes data after
performing garbage collection for flush events.

### `Tokudb_CHECKPOINT_PERIOD`

This variable shows the interval in seconds between the end of an automatic
checkpoint and the beginning of the next automatic checkpoint.

### `Tokudb_CHECKPOINT_FOOTPRINT`

This variable shows at what stage the checkpointer is at. It’s used for
debugging purposes only and not a useful value for a normal user.

### `Tokudb_CHECKPOINT_LAST_BEGAN`

This variable shows the time the last checkpoint began. If a checkpoint is
currently in progress, then this time may be later than the time the last
checkpoint completed. If no checkpoint has ever taken place, then this value
will be `Dec 31, 1969` on Linux hosts.

### `Tokudb_CHECKPOINT_LAST_COMPLETE_BEGAN`

This variable shows the time the last complete checkpoint started. Any data
that changed after this time will not be captured in the checkpoint.

### `Tokudb_CHECKPOINT_LAST_COMPLETE_ENDED`

This variable shows the time the last complete checkpoint ended.

### `Tokudb_CHECKPOINT_DURATION`

This variable shows time (in seconds) required to complete all
checkpoints.

### `Tokudb_CHECKPOINT_DURATION_LAST`

This variable shows time (in seconds) required to complete the last
checkpoint.

### `Tokudb_CHECKPOINT_LAST_LSN`

This variable shows the last successful checkpoint LSN. Each checkpoint from
the time the PerconaFT environment is created has a monotonically incrementing
LSN. This is not a useful value for a normal user to use for any purpose other
than having some idea of how many checkpoints have occurred since the system
was first created.

### `Tokudb_CHECKPOINT_TAKEN`

This variable shows the number of complete checkpoints that have been taken.

### `Tokudb_CHECKPOINT_FAILED`

This variable shows the number of checkpoints that have failed for any reason.

### `Tokudb_CHECKPOINT_WAITERS_NOW`

This variable shows the current number of threads waiting for the `checkpoint
safe` lock. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_CHECKPOINT_WAITERS_MAX`

This variable shows the maximum number of threads that concurrently waited for
the `checkpoint safe` lock. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_CHECKPOINT_CLIENT_WAIT_ON_MO`

This variable shows the number of times a non-checkpoint client thread waited
for the multi-operation lock. It is an internal `rwlock` that is similar in
nature to the *InnoDB* kernel mutex, it effectively halts all access to the
PerconaFT API when write locked. The `begin` phase of the checkpoint takes
this lock for a brief period.

### `Tokudb_CHECKPOINT_CLIENT_WAIT_ON_CS`

This variable shows the number of times a non-checkpoint client thread waited
for the checkpoint-safe lock. This is the lock taken when you `SET
tokudb_checkpoint_lock=1`. If a client trying to lock/postpone the
checkpointer has to wait for the currently running checkpoint to complete, that
wait time will be reflected here and summed. This is not a useful metric as
regular users should never be manipulating the checkpoint lock.

### `Tokudb_CHECKPOINT_BEGIN_TIME`

This variable shows the cumulative time (in microseconds) required to mark all
dirty nodes as pending a checkpoint.

### `Tokudb_CHECKPOINT_LONG_BEGIN_TIME`

This variable shows the cumulative actual time (in microseconds) of checkpoint
`begin` stages that took longer than 1 second.

### `Tokudb_CHECKPOINT_LONG_BEGIN_COUNT`

This variable shows the number of checkpoints whose `begin` stage took longer
than 1 second.

### `Tokudb_CHECKPOINT_END_TIME`

This variable shows the time spent in checkpoint end operation in seconds.

### `Tokudb_CHECKPOINT_LONG_END_TIME`

This variable shows the total time of long checkpoints in seconds.

### `Tokudb_CHECKPOINT_LONG_END_COUNT`

This variable shows the number of checkpoints whose `end_checkpoint`
operations exceeded 1 minute.

### `Tokudb_CACHETABLE_MISS`

This variable shows the number of times the application was unable to access
the data in the internal cache. A cache miss means that date will need to be
read from disk.

### `Tokudb_CACHETABLE_MISS_TIME`

This variable shows the total time, in microseconds, of how long the database
has had to wait for a disk read to complete.

### `Tokudb_CACHETABLE_PREFETCHES`

This variable shows the total number of times that a block of memory has been
prefetched into the database’s cache. Data is prefetched when the database’s
algorithms determine that a block of memory is likely to be accessed by the
application.

### `Tokudb_CACHETABLE_SIZE_CURRENT`

This variable shows how much of the uncompressed data, in bytes, is
currently in the database’s internal cache.

### `Tokudb_CACHETABLE_SIZE_LIMIT`

This variable shows how much of the uncompressed data, in bytes, will fit in
the database’s internal cache.

### `Tokudb_CACHETABLE_SIZE_WRITING`

This variable shows the number of bytes that are currently queued up to be
written to disk.

### `Tokudb_CACHETABLE_SIZE_NONLEAF`

This variable shows the amount of memory, in bytes, the current set of non-leaf
nodes occupy in the cache.

### `Tokudb_CACHETABLE_SIZE_LEAF`

This variable shows the amount of memory, in bytes, the current set of
(decompressed) leaf nodes occupy in the cache.

### `Tokudb_CACHETABLE_SIZE_ROLLBACK`

This variable shows the rollback nodes size, in bytes, in the cache.

### `Tokudb_CACHETABLE_SIZE_CACHEPRESSURE`

This variable shows the number of bytes causing cache pressure (the sum of
buffers and work done counters), helps to understand if cleaner threads are
keeping up with workload. It should really be looked at as more of a value to
use in a ratio of cache pressure / cache table size. The closer that ratio
evaluates to 1, the higher the cache pressure.

### `Tokudb_CACHETABLE_SIZE_CLONED`

This variable shows the amount of memory, in bytes, currently used for cloned
nodes. During the checkpoint operation, dirty nodes are cloned prior to
serialization/compression, then written to disk. After which, the memory for
the cloned block is returned for re-use.

### `Tokudb_CACHETABLE_EVICTIONS`

This variable shows the number of blocks evicted from cache. On its own this is
not a useful number as its impact on performance depends entirely on the
hardware and workload in use. For example, two workloads, one random, one
linear for the same starting data set will have two wildly different eviction
patterns.

### `Tokudb_CACHETABLE_CLEANER_EXECUTIONS`

This variable shows the total number of times the cleaner thread loop has
executed.

### `Tokudb_CACHETABLE_CLEANER_PERIOD`

*TokuDB* includes a cleaner thread that optimizes indexes in the background.
This variable is the time, in seconds, between the completion of a group of
cleaner operations and the beginning of the next group of cleaner operations.
The cleaner operations run on a background thread performing work that does not
need to be done on the client thread.

### `Tokudb_CACHETABLE_CLEANER_ITERATIONS`

This variable shows the number of cleaner operations that are performed every
cleaner period.

### `Tokudb_CACHETABLE_WAIT_PRESSURE_COUNT`

This variable shows the number of times a thread was stalled due to cache
pressure.

### `Tokudb_CACHETABLE_WAIT_PRESSURE_TIME`

This variable shows the total time, in microseconds, waiting on cache pressure
to subside.

### `Tokudb_CACHETABLE_LONG_WAIT_PRESSURE_COUNT`

This variable shows the number of times a thread was stalled for more than one
second due to cache pressure.

### `Tokudb_CACHETABLE_LONG_WAIT_PRESSURE_TIME`

This variable shows the total time, in microseconds, waiting on cache pressure
to subside for more than one second.

### `Tokudb_CACHETABLE_POOL_CLIENT_NUM_THREADS`

This variable shows the number of threads in the client thread pool.

### `Tokudb_CACHETABLE_POOL_CLIENT_NUM_THREADS_ACTIVE`

This variable shows the number of currently active threads in the client
thread pool.

### `Tokudb_CACHETABLE_POOL_CLIENT_QUEUE_SIZE`

This variable shows the number of currently queued work items in the client
thread pool.

### `Tokudb_CACHETABLE_POOL_CLIENT_MAX_QUEUE_SIZE`

This variable shows the largest number of queued work items in the client
thread pool.

### `Tokudb_CACHETABLE_POOL_CLIENT_TOTAL_ITEMS_PROCESSED`

This variable shows the total number of work items processed in the client
thread pool.

### `Tokudb_CACHETABLE_POOL_CLIENT_TOTAL_EXECUTION_TIME`

This variable shows the total execution time of processing work items in the
client thread pool.

### `Tokudb_CACHETABLE_POOL_CACHETABLE_NUM_THREADS`

This variable shows the number of threads in the cachetable threadpool.

### `Tokudb_CACHETABLE_POOL_CACHETABLE_NUM_THREADS_ACTIVE`

This variable shows the number of currently active threads in the cachetable
thread pool.

### `Tokudb_CACHETABLE_POOL_CACHETABLE_QUEUE_SIZE`

This variable shows the number of currently queued work items in the cachetable
thread pool.

### `Tokudb_CACHETABLE_POOL_CACHETABLE_MAX_QUEUE_SIZE`

This variable shows the largest number of queued work items in the cachetable
thread pool.

### `Tokudb_CACHETABLE_POOL_CACHETABLE_TOTAL_ITEMS_PROCESSED`

This variable shows the total number of work items processed in the cachetable
thread pool.

### `Tokudb_CACHETABLE_POOL_CACHETABLE_TOTAL_EXECUTION_TIME`

This variable shows the total execution time of processing work items in the
cachetable thread pool.

### `Tokudb_CACHETABLE_POOL_CHECKPOINT_NUM_THREADS`

This variable shows the number of threads in the checkpoint threadpool.

### `Tokudb_CACHETABLE_POOL_CHECKPOINT_NUM_THREADS_ACTIVE`

This variable shows the number of currently active threads in the checkpoint
thread pool.

### `Tokudb_CACHETABLE_POOL_CHECKPOINT_QUEUE_SIZE`

This variable shows the number of currently queued work items in the checkpoint
thread pool.

### `Tokudb_CACHETABLE_POOL_CHECKPOINT_MAX_QUEUE_SIZE`

This variable shows the largest number of queued work items in the checkpoint
thread pool.

### `Tokudb_CACHETABLE_POOL_CHECKPOINT_TOTAL_ITEMS_PROCESSED`

This variable shows the total number of work items processed in the checkpoint
thread pool.

### `Tokudb_CACHETABLE_POOL_CHECKPOINT_TOTAL_EXECUTION_TIME`

This variable shows the total execution time of processing work items in the
checkpoint thread pool.

### `Tokudb_LOCKTREE_MEMORY_SIZE`

This variable shows the amount of memory, in bytes, that the locktree is
currently using.

### `Tokudb_LOCKTREE_MEMORY_SIZE_LIMIT`

This variable shows the maximum amount of memory, in bytes, that the locktree
is allowed to use.

### `Tokudb_LOCKTREE_ESCALATION_NUM`

This variable shows the number of times the locktree needed to run lock
escalation to reduce its memory footprint.

### `Tokudb_LOCKTREE_ESCALATION_SECONDS`

This variable shows the total number of seconds spent performing locktree
escalation.

### `Tokudb_LOCKTREE_LATEST_POST_ESCALATION_MEMORY_SIZE`

This variable shows the locktree size, in bytes, after most current locktree
escalation.

### `Tokudb_LOCKTREE_OPEN_CURRENT`

This variable shows the number of locktrees that are currently opened.

### `Tokudb_LOCKTREE_PENDING_LOCK_REQUESTS`

This variable shows the number of requests waiting for a lock grant.

### `Tokudb_LOCKTREE_STO_ELIGIBLE_NUM`

This variable shows the number of locktrees eligible for `Single Transaction
optimizations`. STO optimization are behaviors that can happen within the
locktree when there is exactly one transaction active within the locktree. This
is a not a useful value for a regular user to use for any purpose.

### `Tokudb_LOCKTREE_STO_ENDED_NUM`

This variable shows the total number of times a `Single Transaction
Optimization` was ended early due to another transaction starting. STO
optimization are behaviors that can happen within the locktree when there is
exactly one transaction active within the locktree. This is a not a useful
value for a regular user to use for any purpose.

### `Tokudb_LOCKTREE_STO_ENDED_SECONDS`

This variable shows the total number of seconds ending the `Single
Transaction Optimizations`. STO optimization are behaviors that can happen
within the locktree when there is exactly one transaction active within the
locktree. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_LOCKTREE_WAIT_COUNT`

This variable shows the number of times that a lock request could not be
acquired because of a conflict with some other transaction. PerconaFT lock
request  cycles to try to obtain a lock, if it can not get a lock, it
sleeps/waits and times out, checks to get the lock again, repeat. This value
indicates the number of cycles it needed to execute before it obtained the
lock.

### `Tokudb_LOCKTREE_WAIT_TIME`

This variable shows the total time, in microseconds, spent by client waiting
for a lock conflict to be resolved.

### `Tokudb_LOCKTREE_LONG_WAIT_COUNT`

This variable shows number of lock waits greater than one second in duration.

### `Tokudb_LOCKTREE_LONG_WAIT_TIME`

This variable shows the total time, in microseconds, of the long waits.

### `Tokudb_LOCKTREE_TIMEOUT_COUNT`

This variable shows the number of times that a lock request timed out.

### `Tokudb_LOCKTREE_WAIT_ESCALATION_COUNT`

When the sum of the sizes of locks taken reaches the lock tree limit, we run
lock escalation on a background thread. The clients threads need to wait for
escalation to consolidate locks and free up memory. This variables shows the
number of times a client thread had to wait on lock escalation.

### `Tokudb_LOCKTREE_WAIT_ESCALATION_TIME`

This variable shows the total time, in microseconds, that a client thread spent
waiting for lock escalation to free up memory.

### `Tokudb_LOCKTREE_LONG_WAIT_ESCALATION_COUNT`

This variable shows number of times that a client thread had to wait on lock
escalation and the wait time was greater than one second.

### `Tokudb_LOCKTREE_LONG_WAIT_ESCALATION_TIME`

This variable shows the total time, in microseconds, of the long waits for lock
escalation to free up memory.

### `Tokudb_DICTIONARY_UPDATES`

This variable shows the total number of rows that have been updated in all
primary and secondary indexes combined, if those updates have been done with a
separate recovery log entry per index.

### `Tokudb_DICTIONARY_BROADCAST_UPDATES`

This variable shows the number of broadcast updates that have been successfully
performed. A broadcast update is an update that affects all rows in a
dictionary.

### `Tokudb_DESCRIPTOR_SET`

This variable shows the number of time a descriptor was updated when the entire
dictionary was updated (for example, when the schema has been changed).

### `Tokudb_MESSAGES_IGNORED_BY_LEAF_DUE_TO_MSN`

This variable shows the number of messages that were ignored by a leaf because
it had already been applied.

### `Tokudb_TOTAL_SEARCH_RETRIES`

Internal value that is no use to anyone other than a developer debugging a
specific query/search issue.

### `Tokudb_SEARCH_TRIES_GT_HEIGHT`

Internal value that is no use to anyone other than a developer debugging a
specific query/search issue.

### `Tokudb_SEARCH_TRIES_GT_HEIGHTPLUS3`

Internal value that is no use to anyone other than a developer debugging a
specific query/search issue.

### `Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT`

This variable shows the number of leaf nodes flushed to disk, not for
checkpoint.

### `Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_BYTES`

This variable shows the size, in bytes, of leaf nodes flushed to disk, not
for checkpoint.

### `Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_UNCOMPRESSED_BYTES`

This variable shows the size, in bytes, of uncompressed leaf nodes flushed to
disk not for checkpoint.

### `Tokudb_LEAF_NODES_FLUSHED_NOT_CHECKPOINT_SECONDS`

This variable shows the number of seconds waiting for I/O when writing leaf
nodes flushed to disk, not for checkpoint

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT`

This variable shows the number of non-leaf nodes flushed to disk, not for
checkpoint.

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_BYTES`

This variable shows the size, in bytes, of non-leaf nodes flushed to disk, not
for checkpoint.

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_UNCOMPRESSE`

This variable shows the size, in bytes, of uncompressed non-leaf nodes flushed
to disk not for checkpoint.

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_NOT_CHECKPOINT_SECONDS`

This variable shows the number of seconds waiting for I/O when writing non-leaf
nodes flushed to disk, not for checkpoint

### `Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT`

This variable shows the number of leaf nodes flushed to disk, for checkpoint.

### `Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_BYTES`

This variable shows the size, in bytes, of leaf nodes flushed to disk, for
checkpoint.

### `Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_UNCOMPRESSED_BYTES`

This variable shows the size, in bytes, of uncompressed leaf nodes flushed to
disk for checkpoint.

### `Tokudb_LEAF_NODES_FLUSHED_CHECKPOINT_SECONDS`

This variable shows the number of seconds waiting for I/O when writing leaf
nodes flushed to disk for checkpoint

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT`

This variable shows the number of non-leaf nodes flushed to disk, for
checkpoint.

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_BYTES`

This variable shows the size, in bytes, of non-leaf nodes flushed to disk, for
checkpoint.

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_UNCOMPRESSED_BY`

This variable shows the size, in bytes, of uncompressed non-leaf nodes flushed
to disk for checkpoint.

### `Tokudb_NONLEAF_NODES_FLUSHED_TO_DISK_CHECKPOINT_SECONDS`

This variable shows the number of seconds waiting for I/O when writing non-leaf
nodes flushed to disk for checkpoint

### `Tokudb_LEAF_NODE_COMPRESSION_RATIO`

This variable shows the ratio of uncompressed bytes (in-memory) to compressed
bytes (on-disk) for leaf nodes.

### `Tokudb_NONLEAF_NODE_COMPRESSION_RATIO`

This variable shows the ratio of uncompressed bytes (in-memory) to compressed
bytes (on-disk) for non-leaf nodes.

### `Tokudb_OVERALL_NODE_COMPRESSION_RATIO`

This variable shows the ratio of uncompressed bytes (in-memory) to compressed
bytes (on-disk) for all nodes.

### `Tokudb_NONLEAF_NODE_PARTIAL_EVICTIONS`

This variable shows the number of times a partition of a non-leaf node was
evicted from the cache.

### `Tokudb_NONLEAF_NODE_PARTIAL_EVICTIONS_BYTES`

This variable shows the amount, in bytes, of memory freed by evicting
partitions of non-leaf nodes from the cache.

### `Tokudb_LEAF_NODE_PARTIAL_EVICTIONS`

This variable shows the number of times a partition of a leaf node was evicted
from the cache.

### `Tokudb_LEAF_NODE_PARTIAL_EVICTIONS_BYTES`

This variable shows the amount, in bytes, of memory freed by evicting
partitions of leaf nodes from the cache.

### `Tokudb_LEAF_NODE_FULL_EVICTIONS`

This variable shows the number of times a full leaf node was evicted from the
cache.

### `Tokudb_LEAF_NODE_FULL_EVICTIONS_BYTES`

This variable shows the amount, in bytes, of memory freed by evicting full leaf
nodes from the cache.

### `Tokudb_NONLEAF_NODE_FULL_EVICTIONS`

This variable shows the number of times a full non-leaf node was evicted from
the cache.

### `Tokudb_NONLEAF_NODE_FULL_EVICTIONS_BYTES`

This variable shows the amount, in bytes, of memory freed by evicting full
non-leaf nodes from the cache.

### `Tokudb_LEAF_NODES_CREATED`

This variable shows the number of created leaf nodes.

### `Tokudb_NONLEAF_NODES_CREATED`

This variable shows the number of created non-leaf nodes.

### `Tokudb_LEAF_NODES_DESTROYED`

This variable shows the number of destroyed leaf nodes.

### `Tokudb_NONLEAF_NODES_DESTROYED`

This variable shows the number of destroyed non-leaf nodes.

### `Tokudb_MESSAGES_INJECTED_AT_ROOT_BYTES`

This variable shows the size, in bytes, of messages injected at root (for all
trees).

### `Tokudb_MESSAGES_FLUSHED_FROM_H1_TO_LEAVES_BYTES`

This variable shows the size, in bytes, of messages flushed from `h1` nodes
to leaves.

### `Tokudb_MESSAGES_IN_TREES_ESTIMATE_BYTES`

This variable shows the estimated size, in bytes, of messages currently in
trees.

### `Tokudb_MESSAGES_INJECTED_AT_ROOT`

This variables shows the number of messages that were injected at root node of
a tree.

### `Tokudb_BROADCASE_MESSAGES_INJECTED_AT_ROOT`

This variable shows the number of broadcast messages dropped into the root node
of a tree. These are things such as the result of `OPTIMIZE TABLE` and a few
other operations. This is not a useful metric for a regular user to use for any
purpose.

### `Tokudb_BASEMENTS_DECOMPRESSED_TARGET_QUERY`

This variable shows the number of basement nodes decompressed for queries.

### `Tokudb_BASEMENTS_DECOMPRESSED_PRELOCKED_RANGE`

This variable shows the number of basement nodes aggressively decompressed by
queries.

### `Tokudb_BASEMENTS_DECOMPRESSED_PREFETCH`

This variable shows the number of basement nodes decompressed by a prefetch
thread.

### `Tokudb_BASEMENTS_DECOMPRESSED_FOR_WRITE`

This variable shows the number of basement nodes decompressed for writes.

### `Tokudb_BUFFERS_DECOMPRESSED_TARGET_QUERY`

This variable shows the number of buffers decompressed for queries.

### `Tokudb_BUFFERS_DECOMPRESSED_PRELOCKED_RANGE`

This variable shows the number of buffers decompressed by queries aggressively.

### `Tokudb_BUFFERS_DECOMPRESSED_PREFETCH`

This variable shows the number of buffers decompressed by a prefetch thread.

### `Tokudb_BUFFERS_DECOMPRESSED_FOR_WRITE`

This variable shows the number of buffers decompressed for writes.

### `Tokudb_PIVOTS_FETCHED_FOR_QUERY`

This variable shows the number of pivot nodes fetched for queries.

### `Tokudb_PIVOTS_FETCHED_FOR_QUERY_BYTES`

This variable shows the number of bytes of pivot nodes fetched for queries.

### `Tokudb_PIVOTS_FETCHED_FOR_QUERY_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching pivot
nodes for queries.

### `Tokudb_PIVOTS_FETCHED_FOR_PREFETCH`

This variable shows the number of pivot nodes fetched by a prefetch thread.

### `Tokudb_PIVOTS_FETCHED_FOR_PREFETCH_BYTES`

This variable shows the number of bytes of pivot nodes fetched for queries.

### `Tokudb_PIVOTS_FETCHED_FOR_PREFETCH_SECONDS`

This variable shows the number seconds waiting for I/O when fetching pivot
nodes by a prefetch thread.

### `Tokudb_PIVOTS_FETCHED_FOR_WRITE`

This variable shows the number of pivot nodes fetched for writes.

### `Tokudb_PIVOTS_FETCHED_FOR_WRITE_BYTES`

This variable shows the number of bytes of pivot nodes fetched for writes.

### `Tokudb_PIVOTS_FETCHED_FOR_WRITE_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching pivot
nodes for writes.

### `Tokudb_BASEMENTS_FETCHED_TARGET_QUERY`

This variable shows the number of basement nodes fetched from disk for queries.

### `Tokudb_BASEMENTS_FETCHED_TARGET_QUERY_BYTES`

This variable shows the number of basement node bytes fetched from disk for
queries.

### `Tokudb_BASEMENTS_FETCHED_TARGET_QUERY_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching
basement nodes from disk for queries.

### `Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE`

This variable shows the number of basement nodes fetched from disk
aggressively.

### `Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE_BYTES`

This variable shows the number of basement node bytes fetched from disk
aggressively.

### `Tokudb_BASEMENTS_FETCHED_PRELOCKED_RANGE_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching
basement nodes from disk aggressively.

### `Tokudb_BASEMENTS_FETCHED_PREFETCH`

This variable shows the number of basement nodes fetched from disk by a
prefetch thread.

### `Tokudb_BASEMENTS_FETCHED_PREFETCH_BYTES`

This variable shows the number of basement node bytes fetched from disk by a
prefetch thread.

### `Tokudb_BASEMENTS_FETCHED_PREFETCH_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching
basement nodes from disk by a prefetch thread.

### `Tokudb_BASEMENTS_FETCHED_FOR_WRITE`

This variable shows the number of buffers fetched from disk for writes.

### `Tokudb_BASEMENTS_FETCHED_FOR_WRITE_BYTES`

This variable shows the number of buffer bytes fetched from disk for writes.

### `Tokudb_BASEMENTS_FETCHED_FOR_WRITE_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching buffers
from disk for writes.

### `Tokudb_BUFFERS_FETCHED_TARGET_QUERY`

This variable shows the number of buffers fetched from disk for queries.

### `Tokudb_BUFFERS_FETCHED_TARGET_QUERY_BYTES`

This variable shows the number of buffer bytes fetched from disk for queries.

### `Tokudb_BUFFERS_FETCHED_TARGET_QUERY_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching buffers
from disk for queries.

### `Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE`

This variable shows the number of buffers fetched from disk aggressively.

### `Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE_BYTES`

This variable shows the number of buffer bytes fetched from disk aggressively.

### `Tokudb_BUFFERS_FETCHED_PRELOCKED_RANGE_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching buffers
from disk aggressively.

### `Tokudb_BUFFERS_FETCHED_PREFETCH`

This variable shows the number of buffers fetched from disk aggressively.

### `Tokudb_BUFFERS_FETCHED_PREFETCH_BYTES`

This variable shows the number of buffer bytes fetched from disk by a prefetch
thread.

### `Tokudb_BUFFERS_FETCHED_PREFETCH_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching buffers
from disk by a prefetch thread.

### `Tokudb_BUFFERS_FETCHED_FOR_WRITE`

This variable shows the number of buffers fetched from disk for writes.

### `Tokudb_BUFFERS_FETCHED_FOR_WRITE_BYTES`

This variable shows the number of buffer bytes fetched from disk for writes.

### `Tokudb_BUFFERS_FETCHED_FOR_WRITE_SECONDS`

This variable shows the number of seconds waiting for I/O when fetching buffers
from disk for writes.

### `Tokudb_LEAF_COMPRESSION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent compressing leaf nodes.

### `Tokudb_LEAF_SERIALIZATION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent serializing leaf nodes.

### `Tokudb_LEAF_DECOMPRESSION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent decompressing leaf nodes.

### `Tokudb_LEAF_DESERIALIZATION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent deserializing leaf nodes.

### `Tokudb_NONLEAF_COMPRESSION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent compressing non leaf
nodes.

### `Tokudb_NONLEAF_SERIALIZATION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent serializing non leaf
nodes.

### `Tokudb_NONLEAF_DECOMPRESSION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent decompressing non leaf
nodes.

### `Tokudb_NONLEAF_DESERIALIZATION_TO_MEMORY_SECONDS`

This variable shows the total time, in seconds, spent deserializing non leaf
nodes.

### `Tokudb_PROMOTION_ROOTS_SPLIT`

This variable shows the number of times the root split during promotion.

### `Tokudb_PROMOTION_LEAF_ROOTS_INJECTED_INTO`

This variable shows the number of times a message stopped at a root with
height `0`.

### `Tokudb_PROMOTION_H1_ROOTS_INJECTED_INTO`

This variable shows the number of times a message stopped at a root with
height `1`.

### `Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_0`

This variable shows the number of times a message stopped at depth `0`.

### `Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_1`

This variable shows the number of times a message stopped at depth `1`.

### `Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_2`

This variable shows the number of times a message stopped at depth `2`.

### `Tokudb_PROMOTION_INJECTIONS_AT_DEPTH_3`

This variable shows the number of times a message stopped at depth `3`.

### `Tokudb_PROMOTION_INJECTIONS_LOWER_THAN_DEPTH_3`

This variable shows the number of times a message was promoted past depth
`3`.

### `Tokudb_PROMOTION_STOPPED_NONEMPTY_BUFFER`

This variable shows the number of times a message stopped because it reached
a nonempty buffer.

### `Tokudb_PROMOTION_STOPPED_AT_HEIGHT_1`

This variable shows the number of times a message stopped because it had
reached height `1`.

### `Tokudb_PROMOTION_STOPPED_CHILD_LOCKED_OR_NOT_IN_MEMORY`

This variable shows the number of times a message stopped because it could not
cheaply get access to a child.

### `Tokudb_PROMOTION_STOPPED_CHILD_NOT_FULLY_IN_MEMORY`

This variable shows the number of times a message stopped because it could not
cheaply get access to a child.

### `Tokudb_PROMOTION_STOPPED_AFTER_LOCKING_CHILD`

This variable shows the number of times a message stopped before a child which
had been locked.

### `Tokudb_BASEMENT_DESERIALIZATION_FIXED_KEY`

This variable shows the number of basement nodes deserialized where all keys
had the same size, leaving the basement in a format that is optimal for
in-memory workloads.

### `Tokudb_BASEMENT_DESERIALIZATION_VARIABLE_KEY`

This variable shows the number of basement nodes deserialized where all keys
did not have the same size, and thus ineligible for an in-memory optimization.

### `Tokudb_PRO_RIGHTMOST_LEAF_SHORTCUT_SUCCESS`

This variable shows the number of times a message injection detected a series
of sequential inserts to the rightmost side of the tree and successfully
applied an insert message directly to the rightmost leaf node. This is a not a
useful value for a regular user to use for any purpose.

### `Tokudb_PRO_RIGHTMOST_LEAF_SHORTCUT_FAIL_POS`

This variable shows the number of times a message injection detected a series
of sequential inserts to the rightmost side of the tree and was unable to
follow the pattern of directly applying an insert message directly to the
rightmost leaf node because the key does not continue the sequence. This is a
not a useful value for a regular user to use for any purpose.

### `Tokudb_RIGHTMOST_LEAF_SHORTCUT_FAIL_REACTIVE`

This variable shows the number of times a message injection detected a series
of sequential inserts to the rightmost side of the tree and was unable to
follow the pattern of directly applying an insert message directly to the
rightmost leaf node because the leaf is full. This is a not a useful value for
a regular user to use for any purpose.

### `Tokudb_CURSOR_SKIP_DELETED_LEAF_ENTRY`

This variable shows the number of leaf entries skipped during search/scan
because the result of message application and reconciliation of the leaf entry
MVCC stack reveals that the leaf entry is `deleted` in the current
transactions view. It is a good indicator that there might be excessive garbage
in a tree if a range scan seems to take too long.

### `Tokudb_FLUSHER_CLEANER_TOTAL_NODES`

This variable shows the total number of nodes potentially flushed by flusher or
cleaner threads. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_FLUSHER_CLEANER_H1_NODES`

This variable shows the number of height `1` nodes that had messages flushed
by flusher or cleaner threads, i.e., internal nodes immediately above leaf
nodes. This is a not a useful value for a regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_HGT1_NODES`

This variable shows the number of nodes with height greater than `1` that had
messages flushed by flusher or cleaner threads. This is a not a useful value
for a regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_EMPTY_NODES`

This variable shows the number of nodes cleaned by flusher or cleaner threads
which had empty message buffers. This is a not a useful value for a regular
user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_NODES_DIRTIED`

This variable shows the number of nodes dirtied by flusher or cleaner threads
as a result of flushing messages downward. This is a not a useful value for a
regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_MAX_BUFFER_SIZE`

This variable shows the maximum bytes in a message buffer flushed by flusher or
cleaner threads. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_FLUSHER_CLEANER_MIN_BUFFER_SIZE`

This variable shows the minimum bytes in a message buffer flushed by flusher or
cleaner threads. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_FLUSHER_CLEANER_TOTAL_BUFFER_SIZE`

This variable shows the total bytes in buffers flushed by flusher and cleaner
threads. This is a not a useful value for a regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_MAX_BUFFER_WORKDONE`

This variable shows the maximum bytes worth of work done in a message buffer
flushed by flusher or cleaner threads. This is a not a useful value for a
regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_MIN_BUFFER_WORKDONE`

This variable shows the minimum bytes worth of work done in a message buffer
flushed by flusher or cleaner threads. This is a not a useful value for a
regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_TOTAL_BUFFER_WORKDONE`

This variable shows the total bytes worth of work done in buffers flushed by
flusher or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_STARTED`

This variable shows the number of times flusher and cleaner threads tried to
merge two leafs. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_RUNNING`

This variable shows the number of flusher and cleaner threads leaf merges in
progress. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_FLUSHER_CLEANER_NUM_LEAF_MERGES_COMPLETED`

This variable shows the number of successful flusher and cleaner threads leaf
merges. This is a not a useful value for a regular user to use for any purpose.

### `Tokudb_FLUSHER_CLEANER_NUM_DIRTIED_FOR_LEAF_MERGE`

This variable shows the number of nodes dirtied by flusher or cleaner threads
performing leaf node merges. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_FLUSH_TOTAL`

This variable shows the total number of flushes done by flusher threads or
cleaner threads. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_FLUSHER_FLUSH_IN_MEMORY`

This variable shows the number of in memory flushes (required no disk reads) by
flusher or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_FLUSH_NEEDED_IO`

This variable shows the number of flushes that read something off disk by
flusher or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES`

This variable shows the number of flushes that triggered a flush in child node
by flusher or cleaner threads. This is a not a useful value for a regular user
to use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES_1`

This variable shows the number of flushes that triggered one cascading flush by
flusher or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES_2`

This variable shows the number of flushes that triggered two cascading flushes
by flusher or cleaner threads. This is a not a useful value for a regular user
to use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES_3`

This variable shows the number of flushes that triggered three cascading
flushes by flusher or cleaner threads. This is a not a useful value for a
regular user to use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES_4`

This variable shows the number of flushes that triggered four cascading
flushes by flusher or cleaner threads. This is a not a useful value for a
regular user to use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES_5`

This variable shows the number of flushes that triggered five cascading
flushes by flusher or cleaner threads. This is a not a useful value for a
regular user to use for any purpose.

### `Tokudb_FLUSHER_FLUSH_CASCADES_GT_5`

This variable shows the number of flushes that triggered more than five
cascading flushes by flusher or cleaner threads. This is a not a useful value
for a regular user to use for any purpose.

### `Tokudb_FLUSHER_SPLIT_LEAF`

This variable shows the total number of leaf node splits done by flusher
threads or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_SPLIT_NONLEAF`

This variable shows the total number of non-leaf node splits done by flusher
threads or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_MERGE_LEAF`

This variable shows the total number of leaf node merges done by flusher
threads or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_MERGE_NONLEAF`

This variable shows the total number of non-leaf node merges done by flusher
threads or cleaner threads. This is a not a useful value for a regular user to
use for any purpose.

### `Tokudb_FLUSHER_BALANCE_LEAF`

This variable shows the number of times two adjacent leaf nodes were rebalanced
or had their content redistributed evenly by flusher or cleaner threads. This
is a not a useful value for a regular user to use for any purpose.

### `Tokudb_HOT_NUM_STARTED`

This variable shows the number of hot operations started (`OPTIMIZE TABLE`).
This is a not a useful value for a regular user to use for any purpose.

### `Tokudb_HOT_NUM_COMPLETED`

This variable shows the number of hot operations completed (`OPTIMIZE TABLE`).
This is a not a useful value for a regular user to use for any purpose.

### `Tokudb_HOT_NUM_ABORTED`

This variable shows the number of hot operations aborted (`OPTIMIZE TABLE`).
This is a not a useful value for a regular user to use for any purpose.

### `Tokudb_HOT_MAX_ROOT_FLUSH_COUNT`

This variable shows the maximum number of flushes from root ever required to
optimize trees. This is a not a useful value for a regular user to use for any
purpose.

### `Tokudb_TXN_BEGIN`

This variable shows the number of transactions that have been started.

### `Tokudb_TXN_BEGIN_READ_ONLY`

This variable shows the number of read-only transactions started.

### `Tokudb_TXN_COMMITS`

This variable shows the total number of transactions that have been committed.

### `Tokudb_TXN_ABORTS`

This variable shows the total number of transactions that have been aborted.

### `Tokudb_LOGGER_NEXT_LSN`

This variable shows the recovery logger next LSN. This is a not a useful value
for a regular user to use for any purpose.

### `Tokudb_LOGGER_WRITES`

This variable shows the number of times the logger has written to disk.

### `Tokudb_LOGGER_WRITES_BYTES`

This variable shows the number of bytes the logger has written to disk.

### `Tokudb_LOGGER_WRITES_UNCOMPRESSED_BYTES`

This variable shows the number of uncompressed bytes the logger has written to
disk.

### `Tokudb_LOGGER_WRITES_SECONDS`

This variable shows the number of seconds waiting for IO when writing logs to
disk.

### `Tokudb_LOGGER_WAIT_LONG`

This variable shows the number of times a logger write operation required 100ms
or more.

### `Tokudb_LOADER_NUM_CREATED`

This variable shows the number of times one of our internal objects, a loader,
has been created.

### `Tokudb_LOADER_NUM_CURRENT`

This variable shows the number of loaders that currently exist.

### `Tokudb_LOADER_NUM_MAX`

This variable shows the maximum number of loaders that ever existed
simultaneously.

### `Tokudb_MEMORY_MALLOC_COUNT`

This variable shows the number of `malloc` operations by PerconaFT.

### `Tokudb_MEMORY_FREE_COUNT`

This variable shows the number of `free` operations by PerconaFT.

### `Tokudb_MEMORY_REALLOC_COUNT`

This variable shows the number of `realloc` operations by PerconaFT.

### `Tokudb_MEMORY_MALLOC_FAIL`

This variable shows the number of `malloc` operations that failed by
PerconaFT.

### `Tokudb_MEMORY_REALLOC_FAIL`

This variable shows the number of `realloc` operations that failed by
PerconaFT.

### `Tokudb_MEMORY_REQUESTED`

This variable shows the number of bytes requested by PerconaFT.

### `Tokudb_MEMORY_USED`

This variable shows the number of bytes used (requested + overhead) by
PerconaFT.

### `Tokudb_MEMORY_FREED`

This variable shows the number of bytes freed by PerconaFT.

### `Tokudb_MEMORY_MAX_REQUESTED_SIZE`

This variable shows the largest attempted allocation size by PerconaFT.

### `Tokudb_MEMORY_LAST_FAILED_SIZE`

This variable shows the size of the last failed allocation attempt by
PerconaFT.

### `Tokudb_MEM_ESTIMATED_MAXIMUM_MEMORY_FOOTPRINT`

This variable shows the maximum memory footprint of the storage engine, the
max value of (used - freed).

### `Tokudb_MEMORY_MALLOCATOR_VERSION`

This variable shows the version of the memory allocator library detected by
PerconaFT.

### `Tokudb_MEMORY_MMAP_THRESHOLD`

This variable shows the `mmap` threshold in PerconaFT, anything larger than
this gets `mmap'ed`.

### `Tokudb_FILESYSTEM_THREADS_BLOCKED_BY_FULL_DISK`

This variable shows the number of threads that are currently blocked because
they are attempting to write to a full disk. This is normally zero. If this
value is non-zero, then a warning will appear in the `disk free space` field.

### `Tokudb_FILESYSTEM_FSYNC_TIME`

This variable shows the total time, in microseconds, used to `fsync` to disk.

### `Tokudb_FILESYSTEM_FSYNC_NUM`

This variable shows the total number of times the database has flushed the
operating system’s file buffers to disk.

### `Tokudb_FILESYSTEM_LONG_FSYNC_TIME`

This variable shows the total time, in microseconds, used to `fsync` to dis
k when the operation required more than one second.

### `Tokudb_FILESYSTEM_LONG_FSYNC_NUM`

This variable shows the total number of times the database has flushed the
operating system’s file buffers to disk and this operation required more than
one second.
