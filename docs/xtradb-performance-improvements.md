# XtraDB performance improvements for I/O-bound highly-concurrent workloads

## Priority refill for the buffer pool free list

Under heavy concurrent I/O load, the buffer pool free list can fall behind
demand.

The following issues can occur:

* Query and purge threads consume free pages faster than the Least Recently Used
  (LRU) cleaner thread refills the free list

* Empty free lists force query and purge threads to poll, sleep, or run
  single-page LRU flushes

* Many waiting threads increase contention on the buffer pool free list mutex

* Mutex contention delays the return of freed pages to the free list

Percona Server for MySQL addresses these issues with the following changes:

* The LRU manager thread handles all LRU flushes

* Query threads avoid page eviction and single-page LRU flushes

* A backoff algorithm reduces mutex pressure on empty free lists

Configure this behavior with `innodb_empty_free_list_algorithm`.

### `innodb_empty_free_list_algorithm`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Enumeration        |
| Default:       | legacy             |

#### Values

| Value     | Description                                      |
| --------- | ------------------------------------------------ |
| `legacy`  | Uses the upstream algorithm. Default value       |
| `backoff` | Uses the Percona Server for MySQL algorithm      |

## Adaptive page cleaner flushing

InnoDB page cleaners flush dirty buffer pool pages to disk. This frees redo log
space.

The adaptive flushing algorithm sets the flush rate from checkpoint age.
Checkpoint age is the gap between the current Log Sequence Number (LSN) and the
LSN of the last completed checkpoint. A larger checkpoint age triggers more
aggressive flushing.

Percona Server for MySQL uses a different age-factor formula than upstream
MySQL. The `innodb_cleaner_lsn_age_factor` variable selects the formula.

The default value is `high_checkpoint`. Flushing starts slower at low
checkpoint ages. Flushing accelerates as checkpoint age grows. The server can
keep more dirty pages in the buffer pool. Write throughput improves on sustained
write-heavy workloads.

The `legacy` value uses the upstream MySQL formula. Flushing starts earlier for
a given checkpoint age. Use `legacy` when checkpoint age spikes cause flush
storms or write pauses with `high_checkpoint`.

Monitor checkpoint age with these status variables:

* [`Innodb_checkpoint_age`](innodb-show-status.md#innodb_checkpoint_age)

* `Innodb_checkpoint_max_age`

You can also use the InnoDB Checkpoint Age graph in Percona Monitoring and
Management (PMM). Keep checkpoint age high without flush storms or write pauses
near the maximum checkpoint age.

Adaptive flushing also uses these variables:

* `innodb_adaptive_flushing`

* `innodb_adaptive_flushing_lwm`

* `innodb_io_capacity`

* `innodb_io_capacity_max`

See the following posts for more detail on variable interaction:

* [Tuning MySQL/InnoDB Flushing for a Write-Intensive Workload :octicons-link-external-16:](https://www.percona.com/blog/tuning-mysql-innodb-flushing-for-a-write-intensive-workload/)

* [InnoDB Flushing in Action for Percona Server for MySQL :octicons-link-external-16:](https://www.percona.com/blog/innodb-flushing-in-action-for-percona-server-for-mysql/)

### `innodb_cleaner_lsn_age_factor`

| Option         | Description              |
| -------------- | ------------------------ |
| Command-line:  | Yes                      |
| Config file:   | Yes                      |
| Scope:         | Global                   |
| Dynamic:       | Yes                      |
| Data type:     | Enumeration              |
| Default:       | high_checkpoint          |

#### Values

| Value             | Description |
| ----------------- | ----------- |
| `high_checkpoint` | Uses the Percona Server for MySQL age-factor formula. Flushing pressure rises slowly at low checkpoint ages and faster at higher ages. The server keeps more dirty pages. Default value |
| `legacy`          | Uses the upstream MySQL age-factor formula. Flushing starts earlier for a given checkpoint age. Use when checkpoint age spikes cause flush storms or write pauses with `high_checkpoint` |

Change the value at runtime:

```sql
SET GLOBAL innodb_cleaner_lsn_age_factor = 'legacy';
```

Add a persistent setting in the option file:

```ini
[mysqld]
innodb_cleaner_lsn_age_factor = high_checkpoint
```

## Multi-threaded LRU flusher

Percona Server for MySQL restores the InnoDB LRU threads from earlier releases.

These threads flush pages by LRU.

These threads also reclaim free pages and move the pages to the free list.

Earlier releases always ran these threads.

Earlier releases had no option to enable or disable the threads.

The `innodb_lru_threads` variable enables or disables the threads.

Disable the threads for low-concurrency setups.

Enable the threads for high-concurrency setups.

The default value is OFF.

When `innodb_lru_threads` is ON, each buffer pool instance has a dedicated LRU
manager thread.

That thread flushes and evicts pages to refill the instance free list.

When `innodb_lru_threads` is OFF, page cleaners flush pages by LRU.

### `innodb_lru_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type:     | Boolean            |
| Default:       | OFF                |

Add a persistent setting in the option file:

```ini
[mysqld]
innodb_lru_threads=ON
```

### `innodb_sched_priority_master`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Boolean            |

Add this variable to the configuration file.
