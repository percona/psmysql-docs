# Extended mysqldump

## Backup Locks support

In *Percona Server for MySQL* Percona Server for MySQL 5.7.10-1 `mysqldump` has been extended with a
new option, `lock-for-backup` (disabled by default). When used together
with the `--single-transaction` option, the option makes `mysqldump`
issue `LOCK TABLES FOR BACKUP` before starting the dump operation to prevent
unsafe statements that would normally result in an inconsistent backup.

More information can be found on the Backup Locks feature documentation.

## Compressed Columns support

In *Percona Server for MySQL* Percona Server for MySQL 5.7.17-11 **mysqldump** has been extended to
support Compressed columns with dictionaries feature. More information about the new
options can be found on the Compressed columns with dictionaries feature page.

## Taking backup by descending primary key order

In Percona Server for MySQL 5.7.17-12 new `--order-by-primary-desc` has been
implemented. This feature tells `mysqldump` to take the backup by
descending primary key order (`PRIMARY KEY DESC`) which can be useful if
storage engine is using reverse order column for a primary key.

## RocksDB support

**mysqldump** will now detect when MyRocks is installed and available
by seeing if there is a session variable named
rocksdb_skip_fill_cache and setting it to `1` if it exists.

**mysqldump** will now automatically enable session variable
rocksdb_bulk_load if it is supported by target server.

## Version Specific Information

* Percona Server for MySQL 5.7.10-1: **mysqldump** has been extended with Backup Locks support options

* Percona Server for MySQL 5.7.17-11: **mysqldump** has been extended with Compressed columns with dictionaries support options


* Percona Server for MySQL 5.7.17-12: **mysqldump** option `--order-by-primary-desc` introduced
