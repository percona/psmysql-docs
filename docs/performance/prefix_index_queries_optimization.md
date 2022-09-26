# Prefix Index Queries Optimization

*Percona Server for MySQL* has ported Prefix Index Queries Optimization feature from
Facebook patch for *MySQL*.

Prior to this *InnoDB* would always fetch the clustered index for all prefix
columns in an index, even when the value of a particular record was smaller
than the prefix length. This implementation optimizes that case to use the
record from the secondary index and avoid the extra lookup.

## Status Variables

### `Innodb_secondary_index_triggered_cluster_reads`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This variable shows the number of times secondary index lookup triggered
cluster lookup.

### `Innodb_secondary_index_triggered_cluster_reads_avoided`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This variable shows the number of times prefix optimization avoided
triggering cluster lookup.

## Version Specific Information

* 8.0.12-1: The feature was ported from *Percona Server for MySQL* 5.7
