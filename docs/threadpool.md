# Thread pool

You can use thread pooling for MySQL databases to improve performance and scalability. Thread pooling is a technique that reuses a fixed number of threads to handle multiple client connections and execute statements. Thread pooling reduces the overhead of creating and destroying threads, and avoids the contention and context switching that can occur when there are too many threads.

MySQL supports thread pooling through the thread pool plugin, which replaces the default one-thread-per-connection model. When a statement arrives, the thread group either begins executing it immediately or queues it for later execution in a round-robin fashion.  The high-priority queue consists of a number of thread groups, each of which manages a set of client connections.  Each thread group has a listener thread that listens for incoming statements from the connections assigned to the group.  The thread pool exposes several system variables that can be used to configure its operation, such as thread_pool_size, thread_pool_algorithm, thread_pool_stall_limit and others.

The thread pool plugin consists of a number of thread groups, each of which manages a set of client connections. As connections are established, the thread pool assigns them to thread groups in round-robin fashion. For more details, see   .

MySQL executes statements using one thread per client connection. When the number of connections increases past a specific point, performance degrades.
This feature introduces a dynamic thread pool, which enables the server to keep the top performance even with a large number of client connections. The server decreases the number of threads using the thread pool and reduces the context switching and hot locks contentions. The thread pool is most effective with `OLTP` workloads (relatively short CPU-bound queries).

Set the thread pool variable [thread_handling](#thread_handling) to `pool-of-threads` by adding the following line to `my.cnf`:

```text
thread_handling=pool-of-threads
```

Although the default values for the thread pool should provide good performance, perform additional tuning with the dynamic system variables. The goal is to minimize the number of open transactions on the server. Short-running transactions commit faster and deallocate server resources and locks.

Due to the following differences, this implementation is not compatible with upstream:

* Built into the server, upstream implements the thread pool as a plugin

* Does not minimize the number of concurrent transactions

Priority Queue:

This is a queue that assigns a priority to each data element and processes them according to their priority. The data element with the highest priority is served first, regardless of its order in the queue. A priority queue can be implemented using an array, a linked list, a heap or a binary search tree. A priority queue can also be ascending or descending, meaning that the highest priority is either the smallest or the largest value.

## Version specific information

Starting with 8.0.14, Percona Server for MySQL uses the upstream implementation of the [`admin_port`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_admin_port). The variables [extra_port](#extra_port) and [extra_max_connections](#extra_max_connections) are removed and not supported. Remove the `extra_port` and `extra_max_connections` variables from your configuration file before upgrading to 8.0.14 or higher. In 8.0.14 or higher, the variables cause a boot error, and the server refuses to start.

Implemented in 8.0.12-1: We ported the `Thread Pool` feature from Percona Server for MySQL 5.7.

## Priority connection scheduling

The thread pool limits the number of concurrently running queries. The number of open transactions may remain high. Connections with already-started transactions are added to the end of the queue. A high number of open transactions has implications for the currently running queries. The [thread_pool_high_prio_tickets](#thread_pool_high_prio_tickets) variable controls the high-priority queue policy and assigns tickets to each new connection.

The thread pool adds the connection to the high-priority queue and decrements the ticket if the connection has the following attributes:

* Has an open transaction

* Has a non-zero number of high-priority tickets

Otherwise, the variable adds the connection to the low-priority queue with the initial value.

The thread pool checks the high-priority queue for the next connection each time. The thread pool picks connections from the low-priority queue when the high-priority queue is empty. The default behavior is to put events from already started transactions into the high-priority queue.

If the value equals `0`, all connections are put into the low-priority queue. Each connection could be put into a high-priority queue if the value exceeds zero.

The [thread_pool_high_prio_mode](#thread_pool_high_prio_mode) variable prioritizes all statements for a connection or assigns connections to the low-priority queue. To implement this new [thread_pool_high_prio_mode](#thread_pool_high_prio_mode) variable


## Low-priority queue throttling

One case that can limit thread pool performance and even lead to deadlocks under high concurrency is when thread groups are oversubscribed due to active threads reaching the oversubscribe limit. Still, all/most worker threads are waiting on locks currently held by a transaction from another connection not currently in the thread pool.

In this case, the oversubscribe limit does not account for those threads in the pool that marked themselves inactive. As a result, the number of threads (both active and waiting) in the pool grows until it hits the [`thread_pool_max_threads`](#thread_pool_max_threads) value. If the connection executing the transaction holding the lock has managed to enter the thread pool by then, we get a large (depending on the [`thread_pool_max_threads`](#thread_pool_max_threads) value) number of concurrently running threads and, thus, suboptimal performance. Otherwise, we get a deadlock as no more threads can be created to process those transaction(s) and release the lock(s).

Such situations are prevented by throttling the low-priority queue when the total number of worker threads (both active and waiting ones) reaches the oversubscribe limit. If there are too many worker threads, do not start new transactions and create new threads until queued events from the already started transactions are processed.

## Handling long network waits

Specific workloads (large result sets, BLOBs, slow clients) can wait longer on network I/O (socket reads and writes). Whenever the server waits, this should be communicated to the thread pool so it can start a new query by either waking a waiting thread or sometimes creating a new one. This implementation has been ported from *MariaDB* patch MDEV-156.



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


This variable defines how the server handles threads for connections from the client.

| Values                    | Description                                            |
|---------------------------|--------------------------------------------------------|
| one-thread-per-connection | One thread handles all requests for a connection       |
| pool-of-threads           | A thread pool handles requests for all connections     |
| no-threads                | A single thread for all connections for debugging mode |

### `thread_pool_idle_timeout`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 60 (seconds)       |

This variable can limit the time an idle thread should wait before exiting.

### `thread_pool_high_prio_mode`

This variable provides more fine-grained control over high-priority scheduling globally or per connection.

The following values are allowed:

* `transactions` (the default). In this mode, only statements from already started transactions may go into the high-priority queue depending on the number of high-priority tickets currently available in a connection (see thread_pool_high_prio_tickets).

* `statements`. In this mode, all individual statements go into the high-priority queue, regardless of the transactional state and the number of available high-priority tickets. Use this value to prioritize `AUTOCOMMIT` transactions or other statements, such as administrative ones. Setting this value globally essentially disables high-priority scheduling. All connections use the high-priority queue.

* `none`. This mode disables the priority queue for a connection. Certain types of connections, for example, monitoring, are insensitive to execution latency and do not allocate the server resources that would impact the performance of other connections. These types of connections do not require high-priority scheduling. Setting this value globally essentially disables high-priority scheduling. All connections use the low-priority queue.

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

### `thread_pool_max_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 100000             |

This variable can limit the maximum number of threads in the pool. The server does not create new threads when the limit is reached.

### `thread_pool_oversubscribe`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | 3                  |

Determines the number of threads run simultaneously. A value lower than `3` could cause sleep and wake-up actions.

### `thread_pool_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default value: | Number of processors   |

Defines the number of threads that can use the CPU simultaneously.

### `thread_pool_stall_limit`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type:     | Numeric            |
| Default value: | 500 (ms)           |

Defines the number of milliseconds before a running thread is considered stalled. The thread pool will wake up or create another thread when this limit is reached. This variable prevents a long-running query from monopolizing the pool.

### Upgrading from a version before 8.0.14 to 8.0.14 or higher



### `extra_port`

The variable was removed in [Percona Server for MySQL 8.0.14](release-notes/Percona-Server-8.0.14.md).

Specifies an additional port that Percona Server for MySQL listens on. This can be used in case no new connections can be established
due to all worker threads being busy or being locked when `pool-of-threads`
feature is enabled.

The following command connects to the extra port:

```shell
mysql --port='extra-port-number' --protocol=tcp
```

### `extra_max_connections`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | Yes                |
| Config file:   | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type:     | Numeric            |
| Default value: | 1                  |

The varible was removed in [Percona Server for MySQL 8.0.14](release-notes/Percona-Server-8.0.14.md). This variable can be used to specify the maximum allowed number of connections
plus one extra `SUPER` users connection on the extra_port. This
can be used with the extra_port variable to access the server in
case no new connections can be established due to all worker threads being busy
or being locked when `pool-of-threads` feature is enabled.

## Status variables

### `Threadpool_idle_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the number of idle threads in the pool.

### `Threadpool_threads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This status variable shows the number of threads in the pool.

## Other reading

* [Thread pool in MariaDB 5.5](https://kb.askmonty.org/en/threadpool-in-55/)

* [Thread pool implementation in Oracle MySQL](https://mikaelronstrom.blogspot.com/2011_10_01_archive.html)
