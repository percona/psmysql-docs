# MyRocks supported features

MyRocks implements the following engine features.

## Locking reads with `SKIP LOCKED` and `NOWAIT`

MyRocks supports `SELECT ... FOR UPDATE SKIP LOCKED` and `SELECT ... FOR UPDATE NOWAIT`. Use the `READ COMMITTED` isolation level.

`SKIP LOCKED` skips rows that another transaction holds with a conflicting lock. MyRocks also skips rows that return lock wait timeout, deadlock, or a busy status.

`NOWAIT` does not wait for a conflicting lock.

## Generated columns

MyRocks supports [generated columns :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/create-table-generated-columns.html).

MyRocks can index virtual generated columns. The server evaluates virtual generated column values when MyRocks reads a row.

## Default value expressions

MyRocks supports [explicit default value expressions :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/data-type-defaults.html) when [`rocksdb_column_default_value_as_expression`](myrocks-server-variables.md#rocksdb_column_default_value_as_expression) is `ON`. The default for this variable is `ON`.

## Cancel manual compaction

MyRocks can compact a column family with [`rocksdb_compact_cf`](myrocks-server-variables.md#rocksdb_compact_cf). Set the variable to the column family name. Use an empty string or `default` to compact the default column family.

The session that runs `SET GLOBAL rocksdb_compact_cf` waits until the compaction ends.

Cancel that compaction in the following ways:

* Interrupt the session with Ctrl+C

* Run `KILL` on that session from another session

Those actions mark the session as killed. MyRocks then cancels the pending or running compaction. The cancel wait can last up to 60 seconds.

To cancel all pending and running manual compactions, set [`rocksdb_cancel_manual_compactions`](myrocks-server-variables.md#rocksdb_cancel_manual_compactions) to `ON`.

For column family layout, see [MyRocks column families](myrocks-column-families.md).
