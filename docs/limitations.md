# MyRocks limitations

## Online DDL limitations

MyRocks has limited support for [Online DDL operations](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-online-ddl.html) due to the lack of [atomic DDL](./glossary.md#atomic-ddl-data-definition-language). As a result the schema changes are more restricted compared to InnoDB.

### Traditional MyRocks DDL behavior

| Operation type      | Examples                                         | ALGORITHM                   |
|---------------------|--------------------------------------------------|-----------------------------|
| Index operations    | `ADD INDEX`, `DROP INDEX`, `RENAME INDEX`        | `INPLACE` (always)          |
| Column changes      | `ADD COLUMN`, `DROP COLUMN`, `MODIFY COLUMN`     | `COPY` (full table rebuild) |
| Metadata changes    | `RENAME TABLE`, some `RENAME COLUMN` operations  | May be `INSTANT`            |

**Note:** MyRocks does not support [atomic DDL](./glossary.md#atomic-ddl-data-definition-language). Even metadata-only operations may require a full table rebuild, depending on the nature of the change.

### Partition management support

As of `Percona Server for MySQL 8.0.25-15`, MyRocks supports `INPLACE` partition management for certain operations:

```sql
ALTER TABLE t1 DROP PARTITION p1, ALGORITHM=INPLACE;
ALTER TABLE t1 ADD PARTITION (PARTITION p2 VALUES LESS THAN (MAXVALUE)), ALGORITHM=INPLACE;
```
These operations no longer require a full table rebuild. However, operations that modify partitioning schemes, such as changing `VALUES LESS THAN`, still fall back to the `COPY` algorithm.

**Note:** Dropping a partition permanently deletes any data stored in it unless that data is reassigned to another partition.

### Instant DDL support    

As of `Percona Server for MySQL 8.0.42-33`, MyRocks provides limited Instant DDL support that is disabled by default, and you can activate the specific instant operations you need by setting the appropriate configuration variables.

| Configuration variable | Enables Instant DDL for  |
|------------------------|--------------------------|
| [`rocksdb_enable_instant_ddl_for_append_column=ON`](variables.md#rocksdb_enable_instant_ddl_for_append_column) | `ALTER TABLE ... ADD COLUMN` |
| [`rocksdb_enable_instant_ddl_for_column_default_changes=ON`](variables.md#rocksdb_enable_instant_ddl_for_column_default_changes) | `ALTER/MODIFY COLUMN … DEFAULT` |
| [`rocksdb_enable_instant_ddl_for_drop_index_changes=ON`](variables.md#rocksdb_enable_instant_ddl_for_drop_index_changes) | `ALTER TABLE ... DROP INDEX` |
| [`rocksdb_enable_instant_ddl_for_table_comment_changes=ON`](variables.md#rocksdb_enable_instant_ddl_for_table_comment_changes) | `ALTER TABLE ... COMMENT` |

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

* [ALTER TABLE .. EXCHANGE PARTITION](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html).

* [SAVEPOINT](https://dev.mysql.com/doc/refman/8.0/en/savepoint.html)

* [Transportable tablespace](https://dev.mysql.com/doc/refman/8.0/en/innodb-table-import.html)

* [Foreign keys](https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html)

* [Spatial indexes](https://dev.mysql.com/doc/refman/8.0/en/using-spatial-indexes.html)

* [Fulltext indexes](https://dev.mysql.com/doc/refman/8.0/en/innodb-fulltext-index.html)

* [Gap locks](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#innodb-gap-locks)

* [Group Replication](https://dev.mysql.com/doc/refman/8.0/en/group-replication.html)

* [Partial Update of LOB in InnoDB](https://dev.mysql.com/blog-archive/mysql-8-0-optimizing-small-partial-update-of-lob-in-innodb/)

You should also consider the following:

* All collations are supported on ``CHAR`` and ``VARCHAR`` indexed columns. By default, MyRocks prevents creating indexes with non-binary collations (including `latin1`). You can optionally use it by setting [rocksdb_strict_collation_exceptions](variables.md#rocksdb_strict_collation_exceptions) to `t1` (table names with regex format), but non-binary covering indexes other than `latin1` (excluding `german1`) still require a primary key lookup to return the `CHAR` or `VARCHAR` column.

* Either `ORDER BY DESC` or `ORDER BY ASC` is slow. This is because of “Prefix Key Encoding” feature in RocksDB. See [https://www.slideshare.net/matsunobu/myrocks-deep-dive/58](https://www.slideshare.net/matsunobu/myrocks-deep-dive/58) for details. By default, ascending scan is faster and descending scan is slower. If the “reverse column family” is configured, then descending scan will be faster and ascending scan will be slower. Note that InnoDB also imposes a cost when the index is scanned in the opposite order.

* When converting from large MyISAM/InnoDB tables, either by using the `ALTER` or `INSERT INTO SELECT` statements it’s recommended that you check the [Data loading](data-loading.md#myrocks-data-loading) documentation and create MyRocks tables as below (in case the table is sufficiently big it will cause the server to consume all the memory and then be terminated by the OOM killer):

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

* With partitioned tables that use the *TokuDB* or *MyRocks* storage engine, the upgrade only works with native partitioning.

    !!! admonition "See also"

        [MySQL Documentation: Preparing Your Installation for Upgrade](https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.html)

* **Percona Server for MySQL** 8.0 and Unicode 9.0.0 standards have defined a change in the handling of binary collations. These collations are handled as NO PAD, trailing spaces are included in key comparisons. A binary collation comparison may result in two unique rows inserted and does not generate a\`DUP_ENTRY\` error. MyRocks key encoding and comparison does not account for this character set attribute.

## Not supported on MyRocks

MyRocks does not support the following:

* Operating as either a source or a replica in any replication topology that is not exclusively row-based. Statement-based and mixed-format binary logging is not supported. For more information, see [Replication Formats](https://dev.mysql.com/doc/refman/8.0/en/replication-formats.html).

* Using [multi-valued indexes](https://dev.mysql.com/doc/refman/8.0/en/create-index.html#create-index-multi-valued). Implemented in **Percona Server for MySQL** 8.0.17, InnoDB supports this feature.

* Using [spatial data types](https://dev.mysql.com/doc/refman/8.0/en/spatial-type-overview.html) .

* Using the [Clone Plugin](https://dev.mysql.com/doc/refman/8.0/en/clone-plugin.html) and the Clone Plugin API.  As of **Percona Server for MySQL** 8.0.17, InnoDB supports either these features.

* Using encryption in tables. At this time, during an `ALTER TABLE` operation, MyRocks mistakenly detects all InnoDB tables as encrypted. Therefore, any attempt to `ALTER` an InnoDB table to MyRocks fails.

    As a workaround, we recommend a manual move of the table. The following  steps are the same as the `ALTER TABLE ... ENGINE=...` process:

    * Use `SHOW CREATE TABLE ...` to return the InnoDB table definition.

    * With the table definition as the source, perform a `CREATE TABLE ... ENGINE=RocksDB`.

    * In the new table, use `INSERT INTO <new table> SELECT \* FROM <old table>`.

    !!! note

        With MyRocks and with large tables, it is recommended to set the session variable `rocksdb_bulk_load=1` during the load to prevent running out of memory. This recommendation is because of the MyRocks large transaction limitation. For more information, see [MyRocks Data Loading](https://docs.percona.com/percona-server/8.0/myrocks/data-loading.html)

