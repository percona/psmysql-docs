# Manage group replication flow control

Flow control prevents one member from falling too far behind the cluster. This mechanism avoids excessive buffering in the relay log. Each member sends statistics to the group to coordinate throughput.

Flow control monitors two queues:

* Transactions waiting in the certification queue

* Transactions waiting in the applier queue

When transactions exceed the configured thresholds, flow control throttles writer members. This throttling matches writer throughput to the capacity of the slowest member.

Flow control operates asynchronously and depends on the following:

* Monitoring the throughput and queue sizes of each member

* Throttling members to prevent writes beyond available capacity

## System variables

The following system variables configure flow control behavior for Group Replication:

* [`group_replication_flow_control_mode`](#group_replication_flow_control_mode)

* [`group_replication_flow_control_certifier_threshold`](#group_replication_flow_control_certifier_threshold)

* [`group_replication_flow_control_applier_threshold`](#group_replication_flow_control_applier_threshold)

### `group_replication_flow_control_mode`

Specifies the mode used for flow control.

| Option | Description |
|--------|-------------|
| Command-line | `--group-replication-flow-control-mode` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Enumeration |
| Default | `QUOTA` |

The following values are valid:

* `DISABLED` - Flow control is off

* `QUOTA` - Flow control uses a quota-based throttling mechanism

* `MAJORITY` - Flow control triggers when a majority of members exceed the threshold

```sql
-- Disable flow control
SET GLOBAL group_replication_flow_control_mode = 'DISABLED';

-- Enable quota-based flow control
SET GLOBAL group_replication_flow_control_mode = 'QUOTA';

-- Enable majority-based flow control
SET GLOBAL group_replication_flow_control_mode = 'MAJORITY';
```

### `group_replication_flow_control_certifier_threshold`

Specifies the number of waiting transactions in the certifier queue that trigger flow control.

| Option | Description |
|--------|-------------|
| Command-line | `--group-replication-flow-control-certifier-threshold` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Integer |
| Default | `25000` |
| Range | `0` to `2147483647` |

The default value of 25000 suits most workloads. Tune this value based on your hardware, workload, and latency requirements:

* Lower values trigger flow control sooner, protecting slow secondaries at the cost of primary throughput

* Higher values allow more lag before throttling, improving throughput but risking secondaries falling behind

Setting this variable to the maximum value effectively disables threshold-based triggering for this queue. This configuration risks memory exhaustion on slower members and extended failover times. Setting the value to `0` triggers flow control immediately when any transaction waits in the queue.

```sql
-- Set certifier threshold to 10000 transactions
SET GLOBAL group_replication_flow_control_certifier_threshold = 10000;
```

### `group_replication_flow_control_applier_threshold`

Specifies the number of waiting transactions in the applier queue that trigger flow control.

| Option | Description |
|--------|-------------|
| Command-line | `--group-replication-flow-control-applier-threshold` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Integer |
| Default | `25000` |
| Range | `0` to `2147483647` |

The default value of 25000 suits most workloads. Tune this value based on your hardware, workload, and latency requirements:

* Lower values trigger flow control sooner, protecting slow secondaries at the cost of primary throughput

* Higher values allow more lag before throttling, improving throughput but risking secondaries falling behind

Setting this variable to the maximum value effectively disables threshold-based triggering for this queue. This configuration risks memory exhaustion on slower members and extended failover times. Setting the value to `0` triggers flow control immediately when any transaction waits in the queue.

```sql
-- Set applier threshold to 10000 transactions
SET GLOBAL group_replication_flow_control_applier_threshold = 10000;
```

Flow control triggers when either threshold is exceeded on any member.

## Status variables

Status variables are read-only and cannot be changed at runtime. These variables report the state of flow control on each member.

* `group_replication_flow_control_active` - Reports whether flow control is throttling transactions. Returns `ACTIVE` when engaged or `DISABLED` when not throttling.

* `group_replication_flow_control_threshold_nodes` - Lists members that trigger flow control. The format is `(count/total)` followed by a comma-separated list of member IDs.

* `group_replication_flow_control_throttle_quota` - Reports the maximum transactions allowed per flow control period.

### Query flow control status

The following query displays flow control status variables when throttling is active:

```sql
mysql> SHOW GLOBAL STATUS LIKE '%flow_control%';
+-----------------------------------------------+------------------------------------------+
| Variable_name                                 | Value                                    |
+-----------------------------------------------+------------------------------------------+
| group_replication_flow_control_active         | ACTIVE                                   |
| group_replication_flow_control_threshold_nodes| (2/3)node1:33061,node2:33061             |
| group_replication_flow_control_throttle_quota | 5000                                     |
+-----------------------------------------------+------------------------------------------+
```

The following output shows the status variables when flow control is not engaged:

```sql
mysql> SHOW GLOBAL STATUS LIKE '%flow_control%';
+-----------------------------------------------+------------------------------------------+
| Variable_name                                 | Value                                    |
+-----------------------------------------------+------------------------------------------+
| group_replication_flow_control_active         | DISABLED                                 |
| group_replication_flow_control_threshold_nodes| (0/3)                                    |
| group_replication_flow_control_throttle_quota | 0                                        |
+-----------------------------------------------+------------------------------------------+
```

## Related topics

* [Group Replication system variables](group-replication-system-variables.md)

* [Binary logs and replication improvements](binlogging-replication-improvements.md)

* [Percona Server for MySQL feature comparison](feature-comparison.md)
