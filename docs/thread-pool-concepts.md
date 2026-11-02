# Thread pool concepts

Percona Server for MySQL version 9.7.2-2 includes two thread pool implementations:

* Built-in Percona thread pool. See [Thread pool](threadpool.md).

* `thread_pool` plugin from Oracle. See [MySQL thread pool plugin](mysql-thread-pool.md).

Both implementations resolve connection performance issues in the same manner.

## Why use a thread pool

By default, the MySQL server creates one thread for each client connection. The `one-thread-per-connection` model handles every statement on a client connection until the connection closes. This model works well for a moderate number of connections.

High connection numbers make the `one-thread-per-connection` model inefficient. Many active threads increase context switches and lock contention. Database performance decreases as context switches increase.

A thread pool reuses a fixed set of worker threads across multiple connections. This architecture provides the following benefits:

* Reduces overhead from thread creation and thread destruction

* Prevents high context switches

* Reduces lock contention

A thread pool is most effective for Online Transaction Processing (OLTP) workloads with short, CPU-bound queries. With fewer than 20,000 connections, a thread pool provides limited performance benefit. The `one-thread-per-connection` model often performs better with low connection counts.

## Thread groups and round-robin assignment

A thread pool organizes worker threads into thread groups. Each thread group manages a subset of client connections with a limited number of worker threads.

When a client opens a connection, the thread pool assigns the connection to a thread group. The thread pool uses round-robin assignment to distribute connections in order:

* The first connection assigns to group one

* The second connection assigns to group two

* The third connection assigns to group three

* The fourth connection assigns to group four

* The fifth connection assigns to group one

Round-robin assignment spreads connections evenly across all thread groups. This distribution prevents group overload and balances pool performance.

Each thread group includes one listener thread. The listener thread monitors statements from connections assigned to that thread group. The listener thread sends statements to an available worker thread. If no worker thread is free, the listener thread queues the statement.

## Priority queues

Each thread group maintains two queues:

* High-priority queue

* Normal-priority queue

The first statement of a transaction enters the normal-priority queue. Subsequent statements from an open transaction enter the high-priority queue. A thread group processes all items in the high-priority queue before processing items in the normal-priority queue.

Open transactions hold database locks and server resources. Fast execution of open transactions releases resources and reduces lock contention.

System variables control priority queue configuration. Administrators can configure the following options:

* The number of statements a connection sends to the high-priority queue

* The priority rule based on transaction state or statement type

Consult the system variable documentation for implementation details.