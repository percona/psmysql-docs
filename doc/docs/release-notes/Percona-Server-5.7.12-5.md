# *Percona Server for MySQL* 5.7.12-5 (2016-06-06)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.12-5 on June 6th, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.12-5/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.12](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-12.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.12-5 is the current GA release in
the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source and
free, all the details of the release can be found in the [5.7.12-5 milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.12-5)

## Bugs Fixed

`MEMORY` storage engine did not support JSON columns. Bug fixed
[#1536469](https://bugs.launchpad.net/percona-server/+bug/1536469).

When Read Free Replication was enabled for TokuDB and there
was no explicit primary key for the replicated TokuDB table there could be
duplicated records in the table on update operation. The fix disables
Read Free Replication for tables without explicit primary key
and does rows lookup for `UPDATE` and `DELETE` binary log events and
issues warning. Bug fixed [#1536663](https://bugs.launchpad.net/percona-server/+bug/1536663) ([#950](https://tokutek.atlassian.net/browse/DB-950)).

Attempting to execute a non-existing prepared statement with
Response Time Distribution plugin enabled could lead to a server crash.
Bug fixed [#1538019](https://bugs.launchpad.net/percona-server/+bug/1538019).

TokuDB was using different memory allocators, this was causing
`safemalloc` warnings in debug builds and crashes because memory accounting
didn’t add up. Bug fixed [#1546538](https://bugs.launchpad.net/percona-server/+bug/1546538) ([#962](https://tokutek.atlassian.net/browse/DB-962)).

Adding an index to an InnoDB temporary table while `expand_fast_index_creation` was enabled could lead to server assertion. Bug fixed [#1554622](https://bugs.launchpad.net/percona-server/+bug/1554622).

*Percona Server for MySQL* was missing the `innodb_numa_interleave` server
variable. Bug fixed [#1561091](https://bugs.launchpad.net/percona-server/+bug/1561091) (upstream [#80288](http://bugs.mysql.com/bug.php?id=80288)).

Running `SHOW STATUS` in parallel to online buffer pool resizing could lead
to a server crash. Bug fixed [#1577282](https://bugs.launchpad.net/percona-server/+bug/1577282).

InnoDB crash recovery might fail if `innodb_flush_method` was set
to `ALL_O_DIRECT`. Bug fixed [#1529885](https://bugs.launchpad.net/percona-server/+bug/1529885).

Fixed heap allocator/deallocator mismatch in
Metrics for scalability measurement. Bug fixed [#1581051](https://bugs.launchpad.net/percona-server/+bug/1581051).

*Percona Server for MySQL* is now built with the system `zlib` library instead of the
older bundled one. Bug fixed [#1108016](https://bugs.launchpad.net/percona-server/+bug/1108016).

`CMake` would fail if TokuDB tests passed. Bug fixed [#1521566](https://bugs.launchpad.net/percona-server/+bug/1521566).

Reduced the memory overhead per page in the InnoDB buffer pool. The fix was
based on the Facebook patch
[#91e979e](https://github.com/facebook/mysql-5.6/commit/91e979e8436b83400e918fa0f251036e50d0cb5f).
Bug fixed [#1536693](https://bugs.launchpad.net/percona-server/+bug/1536693) (upstream [#72466](http://bugs.mysql.com/bug.php?id=72466)).

The `CREATE TABLE ... LIKE ...` statement could create a system table with an unsupported
enforced engine. Bug fixed [#1540338](https://bugs.launchpad.net/percona-server/+bug/1540338).

Change buffer merge could throttle to 5% of I/O capacity on an idle server.
Bug fixed [#1547525](https://bugs.launchpad.net/percona-server/+bug/1547525).

Parallel doublewrite memory was not freed with `innodb_fast_shutdown` set to `2`. Bug fixed [#1578139](https://bugs.launchpad.net/percona-server/+bug/1578139).

The server will now show a more descriptive error message when *Percona Server for MySQL* fails with `errno == 22 "Invalid argument"` if `innodb_flush_method` was set to `ALL_O_DIRECT`. Bug fixed
[#1578604](https://bugs.launchpad.net/percona-server/+bug/1578604).

The error log warning `Too many connections` was only printed for connection
attempts when `max_connections` + one `SUPER` have connected. If
the extra `SUPER` is not connected, the warning was not printed for a
non-SUPER connection attempt. Bug fixed [#1583553](https://bugs.launchpad.net/percona-server/+bug/1583553).

`apt-cache show` command for `percona-server-client` was showing
`innotop` included as part of the package. Bug fixed [#1201074](https://bugs.launchpad.net/percona-server/+bug/1201074).

A replication slave would fail to connect to a master running 5.5. Bug fixed
[#1566642](https://bugs.launchpad.net/percona-server/+bug/1566642) (upstream [#80962](http://bugs.mysql.com/bug.php?id=80962)).

Upgrade logic for figuring if TokuDB upgrade can be performed from the
version on disk to the current version was broken due to regression introduced
when fixing [#684](https://tokutek.atlassian.net/browse/FT-684) in *Percona Server for MySQL* `5.7.11-4`. Bug fixed
[#717](https://tokutek.atlassian.net/browse/FT-717).

Fixed `jemalloc` version parsing error. Bug fixed [#528](https://tokutek.atlassian.net/browse/DB-528).

If `ALTER TABLE` was run while `tokudb_auto_analyze` variable was
enabled it would trigger auto-analysis, which could lead to a server crash if
`ALTER TABLE DROP KEY` was used because it would be operating on the old
table/key meta-data. Bug fixed [#945](https://tokutek.atlassian.net/browse/DB-945).

The `tokudb_pk_insert_mode` session variable has been deprecated and
the behavior will be that of the former `tokudb_pk_insert_mode` set
to `1`. The optimization will be used were safe and not used were not
safe. Bug fixed [#952](https://tokutek.atlassian.net/browse/DB-952).

Bug in TokuDB Index Condition Pushdown was causing `ORDER BY DESC` to
reverse the scan outside of the WHERE bounds. This would cause a query to hang
in a `sending data` state for several minutes in some environments with
large amounts of data (3 billion records) if the `ORDER BY DESC` statement
was used. Bugs fixed [#988](https://tokutek.atlassian.net/browse/DB-988), [#233](https://tokutek.atlassian.net/browse/DB-233), and [#534](https://tokutek.atlassian.net/browse/DB-534).

Other bugs fixed: [#1510564](https://bugs.launchpad.net/percona-server/+bug/1510564) (upstream [#78981](http://bugs.mysql.com/bug.php?id=78981)), [#1533482](https://bugs.launchpad.net/percona-server/+bug/1533482)
(upstream [#79999](http://bugs.mysql.com/bug.php?id=79999)), [#1553166](https://bugs.launchpad.net/percona-server/+bug/1553166), [#1496282](https://bugs.launchpad.net/percona-server/+bug/1496282) ([#964](https://tokutek.atlassian.net/browse/DB-964)),
[#1496786](https://bugs.launchpad.net/percona-server/+bug/1496786) ([#956](https://tokutek.atlassian.net/browse/DB-956)), [#1566790](https://bugs.launchpad.net/percona-server/+bug/1566790), [#718](https://tokutek.atlassian.net/browse/FT-718), [#914](https://tokutek.atlassian.net/browse/DB-914),
[#937](https://tokutek.atlassian.net/browse/DB-937), [#954](https://tokutek.atlassian.net/browse/DB-954), [#955](https://tokutek.atlassian.net/browse/DB-955), [#970](https://tokutek.atlassian.net/browse/DB-970), [#971](https://tokutek.atlassian.net/browse/DB-971),
[#972](https://tokutek.atlassian.net/browse/DB-972), [#976](https://tokutek.atlassian.net/browse/DB-976), [#977](https://tokutek.atlassian.net/browse/DB-977), [#981](https://tokutek.atlassian.net/browse/DB-981), [#982](https://tokutek.atlassian.net/browse/DB-982),
[#637](https://tokutek.atlassian.net/browse/DB-637), and [#982](https://tokutek.atlassian.net/browse/DB-982).
