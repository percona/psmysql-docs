# Thread pool

## Introduction

Thread pooling improves performance and scalability for MySQL-compatible databases by
reusing a fixed number of pre-created threads to manage multiple client
sessions. This design reduces resource overhead, lowers contention, and avoids
context-switching bottlenecks during high concurrency.

The default MySQL method creates one thread per client connection. This approach
works efficiently under moderate connection loads. However, as the number of active
connections increases, especially beyond 20,000, system overhead becomes
significant, and throughput decreases.

Percona Server for MySQL includes an integrated thread pool that replaces the
default model. The thread pool manages connections more efficiently by queuing
work and reusing threads, especially in OLTP environments with many short-lived
queries.

## Version-specific notes

Thread pool support in Percona Server for MySQL evolved across releases. Review
the following version details to avoid configuration errors and ensure
compatibility.

  
### 8.0.14

Beginning with 8.0.14, the upstream implementation of `admin_port` replaced the
previous mechanism that used `extra_port` and `extra_max_connections`.
 
Removed:

* These options are removed:`extra_port` and `extra_max_connections`. They are no longer recognized and cause server startup failure.
 
Migration steps:

* Remove all references to `extra_port` and `extra_max_connections` from the
  configuration file before upgrading to 8.0.14 or later.

* Use the `admin_port` variable to configure administrative access if needed.

  
### 8.0.12-1

Percona Server for MySQL 8.0.12-1 introduced native support for the thread pool.
This version ported the feature from Percona Server 5.7.

## Core concepts and usage examples

### Fixed pool of threads

The server initializes a specified number of threads during the startup process and maintains these active threads to handle incoming queries efficiently. The server minimizes the overhead associated with creating and destroying threads for each query by reusing threads, enhancing overall performance and responsiveness.

The following configuration setting activates the thread pool model:

```ini
[mysqld]
thread_handling = pool-of-threads
```

In this model, the server allocates threads from the pool to process queries as they arrive, allowing for better resource management and improved throughput, particularly in environments with high query loads. This approach ensures that available threads are quickly assigned to incoming requests, enabling timely query processing while optimizing system resources.

### How the thread pool works

When a client connects, the server assigns the connection to a thread group using a round-robin method. Each group consists of a listener thread and multiple worker threads. The listener thread monitors active connections and queues incoming statements for processing.

The server assigns new connections to thread groups using a round-robin method. This approach balances workload evenly and prevents any group from becoming a bottleneck.

Connection 1 goes to Group 1

Connection 2 goes to Group 2

Connection 3 goes to Group 3

Connection 4 goes to Group 4

Connection 5 returns to Group 1

New queries are routed to either the high-priority queue or the low-priority queue. A query enters the high-priority queue if the connection has an open transaction and there are available high-priority tickets, which allow certain queries to be processed more quickly, ensuring that critical operations receive immediate attention. All other queries are directed to the low-priority queue.

Worker threads first scan the high-priority queue for queries to process. Once all high-priority queries have been handled, the threads process queries from the low-priority queue. After completing a query, a worker thread becomes idle and waits for the next task, helping to avoid excessive thread creation and maintaining steady performance under load.

The thread pool adapts to shifts in workload by redistributing queued tasks and prioritizing available threads. This dynamic management improves system responsiveness while minimizing the number of threads in use.

<img src="../_static/thread-pool-diagram.png" alt="Thread pool diagram" width="250" />

### Thread groups

The thread pool organizes threads into distinct groups to manage client connections efficiently. Each group consists of a listener thread and multiple worker threads. The listener thread monitors incoming client connections and queuing requests for processing. Meanwhile, the worker threads handle the actual processing of these requests, allowing for concurrent execution of tasks.

```ini
[mysqld]
thread_pool_size = 8
```

This configuration spreads work across eight thread groups.

### Priority queues

Each thread group maintains both a high-priority and low-priority queue to manage incoming queries effectively. When a new query arrives, the system determines its placement in one of the two queues based on the availability of high-priority tickets and the state of the transaction. The thread pool prioritizes processing by constantly checking the high-priority queue first, ensuring that critical queries receive immediate attention before any lower-priority queries are addressed. This approach optimizes resource allocation and enhances overall system responsiveness.


### High-priority ticketing

Each connection begins with a set number of high-priority tickets that allow for the prioritization of a limited number of queries. Every time the thread pool promotes a query to the high-priority queue, one ticket is used. When queries are submitted to the server, each query is assigned a "ticket" indicating its priority level, which the thread pool uses to determine the processing order.

Here’s how the ticket system works in more detail:

| Feature               | Description                                                                                                                                                                                                                     |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ticket Assignment      | When a query is submitted, it is evaluated based on its priority. High-priority queries receive a special ticket that allows them to be processed ahead of lower-priority queries. This assignment ensures that critical tasks are addressed promptly. |
| Queue Management       | The thread pool maintains separate queues for high-priority and low-priority queries. High-priority queries are placed in a queue that is processed first, while lower-priority queries wait in a separate queue. This separation helps manage resources effectively and ensures that important tasks do not get delayed. |
| Resource Allocation    | The thread pool allocates resources based on the tickets. When a thread becomes available, it checks the high-priority queue first. If there are high-priority queries waiting, those queries are executed before any from the lower-priority queue. This approach maximizes the responsiveness of the system for critical operations. |
| Dynamic Adjustment     | The ticket system allows for dynamic adjustments based on the current workload. If the number of high-priority queries increases, the system can adapt by allocating more resources to handle them efficiently, ensuring that performance remains optimal even during peak times. |

## Configure thread pool

For example, this configuration setting in the server's configuration file, `my.cnf`, specifies that each new connection receives five high-priority tickets. These tickets allow up to five queries to be processed before lower-priority ones.

```ini
[mysqld]
thread_pool_high_prio_tickets = 5
```

By executing this command in the client, users enable the server to prioritize up to five queries for processing ahead of lower-priority queries. This setting is beneficial in environments where certain operations require immediate attention. The change applies globally, affecting all new connections established after the command is executed.

```mysql
mysql> mysql> SET GLOBAL thread_pool_high_prio_tickets = 5;
```

Either of these configurations assigns five tickets to each new connection.


### High-priority modes

The [`thread_pool_high_prio_mode`](#thread_pool_high_prio_mode) setting is an option that manages how queries are scheduled in the thread pool using a ticket system. 

When this setting is turned on, the system prioritizes high-priority queries. Adjusting this setting can improve the performance of your applications, especially during busy times.

### Configuration and monitoring

Administrators can fine-tune thread pool behavior by adjusting dynamic and static variables.


```ini
[mysqld]
thread_pool_stall_limit = 100
```

```mysql
mysql> SET GLOBAL thread_pool_stall_limit = 100;
```

This value, in milliseconds, limits how long a task can stall before being redistributed. As with other thread pool settings, existing sessions retain their previous values.


## Thread Pool Configuration Reference Sheet

A quick overview of system variables available for configuring the thread pool in Percona Server for MySQL.

<h2>General Variables</h2>
<table>
  <thead>
    <tr>
      <th style="width: 280px;">Variable name</th>
      <th>Default</th>
      <th>Scope</th>
      <th>Dynamic</th>
      <th>Config file</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code><a href="#thread_handling">thread_handling</a></code></td>
      <td><code>one-thread-per-connection</code></td>
      <td>Global</td>
      <td>No</td>
      <td>Yes</td>
      <td>Chooses the thread model. Use <code>pool-of-threads</code> to enable thread pooling.</td>
    </tr>
    <tr>
      <td><code><a href="#thread_pool_size">thread_pool_size</a></code></td>
      <td><code>16</code></td>
      <td>Global</td>
      <td>No</td>
      <td>Yes</td>
      <td>Defines the number of thread groups.</td>
    </tr>
    <tr>
        <td><a href="#thread_pool_oversubscribe"><code>thread_pool_oversubscribe</code></a></td>
        <td><code>3</code></td>
        <td>Global</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Defines per-group queue saturation threshold.</td>
    </tr>
  </tbody>
</table>

<h2>Priority Handling</h2>
<table>
  <thead>
    <tr>
      <th style="width: 280px;">Variable name</th>
      <th>Default</th>
      <th>Scope</th>
      <th>Dynamic</th>
      <th>Config file</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code><a href="#thread_pool_high_prio_tickets">thread_pool_high_prio_tickets</a></code></td>
      <td><code>4294967295</code></td>
      <td>Global</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Maximum high-priority executions allowed per connection.</td>
    </tr>
    <tr>
        <td><code><a href="#thead_pool_high_prio_mode">thread_pool_high_prio_mode</a></code></td>
      <td><code>transactions</code></td>
      <td>Global</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Determines which queries receive high priority.</td>
    </tr>
  </tbody>
</table>

<h2>Thread Management</h2>
<table>
  <thead>
    <tr>
      <th style="width: 280px;">Variable name</th>
      <th>Default</th>
      <th>Scope</th>
      <th>Dynamic</th>
      <th>Config file</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td><code><a href="#thread_pool_max_threads">thread_pool_max_threads</a></code></td>
      <td><code>1000</code></td>
      <td>Global</td>
      <td>No</td>
      <td>Yes</td>
      <td>Maximum number of worker threads per group.</td>
    </tr>
    <tr>
        <td><code><a href="#thread_pool_stall_limit">thread_pool_stall_limit</a></code></td>
      <td><code>6</code></td>
      <td>Global</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Wait time in milliseconds before reassigning stalled queries.</td>
    </tr>
    <tr>
        <td><a href="#thread_pool_idle_timeout"><code>thread_pool_idle_timeout</code></a></td>
        <td><code>60</code></td>
        <td>Global</td>
        <td>Yes</td>
        <td>Yes</td>
        <td>Seconds before idle threads above min are released.</td>
    </tr>
  </tbody>
</table>

<h2 id="extra-port-behavior">Extra Port Behavior</h2>
<details>
  <summary><strong>Deprecated variables (click to expand)</strong></summary>
  <table>
    <thead>
      <tr>
        <th style="width: 280px;">Variable name</th>
        <th>Default</th>
        <th>Scope</th>
        <th>Dynamic</th>
        <th>Config file</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><a href="#extra_port"><code>extra_port</code></a></td>
        <td><code>0</code></td>
        <td>Global</td>
        <td>No</td>
        <td>Yes</td>
        <td>Legacy variable replaced by <code>admin_port</code>.</td>
      </tr>
      <tr>
        <td><a href="#extra_max_connections"><code>extra_max_connections</code></a></td>
        <td><code>1</code></td>
        <td>Global</td>
        <td>No</td>
        <td>Yes</td>
        <td>Legacy limit for <code>extra_port</code> access.</td>
      </tr>
    </tbody>
  </table>
</details>

<h2 id="status-metrics-read-only">Status Metrics (Read-Only)</h2>
<table>
  <thead>
    <tr>
      <th style="width: 280px;">Variable name</th>
      <th>Scope</th>
      <th>Dynamic</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="#threadpool_threads"><code>threadpool_threads</code></a></td>
      <td>Session</td>
      <td>N/A</td>
      <td>Total worker threads across all groups.</td>
    </tr>
    <tr>
      <td><a href="#thread_pool_idle_threads"><code>thread_pool_idle_threads</code></a></td>
      <td>Session</td>
      <td>N/A</td>
      <td>Idle worker threads available for reuse.</td>
    </tr>
  </tbody>
</table>

### Observability Commands

Use these statements to inspect runtime thread pool behavior:

```mysql
mysql> SHOW STATUS LIKE 'Threadpool%';
```

These commands reveal thread activity, idle counts, and queue saturation by group.


Note: For dynamic variables, changes apply only to new connections. Existing sessions retain their original settings until reconnect.

## Configuration reference

This section consolidates key thread pool variables, their behavior, and how to
configure them both statically and dynamically.


### `thread_handling`

Controls which thread management model the server uses.

* Allowed values: `one-thread-per-connection`, `pool-of-threads`

* Description: Use `pool-of-threads` to enable the thread pool. This setting must
  be configured in `my.cnf` before server startup.

* Default: `one-thread-per-connection`

* This value is not dynamic and requires a server restart.


### `thread_pool_size`

Defines the number of thread groups.

* Allowed values: Any positive integer (commonly 2 to 64)

* Description: Each group manages client connections with its own listener and
  worker threads.

* Default: 16

* This value is static and requires a server restart.



### `thread_pool_high_prio_tickets`

Limits the number of high-priority queries per connection.

* Allowed values: 0 to 4294967295

* Description: Each time a connection uses high-priority scheduling, one ticket is
  consumed.

* Default: 4294967295

* This setting can be configured statically.

* This setting can be configured dynamically.

* This change applies only to new client connections.



### `thread_pool_high_prio_mode`

Controls which queries qualify for high-priority scheduling.

* Allowed values: `transactions`, `statements`, `none`

* Description: Use `transactions` to prioritize active transactions, or `statements`
  to prioritize all statements from ticketed connections.

* Default: `transactions`

* This setting can be configured statically.

* This setting can be configured dynamically.

* This change affects new sessions only. Existing sessions retain the previous mode
  until reconnect.


### `thread_pool_stall_limit`

Controls how long to wait before rescheduling stalled queries.

* Allowed values: Integer ≥ 1 (milliseconds)

* Description: If a query remains blocked beyond this time, the pool may redistribute
  it to another group.

* Default: 6

* This setting can be configured statically.

* This setting can be configured dynamically.

* This setting helps improve query responsiveness under unbalanced workloads.


### `thread_pool_min_threads`

Defines the minimum number of worker threads per group.

* Allowed values: Integer ≥ 1

* Description: Sets a floor for thread availability within each group.

* Default: 4

* This value is not dynamic.



### `thread_pool_max_threads`

Defines the maximum number of worker threads per group.

* Allowed values: Integer ≥ `thread_pool_min_threads`

* Description: Controls the upper bound on thread creation. If reached, new queries wait
  in the queue.

* Default: 1000

* This setting is not dynamic and requires a server restart.



Use these variables together to tune concurrency, queue behavior, and scheduling
control based on your workload and connection volume.


