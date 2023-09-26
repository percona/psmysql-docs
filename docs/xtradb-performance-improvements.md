# XtraDB performance improvements for I/O-bound highly-concurrent workloads

## Priority refill for the buffer pool free list

In highly-concurrent I/O-bound workloads the following situation may happen:

* Buffer pool free lists are used faster than they are refilled by the LRU cleaner thread.

* Buffer pool free lists become empty and more and more query and utility (i.e., purge) threads stall, checking whether a buffer pool free list has became non-empty, sleeping, performing single-page LRU flushes.

* The number of buffer pool free list mutex waiters increases.

* When the LRU manager thread (or a single page LRU flush by a query thread) finally produces a free page, it is starved from putting it on the buffer
pool free list as it must acquire the buffer pool free list mutex too.
However, being one thread in up to hundreds, the chances of a prompt
acquisition are low.

This is addressed by delegating all the LRU flushes to the to the LRU manager
thread, never attempting to evict a page or perform a LRU single page flush by
a query thread, and introducing a backoff algorithm to reduce buffer pool free
list mutex pressure on empty buffer pool free lists. This is controlled through
a new system variable innodb_empty_free_list_algorithm.

### `innodb_empty_free_list_algorithm`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | legacy, backoff    |
| Default        | legacy             |

When `legacy` option is set, server will use the upstream algorithm and when
the `backoff` is selected, Percona implementation will be used.

## Multi-threaded LRU flusher

Percona Server for MySQL features a true multi-threaded LRU flushing. In this scheme, each buffer pool instance has its own dedicated LRU manager thread that is
tasked with performing LRU flushes and evictions to refill the free list of that
buffer pool instance. Existing multi-threaded flusher no longer does any LRU
flushing and is tasked with flush list flushing only.

* All threads still synchronize on each coordinator thread iteration. If a
particular flushing job is stuck on one of the worker threads, the rest will
idle until the stuck one completes.

* The coordinator thread heuristics focus on flush list adaptive flushing
without considering the state of free lists, which might be in need of urgent
refill for a subset of buffer pool instances on a loaded server.

* LRU flushing is serialized with flush list flushing for each buffer pool
instance, introducing the risk that the right flushing mode will not happen
for a particular instance because it is being flushed in the other mode.

The following InnoDB metrics are no longer accounted, as their semantics do
not make sense under the current LRU flushing design:
`buffer_LRU_batch_flush_avg_time_slot`, `buffer_LRU_batch_flush_avg_pass`,
`buffer_LRU_batch_flush_avg_time_thread`,
`buffer_LRU_batch_flush_avg_time_est`.

The need for InnoDB recovery thread writer threads is also removed,
consequently all associated code is deleted.


### `innodb_sched_priority_master`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Boolean            |

This variable can be added to the configuration file.

