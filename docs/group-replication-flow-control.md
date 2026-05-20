# Manage group replication flow control

Group Replication flow control signals the cluster to reduce queue growth on
members that fall behind. Flow control does not prevent members from lagging
behind the group. Flow control does not stop writes when queues remain above
the configured limits.

Each member reports statistics to the group. Flow control compares queue sizes
against thresholds on the certification queue and the applier queue. When a
threshold is exceeded, the group asks writer members to slow down so the
delayed member can reduce its queues toward the limit. If the member cannot
catch up, the cluster continues to run. Flow control never blocks the group
indefinitely.

For a deeper discussion of failover behavior when queues grow, see [The
failover brownout: rethinking high availability in MySQL Group
Replication](https://www.percona.com/blog/the-failover-brownout-rethinking-high-availability-in-mysql-group-replication/).

## How flow control behaves

Flow control runs asynchronously. The group monitors throughput and queue
sizes on each member. When thresholds are exceeded, the group throttles
writers to match the capacity of the slowest member.

The cluster aims to bring the applier queue back under the configured limit.
The cluster does not guarantee that result. Members can remain at different
stages of applied data. Secondary members may and will hold a different view
of applied data than the primary.

## What to expect when members lag

When flow control cannot keep queues under the limit, the following effects
are common:

* The certification buffer grows on the primary and on secondary members.

* After failover, the group elects a new primary but keeps the new primary in
  read-only mode until the applier queue is processed.

* Pending transactions accumulate in the relay log on lagging members.

Plan capacity, monitoring, and failover testing with these limits in mind.
Do not treat flow control as a substitute for right-sized hardware, parallel
apply tuning, or application design.

## Tune parallel apply with flow control

Flow control works with the replication applier. The
[`replica_parallel_workers`](https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-replica.html#sysvar_replica_parallel_workers)
variable controls how many applier threads process the relay log.

Set `replica_parallel_workers` to approximately 2.5 times the number of CPU
cores on the member. For example, a host with 8 cores can use
`replica_parallel_workers = 20`. Parallel apply helps the member drain the
applier queue more efficiently. The setting does not guarantee that flow
control prevents lag.

Review workload patterns, commit ordering requirements, and any known
limitations before raising `replica_parallel_workers` in production.

## Configure flow control variables

The following system variables control flow control behavior for Group
Replication:

* [group_replication_flow_control_mode :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_mode)

* [group_replication_flow_control_certifier_threshold :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_certifier_threshold)

* [group_replication_flow_control_applier_threshold :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_applier_threshold)

Enable or disable flow control with
`group_replication_flow_control_mode`. You can apply thresholds on the
certifier queue, the applier queue, or both. Percona Server for MySQL also
adds a `MAJORITY` mode. For details, see [Group replication system
variables](group-replication-system-variables.md).
