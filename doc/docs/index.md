
# *Percona Server for MySQL* 5.7 - Documentation

Percona Server for MySQL is a free, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior performance, scalability, and instrumentation.

Percona Server for MySQL is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads. It delivers higher value to MySQL server users with optimized performance, greater performance scalability and availability, enhanced backups, and increased visibility.

## Introduction


* [The *Percona XtraDB* Storage Engine](percona_xtradb.md)


* [List of features available in Percona Server for MySQL releases](ps-versions-comparison.md)


* [*Percona Server for MySQL* Feature Comparison](feature_comparison.md)


* [Changed in Percona Server 5.7](changed_in_57.md)


## Installation


* [Installing *Percona Server for MySQL* 5.7](installation.md)


    * [Installing *Percona Server for MySQL* from Repositories](installation.md#)
  
    * [Installing *Percona Server for MySQL* on *Debian* and *Ubuntu*](installation/apt_repo.md)

    * [Installing *Percona Server for MySQL* on *Red Hat* EnterpriseLinux and *CentOS*](installation/yum.md)

    * [Installing *Percona Server for MySQL* from a Binary Tarball](installation/binary-tarball.md)


    * [Installing *Percona Server for MySQL* from a Source Tarball](installation/source-tarball.md)


    * [Installing *Percona Server for MySQL* from the Git Source Tree](installation/git-source-tree.md)


    * [Compiling *Percona Server for MySQL* from Source](installation/compile.md)



* Percona Server In-Place Upgrading Guide: From 5.6 to 5.7

    * [Upgrading Guide](upgrading_guide_56_57.md)
  
    * [Upgrading using the Percona repositories](upgrade-repos.md)

    * [Upgrading using Standalone Packages](upgrade-standalone.md)

    * [Upgrading a Distribution upgrade in-place on a system with 
      installed Percona packages](upgrade-distribution.md)
  
    * Post-Installation(installation-post-installation)

   
## Scalability


* [Improved Buffer Pool Scalability](scalability/innodb_split_buf_pool_mutex.md)


* [Improved InnoDB I/O Scalability](scalability/innodb_io.md)


## Performance


* [Multiple page asynchronous I/O requests](performance/aio_page_requests.md)


* [Query Cache Enhancements](/performance/query_cache_enhance.md)


* [Limiting the Estimation of Records in a Query](performance/query_limit_records.md)


* [Improved NUMA support](performance/innodb_numa_support.md)


* [Thread Pool](performance/threadpool.md)


* [XtraDB Performance Improvements for I/O-Bound Highly-Concurrent 
  Workloads](performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.md)


* [Prefix Index Queries Optimization](performance/prefix_index_queries_optimization.md)


## Flexibility Improvements


* Suppress Warning Messages


* `Improved MEMORY` Storage Engine


* Restricting the number of binlog files


* Extended `mysqldump`


* Extended `SELECT INTO OUTFILE/DUMPFILE`


* Per-query variable statement


* Extended `mysqlbinlog`


* Slow Query Log Rotation and Expiration


* CSV engine mode for standard-compliant quote and comma parsing


* Support for PROXY protocol


* Per-session server-id


* Compressed columns with dictionaries


* InnoDB Full-Text Search improvements


* Binlogging and replication improvements


## Reliability Improvements


* Too Many Connections Warning


* Handle Corrupted Tables


## Management Improvements


* *Percona Toolkit* UDFs


* Kill Idle Transactions


* Enforcing Storage Engine


* Utility user


* Expanded Program Option Modifiers


* XtraDB changed page tracking


* PAM Authentication Plugin


* Expanded Fast Index Creation


* Backup Locks


* Audit Log Plugin


* Start transaction with consistent snapshot


* Extended `SHOW GRANTS`


* SSL Improvements


* Utility user


* PS-Admin script


## Security Improvements


* Data at Rest Encryption


* Vault Keyring Plugin


* Data Masking


* SSL Improvements


* PAM Authentication Plugin


## Diagnostics Improvements


* User Statistics


* Slow Query Log


* Extended Show Engine InnoDB Status


* Show Storage Engines


* Process List


* Misc. INFORMATION_SCHEMA Tables


* Thread Based Profiling


* Metrics for scalability measurement


* Response Time Distribution


* InnoDB Page Fragmentation Counters


* Using libcoredumper


* Stack Trace


## TokuDB


* TokuDB Introduction


* TokuDB Installation


* Using TokuDB


* Fast Updates with TokuDB


* TokuDB files and file types


* TokuDB file management


* TokuDB Background ANALYZE TABLE


* TokuDB Variables


* TokuDB Status Variables


* TokuDB Fractal Tree Indexing


* TokuDB Troubleshooting


* TokuDB Performance Schema Integration


* Percona TokuBackup


* Frequently Asked Questions


* Removing TokuDB storage engine


## Percona MyRocks


* Introduction


* Installation


* Limitations


* Differences

* Information Schema tables 


* Server Variables


* Status Variables


* Gap locks detection


* Data Loading


## Reference


* List of upstream MySQL bugs fixed in *Percona Server for MySQL*  5.7


* List of variables introduced in Percona Server 5.7


* Development of *Percona Server for MySQL*


* Trademark Policy


* Index of `INFORMATION_SCHEMA` Tables


* Frequently Asked Questions


* Copyright and Licensing Information


* *Percona Server for MySQL* 5.7 Release notes


* Glossary



* Index


* Module Index
