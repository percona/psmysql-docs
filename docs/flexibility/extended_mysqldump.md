# Extended mysqldump

## Backup Locks support

When used together with the –single-transaction option, the
lock-for-backup option makes `mysqldump` issue `LOCK
TABLES FOR BACKUP` before starting the dump operation to prevent
unsafe statements that would normally result in an inconsistent
backup.

More information can be found on the Backup Locks feature documentation.

## Compressed Columns support

**mysqldump** supports the Compressed columns with dictionaries feature. More
information about the relevant options can be found on the
Compressed columns with dictionaries feature page.

## Taking backup by descending primary key order

–order-by-primary-desc tells `mysqldump` to take the backup by
descending primary key order (`PRIMARY KEY DESC`) which can be useful if
the storage engine is using the reverse order column for a primary key.

## RocksDB support

**mysqldump** detects when MyRocks is installed and available.
If there is a session variable named
rocksdb_skip_fill_cache **mysqldump** sets it to **1**.

**mysqldump** will now automatically enable session the variable
rocksdb_bulk_load if it is supported by the target server.

## Version Specific Information

    * 8.0.12-1: The feature was ported from *Percona Server for MySQL* 5.7
