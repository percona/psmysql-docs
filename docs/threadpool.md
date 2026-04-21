# Thread pool

Thread pooling can improve performance and scalability for MySQL databases. This technique reuses a fixed number of threads to handle multiple client connections and execute statements. It reduces the overhead of creating and destroying threads and avoids the contention and context switching that can occur when there are too many threads.

If you have fewer than 20,000 connections, using the thread pool does not provide significant benefits. It’s better to keep thread pooling disabled and use the default method.

The default method, called one-thread-per-connection, creates a new thread for each client that connects to the MySQL server. This thread manages all queries and responses for that connection until it’s closed. This approach works well for a moderate number of connections, but it can become inefficient as the number of connections increases.

MySQL supports thread pooling through the thread pool plugin, which replaces the default one-thread-per-connection model. When a statement arrives, the thread group either begins executing it immediately or queues it for later execution in a round-robin fashion. The high-priority queue consists of several thread groups, each managing client connections. Each thread group has a listener thread that listens for incoming statements from the connections assigned to the group. The thread pool exposes several system variables that can be used to configure its operation, such as thread_pool_size, thread_pool_algorithm, thread_pool_stall_limit, and others.

The thread pool plugin consists of several thread groups, each of which manages a set of client connections. As connections are established, the thread pool assigns them to thread groups using the round-robin method. This method assigns threads fairly and efficiently. Here's how it works:

1. The thread pool starts with a set number of thread groups.

2. When a new task arrives, the pool needs to assign it to a group.

3. It does this by going through the groups in order, one by one.

4. Let's say you have four thread groups. The assignment would work like this:
   - Task 1 goes to Group 1
   - Task 2 goes to Group 2
   - Task 3 goes to Group 3
   - Task 4 goes to Group 4
   - Task 5 goes back to Group 1
   
5. This pattern continues, always moving to the next group and starting over when it reaches the end.

6. Each group handles its assigned tasks using its available threads.

This round-robin approach spreads work evenly across all groups. It prevents any single group from getting overloaded while others sit idle. This method helps maintain balanced performance across the system.

MySQL executes statements using one thread per client connection. When the number of connections increases past a specific point, performance degrades.
This feature introduces a dynamic thread pool, which enables the server to maintain top performance even with a large number of client connections. The server decreases the number of threads using the thread pool and reduces the context switching and hot lock contentions. The thread pool is most effective with `OLTP` workloads (relatively short CPU-bound queries).

Set the thread pool variable [thread_handling](#thread_handling) to `pool-of-threads` by adding the following line to `my.cnf`:

```text
thread_handling=pool-of-threads
```

Although the default values for the thread pool should provide good performance, additional tuning should be performed with the dynamic system variables. The goal is to minimize the number of open transactions on the server. Short-running transactions commit faster and deallocate server resources and locks.

Due to the following differences, this implementation is not compatible with upstream:

* Built into the server, upstream implements the thread pool as a plugin

* Does not minimize the number of concurrent transactions

Priority Queue:

A queue that assigns a priority to each data element and processes them according to their priority. The data element with the highest priority is served first, regardless of its order in the queue. A priority queue can be implemented using an array, a linked list, a heap, or a binary search tree. It can also be ascending or descending, meaning that the highest priority is either the smallest or the largest value.

## Priority connection scheduling

The thread pool limits the number of concurrently running queries. The number of open transactions may remain high. Connections with already-started transactions are added to the end of the queue. A high number of open transactions has implications for the currently running queries. The [thread_pool_high_prio_tickets](#thread_pool_high_prio_tickets) variable controls the high-priority queue policy and assigns tickets to each new connection.

The thread pool adds the connection to the high-priority queue and decrements the ticket if the connection has the following attributes:

* Has an open transaction

* Has a non-zero number of high-priority tickets

Otherwise, the variable adds the connection to the normal-priority queue with the initial value.

Each time, the thread pool checks the high-priority queue for the next connection. When the high-priority queue is empty, the thread pool picks connections from the normal-priority queue. The default behavior is to put events from already started transactions into the high-priority queue.

If the value equals `0`, all connections are put into the normal-priority queue. If the value exceeds zero, each connection could be put into a high-priority queue.

The [thread_pool_high_prio_mode](#thread_pool_high_prio_mode) variable prioritizes all statements for a connection or assigns connections to the normal-priority queue. To implement this new [thread_pool_high_prio_mode](#thread_pool_high_prio_mode) variable

## Normal-priority queue throttling

Thread pool performance can degrade, or even deadlock, under high concurrency when a thread group becomes oversubscribed — that is, when the number of active worker threads in the group reaches [`thread_pool_oversubscribe`](#thread_pool_oversubscribe) — and most of those threads are simultaneously waiting on locks held by a transaction whose connection has not yet been picked up by the thread pool.

The oversubscribe limit does not account for threads that have marked themselves inactive while waiting. As a result, the total number of threads in the pool (both active and waiting) continues to grow until the pool reaches [`thread_pool_max_threads`](#thread_pool_max_threads). If the connection executing the transaction that holds the lock enters the thread pool before `thread_pool_max_threads` is reached, the pool ends up running a large number of threads concurrently (proportional to [`thread_pool_max_threads`](#thread_pool_max_threads)), resulting in suboptimal performance. Otherwise, the pool deadlocks, because no more threads can be created to process the blocking transactions and release their locks.

To prevent this scenario, the thread pool throttles the normal-priority queue when the total number of worker threads (both active and waiting) reaches the [`thread_pool_oversubscribe`](#thread_pool_oversubscribe) limit. While the pool is throttled, new transactions are not started and no new threads are created; the pool processes only queued events from already-started transactions, allowing their locks to be released so the pool can drain.

## Handling long network waits

Specific workloads (large result sets, BLOBs, slow clients) can wait longer on network I/O (socket reads and writes). Whenever the server waits, this should be communicated to the thread pool so it can start a new query by either waking a waiting thread or sometimes creating a new one.

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


Defines how the server dispatches statements from client connections to execution threads. The default, `one-thread-per-connection`, dedicates a single thread to each connection for the connection's entire lifetime. To activate the thread pool, set `thread_handling` to `pool-of-threads` in `my.cnf` and restart the server; all connections are then processed through the shared pool controlled by [`thread_pool_size`](#thread_pool_size) and the other `thread_pool_*` variables. The `no-threads` value serves all connections from a single thread and is intended for debugging only. Because `thread_handling` is not dynamic, changing the value requires a server restart. As a rule of thumb, the thread pool benefits workloads with very high connection counts (typically 20,000 or more) and short CPU-bound queries; for smaller connection counts, `one-thread-per-connection` usually performs better.

| Value                     | Description                                                  |
|---------------------------|--------------------------------------------------------------|
| one-thread-per-connection | One thread handles all requests for a connection.            |
| pool-of-threads           | A thread pool handles requests for all connections.          |
| no-threads                | A single thread serves all connections (debugging mode only).|

### `thread_pool_high_prio_mode`

This variable provides more fine-grained control over high-priority scheduling globally or per connection.

The following values are allowed:

| Value          | Description                                                                                                                                                                                                                         |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `transactions` | Default. Only statements from already started transactions may go into the high-priority queue, depending on the number of high-priority tickets currently available in the connection (see [`thread_pool_high_prio_tickets`](#thread_pool_high_prio_tickets)). |
| `statements`   | All individual statements go into the high-priority queue, regardless of transactional state or available tickets. Use the `statements` value to prioritize `AUTOCOMMIT` transactions or administrative statements. Setting `thread_pool_high_prio_mode` to `statements` globally effectively disables high-priority scheduling, because all connections use the high-priority queue. |
| `none`         | Disables the priority queue for a connection. Useful for connections that are insensitive to execution latency, such as monitoring. Setting `thread_pool_high_prio_mode` to `none` globally effectively disables high-priority scheduling, because all connections use the normal-priority queue. |

### `thread_pool_high_prio_tickets`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global, Session    |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 4294967295         |

This variable controls the high-priority queue policy. Assigns the selected number of tickets to each new connection to enter the high-priority queue. Setting this variable to `0` disables the high-priority queue.

### `thread_pool_idle_timeout`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 60 (seconds)       |

Defines the number of seconds a worker thread that has no work remains in the thread pool before exiting. When an idle thread's wait exceeds `thread_pool_idle_timeout`, the thread is removed from the pool, freeing memory and OS resources; if load returns, a new worker thread is created (subject to [`thread_pool_oversubscribe`](#thread_pool_oversubscribe) and [`thread_pool_max_threads`](#thread_pool_max_threads)). A lower value reclaims resources faster under bursty or intermittent workloads but increases thread-creation overhead when activity resumes; a higher value keeps threads warm and reduces creation churn at the cost of additional idle memory. Observe [`Threadpool_idle_threads`](#threadpool_idle_threads) and [`Threadpool_threads`](#threadpool_threads) to see how many threads are being retained in the pool at the current setting.

### `thread_pool_max_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 100000             |

This variable can limit the maximum number of threads in the pool. When the limit is reached, the server does not create new threads.

### `thread_pool_oversubscribe`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 3                  |

Defines the maximum number of worker threads that may be active simultaneously within a single thread group. When a worker thread in a group blocks (on I/O, a lock, or is otherwise stalled — see [`thread_pool_stall_limit`](#thread_pool_stall_limit)), the group may create additional worker threads up to the `thread_pool_oversubscribe` limit so that queued requests can continue to be processed. A higher value improves responsiveness under workloads that frequently block, at the cost of more context switching and contention; a lower value keeps concurrency tighter to the CPU, but values below the default of `3` can cause frequent thread sleep and wake-up cycles. When the total number of worker threads in a group (both active and waiting) reaches the `thread_pool_oversubscribe` limit, the thread pool throttles the normal-priority queue (see [Normal-priority queue throttling](#normal-priority-queue-throttling)) to prevent deadlocks and runaway thread creation. Tune alongside [`thread_pool_size`](#thread_pool_size) and observe [`Threadpool_threads`](#threadpool_threads) together with the queue-wait metrics to evaluate the effect.

### `thread_pool_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | Number of processors   |

Defines the number of thread groups in the thread pool. Each thread group maintains its own high-priority and normal-priority queues and handles the connections assigned to the group, using one active worker thread at a time; additional worker threads may be created within the group up to the [`thread_pool_oversubscribe`](#thread_pool_oversubscribe) limit. New connections are distributed across the thread groups in round-robin order, so `thread_pool_size` effectively sets the target concurrency of the thread pool. As a starting point, use a value equal to the number of available CPU cores and tune from there based on observed [`Threadpool_idle_threads`](#threadpool_idle_threads), [`Threadpool_threads`](#threadpool_threads), and the queue-wait metrics [`Threadpool_average_queue_wait_us`](#threadpool_average_queue_wait_us) and [`Threadpool_average_hp_queue_wait_us`](#threadpool_average_hp_queue_wait_us).

### `thread_pool_stall_limit`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type:     | Numeric            |
| Default value: | 500 (ms)           |

Defines the number of milliseconds before a running thread is considered stalled. When this limit is reached, the thread pool will wake up or create another thread. This variable prevents a long-running query from monopolizing the pool.

## Status variables

### `Threadpool_average_hp_queue_wait_us`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | String             |

This status variable reports aggregated wait-time statistics, in microseconds, for requests waiting in the high-priority queue. The value is a formatted string, for example:

```text
avg: 0.000, min: 0.000, max: 0.000, dev: 0.000, cnt: 0
```

Each sample is a single wait-time measurement, in microseconds, taken when a request is dequeued by a worker thread. Every dequeued request contributes exactly one sample. The `cnt` field shows the number of samples collected since server start; `avg`, `min`, `max`, and `dev` (standard deviation) are computed across all samples. Requests that the listener thread picks up immediately, without waiting, are included as zero-valued samples.

### `Threadpool_average_queue_wait_us`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | String             |

This status variable reports aggregated wait-time statistics, in microseconds, for requests waiting in the normal-priority queue. The value is a formatted string, for example:

```text
avg: 590.000, min: 470.000, max: 736.000, dev: 110.266, cnt: 5
```

Each sample is a single wait-time measurement, in microseconds, taken when a request is dequeued by a worker thread. Every dequeued request contributes exactly one sample. The `cnt` field shows the number of samples collected since server start; `avg`, `min`, `max`, and `dev` (standard deviation) are computed across all samples. Requests that the listener thread picks up immediately, without waiting, are included as zero-valued samples.

### `Threadpool_idle_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the number of idle threads in the pool — worker threads that are part of the pool but are not currently executing a request. Together with [`Threadpool_threads`](#threadpool_threads), `Threadpool_idle_threads` indicates how busy the pool is: when the value is close to `Threadpool_threads`, the pool is underutilized; when the value is near zero, the pool is saturated. Threads that remain idle longer than [`thread_pool_idle_timeout`](#thread_pool_idle_timeout) seconds may exit the pool.

### `Threadpool_requests_starved_in_queue`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the number of requests in the normal-priority queue that are being starved by requests in the high-priority queue. A non-zero value indicates that worker threads are busy processing high-priority traffic and normal-priority requests are not being picked up, which can be used as an indicator of thread pool saturation.

### `Threadpool_requests_waiting_in_hp_queue`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the number of requests currently waiting in the thread pool's high-priority queue. Which requests enter the high-priority queue is governed by [`thread_pool_high_prio_mode`](#thread_pool_high_prio_mode) and [`thread_pool_high_prio_tickets`](#thread_pool_high_prio_tickets). A sustained or growing value indicates that high-priority traffic is arriving faster than worker threads can drain the queue. Observe `Threadpool_requests_waiting_in_hp_queue` alongside [`Threadpool_average_hp_queue_wait_us`](#threadpool_average_hp_queue_wait_us) to gauge the effect on latency, and alongside [`Threadpool_requests_starved_in_queue`](#threadpool_requests_starved_in_queue) to detect when high-priority traffic is starving the normal-priority queue.

### `Threadpool_requests_waiting_in_queue`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the number of requests currently waiting in the thread pool's normal-priority queue. Requests enter the normal-priority queue when they do not meet the criteria for the high-priority queue set by [`thread_pool_high_prio_mode`](#thread_pool_high_prio_mode) and [`thread_pool_high_prio_tickets`](#thread_pool_high_prio_tickets). A sustained or growing value indicates either that normal-priority traffic is arriving faster than worker threads can drain the queue, or that high-priority traffic is monopolizing the worker threads. Observe `Threadpool_requests_waiting_in_queue` alongside [`Threadpool_average_queue_wait_us`](#threadpool_average_queue_wait_us) to gauge the effect on latency, and alongside [`Threadpool_requests_starved_in_queue`](#threadpool_requests_starved_in_queue) to detect starvation by the high-priority queue.

### `Threadpool_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the total number of worker threads currently in the pool, including both idle threads and threads actively executing requests. The pool grows dynamically, up to [`thread_pool_max_threads`](#thread_pool_max_threads), as load increases and threads stall (see [`thread_pool_stall_limit`](#thread_pool_stall_limit)); threads that remain idle longer than [`thread_pool_idle_timeout`](#thread_pool_idle_timeout) seconds may exit. The target concurrency of the pool is set by [`thread_pool_size`](#thread_pool_size) and [`thread_pool_oversubscribe`](#thread_pool_oversubscribe). Compare `Threadpool_threads` with [`Threadpool_idle_threads`](#threadpool_idle_threads) to determine how many threads are actively running requests: busy threads = `Threadpool_threads` − `Threadpool_idle_threads`.
