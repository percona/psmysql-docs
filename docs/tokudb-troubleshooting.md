# TokuDB troubleshooting

!!! important

    Starting with [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds.

    Starting with [Percona Server for MySQL 8.0.26-16](release-notes/Percona-Server-8.0.26-16.md), the binary builds and packages include but disable the TokuDB storage engine plugins. The tokudb_enabled option and the tokudb_backup_enabled option control the state of the plugins and have a default setting of FALSE. The result of attempting to load the plugins are the plugins fail to initialize and print a deprecation message.

    We recommend [Migrating the data to the MyRocks storage engine](https://docs.percona.com/percona-server/latest/tokudb/removing_tokudb.html#migrate-myrocks). To enable the plugins to migrate to another storage engine, set the tokudb_enabled and tokudb_backup_enabled options to TRUE in your my.cnf file and restart your server instance. Then, you can load the plugins.

    The TokuDB storage engine was declared as deprecated in [Percona Server for MySQL 8.0](release-notes/Percona-Server-8.0.13-3.md). For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).

## Known Issues

**Replication and binary logging**: *TokuDB* supports binary logging and replication, with one restriction. *TokuDB* does not implement a lock on the auto-increment function, so concurrent insert statements with one or more of the statements inserting multiple rows may result in a non-deterministic interleaving of the auto-increment values. When running replication with these concurrent inserts, the auto-increment values on the replica table may not match the auto-increment values on the source table. Note that this is only an issue with Statement Based Replication (SBR), and not Row Based Replication (RBR).

For more information about auto-increment and replication, see the *MySQL*
Reference Manual: [AUTO_INCREMENT handling in InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-auto-increment-handling.html).

In addition, when using the `REPLACE INTO` or `INSERT IGNORE` on tables with no secondary indexes or tables where secondary indexes are subsets of the primary, the session variable tokudb_pk_insert_mode controls whether row based replication will work.

**Uninformative error message**: The `LOAD DATA INFILE` command can sometimes

    produce `ERROR 1030 (HY000): Got error 1 from storage engine`. The message
    should say that the error is caused by insufficient disk space for the
    temporary files created by the loader.

**Transparent Huge Pages**: *TokuDB* will refuse to start if transparent huge

    pages are enabled. Transparent huge page support can be disabled by issuing the
    following as root:

```shell
# echo never > /sys/kernel/mm/redhat_transparent_hugepage/enabled
```

[Lock](#lock-visualization-in-tokudb)
!!! note

    The previous command needs to be executed after every reboot, because it defaults to `always`.

**XA behavior vs. InnoDB**: *InnoDB* forces a deadlocked XA transaction to

    abort, *TokuDB* does not.

**Disabling the unique checks**: For tables with unique keys, every insertion
into the table causes a lookup by key followed by an insertion, if the key is
not in the table. This greatly limits insertion performance. If one knows by
design that the rows being inserted into the table have unique keys, then one
can disable the key lookup prior to insertion.

If your primary key is an auto-increment key, and none of your secondary keys
are declared to be unique, then setting `unique_checks=OFF` will provide
limited performance gains. On the other hand, if your primary key has a lot of
entropy (it looks random), or your secondary keys are declared unique and have
a lot of entropy, then disabling unique checks can provide a significant
performance boost.

If unique_checks is disabled when the primary key is not unique,
secondary indexes may become corrupted. In this case, the indexes should be
dropped and rebuilt. This behavior differs from that of *InnoDB*, in which
uniqueness is always checked on the primary key, and setting
unique_checks to off turns off uniqueness checking on secondary
indexes only. Turning off uniqueness checking on the primary key can provide
large performance boosts, but it should only be done when the primary key is
known to be unique.

**Group Replication**: *TokuDB* storage engine doesn’t support [Group Replication](https://dev.mysql.com/doc/refman/8.0/en/group-replication.html).

As of 8.0.17, InnoDB supports [multi-valued indexes](https://dev.mysql.com/doc/refman/8.0/en/create-index.html#create-index-multi-valued). TokuDB does not support this feature.

As of 8.0.17, InnoDB supports the [Clone Plugin](https://dev.mysql.com/doc/refman/8.0/en/clone-plugin.html) and the Clone Plugin API. TokuDB tables do not support either of these features.

## Lock Visualization in TokuDB

*TokuDB* uses key range locks to implement serializable transactions, which are
acquired as the transaction progresses. The locks are released when the
transaction commits or aborts (this implements two phase locking).

*TokuDB* stores these locks in a data structure called the lock tree. The lock
tree stores the set of range locks granted to each transaction. In addition, the
lock tree stores the set of locks that are not granted due to a conflict with
locks granted to some other transaction. When these other transactions are
retired, these pending lock requests are retried. If a pending lock request is
not granted before the lock timer expires, then the lock request is aborted.

Lock visualization in *TokuDB* exposes the state of the lock tree with tables in
the information schema. We also provide a mechanism that may be used by a
database client to retrieve details about lock conflicts that it encountered
while executing a transaction.

### The `TOKUDB_TRX` table

The TOKUDB_TRX table in the `INFORMATION_SCHEMA` maps *TokuDB*
transaction identifiers to *MySQL* client identifiers. This mapping allows one
to associate a *TokuDB* transaction with a *MySQL* client operation.

The following query returns the *MySQL* clients that have a live *TokuDB*
transaction:

```sql
SELECT * FROM INFORMATION_SCHEMA.TOKUDB_TRX,
INFORMATION_SCHEMA.PROCESSLIST
WHERE trx_mysql_thread_id = id;
```

### The `TOKUDB_LOCKS` table

The tokudb_locks table in the information schema contains the set of
locks granted to *TokuDB* transactions.

The following query returns all of the locks granted to some *TokuDB*
transaction:

```sql
SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCKS;
```

The following query returns the locks granted to some *MySQL* client:

```sql
SELECT id FROM INFORMATION_SCHEMA.TOKUDB_LOCKS,
INFORMATION_SCHEMA.PROCESSLIST
WHERE locks_mysql_thread_id = id;
```

### The `TOKUDB_LOCK_WAITS` table

The tokudb_lock_waits table in the information schema contains the set
of lock requests that are not granted due to a lock conflict with some other
transaction.

The following query returns the locks that are waiting to be granted due to a
lock conflict with some other transaction:

```sql
SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCK_WAITS;
```

### Supporting explicit DEFAULT value expressions as of 8.0.13-3

TokuDB does not support [explicit DEFAULT value expressions](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html) as of verion 8.0.13-3.

### The tokudb_lock_timeout_debug session variable

The tokudb_lock_timeout_debug session variable controls how lock
timeouts and lock deadlocks seen by the database client are reported.

The following values are available:

* **0**

    No lock timeouts or lock deadlocks are reported.

* **1**

    A JSON document that describes the lock conflict is stored in the
    tokudb_last_lock_timeout session variable

* **2**

    A JSON document that describes the lock conflict is printed to the *MySQL*
    error log.

    *Supported since 7.5.5*: In addition to the JSON document describing the lock conflict, the following lines are printed to the MySQL error log:

    * A line containing the blocked thread id and blocked SQL

    * A line containing the blocking thread id and the blocking SQL.

* **3**

    A JSON document that describes the lock conflict is stored in the tokudb_last_lock_timeout session variable and is printed to the *MySQL* error log.

    *Supported since 7.5.5*: In addition to the JSON document describing the lock conflict, the following lines are printed to the *MySQL* error log:

    * A line containing the blocked thread id and blocked SQL

    * A line containing the blocking thread id and the blocking SQL.


### The tokudb_last_lock_timeout session variable

The tokudb_last_lock_timeout session variable contains a JSON
document that describes the last lock conflict seen by the current *MySQL*
client. It gets set when a blocked lock request times out or a lock deadlock is
detected. The tokudb_lock_timeout_debug session variable should have
bit `0` set (decimal `1`).

### Example

Suppose that we create a table with a single column that is the primary key.

```sql
mysql> SHOW CREATE TABLE table;

Create Table: CREATE TABLE ‘table‘ (
‘id‘ int(11) NOT NULL,
PRIMARY KEY (‘id‘)) ENGINE=TokuDB DEFAULT CHARSET=latin1
```

Suppose that we have 2 *MySQL* clients with ID’s 1 and 2 respectively. Suppose
that *MySQL* client 1 inserts some values into `table`. *TokuDB* transaction
51 is created for the insert statement. Since autocommit is disabled,
transaction 51 is still live after the insert statement completes, and we can
query the tokudb_locks table in information schema to see the locks
that are held by the transaction.

```sql
mysql> SET AUTOCOMMIT=OFF;
mysql> INSERT INTO table VALUES (1),(10),(100);
```

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCKS;
```

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCK_WAITS;
```

The keys are currently hex dumped.

Now we switch to the other *MySQL* client with ID 2.

```sql
mysql> INSERT INTO table VALUES (2),(20),(100);
```

The insert gets blocked since there is a conflict on the primary key with value 100.

The granted *TokuDB* locks are:

```sql
SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCKS;
```

The locks that are pending due to a conflict are:

```sql
SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCK_WAITS;
```

THe output could be:

```text
+-------------------+-----------------+------------------+---------------------+----------------------+-----------------------+--------------------+------------------+-----------------------------+
| requesting_trx_id | blocking_trx_id | lock_waits_dname | lock_waits_key_left | lock_waits_key_right | lock_waits_start_time | locks_table_schema | locks_table_name | locks_table_dictionary_name |
+-------------------+-----------------+------------------+---------------------+----------------------+-----------------------+--------------------+------------------+-----------------------------+
|                62 |              51 | ./test/t-main    | 0064000000          | 0064000000           |         1380656990910 | test               | t                | main                        |
+-------------------+-----------------+------------------+---------------------+----------------------+-----------------------+--------------------+------------------+-----------------------------+
```

Eventually, the lock for client 2 times out, and we can retrieve a JSON document that describes the conflict.

```sql
SELECT @@TOKUDB_LAST_LOCK_TIMEOUT;
```

```sql
ROLLBACK;
```

Since transaction 62 was rolled back, all of the locks taken by it are released.

```sql
SELECT * FROM INFORMATION_SCHEMA.TOKUDB_LOCKS;
```

### Engine Status

Engine status provides details about the inner workings of *TokuDB* and can be
useful in tuning your particular environment. The engine status can be
determined by running the following command:  `SHOW ENGINE tokudb STATUS;`

The following is a reference of the table status statements:

<table class="colwidths-given docutils align-default">
<colgroup>
<col style="width: 15%" />
<col style="width: 85%" />
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Table Status</p></th>
<th class="head"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p>disk free space</p></td>
<td><p>This is a gross estimate of how much of your file system is available.
Possible displays in this field are:</p>
<ul class="simple">
<li><p>More than twice the reserve (“more than 10 percent of total file system
space”)</p></li>
<li><p>Less than twice the reserve</p></li>
<li><p>Less than the reserve</p></li>
<li><p>File system is completely full</p></li>
</ul>
</td>
</tr>
<tr class="row-odd"><td><p>time of environment creation</p></td>
<td><p>This is the time when the <em>TokuDB</em> storage engine was first started up.
Normally, this is when <code class="docutils literal notranslate"><span class="pre">mysqld</span></code> was initially installed with <em>TokuDB</em>. If
the environment was upgraded from <em>TokuDB</em> 4.x (4.2.0 or later), then this
will be displayed as “Dec 31, 1969” on Linux hosts.</p></td>
</tr>
<tr class="row-even"><td><p>time of engine startup</p></td>
<td><p>This is the time when the <em>TokuDB</em> storage engine started up. Normally, this
is when <code class="docutils literal notranslate"><span class="pre">mysqld</span></code> started.</p></td>
</tr>
<tr class="row-odd"><td><p>time now</p></td>
<td><p>Current date/time on server.</p></td>
</tr>
<tr class="row-even"><td><p>db opens</p></td>
<td><p>This is the number of times an individual PerconaFT dictionary file was
opened. This is a not a useful value for a regular user to use for any purpose
due to layers of open/close caching on top.</p></td>
</tr>
<tr class="row-odd"><td><p>db closes</p></td>
<td><p>This is the number of times an individual PerconaFT dictionary file was
closed. This is a not a useful value for a regular user to use for any purpose
due to layers of open/close caching on top.</p></td>
</tr>
<tr class="row-even"><td><p>num open dbs now</p></td>
<td><p>This is the number of currently open databases.</p></td>
</tr>
<tr class="row-odd"><td><p>max open dbs</p></td>
<td><p>This is the maximum number of concurrently opened databases.</p></td>
</tr>
<tr class="row-even"><td><p>period, in ms, that recovery log is automatically fsynced</p></td>
<td><p><code class="docutils literal notranslate"><span class="pre">fsync()</span></code> frequency in milliseconds.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary inserts</p></td>
<td><p>This is the total number of rows that have been inserted into all primary and
secondary indexes combined, when those inserts have been done with a separate
recovery log entry per index. For example, inserting a row into a table with
one primary and two secondary indexes will increase this count by three, if
the inserts were done with separate recovery log entries.</p></td>
</tr>
<tr class="row-even"><td><p>dictionary inserts fail</p></td>
<td><p>This is the number of single-index insert operations that failed.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary deletes</p></td>
<td><p>This is the total number of rows that have been deleted from all primary and
secondary indexes combined, if those deletes have been done with a separate
recovery log entry per index.</p></td>
</tr>
<tr class="row-even"><td><p>dictionary deletes fail</p></td>
<td><p>This is the number of single-index delete operations that failed.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary updates</p></td>
<td><p>This is the total number of rows that have been updated in all primary and
secondary indexes combined, if those updates have been done with a separate
recovery log entry per index.</p></td>
</tr>
<tr class="row-even"><td><p>dictionary updates fail</p></td>
<td><p>This is the number of single-index update operations that failed.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary broadcast updates</p></td>
<td><p>This is the number of broadcast updates that have been successfully performed.
A broadcast update is an update that affects all rows in a dictionary.</p></td>
</tr>
<tr class="row-even"><td><p>dictionary broadcast updates fail</p></td>
<td><p>This is the number of broadcast updates that have failed.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary multi inserts</p></td>
<td><p>This is the total number of rows that have been inserted into all primary and
secondary indexes combined, when those inserts have been done with a single
recovery log entry for the entire row. (For example, inserting a row into a
table with one primary and two secondary indexes will normally increase this
count by three).</p></td>
</tr>
<tr class="row-even"><td><p>dictionary multi inserts fail</p></td>
<td><p>This is the number of multi-index insert operations that failed.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary multi deletes</p></td>
<td><p>This is the total number of rows that have been deleted from all primary and
secondary indexes combined, when those deletes have been done with a single
recovery log entry for the entire row.</p></td>
</tr>
<tr class="row-even"><td><p>dictionary multi deletes fail</p></td>
<td><p>This is the number of multi-index delete operations that failed.</p></td>
</tr>
<tr class="row-odd"><td><p>dictionary updates multi</p></td>
<td><p>This is the total number of rows that have been updated in all primary and
secondary indexes combined, if those updates have been done with a single
recovery log entry for the entire row.</p></td>
</tr>
<tr class="row-even"><td><p>dictionary updates fail multi</p></td>
<td><p>This is the number of multi-index update operations that failed.</p></td>
</tr>
<tr class="row-odd"><td><p>le: max committed xr</p></td>
<td><p>This is the maximum number of committed transaction records that were stored
on disk in a new or modified row.</p></td>
</tr>
<tr class="row-even"><td><p>le: max provisional xr</p></td>
<td><p>This is the maximum number of provisional transaction records that were stored
on disk in a new or modified row.</p></td>
</tr>
<tr class="row-odd"><td><p>le: expanded</p></td>
<td><p>This is the number of times that an expanded memory mechanism was used to
store a new or modified row on disk.</p></td>
</tr>
<tr class="row-even"><td><p>le: max memsize</p></td>
<td><p>This is the maximum number of bytes that were stored on disk as a new or
modified row. This is the maximum uncompressed size of any row stored in
<em>TokuDB</em> that was created or modified since the server started.</p></td>
</tr>
<tr class="row-odd"><td><p>le: size of leafentries before garbage collection (during message application)</p></td>
<td><p>Total number of bytes of leaf nodes data before performing garbage collection
for non-flush events.</p></td>
</tr>
<tr class="row-even"><td><p>le: size of leafentries after garbage collection (during message application)</p></td>
<td><p>Total number of bytes of leaf nodes data after performing garbage collection
for non-flush events.</p></td>
</tr>
<tr class="row-odd"><td><p>le: size of leafentries before garbage collection (outside message application)</p></td>
<td><p>Total number of bytes of leaf nodes data before performing garbage collection
for flush events.</p></td>
</tr>
<tr class="row-even"><td><p>le: size of leafentries after garbage collection (outside message application)</p></td>
<td><p>Total number of bytes of leaf nodes data after performing garbage collection
for flush events.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: period</p></td>
<td><p>This is the interval in seconds between the end of an automatic checkpoint and
the beginning of the next automatic checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: footprint</p></td>
<td><p>Where the database is in the checkpoint process.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: last checkpoint began</p></td>
<td><p>This is the time the last checkpoint began. If a checkpoint is currently in
progress, then this time may be later than the time the last checkpoint
completed.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>If no checkpoint has ever taken place, then this value will be <code class="docutils literal notranslate"><span class="pre">Dec</span> <span class="pre">31,</span>
<span class="pre">1969</span></code> on Linux hosts.</p>
</div>
</td>
</tr>
<tr class="row-even"><td><p>checkpoint: last complete checkpoint began</p></td>
<td><p>This is the time the last complete checkpoint started. Any data that changed
after this time will not be captured in the checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: last complete checkpoint ended</p></td>
<td><p>This is the time the last complete checkpoint ended.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: time spent during checkpoint (begin and end phases)</p></td>
<td><p>Time (in seconds) required to complete all checkpoints.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: time spent during last checkpoint (begin and end phases)</p></td>
<td><p>Time (in seconds) required to complete the last checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: last complete checkpoint LSN</p></td>
<td><p>This is the Log Sequence Number of the last complete checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: checkpoints taken</p></td>
<td><p>This is the number of complete checkpoints that have been taken.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: checkpoints failed</p></td>
<td><p>This is the number of checkpoints that have failed for any reason.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: waiters now</p></td>
<td><p>This is the current number of threads simultaneously waiting for the
checkpoint-safe lock to perform a checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: waiters max</p></td>
<td><p>This is the maximum number of threads ever simultaneously waiting for the
checkpoint-safe lock to perform a checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: non-checkpoint client wait on mo lock</p></td>
<td><p>The number of times a non-checkpoint client thread waited for the
multi-operation lock.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: non-checkpoint client wait on cs lock</p></td>
<td><p>The number of times a non-checkpoint client thread waited for the
checkpoint-safe lock.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: checkpoint begin time</p></td>
<td><p>Cumulative time (in microseconds) required to mark all dirty nodes as
pending a checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: long checkpoint begin time</p></td>
<td><p>The total time, in microseconds, of long checkpoint begins. A long checkpoint
begin is one taking more than 1 second.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: long checkpoint begin count</p></td>
<td><p>The total number of times a checkpoint begin took more than 1 second.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: checkpoint end time</p></td>
<td><p>The time spent in checkpoint end operation in seconds.</p></td>
</tr>
<tr class="row-odd"><td><p>checkpoint: long checkpoint end time</p></td>
<td><p>The time spent in checkpoint end operation in seconds.</p></td>
</tr>
<tr class="row-even"><td><p>checkpoint: long checkpoint end count</p></td>
<td><p>This is the count of end_checkpoint operations that exceeded 1 minute.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: miss</p></td>
<td><p>This is a count of how many times the application was unable to access your
data in the internal cache.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: miss time</p></td>
<td><p>This is the total time, in microseconds, of how long the database has had to
wait for a disk read to complete.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: prefetches</p></td>
<td><p>This is the total number of times that a block of memory has been prefetched
into the database’s cache. Data is prefetched when the database’s algorithms
determine that a block of memory is likely to be accessed by the application.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: size current</p></td>
<td><p>This shows how much of the uncompressed data, in bytes, is currently in the
database’s internal cache.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: size limit</p></td>
<td><p>This shows how much of the uncompressed data, in bytes, will fit in the
database’s internal cache.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: size writing</p></td>
<td><p>This is the number of bytes that are currently queued up to be written to
disk.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: size nonleaf</p></td>
<td><p>This shows the amount of memory, in bytes, the current set of non-leaf nodes
occupy in the cache.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: size leaf</p></td>
<td><p>This shows the amount of memory, in bytes, the current set of (decompressed)
leaf nodes occupy in the cache.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: size rollback</p></td>
<td><p>This shows the rollback nodes size, in bytes, in the cache.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: size cachepressure</p></td>
<td><p>This shows the number of bytes causing cache pressure (the sum of buffers and
work done counters), helps to understand if cleaner threads are keeping up
with workload. It should really be looked at as more of a value to use in a
ratio of cache pressure / cache table size. The closer that ratio evaluates to
1, the higher the cache pressure.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: size currently cloned data for checkpoint</p></td>
<td><p>Amount of memory, in bytes, currently used for cloned nodes. During the
checkpoint operation, dirty nodes are cloned prior to
serialization/compression, then written to disk. After which, the memory for
the cloned block is returned for re-use.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: evictions</p></td>
<td><p>Number of blocks evicted from cache.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: cleaner executions</p></td>
<td><p>Total number of times the cleaner thread loop has executed.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: cleaner period</p></td>
<td><p><em>TokuDB</em> includes a cleaner thread that optimizes indexes in the background.
This variable is the time, in seconds, between the completion of a group of
cleaner operations and the beginning of the next group of cleaner operations.
The cleaner operations run on a background thread performing work that does
not need to be done on the client thread.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: cleaner iterations</p></td>
<td><p>This is the number of cleaner operations that are performed every cleaner
period.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: number of waits on cache pressure</p></td>
<td><p>The number of times a thread was stalled due to cache pressure.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: time waiting on cache pressure</p></td>
<td><p>Total time, in microseconds, waiting on cache pressure to subside.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: number of long waits on cache pressure</p></td>
<td><p>The number of times a thread was stalled for more than 1 second due to cache
pressure.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: long time waiting on cache pressure</p></td>
<td><p>Total time, in microseconds, waiting on cache pressure to subside for more
than 1 second.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: client pool: number of threads in pool</p></td>
<td><p>The number of threads in the client thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: client pool: number of currently active threads in pool</p></td>
<td><p>The number of currently active threads in the client thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: client pool: number of currently queued work items</p></td>
<td><p>The number of currently queued work items in the client thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: client pool: largest number of queued work items</p></td>
<td><p>The largest number of queued work items in the client thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: client pool: total number of work items processed</p></td>
<td><p>The total number of work items processed in the client thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: client pool: total execution time of processing work items</p></td>
<td><p>The total execution time of processing work items in the client thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: cachetable pool: number of threads in pool</p></td>
<td><p>The number of threads in the cachetable thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: cachetable pool: number of currently active threads in pool</p></td>
<td><p>The number of currently active threads in the cachetable thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: cachetable pool: number of currently queued work items</p></td>
<td><p>The number of currently queued work items in the cachetable thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: cachetable pool: largest number of queued work items</p></td>
<td><p>The largest number of queued work items in the cachetable thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: cachetable pool: total number of work items processed</p></td>
<td><p>The total number of work items processed in the cachetable thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: cachetable pool: total execution time of processing work items</p></td>
<td><p>The total execution time of processing work items in the cachetable thread
pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: checkpoint pool: number of threads in pool</p></td>
<td><p>The number of threads in the checkpoint thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: checkpoint pool: number of currently active threads in pool</p></td>
<td><p>The number of currently active threads in the checkpoint thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: checkpoint pool: number of currently queued work items</p></td>
<td><p>The number of currently queued work items in the checkpoint thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: checkpoint pool: largest number of queued work items</p></td>
<td><p>The largest number of queued work items in the checkpoint thread pool.</p></td>
</tr>
<tr class="row-even"><td><p>cachetable: checkpoint pool: total number of work items processed</p></td>
<td><p>The total number of work items processed in the checkpoint thread pool.</p></td>
</tr>
<tr class="row-odd"><td><p>cachetable: checkpoint pool: total execution time of processing work items</p></td>
<td><p>The total execution time of processing work items in the checkpoint thread
pool.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: memory size</p></td>
<td><p>The amount of memory, in bytes, that the locktree is currently using.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: memory size limit</p></td>
<td><p>The maximum amount of memory, in bytes, that the locktree is allowed to use.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: number of times lock escalation ran</p></td>
<td><p>Number of times the locktree needed to run lock escalation to reduce its
memory footprint.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: time spent running escalation (seconds)</p></td>
<td><p>Total number of seconds spent performing locktree escalation.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: latest post-escalation memory size</p></td>
<td><p>Size of the locktree, in bytes, after most current locktree escalation.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: number of locktrees open now</p></td>
<td><p>Number of locktrees currently open.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: number of pending lock requests</p></td>
<td><p>Number of requests waiting for a lock grant.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: number of locktrees eligible for the STO</p></td>
<td><p>Number of locktrees eligible for “Single Transaction Optimizations”. <code class="docutils literal notranslate"><span class="pre">STO</span></code>
optimization are behaviors that can happen within the locktree when there is
exactly one transaction active within the locktree. This is a not a useful
value for a regular user to use for any purpose.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: number of times a locktree ended the STO early</p></td>
<td><p>Total number of times a “single transaction optimization” was ended early due
to another trans- action starting.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: time spent ending the STO early (seconds)</p></td>
<td><p>Total number of seconds ending “Single Transaction Optimizations”. <code class="docutils literal notranslate"><span class="pre">STO</span></code>
optimization are behaviors that can happen within the locktree when there is
exactly one transaction active within the locktree. This is a not a useful
value for a regular user to use for any purpose.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: number of wait locks</p></td>
<td><p>Number of times that a lock request could not be acquired because of a
conflict with some other transaction.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: time waiting for locks</p></td>
<td><p>Total time, in microseconds, spend by some client waiting for a lock conflict
to be resolved.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: number of long wait locks</p></td>
<td><p>Number of lock waits greater than 1 second in duration.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: long time waiting for locks</p></td>
<td><p>Total time, in microseconds, of the long waits.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: number of lock timeouts</p></td>
<td><p>Count of the number of times that a lock request timed out.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: number of waits on lock escalation</p></td>
<td><p>When the sum of the sizes of locks taken reaches the lock tree limit, we run
lock escalation on a background thread. The clients threads need to wait for
escalation to consolidate locks and free up memory. This counter counts the
number of times a client thread has to wait on lock escalation.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: time waiting on lock escalation</p></td>
<td><p>Total time, in microseconds, that a client thread spent waiting for lock
escalation to free up memory.</p></td>
</tr>
<tr class="row-odd"><td><p>locktree: number of long waits on lock escalation</p></td>
<td><p>Number of times that a client thread had to wait on lock escalation and the
wait time was greater than 1 second.</p></td>
</tr>
<tr class="row-even"><td><p>locktree: long time waiting on lock escalation</p></td>
<td><p>Total time, in microseconds, of the long waits for lock escalation to free up
memory.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: dictionary updates</p></td>
<td><p>This is the total number of rows that have been updated in all primary and
secondary indexes combined, if those updates have been done with a separate
recovery log entry per index.</p></td>
</tr>
<tr class="row-even"><td><p>ft: dictionary broadcast updates</p></td>
<td><p>This is the number of broadcast updates that have been successfully performed.
A broadcast update is an update that affects all rows in a dictionary.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: descriptor set</p></td>
<td><p>This is the number of time a descriptor was updated when the entire dictionary
was updated (for example, when the schema has been changed).</p></td>
</tr>
<tr class="row-even"><td><p>ft: messages ignored by leaf due to msn</p></td>
<td><p>The number of messages that were ignored by a leaf because it had already been
applied.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: total search retries due to TRY AGAIN</p></td>
<td><p>Total number of search retries due to TRY AGAIN. Internal value that is no use
to anyone other than a developer debugging a specific query/search issue.</p></td>
</tr>
<tr class="row-even"><td><p>ft: searches requiring more tries than the height of the tree</p></td>
<td><p>Number of searches that required more tries than the height of the tree.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: searches requiring more tries than the height of the tree plus three</p></td>
<td><p>Number of searches that required more tries than the height of the tree plus
three.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf nodes flushed to disk (not for checkpoint)</p></td>
<td><p>Number of leaf nodes flushed to disk, not for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf nodes flushed to disk (not for checkpoint) (bytes)</p></td>
<td><p>Number of bytes of leaf nodes flushed to disk, not for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf nodes flushed to disk (not for checkpoint) (uncompressed bytes)</p></td>
<td><p>Number of bytes of leaf nodes flushed to disk, not for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf nodes flushed to disk (not for checkpoint) (seconds)</p></td>
<td><p>Number of seconds waiting for IO when writing leaf nodes flushed to disk, not
for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf nodes flushed to disk (not for checkpoint)</p></td>
<td><p>Number of non-leaf nodes flushed to disk, not for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf nodes flushed to disk (not for checkpoint) (bytes)</p></td>
<td><p>Number of bytes of non-leaf nodes flushed to disk, not for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf nodes flushed to disk (not for checkpoint) (uncompressed bytes)</p></td>
<td><p>Number of uncompressed bytes of non-leaf nodes flushed to disk, not for
checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf nodes flushed to disk (not for checkpoint) (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when writing non-leaf nodes flushed to disk,
not for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf nodes flushed to disk (for checkpoint)</p></td>
<td><p>Number of leaf nodes flushed to disk for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf nodes flushed to disk (for checkpoint) (bytes)</p></td>
<td><p>Number of bytes of leaf nodes flushed to disk for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf nodes flushed to disk (for checkpoint) (uncompressed bytes)</p></td>
<td><p>Number of uncompressed bytes of leaf nodes flushed to disk for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf nodes flushed to disk (for checkpoint) (seconds)</p></td>
<td><p>Number of seconds waiting for IO when writing leaf nodes flushed to disk for
checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf nodes flushed to disk (for checkpoint)</p></td>
<td><p>Number of non-leaf nodes flushed to disk for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf nodes flushed to disk (for checkpoint) (bytes)</p></td>
<td><p>Number of bytes of non-leaf nodes flushed to disk for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf nodes flushed to disk (for checkpoint) (uncompressed bytes)</p></td>
<td><p>Number of uncompressed bytes of non-leaf nodes flushed to disk for checkpoint.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf nodes flushed to disk (for checkpoint) (seconds)</p></td>
<td><p>Number of seconds waiting for IO when writing non-leaf nodes flushed to disk
for checkpoint.</p></td>
</tr>
<tr class="row-even"><td><p>ft: uncompressed / compressed bytes written (leaf)</p></td>
<td><p>Ratio of uncompressed bytes (in-memory) to compressed bytes (on-disk) for leaf
nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: uncompressed / compressed bytes written (nonleaf)</p></td>
<td><p>Ratio of uncompressed bytes (in-memory) to compressed bytes (on-disk) for
non-leaf nodes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: uncompressed / compressed bytes written (overall)</p></td>
<td><p>Ratio of uncompressed bytes (in-memory) to compressed bytes (on-disk) for all
nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf node partial evictions</p></td>
<td><p>The number of times a partition of a non-leaf node was evicted from the cache.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf node partial evictions (bytes)</p></td>
<td><p>The number of bytes freed by evicting partitions of non-leaf nodes from the
cache.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf node partial evictions</p></td>
<td><p>The number of times a partition of a leaf node was evicted from the cache.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf node partial evictions (bytes)</p></td>
<td><p>The number of bytes freed by evicting partitions of leaf nodes from the cache.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf node full evictions</p></td>
<td><p>The number of times a full leaf node was evicted from the cache.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf node full evictions (bytes)</p></td>
<td><p>The number of bytes freed by evicting full leaf nodes from the cache.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf node full evictions (bytes)</p></td>
<td><p>The number of bytes freed by evicting full non-leaf nodes from the cache.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf node full evictions</p></td>
<td><p>The number of times a full non-leaf node was evicted from the cache.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf nodes created</p></td>
<td><p>Number of created leaf nodes .</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf nodes created</p></td>
<td><p>Number of created non-leaf nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf nodes destroyed</p></td>
<td><p>Number of destroyed leaf nodes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf nodes destroyed</p></td>
<td><p>Number of destroyed non-leaf nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: bytes of messages injected at root (all trees)</p></td>
<td><p>Amount of messages, in bytes, injected at root (for all trees).</p></td>
</tr>
<tr class="row-even"><td><p>ft: bytes of messages flushed from h1 nodes to leaves</p></td>
<td><p>Amount of messages, in bytes, flushed from <code class="docutils literal notranslate"><span class="pre">h1</span></code> nodes to leaves.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: bytes of messages currently in trees (estimate)</p></td>
<td><p>Amount of messages, in bytes, currently in trees (estimate).</p></td>
</tr>
<tr class="row-even"><td><p>ft: messages injected at root</p></td>
<td><p>Number of messages injected at root node of a tree.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: broadcast messages injected at root</p></td>
<td><p>Number of broadcast messages injected at root node of a tree.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements decompressed as a target of a query</p></td>
<td><p>Number of basement nodes decompressed for queries.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements decompressed for prelocked range</p></td>
<td><p>Number of basement nodes decompressed by queries aggressively.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements decompressed for prefetch</p></td>
<td><p>Number of basement nodes decompressed by a prefetch thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements decompressed for write</p></td>
<td><p>Number of basement nodes decompressed for writes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers decompressed as a target of a query</p></td>
<td><p>Number of buffers decompressed for queries.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers decompressed for prelocked range</p></td>
<td><p>Number of buffers decompressed by queries aggressively.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers decompressed for prefetch</p></td>
<td><p>Number of buffers decompressed by a prefetch thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers decompressed for write</p></td>
<td><p>Number of buffers decompressed for writes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: pivots fetched for query</p></td>
<td><p>Number of pivot nodes fetched for queries.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: pivots fetched for query (bytes)</p></td>
<td><p>Number of bytes of pivot nodes fetched for queries.</p></td>
</tr>
<tr class="row-even"><td><p>ft: pivots fetched for query (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching pivot nodes for queries.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: pivots fetched for prefetch</p></td>
<td><p>Number of pivot nodes fetched by a prefetch thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft: pivots fetched for prefetch (bytes)</p></td>
<td><p>Number of bytes of pivot nodes fetched by a prefetch thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: pivots fetched for prefetch (seconds)</p></td>
<td><p>Number seconds waiting for I/O when fetching pivot nodes by a prefetch thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft: pivots fetched for write</p></td>
<td><p>Number of pivot nodes fetched for writes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: pivots fetched for write (bytes)</p></td>
<td><p>Number of bytes of pivot nodes fetched for writes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: pivots fetched for write (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching pivot nodes for writes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements fetched as a target of a query</p></td>
<td><p>Number of basement nodes fetched from disk for queries.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements fetched as a target of a query (bytes)</p></td>
<td><p>Number of basement node bytes fetched from disk for queries.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements fetched as a target of a query (seconds)</p></td>
<td><p>Number of seconds waiting for IO when fetching basement nodes from disk for
queries.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements fetched for prelocked range</p></td>
<td><p>Number of basement nodes fetched from disk aggressively.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements fetched for prelocked range (bytes)</p></td>
<td><p>Number of basement node bytes fetched from disk aggressively.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements fetched for prelocked range (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching basement nodes from disk
aggressively.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements fetched for prefetch</p></td>
<td><p>Number of basement nodes fetched from disk by a prefetch thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements fetched for prefetch (bytes)</p></td>
<td><p>Number of basement node bytes fetched from disk by a prefetch thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements fetched for prefetch (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching basement nodes from disk by a
prefetch thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements fetched for write</p></td>
<td><p>Number of basement nodes fetched from disk for writes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basements fetched for write (bytes)</p></td>
<td><p>Number of basement node bytes fetched from disk for writes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basements fetched for write (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching basement nodes from disk for
writes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers fetched as a target of a query</p></td>
<td><p>Number of buffers fetched from disk for queries.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers fetched as a target of a query (bytes)</p></td>
<td><p>Number of buffer bytes fetched from disk for queries.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers fetched as a target of a query (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching buffers from disk for queries.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers fetched for prelocked range</p></td>
<td><p>Number of buffers fetched from disk aggressively.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers fetched for prelocked range (bytes)</p></td>
<td><p>Number of buffer bytes fetched from disk aggressively.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers fetched for prelocked range (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching buffers from disk
aggressively.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers fetched for prefetch</p></td>
<td><p>Number of buffers fetched from disk by a prefetch thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers fetched for prefetch (bytes)</p></td>
<td><p>Number of buffer bytes fetched from disk by a prefetch thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers fetched for prefetch (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching buffers from disk by a
prefetch thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers fetched for write</p></td>
<td><p>Number of buffers fetched from disk for writes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: buffers fetched for write (bytes)</p></td>
<td><p>Number of buffer bytes fetched from disk for writes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: buffers fetched for write (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when fetching buffers from disk for writes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf compression to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent compressing leaf nodes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf serialization to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent serializing leaf nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: leaf decompression to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent decompressing leaf nodes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: leaf deserialization to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent deserializing leaf nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf compression to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent compressing non leaf nodes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf serialization to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent serializing non leaf nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: nonleaf decompression to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent decompressing non leaf nodes.</p></td>
</tr>
<tr class="row-even"><td><p>ft: nonleaf deserialization to memory (seconds)</p></td>
<td><p>Total time, in seconds, spent deserializing non leaf nodes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: roots split</p></td>
<td><p>Number of times the root split during promotion.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: leaf roots injected into</p></td>
<td><p>Number of times a message stopped at a root with height <code class="docutils literal notranslate"><span class="pre">0</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: h1 roots injected into</p></td>
<td><p>Number of times a message stopped at a root with height <code class="docutils literal notranslate"><span class="pre">1</span></code>.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: injections at depth 0</p></td>
<td><p>Number of times a message stopped at depth <code class="docutils literal notranslate"><span class="pre">0</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: injections at depth 1</p></td>
<td><p>Number of times a message stopped at depth <code class="docutils literal notranslate"><span class="pre">1</span></code>.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: injections at depth 2</p></td>
<td><p>Number of times a message stopped at depth <code class="docutils literal notranslate"><span class="pre">2</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: injections at depth 3</p></td>
<td><p>Number of times a message stopped at depth <code class="docutils literal notranslate"><span class="pre">3</span></code>.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: injections lower than depth 3</p></td>
<td><p>Number of times a message was promoted past depth <code class="docutils literal notranslate"><span class="pre">3</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: stopped because of a nonempty buffer</p></td>
<td><p>Number of times a message stopped because it reached a nonempty buffer.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: stopped at height 1</p></td>
<td><p>Number of times a message stopped because it had reached height <code class="docutils literal notranslate"><span class="pre">1</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: stopped because the child was locked or not at all in memory</p></td>
<td><p>Number of times promotion was stopped because the child node was locked or not
at all in memory. This is a not a useful value for a regular user to use for
any purpose.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: stopped because the child was not fully in memory</p></td>
<td><p>Number of times promotion was stopped because the child node was not at all in
memory. This is a not a useful value for a normal user to use for any purpose.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: stopped anyway, after locking the child</p></td>
<td><p>Number of times a message stopped before a child which had been locked.</p></td>
</tr>
<tr class="row-even"><td><p>ft: basement nodes deserialized with fixed-keysize</p></td>
<td><p>The number of basement nodes deserialized where all keys had the same size,
leaving the basement in a format that is optimal for in-memory workloads.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: basement nodes deserialized with variable-keysize</p></td>
<td><p>The number of basement nodes deserialized where all keys did not have the same
size, and thus ineligible for an in-memory optimization.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: succeeded in using the rightmost leaf shortcut</p></td>
<td><p>Rightmost insertions used the rightmost-leaf pin path, meaning that the
Fractal Tree index detected and properly optimized rightmost inserts.</p></td>
</tr>
<tr class="row-odd"><td><p>ft: promotion: tried the rightmost leaf shortcut but failed (out-of-bounds)</p></td>
<td><p>Rightmost insertions did not use the rightmost-leaf pin path, due to the
insert not actually being into the rightmost leaf node.</p></td>
</tr>
<tr class="row-even"><td><p>ft: promotion: tried the rightmost leaf shortcut but failed (child reactive)</p></td>
<td><p>Rightmost insertions did not use the rightmost-leaf pin path, due to the
leaf being too large (needed to split).</p></td>
</tr>
<tr class="row-odd"><td><p>ft: cursor skipped deleted leaf entries</p></td>
<td><p>Number of leaf entries skipped during search/scan because the result of
message application and reconciliation of the leaf entry MVCC stack reveals
that the leaf entry is deleted in the current transactions view. It is a good
indicator that there might be excessive garbage in a tree if a range scan
seems to take too long.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: total nodes potentially flushed by cleaner thread</p></td>
<td><p>Total number of nodes whose buffers are potentially flushed by cleaner thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: height-one nodes flushed by cleaner thread</p></td>
<td><p>Number of nodes of height one whose message buffers are flushed by cleaner
thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: height-greater-than-one nodes flushed by cleaner thread</p></td>
<td><p>Number of nodes of height &gt; 1 whose message buffers are flushed by cleaner
thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: nodes cleaned which had empty buffers</p></td>
<td><p>Number of nodes that are selected by cleaner, but whose buffers are empty.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: nodes dirtied by cleaner thread</p></td>
<td><p>Number of nodes that are made dirty by the cleaner thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: max bytes in a buffer flushed by cleaner thread</p></td>
<td><p>Max number of bytes in message buffer flushed by cleaner thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: min bytes in a buffer flushed by cleaner thread</p></td>
<td><p>Min number of bytes in message buffer flushed by cleaner thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: total bytes in buffers flushed by cleaner thread</p></td>
<td><p>Total number of bytes in message buffers flushed by cleaner thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: max workdone in a buffer flushed by cleaner thread</p></td>
<td><p>Max workdone value of any message buffer flushed by cleaner thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: min workdone in a buffer flushed by cleaner thread</p></td>
<td><p>Min workdone value of any message buffer flushed by cleaner thread.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: total workdone in buffers flushed by cleaner thread</p></td>
<td><p>Total workdone value of message buffers flushed by cleaner thread.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: times cleaner thread tries to merge a leaf</p></td>
<td><p>The number of times the cleaner thread tries to merge a leaf.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: cleaner thread leaf merges in progress</p></td>
<td><p>The number of cleaner thread leaf merges in progress.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: cleaner thread leaf merges successful</p></td>
<td><p>The number of times the cleaner thread successfully merges a leaf.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: nodes dirtied by cleaner thread leaf merges</p></td>
<td><p>The number of nodes dirtied by the “flush from root” process to merge a leaf node.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: total number of flushes done by flusher threads or cleaner threads</p></td>
<td><p>Total number of flushes done by flusher threads or cleaner threads.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: number of in memory flushes</p></td>
<td><p>Number of in-memory flushes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: number of flushes that read something off disk</p></td>
<td><p>Number of flushes that had to read a child (or part) off disk.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: number of flushes that triggered another flush in child</p></td>
<td><p>Number of flushes that triggered another flush in the child.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: number of flushes that triggered 1 cascading flush</p></td>
<td><p>Number of flushes that triggered 1 cascading flush.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: number of flushes that triggered 2 cascading flushes</p></td>
<td><p>Number of flushes that triggered 2 cascading flushes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: number of flushes that triggered 3 cascading flushes</p></td>
<td><p>Number of flushes that triggered 3 cascading flushes.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: number of flushes that triggered 4 cascading flushes</p></td>
<td><p>Number of flushes that triggered 4 cascading flushes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: number of flushes that triggered 5 cascading flushes</p></td>
<td><p>Number of flushes that triggered 5 cascading flushes.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: number of flushes that triggered over 5 cascading flushes</p></td>
<td><p>Number of flushes that triggered more than 5 cascading flushes.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: leaf node splits</p></td>
<td><p>Number of leaf nodes split.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: nonleaf node splits</p></td>
<td><p>Number of non-leaf nodes split.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: leaf node merges</p></td>
<td><p>Number of times leaf nodes are merged.</p></td>
</tr>
<tr class="row-even"><td><p>ft flusher: nonleaf node merges</p></td>
<td><p>Number of times non-leaf nodes are merged.</p></td>
</tr>
<tr class="row-odd"><td><p>ft flusher: leaf node balances</p></td>
<td><p>Number of times a leaf node is balanced.</p></td>
</tr>
<tr class="row-even"><td><p>hot: operations ever started</p></td>
<td><p>This variable shows the number of hot operations started (<code class="docutils literal notranslate"><span class="pre">OPTIMIZE</span> <span class="pre">TABLE</span></code>).
This is a not a useful value for a regular user to use for any purpose.</p></td>
</tr>
<tr class="row-odd"><td><p>hot: operations successfully completed</p></td>
<td><p>The number of hot operations that have successfully completed (<code class="docutils literal notranslate"><span class="pre">OPTIMIZE</span>
<span class="pre">TABLE</span></code>). This is a not a useful value for a regular user to use for any
purpose.</p></td>
</tr>
<tr class="row-even"><td><p>hot: operations aborted</p></td>
<td><p>The number of hot operations that have been aborted (<code class="docutils literal notranslate"><span class="pre">OPTIMIZE</span> <span class="pre">TABLE</span></code>).
This is a not a useful value for a regular user to use for any purpose.</p></td>
</tr>
<tr class="row-odd"><td><p>hot: max number of flushes from root ever required to optimize a tree</p></td>
<td><p>The maximum number of flushes from the root ever required to optimize a tree.</p></td>
</tr>
<tr class="row-even"><td><p>txn: begin</p></td>
<td><p>This is the number of transactions that have been started.</p></td>
</tr>
<tr class="row-odd"><td><p>txn: begin read only</p></td>
<td><p>Number of read only transactions started.</p></td>
</tr>
<tr class="row-even"><td><p>txn: successful commits</p></td>
<td><p>This is the total number of transactions that have been committed.</p></td>
</tr>
<tr class="row-odd"><td><p>txn: aborts</p></td>
<td><p>This is the total number of transactions that have been aborted.</p></td>
</tr>
<tr class="row-even"><td><p>logger: next LSN</p></td>
<td><p>This is the next unassigned Log Sequence Number. It will be assigned to the
next entry in the recovery log.</p></td>
</tr>
<tr class="row-odd"><td><p>logger: writes</p></td>
<td><p>Number of times the logger has written to disk.</p></td>
</tr>
<tr class="row-even"><td><p>logger: writes (bytes)</p></td>
<td><p>Number of bytes the logger has written to disk.</p></td>
</tr>
<tr class="row-odd"><td><p>logger: writes (uncompressed bytes)</p></td>
<td><p>Number of uncompressed the logger has written to disk.</p></td>
</tr>
<tr class="row-even"><td><p>logger: writes (seconds)</p></td>
<td><p>Number of seconds waiting for I/O when writing logs to disk.</p></td>
</tr>
<tr class="row-odd"><td><p>logger: number of long logger write operations</p></td>
<td><p>Number of times a logger write operation required 100ms or more.</p></td>
</tr>
<tr class="row-even"><td><p>indexer: number of indexers successfully created</p></td>
<td><p>This is the number of times one of our internal objects, a indexer, has been
created.</p></td>
</tr>
<tr class="row-odd"><td><p>indexer: number of calls to toku_indexer_create_indexer() that failed</p></td>
<td><p>This is the number of times a indexer was requested but could not be created.</p></td>
</tr>
<tr class="row-even"><td><p>indexer: number of calls to indexer-&gt;build() succeeded</p></td>
<td><p>This is the total number of times that indexes were created using a indexer.</p></td>
</tr>
<tr class="row-odd"><td><p>indexer: number of calls to indexer-&gt;build() failed</p></td>
<td><p>This is the total number of times that indexes were unable to be created using a indexer</p></td>
</tr>
<tr class="row-even"><td><p>indexer: number of calls to indexer-&gt;close() that succeeded</p></td>
<td><p>This is the number of indexers that successfully created the requested index(es).</p></td>
</tr>
<tr class="row-odd"><td><p>indexer: number of calls to indexer-&gt;close() that failed</p></td>
<td><p>This is the number of indexers that were unable to create the requested index(es).</p></td>
</tr>
<tr class="row-even"><td><p>indexer: number of calls to indexer-&gt;abort()</p></td>
<td><p>This is the number of indexers that were aborted.</p></td>
</tr>
<tr class="row-odd"><td><p>indexer: number of indexers currently in existence</p></td>
<td><p>This is the number of indexers that currently exist.</p></td>
</tr>
<tr class="row-even"><td><p>indexer: max number of indexers that ever existed simultaneously</p></td>
<td><p>This is the maximum number of indexers that ever existed simultaneously.</p></td>
</tr>
<tr class="row-odd"><td><p>loader: number of loaders successfully created</p></td>
<td><p>This is the number of times one of our internal objects, a loader, has been
created.</p></td>
</tr>
<tr class="row-even"><td><p>loader: number of calls to toku_loader_create_loader() that failed</p></td>
<td><p>This is the number of times a loader was requested but could not be created.</p></td>
</tr>
<tr class="row-odd"><td><p>loader: number of calls to loader-&gt;put() succeeded</p></td>
<td><p>This is the total number of rows that were inserted using a loader.</p></td>
</tr>
<tr class="row-even"><td><p>loader: number of calls to loader-&gt;put() failed</p></td>
<td><p>This is the total number of rows that were unable to be inserted using a
loader.</p></td>
</tr>
<tr class="row-odd"><td><p>loader: number of calls to loader-&gt;close() that succeeded</p></td>
<td><p>This is the number of loaders that successfully created the requested table.</p></td>
</tr>
<tr class="row-even"><td><p>loader: number of calls to loader-&gt;close() that failed</p></td>
<td><p>This is the number of loaders that were unable to create the requested table.</p></td>
</tr>
<tr class="row-odd"><td><p>loader: number of calls to loader-&gt;abort()</p></td>
<td><p>This is the number of loaders that were aborted.</p></td>
</tr>
<tr class="row-even"><td><p>loader: number of loaders currently in existence</p></td>
<td><p>This is the number of loaders that currently exist.</p></td>
</tr>
<tr class="row-odd"><td><p>loader: max number of loaders that ever existed simultaneously</p></td>
<td><p>This is the maximum number of loaders that ever existed simultaneously.</p></td>
</tr>
<tr class="row-even"><td><p>memory: number of malloc operations</p></td>
<td><p>Number of calls to <code class="docutils literal notranslate"><span class="pre">malloc()</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>memory: number of free operations</p></td>
<td><p>Number of calls to <code class="docutils literal notranslate"><span class="pre">free()</span></code>.</p></td>
</tr>
<tr class="row-even"><td><p>memory: number of realloc operations</p></td>
<td><p>Number of calls to <code class="docutils literal notranslate"><span class="pre">realloc()</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>memory: number of malloc operations that failed</p></td>
<td><p>Number of failed calls to <code class="docutils literal notranslate"><span class="pre">malloc()</span></code>.</p></td>
</tr>
<tr class="row-even"><td><p>memory: number of realloc operations that failed</p></td>
<td><p>Number of failed calls to <code class="docutils literal notranslate"><span class="pre">realloc()</span></code>.</p></td>
</tr>
<tr class="row-odd"><td><p>memory: number of bytes requested</p></td>
<td><p>Total number of bytes requested from memory allocator library.</p></td>
</tr>
<tr class="row-even"><td><p>memory: number of bytes freed</p></td>
<td><p>Total number of bytes allocated from memory allocation library that have been
freed (used - freed = bytes in use).</p></td>
</tr>
<tr class="row-odd"><td><p>memory: largest attempted allocation size</p></td>
<td><p>Largest number of bytes in a single successful <code class="docutils literal notranslate"><span class="pre">malloc()</span></code> operation.</p></td>
</tr>
<tr class="row-even"><td><p>memory: size of the last failed allocation attempt</p></td>
<td><p>Largest number of bytes in a single failed <code class="docutils literal notranslate"><span class="pre">malloc()</span></code> operation.</p></td>
</tr>
<tr class="row-odd"><td><p>memory: number of bytes used (requested + overhead)</p></td>
<td><p>Total number of bytes allocated by memory allocator library.</p></td>
</tr>
<tr class="row-even"><td><p>memory: estimated maximum memory footprint</p></td>
<td><p>Maximum memory footprint of the storage engine,
the max value of (used - freed).</p></td>
</tr>
<tr class="row-odd"><td><p>memory: mallocator version</p></td>
<td><p>Version string from in-use memory allocator.</p></td>
</tr>
<tr class="row-even"><td><p>memory: mmap threshold</p></td>
<td><p>The threshold for malloc to use mmap.</p></td>
</tr>
<tr class="row-odd"><td><p>filesystem: ENOSPC redzone state</p></td>
<td><p>The state of how much disk space exists with respect to the red zone value.
Redzone is space greater than <a class="reference internal" href="https://docs.percona.com/percona-server/8.0/tokudb/tokudb_variables.html#tokudb_fs_reserve_percent"><span class="std std-ref">tokudb_fs_reserve_percent</span></a> and less
than full disk.</p>
<p>Valid values are:</p>
<dl class="field-list simple">
<dt class="field-odd">0</dt>
<dd class="field-odd"><p>Space is available</p>
</dd>
<dt class="field-even">1</dt>
<dd class="field-even"><p>Warning, with 2x of redzone value. Operations are allowed, but engine
status prints a warning.</p>
</dd>
<dt class="field-odd">2</dt>
<dd class="field-odd"><p>In red zone, insert operations are blocked</p>
</dd>
<dt class="field-even">3</dt>
<dd class="field-even"><p>All operations are blocked</p>
</dd>
</dl>
</td>
</tr>
<tr class="row-even"><td><p>filesystem: threads currently blocked by full disk</p></td>
<td><p>This is the number of threads that are currently blocked because they are
attempting to write to a full disk. This is normally zero. If this value is
non-zero, then a warning will appear in the “disk free space” field.</p></td>
</tr>
<tr class="row-odd"><td><p>filesystem: number of operations rejected by enospc prevention (red zone)</p></td>
<td><p>This is the number of database inserts that have been rejected because the
amount of disk free space was less than the reserve.</p></td>
</tr>
<tr class="row-even"><td><p>filesystem: most recent disk full</p></td>
<td><p>This is the most recent time when the disk file system was entirely full. If
the disk has never been full, then this value will be <code class="docutils literal notranslate"><span class="pre">Dec</span> <span class="pre">31,</span> <span class="pre">1969</span></code> on
Linux hosts.</p></td>
</tr>
<tr class="row-odd"><td><p>filesystem: number of write operations that returned ENOSPC</p></td>
<td><p>This is the number of times that an attempt to write to disk failed because
the disk was full. If the disk is full, this number will continue increasing
until space is available.</p></td>
</tr>
<tr class="row-even"><td><p>filesystem: fsync time</p></td>
<td><p>This the total time, in microseconds, used to fsync to disk.</p></td>
</tr>
<tr class="row-odd"><td><p>filesystem: fsync count</p></td>
<td><p>This is the total number of times the database has flushed the operating
system’s file buffers to disk.</p></td>
</tr>
<tr class="row-even"><td><p>filesystem: long fsync time</p></td>
<td><p>This the total time, in microseconds, used to fsync to disk when the operation
required more than 1 second.</p></td>
</tr>
<tr class="row-odd"><td><p>filesystem: long fsync count</p></td>
<td><p>This is the total number of times the database has flushed the operating
system’s file buffers to disk and this operation required more than 1 second.</p></td>
</tr>
<tr class="row-even"><td><p>context: tree traversals blocked by a full fetch</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of a full fetch.</p></td>
</tr>
<tr class="row-odd"><td><p>context: tree traversals blocked by a partial fetch</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of a partial fetch.</p></td>
</tr>
<tr class="row-even"><td><p>context: tree traversals blocked by a full eviction</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of a full eviction.</p></td>
</tr>
<tr class="row-odd"><td><p>context: tree traversals blocked by a partial eviction</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of a partial eviction.</p></td>
</tr>
<tr class="row-even"><td><p>context: tree traversals blocked by a message injection</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of message injection.</p></td>
</tr>
<tr class="row-odd"><td><p>context: tree traversals blocked by a message application</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of message application (applying fresh ancestors
messages to a basement node).</p></td>
</tr>
<tr class="row-even"><td><p>context: tree traversals blocked by a flush</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of a buffer flush from parent to child.</p></td>
</tr>
<tr class="row-odd"><td><p>context: tree traversals blocked by a the cleaner thread</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of a cleaner thread.</p></td>
</tr>
<tr class="row-even"><td><p>context: tree traversals blocked by something uninstrumented</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed while pinning nodes
from root to leaf because of something uninstrumented.</p></td>
</tr>
<tr class="row-odd"><td><p>context: promotion blocked by a full fetch (should never happen)</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of a
full fetch.</p></td>
</tr>
<tr class="row-even"><td><p>context: promotion blocked by a partial fetch (should never happen)</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of a
partial fetch.</p></td>
</tr>
<tr class="row-odd"><td><p>context: promotion blocked by a full eviction (should never happen)</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of a
full eviction.</p></td>
</tr>
<tr class="row-even"><td><p>context: promotion blocked by a partial eviction (should never happen)</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of a
partial eviction.</p></td>
</tr>
<tr class="row-odd"><td><p>context: promotion blocked by a message injection</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of
message injection.</p></td>
</tr>
<tr class="row-even"><td><p>context: promotion blocked by a message application</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of
message application (applying fresh ancestors messages to a basement node).</p></td>
</tr>
<tr class="row-odd"><td><p>context: promotion blocked by a flush</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of a
buffer flush from parent to child.</p></td>
</tr>
<tr class="row-even"><td><p>context: promotion blocked by the cleaner thread</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of a
cleaner thread.</p></td>
</tr>
<tr class="row-odd"><td><p>context: promotion blocked by something uninstrumented</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed within promotion
(pinning nodes from root to the buffer to receive the message) because of
something uninstrumented.</p></td>
</tr>
<tr class="row-even"><td><p>context: something uninstrumented blocked by something uninstrumented</p></td>
<td><p>Number of times node <code class="docutils literal notranslate"><span class="pre">rwlock</span></code> contention was observed for an uninstrumented
process because of something uninstrumented.</p></td>
</tr>
<tr class="row-odd"><td><p>handlerton: primary key bytes inserted</p></td>
<td><p>Total number of bytes inserted into all primary key indexes.</p></td>
</tr>
</tbody>
</table>