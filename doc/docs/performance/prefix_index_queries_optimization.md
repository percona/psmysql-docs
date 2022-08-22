# Prefix Index Queries Optimization

*Percona Server for MySQL* 5.6 has ported the Prefix Index Queries Optimization feature from the Facebook patch for MySQL.

Prior to this InnoDB would always fetch the clustered index for all prefix
columns in an index, even when the value of a particular record was smaller
than the prefix length. This implementation optimizes that case to use the
record from the secondary index and avoid the extra lookup.

## Status Variables

### `Innodb_secondary_index_triggered_cluster_reads`

Implemented in Percona Server for MySQL 5.7.18-14.

| Option    | Description |
|-----------|-------------|
| Data type | Numeric     |
| Scope     | Global      |

This variable shows the number of times secondary index lookup triggered
cluster lookup.

### `Innodb_secondary_index_triggered_cluster_reads_avoided`

Implemented in Percona Server for MySQL 5.7.18-14.

| Option    | Description |
|-----------|-------------|
| Data type | Numeric     |
| Scope     | Global      |
This variable shows the number of times prefix optimization avoided
triggering cluster lookup.
