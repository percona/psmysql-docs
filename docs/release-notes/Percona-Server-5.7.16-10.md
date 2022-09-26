# Percona Server for MySQL 5.7.16-10 (2016-11-28)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.16-10 on November 28th, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.16-10/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.16](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-16.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.16-10 is the current GA release
in the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source
and free, all the details of the release can be found in the [5.7.16-10
milestone at Launchpad](https://launchpad.net/percona-server/+milestone/5.7.16-10)

## Deprecated Features

Metrics for scalability measurement feature is now deprecated. Users who have
installed this plugin but are not using its capability are advised to
uninstall the plugin due to known crashing bugs.

## Bugs Fixed

When a stored routine would call an administrative command such as
`OPTIMIZE TABLE`, `ANALYZE TABLE`, `ALTER TABLE`, `CREATE/DROP INDEX`,
etc. the effective value of `log_slow_sp_statements` was overwritten
by the value of `log_slow_admin_statements`. Bug fixed
[#719368](https://bugs.launchpad.net/percona-server/+bug/719368).

The server wouldn’t start after crash with with `innodb_force_recovery`
set to `6` if a parallel doublewrite file existed. Bug fixed [#1629879](https://bugs.launchpad.net/percona-server/+bug/1629879).

The Thread Pool `thread limit reached` and `failed to create thread`
messages are now printed on the first occurrence as well. Bug fixed
[#1636500](https://bugs.launchpad.net/percona-server/+bug/1636500).

`INFORMATION_SCHEMA.TABLE_STATISTICS` and `INFORMATION_SCHEMA.INDEX_STATISTICS`
tables were not correctly updated
for TokuDB. Bug fixed [#1629448](https://bugs.launchpad.net/percona-server/+bug/1629448).

Other bugs fixed: [#1633061](https://bugs.launchpad.net/percona-server/+bug/1633061), [#1633430](https://bugs.launchpad.net/percona-server/+bug/1633430), and [#1635184](https://bugs.launchpad.net/percona-server/+bug/1635184).
