# Percona Server for MySQL 5.7.17-12 (2017-03-24)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.17-12 on March 24th, 2017 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.17-12/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.17](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-17.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.17-12 is the current GA release
in the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source
and free, all the details of the release can be found in the [5.7.17-12
milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.17-12)

## New Features

*Percona Server for MySQL* has implemented new **mysqldump**
`--order-by-primary-desc` option. This feature tells `mysqldump`
to take the backup by descending primary key order (`PRIMARY KEY DESC`)
which can be useful if the storage engine is using a reverse order column family
for a primary key.

**mysqldump** will now detect when MyRocks is installed and available
by seeing if there is a session variable named `rocksdb_skip_fill_cache`
and setting it to `1` if it exists.

Now **mysqldump** automatically enables the session variable `rocksdb_bulk_load` if it is supported by the target server.

## Bugs Fixed

If the variable `thread_handling` was set to `pool-of-threads` in
the MySQL configuration file, the server couldn’t be gracefully shut down by a
`SIGTERM` signal. Bug fixed [#1537554](https://bugs.launchpad.net/percona-server/+bug/1537554).

When `innodb_ft_result_cache_limit` was exceeded by internal memory
allocated by InnoDB during the FT scan not all memory was released which
could lead to server assertion. Bug fixed [#1634932](https://bugs.launchpad.net/percona-server/+bug/1634932) (upstream
[#83648](http://bugs.mysql.com/bug.php?id=83648)).

Executing the `FLUSH LOGS` on a read-only slave with a user that doesn’t
have the `SUPER` privilege would result in `Error 1290`. Bug fixed
[#1652852](https://bugs.launchpad.net/percona-server/+bug/1652852) (upstream [#84350](http://bugs.mysql.com/bug.php?id=84350)).

`FLUSH LOGS` was disabled with `read_only` and `super_read_only` variables. Bug fixed [#1654682](https://bugs.launchpad.net/percona-server/+bug/1654682) (upstream
[#84437](http://bugs.mysql.com/bug.php?id=84437)).

If `SHOW BINLOGS` or `PERFORMANCE_SCHEMA.GLOBAL_STATUS` query, and a
transaction commit would run in parallel, they could deadlock. Bug fixed
[#1657128](https://bugs.launchpad.net/percona-server/+bug/1657128).

A long-running binary log commit would block `SHOW STATUS`, which in turn
could block a number of other operations such as client connects and
disconnects. Bug fixed  [#1646100](https://bugs.launchpad.net/percona-server/+bug/1646100).

Log tracking initialization did not find the last valid bitmap data correctly. Bug
fixed [#1658055](https://bugs.launchpad.net/percona-server/+bug/1658055).

A query using a range scan with a complex range condition could lead to a server
crash. Bug fixed [#1660591](https://bugs.launchpad.net/percona-server/+bug/1660591) (upstream [#84736](http://bugs.mysql.com/bug.php?id=84736)).

Race condition between buffer pool page optimistic access and eviction could
lead to a server crash. Bug fixed [#1664280](https://bugs.launchpad.net/percona-server/+bug/1664280).

If Audit Log Plugin was unable to create a file pointed by `audit_log_file`, the server would crash during the startup. Bug fixed
[#1666496](https://bugs.launchpad.net/percona-server/+bug/1666496).

A `DROP TEMPORARY TABLE ...`  for a table created by a `CREATE TEMPORARY
TABLE ... SELECT ...` would get logged in the binary log on a disconnect
with mixed mode replication. Bug fixed [#1671013](https://bugs.launchpad.net/percona-server/+bug/1671013).

TokuDB did not use index with even if cardinality was good. Bug fixed
[#1671152](https://bugs.launchpad.net/percona-server/+bug/1671152).

Row-based replication events were not reflected in `Rows_updated` fields in
the User Statistics `INFORMATION_SCHEMA` tables. Bug fixed [#995624](https://bugs.launchpad.net/percona-server/+bug/995624).

When `DuplicateWeedout` strategy was used for joins, use was not reported in
the query plan info output extension for the slow query log. Bug fixed
[#1592694](https://bugs.launchpad.net/percona-server/+bug/1592694).

It was impossible to use column compression dictionaries with partitioned
InnoDB tables. Bug fixed [#1653104](https://bugs.launchpad.net/percona-server/+bug/1653104).

Diagnostics for OpenSSL errors have been improved. Bug fixed [#1660339](https://bugs.launchpad.net/percona-server/+bug/1660339)
(upstream [#75311](http://bugs.mysql.com/bug.php?id=75311)).

Other bugs fixed: [#1665545](https://bugs.launchpad.net/percona-server/+bug/1665545), [#1650321](https://bugs.launchpad.net/percona-server/+bug/1650321), [#1654501](https://bugs.launchpad.net/percona-server/+bug/1654501),
[#1663251](https://bugs.launchpad.net/percona-server/+bug/1663251), [#1659548](https://bugs.launchpad.net/percona-server/+bug/1659548), [#1663452](https://bugs.launchpad.net/percona-server/+bug/1663452), [#1670834](https://bugs.launchpad.net/percona-server/+bug/1670834), [#1672871](https://bugs.launchpad.net/percona-server/+bug/1672871),
[#1626545](https://bugs.launchpad.net/percona-server/+bug/1626545), [#1658006](https://bugs.launchpad.net/percona-server/+bug/1658006), [#1658021](https://bugs.launchpad.net/percona-server/+bug/1658021), [#1659218](https://bugs.launchpad.net/percona-server/+bug/1659218), [#1659746](https://bugs.launchpad.net/percona-server/+bug/1659746),
[#1660239](https://bugs.launchpad.net/percona-server/+bug/1660239), [#1660243](https://bugs.launchpad.net/percona-server/+bug/1660243), [#1660348](https://bugs.launchpad.net/percona-server/+bug/1660348), [#1662163](https://bugs.launchpad.net/percona-server/+bug/1662163) (upstream
[#81467](http://bugs.mysql.com/bug.php?id=81467)), [#1664219](https://bugs.launchpad.net/percona-server/+bug/1664219), [#1664473](https://bugs.launchpad.net/percona-server/+bug/1664473), [#1671076](https://bugs.launchpad.net/percona-server/+bug/1671076), and
[#1671123](https://bugs.launchpad.net/percona-server/+bug/1671123).
