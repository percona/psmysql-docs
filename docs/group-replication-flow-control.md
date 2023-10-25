# Manage group replication flow control

In replication, flow control prevents one member from falling too far behind the cluster and avoids excessive buffering. A cluster is not required to keep members in sync together for replication. The pending transactions in the relay log only increase for the lagging replica. Each member sends statistics to the group.

Flow control sets a threshold on the queue for transactions waiting in the certification queue or the transactions waiting in the applier queue. If the thresholds are exceeded, and during the duration that they are exceeded, flow control adjusts the writer members to the capacity of the delayed member. This action ensures that all members are in sync.

Flow controls work asynchronously and depend on the following:

* Monitoring the throughput and queue sizes of each member
* Throttling members to avoid writing beyond the capacity available

The following system variables set flow control behavior for Group Replication:

* [group_replication_flow_control_mode]
* [group_replication_flow_control_certifier_threshold]
* [group_replication_flow_control_applier_threshold]

Flow control is enabled and disabled by selecting a value in the group_replication_flow_control_mode variable. Flow control can also be enabled on the certifier or applier level or both and sets the threshold level.

[group_replication_flow_control_mode]: https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_mode
[group_replication_flow_control_certifier_threshold]: https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_certifier_threshold
[group_replication_flow_control_applier_threshold]: https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication-options.html#sysvar_group_replication_flow_control_applier_threshold