# Percona Server 5.7.20-19 (2018-01-03)

Percona is glad to announce the release of Percona Server 5.7.20-19
on January 3, 2018. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.20-19/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.20](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-20.html)
and includes all the bug fixes in it.
Percona Server 5.7.20-19 is now the current GA (Generally Available) release
in the 5.7 series. All software developed by Percona is open-source and free.
Details of this release can be found in the [5.7.20-19 milestone on Launchpad](https://launchpad.net/percona-server/+milestone/5.7.20-19).

## New Features

* Now MyRocks Storage Engine has *General Availability* status.

* Binary log encryption has been implemented and can be now switched on using
the `encrypt_binlog` variable.

* `innodb_print_lock_wait_timeout_info` variable, introduced in the previous
release, but undocumented, allows to log information about all lock wait
timeout errors.

## Bugs Fixed

* Intermediary slave with Blackhole storage engine couldn’t record updates
from master to its own binary log in case the master has the `binlog_rows_query_log_events` option enabled. Bug fixed [#1722789](https://bugs.launchpad.net/percona-server/+bug/1722789)
(upstream [#88057](http://bugs.mysql.com/bug.php?id=88057)).

* Help command in the MySQL command line client provided a link to an older
version of the *Percona Server for MySQL* manual. Bug fixed [#1708073](https://bugs.launchpad.net/percona-server/+bug/1708073).

* A regression in the `mysqld_safe` script forced it to print an extra error when
stopping the MySQL service. Bugs fixed [#1738742](https://bugs.launchpad.net/percona-server/+bug/1738742).

* Blackhole storage engine was incompatible with a newer length limit of the
InnoDB index key prefixes. Bug fixed [#1733049](https://bugs.launchpad.net/percona-server/+bug/1733049) (upstream [#53588](http://bugs.mysql.com/bug.php?id=53588)).

* Heartbeats received by a slave were reacted with `mysql.slave_master_info`
table sync on each of them even with `sync_master_info` set to zero, causing a huge increase in write load. Bug fixed [#1708033](https://bugs.launchpad.net/percona-server/+bug/1708033) (upstream [#85158](http://bugs.mysql.com/bug.php?id=85158)).

## MyRocks Changes

* The replication writebatch functionality has been removed from
*Percona Server for MySQL* 5.7 due to the unsafety of the current implementation.

* The variables `rocksdb_block_cachecompressed_hit`, `rocksdb_block_cachecompressed_miss`, and `rocksdb_getupdatessince_calls`
were renamed to `rocksdb_block_cache_compressed_hit`, `rocksdb_block_cache_compressed_miss`, and `rocksdb_get_updates_since_calls`
respectively.
