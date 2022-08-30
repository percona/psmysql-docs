# *Percona Server for MySQL* 5.7.13-6 (2016-07-16)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.13-6 on July 6th, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.13-6/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.13](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-13.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.13-6 is the current GA release in
the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source and
free, all the details of the release can be found in the [5.7.13-6 milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.13-6)

## New Features

TokuDB MTR suite is now part of the default MTR suite in *Percona Server for MySQL*
5.7.

## Bugs Fixed

Querying the `GLOBAL_TEMPORARY_TABLES` table would cause a server crash
if temporary table owning threads would execute new queries. Bug fixed
[#1581949](https://bugs.launchpad.net/percona-server/+bug/1581949).

`IMPORT TABLESPACE` and undo tablespace truncate could get stuck
indefinitely with a writing workload in parallel. Bug fixed [#1585095](https://bugs.launchpad.net/percona-server/+bug/1585095).

Requesting to flush the whole of the buffer pool with doublewrite parallel
buffer wasn’t working correctly. Bug fixed [#1586265](https://bugs.launchpad.net/percona-server/+bug/1586265).

Audit Log Plugin would hang when trying to write a log record of `audit_log_buffer_size` length. Bug fixed [#1588439](https://bugs.launchpad.net/percona-server/+bug/1588439).

Audit log in `ASYNC` mode could skip log records that don’t fit into the log
buffer. Bug fixed [#1588447](https://bugs.launchpad.net/percona-server/+bug/1588447).

In order to support `innodb_flush_method` being set to
`ALL_O_DIRECT`, the log I/O buffers were aligned to `innodb_log_write_ahead_size`. This missed that the variable is
dynamic and could still cause the server to crash. Bug fixed [#1597143](https://bugs.launchpad.net/percona-server/+bug/1597143).

InnoDB tablespace import would fail when trying to import a table with
a different data directory. Bug fixed [#1548597](https://bugs.launchpad.net/percona-server/+bug/1548597) (upstream
[#76142](http://bugs.mysql.com/bug.php?id=76142)).

The Audit Log plugin was truncating SQL queries to 512 bytes. Bug fixed
[#1557293](https://bugs.launchpad.net/percona-server/+bug/1557293).

`mysqlbinlog` did not free the existing connection before opening a new
remote one. Bug fixed [#1587840](https://bugs.launchpad.net/percona-server/+bug/1587840) (upstream [#81675](http://bugs.mysql.com/bug.php?id=81675)).

Fixed a memory leak in `mysqldump`. Bug fixed [#1588845](https://bugs.launchpad.net/percona-server/+bug/1588845) (upstream
[#81714](http://bugs.mysql.com/bug.php?id=81714)).

Transparent Huge Pages check will now only happen if `tokudb_check_jemalloc` option is set. Bugs fixed [#939](https://tokutek.atlassian.net/browse/DB-939) and
[#713](https://tokutek.atlassian.net/browse/FT-713).

Logging in `ydb` environment validation functions now prints more useful
context. Bug fixed [#722](https://tokutek.atlassian.net/browse/FT-722).

Other bugs fixed: [#1541698](https://bugs.launchpad.net/percona-server/+bug/1541698) (upstream [#80261](http://bugs.mysql.com/bug.php?id=80261)), [#1587426](https://bugs.launchpad.net/percona-server/+bug/1587426)
(upstream, [#81657](http://bugs.mysql.com/bug.php?id=81657)), [#1589431](https://bugs.launchpad.net/percona-server/+bug/1589431), [#956](https://tokutek.atlassian.net/browse/DB-956), [#964](https://tokutek.atlassian.net/browse/DB-964),
