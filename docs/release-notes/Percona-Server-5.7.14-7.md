# Percona Server for MySQL 5.7.14-7 (2016-08-23)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.14-7 on August 23rd, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.14-7/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.13](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-14.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.14-7 is the current GA release in
the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source and
free, all the details of the release can be found in the [5.7.14-7 milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.14-7)

## New Features

*Percona Server for MySQL* Audit Log Plugin now supports filtering by user, database, and
sql_command.

*Percona Server for MySQL* now supports [tree map file block allocation strategy](https://www.percona.com/blog/2016/08/17/improve-tokudbperconaft-fragmented-data-file-performance/)
for TokuDB.

## Bugs Fixed

Fixed the potential cardinality `0` issue for TokuDB tables if `ANALYZE
TABLE` finds only deleted rows and no actual logical rows before it times
out. Bug fixed [#1607300](https://bugs.launchpad.net/percona-server/+bug/1607300) ([#1006](https://tokutek.atlassian.net/browse/DB-1006), [#732](https://tokutek.atlassian.net/browse/FT-732)).

TokuDB `database.table.index` names longer than 256 characters could cause
server crash if background analyze table status was checked while running. Bug fixed
[#1005](https://tokutek.atlassian.net/browse/DB-1005).

PAM Authentication Plugin would abort authentication while checking UNIX user group
membership if there were more than a thousand members. Bug fixed
[#1608902](https://bugs.launchpad.net/percona-server/+bug/1608902).

If `DROP DATABASE` would fail to delete some of the tables in the database,
the partially-executed command is logged in the binlog as `DROP TABLE t1, t2,
...`  for the tables for which drop succeeded. A slave might fail to
replicate such `DROP TABLE` statement if there exist foreign key
relationships to any of the dropped tables and the slave has a different
schema from master. Fix by checking, on the master, whether any of the
database to be dropped tables participate in a Foreign Key relationship, and
fail the `DROP DATABASE` statement immediately. Bug fixed [#1525407](https://bugs.launchpad.net/percona-server/+bug/1525407)
(upstream [#79610](http://bugs.mysql.com/bug.php?id=79610)).

PAM Authentication Plugin didn’t support spaces in the UNIX user group names. Bug
fixed [#1544443](https://bugs.launchpad.net/percona-server/+bug/1544443).

Due to security reasons `ld_preload` libraries can now only be loaded from
the system directories (`/usr/lib64`, `/usr/lib`) and the *MySQL*
installation base directory.

In the client library, any EINTR received during network I/O was not handled
correctly. Bug fixed [#1591202](https://bugs.launchpad.net/percona-server/+bug/1591202) (upstream [#82019](http://bugs.mysql.com/bug.php?id=82019)).

`SHOW GLOBAL STATUS` was locking more than the upstream implementation which
made it less suitable to be called with high frequency. Bug fixed
[#1592290](https://bugs.launchpad.net/percona-server/+bug/1592290).

The included `.gitignore` in the percona-server source distribution had
a line `\*.spec`, which means someone trying to check in a copy of the
percona-server source would be missing the spec file required to build the
RPMs. Bug fixed [#1600051](https://bugs.launchpad.net/percona-server/+bug/1600051).

Audit Log Plugin did not transcode queries. Bug fixed [#1602986](https://bugs.launchpad.net/percona-server/+bug/1602986).

If the changed page bitmap redo log tracking thread stops due to any reason,
then shutdown will wait for a long time for the log tracker thread to quit,
which it never does. Bug fixed [#1606821](https://bugs.launchpad.net/percona-server/+bug/1606821).

Changed page tracking was initialized too late by InnoDB. Bug fixed
[#1612574](https://bugs.launchpad.net/percona-server/+bug/1612574).

Fixed stack buffer overflow if `--ssl-cipher` had more than 4000
characters. Bug fixed [#1596845](https://bugs.launchpad.net/percona-server/+bug/1596845) (upstream [#82026](http://bugs.mysql.com/bug.php?id=82026)).

Audit Log Plugin events did not report the default database. Bug fixed
[#1435099](https://bugs.launchpad.net/percona-server/+bug/1435099).

Canceling the TokuDB Background ANALYZE TABLE job twice or while it was
in the queue could lead to server assertion. Bug fixed [#1004](https://tokutek.atlassian.net/browse/DB-1004).

Fixed various spelling errors in comments and function names. Bug fixed
[#728](https://tokutek.atlassian.net/browse/FT-728) (*Otto Kekäläinen*)

Implemented a set of fixes to make PerconaFT build and run on the AArch64
(64-bit ARMv8) architecture. Bug fixed [#726](https://tokutek.atlassian.net/browse/FT-726) (*Alexey Kopytov*).

Other bugs fixed: [#1542874](https://bugs.launchpad.net/percona-server/+bug/1542874) (upstream [#80296](http://bugs.mysql.com/bug.php?id=80296)), [#1610242](https://bugs.launchpad.net/percona-server/+bug/1610242),
[#1604462](https://bugs.launchpad.net/percona-server/+bug/1604462) (upstream [#82283](http://bugs.mysql.com/bug.php?id=82283)), [#1604774](https://bugs.launchpad.net/percona-server/+bug/1604774) (upstream
[#82307](http://bugs.mysql.com/bug.php?id=82307)), [#1606782](https://bugs.launchpad.net/percona-server/+bug/1606782), [#1607359](https://bugs.launchpad.net/percona-server/+bug/1607359), [#1607606](https://bugs.launchpad.net/percona-server/+bug/1607606),
[#1607606](https://bugs.launchpad.net/percona-server/+bug/1607606), [#1607671](https://bugs.launchpad.net/percona-server/+bug/1607671), [#1609422](https://bugs.launchpad.net/percona-server/+bug/1609422), [#1610858](https://bugs.launchpad.net/percona-server/+bug/1610858), [#1612551](https://bugs.launchpad.net/percona-server/+bug/1612551),
[#1613663](https://bugs.launchpad.net/percona-server/+bug/1613663), [#1613986](https://bugs.launchpad.net/percona-server/+bug/1613986), [#1455430](https://bugs.launchpad.net/percona-server/+bug/1455430), [#1455432](https://bugs.launchpad.net/percona-server/+bug/1455432), [#1581195](https://bugs.launchpad.net/percona-server/+bug/1581195),
[#998](https://tokutek.atlassian.net/browse/DB-998), [#1003](https://tokutek.atlassian.net/browse/DB-1003), and [#730](https://tokutek.atlassian.net/browse/FT-730).
