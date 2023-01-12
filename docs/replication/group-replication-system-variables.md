# Group replication system variables


| group_replication_auto_evict_timeout |
|---|
| group_replication_flow_control_mode |
|  |

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

## group_replication_flow_control_mode

The "MAJORITY" value is in [tech preview](../glossary.md#tech-preview) mode. Before using the variable in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

| Option | Description |
|---|---|
| Introduced | 8.0.30-22 |
| Command-line |--group_replication_flow_control_mode |
| Dynamic | Yes |
| Scope | Global |
| Data type | Enumeration |
| Default value | Quota |
| Valid values | DISABLED <br> QUOTA <br> MAJORITY |

The variable specifies the mode use for flow control.

*Percona Server for MySQL* 8.0.30-22 adds the "MAJORITY" value to the [group_replication_flow_control_mode](https://dev.mysql.com/doc/refman/8.0/en/group-replication-options.html#sysvar_group_replication_flow_control_mode) variable. In "MAJORITY" mode, [flow control](group-replication-flow-control.md) is activated only if the majority, more than half the number of members, exceed the flow control threshold. The other values are not changed. 