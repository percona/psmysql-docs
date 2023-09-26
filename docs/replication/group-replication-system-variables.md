# Group replication system variables


| variable name |
|---|
| [`group_replication_auto_evict_timeout`](#group_replication_auto_evict_timeout) |
| [`group_replication_certification_loop_chunk_size`](#group_replication_certification_loop_chunk_size) |
| [`group_replication_certification_loop_sleep_time`](#group_replication_certification_loop_sleep_time) |
| [`group_replication_flow_control_mode`](#group_replication_flow_control_mode) |
| [`group_replication_xcom_ssl_accept_retries`](#group_replication_xcom_ssl_accept_retries) |
| [`group_replication_xcom_ssl_socket_timeout`](#group_replication_xcom_ssl_socket_timeout) |


## group_replication_auto_evict_timeout

The variable is in [tech preview](../glossary.md#tech-preview) mode. Before using the variable in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

| Option | Description |
|---|---|
| Introduced | 8.0.30-22 |
| Command-line |--group-replication-auto-evict-timeout  |
| Dynamic | Yes |
| Scope | Global |
| Type | Integer |
| Default value | 0 |
| Maximum Value | 65535  |
| Unit | seconds |

The value can be changed while Group Replication is running. The change takes effect immediately. Every node in the group can have a different timeout value, but, to avoid unexpected exits, we recommend that all nodes have the same value.

The variable specifies a period of time in seconds before a node is automatically evicted if the node exceeds the [flow control threshold](group-replication-flow-control.md). The default value is 0, which disables the eviction. To set the timeout, change the value with a number higher than zero.

In single-primary mode, the primary server ignores the timeout.

## group_replication_certification_loop_chunk_size

| Option | Description |
|---|---|
| Introduced | 8.0.32-24 |
| Command-line |--group-replication-certification-loop-chunk-size |
| Dynamic | Yes |
| Scope | Global |
| Data type | ulong |
| Default value | 0 |

Defines the size of the chunk that must be processed during the certifier garbage collection phase after which the client transactions are allowed to interleave. The default value is 0.

The minimum value is 0. The maximum value is 4294967295.

## group_replication_certification_loop_sleep_time

| Option | Description |
|---|---|
| Introduced | 8.0.32-24 |
| Command-line |--group-replication-certification-loop-sleep-time |
| Dynamic | Yes |
| Scope | Global |
| Data type | ulong |
| Default value | 0 |

Defines the sleep time in microseconds that the certifier garbage collection loop allows client transactions to interleave. The default value is 0.

The minimum value is 0. The maximum value is 1000000.

## group_replication_flow_control_mode

| Option | Description |
|---|---|
| Introduced | 8.0.32-24 |
| Command-line |--group_replication_flow_control_mode |
| Dynamic | Yes |
| Scope | Global |
| Data type | Enumeration |
| Default value | Quota |
| Valid values | DISABLED <br> QUOTA <br> MAJORITY |

The "MAJORITY" value is in [tech preview](../glossary.md#tech-preview) mode. Before using the variable in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

The variable specifies the mode use for flow control.

*Percona Server for MySQL* 8.0.30-22 adds the "MAJORITY" value to the [group_replication_flow_control_mode](https://dev.mysql.com/doc/refman/8.0/en/group-replication-options.html#sysvar_group_replication_flow_control_mode) variable. In "MAJORITY" mode, [flow control](group-replication-flow-control.md) is activated only if the majority, more than half the number of members, exceed the flow control threshold. The other values are not changed.

## group_replication_xcom_ssl_accept_retries

| Option | Description |
|---|---|
| Introduced | 8.0.34-26 |
| Command-line |--group_replication_xcom_ssl_accept_retries |
| Dynamic | Yes |
| Scope | Global |
| Data type | integer |
| Default value | 10 |

This variable is only effective on `START GROUP_REPLICATION`, and only when group replication is
configured with SSL.

Defines the number of retries before closing the socket. On each retry, the server thread calls SSL_accept(), with a timeout defined by `group_replication_xcom_ssl_socket_timeout`. Used by the SSL handshake process after the connection has been accepted by the first accept() call.

The default value is 10.

## group_replication_xcom_ssl_socket_timeout

| Option | Description |
|---|---|
| Introduced | 8.0.34-26 |
| Command-line |--group_replication_xcom_ssl_socket_timeout |
| Dynamic | Yes |
| Scope | Global |
| Data type | integer |
| Default value | 0 |
| Measured in | seconds |

This variable is only effective on `START GROUP_REPLICATION`, and only when group replication is
configured with SSL.

Defines a file-descriptor level timeout, measured in seconds, for both accept() and SSL_accept() calls when group replication listens on the xcom port.

When set to a valid value, for example, 5 then both accept() and
SSL_accept() return after 5 seconds. 

The default value has been set to 0 (waits infinitely) for backward compatibility.