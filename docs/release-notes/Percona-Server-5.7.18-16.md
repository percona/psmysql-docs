# Percona Server for MySQL 5.7.18-16 (2017-07-28)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.18-16 on July 28, 2017 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.18-16/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.18](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-18.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.18-16 is the current GA release
in the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source
and free, all the details of the release can be found in the [5.7.18-16
milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.18-16)

Please note that RHEL 5, CentOS 5, and Ubuntu versions 12.04 and older are not
supported in future releases of *Percona Server for MySQL* and no further packages are
added for these distributions.

## New Feature

*Percona Server for MySQL* is now available on Debian 9 (stretch). The support only
covers the `amd64` architecture.

*Percona Server for MySQL* can now be built with the support of OpenSSL 1.1.

MyRocks storage engine has been merged into *Percona Server for MySQL*.

TokuDB is able to kill a query that is awaiting an FT locktree lock.

TokuDB enables using the `MySQL DEBUG_SYNC` facility within *Percona FT*.

## Bugs Fixed

Row counts in TokuDB could be lost intermittently after restarts. Bug fixed
[#2](https://jira.percona.com/browse/TDB-2).

In TokuDB, two races in the fractal tree lock manager could significantly
affect transactional throughput for some applications that used a small number
of concurrent transactions.  These races manifested as transactions
unnecessarily waiting for an available lock. Bug fixed [#3](https://jira.percona.com/browse/TDB-3).

*Percona FT* could assert when opening a dictionary with no useful information
to the error log. Bug fixed [#23](https://jira.percona.com/browse/TDB-23).

*Percona FT* could assert for various reasons deserializing nodes with no
useful error output. Bug fixed [#24](https://jira.percona.com/browse/TDB-24).

It was not possible to build *Percona Server for MySQL* on Debian 9 (stretch) due to
issues with OpenSSL 1.1. Bug fixed [#1702903](https://bugs.launchpad.net/percona-server/+bug/1702903) (upstream [#83814](http://bugs.mysql.com/bug.php?id=83814)).

Packaging was using the `dpkg --verify` command which is not available on
wheezy/precise. Bug fixed [#1694907](https://bugs.launchpad.net/percona-server/+bug/1694907).

Enabling and disabling the slow query log rotation spuriously added the version
suffix to the next slow query log file name. Bug fixed [#1704056](https://bugs.launchpad.net/percona-server/+bug/1704056).

With two client connections to a server (debug server build), the server could
crash after one of the clients set the global option `userstat` and flushed
the client statistics (`FLUSH CLIENT_STATISTICS`), and then both clients were
closed. Bug fixed [#1661488](https://bugs.launchpad.net/percona-server/+bug/1661488).

*Percona FT* did not pass cmake flags on to snappy cmake. Bug fixed
[#41](https://jira.percona.com/browse/TDB-41).  The progress status for partitioned TokuDB table ALTERs was
misleading. Bug fixed [#42](https://jira.percona.com/browse/TDB-42).

When a client application connecting to the Aurora cluster end point
using SSL (`--ssl-verify-server-cert` or
`--ssl-mode=VERIFY_IDENTITY` option), wildcard and  enabled SSL certificates were ignored. See
also Compatibility Matrix.  Note that the
`--ssl-verify-server-cert` option is deprecated in *Percona Server for MySQL*
5.7. Bug fixed [#1673656](https://bugs.launchpad.net/percona-server/+bug/1673656) (upstream [#68052](http://bugs.mysql.com/bug.php?id=68052)).

Killing a stored procedure execution could result in an assert failure on a
debug server build. Bug fixed [#1689736](https://bugs.launchpad.net/percona-server/+bug/1689736) (upstream [#86260](http://bugs.mysql.com/bug.php?id=86260)).

The `SET STATEMENT .. FOR` statement changed the global instead of the
session value of a variable if the statement occurred immediately after the
`SET GLOBAL` or `SHOW GLOBAL STATUS` command. Bug fixed [#1385352](https://bugs.launchpad.net/percona-server/+bug/1385352).

When running `SHOW ENGINE INNODB STATUS`, the `Buffer pool size, bytes`
entry contained **0**. Bug fixed [#1586262](https://bugs.launchpad.net/percona-server/+bug/1586262).

The synchronization between the LRU manager and page cleaner threads was not
done at shutdown. Bug fixed [#1689552](https://bugs.launchpad.net/percona-server/+bug/1689552).

Removed spurious `lock_wait_timeout_thread` wakeups, potentially reducing
`lock_sys_wait_mutex` contention. Patch by Inaam Rama merged from
`WebScaleSQL`. Bug fixed [#1704267](https://bugs.launchpad.net/percona-server/+bug/1704267) (upstream [#72123](http://bugs.mysql.com/bug.php?id=72123)).

Other bugs fixed:
[#1686603](https://bugs.launchpad.net/percona-server/+bug/1686603),
[#6](https://jira.percona.com/browse/TDB-6),
[#44](https://jira.percona.com/browse/TDB-44),
[#65](https://jira.percona.com/browse/TDB-65),
[#1160986](https://bugs.launchpad.net/percona-server/+bug/1160986),
[#1686934](https://bugs.launchpad.net/percona-server/+bug/1686934),
[#1688319](https://bugs.launchpad.net/percona-server/+bug/1688319),
[#1689989](https://bugs.launchpad.net/percona-server/+bug/1689989),
[#1690012](https://bugs.launchpad.net/percona-server/+bug/1690012),
[#1691682](https://bugs.launchpad.net/percona-server/+bug/1691682),
[#1697700](https://bugs.launchpad.net/percona-server/+bug/1697700),
[#1699788](https://bugs.launchpad.net/percona-server/+bug/1699788),
[#1121072](https://bugs.launchpad.net/percona-server/+bug/1121072), and
[#1684601](https://bugs.launchpad.net/percona-server/+bug/1684601) (upstream [#86016](http://bugs.mysql.com/bug.php?id=86016)).

!!! note

    Due to new package dependency, Ubuntu/Debian users should use `apt-get dist-upgrade` or `apt-get install percona-server-server-5.7` to upgrade.

## Compatibility Matrix

| Feature                 | YaSSL | OpenSSL &lt; 1.0.2 | OpenSSL &gt;= 1.0.2 |
|-------------------------|-------|--------------------|---------------------|
| ‘commonName’ validation | Yes   | Yes                | Yes                 |
| SAN validation          | No    | Yes                | Yes                 |
| Wildcards support       | No    | No                 | Yes                 |
