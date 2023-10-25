# Extended show engine InnoDB status

This feature reorganizes the output of `SHOW ENGINE INNODB STATUS`
to improve readability and to provide additional information. The
variable innodb_show_locks_held controls the umber of
locks held to print for each *InnoDB* transaction.

This feature modified the `SHOW ENGINE INNODB STATUS` command as follows:

* Added extended information about *InnoDB* internal hash table sizes (in bytes) in the `BUFFER POOL AND MEMORY` section; also added buffer pool size in bytes.

* Added additional LOG section information.

## Other information

* Author / Origin: Baron Schwartz, [https://lists.mysql.com/internals/35174](https://lists.mysql.com/internals/35174)

## System variables

### `innodb_show_locks_held`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | Yes         |
| Data type    | ULONG       |
| Default      | 10          |
| Range        | 0 - 1000    |

Specifies the number of locks held to print for each *InnoDB* transaction in
`SHOW ENGINE INNODB STATUS`.

### `innodb_print_lock_wait_timeout_info`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | Yes         |
| Data type    | Boolean     |
| Default      | OFF         |

Makes *InnoDB* to write information about all lock wait timeout errors
into the log file.

This allows to find out details about the failed transaction, and, most
importantly, the blocking transaction. Query string can be obtained from EVENTS_STATEMENTS_CURRENT table, based on the
`PROCESSLIST_ID` field, which corresponds to `thread_id` from the log
output.

Taking into account that blocking transaction is often a multiple statement
one, following query can be used to obtain blocking thread statements history:

```sql
SELECT s.SQL_TEXT FROM performance_schema.events_statements_history s
INNER JOIN performance_schema.threads t ON t.THREAD_ID = s.THREAD_ID
WHERE t.PROCESSLIST_ID = %d
UNION
SELECT s.SQL_TEXT FROM performance_schema.events_statements_current s
INNER JOIN performance_schema.threads t ON t.THREAD_ID = s.THREAD_ID
WHERE t.PROCESSLIST_ID = %d;
```

The `PROCESSLIST_ID` in this example is exactly the thread id from error log output.

## Status variables

The status variables here contain information available in the output of `SHOW
ENGINE INNODB STATUS`, organized by the sections `SHOW ENGINE INNODB STATUS`
displays. If you are familiar with the output of `SHOW ENGINE INNODB STATUS`,
you will probably already recognize the information these variables contain.

### BACKGROUND THREAD

The following variables contain information in the `BACKGROUND THREAD`
section of the output from `SHOW ENGINE INNODB STATUS`. 

??? example "Expected output"

    ```{.text .no-copy}

    -----------------
    BACKGROUND THREAD
    -----------------
    srv_master_thread loops: 1 srv_active, 0 srv_shutdown, 11844 srv_idle
    srv_master_thread log flush and writes: 11844
    ```

*InnoDB* has a source thread which performs background tasks depending on the
server state, once per second. If the server is under workload, the source
thread runs the following: performs background table drops; performs change
buffer merge, adaptively; flushes the redo log to disk; evicts tables from the
dictionary cache if needed to satisfy its size limit; makes a checkpoint. If
the server is idle: performs background table drops, flushes and/or checkpoints
the redo log if needed due to the checkpoint age; performs change buffer merge
at full I/O capacity; evicts tables from the dictionary cache if
needed; and makes a checkpoint.

### `Innodb_master_thread_active_loops`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the number of times the above one-second loop was executed
for active server states.

### `Innodb_master_thread_idle_loops`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the number of times the above one-second loop was executed
for idle server states.

### `Innodb_background_log_sync`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the number of times the *InnoDB* source thread has written
and flushed the redo log.

### SEMAPHORES

The following variables contain information in the `SEMAPHORES` section of
the output from `SHOW ENGINE INNODB STATUS`. An example of that output is:

??? example "Expected output"

    ```{.text .no-copy}
    ----------
    SEMAPHORES
    ----------
    OS WAIT ARRAY INFO: reservation count 9664, signal count 11182
    Mutex spin waits 20599, rounds 223821, OS waits 4479
    RW-shared spins 5155, OS waits 1678; RW-excl spins 5632, OS waits 2592
    Spin rounds per wait: 10.87 mutex, 15.01 RW-shared, 27.19 RW-excl
    ```

### INSERT BUFFER AND ADAPTIVE HASH INDEX

The following variables contain information in the `INSERT BUFFER AND ADAPTIVE
HASH INDEX` section of the output from `SHOW ENGINE INNODB STATUS`. An
example of that output is:

??? example "Expected output"

    ```{.text .no-copy}
    -------------------------------------
    INSERT BUFFER AND ADAPTIVE HASH INDEX
    -------------------------------------
    Ibuf: size 1, free list len 6089, seg size 6091,
    44497 inserts, 44497 merged recs, 8734 merges
    0.00 hash searches/s, 0.00 non-hash searches/s
    ```

### `Innodb_ibuf_free_list`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

### `Innodb_ibuf_segment_size`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

### LOG

The following variables contain information in the `LOG` section of the
output from `SHOW ENGINE INNODB STATUS`. An example of that output is:

??? example "Expected output"

    ```{.text .no-copy}
    LOG
    ---
    Log sequence number 10145937666
    Log flushed up to   10145937666
    Pages flushed up to 10145937666
    Last checkpoint at  10145937666
    Max checkpoint age    80826164
    Checkpoint age target 78300347
    Modified age          0
    Checkpoint age        0
    0 pending log writes, 0 pending chkp writes
    9 log i/o's done, 0.00 log i/o's/second
    Log tracking enabled
    Log tracked up to   10145937666
    Max tracked LSN age 80826164
    ```

### `Innodb_lsn_current`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the current log sequence number.

### `Innodb_lsn_flushed`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the current maximum LSN that has been written and flushed
to disk.

### `Innodb_lsn_last_checkpoint`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the LSN of the latest completed checkpoint.

### `Innodb_checkpoint_age`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the current *InnoDB* checkpoint age, i.e., the difference
between the current LSN and the LSN of the last completed checkpoint.

### BUFFER POOL AND MEMORY

The following variables contain information in the `BUFFER POOL AND MEMORY`
section of the output from `SHOW ENGINE INNODB STATUS`. An example of that
output is:

??? example "Expected output"

    ```{.text .no-copy}
    ----------------------
    BUFFER POOL AND MEMORY
    ----------------------
    Total memory allocated 137363456; in additional pool allocated 0
    Total memory allocated by read views 88
    Internal hash tables (constant factor + variable factor)
        Adaptive hash index 2266736         (2213368 + 53368)
        Page hash           139112 (buffer pool 0 only)
        Dictionary cache    729463  (554768 + 174695)
        File system         824800  (812272 + 12528)
        Lock system         333248  (332872 + 376)
        Recovery system     0       (0 + 0)
    Dictionary memory allocated 174695
    Buffer pool size        8191
    Buffer pool size, bytes 134201344
    Free buffers            7481
    Database pages          707
    Old database pages      280
    Modified db pages       0
    Pending reads 0
    Pending writes: LRU 0, flush list 0 single page 0
    Pages made young 0, not young 0
    0.00 youngs/s, 0.00 non-youngs/s
    Pages read 707, created 0, written 1
    0.00 reads/s, 0.00 creates/s, 0.00 writes/s
    No buffer pool page gets since the last printout
    Pages read ahead 0.00/s, evicted without access 0.00/s, Random read ahead 0.00/s
    LRU len: 707, unzip_LRU len: 0
    ```

### `Innodb_mem_adaptive_hash`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the current size, in bytes, of the adaptive hash index.

### `Innodb_mem_dictionary`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the current size, in bytes, of the *InnoDB* in-memory data
dictionary info.

### `Innodb_mem_total`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the total amount of memory, in bytes, *InnoDB* has
allocated in the process heap memory.

### `Innodb_buffer_pool_pages_LRU_flushed`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the total number of buffer pool pages which have been
flushed from the LRU list, i.e., too old pages which had to be flushed in
order to make buffer pool room to read in new data pages.

### `Innodb_buffer_pool_pages_made_not_young`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the number of times a buffer pool page was not marked as
accessed recently in the LRU list because of innodb_old_blocks_time
variable setting.

### `Innodb_buffer_pool_pages_made_young`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the number of times a buffer pool page was moved to the
young end of the LRU list due to its access, to prevent its eviction from the
buffer pool.

### `Innodb_buffer_pool_pages_old`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the total number of buffer pool pages which are considered
to be old according to the [Making the Buffer Pool Scan Resistant manual page].

### TRANSACTIONS

The following variables contain information in the `TRANSACTIONS` section of
the output from `SHOW INNODB STATUS`. An example of that output is:

??? example "Expected output"

    ```{.text .no-copy}
    ------------
    TRANSACTIONS
    ------------
    Trx id counter F561FD
    Purge done for trx's n:o < F561EB undo n:o < 0
    History list length 19
    LIST OF TRANSACTIONS FOR EACH SESSION:
    ---TRANSACTION 0, not started, process no 993, OS thread id 140213152634640
    mysql thread id 15933, query id 32109 localhost root
    show innodb status
    ---TRANSACTION F561FC, ACTIVE 29 sec, process no 993, OS thread id 140213152769808 updating or deleting
    mysql tables in use 1, locked 1
    ```

### `Innodb_max_trx_id`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the next free transaction id number.

### `Innodb_oldest_view_low_limit_trx_id`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the highest transaction id, above which the current oldest
open read view does not see any transaction changes. Zero if there is no open
view.

### `Innodb_purge_trx_id`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable shows the oldest transaction id whose records have not been
purged yet.

### `Innodb_purge_undo_no`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

## INFORMATION_SCHEMA Tables

The following table contains information about the oldest active transaction in
the system.

### `INFORMATION_SCHEMA.XTRADB_READ_VIEW`

The data type for the following columns is `BIGINT UNSIGNED`. The columns contain 64-bit integers.

| Column Name                      | Description                                                    |
|----------------------------------|----------------------------------------------------------------|
| ‘READ_VIEW_LOW_LIMIT_TRX_NUMBER’ | This is the highest transactions number at the time the view was created.  |
| ‘READ_VIEW_UPPER_LIMIT_TRX_ID’   | This is the highest transactions ID at the time the view was created. This means that it should not see newer transactions with IDs bigger than or equal to that value.          |
| ‘READ_VIEW_LOW_LIMIT_TRX_ID’     | This is the latest committed transaction ID at the time the oldest view was created. This means that it should see all transactions with IDs smaller than or equal to that value. |

The following table contains information about the memory usage for
InnoDB/XtraDB hash tables.

### `INFORMATION_SCHEMA.XTRADB_INTERNAL_HASH_TABLES`

| Column Name                | Description            |
|----------------------------|------------------------|
| ‘INTERNAL_HASH_TABLE_NAME’ | Hash table name        |
| ‘TOTAL_MEMORY’             | Total amount of memory |
| ‘CONSTANT_MEMORY’          | Constant memory        |
| ‘VARIABLE_MEMORY’          | Variable memory        |

## Other reading

* [SHOW INNODB STATUS walk through](https://www.mysqlperformanceblog.com/2006/07/17/show-innodb-status-walk-through/)

* [Table locks in SHOW INNODB STATUS](https://www.mysqlperformanceblog.com/2010/06/08/table-locks-in-show-innodb-status/)


[Making the Buffer Pool Scan Resistant manual page]: https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-performance-midpoint_insertion.html