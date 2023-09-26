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


| Features | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
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
| [MyRocks Storage Engine](./myrocks/index.md) | Yes | No |


| Improvements for Developers | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
|---|---|---|
| NoSQL Socket-Level Interface | Yes | Yes |
| X API Support | Yes | Yes |
| JSON Functions | Yes | Yes |
| [InnoDB Full-Text Search Improvements](./flexibility/innodb_fts_improvements.md) | Yes | No |
| Extra Hash/Digest Functions | Yes | No |

| Instrumentation and Troubleshooting Features | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
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
| [Enhanced SHOW INNODB ENGINE STATUS](./diagnostics/innodb_show_status.md) | Yes | No |
| Undo Segment Information | Yes | No |
| Temporary Tables Information | Yes | No |
| [Extended Slow Query Logging](./diagnostics/slow_extended.md) | Yes | No |
| [User Statistics](./diagnostics/user_stats.md) | Yes | No |

| Performance and Scalability Features | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
|---|---|---|
| InnoDB Resource Groups | Yes | Yes |
| Configurable Page Sizes | Yes | Yes |
| Contention-Aware Transaction Scheduling | Yes | Yes |
| Improved Scalability By Splitting Mutexes | Yes | No |
| [Improved MEMORY Storage Engine](./flexibility/improved_memory_engine.md) | Yes | No |
| [Improved Flushing](./performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.md#multi-threaded-flusher) | Yes | No |
| Parallel Doublewrite Buffer | Yes | Yes |
| [Configurable Fast Index Creation](./management/innodb_expanded_fast_index_creation.md) | Yes | No |
| Per-Column Compression for VARCHAR/BLOB and JSON | Yes | No |
| [Compressed Columns with Dictionaries](./flexibility/compressed_columns.md) | Yes | No |

| Security Features | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
|---|---|---|
| SQL Roles | Yes | Yes |
| SHA-2 Based Password Hashing | Yes | Yes |
| Password Rotation Policy | Yes | Yes |
| [PAM Authentication Plugin](./security/pam_plugin.md) | Yes | Enterprise-Only |
| [Audit Logging Plugin](./management/audit_log_plugin.md) | Yes | Enterprise-Only |

| Encryption Features | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
|---|---|---|
| Storing Keyring in a File | Yes | Yes |
| Storing Keyring in Hashicorp Vault | Yes | Enterprise Only |
| Encrypt InnoDB Data | Yes | Yes |
| Encrypt InnoDB Logs | Yes | Yes |
| Encrypt Built-In InnoDB Tablespaces (General, System, Undo, Temp) | Yes | Yes |
| [Encrypt Binary Logs](./security/encrypting-binlogs.md) | Yes | No |
| [Encrypt Temporary Files](./security/encrypting-temporary-files.md) | Yes | No |
| Enforce Encryption | Yes | No |

| Operational Improvements | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
|---|---|---|
| Atomic DDL | Yes | Yes |
| Transactional Data Dictionary | Yes | Yes |
| Instant DDL | Yes | Yes |
| SET PERSIST | Yes | Yes |
| Invisible Indexes | Yes | Yes |
| [Threadpool](./performance/threadpool.md) | Yes | Enterprise-Only |
| [Backup Locks](./backup-locks.md) | Yes | No |
| [Extended SHOW GRANTS](./management/extended_show_grants.md) | Yes | No |
| [Improved Handling of Corrupted Tables](./reliability/innodb_corrupt_table_action.md) | Yes | No |
| [Ability to Kill Idle Transactions](./management/kill_idle_trx.md) | Yes | No |
| [Improvements to START TRANSACTION WITH CONSISTENT SNAPSHOT](./start-transaction-with-consistent-snapshot.md) | Yes | No |

| Features for Running Database as a Service (DBaaS) | Percona Server for MySQL 8.0.30 | MySQL 8.0.30 |
|---|---|---|
| [Enforce a Specific Storage Engine](./management/enforce_engine.md) | Yes | Yes |