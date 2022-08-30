# Percona Server 5.7.21-20 (2018-02-19)

Percona is glad to announce the release of Percona Server 5.7.21-20
on February 19, 2018. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.21-20/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.21](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-21.html)
and includes all the bug fixes in it.
Percona Server 5.7.21-20 is now the current GA (Generally Available) release
in the 5.7 series. All software developed by Percona is open-source and free.

## New Features

* A new string variable `version_suffix` allows changing suffix
for the *Percona Server for MySQL* version string returned by the read-only
`version` variable. Also `version_comment` is converted from a global read-only to a global read-write variable.

* A new `keyring_vault_timeout` variable allows setting the number
of seconds for the Vault server connection timeout. Bug fixed [#298](https://jira.percona.com/browse/PS-298).

## Bugs Fixed

* The mysqld startup script was unable to detect jemalloc library location for
preloading, and that prevented starting the *Percona Server for MySQL* on systemd-based machines. Bugs fixed [#3784](https://jira.percona.com/browse/PS-3784) and [#3791](https://jira.percona.com/browse/PS-3791).

* There was a problem with fulltext search, which could find a word with
punctuation marks in natural language mode only, but not in boolean mode.
Bugs fixed [#258](https://jira.percona.com/browse/PS-258), [#2501](https://jira.percona.com/browse/PS-2501) (upstream [#86164](http://bugs.mysql.com/bug.php?id=86164)).

* Build errors were present on FreeBSD (caused by fixing the bug
[#255](https://jira.percona.com/browse/PS-255) in *Percona Server for MySQL* 
`5.6.38-83.0` and on MacOS (caused
by fixing the bug [#264](https://jira.percona.com/browse/PS-264) in *Percona Server for MySQL* `5.7.20-19`. Bugs
fixed [#2284](https://jira.percona.com/browse/PS-2284) and [#2286](https://jira.percona.com/browse/PS-2286).

* A bunch of fixes were introduced to remove GCC 7 compilation warnings for
the *Percona Server for MySQL* build. Bugs fixed [#3780](https://jira.percona.com/browse/PS-3780) (upstream
[#89420](http://bugs.mysql.com/bug.php?id=89420), [#89421](http://bugs.mysql.com/bug.php?id=89421), and [#89422](http://bugs.mysql.com/bug.php?id=89422)).

* CMake error took place at compilation with bundled zlib. Bug fixed
[#302](https://jira.percona.com/browse/PS-302).

* A GCC 7 warning fix introduced a regression in *Percona Server for MySQL* that led to
a wrong SQL query built to access the remote server when the Federated storage
engine was used. Bug fixed [#1134](https://jira.percona.com/browse/PS-1134).

* It was possible to enable `encrypt_binlog` with no binary or relay
logging enabled. Bug fixed [#287](https://jira.percona.com/browse/PS-287).

* Long buffer wait times were occurring on busy servers in case of the
`IMPORT TABLESPACE` command. Bug fixed [#276](https://jira.percona.com/browse/PS-276).

* Server queries that contained JSON special characters and were logged by
Audit Log Plugin in JSON format caused invalid output due to lack of
escaping. Bug fixed [#1115](https://jira.percona.com/browse/PS-1115).

* Percona Server now uses *Travis CI*  for additional tests. Bug fixed
[#3777](https://jira.percona.com/browse/PS-3777).

Other bugs fixed: [#257](https://jira.percona.com/browse/PS-257), [#264](https://jira.percona.com/browse/PS-264), [#1090](https://jira.percona.com/browse/PS-1090)
(upstream [#78048](http://bugs.mysql.com/bug.php?id=78048)), [#1109](https://jira.percona.com/browse/PS-1109), [#1127](https://jira.percona.com/browse/PS-1127), [#2204](https://jira.percona.com/browse/PS-2204),
[#2414](https://jira.percona.com/browse/PS-2414), [#2415](https://jira.percona.com/browse/PS-2415), [#3767](https://jira.percona.com/browse/PS-3767), [#3794](https://jira.percona.com/browse/PS-3794), and [#3804](https://jira.percona.com/browse/PS-3804)
(upstream [#89598](http://bugs.mysql.com/bug.php?id=89598)).

This release also contains fixes for the following CVE issues: CVE-2018-2565,
CVE-2018-2573, CVE-2018-2576, CVE-2018-2583, CVE-2018-2586, CVE-2018-2590,
CVE-2018-2612, CVE-2018-2600, CVE-2018-2622, CVE-2018-2640, CVE-2018-2645,
CVE-2018-2646, CVE-2018-2647, CVE-2018-2665, CVE-2018-2667, CVE-2018-2668,
CVE-2018-2696, CVE-2018-2703, CVE-2017-3737.

## MyRocks Changes

* A new behavior makes *Percona Server for MySQL* fail to restart on detected data
corruption; `rocksdb_allow_to_start_after_corruption` variable can
be passed to `mysqld` as a command line parameter to switch off this
restart failure.

* A new cmake option `ALLOW_NO_SSE42` was introduced to allow MyRocks build
on hosts not supporting SSE 4.2 instructions set, which makes MyRocks usable
without FastCRC32-capable hardware. Bug fixed [MYR-207](https://jira.percona.com/browse/MYR-207).

* `rocksdb_bytes_per_sync` and `rocksdb_wal_bytes_per_sync` variables were turned into dynamic ones.

* `rocksdb_flush_memtable_on_analyze` variable has been removed.

* `rocksdb_concurrent_prepare` is now deprecated, as it has been
renamed in upstream to `rocksdb_two_write_queues`.

* `rocksdb_row_lock_deadlocks` and `rocksdb_row_lock_wait_timeouts` global status counters were added to track the number of deadlocks and the number of row lock wait timeouts.

* Creating a table with string indexed column to non-binary collation now
generates a warning about using inefficient collation instead of an error. Bug
fixed [MYR-223](https://jira.percona.com/browse/MYR-223).

## TokuDB Changes

* A memory leak was fixed in the PerconaFT library, caused by not destroying
PFS key objects on shutdown. Bug fixed [TDB-98](https://jira.percona.com/browse/TDB-98).

* A clang-format configuration was added to PerconaFT and TokuDB. Bug fixed
[TDB-104](https://jira.percona.com/browse/TDB-104).

* A data race was fixed in minicron utility of the PerconaFT. Bug fixed
[TDB-107](https://jira.percona.com/browse/TDB-107).

* Row count and cardinality decrease to zero took place after long-running
`REPLACE` load.

Other bugs fixed: [TDB-48](https://jira.percona.com/browse/TDB-48), [TDB-78](https://jira.percona.com/browse/TDB-78), [TDB-93](https://jira.percona.com/browse/TDB-93),
and [TDB-99](https://jira.percona.com/browse/TDB-99).
