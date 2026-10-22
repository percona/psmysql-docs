# Gap locks detection

MyRocks does not support [gap locks :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-locking.html#innodb-gap-locks). [`rocksdb_gap_lock_raise_error`](myrocks-server-variables.md#rocksdb_gap_lock_raise_error) controls a query that would need one, for example a locking read with a range condition under `REPEATABLE READ` or `SERIALIZABLE`. The setting also applies to partitioned tables. InnoDB is not affected.

Added in Percona Server for MySQL 8.4.12-13, the `rocksdb_gap_lock_raise_error` variable was added. The default is `ERROR`, which keeps the previous behavior: the query is rejected and no gap lock is taken.

| Value | Behavior |
|-------|----------|
| `OFF` | The query runs without gap locks. |
| `WARNING` | The query runs, and the server returns one warning per statement. |
| `ERROR` | The query is rejected. |

With `ERROR`, the client receives the following error. The detection is based on a Facebook MySQL patch.

??? example "Error message"

    ```{.text .no-copy}
    ERROR HY000: Using Gap Lock without full unique key in multi-table or multi-statement transactions is not allowed. You need to either rewrite queries to use all unique key columns in WHERE equal conditions, or rewrite to single-table, single-statement transaction.
    ```
