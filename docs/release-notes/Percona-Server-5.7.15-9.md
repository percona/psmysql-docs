# Percona Server for MySQL 5.7.15-9 (2016-10-21)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.15-9 on October 21st, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.15-9/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.15](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-15.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.15-9 is the current GA release in
the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source and
free, all the details of the release can be found in the [5.7.15-9 milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.15-9)

## New Features

A new TokuDB `tokudb_dir_per_db` option has been introduced to
address two TokuDB shortcomings, the renaming of data files on table/index rename, and the ability to group data files together within a directory that represents a single database. This feature is enabled by default.

## Bugs Fixed

The Audit Log plugin malformed record could be written after `audit_log_flush` was set to `ON` in `ASYNC` and `PERFORMANCE`
modes. Bug fixed [#1613650](https://bugs.launchpad.net/percona-server/+bug/1613650).

Running `SELECT DISTINCT x...ORDER BY y LIMIT N,N` could lead to a server
crash. Bug fixed [#1617586](https://bugs.launchpad.net/percona-server/+bug/1617586).

Workloads with statements that take non-transactional locks (`LOCK TABLES`,
global read lock, and similar) could have caused deadlocks when running
under Thread Pool with high priority queue enabled and `thread_pool_high_prio_mode` set to `transactions`. Fixed by
placing such statements into the high priority queue even with the above `thread_pool_high_prio_mode` setting. Bugs fixed [#1619559](https://bugs.launchpad.net/percona-server/+bug/1619559) and
[#1374930](https://bugs.launchpad.net/percona-server/+bug/1374930).

Fixed memory leaks in Audit Log Plugin. Bug fixed [#1620152](https://bugs.launchpad.net/percona-server/+bug/1620152)
(upstream [#71759](http://bugs.mysql.com/bug.php?id=71759)).

A server could crash due to a `glibc` bug in handling short-lived detached
threads. Bug fixed [#1621012](https://bugs.launchpad.net/percona-server/+bug/1621012) (upstream [#82886](http://bugs.mysql.com/bug.php?id=82886)).

`QUERY_RESPONSE_TIME_READ` and `QUERY_RESPONSE_TIME_WRITE` were returning
`QUERY_RESPONSE_TIME` table data if accessed through a name that is not
full uppercase. Bug fixed [#1552428](https://bugs.launchpad.net/percona-server/+bug/1552428).

Cipher `ECDHE-RSA-AES128-GCM-SHA256` was listed in the [list](https://dev.mysql.com/doc/refman/5.7/en/secure-connection-protocols-ciphers.html)
of supported ciphers but it wasn’t supported. Bug fixed [#1622034](https://bugs.launchpad.net/percona-server/+bug/1622034)
(upstream [#82935](http://bugs.mysql.com/bug.php?id=82935)).

Successful recovery of a torn page from the doublewrite buffer was shown as a
warning in the error log. Bug fixed [#1622985](https://bugs.launchpad.net/percona-server/+bug/1622985).

LRU manager threads could run too long on a server shutdown, causing a server
crash. Bug fixed [#1626069](https://bugs.launchpad.net/percona-server/+bug/1626069).

`tokudb_default` was not recognized by *Percona Server for MySQL* as a valid row
format. Bug fixed [#1626206](https://bugs.launchpad.net/percona-server/+bug/1626206).

InnoDB `ANALYZE TABLE` didn’t remove its table from the background
statistics processing queue. Bug fixed [#1626441](https://bugs.launchpad.net/percona-server/+bug/1626441) (upstream
[#71761](http://bugs.mysql.com/bug.php?id=71761)).

Upstream merge for [#81657](http://bugs.mysql.com/bug.php?id=81657) to 5.6 was incorrect. Bug fixed
[#1626936](https://bugs.launchpad.net/percona-server/+bug/1626936) (upstream [#83124](http://bugs.mysql.com/bug.php?id=83124)).

Fixed multi-threaded slave thread leaks that happened in case of thread create
failure. Bug fixed [#1619622](https://bugs.launchpad.net/percona-server/+bug/1619622) (upstream [#82980](http://bugs.mysql.com/bug.php?id=82980)).

The shutdown waiting for a purge to complete was undiagnosed for the first minute.
Bug fixed [#1616785](https://bugs.launchpad.net/percona-server/+bug/1616785).

Other bugs fixed: [#1614439](https://bugs.launchpad.net/percona-server/+bug/1614439), [#1614949](https://bugs.launchpad.net/percona-server/+bug/1614949), [#1624993](https://bugs.launchpad.net/percona-server/+bug/1624993)
([#736](https://tokutek.atlassian.net/browse/FT-736)), [#1613647](https://bugs.launchpad.net/percona-server/+bug/1613647), [#1615468](https://bugs.launchpad.net/percona-server/+bug/1615468), [#1617828](https://bugs.launchpad.net/percona-server/+bug/1617828), [#1617833](https://bugs.launchpad.net/percona-server/+bug/1617833),
[#1626002](https://bugs.launchpad.net/percona-server/+bug/1626002) (upstream [#83073](http://bugs.mysql.com/bug.php?id=83073)), [#904714](https://bugs.launchpad.net/percona-server/+bug/904714), [#1610102](https://bugs.launchpad.net/percona-server/+bug/1610102),
[#1610110](https://bugs.launchpad.net/percona-server/+bug/1610110), [#1613728](https://bugs.launchpad.net/percona-server/+bug/1613728), [#1614885](https://bugs.launchpad.net/percona-server/+bug/1614885), [#1615959](https://bugs.launchpad.net/percona-server/+bug/1615959), [#1616333](https://bugs.launchpad.net/percona-server/+bug/1616333),
[#1616404](https://bugs.launchpad.net/percona-server/+bug/1616404), [#1616768](https://bugs.launchpad.net/percona-server/+bug/1616768), [#1617150](https://bugs.launchpad.net/percona-server/+bug/1617150), [#1617216](https://bugs.launchpad.net/percona-server/+bug/1617216), [#1617267](https://bugs.launchpad.net/percona-server/+bug/1617267),
[#1618478](https://bugs.launchpad.net/percona-server/+bug/1618478), [#1618819](https://bugs.launchpad.net/percona-server/+bug/1618819), [#1619547](https://bugs.launchpad.net/percona-server/+bug/1619547), [#1619572](https://bugs.launchpad.net/percona-server/+bug/1619572), [#1620583](https://bugs.launchpad.net/percona-server/+bug/1620583),
[#1622449](https://bugs.launchpad.net/percona-server/+bug/1622449), [#1623011](https://bugs.launchpad.net/percona-server/+bug/1623011), [#1624992](https://bugs.launchpad.net/percona-server/+bug/1624992) ([#1014](https://tokutek.atlassian.net/browse/DB-1014)), [#735](https://tokutek.atlassian.net/browse/FT-735),
[#1626500](https://bugs.launchpad.net/percona-server/+bug/1626500), [#1628913](https://bugs.launchpad.net/percona-server/+bug/1628913), [#952920](https://bugs.launchpad.net/percona-server/+bug/952920), and [#964](https://tokutek.atlassian.net/browse/DB-964).
