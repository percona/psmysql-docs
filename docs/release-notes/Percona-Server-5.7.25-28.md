# Percona Server for MySQL 5.7.25-28 (2019-02-18)

Percona is glad to announce the release of *Percona Server for MySQL* 5.7.25-28 on
February 18, 2019. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.25-28/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.25](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-25.html) and includes
all the bug fixes in it. *Percona Server for MySQL* 5.7.25-28 is now the current GA
(Generally Available) release in the 5.7 series.

All software developed by Percona is open-source and free.

In this release, *Percona Server for MySQL* introduces the variable `binlog_skip_flush_commands`. This variable controls whether or not `FLUSH` commands are written to the binary log. Setting this variable to **ON** can help avoid problems in replication. For more information, see Writing FLUSH Commands to the Binary Log.

!!! note

    If you’re currently using *Percona Server for MySQL* 5.7, Percona recommends upgrading to this version of 5.7 prior to upgrading to *Percona Server for MySQL* 8.0.

## Bugs Fixed

* FLUSH commands written to the binary log could cause errors in case
of replication. Bug fixed [#1827](https://jira.percona.com/browse/PS-1827): (upstream `88720`).

* Running LOCK TABLES FOR BACKUP followed by STOP SLAVE SQL_THREAD
could block replication preventing it from being restarted
normally. Bug fixed [#4758](https://jira.percona.com/browse/PS-4758).

* The `ACCESS_DENIED` field of the
information_schema.user_statistics table was not updated
correctly. Bug fixed [#3956](https://jira.percona.com/browse/PS-3956).

* MySQL could report that the maximum number of connections was
exceeded with too many connections being in the CLOSE_WAIT state. Bug
fixed [#4716](https://jira.percona.com/browse/PS-4716) (upstream [#92108](http://bugs.mysql.com/bug.php?id=92108))

* Wrong query results could be received in semi-join sub queries with
materialization-scan that allowed inner tables of different
semi-join nests to interleave. Bug fixed [#4907](https://jira.percona.com/browse/PS-4907) (upstream bug
[#92809](http://bugs.mysql.com/bug.php?id=92809)).

* In some cases, the server using the MyRocks storage engine could crash
when TTL (Time to Live) was defined on a table. Bug fixed [#4911](https://jira.percona.com/browse/PS-4911).

* Running the SELECT statement with the ORDER BY and
LIMIT clauses could result in a less than optimal performance. Bug
fixed [#4949](https://jira.percona.com/browse/PS-4949) (upstream [#92850](http://bugs.mysql.com/bug.php?id=92850))

* There was a typo in `mysqld_safe.sh`: **trottling** was replaced
with **throttling**. Bug fixed [#240](https://jira.percona.com/browse/PS-240). Thanks to Michael
Coburn for the patch.

* MyRocks could crash while running `START TRANSACTION WITH
CONSISTENT SNAPSHOT` if other transactions were in specific
states. Bug fixed [#4705](https://jira.percona.com/browse/PS-4705).

* In some cases, `mysqld` could crash when inserting data into a
database the name of which contained special characters (CVE-2018-20324). Bug fixed
[#5158](https://jira.percona.com/browse/PS-5158).

* MyRocks incorrectly processed transactions in which multiple
statements had to be rolled back.  Bug fixed [#5219](https://jira.percona.com/browse/PS-5219).

* In some cases, the MyRocks storage engine could crash without triggering the
crash recovery. Bug fixed [#5366](https://jira.percona.com/browse/PS-5366).

* When bootstrapped with undo or redo log encryption enabled on a very fast
storage, the server could fail to start. Bug fixed [#4958](https://jira.percona.com/browse/PS-4958).

* Some fields in the output of `SHOW USER_STATISTICS` command did
not contain correct information. Bug fixed [#4996](https://jira.percona.com/browse/PS-4996).

Other bugs fixed:
[#2455](https://jira.percona.com/browse/PS-2455),
[#4791](https://jira.percona.com/browse/PS-4791),
[#4855](https://jira.percona.com/browse/PS-4855),
[#5268](https://jira.percona.com/browse/PS-5268).

This release also contains fixes for the following CVE issues:
CVE-2019-2534,
CVE-2019-2529,
CVE-2019-2482,
CVE-2019-2434.