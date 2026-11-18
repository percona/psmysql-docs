# Extended mysqldump

## Backup locks support

When used together with the `–single-transaction` option, the
lock-for-backup option makes `mysqldump` issue `LOCK
TABLES FOR BACKUP` before starting the dump operation to prevent
unsafe statements that would normally result in an inconsistent
backup.

More information can be found in [Backup Locks](backup-locks.md).

## Compressed columns support

**mysqldump** supports the Compressed columns with dictionaries feature. 

More information can be found in
[Compressed columns with dictionaries](compressed-columns.md).

## `InnoDB` secondary keys and `--innodb-optimize-keys`

For *InnoDB* tables, `--innodb-optimize-keys` omits secondary keys (and related
constraints) from the initial `CREATE TABLE` in the dump and adds them in a
follow-up `ALTER TABLE` after the data is loaded. That pattern lets the server
build the indexes with [InnoDB fast index creation](innodb-expanded-fast-index-creation.md)
after the data is loaded. See that page for limitations (foreign keys,
partitioned tables, `AUTO_INCREMENT`, implicit primary keys, and others).

## Taking backup by descending primary key order

–order-by-primary-desc tells `mysqldump` to take the backup by
descending primary key order (`PRIMARY KEY DESC`) which can be useful if
the storage engine is using the reverse order column for a primary key.

## RocksDB support

**mysqldump** detects when MyRocks is installed and available.
If there is a session variable named
`rocksdb_skip_fill_cache`, **mysqldump** sets the variable to **1**.

**mysqldump** automatically enables `rocksdb_bulk_load` if the the target server supports the variable.

