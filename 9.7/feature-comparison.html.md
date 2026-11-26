> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Percona Server for MySQL feature comparison

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads. It delivers higher value to MySQL server users with optimized performance, greater performance scalability and availability, enhanced backups, and increased visibility.

We provide these benefits by significantly enhancing *Percona Server for MySQL* as compared to the standard *MySQL* database server:

| Features                                                                               | Percona Server for MySQL 9.7 | MySQL 9.7 |
| -------------------------------------------------------------------------------------- | ---------------------------- | --------- |
| Open Source                                                                            | Yes                          | Yes       |
| ACID Compliance                                                                        | Yes                          | Yes       |
| Multi-Version Concurrency Control                                                      | Yes                          | Yes       |
| Row-Level Locking                                                                      | Yes                          | Yes       |
| Automatic Crash Recovery                                                               | Yes                          | Yes       |
| Table Partitioning                                                                     | Yes                          | Yes       |
| Views                                                                                  | Yes                          | Yes       |
| Subqueries                                                                             | Yes                          | Yes       |
| Triggers                                                                               | Yes                          | Yes       |
| Stored Procedures                                                                      | Yes                          | Yes       |
| Foreign Keys                                                                           | Yes                          | Yes       |
| Window Functions                                                                       | Yes                          | Yes       |
| Common Table Expressions                                                               | Yes                          | Yes       |
| Geospatial Features (GIS, SRS)                                                         | Yes                          | Yes       |
| GTID Replication                                                                       | Yes                          | Yes       |
| Group Replication                                                                      | Yes                          | Yes       |
| [MyRocks Storage Engine](https://docs.percona.com/percona-server/9.7/myrocks-index.md) | Yes                          | No        |

| Improvements for Developers                                                                                    | Percona Server for MySQL 9.7 | MySQL 9.7 |
| -------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------- |
| NoSQL Socket-Level Interface                                                                                   | Yes                          | Yes       |
| X API Support                                                                                                  | Yes                          | Yes       |
| JSON Functions                                                                                                 | Yes                          | Yes       |
| [InnoDB Full-Text Search Improvements](https://docs.percona.com/percona-server/9.7/innodb-fts-improvements.md) | Yes                          | No        |
| Extra Hash/Digest Functions                                                                                    | Yes                          | No        |

| Instrumentation and Troubleshooting Features                                                            | Percona Server for MySQL 9.7 | MySQL 9.7 |
| ------------------------------------------------------------------------------------------------------- | ---------------------------- | --------- |
| INFORMATION_SCHEMA Tables                                                                               | 95                           | 65        |
| Global Performance and Status Counters                                                                  | 853                          | 434       |
| Optimizer Histograms                                                                                    | Yes                          | Yes       |
| Per-Table Performance Counters                                                                          | Yes                          | No        |
| Per-Index Performance Counters                                                                          | Yes                          | No        |
| Per-User Performance Counters                                                                           | Yes                          | No        |
| Per-Client Performance Counters                                                                         | Yes                          | No        |
| Per-Thread Performance Counters                                                                         | Yes                          | No        |
| Global Query Response Time Statistics                                                                   | Yes                          | No        |
| [Enhanced SHOW INNODB ENGINE STATUS](https://docs.percona.com/percona-server/9.7/innodb-show-status.md) | Yes                          | No        |
| Undo Segment Information                                                                                | Yes                          | No        |
| Temporary Tables Information                                                                            | Yes                          | No        |
| [Extended Slow Query Logging](https://docs.percona.com/percona-server/9.7/slow-extended.md)             | Yes                          | No        |
| [User Statistics](https://docs.percona.com/percona-server/9.7/user-stats.md)                            | Yes                          | No        |

| Performance and Scalability Features                                                                                           | Percona Server for MySQL 9.7 | MySQL 9.7 |
| ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- | --------- |
| InnoDB Resource Groups                                                                                                         | Yes                          | Yes       |
| Configurable Page Sizes                                                                                                        | Yes                          | Yes       |
| Contention-Aware Transaction Scheduling                                                                                        | Yes                          | Yes       |
| Improved Scalability By Splitting Mutexes                                                                                      | Yes                          | No        |
| [Improved MEMORY Storage Engine](https://docs.percona.com/percona-server/9.7/improved-memory-engine.md)                        | Yes                          | No        |
| [Improved Flushing](https://docs.percona.com/percona-server/9.7/xtradb-performance-improvements.md#multi-threaded-lru-flusher) | Yes                          | No        |
| Parallel Doublewrite Buffer                                                                                                    | Yes                          | Yes       |
| [Configurable Fast Index Creation](https://docs.percona.com/percona-server/9.7/innodb-expanded-fast-index-creation.md)         | Yes                          | No        |
| Per-Column Compression for VARCHAR/BLOB and JSON                                                                               | Yes                          | No        |
| [Compressed Columns with Dictionaries](https://docs.percona.com/percona-server/9.7/compressed-columns.md)                      | Yes                          | No        |

| Security Features                                                                      | Percona Server for MySQL 9.7 | MySQL 9.7       |
| -------------------------------------------------------------------------------------- | ---------------------------- | --------------- |
| SQL Roles                                                                              | Yes                          | Yes             |
| SHA-2 Based Password Hashing                                                           | Yes                          | Yes             |
| Password Rotation Policy                                                               | Yes                          | Yes             |
| [PAM Authentication Plugin](https://docs.percona.com/percona-server/9.7/pam-plugin.md) | Yes                          | Enterprise-Only |

| Encryption Features                                                                                  | Percona Server for MySQL 9.7 | MySQL 9.7       |
| ---------------------------------------------------------------------------------------------------- | ---------------------------- | --------------- |
| Storing Keyring in a File                                                                            | Yes                          | Yes             |
| Storing Keyring in Hashicorp Vault                                                                   | Yes                          | Enterprise Only |
| Encrypt InnoDB Data                                                                                  | Yes                          | Yes             |
| Encrypt InnoDB Logs                                                                                  | Yes                          | Yes             |
| Encrypt Built-In InnoDB Tablespaces (General, System, Undo, Temp)                                    | Yes                          | Yes             |
| [Encrypt Binary Logs](https://docs.percona.com/percona-server/9.7/encrypt-binary-relay-log-files.md) | Yes                          | No              |
| [Encrypt Temporary Files](https://docs.percona.com/percona-server/9.7/encrypt-temporary-files.md)    | Yes                          | No              |
| Enforce Encryption                                                                                   | Yes                          | No              |

| Operational Improvements                                                                                                                                | Percona Server for MySQL 9.7 | MySQL 9.7       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------- |
| Atomic DDL                                                                                                                                              | Yes                          | Yes             |
| Transactional Data Dictionary                                                                                                                           | Yes                          | Yes             |
| Instant DDL                                                                                                                                             | Yes                          | Yes             |
| SET PERSIST                                                                                                                                             | Yes                          | Yes             |
| Invisible Indexes                                                                                                                                       | Yes                          | Yes             |
| [Threadpool](https://docs.percona.com/percona-server/9.7/threadpool.md)                                                                                 | Yes                          | Enterprise-Only |
| [Backup Locks](https://docs.percona.com/percona-server/9.7/backup-locks.md)                                                                             | Yes                          | No              |
| [Extended SHOW GRANTS](https://docs.percona.com/percona-server/9.7/extended-show-grants.md)                                                             | Yes                          | No              |
| [Improved Handling of Corrupted Tables](https://docs.percona.com/percona-server/9.7/innodb-corrupt-table-action.md)                                     | Yes                          | No              |
| [Ability to Kill Idle Transactions](https://docs.percona.com/percona-server/9.7/kill-idle-trx.md)                                                       | Yes                          | No              |
| [Improvements to START TRANSACTION WITH CONSISTENT SNAPSHOT](https://docs.percona.com/percona-server/9.7/start-transaction-with-consistent-snapshot.md) | Yes                          | No              |

| Features for Running Database as a Service (DBaaS)                                                 | Percona Server for MySQL 9.7 | MySQL 9.7 |
| -------------------------------------------------------------------------------------------------- | ---------------------------- | --------- |
| [Enforce a Specific Storage Engine](https://docs.percona.com/percona-server/9.7/enforce-engine.md) | Yes                          | Yes       |
