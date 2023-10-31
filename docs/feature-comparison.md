<!--- Check whether we need this doc --->
# Percona Server for MySQL feature comparison

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads. It delivers higher value to MySQL server users with optimized performance, greater performance scalability and availability, enhanced backups, and increased visibility.

We provide these benefits by significantly enhancing *Percona Server for MySQL* as
compared to the standard *MySQL* database server:

<style>
    table {
        table-layout: fixed;
        width: 100%';
        border-collapse: collapse
        border: 3px solid blue
    }

    thead th:nth-child(1) {
        width: 30%;
        text-align: left;
        vertical-align: top;
    }
    thead th:nth-child(2) {
        width: 25%;
        text-align: center;
        vertical-align: top;
    }
    thead th:nth-child(3) {
        width: 25%;
        text-align: center;
        vertical-align: top;
    }
    th,
    td {padding: 20px;}
</style>


| Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
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


| Improvements for Developers | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
|---|---|---|
| NoSQL Socket-Level Interface | Yes | Yes |
| X API Support | Yes | Yes |
| JSON Functions | Yes | Yes |
| [InnoDB Full-Text Search Improvements](innodb-fts-improvements.md) | Yes | No |
| Extra Hash/Digest Functions | Yes | No |

| Instrumentation and Troubleshooting Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
|---|---|---|
| INFORMATION_SCHEMA Tables | 95 | 65 |
| Global Performance and Status Counters | 853 | 434 |
| Optimizer Histograms | Yes | Yes |
| Per-Table Performance Counters | Yes | No |
| Per-Index Performance Counters | Yes | No |
| Per-User Performance Counters | Yes | No |
| Per-Client Performance Counters | Yes | No |
| Per-Thread Performance Counters | Yes | No |
| Global Query Response Time Statistics | Yes | No |
| [Enhanced SHOW INNODB ENGINE STATUS](innodb-show-status.md) | Yes | No |
| Undo Segment Information | Yes | No |
| Temporary Tables Information | Yes | No |
| [Extended Slow Query Logging](slow-extended.md) | Yes | No |
| [User Statistics](user-stats.md) | Yes | No |

| Performance and Scalability Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
|---|---|---|
| InnoDB Resource Groups | Yes | Yes |
| Configurable Page Sizes | Yes | Yes |
| Contention-Aware Transaction Scheduling | Yes | Yes |
| Improved Scalability By Splitting Mutexes | Yes | No |
| [Improved MEMORY Storage Engine](improved-memory-engine.md) | Yes | No |
| [Improved Flushing](xtradb-performance-improvements.md#multi-threaded-flusher) | Yes | No |
| Parallel Doublewrite Buffer | Yes | Yes |
| [Configurable Fast Index Creation](innodb-expanded-fast-index-creation.md) | Yes | No |
| Per-Column Compression for VARCHAR/BLOB and JSON | Yes | No |
| [Compressed Columns with Dictionaries](compressed-columns.md) | Yes | No |

| Security Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
|---|---|---|
| SQL Roles | Yes | Yes |
| SHA-2 Based Password Hashing | Yes | Yes |
| Password Rotation Policy | Yes | Yes |
| [PAM Authentication Plugin](pam-plugin.md) | Yes | Enterprise-Only |

| Encryption Features | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
|---|---|---|
| Storing Keyring in a File | Yes | Yes |
| Storing Keyring in Hashicorp Vault | Yes | Enterprise Only |
| Encrypt InnoDB Data | Yes | Yes |
| Encrypt InnoDB Logs | Yes | Yes |
| Encrypt Built-In InnoDB Tablespaces (General, System, Undo, Temp) | Yes | Yes |
| [Encrypt Binary Logs](encrypt-binary-relay-log-files.md) | Yes | No |
| [Encrypt Temporary Files](encrypt-temporary-files.md) | Yes | No |
| Enforce Encryption | Yes | No |

| Operational Improvements | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
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

| Features for Running Database as a Service (DBaaS) | Percona Server for MySQL {{vers}} | MySQL {{vers}} |
|---|---|---|
| [Enforce a Specific Storage Engine](enforce-engine.md) | Yes | Yes |