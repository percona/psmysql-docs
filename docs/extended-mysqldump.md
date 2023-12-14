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

## Taking backup by descending primary key order

–order-by-primary-desc tells `mysqldump` to take the backup by
descending primary key order (`PRIMARY KEY DESC`) which can be useful if
the storage engine is using the reverse order column for a primary key.

## RocksDB support

**mysqldump** detects when MyRocks is installed and available.
If there is a session variable named
`rocksdb_skip_fill_cache`, **mysqldump** sets the variable to **1**.

**mysqldump** automatically enables `rocksdb_bulk_load` if the the target server supports the variable.

