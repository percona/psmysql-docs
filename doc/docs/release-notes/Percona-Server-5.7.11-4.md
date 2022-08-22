# *Percona Server for MySQL* 5.7.11-4 (2016-03-15)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.11-4 on March 15th, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.11-4/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.11](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-11.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.11-4 is the current GA release in
the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source and
free, all the details of the release can be found in the [5.7.11-4 milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.11-4)

## New Features

*Percona Server for MySQL* has implemented a Parallel doublewrite buffer.

The TokuDB Background ANALYZE TABLE feature is now enabled by default
(`tokudb_analyze_in_background` is set to `ON` by default).
Variable `tokudb_auto_analyze` default value has been changed from
`0` to `30`. ([#935](https://tokutek.atlassian.net/browse/DB-935))

Suppress Warning Messages feature has been removed from *Percona Server for MySQL* 5.7
because MySQL 5.7.11 has implemented a new system variable,
[log_statements_unsafe_for_binlog](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_log_statements_unsafe_for_binlog),
which implements the same effect.

## Bugs Fixed

If `pid-file` option wasn’t specified with the full path, *Ubuntu*/*Debian*
`sysvinit` script wouldn’t notice the server is actually running and it will
timeout or in some cases even hang. Bug fixed [#1549333](https://bugs.launchpad.net/percona-server/+bug/1549333).

Buffer pool may fail to remove dirty pages for a particular tablespace from
the flush list, as requested by, for example, `DROP TABLE` or `TRUNCATE
TABLE` commands. This could lead to a crash. Bug fixed [#1552673](https://bugs.launchpad.net/percona-server/+bug/1552673).

Audit Log Plugin worker thread may crash on write call writing fewer
bytes than requested. Bug fixed [#1552682](https://bugs.launchpad.net/percona-server/+bug/1552682) (upstream [#80606](http://bugs.mysql.com/bug.php?id=80606)).

*Percona Server for MySQL* 5.7 `systemd` script now takes the last option specified in
`my.cnf` if the same option is specified multiple times. Previously it
would try to take all values which would break the script and server would
fail to start. Bug fixed [#1554976](https://bugs.launchpad.net/percona-server/+bug/1554976).

`mysqldumpslow` script has been removed because it was not compatible with
*Percona Server for MySQL* extended slow query log format. Please use [pt-query-digest](https://www.percona.com/doc/percona-toolkit/2.2/pt-query-digest.html) from
*Percona Toolkit* instead. Bug fixed [#856910](https://bugs.launchpad.net/percona-server/+bug/856910).

Other bugs fixed: [#1521120](https://bugs.launchpad.net/percona-server/+bug/1521120), [#1549301](https://bugs.launchpad.net/percona-server/+bug/1549301) (upstream [#80496](http://bugs.mysql.com/bug.php?id=80496)),
and [#1554043](https://bugs.launchpad.net/percona-server/+bug/1554043) (upstream [#80607](http://bugs.mysql.com/bug.php?id=80607)).
