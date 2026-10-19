# SHOW ENGINE ROCKSDB TRANSACTION STATUS

Added in Percona Server for MySQL 8.4.12-13, the `SHOW ENGINE ROCKSDB TRANSACTION STATUS` statement was added.

The statement is ported from Facebook MySQL. Like the other `SHOW ENGINE` statements, it requires the [`PROCESS`](https://dev.mysql.com/doc/refman/{{vers}}/en/privileges-provided.html#priv_process) privilege.

It returns one row with the columns `Type`, `Name`, and `Status`. `Status` holds the `ROCKSDB TRANSACTION MONITOR OUTPUT` text.

```{.bash data-prompt="mysql>"}
SHOW ENGINE ROCKSDB TRANSACTION STATUS;
```

The output has two parts.

One entry for each connection that has a MyRocks transaction object. Each entry shows:

* whether the transaction has an active snapshot, and for how long

* the connection's security context: thread id, user, host, and current query

* when its earliest snapshot was created

* its lock count and write count

A `LATEST DETECTED DEADLOCKS` section that lists the most recent deadlock paths kept by RocksDB. The number of paths kept is [`rocksdb_max_latest_deadlocks`](myrocks-server-variables.md#rocksdb_max_latest_deadlocks). For each transaction the section shows the timestamp, transaction id, column family, waiting key, lock type, index and table name, and which transaction was chosen as the victim.

??? example "Per-session entry"

    ```{.text .no-copy}
    ---SNAPSHOT, ACTIVE 3 sec
    MySQL thread id 12, OS thread handle 140..., query id 71 localhost root
    earliest snapshot created 3 sec ago
    lock count 0, write count 0
    ```

`SHOW ENGINE INNODB TRANSACTION STATUS` returns an empty result.

`SHOW ENGINE ALL TRANSACTION STATUS` is also accepted.

## `Com_show_engine_trans`

Added in Percona Server for MySQL 8.4.12-13, the `Com_show_engine_trans` status counter was added.

| Option | Description |
| --- | --- |
| Scope | Global, Session |
| Data type | Numeric |

`Com_show_engine_trans` counts executions of `SHOW ENGINE ROCKSDB TRANSACTION STATUS`.
