> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Percona Server for MySQL feature comparison

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads. It delivers higher value to MySQL server users with optimized performance, greater performance scalability and availability, enhanced backups, and increased visibility.

We provide these benefits by significantly enhancing *Percona Server for MySQL* as compared to the standard *MySQL* database server:

MySQL Version Comparison

This comparison table compares *Percona Server for MySQL 8.4* with *MySQL 8.4 Community Edition*. When a feature shows “Enterprise-Only” for MySQL, it means that feature is only available in *MySQL 8.4 Enterprise Edition*, not in the Community Edition. *Percona Server for MySQL* includes many Enterprise features at no cost.

| Features                                                                                 | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| ---------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| Open Source                                                                              | Yes                          | Yes                         |
| ACID Compliance                                                                          | Yes                          | Yes                         |
| Multi-Version Concurrency Control                                                        | Yes                          | Yes                         |
| Row-Level Locking                                                                        | Yes                          | Yes                         |
| Automatic Crash Recovery                                                                 | Yes                          | Yes                         |
| Table Partitioning                                                                       | Yes                          | Yes                         |
| Views                                                                                    | Yes                          | Yes                         |
| Subqueries                                                                               | Yes                          | Yes                         |
| Triggers                                                                                 | Yes                          | Yes                         |
| Stored Procedures                                                                        | Yes                          | Yes                         |
| Foreign Keys                                                                             | Yes                          | Yes                         |
| Window Functions                                                                         | Yes                          | Yes                         |
| Common Table Expressions                                                                 | Yes                          | Yes                         |
| Geospatial Features (GIS, SRS)                                                           | Yes                          | Yes                         |
| GTID Replication                                                                         | Yes                          | Yes                         |
| Group Replication                                                                        | Yes                          | Yes                         |
| [MyRocks Storage Engine](https://docs.percona.com/percona-server/8.4/myrocks-index.html) | Yes                          | No                          |

| Improvements for Developers                                                                                      | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| ---------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| NoSQL Socket-Level Interface                                                                                     | Yes                          | Yes                         |
| X API Support                                                                                                    | Yes                          | Yes                         |
| JSON Functions                                                                                                   | Yes                          | Yes                         |
| [InnoDB Full-Text Search Improvements](https://docs.percona.com/percona-server/8.4/innodb-fts-improvements.html) | Yes                          | No                          |
| [Extra Hash/Digest Functions](https://docs.percona.com/percona-server/8.4/encryption-functions.html)             | Yes                          | No                          |
| [UUID_VX Component](https://docs.percona.com/percona-server/8.4/uuid-versions.html)                              | Yes                          | No                          |

| Instrumentation and Troubleshooting Features                                                                                                             | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| INFORMATION_SCHEMA Tables                                                                                                                                | 95                           | 65                          |
| Global Performance and Status Counters                                                                                                                   | 853                          | 434                         |
| Optimizer Histograms                                                                                                                                     | Yes                          | Yes                         |
| [Per-Table Performance Counters](https://docs.percona.com/percona-server/8.4/user-stats.html#information_schematable_statistics)                         | Yes                          | No                          |
| [Per-Index Performance Counters](https://docs.percona.com/percona-server/8.4/user-stats.html#information_schemaindex_statistics)                         | Yes                          | No                          |
| [Per-User Performance Counters](https://docs.percona.com/percona-server/8.4/user-stats.html#information_schemauser_statistics)                           | Yes                          | No                          |
| [Per-Client Performance Counters](https://docs.percona.com/percona-server/8.4/user-stats.html#information_schemaclient_statistics)                       | Yes                          | No                          |
| [Per-Thread Performance Counters](https://docs.percona.com/percona-server/8.4/user-stats.html#information_schemathread_statistics)                       | Yes                          | No                          |
| [Global Query Response Time Statistics](https://docs.percona.com/percona-server/8.4/index-info-schema-tables.html#information_schemaquery_response_time) | Yes                          | No                          |
| [Enhanced SHOW INNODB ENGINE STATUS](https://docs.percona.com/percona-server/8.4/innodb-show-status.html)                                                | Yes                          | No                          |
| [Undo Segment Information](https://docs.percona.com/percona-server/8.4/innodb-show-status.html)                                                          | Yes                          | No                          |
| [Temporary Tables Information](https://docs.percona.com/percona-server/8.4/misc-info-schema-tables.html#information_schematemporary_tables)              | Yes                          | No                          |
| [Extended Slow Query Logging](https://docs.percona.com/percona-server/8.4/slow-extended.html)                                                            | Yes                          | No                          |
| [User Statistics](https://docs.percona.com/percona-server/8.4/user-stats.html)                                                                           | Yes                          | No                          |

| Performance and Scalability Features                                                                                             | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| InnoDB Resource Groups                                                                                                           | Yes                          | Yes                         |
| Configurable Page Sizes                                                                                                          | Yes                          | Yes                         |
| Contention-Aware Transaction Scheduling                                                                                          | Yes                          | Yes                         |
| [Improved Scalability By Splitting Mutexes](https://docs.percona.com/percona-server/8.4/xtradb-performance-improvements.html)    | Yes                          | No                          |
| [Improved MEMORY Storage Engine](https://docs.percona.com/percona-server/8.4/improved-memory-engine.html)                        | Yes                          | No                          |
| [Improved Flushing](https://docs.percona.com/percona-server/8.4/xtradb-performance-improvements.html#multi-threaded-lru-flusher) | Yes                          | No                          |
| Improved Binlog Transaction Dependency Tracking                                                                                  | Yes                          | No                          |
| Parallel Doublewrite Buffer                                                                                                      | Yes                          | Yes                         |
| [Configurable Fast Index Creation](https://docs.percona.com/percona-server/8.4/innodb-expanded-fast-index-creation.html)         | Yes                          | No                          |
| [Per-Column Compression for VARCHAR/BLOB and JSON](https://docs.percona.com/percona-server/8.4/compressed-columns.html)          | Yes                          | No                          |
| [Compressed Columns with Dictionaries](https://docs.percona.com/percona-server/8.4/compressed-columns.html)                      | Yes                          | No                          |

| Security Features                                                                                | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| ------------------------------------------------------------------------------------------------ | ---------------------------- | --------------------------- |
| SQL Roles                                                                                        | Yes                          | Yes                         |
| SHA-2 Based Password Hashing                                                                     | Yes                          | Yes                         |
| Password Rotation Policy                                                                         | Yes                          | Yes                         |
| [PAM Authentication Plugin](https://docs.percona.com/percona-server/8.4/pam-plugin.html)         | Yes                          | Enterprise-Only             |
| [Data Masking Component](https://docs.percona.com/percona-server/8.4/data-masking-overview.html) | Yes                          | Enterprise-Only             |

| Encryption Features                                                                                                 | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| ------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| Storing Keyring in a File                                                                                           | Yes                          | Yes                         |
| Storing Keyring in Hashicorp Vault                                                                                  | Yes                          | Enterprise-Only             |
| Encrypt InnoDB Data                                                                                                 | Yes                          | Yes                         |
| Encrypt InnoDB Logs                                                                                                 | Yes                          | Yes                         |
| Encrypt Built-In InnoDB Tablespaces (General, System, Undo, Temp)                                                   | Yes                          | Yes                         |
| [Encrypt Binary Logs](https://docs.percona.com/percona-server/8.4/encrypt-binary-relay-log-files.html)              | Yes                          | No                          |
| [Encrypt Temporary Files](https://docs.percona.com/percona-server/8.4/encrypt-temporary-files.html)                 | Yes                          | No                          |
| [Enforce Encryption](https://docs.percona.com/percona-server/8.4/encrypt-tablespaces.html#default_table_encryption) | Yes                          | No                          |

| Operational Improvements                                                                                                                                  | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| Atomic DDL                                                                                                                                                | Yes                          | Yes                         |
| Transactional Data Dictionary                                                                                                                             | Yes                          | Yes                         |
| Instant DDL                                                                                                                                               | Yes                          | Yes                         |
| SET PERSIST                                                                                                                                               | Yes                          | Yes                         |
| Invisible Indexes                                                                                                                                         | Yes                          | Yes                         |
| [Threadpool](https://docs.percona.com/percona-server/8.4/threadpool.html)                                                                                 | Yes                          | Enterprise-Only             |
| [Backup Locks](https://docs.percona.com/percona-server/8.4/backup-locks.html)                                                                             | Yes                          | No                          |
| [Extended SHOW GRANTS](https://docs.percona.com/percona-server/8.4/extended-show-grants.html)                                                             | Yes                          | No                          |
| [Improved Handling of Corrupted Tables](https://docs.percona.com/percona-server/8.4/innodb-corrupt-table-action.html)                                     | Yes                          | No                          |
| [Ability to Kill Idle Transactions](https://docs.percona.com/percona-server/8.4/kill-idle-trx.html)                                                       | Yes                          | No                          |
| [Improvements to START TRANSACTION WITH CONSISTENT SNAPSHOT](https://docs.percona.com/percona-server/8.4/start-transaction-with-consistent-snapshot.html) | Yes                          | No                          |

| Features for Running Database as a Service (DBaaS)                                                   | Percona Server for MySQL 8.4 | MySQL 8.4 Community Edition |
| ---------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------- |
| [Enforce a Specific Storage Engine](https://docs.percona.com/percona-server/8.4/enforce-engine.html) | Yes                          | Yes                         |
