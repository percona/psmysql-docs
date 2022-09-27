# Percona Server for MySQL 5.7.10-2 (2016-02-05)

Percona is glad to announce the second Release Candidate release of *Percona Server for MySQL* 5.7.10-2 on February 5th, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.10-2rc2/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.10](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-10.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.10-2 is the current Release
Candidate release in the *Percona Server for MySQL* 5.7 series. All of Percona’s
software is open-source and free, all the details of the release can be found
in the [5.7.10-2 milestone at Launchpad](https://launchpad.net/percona-server/+milestone/5.7.10-2rc2)

## New Features

A complete list of changes between *Percona Server for MySQL* 5.6 and 5.7 can be seen in Changed in Percona Server 5.7.

The 5.7 binlog group commit algorithm is now supported in TokuDB as well.

New TokuDB index statistics reporting has been implemented to be compatible with the changes implemented in upstream 5.7. Following the InnoDB example, the default value for `tokudb_cardinality_scale_percent` has been changed from `50%` to `100%`. Implementing this feature also addresses a server crash deep in the optimizer code.

## Known Issues

In *Percona Server for MySQL* 5.7 [super_read_only](https://www.percona.com/doc/percona-server/5.6/management/super_read_only.html) feature has been replaced with upstream implementation. There are currently two known issues compared to *Percona Server for MySQL* 5.6 implementation:

* Bug [#78963](http://bugs.mysql.com/bug.php?id=78963), `super_read_only` aborts `STOP SLAVE` if `relay_log_info_repository` is set to `TABLE` which could lead to a server crash in Debug builds.


* Bug [#79328](http://bugs.mysql.com/bug.php?id=79328), `super_read_only` set as a server option has no effect. InnoDB crash recovery might fail if `innodb_flush_method` is set to `ALL_O_DIRECT`. The workaround is to set this variable to a different value before starting up the crashed instance (bug [#1529885](https://bugs.launchpad.net/percona-server/+bug/1529885)).

## Bugs Fixed

Clustering secondary index could not be created on a partitioned TokuDB table. Bug fixed [#1527730](https://bugs.launchpad.net/percona-server/+bug/1527730) ([#720](https://tokutek.atlassian.net/browse/DB-720)).

Percona TokuBackup was failing to compile with *Percona Server for MySQL* 5.7. Bug fixed [#123](https://tokutek.atlassian.net/browse/BACKUP-123).

Granting privileges to a user authenticating with PAM Authentication Plugin could lead to a server crash. Bug fixed [#1521474](https://bugs.launchpad.net/percona-server/+bug/1521474).
TokuDB status variables were missing from *Percona Server for MySQL* `5.7.10-1`.
Bug fixed [#1527364](https://bugs.launchpad.net/percona-server/+bug/1527364) ([#923](https://tokutek.atlassian.net/browse/DB-923)).

Attempting to rotate the audit log file would result in the audit log file name`foo.log.%u` (literally) instead of a numeric suffix. Bug fixed[#1528603](https://bugs.launchpad.net/percona-server/+bug/1528603).

Adding an index to an InnoDB temporary table while `expand_fast_index_creation`
was enabled could lead to server assertion. Bug fixed [#1529555](https://bugs.launchpad.net/percona-server/+bug/1529555).

TokuDB would not be upgraded on *Debian*/*Ubuntu* distributions while performing an upgrade from *Percona Server for MySQL* 5.6 to *Percona Server for MySQL* 5.7 even if explicitly requested. Bug fixed [#1533580](https://bugs.launchpad.net/percona-server/+bug/1533580).

The server would assert when both TokuDB and InnoDB tables were used within one transaction on a replication slave which has binary log enabled and slave updates logging disabled. Bug fixed [#1534249](https://bugs.launchpad.net/percona-server/+bug/1534249) (upstream bug [#80053](http://bugs.mysql.com/bug.php?id=80053)).

[MeCab Full-Text Parser Plugin](https://dev.mysql.com/doc/refman/5.7/en/fulltext-search-mecab.html) has not been included in the previous release. Bug fixed [#1534617](https://bugs.launchpad.net/percona-server/+bug/1534617).

Fixed server assertion caused by `Performance Schema` memory key mix-up in
`SET STATEMENT ... FOR ...` statements. Bug fixed [#1534874](https://bugs.launchpad.net/percona-server/+bug/1534874).

The service name on *CentOS* 6 has been renamed from `mysqld` back to `mysql`.This change requires a manual service restart after being upgraded from *Percona Server for MySQL* `5.7.10-1`

Bug fixed [#1542332](https://bugs.launchpad.net/percona-server/+bug/1542332).
Setting the `innodb_sched_priority_purge` (available only in debug builds) while purge threads were stopped would cause a server crash. Bug fixed [#1368552](https://bugs.launchpad.net/percona-server/+bug/1368552).

Enabling TokuDB with the `ps_tokudb_admin` script inside the Docker container
would cause an error due to insufficient privileges even when running as root.
In order for this script to be used inside docker containers, this error has
been changed to a warning that a check is impossible. Bug fixed [#1520890](https://bugs.launchpad.net/percona-server/+bug/1520890).

Write-heavy workload with a small buffer pool could lead to a deadlock when free buffers are exhausted. Bug fixed [#1521905](https://bugs.launchpad.net/percona-server/+bug/1521905).

InnoDB status will start printing negative values for spin rounds per wait, if the wait number, even though being accounted as a signed 64-bit integer, will not fit into a signed 32-bit integer. Bug fixed [#1527160](https://bugs.launchpad.net/percona-server/+bug/1527160) (upstream[#79703](http://bugs.mysql.com/bug.php?id=79703)).

*Percona Server for MySQL* 5.7 couldn’t be restarted after TokuDB has been installed with the `ps_tokudb_admin` script. Bug fixed [#1527535](https://bugs.launchpad.net/percona-server/+bug/1527535).

Fixed memory leak when `utility_user`is enabled. Bug fixed
[#1530918](https://bugs.launchpad.net/percona-server/+bug/1530918).

Page cleaner worker threads were not instrumented for `Performance Schema`. Bug fixed [#1532747](https://bugs.launchpad.net/percona-server/+bug/1532747) (upstream bug [#79894](http://bugs.mysql.com/bug.php?id=79894)).

The busy server was preferring LRU flushing over flush list flushing too strongly which could lead to performance degradation. Bug fixed [#1534114](https://bugs.launchpad.net/percona-server/+bug/1534114).

`libjemalloc.so.1` was missing from the binary tarball. Bug fixed [#1537129](https://bugs.launchpad.net/percona-server/+bug/1537129).

When `cmake/make/make_binary_distribution` workflow was used to produce binary tarballs it would produce tarballs with `mysql-...` naming instead of
`percona-server-...`. Bug fixed [#1540385](https://bugs.launchpad.net/percona-server/+bug/1540385).

Added proper memory cleanup if for some reason a table is unable to be opened from a dead closed state. This prevents an assertion from happening the next time the table is attempted to be opened. Bug fixed [#917](https://tokutek.atlassian.net/browse/DB-917).

The variable `tokudb_support_xa` has been modified to prevent setting it to anything but `ON`/`ENABLED` and to print a SQL warning anytime an attempt is made to change it, just like `innodb_support_xa`. Bug fixed [#928](https://tokutek.atlassian.net/browse/DB-928).

Other bugs fixed: [#1179451](https://bugs.launchpad.net/percona-server/+bug/1179451), [#1534246](https://bugs.launchpad.net/percona-server/+bug/1534246), [#1524763](https://bugs.launchpad.net/percona-server/+bug/1524763),
[#1525109](https://bugs.launchpad.net/percona-server/+bug/1525109) (upstream [#79569](http://bugs.mysql.com/bug.php?id=79569)), [#1530102](https://bugs.launchpad.net/percona-server/+bug/1530102), [#897](https://tokutek.atlassian.net/browse/DB-897),
[#898](https://tokutek.atlassian.net/browse/DB-898), [#899](https://tokutek.atlassian.net/browse/DB-899), [#900](https://tokutek.atlassian.net/browse/DB-900), [#901](https://tokutek.atlassian.net/browse/DB-901), [#902](https://tokutek.atlassian.net/browse/DB-902),
[#903](https://tokutek.atlassian.net/browse/DB-903), [#905](https://tokutek.atlassian.net/browse/DB-905), [#906](https://tokutek.atlassian.net/browse/DB-906), [#907](https://tokutek.atlassian.net/browse/DB-907), [#908](https://tokutek.atlassian.net/browse/DB-908),
[#909](https://tokutek.atlassian.net/browse/DB-909), [#910](https://tokutek.atlassian.net/browse/DB-910), [#911](https://tokutek.atlassian.net/browse/DB-911), [#912](https://tokutek.atlassian.net/browse/DB-912), [#913](https://tokutek.atlassian.net/browse/DB-913),
[#915](https://tokutek.atlassian.net/browse/DB-915), [#919](https://tokutek.atlassian.net/browse/DB-919), and [#904](https://tokutek.atlassian.net/browse/DB-904).
