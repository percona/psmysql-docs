# Percona Server for MySQL thread pool

!!! note "Version notice"

    This page documents the built-in Percona Server for MySQL thread pool.
    
    Percona Server for MySQL 9.7.2-2 and later also includes the MySQL thread_pool plugin. Only one implementation can be active at a timetime; configuring the built-in thread pool prevents the MySQL thread pool plugin from loading. See the [MySQL thread pool plugin](#mysql-thread-pool.md) for details.

Percona Server for MySQL provides thread pooling as a built-in feature controlled by the thread_handling system variable. Thread pooling replaces the default one-thread-per-connection model with a fixed set of worker threads, organized into thread groups, shared across client connections.

Set the thread pool variable [thread_handling](#thread_handling) to `pool-of-threads` by adding the following line to `my.cnf`:

```ini
thread_handling=pool-of-threads
```

## Priority connection scheduling

The thread pool limits concurrently running queries using high-priority and normal-priority queues. A connection enters the high-priority queue and decrements its ticket count if it meets both conditions:

* Has an active open transaction

* Holds a non-zero number of high-priority tickets (thread_pool_high_prio_tickets)

Otherwise, the connection enters the normal-priority queue. Worker threads check the high-priority queue first and process normal-priority requests only when the high-priority queue is empty. Setting high-priority tickets to `0` routes all connections to the normal-priority queue.

## Normal-priority queue throttling

Under high concurrency, thread groups can become oversubscribed when active worker threads reach [thread_pool_oversubscribe](#thread_pool_oversubscribe) while waiting on locks. Because oversubscription tracking excludes inactive waiting threads, total threads can grow until reaching [thread_pool_max_threads](#thread_pool_max_threads), causing performance degradation or deadlocks.

To prevent oversubscription deadlocks:

* The thread pool throttles the normal-priority queue when total worker threads (active and waiting) reach the [thread_pool_oversubscribe](#thread_pool_oversubscribe) limit.

* New transactions pause while throttled.

* Queued events from existing transactions continue processing, releasing locks so the pool can drain.

## Handling long network waits

Workloads with large result sets, BLOBs, or slow network I/O report socket waits to the thread pool. The pool responds by waking an idle worker thread or spawning a new thread to keep pending queries moving.

## System variables

### `thread_handling`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | Yes                       |
| Config file  | Yes                       |
| Scope        | Global                    |
| Dynamic      | No                        |
| Data type    | String                    |
| Default      | one-thread-per-connection |


Defines how the server dispatches statements from client connections to execution threads.

| Option | Description |
|---|---|
| `one-thread-per-connection` | Allocates one dedicated thread per client connection for its lifetime. |
| `pool-of-threads` | Shares execution requests across a managed thread pool. |
| `no-threads` | Executes all requests inside a single thread (debugging mode only). |

### `thread_pool_high_prio_mode`

Controls fine-grained high-priority queue scheduling.

| Value | Description |
|---|---|
| `transactions` | Default. Statement priority depends on active transactions and available tickets. |
| `statements` | Directs all individual statements to the high-priority queue, overriding transaction state and ticket limits. |
| `none` | Disables high-priority queuing for the connection, routing all statements to the normal-priority queue. |

### `thread_pool_high_prio_tickets`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global, Session    |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 4294967295         |

Sets the number of high-priority tickets assigned to each new connection. Setting this value to 0 disables the high-priority queue.

### `thread_pool_idle_timeout`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 60 (seconds)       |

Specifies the number of seconds an idle worker thread stays in the pool before exiting. Lower values reclaim memory faster during bursty workloads; higher values reduce thread-creation overhead when traffic resumes.

### `thread_pool_max_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 100000             |

Caps the maximum total number of threads allowed in the pool. When this limit is reached, the server refuses to spawn new worker threads.

### `thread_pool_oversubscribe`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 3                  |

Sets the maximum active worker threads permitted simultaneously within a single thread group. When threads stall on I/O or locks, the group creates worker threads up to this limit to keep queued requests moving.

### `thread_pool_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | Number of processors   |

Sets the number of thread groups in the thread pool. Connections are assigned to thread groups in round-robin order. Start with a value equal to the available CPU cores and tune based on queue metrics.

### `thread_pool_stall_limit`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type:     | Numeric            |
| Default value: | 500 (ms)           |

Defines the elapsed time in milliseconds before a running statement is marked stalled, triggering the pool to wake or spawn another thread to prevent long queries from blocking the group.

## Status variables

### `Threadpool_average_hp_queue_wait_us`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | String             |

Reports aggregated wait-time statistics in microseconds for requests in the high-priority queue: 

The value is a formatted string, for example:

```text
avg: 0.000, min: 0.000, max: 0.000, dev: 0.000, cnt: 0
```

* cnt: Number of samples collected since server startup.

* avg, min, max, dev: Computed wait-time metrics across all dequeued requests.

### `Threadpool_average_queue_wait_us`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | String             |

Reports aggregated wait-time statistics in microseconds for requests in the normal-priority queue:

```text
avg: 590.000, min: 470.000, max: 736.000, dev: 110.266, cnt: 5
```


### `Threadpool_idle_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

Tracks worker threads that are currently idle. Calculate active threads using: [Threadpool_threads](#threadpool_threads) - [Threadpool_idle_threads](#threadpool_idle_threads).

### `Threadpool_requests_starved_in_queue`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

Counts normal-priority requests starved because worker threads were occupied processing high-priority traffic.

### `Threadpool_requests_waiting_in_hp_queue`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

Tracks requests currently waiting in the high-priority queue. Sustained non-zero values indicate high-priority traffic is arriving faster than worker threads can drain it.

### `Threadpool_requests_waiting_in_queue`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

Tracks requests currently waiting in the normal-priority queue. High values indicate capacity bottlenecks or high-priority queue saturation.

### `Threadpool_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

Shows total worker threads in the pool, including both active and idle threads.