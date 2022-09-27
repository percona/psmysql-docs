# Percona Server for MySQL 5.7.10-1 (2015-12-14)

Percona is glad to announce the first Release Candidate release of *Percona Server for MySQL* 5.7.10-1 on December 14th, 2015 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.10-1rc1/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.10](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-10.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.10-1 is the current Release
Candidate release in the *Percona Server for MySQL* 5.7 series. All of Percona’s
software is open-source and free, all the details of the release can be found
in the [5.7.10-1 milestone at Launchpad](https://launchpad.net/percona-server/+milestone/5.7.10-1rc1)

This release contains all the bug fixes from the latest *Percona Server for MySQL* 5.6
release (currently *Percona Server for MySQL* [5.6.27-76.0](http://www.percona.com/doc/percona-server/5.6/release-notes/Percona-Server-5.6.27-76.0.html)).

## New Features

* Percona Server for MySQL* 5.7.10-1 is not available on either the *RHEL* 5 family of Linux distributions or *Debian* 6 (squeeze).

A complete list of the changes between *Percona Server for MySQL* 5.6 and 5.7 can be found in [Changed in Percona Server 5.7](/changed_in_57.md).

## Known issues

[MeCab Full-Text Parser Plugin](https://dev.mysql.com/doc/refman/5.7/en/fulltext-search-mecab.html)  has not been included in this release.

PAM Authentication Plugin currently isn’t working correctly.

The following variables do not work correctly:

* `innodb_show_verbose_locks`

* `innodb_show_locks_held`


In *Percona Server for MySQL* 5.7 [`super_read_only`](https://www.percona.com/doc/percona-server/5.6/management/super_read_only.html) feature has been replaced with upstream implementation. There are currently two known issues compared to *Percona Server for MySQL* 5.6 implementation:

* Bug [#78963](http://bugs.mysql.com/bug.php?id=78963): If the `relay_log_info_repository`= TABLE, using`super_read_only`aborts the `STOP SLAVE` and could lead to a server crash in debug builds.
* Bug [#79328](http://bugs.mysql.com/bug.php?id=79328), passing `super_read_only` as a server option has no effect. 

Using a primary key with a `BLOB` in the TokuDB table could lead to a server crash ([#916](https://tokutek.atlassian.net/browse/DB-916)).

Using XA transactions with TokuDB could lead to a server crash([#900](https://tokutek.atlassian.net/browse/DB-900)).

Percona TokuBackup has not been included in this release.

## Bugs Fixed

Running `ALTER TABLE` without specifying the storage engine (without `ENGINE=` clause) or `OPTIMIZE TABLE` when `enforce_storage_engine` was enabled could lead to unrequested and unexpected storage engine changes. If done for a system table, it would circumvent regular system table storage engine compatibility checks, resulting in crashes or otherwise broken server operation. Bug fixed [#1488055](https://bugs.launchpad.net/percona-server/+bug/1488055).

Some transaction deadlocks did not increase the `INFORMATION_SCHEMA.INNODB_METRICS` `lock_deadlocks` counter. Bug fixed [#1466414](https://bugs.launchpad.net/percona-server/+bug/1466414) (upstream [#77399](http://bugs.mysql.com/bug.php?id=77399)).

Removed excessive locking during the buffer pool resize when checking whether
AHI is enabled. Bug fixed [#1525215](https://bugs.launchpad.net/percona-server/+bug/1525215) (upstream [#78894](http://bugs.mysql.com/bug.php?id=78894)).

Removed unnecessary code in the InnoDB error monitor thread. Bug fixed
[#1521564](https://bugs.launchpad.net/percona-server/+bug/1521564) (upstream [#79477](http://bugs.mysql.com/bug.php?id=79477)).

With Expanded Fast Index Creation enabled, DDL queries involving InnoDB temporary tables would cause later queries on the same tables to produce warnings that their indexes were not found in the index translation table. Bug fixed [#1233431](https://bugs.launchpad.net/percona-server/+bug/1233431).

Other bugs fixed: [#371752](https://bugs.launchpad.net/percona-server/+bug/371752) (upstream [#45379](http://bugs.mysql.com/bug.php?id=45379)), [#1441362](https://bugs.launchpad.net/percona-server/+bug/1441362)
(upstream [#56155](http://bugs.mysql.com/bug.php?id=56155)), [#1385062](https://bugs.launchpad.net/percona-server/+bug/1385062) (upstream [#74810](http://bugs.mysql.com/bug.php?id=74810)),
[#1519201](https://bugs.launchpad.net/percona-server/+bug/1519201) (upstream [#79391](http://bugs.mysql.com/bug.php?id=79391)), [#1515602](https://bugs.launchpad.net/percona-server/+bug/1515602), [#1506697](https://bugs.launchpad.net/percona-server/+bug/1506697)
(upstream [#57552](http://bugs.mysql.com/bug.php?id=57552)), [#1501089](https://bugs.launchpad.net/percona-server/+bug/1501089) (upstream [#75239](http://bugs.mysql.com/bug.php?id=75239)),
[#1447527](https://bugs.launchpad.net/percona-server/+bug/1447527) (upstream [#75368](http://bugs.mysql.com/bug.php?id=75368)), [#1384658](https://bugs.launchpad.net/percona-server/+bug/1384658) (upstream
[#74619](http://bugs.mysql.com/bug.php?id=74619)), [#1384656](https://bugs.launchpad.net/percona-server/+bug/1384656) (upstream [#74584](http://bugs.mysql.com/bug.php?id=74584)), and
[#1192052](https://bugs.launchpad.net/percona-server/+bug/1192052).
