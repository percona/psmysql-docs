# MyRocks limitations

## Online DDL limitations

MyRocks has limited support for [Online DDL operations :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-online-ddl.html) due to the lack of [atomic DDL](./glossary.md#atomic-ddl-data-definition-language). As a result the schema changes are more restricted compared to InnoDB.

### Traditional MyRocks DDL behavior

| Operation type      | Examples                                         | ALGORITHM                   |
|---------------------|--------------------------------------------------|-----------------------------|
| Index operations    | `ADD INDEX`, `DROP INDEX`, `RENAME INDEX`        | `INPLACE` (always)          |
| Column changes      | `ADD COLUMN`, `DROP COLUMN`, `MODIFY COLUMN`     | `COPY` (full table rebuild) |
| Metadata changes    | `RENAME TABLE`, some `RENAME COLUMN` operations  | May be `INSTANT`            |

**Note:** MyRocks does not support [atomic DDL](./glossary.md#atomic-ddl-data-definition-language). Even metadata-only operations may require a full table rebuild, depending on the nature of the change.

### Partition management support

MyRocks supports `INPLACE` partition management for certain operations:

```sql
ALTER TABLE t1 DROP PARTITION p1, ALGORITHM=INPLACE;
ALTER TABLE t1 ADD PARTITION (PARTITION p2 VALUES LESS THAN (MAXVALUE)), ALGORITHM=INPLACE;
```
These operations does not require a full table rebuild. However, operations that modify partitioning schemes, such as changing `VALUES LESS THAN`, fall back to the `COPY` algorithm.

**Note:** Dropping a partition permanently deletes any data stored in it unless that data is reassigned to another partition.

`INPLACE` `ADD PARTITION` and `DROP PARTITION` require [`rocksdb_allow_unsafe_alter`](myrocks-server-variables.md#rocksdb_allow_unsafe_alter) set to `ON`. MyRocks does not support `INPLACE` `ADD PARTITION` for `HASH` partitions.

With `ALGORITHM=INPLACE`, the server deletes rows in the dropped partition. With `ALGORITHM=COPY`, the server can move compatible rows into another partition.

### Recover mismatched partition metadata

An `INPLACE` `ADD PARTITION` or `DROP PARTITION` under [`rocksdb_allow_unsafe_alter`](myrocks-server-variables.md#rocksdb_allow_unsafe_alter) is crash-unsafe. A stop before the operation completes can leave the MySQL data dictionary and the MyRocks data dictionary in a mismatched state. Use the following procedure to recover.

MyRocks does not support atomic DDL. An `INPLACE` partition alter updates storage-engine objects and data-dictionary metadata in separate stages. A stop before every stage completes can leave incomplete DDL and inconsistent metadata.

The incomplete DDL can produce the following outcomes:

* Schema mismatch between the MySQL data dictionary and the MyRocks data dictionary

* Orphan partition objects in MyRocks that the MySQL data dictionary does not list

* Partition entries in the MySQL data dictionary that lack matching MyRocks objects

* Startup failure when [`rocksdb_validate_tables`](myrocks-server-variables.md#rocksdb_validate_tables) equals `1`

* Partial `ADD PARTITION` or `DROP PARTITION` results that require repair or restore

!!! warning

    The following actions can make recoverable data inaccessible.

    * Do not repeat the interrupted `ALTER TABLE` statement.

    * Do not edit the MyRocks data dictionary by hand.

    * Do not delete RocksDB files.

    * Do not run another partition operation against the affected table.

#### Step 1: Preserve the current state

1. Stop the server.

2. Preserve a copy or storage snapshot of the complete MySQL data directory and [`rocksdb_datadir`](myrocks-server-variables.md#rocksdb_datadir).

3. Retain the error log and binary logs.

#### Step 2: Select a recovery source

Recover from a known-consistent source. Use the first branch that applies:

| Source | Action |
|--------|--------|
| Healthy replica | If a healthy replica holds matching table and MyRocks metadata, use that replica as the recovery source. Rebuild the damaged server from that replica. |
| Verified backup | If no healthy replica is available, restore a backup taken before the interrupted `ALTER TABLE`. Apply binary logs only to a verified consistent position. Do not replay the interrupted unsafe statement. |
| No replica and no backup | If neither source exists, contact Percona Support or an experienced MyRocks administrator. Do not change the instance before that contact. |

#### Step 3: Diagnose a startup mismatch

Complete this step only when validation reports a mismatch and the server cannot start.

1. Run diagnostics on a copy of the damaged instance.

2. Start that copy in an isolated, read-only environment with the following configuration:

    ```ini
    [mysqld]
    rocksdb_validate_tables=2
    ```

    !!! note

        `rocksdb_validate_tables=2` allows startup despite validation errors. This setting does not repair the mismatch.

3. Compare the partition definitions held by MySQL and MyRocks:

    ```sql
    SELECT PARTITION_NAME
      FROM INFORMATION_SCHEMA.PARTITIONS
     WHERE TABLE_SCHEMA = 'database_name'
       AND TABLE_NAME = 'table_name'
       AND PARTITION_NAME IS NOT NULL
     ORDER BY PARTITION_NAME;

    SELECT DISTINCT PARTITION_NAME
      FROM INFORMATION_SCHEMA.ROCKSDB_DDL
     WHERE TABLE_SCHEMA = 'database_name'
       AND TABLE_NAME = 'table_name'
       AND PARTITION_NAME IS NOT NULL
     ORDER BY PARTITION_NAME;
    ```

#### Step 4: Choose a recovery path

Select the branch that matches the query results:

| Condition | Action |
|-----------|--------|
| Every expected partition is accessible and the table reads completely | Perform a logical salvage. Complete the following logical salvage steps. |
| An expected partition is missing or cannot be read | Restore from a backup or healthy replica. Do not create an empty replacement partition to force a metadata match. The interrupted operation may have deleted or orphaned data for that partition. |

Complete the following logical salvage steps on a copy or separate recovery instance:

1. Export the table schema and rows.

2. Create a new table or clean instance with the intended partition definition.

3. Load the exported rows.

4. Validate row counts, partition placement, and application-level checksums before replacement of the damaged table or instance.

!!! note

    Do not repair the internal MyRocks entries directly.

#### Step 5: Return the server to service

1. Remove `rocksdb_validate_tables=2` or restore the default value of `1`.

2. Set `rocksdb_allow_unsafe_alter=OFF`.

3. Restart the server.

4. Confirm that startup validation succeeds.

5. Confirm that both partition queries return matching names.

6. Confirm that all partitions are readable.

7. Confirm that replication is consistent.

For a `ROCKSDB_CORRUPTED` marker file, see [`rocksdb_allow_to_start_after_corruption`](myrocks-server-variables.md#rocksdb_allow_to_start_after_corruption).

### Instant DDL support    

MyRocks provides limited Instant DDL support that is disabled by default, and you can activate the specific instant operations you need by setting the appropriate configuration variables.

| Configuration variable | Enables Instant DDL for  |
|------------------------|--------------------------|
| [`rocksdb_enable_instant_ddl_for_append_column=ON`](myrocks-server-variables.md#rocksdb_enable_instant_ddl_for_append_column) | `ALTER TABLE ... ADD COLUMN` |
| [`rocksdb_enable_instant_ddl_for_column_default_changes=ON`](myrocks-server-variables.md#rocksdb_enable_instant_ddl_for_column_default_changes) | `ALTER/MODIFY COLUMN … DEFAULT` |
| [`rocksdb_enable_instant_ddl_for_drop_index_changes=ON`](myrocks-server-variables.md#rocksdb_enable_instant_ddl_for_drop_index_changes) | `ALTER TABLE ... DROP INDEX` |
| [`rocksdb_enable_instant_ddl_for_table_comment_changes=ON`](myrocks-server-variables.md#rocksdb_enable_instant_ddl_for_table_comment_changes) | `ALTER TABLE ... COMMENT` |

**Note:** Instant DDL in MyRocks is applied only when **both** of the following conditions are met:

* The configuration variable is set to `ON`.
* The `ALTER TABLE` statement explicitly includes `ALGORITHM=INSTANT`.

For example:

```sql
SET GLOBAL rocksdb_enable_instant_ddl_for_table_comment_changes = ON;
ALTER TABLE my_table COMMENT = 'New comment', ALGORITHM=INSTANT;
```

If either condition is missing:

* When the variable is `ON` but `ALGORITHM=INSTANT` is omitted, MyRocks falls back to the default (non‑instant) algorithm.
* When the variable is `OFF`, any `ALTER TABLE … ALGORITHM=INSTANT` statement fails with an error.

## Unsupported InnoDB features in MyRocks

* [ALTER TABLE .. EXCHANGE PARTITION :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/partitioning-management-exchange.html).

* [SAVEPOINT :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/savepoint.html)

* [Transportable tablespace :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-table-import.html)

* [Foreign keys :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/create-table-foreign-keys.html)

* [Spatial indexes :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/using-spatial-indexes.html)

* [Fulltext indexes :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-fulltext-index.html)

* [Gap locks :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-locking.html#innodb-gap-locks)

* [Group Replication :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/group-replication.html)

* [Partial Update of LOB in InnoDB :octicons-link-external-16:](https://dev.mysql.com/blog-archive/mysql-8-0-optimizing-small-partial-update-of-lob-in-innodb/)

You should also consider the following:

* All collations are supported on ``CHAR`` and ``VARCHAR`` indexed columns. By default, MyRocks prevents creating indexes with non-binary collations (including `latin1`). You can optionally use it by setting [rocksdb_strict_collation_exceptions](myrocks-server-variables.md#rocksdb_strict_collation_exceptions) to `t1` (table names with regex format), but non-binary covering indexes other than `latin1` (excluding `german1`) still require a primary key lookup to return the `CHAR` or `VARCHAR` column.

* Either `ORDER BY DESC` or `ORDER BY ASC` is slow. This is because of “Prefix Key Encoding” feature in RocksDB. See [https://www.slideshare.net/matsunobu/myrocks-deep-dive/58](https://www.slideshare.net/matsunobu/myrocks-deep-dive/58) for details. By default, ascending scan is faster and descending scan is slower. If the “reverse column family” is configured, then descending scan will be faster and ascending scan will be slower. Note that InnoDB also imposes a cost when the index is scanned in the opposite order.

* When converting from large MyISAM/InnoDB tables, either by using the `ALTER` or `INSERT INTO SELECT` statements it’s recommended that you check the [Data loading](myrocks-data-loading.md#loading-data) documentation and create MyRocks tables as below (in case the table is sufficiently big it will cause the server to consume all the memory and then be terminated by the OOM killer):

```sql
 SET session sql_log_bin=0;
 SET session rocksdb_bulk_load=1;
 ALTER TABLE large_myisam_table ENGINE=RocksDB;
 SET session rocksdb_bulk_load=0;
```

??? example "Expected output"

    ```{.text .no-copy}
    .. warning::

       If you are loading large data without enabling :ref:`rocksdb_bulk_load`
       or :ref:`rocksdb_commit_in_the_middle`, please make sure transaction
       ize is small enough. All modifications of the ongoing transactions are
       kept in memory.
    ```

* With partitioned tables that use the *MyRocks* storage engine, the upgrade only works with native partitioning.

    !!! admonition "See also"

        [MySQL Documentation: Preparing Your Installation for Upgrade :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-prerequisites.html)

* Percona Server for MySQL {{vers}} and Unicode 9.0.0 standards have defined a change in the handling of binary collations. These collations are handled as NO PAD, trailing spaces are included in key comparisons. A binary collation comparison may result in two unique rows inserted and does not generate a\`DUP_ENTRY\` error. MyRocks key encoding and comparison does not account for this character set attribute.

## Not supported on MyRocks

MyRocks does not support the following:

* Operating as either a source or a replica in any replication topology that is not exclusively row-based. Statement-based and mixed-format binary logging is not supported. For more information, see [Replication Formats :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/replication-formats.html).

* Using [multi-valued indexes :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/create-index.html#create-index-multi-valued). InnoDB supports this feature.

* Using [spatial data types :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/spatial-type-overview.html) .

* Using the [Clone Plugin :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/clone-plugin.html) and the Clone Plugin API. InnoDB supports either these features.

* Using encryption in tables. At this time, during an `ALTER TABLE` operation, MyRocks mistakenly detects all InnoDB tables as encrypted. Therefore, any attempt to `ALTER` an InnoDB table to MyRocks fails.

    As a workaround, we recommend a manual move of the table. The following  steps are the same as the `ALTER TABLE ... ENGINE=...` process:

    * Use `SHOW CREATE TABLE ...` to return the InnoDB table definition.

    * With the table definition as the source, perform a `CREATE TABLE ... ENGINE=RocksDB`.

    * In the new table, use `INSERT INTO <new table> SELECT \* FROM <old table>`.

    !!! note

        With MyRocks and with large tables, it is recommended to set the session variable `rocksdb_bulk_load=1` during the load to prevent running out of memory. This recommendation is because of the MyRocks large transaction limitation. For more information, see [MyRocks Data Loading](myrocks-data-loading.md)

