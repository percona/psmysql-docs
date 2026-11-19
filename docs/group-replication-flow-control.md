# Manage group replication flow control

In replication, flow control does not prevent a member from falling behind the cluster. Flow control indicates to the cluster to try to reduce the applier queue. The cluster tries to reduce the applier queue to the applier threshold. If the cluster cannot reduce the queue to that threshold, the cluster continues to run. Flow control does not stop the cluster. A secondary may have a different applied data state than the primary. A secondary will have a different applied data state while transactions remain in its applier queue. Each member sends statistics to the group.

When a secondary lags, the certification buffer increases on the primary and on the secondary. On failover, the cluster elects a new primary and keeps that primary read-only (super_read_only = ON) until the applier queue is processed.

Flow control sets a threshold on the queue for transactions waiting in the certification queue or the transactions waiting in the applier queue. If the thresholds are exceeded, and during the duration that they are exceeded, flow control adjusts the writer members to the capacity of the delayed member. This adjustment does not ensure that all members are in sync.

Flow controls work asynchronously and depend on the following:

* Monitoring the throughput and queue sizes of each member
* Throttling writer members to try to reduce the applier queue

The following system variables set flow control behavior for Group Replication:

* [group_replication_flow_control_mode :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_mode)
* [group_replication_flow_control_certifier_threshold :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-system-variables.html#sysvar_group_replication_flow_control_certifier_threshold)
* [group_replication_flow_control_applier_threshold :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_applier_threshold)

Set [replica_parallel_workers :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-replica.html#sysvar_replica_parallel_workers) to the number of CPU cores multiplied by 2.5 (replica_parallel_workers = cores * 2.5). This setting helps the applier manage the queue. This setting does not guarantee that flow control prevents a member from lagging behind.

Flow control is enabled and disabled by selecting a value in the group_replication_flow_control_mode variable. Flow control can also be enabled on the certifier or applier level or both and sets the threshold level.
