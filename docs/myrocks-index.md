# Percona MyRocks introduction

[MyRocks :octicons-link-external-16:](https://myrocks.io) is a storage engine
for [MySQL :octicons-link-external-16:](https://www.mysql.com) based on [RocksDB :octicons-link-external-16:](https://rocksdb.org/),
an embeddable, persistent key-value store.
*Percona MyRocks* is an implementation
for [Percona Server for MySQL :octicons-link-external-16:](https://www.percona.com/software/percona-server).

The RocksDB store is based on the log-structured merge-tree (or LSM
tree). It is optimized for fast storage and combines outstanding
space and write efficiency with acceptable read performance. As a
result, MyRocks has the following advantages compared to other storage
engines, if your workload uses fast storage, such as SSD:

* Requires less storage space

* Provides more storage endurance

* Ensures better IO capacity

!!! important

    The latest MyRocks storage engine is based on recent RocksDB source code, with minor modifications applied by Percona.

    Percona Server for MySQL 8.4.13-12 bundles RocksDB 9.7.4.

    The previous bundle was RocksDB 9.3.1.

    The intermediate bundles were RocksDB 9.3.2, fb.9.6, and 9.7.1.

    [RocksDB 9.4.0 to 9.7.4](myrocks-added-features.md#rocksdb-940-to-974) lists the user-visible RocksDB changes.

    [Downgrade to MyRocks 9.3.1](myrocks-added-features.md#downgrade-to-myrocks-931) lists the downgrade steps.

    To check the RocksDB version currently used by MyRocks, run the following command:

    ```{.bash data-prompt="$"}
    $ head storage/rocksdb/rocksdb/HISTORY.md
    ```

    The first version heading in `HISTORY.md` is the bundled RocksDB version.

[Percona MyRocks Installation Guide](install-myrocks.md)

[MyRocks Limitations](myrocks-limitations.md)

[Differences between Percona MyRocks and Facebook MyRocks](myrocks-differences.md)

[*MyRocks* Column Families](myrocks-column-families.md)

[MyRocks Server Variables](myrocks-server-variables.md)

[MyRocks Information Schema Tables](myrocks-information-schema-tables.md)

[SHOW ENGINE ROCKSDB TRANSACTION STATUS](myrocks-transaction-status.md)

[Performance Schema MyRocks changes](performance-schema-myrocks-changes.md)
