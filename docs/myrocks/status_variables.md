# MyRocks status variables

MyRocks status variables provide details
about the inner workings of the storage engine
and they can be useful in tuning the storage engine
to a particular environment.

You can view these variables and their values by running:

```sql
mysql> SHOW STATUS LIKE 'rocksdb%';
```
## List of status variables

The following global status variables are available:

| Name                                                                                                        | Var Type |
|------------------------------------------------------------------------------------------------------------ |----------|
| [`rocksdb_rows_deleted`](#rocksdbrowsdeleted)                                                               | Numeric  |
| [`rocksdb_rows_inserted`](#rocksdbrowsinserted)                                                             | Numeric  |
| [`rocksdb_rows_read`](#rocksdb_rows_read)                                                                   | Numeric  |
| [`rocksdb_rows_updated`](#rocksdb_rows_updated)                                                             | Numeric  |
| [`rocksdb_rows_expired`](#rocksdb_rows_expired)                                                             | Numeric  |
| [`rocksdb_system_rows_deleted`](#rocksdb_system_rows_deleted)                                               | Numeric  |
| [`rocksdb_system_rows_inserted`](#rocksdb_system_rows_inserted)                                             | Numeric  |
| [`rocksdb_system_rows_read`](#rocksdb_system_rows_read)                                                     | Numeric  |
| [`rocksdb_system_rows_updated`](#rocksdb_system_rows_updated)                                               | Numeric  |
| [`rocksdb_memtable_total`](#rocksdb_memtable_total)                                                         | Numeric  |
| [`rocksdb_memtable_unflushed`](#rocksdb_memtable_unflushed)                                                 | Numeric  |
| [`rocksdb_queries_point`](#rocksdb_queries_point)                                                           | Numeric  |
| [`rocksdb_queries_range`](#rocksdb_queries_range)                                                           | Numeric  |
| [`rocksdb_covered_secondary_key_lookups`](#rocksdb_covered_secondary_key_lookups)                           | Numeric  |
| [`rocksdb_additional_compactions_trigger`](#rocksdb_additional_compactions_trigger)                         | Numeric  |
| [`rocksdb_block_cache_add`](#rocksdb_block_cache_add)                                                       | Numeric  |
| [`rocksdb_block_cache_add_failures`](#rocksdb_block_cache_add_failures)                                     | Numeric  |
| [`rocksdb_block_cache_bytes_read`](#rocksdb_block_cache_bytes_read)                                         | Numeric  |
| [`rocksdb_block_cache_bytes_write`](#rocksdb_block_cache_bytes_write)                                       | Numeric  |
| [`rocksdb_block_cache_data_add`](#rocksdb_block_cache_data_add)                                             | Numeric  |
| [`rocksdb_block_cache_data_bytes_insert`](#rocksdb_block_cache_data_bytes_insert)                           | Numeric  |
| [`rocksdb_block_cache_data_hit`](#rocksdb_block_cache_data_hit)                                             | Numeric  |
| [`rocksdb_block_cache_data_miss`](#rocksdb_block_cache_data_miss)                                           | Numeric  |
| [`rocksdb_block_cache_filter_add`](#rocksdb_block_cache_filter_add)                                         | Numeric  |
| [`rocksdb_block_cache_filter_bytes_evict`](#rocksdb_block_cache_filter_bytes_evict)                         | Numeric  |
| [`rocksdb_block_cache_filter_bytes_insert`](#rocksdb_block_cache_filter_bytes_insert)                       | Numeric  |
| [`rocksdb_block_cache_filter_hit`](#rocksdb_block_cache_filter_hit)                                         | Numeric  |
| [`rocksdb_block_cache_filter_miss`](#rocksdb_block_cache_filter_miss)                                       | Numeric  |
| [`rocksdb_block_cache_hit`](#rocksdb_block_cache_hit)                                                       | Numeric  |
| [`rocksdb_block_cache_index_add`](#rocksdb_block_cache_index_add)                                           | Numeric  |
| [`rocksdb_block_cache_index_bytes_evict`](#rocksdb_block_cache_index_bytes_evict)                           | Numeric  |
| [`rocksdb_block_cache_index_bytes_insert`](#rocksdb_block_cache_index_bytes_insert)                         | Numeric  |
| [`rocksdb_block_cache_index_hit`](#rocksdb_block_cache_index_hit)                                           | Numeric  |
| [`rocksdb_block_cache_index_miss`](#rocksdb_block_cache_index_miss)                                         | Numeric  |
| [`rocksdb_block_cache_miss`](#rocksdb_block_cache_miss)                                                     | Numeric  |
| [`rocksdb_block_cache_compressed_hit`](#rocksdb_block_cache_compressed_hit)                                 | Numeric  |
| [`rocksdb_block_cache_compressed_miss`](#rocksdb_block_cache_compressed_miss)                               | Numeric  |
| [`rocksdb_bloom_filter_prefix_checked`](#rocksdb_bloom_filter_prefix_checked)                               | Numeric  |
| [`rocksdb_bloom_filter_prefix_useful`](#rocksdb_bloom_filter_prefix_useful)                                 | Numeric  |
| [`rocksdb_bloom_filter_useful`](#rocksdb_bloom_filter_useful)                                               | Numeric  |
| [`rocksdb_bytes_read`](#rocksdb_bytes_read)                                                                 | Numeric  |
| [`rocksdb_bytes_written`](#rocksdb_bytes_written)                                                           | Numeric  |
| [`rocksdb_compact_read_bytes`](#rocksdb_compact_read_bytes)                                                 | Numeric  |
| [`rocksdb_compact_write_bytes`](#rocksdb_compact_write_bytes)                                               | Numeric  |
| [`rocksdb_compaction_key_drop_new`](#rocksdb_compaction_key_drop_new)                                       | Numeric  |
| [`rocksdb_compaction_key_drop_obsolete`](#rocksdb_compaction_key_drop_obsolete)                             | Numeric  |
| [`rocksdb_compaction_key_drop_user`](#rocksdb_compaction_key_drop_user)                                     | Numeric  |
| [`rocksdb_flush_write_bytes`](#rocksdb_flush_write_bytes)                                                   | Numeric  |
| [`rocksdb_get_hit_l0`](#rocksdb_get_hit_l0)                                                                 | Numeric  |
| [`rocksdb_get_hit_l1`](#rocksdb_get_hit_l1)                                                                 | Numeric  |
| [`rocksdb_get_hit_l2_and_up`](#rocksdb_get_hit_l2_and_up)                                                   | Numeric  |
| [`rocksdb_get_updates_since_calls`](#rocksdb_get_updates_since_calls)                                       | Numeric  |
| [`rocksdb_iter_bytes_read`](#rocksdb_iter_bytes_read)                                                       | Numeric  |
| [`rocksdb_memtable_hit`](#rocksdb_memtable_hit)                                                             | Numeric  |
| [`rocksdb_memtable_miss`](#rocksdb_memtable_miss)                                                           | Numeric  |
| [`rocksdb_no_file_closes`](#rocksdb_no_file_closes)                                                         | Numeric  |
| [`rocksdb_no_file_errors`](#rocksdb_no_file_errors)                                                         | Numeric  |
| [`rocksdb_no_file_opens`](#rocksdb_no_file_opens)                                                           | Numeric  |
| [`rocksdb_num_iterators`](#rocksdb_num_iterators)                                                           | Numeric  |
| [`rocksdb_number_block_not_compressed`](#rocksdb_number_block_not_compressed)                               | Numeric  |
| [`rocksdb_number_db_next`](#rocksdb_number_db_next)                                                         | Numeric  |
| [`rocksdb_number_db_next_found`](#rocksdb_number_db_next_found)                                             | Numeric  |
| [`rocksdb_number_db_prev`](#rocksdb_number_db_prev)                                                         | Numeric  |
| [`rocksdb_number_db_prev_found`](#rocksdb_number_db_prev_found)                                             | Numeric  |
| [`rocksdb_number_db_seek`](#rocksdb_number_db_seek)                                                         | Numeric  |
| [`rocksdb_number_db_seek_found`](#rocksdb_number_db_seek_found)                                             | Numeric  |
| [`rocksdb_number_deletes_filtered`](#rocksdb_number_deletes_filtered)                                       | Numeric  |
| [`rocksdb_number_keys_read`](#rocksdb_number_keys_read)                                                     | Numeric  |
| [`rocksdb_number_keys_updated`](#rocksdb_number_keys_updated)                                               | Numeric  |
| [`rocksdb_number_keys_written`](#rocksdb_number_keys_written)                                               | Numeric  |
| [`rocksdb_number_merge_failures`](#rocksdb_number_merge_failures)                                           | Numeric  |
| [`rocksdb_number_multiget_bytes_read`](#rocksdb_number_multiget_bytes_read)                                 | Numeric  |
| [`rocksdb_number_multiget_get`](#rocksdb_number_multiget_get)                                               | Numeric  |
| [`rocksdb_number_multiget_keys_read`](#rocksdb_number_multiget_keys_read)                                   | Numeric  |
| [`rocksdb_number_reseeks_iteration`](#rocksdb_number_reseeks_iteration)                                     | Numeric  |
| [`rocksdb_number_sst_entry_delete`](#rocksdb_number_sst_entry_delete)                                       | Numeric  |
| [`rocksdb_number_sst_entry_merge`](#rocksdb_number_sst_entry_merge)                                         | Numeric  |
| [`rocksdb_number_sst_entry_other`](#rocksdb_number_sst_entry_other)                                         | Numeric  |
| [`rocksdb_number_sst_entry_put`](#rocksdb_number_sst_entry_put)                                             | Numeric  |
| [`rocksdb_number_sst_entry_singledelete`](#rocksdb_number_sst_entry_singledelete)                           | Numeric  |
| [`rocksdb_number_stat_computes`](#rocksdb_number_stat_computes)                                             | Numeric  |
| [`rocksdb_number_superversion_acquires`](#rocksdb_number_superversion_acquires)                             | Numeric  |
| [`rocksdb_number_superversion_cleanups`](#rocksdb_number_superversion_cleanups)                             | Numeric  |
| [`rocksdb_number_superversion_releases`](#rocksdb_number_superversion_releases)                             | Numeric  |
| [`rocksdb_rate_limit_delay_millis`](#rocksdb_rate_limit_delay_millis)                                       | Numeric  |
| [`rocksdb_row_lock_deadlocks`](#rocksdb_row_lock_deadlocks)                                                 | Numeric  |
| [`rocksdb_row_lock_wait_timeouts`](#rocksdb_row_lock_wait_timeouts)                                         | Numeric  |
| [`rocksdb_snapshot_conflict_errors`](#rocksdb_snapshot_conflict_errors)                                     | Numeric  |
| [`rocksdb_stall_l0_file_count_limit_slowdowns`](#rocksdb_stall_l0_file_count_limit_slowdowns)               | Numeric  |
| [`rocksdb_stall_locked_l0_file_count_limit_slowdowns`](#rocksdb_stall_locked_l0_file_count_limit_slowdowns) | Numeric  |
| [`rocksdb_stall_l0_file_count_limit_stops`](#rocksdb_stall_l0_file_count_limit_stops)                       | Numeric  |
| [`rocksdb_stall_locked_l0_file_count_limit_stops`](#rocksdb_stall_locked_l0_file_count_limit_stops)         | Numeric  |
| [`rocksdb_stall_pending_compaction_limit_stops`](#rocksdb_stall_pending_compaction_limit_stops)             | Numeric  |
| [`rocksdb_stall_pending_compaction_limit_slowdowns`](#)                                                     | Numeric  |
| [`rocksdb_stall_memtable_limit_stops`](#rocksdb_stall_memtable_limit_stops)                                 | Numeric  |
| [`rocksdb_stall_memtable_limit_slowdowns`](#rocksdb_stall_memtable_limit_slowdowns)                         | Numeric  |
| [`rocksdb_stall_total_stops`](#rocksdb_stall_total_stops)                                                   | Numeric  |
| [`rocksdb_stall_total_slowdowns`](#rocksdb_stall_total_slowdowns)                                           | Numeric  |
| [`rocksdb_stall_micros`](#rocksdb_stall_micros)                                                             | Numeric  |
| [`rocksdb_wal_bytes`](#rocksdb_wal_bytes)                                                                   | Numeric  |
| [`rocksdb_wal_group_syncs`](#rocksdb_wal_group_syncs)                                                       | Numeric  |
| [`rocksdb_wal_synced`](#rocksdb_wal_synced)                                                                 | Numeric  |
| [`rocksdb_write_other`](#rocksdb_write_other)                                                               | Numeric  |
| [`rocksdb_write_self`](#rocksdb_write_self)                                                                 | Numeric  |
| [`rocksdb_write_timedout`](#rocksdb_write_timedout)                                                         | Numeric  |
| [`rocksdb_write_wal`](#rocksdb_write_wal)                                                                   | Numeric  |

### `rocksdb_rows_deleted`

This variable shows the number of rows that were deleted from MyRocks tables.

### `rocksdb_rows_inserted`

This variable shows the number of rows that were inserted into MyRocks tables.

### `rocksdb_rows_read`

This variable shows the number of rows that were read from MyRocks tables.

### `rocksdb_rows_updated`

This variable shows the number of rows that were updated in MyRocks tables.

### `rocksdb_rows_expired`

This variable shows the number of expired rows in MyRocks tables.

### `rocksdb_rows_filtered`

This variable shows the number of rows that were filtered out for TTL in
MyRocks tables.

### `rocksdb_system_rows_deleted`

This variable shows the number of rows that were deleted
from MyRocks system tables.

### `rocksdb_system_rows_inserted`

This variable shows the number of rows that were inserted
into MyRocks system tables.

### `ocksdb_system_rows_read`

This variable shows the number of rows that were read
from MyRocks system tables.

### `rocksdb_system_rows_updated`

This variable shows the number of rows that were updated
in MyRocks system tables.

### `rocksdb_memtable_total`

This variable shows the memory usage, in bytes, of all memtables.

### `rocksdb_memtable_unflushed`

This variable shows the memory usage, in bytes, of all unflushed memtables.

### `rocksdb_queries_point`

This variable shows the number of single row queries.

### `rocksdb_queries_range`

This variable shows the number of multi/range row queries.

### `rocksdb_covered_secondary_key_lookups`

This variable shows the number of lookups via secondary index that were able to
return all fields requested directly from the secondary index when the
secondary index contained a field that is only a prefix of the
`varchar` column.

### `rocksdb_additional_compactions_trigger`

This variable shows the number of triggered additional compactions.
MyRocks triggers an additional compaction if (number of deletions / number of entries) > (rocksdb_compaction_sequential_deletes / rocksdb_compaction_sequential_deletes_window)
in the SST file.

### `rocksdb_block_cache_add`

This variable shows the number of blocks added to block cache.

### `rocksdb_block_cache_add_failures`

This variable shows the number of failures when adding blocks to block cache.

### `rocksdb_block_cache_bytes_read`

This variable shows the number of bytes read from cache.

### `rocksdb_block_cache_bytes_write`

This variable shows the number of bytes written into cache.

### `rocksdb_block_cache_data_add`

This variable shows the number of data blocks added to block cache.

### `rocksdb_block_cache_data_bytes_insert`

This variable shows the number of bytes of data blocks inserted into cache.

### `rocksdb_block_cache_data_hit`

This variable shows the number of cache hits when accessing the
data block from the block cache.

### `rocksdb_block_cache_data_miss`

This variable shows the number of cache misses when accessing the
data block from the block cache.

### `rocksdb_block_cache_filter_add`

This variable shows the number of filter blocks added to block cache.

### `rocksdb_block_cache_filter_bytes_evict`

This variable shows the number of bytes of bloom filter blocks
removed from cache.

### `rocksdb_block_cache_filter_bytes_insert`

This variable shows the number of bytes of bloom filter blocks
inserted into cache.

### `rocksdb_block_cache_filter_hit`

This variable shows the number of times cache hit when accessing filter block
from block cache.

### `rocksdb_block_cache_filter_miss`

This variable shows the number of times cache miss when accessing filter
block from block cache.

### `rocksdb_block_cache_hit`

This variable shows the total number of block cache hits.

### `rocksdb_block_cache_index_add`

This variable shows the number of index blocks added to block cache.

### `rocksdb_block_cache_index_bytes_evict`

This variable shows the number of bytes of index block erased from cache.

### `rocksdb_block_cache_index_bytes_insert`

This variable shows the number of bytes of index blocks inserted into cache.

### `rocksdb_block_cache_index_hit`

This variable shows the total number of block cache index hits.

### `rocksdb_block_cache_index_miss`

This variable shows the number of times cache hit when accessing index
block from block cache.

### `rocksdb_block_cache_miss`

This variable shows the total number of block cache misses.

### `rocksdb_block_cache_compressed_hit`

This variable shows the number of hits in the compressed block cache.

### `rocksdb_block_cache_compressed_miss`

This variable shows the number of misses in the compressed block cache.

### `rocksdb_bloom_filter_prefix_checked`

This variable shows the number of times bloom was checked before
creating iterator on a file.

### `rocksdb_bloom_filter_prefix_useful`

This variable shows the number of times the check was useful in avoiding
iterator creation (and thus likely IOPs).

### `rocksdb_bloom_filter_useful`

This variable shows the number of times bloom filter has avoided file reads.

### `rocksdb_bytes_read`

This variable shows the total number of uncompressed bytes read. It could be
either from memtables, cache, or table files.

### `rocksdb_bytes_written`

This variable shows the total number of uncompressed bytes written.

### `rocksdb_compact_read_bytes`

This variable shows the number of bytes read during compaction

### `rocksdb_compact_write_bytes`

This variable shows the number of bytes written during compaction.

### `rocksdb_compaction_key_drop_new`

This variable shows the number of key drops during compaction because
it was overwritten with a newer value.

### `rocksdb_compaction_key_drop_obsolete`

This variable shows the number of key drops during compaction because
it was obsolete.

### `rocksdb_compaction_key_drop_user`

This variable shows the number of key drops during compaction because
user compaction function has dropped the key.

### `rocksdb_flush_write_bytes`

This variable shows the number of bytes written during flush.

### `rocksdb_get_hit_l0`

This variable shows the number of `Get()` queries served by L0.

### `rocksdb_get_hit_l1`

This variable shows the number of `Get()` queries served by L1.

### `rocksdb_get_hit_l2_and_up`

This variable shows the number of `Get()` queries served by L2 and up.

### `rocksdb_get_updates_since_calls`

This variable shows the number of calls to `GetUpdatesSince` function.
Useful to keep track of transaction log iterator refreshes

### `rocksdb_iter_bytes_read`

This variable shows the number of uncompressed bytes read from an iterator.
It includes size of key and value.

### `rocksdb_memtable_hit`

This variable shows the number of memtable hits.

### `rocksdb_memtable_miss`

This variable shows the number of memtable misses.

### `rocksdb_no_file_closes`

This variable shows the number of time file were closed.

### `rocksdb_no_file_errors`

This variable shows number of errors trying to read in data from an sst file.

### `rocksdb_no_file_opens`

This variable shows the number of time file were opened.

### `rocksdb_num_iterators`

This variable shows the number of currently open iterators.

### `rocksdb_number_block_not_compressed`

This variable shows the number of uncompressed blocks.

### `rocksdb_number_db_next`

This variable shows the number of calls to `next`.

### `rocksdb_number_db_next_found`

This variable shows the number of calls to `next` that returned data.

### `rocksdb_number_db_prev`

This variable shows the number of calls to `prev`.

### `rocksdb_number_db_prev_found`

This variable shows the number of calls to `prev` that returned data.

### `rocksdb_number_db_seek`

This variable shows the number of calls to `seek`.

### `rocksdb_number_db_seek_found`

This variable shows the number of calls to `seek` that returned data.

### `rocksdb_number_deletes_filtered`

This variable shows the number of deleted records that were not required to be
written to storage because key did not exist.

### `rocksdb_number_keys_read`

This variable shows the number of keys read.

### `rocksdb_number_keys_updated`

This variable shows the number of keys updated, if inplace update is enabled.

### `rocksdb_number_keys_written`

This variable shows the number of keys written to the database.

### `rocksdb_number_merge_failures`

This variable shows the number of failures performing merge operator actions
in RocksDB.

### `rocksdb_number_multiget_bytes_read`

This variable shows the number of bytes read during RocksDB
`MultiGet()` calls.

### `rocksdb_number_multiget_get`

This variable shows the number `MultiGet()` requests to RocksDB.

### `rocksdb_number_multiget_keys_read`

This variable shows the keys read via `MultiGet()`.

### `rocksdb_number_reseeks_iteration`

This variable shows the number of times reseek happened inside an iteration to
skip over large number of keys with same userkey.

### `rocksdb_number_sst_entry_delete`

This variable shows the total number of delete markers written by MyRocks.

### `rocksdb_number_sst_entry_merge`

This variable shows the total number of merge keys written by MyRocks.

### `rocksdb_number_sst_entry_other`

This variable shows the total number of non-delete, non-merge, non-put keys
written by MyRocks.

### `rocksdb_number_sst_entry_put`

This variable shows the total number of put keys written by MyRocks.

### `rocksdb_number_sst_entry_singledelete`

This variable shows the total number of single delete keys written by MyRocks.

### `rocksdb_number_stat_computes`

This variable was removed in *Percona Server for MySQL* Percona Server 5.7.23-23.

### `rocksdb_number_superversion_acquires`

This variable shows the number of times the superversion structure has been
acquired in RocksDB, this is used for tracking all of the files for the
database.

### `rocksdb_number_superversion_cleanups`

### `rocksdb_number_superversion_releases`

### `rocksdb_rate_limit_delay_millis`

This variable was removed in *Percona Server for MySQL* Percona Server 5.7.23-23.

### `rocksdb_row_lock_deadlocks`

This variable shows the total number of deadlocks that have been detected since the instance was started.

### `rocksdb_row_lock_wait_timeouts`

This variable shows the total number of row lock wait timeouts that have been detected since the instance was started.

### `rocksdb_snapshot_conflict_errors`

This variable shows the number of snapshot conflict errors occurring during
write transactions that forces the transaction to rollback.

### `rocksdb_stall_l0_file_count_limit_slowdowns`

This variable shows the slowdowns in write due to L0 being close to full.

### `rocksdb_stall_locked_l0_file_count_limit_slowdowns`

This variable shows the slowdowns in write due to L0 being close to full and
compaction for L0 is already in progress.

### `rocksdb_stall_l0_file_count_limit_stops`

This variable shows the stalls in write due to L0 being full.

### `rocksdb_stall_locked_l0_file_count_limit_stops`

This variable shows the stalls in write due to L0 being full and compaction
for L0 is already in progress.

### `rocksdb_stall_pending_compaction_limit_stops`

This variable shows the stalls in write due to hitting limits set for max
number of pending compaction bytes.

### `rocksdb_stall_pending_compaction_limit_slowdowns`

This variable shows the slowdowns in write due to getting close to limits set
for max number of pending compaction bytes.

### `rocksdb_stall_memtable_limit_stops`

This variable shows the stalls in write due to hitting max number of
`memTables` allowed.

### `rocksdb_stall_memtable_limit_slowdowns`

This variable shows the slowdowns in writes due to getting close to
max number of memtables allowed.

### `rocksdb_stall_total_stops`

This variable shows the total number of write stalls.

### `rocksdb_stall_total_slowdowns`

This variable shows the total number of write slowdowns.

### `rocksdb_stall_micros`

This variable shows how long (in microseconds) the writer had to wait for
compaction or flush to finish.

### `rocksdb_wal_bytes`

This variables shows the number of bytes written to WAL.

### `rocksdb_wal_group_syncs`

This variable shows the number of group commit WAL file syncs
that have occurred.

### `rocksdb_wal_synced`

This variable shows the number of times WAL sync was done.

### `rocksdb_write_other`

This variable shows the number of writes processed by another thread.

### `rocksdb_write_self`

This variable shows the number of writes that were processed
by a requesting thread.

### `rocksdb_write_timedout`

This variable shows the number of writes ending up with timed-out.

### `rocksdb_write_wal`

This variable shows the number of Write calls that request WAL.
