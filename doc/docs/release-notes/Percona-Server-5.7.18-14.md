# *Percona Server for MySQL* 5.7.18-14 (2017-05-12)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.18-14 on May 12, 2017 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.18-14/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.18](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-18.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.18-14 is the current GA release
in the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source
and free, all the details of the release can be found in the [5.7.18-14
milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.18-14)

## New Features

*Percona Server for MySQL* 5.7 packages are now available for Ubuntu 17.04 (*Zesty
Zapus*).

*Percona Server for MySQL* now supports Prefix Index Queries Optimization. This feature was ported from a Facebook MySQL patch.

*Percona Server for MySQL* has implemented support for Gap locks detection for
transactional storage engines, like *MyRocks*, that do not support gap locks.
This feature was ported from a Facebook MySQL patch.

`tokudb_dir_cmd` can now be used to edit the TokuDB directory map. This feature is
currently considered Experimental.

## Bugs Fixed

A deadlock could occur in I/O-bound workloads when the server was using several
small buffer pool instances in combination with small redo log files and
variable 

`innodb_empty_free_list_algorithm` set to `backoff`
algorithm. Bug fixed  [#1651657](https://bugs.launchpad.net/percona-server/+bug/1651657).

Fixed a memory leak in Percona TokuBackup. Bug fixed [#1669005](https://bugs.launchpad.net/percona-server/+bug/1669005).

Compressed columns with dictionaries could not be added to a partitioned table by using
`ALTER TABLE`. Bug fixed [#1671492](https://bugs.launchpad.net/percona-server/+bug/1671492).

Fixed a memory leak that happened in case of a failure to create
a multi-threaded slave worker thread. Bug fixed [#1675716](https://bugs.launchpad.net/percona-server/+bug/1675716).

In-Place upgrade from *Percona Server for MySQL* 5.6 to 5.7 by using standalone packages
would fail if `/var/lib/mysql` wasn’t defined as the `datadir`. Bug fixed [#1687276](https://bugs.launchpad.net/percona-server/+bug/1687276).

A combination of using any audit API-using plugin, like Audit Log Plugin
and Response Time Distribution, with multi-byte collation connection
and a `PREPARE` statement with a parse error could lead to a server crash. Bug
fixed [#1688698](https://bugs.launchpad.net/percona-server/+bug/1688698) (upstream [#86209](http://bugs.mysql.com/bug.php?id=86209)).

Fix for a [#1433432](https://bugs.launchpad.net/percona-server/+bug/1433432) bug that caused a performance regression due to suboptimal
LRU manager thread flushing heuristics. Bug fixed [#1631309](https://bugs.launchpad.net/percona-server/+bug/1631309).

Creating Compressed columns with dictionaries in MyISAM tables by specifying partition
engines would not result in an error. Bug fixed [#1631954](https://bugs.launchpad.net/percona-server/+bug/1631954).

It was not possible to configure basedir as a symlink. Bug fixed
[#1639735](https://bugs.launchpad.net/percona-server/+bug/1639735).

Replication slave did not report `Seconds_Behind_Master` correctly when
running in multi-threaded slave mode. Bug fixed [#1654091](https://bugs.launchpad.net/percona-server/+bug/1654091)
(upstream [#84415](http://bugs.mysql.com/bug.php?id=84415)).

`DROP TEMPORARY TABLE` would create a transaction in binary log on a
read-only server. Bug fixed [#1668602](https://bugs.launchpad.net/percona-server/+bug/1668602) (upstream [#85258](http://bugs.mysql.com/bug.php?id=85258)).

Processing GTIDs in the relay log that were already been executed were causing
write/fsync amplification. Bug fixed [#1669928](https://bugs.launchpad.net/percona-server/+bug/1669928) (upstream
[#85141](http://bugs.mysql.com/bug.php?id=85141)).

Text/BLOB fields were not handling sorting of the empty string consistently
between InnoDB and filesort. Bug fixed [#1674867](https://bugs.launchpad.net/percona-server/+bug/1674867) (upstream
[#81810](http://bugs.mysql.com/bug.php?id=81810)) by porting a Facebook patch for MySQL.

InnoDB adaptive hash index was using a partitioning algorithm that would
produce uneven distribution when the server contained many tables with an
identical schema. Bug fixed [#1679155](https://bugs.launchpad.net/percona-server/+bug/1679155) (upstream [#81814](http://bugs.mysql.com/bug.php?id=81814)).

For plugin variables that are signed numbers, doing a `SHOW VARIABLES` would
always show an unsigned number. Fixed by porting a Facebook patch for MySQL.

Other bugs fixed: [#1629250](https://bugs.launchpad.net/percona-server/+bug/1629250) (upstream [#83245](http://bugs.mysql.com/bug.php?id=83245)), [#1660828](https://bugs.launchpad.net/percona-server/+bug/1660828)
(upstream [#84786](http://bugs.mysql.com/bug.php?id=84786)), [#1664519](https://bugs.launchpad.net/percona-server/+bug/1664519) (upstream [#84940](http://bugs.mysql.com/bug.php?id=84940)),
[#1674299](https://bugs.launchpad.net/percona-server/+bug/1674299), [#1670588](https://bugs.launchpad.net/percona-server/+bug/1670588) (upstream [#84173](http://bugs.mysql.com/bug.php?id=84173)), [#1672389](https://bugs.launchpad.net/percona-server/+bug/1672389),
[#1674507](https://bugs.launchpad.net/percona-server/+bug/1674507), [#1675623](https://bugs.launchpad.net/percona-server/+bug/1675623), [#1650294](https://bugs.launchpad.net/percona-server/+bug/1650294), [#1659224](https://bugs.launchpad.net/percona-server/+bug/1659224), [#1662908](https://bugs.launchpad.net/percona-server/+bug/1662908),
[#1669002](https://bugs.launchpad.net/percona-server/+bug/1669002), [#1671473](https://bugs.launchpad.net/percona-server/+bug/1671473), [#1673800](https://bugs.launchpad.net/percona-server/+bug/1673800), [#1674284](https://bugs.launchpad.net/percona-server/+bug/1674284), [#1676441](https://bugs.launchpad.net/percona-server/+bug/1676441),
[#1676705](https://bugs.launchpad.net/percona-server/+bug/1676705), [#1676847](https://bugs.launchpad.net/percona-server/+bug/1676847) (upstream [#85671](http://bugs.mysql.com/bug.php?id=85671)), [#1677130](https://bugs.launchpad.net/percona-server/+bug/1677130)
(upstream [#85678](http://bugs.mysql.com/bug.php?id=85678)), [#1677162](https://bugs.launchpad.net/percona-server/+bug/1677162), [#1677943](https://bugs.launchpad.net/percona-server/+bug/1677943), [#1678692](https://bugs.launchpad.net/percona-server/+bug/1678692),
[#1680510](https://bugs.launchpad.net/percona-server/+bug/1680510) (upstream [#85838](http://bugs.mysql.com/bug.php?id=85838)), [#1683993](https://bugs.launchpad.net/percona-server/+bug/1683993), [#1684012](https://bugs.launchpad.net/percona-server/+bug/1684012),
[#1684078](https://bugs.launchpad.net/percona-server/+bug/1684078), [#1684264](https://bugs.launchpad.net/percona-server/+bug/1684264), [#1687386](https://bugs.launchpad.net/percona-server/+bug/1687386), [#1687432](https://bugs.launchpad.net/percona-server/+bug/1687432), [#1687600](https://bugs.launchpad.net/percona-server/+bug/1687600),
and [#1674281](https://bugs.launchpad.net/percona-server/+bug/1674281).
