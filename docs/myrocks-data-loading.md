# MyRocks Data loading

Default MyRocks settings target short transactions. Use session variables to load large data sets.

For variable details, see [MyRocks server variables](myrocks-server-variables.md#rocksdb_bulk_load).

## Sorted bulk loading

Use this method when the input is in primary key order.

Drop secondary indexes first. Load the data. Then add the secondary indexes with Fast Secondary Index Creation.

### Creating secondary indexes

To load data into empty tables, drop all secondary indexes first. Load the data. Then add the secondary indexes.

MyRocks uses Fast Secondary Index Creation for `CREATE INDEX` and `ALTER TABLE ... ADD INDEX`. Fast Secondary Index Creation writes secondary index entries to the bottommost RocksDB levels. This path skips compaction. Total write volume and CPU time drop.

### Loading data

Load into tables that have a primary key only. Add secondary indexes after the load.

Set the following session variables:

```sql
SET SESSION sql_log_bin=0;
SET SESSION rocksdb_bulk_load_allow_sk=1;
SET SESSION rocksdb_bulk_load=1;
```

`sql_log_bin=0` skips binary log writes. `rocksdb_bulk_load*` session variables are not written to the binary log. Replicas then load without bulk load and can lag.

To convert large MyISAM or InnoDB tables with `ALTER` or `INSERT INTO SELECT`, use the following pattern. A large conversion without bulk load can exhaust memory and trigger the OOM killer:

```sql
SET SESSION sql_log_bin=0;
SET SESSION rocksdb_bulk_load_allow_sk=1;
SET SESSION rocksdb_bulk_load=1;
ALTER TABLE large_myisam_table ENGINE=RocksDB;
SET SESSION rocksdb_bulk_load=0;
SET SESSION rocksdb_bulk_load_allow_sk=0;
```

When [`rocksdb_bulk_load`](myrocks-server-variables.md#rocksdb_bulk_load) is `ON`, MyRocks writes inserts to Sorted String Table (SST) files and ingests those files into the bottommost RocksDB level. The SST ingest path skips the memtable and compaction.

Bulk-load mode also skips unique key checks and row locks. The mode uses the same implicit-commit behavior as [`rocksdb_commit_in_the_middle`](myrocks-server-variables.md#rocksdb_commit_in_the_middle).

Without [`rocksdb_bulk_load_allow_sk`](myrocks-server-variables.md#rocksdb_bulk_load_allow_sk), only the primary key uses SST ingest. Secondary keys use the memtable, write-ahead log (WAL), flush, and compaction path.

With `rocksdb_bulk_load_allow_sk=1`, MyRocks writes secondary keys to temporary files under `rocksdb_tmpdir`, sorts those keys, and ingests them when the bulk load ends.

[`rocksdb_bulk_load`](myrocks-server-variables.md#rocksdb_bulk_load) has the following conditions:

* Keys in the bulk load must not overlap existing keys in the table

* Load into an empty table to meet this rule

* You can load more data later if the new key range does not overlap existing data

* Keep the table empty when the table has secondary indexes

* Rows stay invisible until MyRocks ingests the SST file

* MyRocks ingests the current SST file when you set `rocksdb_bulk_load` to `OFF`

* MyRocks also ingests the current SST file when the session starts a bulk load on a different table

* A `SELECT` during bulk load can return only older rows

* Do not interleave `INSERT` statements across two or more tables in one bulk-load session

By default, bulk load expects inserts in primary key order or reverse order. Reverse-order rows are cached in chunks and rewritten in the expected order.

An out-of-order insert returns an error. Some rows can be ingested and some can be missing. Truncate the table, fix the key order, and load again.

## Unsorted bulk loading

Use this method when the input is not in primary key order. You can keep secondary keys in place.

Primary-key writes go to temporary files first. MyRocks sorts those files, then writes the final SST files. This extra sort step has a performance cost.

To allow unsorted data:

```sql
SET SESSION sql_log_bin=0;
SET SESSION rocksdb_bulk_load_allow_sk=1;
SET SESSION rocksdb_bulk_load_allow_unsorted=1;
SET SESSION rocksdb_bulk_load=1;
...
SET SESSION rocksdb_bulk_load=0;
SET SESSION rocksdb_bulk_load_allow_unsorted=0;
SET SESSION rocksdb_bulk_load_allow_sk=0;
```

Change [`rocksdb_bulk_load_allow_unsorted`](myrocks-server-variables.md#rocksdb_bulk_load_allow_unsorted) only when [`rocksdb_bulk_load`](myrocks-server-variables.md#rocksdb_bulk_load) is `OFF`.

## Other approaches

If [`rocksdb_commit_in_the_middle`](myrocks-server-variables.md#rocksdb_commit_in_the_middle) is `ON`, MyRocks commits every [`rocksdb_bulk_load_size`](myrocks-server-variables.md#rocksdb_bulk_load_size) records. The default is 1000. If `LOAD DATA` or a bulk `INSERT` fails, committed rows stay in the table. Truncate the table and load again.

When [`rocksdb_bulk_load`](myrocks-server-variables.md#rocksdb_bulk_load) is `ON`, MyRocks uses implicit commits.

!!! warning

    If you load large data without [`rocksdb_bulk_load`](myrocks-server-variables.md#rocksdb_bulk_load) or [`rocksdb_commit_in_the_middle`](myrocks-server-variables.md#rocksdb_commit_in_the_middle), keep the transaction small. All changes for an open transaction stay in memory.

## Related variables

* [`rocksdb_bulk_load`](myrocks-server-variables.md#rocksdb_bulk_load)

* [`rocksdb_enable_bulk_load_api`](myrocks-server-variables.md#rocksdb_enable_bulk_load_api)

* [`rocksdb_bulk_load_allow_sk`](myrocks-server-variables.md#rocksdb_bulk_load_allow_sk)

* [`rocksdb_bulk_load_allow_unsorted`](myrocks-server-variables.md#rocksdb_bulk_load_allow_unsorted)

* [`rocksdb_bulk_load_fail_if_not_bottommost_level`](myrocks-server-variables.md#rocksdb_bulk_load_fail_if_not_bottommost_level)

* [`rocksdb_bulk_load_use_sst_partitioner`](myrocks-server-variables.md#rocksdb_bulk_load_use_sst_partitioner)

* [`rocksdb_commit_in_the_middle`](myrocks-server-variables.md#rocksdb_commit_in_the_middle)

## Other reading

* [Data Loading :octicons-link-external-16:](https://github.com/facebook/mysql-5.6/wiki/Data-Loading)

* [ALTER TABLE … ENGINE=ROCKSDB uses too much memory :octicons-link-external-16:](https://github.com/facebook/mysql-5.6/issues/692)
