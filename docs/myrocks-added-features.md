# Updated supported features

The following is a list of the latest supported features:

* Percona Server for MySQLsupports `SELECT FOR UPDATE SKIP LOCKED/NOWAIT`. The transaction isolation level must be `READ COMMITTED`.

* Percona Server for MySQL adds the ability to cancel ongoing manual compactions. The cancel methods are the following:

    * Using either Control+C (from a session) or KILL (from another session) for client sessions running manual compactions by `SET GLOBAL rocksdb_compact_cf (variable)`.

    * Using a global variable `rocksdb_cancel_manual_compactions` to cancel all ongoing manual compactions.

* Percona Server for MySQL adds supported for [Generated Columns :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/create-table-generated-columns.html) and index are supported.

* Percona Server for MySQL adds support for [explicit DEFAULT value expressions :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/data-type-defaults.html).

## Behavior changes in 8.4.12-13

### Index statistics after crash recovery

As of Percona Server for MySQL 8.4.12-13, a compaction that runs before an index has been opened, for example during write-ahead log replay, leaves that index's persisted cardinality statistics in place. Those compactions used to overwrite the statistics with zeros, and query plans regressed until the statistics were recalculated.

### Missing unpack information

As of Percona Server for MySQL 8.4.12-13, missing unpack information in a secondary index record returns an error to the client instead of crashing the server.

### Prepared XA transactions

As of Percona Server for MySQL 8.4.12-13, a prepared XA transaction that modified MyRocks tables is kept across a clean restart. `XA RECOVER` lists it, and `XA COMMIT` or `XA ROLLBACK` completes it. An XA transaction prepared while the session does not write to the binary log (`sql_log_bin=0`) is rolled back at restart. InnoDB rolls back that transaction at restart as well.

As of Percona Server for MySQL 8.4.12-13, the following issue was fixed. Recovering a prepared XA transaction after a crash no longer logs a false failure to prepare it.

`XA PREPARE` of a transaction that wrote to MyRocks with write batches is described under [`rocksdb_master_skip_tx_api`](myrocks-server-variables.md#rocksdb_master_skip_tx_api) and [`rocksdb_rpl_skip_tx_api`](myrocks-server-variables.md#rocksdb_rpl_skip_tx_api).

## Percona fixes in 8.4.12-13

As of Percona Server for MySQL 8.4.12-13, the following issues were fixed.

* A read that fails inside RocksDB, for example with an I/O error during a scan, returns an error. The scan does not end early with partial results.

* If repairing a table left by an interrupted `ALTER TABLE` fails at startup, the original table definition is kept, so the repair can be retried after a restart.

* With `rocksdb_enable_tmp_table=ON`, committing an insert into a temporary table with an `AUTO_INCREMENT` column no longer aborts the server.

* MyRocks messages longer than 1 KiB are no longer truncated in the error log and the RocksDB `LOG` file. 
