# Percona Server for MySQL 8.0.13-3

*Percona* announces the GA release of *Percona Server for MySQL* 8.0.13-3 on December 21, 2018
(downloads are available [here](https://www.percona.com/downloads/Percona-Server-8.0/) and from the [Percona
SoftwareRepositories](https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries)).
This release merges changes of *MySQL* 8.0.13, including all the bug fixes in
it. *Percona Server for MySQL* 8.0.13-3 is now the current GA release in the 8.0
series. All of *Percona*’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the [features available in MySQL 8.0
Community Edition](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html) in addition to
enterprise-grade features developed by Percona.  For a list of
highlighted features from both MySQL 8.0 and Percona Server for MySQL 8.0,
please see the [GA release announcement](https://www.percona.com/blog/2018/12/21/announcing-general-availability-of-percona-server-for-mysql-8-0/).

**NOTE**: If you are upgrading from 5.7 to 8.0, please ensure that you read the
[upgrade guide](https://www.percona.com/doc/percona-server/8.0/upgrading_guide.html) and the
document [Changed in Percona Server for MySQL 8.0](https://www.percona.com/doc/percona-server/8.0/changed_in_version.html).

## Features Removed in Percona Server for MySQL 8.0


* Slow Query Log Rotation and Expiration: Not widely used, can be accomplished
using `logrotate`


* CSV engine mode for standard-compliant quote and comma parsing


* Expanded program option modifiers


* The `ALL_O_DIRECT` InnoDB flush method: it is not compatible with the
new redo logging implementation


* `XTRADB_RSEG` table from `INFORMATION_SCHEMA`


* InnoDB memory size information from `SHOW ENGINE INNODB STATUS;` the
same information is available from Performance Schema memory summary
tables


* Query cache enhancements: The query cache is no longer present in
MySQL 8.0

## Features Being Deprecated in Percona Server for MySQL 8.0


* *TokuDB* Storage Engine: *TokuDB* will be supported throughout the *Percona Server for MySQL* 8.0 release series, but will not be available in the next major
release. *Percona* encourages *TokuDB* users to explore the *MyRocks* Storage
Engine which provides similar benefits for the majority of workloads and has
better optimized support for modern hardware.

## Issues Resolved in *Percona Server for MySQL* 8.0.13-3

### Improvements


* [#5014](https://jira.percona.com/browse/PS-5014): Update Percona Backup Locks feature to use the new `BACKUP_ADMIN`
privilege in MySQL 8.0


* [#4805](https://jira.percona.com/browse/PS-4805): Re-Implemented Compressed Columns with Dictionaries feature in PS 8.0


* [#4790](https://jira.percona.com/browse/PS-4790): Improved accuracy of User Statistics feature

### Bugs Fixed Since 8.0.12-rc1


* Fixed a crash in `mysqldump` in the `--innodb-optimize-keys`
functionality [#4972](https://jira.percona.com/browse/PS-4972)


* Fixed a crash that can occur when system tables are locked by the
user due to a `lock_wait_timeout` [#5134](https://jira.percona.com/browse/PS-5134)


* Fixed a crash that can occur when system tables are locked by the
user from a `SELECT FOR UPDATE` statement [#5027](https://jira.percona.com/browse/PS-5027)


* Fixed a bug that caused `innodb_buffer_pool_size` to be
uninitialized after a restart if it was set using `SET PERSIST` [#5069](https://jira.percona.com/browse/PS-5069)


* Fixed a crash in TokuDB that can occur when a temporary table
experiences an autoincrement rollover [#5056](https://jira.percona.com/browse/PS-5056)


* Fixed a bug where marking an index as invisible would cause a table
rebuild in TokuDB and also in MyRocks [#5031](https://jira.percona.com/browse/PS-5031)


* Fixed a bug where audit logs could get corrupted if the
`audit_log_rotations` was changed during runtime. [#4950](https://jira.percona.com/browse/PS-4950)


* Fixed a bug where `LOCK INSTANCE FOR BACKUP` and
`STOP SLAVE SQL_THREAD` would cause replication to be blocked and
unable to be restarted. [#4758](https://jira.percona.com/browse/PS-4758) (Upstream [#93649](http://bugs.mysql.com/bug.php?id=93649))

Other Bugs Fixed:

[#5155](https://jira.percona.com/browse/PS-5155), [#5139](https://jira.percona.com/browse/PS-5139), [#5057](https://jira.percona.com/browse/PS-5057), [#5049](https://jira.percona.com/browse/PS-5049), [#4999](https://jira.percona.com/browse/PS-4999), [#4971](https://jira.percona.com/browse/PS-4971),
[#4943](https://jira.percona.com/browse/PS-4943), [#4918](https://jira.percona.com/browse/PS-4918), [#4917](https://jira.percona.com/browse/PS-4917), [#4898](https://jira.percona.com/browse/PS-4898), and [#4744](https://jira.percona.com/browse/PS-4744).

## Known Issues

We have a few features and issues outstanding that should be resolved in the
next release.

### Pending Feature Re-Implementations and Improvements


* [#4892](https://jira.percona.com/browse/PS-4892): Re-Implement Expanded Fast Index Creation feature.


* [#5216](https://jira.percona.com/browse/PS-5216): Re-Implement Utility User feature.


* [#5143](https://jira.percona.com/browse/PS-5143): Identify Percona features which can make use of dynamic privileges instead of `SUPER`

### Notable Issues in Features


* [#5148](https://jira.percona.com/browse/PS-5148): Regression in Compressed Columns Feature when using `innodb-force-recovery`


* [#4996](https://jira.percona.com/browse/PS-4996): Regression in User Statistics feature where `TOTAL_CONNECTIONS` field report incorrect data


* [#4933](https://jira.percona.com/browse/PS-4933): Regression in  Slow Query Logging Extensions feature where incorrect transaction idaccounting can cause an assert during certain DDLs.


* [#5206](https://jira.percona.com/browse/PS-5206): TokuDB: A crash can occur in TokuDB when using Native Partioning and the optimizer has `index_merge_union` enabled. Workaround by using `SET SESSION optimizer_switch="index_merge_union=off";`


* [#5174](https://jira.percona.com/browse/PS-5174): MyRocks: Attempting to use unsupported features against MyRocks can lead to a crash rather than an error.


* [#5024](https://jira.percona.com/browse/PS-5024): MyRocks: Queries can return the wrong results on tables with no primary key, non-unique `CHAR`/`VARCHAR` rows, and `UTF8MB4` charset.


* [#5045](https://jira.percona.com/browse/PS-5045): MyRocks: Altering a column or table comment cause the table to be rebuilt

Find the release notes for Percona Server for MySQL 8.0.13-3 in our online documentation. Report bugs in the Jira bug tracker.
