# *Percona Server for MySQL* 5.7.17-11 (2017-02-03)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.17-11 on February 3rd, 2017 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.17-11/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.17](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-17.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.17-11 is the current GA release
in the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source
and free, all the details of the release can be found in the [5.7.17-11
milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.17-11)

## New Features

*Percona Server for MySQL* has implemented support for per-column `VARCHAR/BLOB`
compression for the XtraDB storage engine. This
also features compression dictionary support, to improve compression ratio for
relatively short individual rows, such as JSON data.

The Kill Idle Transactions feature has been re-implemented by setting a
connection socket read timeout value instead of periodically scanning the
internal InnoDB transaction list. This makes the feature applicable to any
transactional storage engine, such as TokuDB, and, in future, MyRocks.
This re-implementation is also addressing some existing bugs, including server
crashes: [#1166744](https://bugs.launchpad.net/percona-server/+bug/1166744), [#1179136](https://bugs.launchpad.net/percona-server/+bug/1179136), [#907719](https://bugs.launchpad.net/percona-server/+bug/907719), and [#1369373](https://bugs.launchpad.net/percona-server/+bug/1369373).

## Bugs Fixed

Logical row counts for TokuDB tables could get inaccurate over time. Bug
fixed [#1651844](https://bugs.launchpad.net/percona-server/+bug/1651844) ([#732](https://tokutek.atlassian.net/browse/FT-732)).

Repeated execution of `SET STATEMENT ... FOR <SELECT FROM view>` could lead
to a server crash. Bug fixed [#1392375](https://bugs.launchpad.net/percona-server/+bug/1392375).

`CREATE TEMPORARY TABLE` would create a transaction in binary log on a read
only server. Bug fixed [#1539504](https://bugs.launchpad.net/percona-server/+bug/1539504) (upstream [#83003](http://bugs.mysql.com/bug.php?id=83003)).

Using Per-query variable statement with subquery temporary tables could
cause a memory leak. Bug fixed [#1635927](https://bugs.launchpad.net/percona-server/+bug/1635927).

Fixed new compilation warnings with GCC 6. Bugs fixed [#1641612](https://bugs.launchpad.net/percona-server/+bug/1641612) and
[#1644183](https://bugs.launchpad.net/percona-server/+bug/1644183).

A server could crash if a bitmap write I/O error happens in the background log
tracking thread while a `FLUSH CHANGED_PAGE_BITMAPS` is executing
concurrently. Bug fixed [#1651656](https://bugs.launchpad.net/percona-server/+bug/1651656).

TokuDB was using wrong function to calculate free space in data files. Bug
fixed [#1656022](https://bugs.launchpad.net/percona-server/+bug/1656022) ([#1033](https://tokutek.atlassian.net/browse/DB-1033)).

`CONCURRENT_CONNECTIONS` column in the `USER_STATISTICS` table was
showing incorrect values. Bug fixed [#728082](https://bugs.launchpad.net/percona-server/+bug/728082).

Audit Log Plugin when set to `JSON` format was not escaping
characters properly. Bug fixed [#1548745](https://bugs.launchpad.net/percona-server/+bug/1548745).

InnoDB index dives did not detect some of the concurrent tree changes, which
could return bogus estimates. Bug fixed [#1625151](https://bugs.launchpad.net/percona-server/+bug/1625151) (upstream
[#84366](http://bugs.mysql.com/bug.php?id=84366)).

`INFORMATION_SCHEMA.INNODB_CHANGED_PAGES` queries would needlessly read
potentially incomplete bitmap data past the needed LSN range. Bug fixed
[#1625466](https://bugs.launchpad.net/percona-server/+bug/1625466).

*Percona Server for MySQL* `cmake` compiler would always attempt to build *RocksDB*
even if `-DWITHOUT_ROCKSDB=1` argument was specified. Bug fixed
[#1638455](https://bugs.launchpad.net/percona-server/+bug/1638455).

Lack of free pages in the buffer pool is not diagnosed with `innodb_empty_free_list_algorithm` set to `backoff` (which is the
default). Bug fixed [#1657026](https://bugs.launchpad.net/percona-server/+bug/1657026).

`mysqld_safe` now limits the use of `rm` and `chown` to avoid privilege
escalation. `chown` can now be used only for `/var/log` directory. Bug
fixed [#1660265](https://bugs.launchpad.net/percona-server/+bug/1660265). Thanks to Dawid Golunski ([https://legalhackers.com](https://legalhackers.com)).

Renaming a TokuDB table to a non-existent database with `tokudb_dir_per_db`
enabled would lead to a server crash. Bug fixed
[#1030](https://tokutek.atlassian.net/browse/DB-1030).

Read Free Replication optimization could not be used for
TokuDB partition tables. Bug fixed [#1012](https://tokutek.atlassian.net/browse/DB-1012).

Other bugs fixed: [#1486747](https://bugs.launchpad.net/percona-server/+bug/1486747), [#1617715](https://bugs.launchpad.net/percona-server/+bug/1617715), [#1633988](https://bugs.launchpad.net/percona-server/+bug/1633988),
[#1638198](https://bugs.launchpad.net/percona-server/+bug/1638198) (upstream [#82823](http://bugs.mysql.com/bug.php?id=82823)), [#1642230](https://bugs.launchpad.net/percona-server/+bug/1642230), [#1646384](https://bugs.launchpad.net/percona-server/+bug/1646384),
[#1640810](https://bugs.launchpad.net/percona-server/+bug/1640810), [#1647530](https://bugs.launchpad.net/percona-server/+bug/1647530), [#1651121](https://bugs.launchpad.net/percona-server/+bug/1651121), [#1658843](https://bugs.launchpad.net/percona-server/+bug/1658843), [#1156772](https://bugs.launchpad.net/percona-server/+bug/1156772),
[#1644583](https://bugs.launchpad.net/percona-server/+bug/1644583), [#1648389](https://bugs.launchpad.net/percona-server/+bug/1648389), [#1648737](https://bugs.launchpad.net/percona-server/+bug/1648737), [#1650256](https://bugs.launchpad.net/percona-server/+bug/1650256), and
[#1647723](https://bugs.launchpad.net/percona-server/+bug/1647723).
