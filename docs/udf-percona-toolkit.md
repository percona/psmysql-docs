
# Percona Toolkit UDFs

The Percona Toolkit component adds user-defined functions (UDFs) that provide fast 64-bit hashing. These UDFs are primarily about speed and data integrity. They are implemented in C++ to perform the hashing operations much faster than standard SQL or stored procedures. With datasets often in the multi-terabyte range, they address several critical scenarios.

!!! note "Prerequisites"

    Before using these functions, add the Percona Repository and install the component.

## Why use these functions

| Use case | Context | Benefit |
|----------|---------|---------|
| High-speed data checksums (pt-table-checksum) | `pt-table-checksum` must hash every row to verify replicas. MySQL's built-in `MD5()` or `SHA1()` is CPU-intensive and slow for billions of rows. | When you install `fnv_64` or `murmur_hash`, the checksum process becomes significantly faster; `pt-table-checksum` can finish in hours instead of days. |
| Efficient data sharding and partitioning | When you shard data across multiple servers, you need a consistent way to map a key (for example, a user ID) to a specific shard. A common pattern is `murmur_hash(user_id) % 10` to distribute data across 10 shards. | MurmurHash has a low collision rate and uniform distribution, so shards stay balanced and one server does not become a hotspot. |
| Change Data Capture (CDC) and auditing | When you sync data to an external warehouse (for example, Snowflake or BigQuery) without a full binary log parser, you can store a hash of each row in a `row_hash` column and recompute on the next sync to detect changed rows. | `fnv_64` is very lightweight, so you can run this in an `INSERT` or `UPDATE` trigger with negligible impact on transaction latency. |
| Fast lookups for large string columns | For tables with very long strings (for example, URLs or JSON) that you need to index or check for uniqueness, indexing the full string is inefficient. | Index `fnv_64(string)` instead; you get a 64-bit integer index that is smaller, uses the buffer pool efficiently, and supports fast equality lookups. |

## Functions provided

The component registers these functions (one load registers all of them):

| Function       | Description |
|----------------|-------------|
| `fnv_64()`     | 64-bit FNV hash. Simple, fast. |
| `fnv1a_64()`   | 64-bit FNV-1a variant. Often better distribution than FNV on sequential input. |
| `murmur_hash()`| 64-bit MurmurHash. Strong avalanche; good for fewer collisions on diverse data. |

Each function takes a string or numeric value and returns an unsigned 64-bit integer.

## Technical comparison: FNV vs Murmur

| Aspect | `fnv_64` / `fnv1a_64` | `murmur_hash()` |
|--------|------------------------|-----------------|
| Speed | Very fast; minimal operations per byte. | Very fast; often comparable or slightly better on long strings. |
| Collision behavior | Good for general use. FNV can cluster more on sequential or similar inputs; FNV-1a usually improves that. | Better distribution and avalanche (small input change → large output change). Prefer for large datasets or when collision rate matters. |
| When to use | General-purpose hashing, simple checksums, shard keys when collision risk is low. | Distributed systems, large tables, or when you need the lowest practical collision rate. |

Benchmark with your own data and workload when you choose; performance depends on key length, data patterns, and hardware.

## Installation

The UDFs are shipped as a MySQL component (not as separate plugin files). After you install the Percona Server package, load the component. Full repository and package steps are in [Install Percona Toolkit UDFs (Optional)](apt-repo.md#install-percona-toolkit-udfs-optional). Then run:

```sql
INSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"
	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

## Examples

Hash a single value (for example, for a lookup key or checksum):

```sql
SELECT fnv_64('test_string');
SELECT murmur_hash(12345);
```

??? example "Expected output"
	```{.text .no-copy}
	+----------------------+
	| fnv_64('test_string') |
	+----------------------+
	|   13528473474361592478 |
	+----------------------+

	+-------------------+
	| murmur_hash(12345) |
	+-------------------+
	|  12345678901234567 |
	+-------------------+
	```

Use in queries—for example, to derive a shard or partition key from `user_id`:

```sql
SELECT user_id, murmur_hash(user_id) AS shard_key FROM users;
```

??? example "Expected output"
	```{.text .no-copy}
	+---------+-------------------+
	| user_id | shard_key         |
	+---------+-------------------+
	|       1 | 12345678901234567 |
	|       2 | 98765432109876543 |
	|       3 | 55555555555555555 |
	+---------+-------------------+
	```

Checksum a column to compare two tables (same expression on both sides gives the same result when data matches):

```sql
SELECT SUM(murmur_hash(col1)) AS checksum FROM replica_db.my_table;
-- Compare with the same expression on the source table.
```

??? example "Expected output"
	```{.text .no-copy}
	+---------------------+
	| checksum            |
	+---------------------+
	| 1234567890123456789 |
	+---------------------+
	```

Use in `WHERE` or joins when you need a stable numeric fingerprint:

```sql
SELECT * FROM events WHERE murmur_hash(device_id) MOD 10 = 0;
```

??? example "Expected output"
	```{.text .no-copy}
	+----+-----------+---------------------+
	| id | device_id | created_at          |
	+----+-----------+---------------------+
	|  2 | dev_abc   | 2024-01-15 10:30:00 |
	|  5 | dev_xyz   | 2024-01-15 11:00:00 |
	+----+-----------+---------------------+
	```

## Maintenance

### Verify the component is loaded

Check that the component is registered:

```sql
SELECT * FROM mysql.component WHERE component_urn = 'file://component_percona_udf';
```

??? example "Expected output"
	```{.text .no-copy}
	+----------------+------------------------------------------+
	| component_id   | component_urn                            |
	+----------------+------------------------------------------+
	|              1 | file://component_percona_udf             |
	+----------------+------------------------------------------+
	```

A single row means the component is installed and will load on restart. You can also confirm the functions exist by invoking one:

```sql
SELECT fnv_64('check');
```

??? example "Expected output"
	```{.text .no-copy}
	+----------------+
	| fnv_64('check') |
	+----------------+
	| 123456789012345 |
	+----------------+
	```

If the component is not loaded, you get an error such as “Unknown function 'fnv_64'”.

### Uninstall the component

To remove the UDFs, uninstall the component. Any views, stored procedures, or triggers that call these functions will become invalid after uninstall.

```sql
UNINSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"
	```{.text .no-copy}
	Query OK, 0 rows affected (0.00 sec)
	```

You need the `DELETE` privilege on the `mysql.component` system table. See [UNINSTALL COMPONENT](uninstall-component.md) for details.

## Troubleshooting

If `INSTALL COMPONENT` fails:

* Check the error message for details.
* Verify the component path `'file://component_percona_udf'` is correct and that the component library exists in the directory given by `SELECT @@plugin_dir;`.
* Ensure you have the required privileges (for example, `INSERT` on `mysql.component` for install, `DELETE` for uninstall).

For further help, see [Percona Support :octicons-link-external-16:](https://www.percona.com/services/support).

## Next steps

* [Post-installation](post-installation.md) — If you installed the server or the UDF component from a package, configure and secure the server next.

* [Percona Toolkit updates for {{vers}}](percona-toolkit-8.4-updates.md) — If you use other Percona Toolkit tools (for example, `pt-replica-find`), see version-specific updates and terminology changes.

* [Upgrade from plugins to components](upgrade-components.md) — If you are migrating from the old UDF plugin to the component, see the upgrade path.

## Other reading

* Percona Toolkit [documentation :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/)

