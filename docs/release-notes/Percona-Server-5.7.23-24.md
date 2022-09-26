# Percona Server 5.7.23-24 (2018-11-09)

Percona announces the release of [Percona Server for MySQL](https://www.percona.com/software/percona-server) 5.7.23-24 on November 9,
2018 (downloads are available [here](https://www.percona.com/downloads/Percona-Server-5.7/) and from the [Percona
Software Repositories](https://www.percona.com/doc/percona-server/5.7/installation.html#installing-from-binaries)).
This release merges changes of [MySQL 5.7.23](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-23.html), including
all the bug fixes in it. Percona Server for MySQL 5.7.23-24 is now the current
GA release in the 5.7 series. All of Percona’s software is open-source and free.

This release introduces InnoDB encryption improvements and merges upstream
MyRocks changes. Also, the usage of column families in MyRocks has been
improved. The InnoDB encryption improvements are in **Alpha** quality and are
not recommended to be used in production.

## New Features

* [#4905](https://jira.percona.com/browse/PS-4905): Upstream MyRocks changes have been merged up to prod201810 tag

* [#4976](https://jira.percona.com/browse/PS-4976): InnoDB Undo Log Encryption has been implemented

* [#4946](https://jira.percona.com/browse/PS-4946): Add the `rocksdb_no_create_column_family` option to prevent the implicit creation of column families in MyRocks

* [#4556](https://jira.percona.com/browse/PS-4556): InnoDB Redo log has been implemented

* [#3839](https://jira.percona.com/browse/PS-3839): InnoDB Data Scrubbing has been implemented

* [#3834](https://jira.percona.com/browse/PS-3834): InnoDB Log Scrubbing has been implemented

## Bugs Fixed

* [#4723](https://jira.percona.com/browse/PS-4723): `PURGE CHANGED_PAGE_BITMAPS` did not work when `innodb_data_home_dir` was used

* [#4937](https://jira.percona.com/browse/PS-4937): `rocksdb_update_cf_options` was ignored when specified in `my.cnf` or on command line

* [#1107](https://jira.percona.com/browse/PS-1107): The binlog could be corrupted when tmpdir got full

* [#4834](https://jira.percona.com/browse/PS-4834): The encrypted system tablespace could have an empty uuid

* [#3906](https://jira.percona.com/browse/PS-3906): The server instance could crash when running the `ALTER` statement

### Other bugs fixed

* [#4106](https://jira.percona.com/browse/PS-4106): “Assertion `log.getting_synced` failed in `rocksdb::DBImpl::MarkLogsSynced(uint64_t, bool, const rocksdb::Status&)`”

* [#4930](https://jira.percona.com/browse/PS-4930): “main.percona_log_slow_innodb: Result content mismatch”

* [#4811](https://jira.percona.com/browse/PS-4811): “5.7 Merge and fixup for old DB-937 introduces possible regression”

* [#4705](https://jira.percona.com/browse/PS-4705): “crash on snapshot size check in RocksDB”

Find the release notes for Percona Server for MySQL 5.7.23-24 in our [online documentation](https://www.percona.com/doc/percona-server/5.7/release-notes/Percona-Server-5.7.23-24.html). Report
bugs in the [Jira bug tracker](https://jira.percona.com/projects/PS).
