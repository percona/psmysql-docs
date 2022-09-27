# Show Storage Engines

This feature changes the comment field displayed when the `SHOW STORAGE ENGINES` command is executed and XtraDB is the storage engine.

Before the change:

```sql
mysql> show storage engines;
```

The output could be similar to the following:

```text
+------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine     | Support | Comment                                                        | Transactions | XA   | Savepoints |
+------------+---------+----------------------------------------------------------------+--------------+------+------------+
| InnoDB     | YES     | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
...
+------------+---------+----------------------------------------------------------------+--------------+------+------------+
```

After the change:

```sql
mysql> show storage engines;
```

The output could be similar to the following:

```text
+------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
| Engine     | Support | Comment                                                                    | Transactions |   XA | Savepoints |
+------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
| InnoDB     | YES     | Percona-XtraDB, Supports transactions, row-level locking, and foreign keys |          YES | YES  | YES        |
...
+------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
```

## Version-Specific Information

* Percona Server for MySQL 5.7.10-1: Feature ported from *Percona Server for MySQL* 5.6
