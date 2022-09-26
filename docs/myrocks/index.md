# Percona MyRocks Introduction

[MyRocks](http://myrocks.io) is a storage engine
for [MySQL](https://www.mysql.com) based on [RocksDB](http://rocksdb.org/),
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

[Percona MyRocks Installation Guide](install.md)

[MyRocks Limitations](limitations.md)

[Differences between Percona MyRocks and Facebook MyRocks](differences.md)

[*MyRocks* Column Families](column-family.md)

[MyRocks Server Variables](variables.md)

[MyRocks Information Schema Tables](information-schema-tables.md)

[Performance Schema MyRocks changes](performance-schema-tables.md)
