# Percona Server 5.7.21-21 (2018-04-24)

Percona is glad to announce the release of Percona Server 5.7.21-21
on April 24, 2018. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.21-21/) and from the Percona Software Repositories.

This release is based on [MySQL 5.7.21](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-21.html) and includes all the bug fixes in it.
Percona Server 5.7.21-21 is now the current GA (Generally Available) release
in the 5.7 series.
This version of Percona Server for MySQL marks the following encryption
features, previously available as beta, as GA: [Vault keyring plugin](https://www.percona.com/doc/percona-server/5.7/management/data_at_rest_encryption.html#id13), [encryption for InnoDB general tablespaces](https://www.percona.com/doc/percona-server/5.7/management/data_at_rest_encryption.html#id7), and [encryption for binary log files](https://www.percona.com/doc/percona-server/5.7/management/data_at_rest_encryption.html#id14).

All software developed by Percona is open-source and free.

## New Features

* A new variable, `innodb_temp_tablespace_encrypt`, is introduced to
turn encryption of temporary tablespace and temporary InnoDB file-per-table
tablespaces on/off. Bug fixed [#3821](https://jira.percona.com/browse/PS-3821).

* A new variable, `innodb_encrypt_online_alter_logs`, simultaneously
turns on encryption of files used by InnoDB for merge sort, online DDL logs,
and temporary tables created by InnoDB for online DDL. Bug fixed
[#3819](https://jira.percona.com/browse/PS-3819).

* A new variable, `innodb_encrypt_tables`, can be set to `ON`, making
InnoDB tables encrypted by default, to `FORCE`, disabling creation of
unencrypted tables, or `OFF`, restoring the like-before behavior. Bug fixed
[#1525](https://jira.percona.com/browse/PS-1525).

* Query response time plugin now can be disabled at session level with use
of a new variable, `query_response_time_session_stats`.

## Bugs Fixed

* Attempting to use a partially-installed query response time plugin could have
caused server crash. Bug fixed [#3959](https://jira.percona.com/browse/PS-3959).

* There was a server crash caused by a materialized temporary table from
semi-join optimization with key length larger than 1000 bytes. Bug fixed
[#296](https://jira.percona.com/browse/PS-296).

* A regression in the original 5.7 port was causing integer overflow with `thread_pool_stall_limit` variable values bigger than 2 seconds. Bug fixed [#1095](https://jira.percona.com/browse/PS-1095).

* A memory leak took place in *Percona Server for MySQL* when performance schema is used
in conjunction with thread pooling. Bug fixed [#1096](https://jira.percona.com/browse/PS-1096).

* A code clean-up was done to fix compilation with clang, both general warnings
(bug fixed [#3814](https://jira.percona.com/browse/PS-3814), upstream [#89646](http://bugs.mysql.com/bug.php?id=89646)) and clang 6 specific warnings and errors (bug fixed [#3893](https://jira.percona.com/browse/PS-3893), upstream [#90111](http://bugs.mysql.com/bug.php?id=90111)).

* Compilation warning was fixed for -DWITH_QUERY_RESPONSE_TIME=ON CMake
compilation option, which makes QRT to be linked statically. Bug fixed
[#3841](https://jira.percona.com/browse/PS-3841).

* *Percona Server for MySQL* returned empty result for `SELECT` query if number of
connections exceeded 65535. Bug fixed [#314](https://jira.percona.com/browse/PS-314) (upstream
[#89313](http://bugs.mysql.com/bug.php?id=89313)).

* A clean-up in *Percona Server for MySQL* binlog-related code was made to avoid
uninitialized memory comparison. Bug fixed [#3925](https://jira.percona.com/browse/PS-3925) (upstream
[#90238](http://bugs.mysql.com/bug.php?id=90238)).

* `mysqldump` utility with `--innodb-optimize-keys` option was incorrectly
working with foreign keys on the same table, producing invalid SQL
statements. Bugs fixed [#1125](https://jira.percona.com/browse/PS-1125) and [#3863](https://jira.percona.com/browse/PS-3863).

* A fix of the mysqld startup script failed to detect jemalloc library
location for preloading, thus not starting on systemd based machines,
introduced in *Percona Server for MySQL* `5.7.21-20`, was improved to take into
account previously created configuration file. Bug fixed [#3850](https://jira.percona.com/browse/PS-3850).

* The possibility of a truncated bitmap file name was fixed in InnoDB logging
subsystem. Bug fixed [#3926](https://jira.percona.com/browse/PS-3926).

* Temporary file I/O was not instrumented for Performance Schema. Bug fixed
[#3937](https://jira.percona.com/browse/PS-3937) (upstream [#90264](http://bugs.mysql.com/bug.php?id=90264)).

* A crash in the unsafe query warning checks with views took place for
`UPDATE` statement in case of statement binlogging format. Bug fixed
[#290](https://jira.percona.com/browse/PS-290).

## MyRocks Changes

* A re-implemented variable, `rpl_skip_tx_api`, allows a user to turn on
simple RocksDB write batches functionality, increasing replication
performance by the transaction API skip. Bug fixed [MYR-47](https://jira.percona.com/browse/MYR-47).

* Decoding value-less padded varchar fields could under some circumstances
cause assertion and/or data corruption. Bug fixed [MYR-232](https://jira.percona.com/browse/MYR-232).

## TokuDB Changes

* Two new variables introduced to facilitate the TokuDB fast updates feature,`tokudb_enable_fast_update`, 
and `tokudb_enable_fast_upsert`. Bugs fixed [#63](https://jira.percona.com/browse/TDB-63) and
[#148](https://jira.percona.com/browse/TDB-148).

* A set of compilation fixes was introduced to make TokuDB successfully
build in MySQL / *Percona Server for MySQL* 8.0. Bugs fixed [#84](https://jira.percona.com/browse/TDB-84),
[#85](https://jira.percona.com/browse/TDB-85), [#114](https://jira.percona.com/browse/TDB-114), [#115](https://jira.percona.com/browse/TDB-115), [#118](https://jira.percona.com/browse/TDB-118), [#128](https://jira.percona.com/browse/TDB-128),
[#139](https://jira.percona.com/browse/TDB-139), [#141](https://jira.percona.com/browse/TDB-141), and [#172](https://jira.percona.com/browse/TDB-172).

* Conditional compilation code dependent on version ID in the TokuDB tree was
separated and arranged to specific version branches. Bugs fixed
[#133](https://jira.percona.com/browse/TDB-133), [#134](https://jira.percona.com/browse/TDB-134), [#135](https://jira.percona.com/browse/TDB-135), and [#136](https://jira.percona.com/browse/TDB-136).

* `ALTER TABLE ... COMMENT = ...` statement caused TokuDB to rebuild the
whole table, which is not needed, as only FRM metadata should be changed.
Bugs fixed [#130](https://jira.percona.com/browse/TDB-130) and [#137](https://jira.percona.com/browse/TDB-137).

* Data race on the cache table pair attributes was fixed. Bug fixed
[#109](https://jira.percona.com/browse/TDB-109).

Other bugs fixed: [#3793](https://jira.percona.com/browse/PS-3793), [#3812](https://jira.percona.com/browse/PS-3812), [#3813](https://jira.percona.com/browse/PS-3813), [#3815](https://jira.percona.com/browse/PS-3815),
[#3818](https://jira.percona.com/browse/PS-3818), [#3835](https://jira.percona.com/browse/PS-3835), [#3875](https://jira.percona.com/browse/PS-3875) (upstream [#89916](http://bugs.mysql.com/bug.php?id=89916)),
[#3843](https://jira.percona.com/browse/PS-3843) (upstream [#89822](http://bugs.mysql.com/bug.php?id=89822)), [#3848](https://jira.percona.com/browse/PS-3848), [#3856](https://jira.percona.com/browse/PS-3856),
[#3887](https://jira.percona.com/browse/PS-3887), [MYR-160](https://jira.percona.com/browse/MYR-160), [MYR-245](https://jira.percona.com/browse/MYR-245), [#109](https://jira.percona.com/browse/TDB-109),
[#111](https://jira.percona.com/browse/TDB-111), [#180](https://jira.percona.com/browse/TDB-180), [#181](https://jira.percona.com/browse/TDB-181), [#182](https://jira.percona.com/browse/TDB-182), and [#188](https://jira.percona.com/browse/TDB-188).
