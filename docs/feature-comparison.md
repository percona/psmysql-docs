<!--- Check whether we need this doc --->
# Percona Server for MySQL feature comparison

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads. It delivers higher value to MySQL server users with optimized performance, greater performance scalability and availability, enhanced backups, and increased visibility.

We provide these benefits by significantly enhancing *Percona Server for MySQL* as
compared to the standard *MySQL* database server:

!!! note "MySQL Version Comparison"
    This comparison table compares *Percona Server for MySQL {{vers}}* with *MySQL {{vers}} Community Edition*. When a feature shows "Enterprise-Only" for MySQL, it means that feature is only available in *MySQL {{vers}} Enterprise Edition*, not in the Community Edition. *Percona Server for MySQL* includes many Enterprise features at no cost.

| Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| Open Source | Yes | Yes |
| ACID Compliance | Yes | Yes |
| Multi-Version Concurrency Control | Yes | Yes |
| Row-Level Locking | Yes | Yes |
| Automatic Crash Recovery | Yes | Yes |
| Table Partitioning | Yes | Yes |
| Views | Yes | Yes |
| Subqueries | Yes | Yes |
| Triggers | Yes | Yes |
| Stored Procedures | Yes | Yes |
| Foreign Keys | Yes | Yes |
| Window Functions | Yes | Yes |
| Common Table Expressions | Yes | Yes |
| Geospatial Features (GIS, SRS) | Yes | Yes |
| GTID Replication | Yes | Yes |
| Group Replication | Yes | Yes |
| [MyRocks Storage Engine](myrocks-index.md) | Yes | No |


| Improvements for Developers | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| NoSQL Socket-Level Interface | Yes | Yes |
| X API Support | Yes | Yes |
| JSON Functions | Yes | Yes |
| [InnoDB Full-Text Search Improvements](innodb-fts-improvements.md) | Yes | No |
| [Extra Hash/Digest Functions](encryption-functions.md) | Yes | No |
| [UUID_VX Component](uuid-versions.md) | Yes | No |

| Instrumentation and Troubleshooting Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| INFORMATION_SCHEMA Tables | 95 | 65 |
| Global Performance and Status Counters | 853 | 434 |
| Optimizer Histograms | Yes | Yes |
| [Per-Table Performance Counters](user-stats.md#information_schematable_statistics) | Yes | No |
| [Per-Index Performance Counters](user-stats.md#information_schemaindex_statistics) | Yes | No |
| [Per-User Performance Counters](user-stats.md#information_schemauser_statistics) | Yes | No |
| [Per-Client Performance Counters](user-stats.md#information_schemaclient_statistics) | Yes | No |
| [Per-Thread Performance Counters](user-stats.md#information_schemathread_statistics) | Yes | No |
| [Global Query Response Time Statistics](index-info-schema-tables.md#information_schemaquery_response_time) | Yes | No |
| [Enhanced SHOW INNODB ENGINE STATUS](innodb-show-status.md) | Yes | No |
| [Undo Segment Information](innodb-show-status.md) | Yes | No |
| [Temporary Tables Information](misc-info-schema-tables.md#information_schematemporary_tables) | Yes | No |
| [Extended Slow Query Logging](slow-extended.md) | Yes | No |
| [User Statistics](user-stats.md) | Yes | No |

| Performance and Scalability Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| InnoDB Resource Groups | Yes | Yes |
| Configurable Page Sizes | Yes | Yes |
| Contention-Aware Transaction Scheduling | Yes | Yes |
| [Improved Scalability By Splitting Mutexes](xtradb-performance-improvements.md) | Yes | No |
| [Improved MEMORY Storage Engine](improved-memory-engine.md) | Yes | No |
| [Improved Flushing](xtradb-performance-improvements.md#multi-threaded-lru-flusher) | Yes | No |
| Improved Binlog Transaction Dependency Tracking | Yes | No |
| Parallel Doublewrite Buffer | Yes | Yes |
| [Configurable Fast Index Creation](innodb-expanded-fast-index-creation.md) | Yes | No |
| [Per-Column Compression for VARCHAR/BLOB and JSON](compressed-columns.md) | Yes | No |
| [Compressed Columns with Dictionaries](compressed-columns.md) | Yes | No |

| Security Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| SQL Roles | Yes | Yes |
| SHA-2 Based Password Hashing | Yes | Yes |
| Password Rotation Policy | Yes | Yes |
| [PAM Authentication Plugin](pam-plugin.md) | Yes | Enterprise-Only |
| [Data Masking Component](data-masking-overview.md) | Yes | Enterprise-Only |

| Encryption Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| Storing Keyring in a File | Yes | Yes |
| Storing Keyring in Hashicorp Vault | Yes | Enterprise-Only |
| Encrypt InnoDB Data | Yes | Yes |
| Encrypt InnoDB Logs | Yes | Yes |
| Encrypt Built-In InnoDB Tablespaces (General, System, Undo, Temp) | Yes | Yes |
| [Encrypt Binary Logs](encrypt-binary-relay-log-files.md) | Yes | No |
| [Encrypt Temporary Files](encrypt-temporary-files.md) | Yes | No |
| [Enforce Encryption](encrypt-tablespaces.md#default_table_encryption) | Yes | No |

| Operational Improvements | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| Atomic DDL | Yes | Yes |
| Transactional Data Dictionary | Yes | Yes |
| Instant DDL | Yes | Yes |
| SET PERSIST | Yes | Yes |
| Invisible Indexes | Yes | Yes |
| [Threadpool](threadpool.md) | Yes | Enterprise-Only |
| [Backup Locks](backup-locks.md) | Yes | No |
| [Extended SHOW GRANTS](extended-show-grants.md) | Yes | No |
| [Improved Handling of Corrupted Tables](innodb-corrupt-table-action.md) | Yes | No |
| [Ability to Kill Idle Transactions](kill-idle-trx.md) | Yes | No |
| [Improvements to START TRANSACTION WITH CONSISTENT SNAPSHOT](start-transaction-with-consistent-snapshot.md) | Yes | No |

| Features for Running Database as a Service (DBaaS) | Percona Server for MySQL {{vers}} | MySQL {{vers}} Community Edition |
|---|---|---|
| [Enforce a Specific Storage Engine](enforce-engine.md) | Yes | Yes |