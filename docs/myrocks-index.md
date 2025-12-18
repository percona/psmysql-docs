---
title: 'RocksDB: Percona MyRocks introduction'
description: MyRocks is a storage engine for MySQL based on RocksDB, an embeddable,
  persistent key-value store.
slug: myrocks-index
stability: stable
technical_preview: false
tags:
- myrocks
- percona-server
- rocksdb
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Percona MyRocks introduction

[MyRocks](https://myrocks.io) is a storage engine
for [MySQL](https://www.mysql.com) based on [RocksDB](https://rocksdb.org/),
an embeddable, persistent key-value store.
*Percona MyRocks* is an implementation
for [Percona Server for MySQL](https://www.percona.com/software/percona-server).

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

    To check the RocksDB version currently used by MyRocks, run the following command:

    ```{.bash data-prompt="$"}
    $ head storage/rocksdb/rocksdb/HISTORY.md
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        ...
        ## 8.5.1 (08/31/2023)
        ...
        ```

[Percona MyRocks Installation Guide](install-myrocks.md)

[MyRocks Limitations](myrocks-limitations.md)

[Differences between Percona MyRocks and Facebook MyRocks](myrocks-differences.md)

[*MyRocks* Column Families](myrocks-column-families.md)

[MyRocks Server Variables](myrocks-server-variables.md)

[MyRocks Information Schema Tables](myrocks-information-schema-tables.md)

[Performance Schema MyRocks changes](performance-schema-myrocks-changes.md)