# Manage Group Replication flow control

Flow control does not prevent members from falling behind. Flow control signals the group to reduce the applier queue toward the configured threshold.

Each member reports queue size and throughput to the group. Flow control monitors two queues:

* Transactions in the certification queue

* Transactions in the applier queue

A queue that exceeds its threshold lowers the transaction quota for writer members. The group then tries to reduce that queue to the limit.

Members may fail to apply transactions at the reduced rate. The queue then continues to grow. Group Replication continues to run. Flow control does not stop the cluster when a queue stays above the threshold.

A secondary can have a different applied data set than the primary. This difference is expected. Reads from a lagging secondary can return older data.

Flow control does not wait for members to catch up. Flow control uses the following data:

* Throughput for each member

* Queue size for each member

Writer members then receive a lower transaction quota.

## System variables

The following system variables configure flow control in Group Replication:

* [`group_replication_flow_control_mode`](#group_replication_flow_control_mode)

* [`group_replication_flow_control_certifier_threshold`](#group_replication_flow_control_certifier_threshold)

* [`group_replication_flow_control_applier_threshold`](#group_replication_flow_control_applier_threshold)

The [`replica_parallel_workers`](#configure-replication-applier-workers) variable is a related applier setting. This variable can reduce queue growth. This variable does not change flow control behavior.

### `group_replication_flow_control_mode`

Specifies the flow control mode.

| Option | Description |
|--------|-------------|
| Command-line | `--group-replication-flow-control-mode` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Enumeration |
| Default | `QUOTA` |

The following values are valid:

* `DISABLED` - Flow control is off

* `QUOTA` - Flow control uses a quota to limit writers

* `MAJORITY` - Flow control starts when a majority of members exceed the threshold

`MAJORITY` is a [tech preview](glossary.md#tech-preview) feature.

```sql
-- Disable flow control
SET GLOBAL group_replication_flow_control_mode = 'DISABLED';

-- Enable quota-based flow control
SET GLOBAL group_replication_flow_control_mode = 'QUOTA';

-- Enable majority-based flow control
SET GLOBAL group_replication_flow_control_mode = 'MAJORITY';
```

### `group_replication_flow_control_certifier_threshold`

Specifies how many transactions in the certifier queue start flow control.

| Option | Description |
|--------|-------------|
| Command-line | `--group-replication-flow-control-certifier-threshold` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Integer |
| Default | `25000` |
| Range | `0` to `2147483647` |

No single value suits every workload. Start with the default. Monitor the certification queue during peak traffic.

A lower value starts quota reduction sooner. Write throughput can decrease.

A higher value delays quota reduction. The certification queue can grow larger.

The maximum value is `2147483647`. Flow control for the certifier queue starts only at that size. The applier threshold can still start flow control.

A large certifier queue increases certification memory on every member. The value `0` starts flow control when the queue has one transaction.

```sql
-- Set certifier threshold to 10000 transactions
SET GLOBAL group_replication_flow_control_certifier_threshold = 10000;
```

### `group_replication_flow_control_applier_threshold`

Specifies how many transactions in the applier queue start flow control.

| Option | Description |
|--------|-------------|
| Command-line | `--group-replication-flow-control-applier-threshold` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Integer |
| Default | `25000` |
| Range | `0` to `2147483647` |

No single value suits every workload. Start with the default. Monitor the applier queue during peak traffic.

A lower value starts quota reduction sooner. Write throughput can decrease.

A higher value delays quota reduction. The applier queue can grow larger.

The maximum value is `2147483647`. Flow control for the applier queue starts only at that size. The certifier threshold can still start flow control.

A large applier queue delays writes after failover. The value `0` starts flow control when the queue has one transaction.

```sql
-- Set applier threshold to 10000 transactions
SET GLOBAL group_replication_flow_control_applier_threshold = 10000;
```

In `QUOTA` mode, either threshold can start flow control on any member.

In `MAJORITY` mode, more than half of the members must exceed a threshold.

## Understand the operational effects

A queue that exceeds a threshold requests a quota reduction. The threshold does not cap the queue. Flow control does not stop Group Replication.

If the reduced quota does not reduce the queue, the following effects occur:

* The applier queue grows on a secondary.

* Secondaries hold a different applied data set than the primary.

* The certification buffer grows on the primary and on secondaries.

* Members keep `certification_info` for a longer time.

* The group low watermark advances more slowly.

The group elects a new primary during failover. The new primary stays read-only until that member applies the remaining queue.

The wait causes a write brownout. The brownout lasts until the new primary applies the backlog.

Resource exhaustion can stop a member. A flow control threshold does not stop a member.

## Configure replication applier workers

The `replica_parallel_workers` variable sets the number of parallel applier workers. More workers can process the applier queue faster. More workers do not keep members at the same applied position. Flow control still does not prevent lag.

| Option | Description |
|--------|-------------|
| Command-line | `--replica-parallel-workers` |
| Dynamic | Yes |
| Scope | Global |
| Data type | Integer |
| Default | `4` |
| Range | `0` to `1024` |

Start with `replica_parallel_workers = CPU_CORES * 2.5`. `CPU_CORES` is the CPU core count on the member. Round the result to a whole number.

The following limits still apply to parallel apply:

* Transaction dependencies

* Storage latency

* CPU capacity

Too many workers can increase scheduling overhead. Too many workers can increase CPU contention. Test the value with your workload and applier metrics.

Restart Group Replication on that member after you change the value. The applier then uses the updated worker count.

```sql
-- Example for 8 CPU cores * 2.5
SET GLOBAL replica_parallel_workers = 20;
```

## Status variables

Status variables are read-only at runtime. These variables report flow control state on each member.

* `group_replication_flow_control_active` - `ACTIVE` when flow control limits writers, or `DISABLED` otherwise

* `group_replication_flow_control_threshold_nodes` - Members that start flow control, in `(count/total)` format plus member IDs

* `group_replication_flow_control_throttle_quota` - Maximum transactions per flow control period

### Query flow control status

The following query shows status when flow control is active:

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

The following output shows status when flow control is idle:

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

* [The Failover Brownout: Rethinking High Availability in MySQL Group Replication](https://www.percona.com/blog/the-failover-brownout-rethinking-high-availability-in-mysql-group-replication/)
