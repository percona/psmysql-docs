# Updated supported features

The following is a list of the latest supported features:

* Percona Server for MySQLsupports `SELECT FOR UPDATE SKIP LOCKED/NOWAIT`. The transaction isolation level must be `READ COMMITTED`.

* Percona Server for MySQL adds the ability to cancel ongoing manual compactions. The cancel methods are the following:

    * Using either Control+C (from a session) or KILL (from another session) for client sessions running manual compactions by `SET GLOBAL rocksdb_compact_cf (variable)`.

    * Using a global variable `rocksdb_cancel_manual_compactions` to cancel all ongoing manual compactions.

* Percona Server for MySQL adds supported for [Generated Columns :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/create-table-generated-columns.html) and index are supported.

* Percona Server for MySQL adds support for [explicit DEFAULT value expressions :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/data-type-defaults.html).

## Behavior changes in 8.4.13-12

### Index statistics after crash recovery

As of Percona Server for MySQL 8.4.13-12, a compaction that runs before an index has been opened, for example during write-ahead log replay, leaves that index's persisted cardinality statistics in place. Those compactions used to overwrite the statistics with zeros, and query plans regressed until the statistics were recalculated.

### Missing unpack information

As of Percona Server for MySQL 8.4.13-12, missing unpack information in a secondary index record returns an error to the client instead of crashing the server.

### Prepared XA transactions

As of Percona Server for MySQL 8.4.13-12, a prepared XA transaction that modified MyRocks tables is kept.

The server keeps that transaction across a clean restart and across a crash.

`XA RECOVER` lists the transaction.

`XA COMMIT` or `XA ROLLBACK` completes the transaction.

The transaction keeps its row locks.

The locks include unique secondary key values and rows read by a locking read.

`TRUNCATE TABLE`, `ALTER TABLE`, and `DROP TABLE` on the tables of that transaction wait for the transaction.

MyRocks stores a marker for each prepared XA transaction in the `__system__` column family.

This rule applies with the binary log enabled and with the binary log disabled.

With the binary log off and [`rocksdb_flush_log_at_trx_commit=2`](myrocks-server-variables.md#rocksdb_flush_log_at_trx_commit), `XA PREPARE`, `XA COMMIT`, and `XA ROLLBACK` are written to the operating system.

Those writes survive a crash of the server process.

With the binary log enabled, an XA transaction prepared with `sql_log_bin=0` is rolled back at restart.

The session that prepares the XA transaction writes nothing to the binary log.

InnoDB rolls that transaction back at restart as well.

A prepared XA transaction survives disconnect of the preparing session when `xa_detach_on_prepare=OFF` (PS-11631).

`XA PREPARE` does not raise Warning 1031 (`Table storage engine for 'ROCKSDB' doesn't have this option`).

A prepared XA transaction that did not write to MyRocks tables is not kept across a restart, same as InnoDB.

As of Percona Server for MySQL 8.4.13-12, the following issue was fixed. Recovering a prepared XA transaction after a crash no longer logs a false failure to prepare it.

`XA PREPARE` of a transaction that wrote to MyRocks with write batches is described under [`rocksdb_master_skip_tx_api`](myrocks-server-variables.md#rocksdb_master_skip_tx_api) and [`rocksdb_rpl_skip_tx_api`](myrocks-server-variables.md#rocksdb_rpl_skip_tx_api).

## Percona fixes in 8.4.13-12

As of Percona Server for MySQL 8.4.13-12, the following issues were fixed.

* A read that fails inside RocksDB, for example with an I/O error during a scan, returns an error. The scan does not end early with partial results.

* If repairing a table left by an interrupted `ALTER TABLE` fails at startup, the original table definition is kept, so the repair can be retried after a restart.

* With `rocksdb_enable_tmp_table=ON`, committing an insert into a temporary table with an `AUTO_INCREMENT` column no longer aborts the server.

* MyRocks messages longer than 1 KiB are no longer truncated in the error log and the RocksDB `LOG` file.

## RocksDB 9.4.0 to 9.7.4 {#rocksdb-940-to-974}

Percona Server for MySQL 8.4.13-12 bundles RocksDB 9.7.4.

The previous bundle was RocksDB 9.3.1.

The intermediate bundles were RocksDB 9.3.2, fb.9.6, and 9.7.1.

A descending scan uses `SeekForPrev` and returns every matching row.

A reverse lookup returns every matching row.

The column family in that case uses a prefix Bloom filter, `whole_key_filtering=false`, and partitioned filters.

SST files written by an earlier RocksDB version keep a miss until compaction rewrites those files.

After the upgrade to RocksDB 9.7.4, compact each affected column family:

```sql
SET GLOBAL rocksdb_compact_cf='<cf>';
```

[`rocksdb_compact_cf`](myrocks-server-variables.md#rocksdb_compact_cf) names the column family.

After [`rocksdb_update_cf_options`](myrocks-server-variables.md#rocksdb_update_cf_options) changes `prefix_extractor`, reads find rows that remain in the memtable.

The column family has `memtable_prefix_bloom_size_ratio` above 0.

A checkpoint from [`rocksdb_create_checkpoint`](myrocks-server-variables.md#rocksdb_create_checkpoint), or a checkpoint for a clone, keeps the RocksDB database ID of its source.

The checkpoint does not sync the live WAL.

The checkpoint contains one extra empty WAL file.

With [`rocksdb_io_error_action=IGNORE_ERROR`](myrocks-server-variables.md#rocksdb_io_error_action), a WAL write error is fatal.

MyRocks refuses writes until the server restarts.

The refusal continues after the cause is corrected.

A commit that fails on a WAL error stays invisible to other sessions and after a restart.

The default `ABORT_SERVER` is unchanged.

## Downgrade to MyRocks 9.3.1 {#downgrade-to-myrocks-931}

A data directory written by MyRocks 9.7.4-1 opens on MyRocks 9.3.1.

That data directory opens after a crash.

RocksDB 9.3.1 replays the write-ahead log written by RocksDB 9.7.4.

Complete the following steps before a downgrade:

1. The `OPTIONS` file written by RocksDB 9.7.4 contains options that RocksDB 9.3.1 does not recognize.

    An earlier release loads that file only with [`rocksdb_ignore_unknown_options=ON`](myrocks-server-variables.md#rocksdb_ignore_unknown_options).

    `ON` is the default.

    With `OFF`, the `ROCKSDB` engine fails to load.

2. An earlier release rejects a table that has a partial index and TTL.

    Compaction in that release cannot decode the partial-index entries.

    The server aborts.

    Drop the partial index, or drop the table, before the downgrade.

3. An earlier release rolls back prepared MyRocks XA transactions at startup.

    That release ignores the markers that keep those transactions prepared.

    Commit each prepared transaction, or roll that transaction back, before the downgrade.

4. Remove each variable in the following list from the configuration file and the command line.

    Or prefix each name with `loose-`.

    Otherwise the earlier release fails to start.

    Values saved with `SET PERSIST` do not block the start.

    * `rocksdb_bulk_load_history_size`

    * `rocksdb_enable_autoinc_compat_mode`

    * `rocksdb_gap_lock_raise_error`

    * `rocksdb_max_trash_db_ratio_pct`

    * `rocksdb_records_in_range_dive_threshold`

    * `rocksdb_skip_bulk_load_notify_ddl`

    * `rocksdb_write_batch_mem_free_threshold` 
