# Start transaction with consistent snapshot

Percona Server for MySQL has ported *MariaDB* [enhancement](https://mariadb.com/kb/en/enhancements-for-start-transaction-with-consistent/) for `START TRANSACTION WITH CONSISTENT SNAPSHOTS` feature to *MySQL* 5.6 group commit implementation. This enhancement makes binary log positions consistent with *InnoDB* transaction snapshots.

This feature is quite useful to obtain logical backups with correct positions without running a `FLUSH TABLES WITH READ LOCK`. Binary log position can be obtained by two newly implemented status variables: [Binlog_snapshot_file](#binlog_snapshot_file) and [Binlog_snapshot_position](#binlog_snapshot_position). After starting a transaction using the `START TRANSACTION WITH CONSISTENT SNAPSHOT`, these two variables will provide you with the binlog position corresponding to the state of the database of the consistent snapshot so taken, irrespectively of which other transactions have been committed since the snapshot was taken.

## Snapshot cloning

The *Percona Server for MySQL* implementation extends the `START TRANSACTION WITH CONSISTENT SNAPSHOT` syntax with the optional `FROM SESSION` clause:

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT FROM SESSION <session_id>;
```

When specified, all participating storage engines and binary log instead of creating a new snapshot of data (or binary log coordinates), create a copy of the snapshot which has been created by an active transaction in the specified session. `session_id` is the session identifier reported in the `Id` column of `SHOW PROCESSLIST`.

Currently snapshot cloning is only supported by *XtraDB* and the binary log. As with the regular `START TRANSACTION WITH CONSISTENT SNAPSHOT`, snapshot clones can only be created with the `REPEATABLE READ` isolation level.

For *XtraDB*, a transaction with a cloned snapshot will only see data visible or changed by the donor transaction. That is, the cloned transaction will see no changes committed by transactions that started after the donor transaction, not even changes made by itself. Note that in case of chained cloning the donor transaction is the first one in the chain. For example, if transaction A is cloned into transaction B, which is in turn cloned into transaction C, the latter will have read view from transaction A (i.e., the donor transaction). Therefore, it will see changes made by transaction A, but not by transaction B.

## mysqldump

`mysqldump` has been updated to use new status variables automatically when they are supported by the server and both –single-transaction and –master-data are specified on the command line. Along with the `mysqldump` improvements introduced in [Backup Locks](./backup-locks.md#backup-locks) there is now a way to generate `mysqldump` backups that are guaranteed to be consistent without using `FLUSH TABLES WITH READ LOCK` even if `--master-data` is requested.

## System variables

### `have_snapshot_cloning`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Config file    | No                 |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | Boolean            |

This server variable is implemented to help other utilities detect if the server supports the `FROM SESSION` extension. When available, the snapshot cloning feature and the syntax extension to `START TRANSACTION WITH CONSISTENT SNAPSHOT` are supported by the server, and the variable value is always `YES`.

## Status variables

### `Binlog_snapshot_file`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type      | String             |

### `Binlog_snapshot_position`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type      | Numeric            |

These status variables are only available when the binary log is enabled globally.

## Other reading

* [MariaDB Enhancements for START TRANSACTION WITH CONSISTENT SNAPSHOT](https://mariadb.com/kb/en/enhancements-for-start-transaction-with-consistent/)
