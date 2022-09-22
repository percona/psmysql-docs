# Percona Server for MySQL 8.0.25-15 (2021-07-13)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/8.0/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.25-15
includes all the features and bug fixes available in the
[MySQL 8.0.24 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-24.html) and
the
[MySQL 8.0.25 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-25.html)
in addition to enterprise-grade features developed by Percona.

**NOTE**: The TokuDB Storage Engine was [declared as deprecated](https://www.percona.com/doc/percona-server/8.0/release-notes/Percona-Server-8.0.13-3.html) in Percona Server for MySQL 8.0 and will be disabled in upcoming 8.0 versions.

We recommend migrating to the MyRocks Storage Engine.

For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).

## New Features


* [PS-7182](https://jira.percona.com/browse/PS-7182): Create functionality to expose defined data from procfs for agentless environment


* [PS-7671](https://jira.percona.com/browse/PS-7671): Add rocksdb_allow_unsafe_alter to enable crash unsafe INPLACE ADD|DROP partition


* [PS-7327](https://jira.percona.com/browse/PS-7327): INPLACE ADD|DROP partitions in MyRocks

## Improvements


* [PS-7366](https://jira.percona.com/browse/PS-7366): Add jemalloc memory allocation profiling on PS 8.0

## Bugs Fixed


* [PS-7722](https://jira.percona.com/browse/PS-7722): Multiple-Column Index using Column Prefix Key Parts fails with Index Condition Pushdown in MyRocks


* [PS-7665](https://jira.percona.com/browse/PS-7665): The `performance_schema.metadata_locks m_column_name_length` is uninitialized for MDL_key::FOREIGN_KEY (Upstream [#103532](http://bugs.mysql.com/bug.php?id=103532))


* [PS-7695](https://jira.percona.com/browse/PS-7695): The `Boost` download is no longer available. Using the -DDOWNLOAD_BOOST option with CMake (Thanks to user Benjamin Kuen for reporting this issue).


* [PS-6802](https://jira.percona.com/browse/PS-6802): Configure fails with make-4.3 with CMake Error at storage/rocksdb/CMakeLists.txt:152 (STRING) (Thanks to user Thomas Deutschmann for reporting this issue).


* [PS-7648](https://jira.percona.com/browse/PS-7648): Optimizer switch “favor_range_scan” is not documented


* [PS-7595](https://jira.percona.com/browse/PS-7595): Same version upgrade from PS->PXC needs mysql_upgrade


* [PS-7657](https://jira.percona.com/browse/PS-7657): A server exit caused with an update query on a partition table with a compressed column


* [PS-7557](https://jira.percona.com/browse/PS-7557): Mysql server version 8.0.22-13 executing the Data Masking plugin causes a server exit (Thanks to user Alfonso Luciano for reporting this issue).


* [PS-1116](https://jira.percona.com/browse/PS-1116): LP #1719506: Audit plugin reports “command_class=error” for server-side prepared statements.

## Known issues


* [PS-7787](https://jira.percona.com/browse/PS-7787): Default values for the procfs_files_spec contains entries blocks by SELinux.


* [PS-7788](https://jira.percona.com/browse/PS-7788): Wildcard globbing in procfs_files_spec does not work.


* [PS-7790](https://jira.percona.com/browse/PS-7790): ProcFS access boundary to /proc and /sys can be bypassed with ...
