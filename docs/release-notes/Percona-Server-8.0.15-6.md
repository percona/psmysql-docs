# Percona Server for MySQL 8.0.15-6

*Percona* announces the release of *Percona Server for MySQL* 8.0.15-6 on May 07, 2019
(downloads are available [here](https://www.percona.com/downloads/Percona-Server-8.0/) and from the [Percona
Software Repositories](https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries)).

This release includes fixes to bugs found in previous releases of *Percona Server for MySQL* 8.0.

*Percona Server for MySQL* 8.0.15-6 is now the current GA release in the 8.0
series. All of *Percona*’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the [features available in MySQL 8.0
Community Edition](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html) in addition to
enterprise-grade features developed by Percona.  For a list of highlighted
features from both MySQL 8.0 and Percona Server for MySQL 8.0, please see the
[GA release announcement](https://www.percona.com/blog/2018/12/21/announcing-general-availability-of-percona-server-for-mysql-8-0/).

!!! note

    If you are upgrading from 5.7 to 8.0, please ensure that you read the [upgrade guide](https://www.percona.com/doc/percona-server/8.0/upgrading_guide.html) and the document [Changed in Percona Server for MySQL 8.0](https://www.percona.com/doc/percona-server/8.0/changed_in_version.html).

## New Features


* The server part of MyRocks cross-engine consistent physical backups has been
implemented by introducing rocksdb_disable_file_deletions and
rocksdb_create_temporary_checkpoint session variables. These
variables are intended to be used by backup tools. Prolonged use or
other misuse can have serious side effects to the server instance.


* RocksDB WAL file information can now be seen in the
performance_schema.log_status table.


* New Audit_log_buffer_size_overflow status variable has been
implemented to track when an Audit Log Plugin entry was either
dropped or written directly to the file due to its size being bigger
than audit_log_buffer_size variable.

## Bugs Fixed


* TokuDB and MyRocks native partitioning handler objects were allocated from a
wrong memory allocator. Memory was released only on shutdown and concurrent
access to global memory allocator caused memory corruptions and therefore
crashes. Bug fixed [#5508](https://jira.percona.com/browse/PS-5508).


* using TokuDB or MyRocks native partitioning and `index_merge` could lead to
a server crash. Bugs fixed [#5206](https://jira.percona.com/browse/PS-5206), [#5562](https://jira.percona.com/browse/PS-5562).


* upgrade from *Percona Server for MySQL* 5.7.24 to Percona Server for MySQL 8.0.13-3 wasn’t working with
encrypted undo tablespaces. Bug fixed [#5223](https://jira.percona.com/browse/PS-5223).


* keyring_vault_plugin couldn’t be initialized on *Ubuntu Cosmic 17.10*.
Bug fixed [#5453](https://jira.percona.com/browse/PS-5453).


* rotated key encryption did not register `encryption_key_id` as a valid
table option. Bug fixed [#5482](https://jira.percona.com/browse/PS-5482).


* INFORMATION_SCHEMA.GLOBAL_TEMPORARY_TABLES queries could crash if
online `ALTER TABLE` was running in parallel. Bug fixed [#5566](https://jira.percona.com/browse/PS-5566).


* setting the log_slow_verbosity to include `innodb` value and
enabling the slow_query_log could lead to a server crash.
Bug fixed [#4933](https://jira.percona.com/browse/PS-4933).


* compression_dictionary operations were not allowed under
innodb-force-recovery. Now they work correctly when
innodb_force_recovery is <= `2`, and are forbidden when
innodb_force_recovery is >= `3`.
Bug fixed [#5148](https://jira.percona.com/browse/PS-5148).


* `BLOB` entries in the binary log could become corrupted
in case when a database with `Blackhole` tables served as an
intermediate binary log server in a replication chain. Bug fixed
[#5353](https://jira.percona.com/browse/PS-5353).


* `FLUSH CHANGED_PAGE_BITMAPS` would leave gaps between the last written
bitmap LSN and the *InnoDB* checkpoint LSN. Bug fixed [#5446](https://jira.percona.com/browse/PS-5446).


* XtraDB changed page tracking was missing pages changed by the in-place DDL.
Bug fixed [#5447](https://jira.percona.com/browse/PS-5447).


* `innodb_system` tablespace information was missing from the
INFORMATION_SCHEMA.innodb_tablespaces view.
Bug fixed [#5473](https://jira.percona.com/browse/PS-5473).


* undo log tablespace encryption status is now available through
INFORMATION_SCHEMA.innodb_tablespaces view.
Bug fixed [#5485](https://jira.percona.com/browse/PS-5485) (upstream [#94665](http://bugs.mysql.com/bug.php?id=94665)).


* enabling temporay tablespace encryption didn’t mark the
`innodb_temporary` tablespace with the encryption flag. Bug fixed
[#5490](https://jira.percona.com/browse/PS-5490).


* server would crash during bootstrap if innodb_encrypt_tables
was set to `1`. Bug fixed [#5492](https://jira.percona.com/browse/PS-5492).


* fixed intermittent shutdown crashes that were happening if Thread Pool
was enabled. Bug fixed [#5510](https://jira.percona.com/browse/PS-5510).


* compression dictionary `INFORMATION_SCHEMA` views were missing when datadir was upgraded from 8.0.13 to 8.0.15. Bug fixed [#5529](https://jira.percona.com/browse/PS-5529).


* innodb_encrypt_tables variable accepted `FORCE` option only
as a string. Bug fixed [#5538](https://jira.percona.com/browse/PS-5538).


* `ibd2sdi` utility was missing in Debian/Ubuntu packages. Bug fixed
[#5549](https://jira.percona.com/browse/PS-5549).


* Docker image is now ignoring password that is set in the configuration
file when first initializing. Bug fixed [#5573](https://jira.percona.com/browse/PS-5573).


* long running `ALTER TABLE ADD INDEX` could cause a `semaphore wait > 600`
assertion. Bug fixed [#3410](https://jira.percona.com/browse/PS-3410) (upstream [#82940](http://bugs.mysql.com/bug.php?id=82940)).


* system keyring keys initialization wasn’t thread safe. Bugs fixed
[#5554](https://jira.percona.com/browse/PS-5554).


* Backup Locks was blocking DML for RocksDB. Bug fixed [#5583](https://jira.percona.com/browse/PS-5583).


* PerconaFT `locktree` library was re-licensed to Apache v2 license.
Bug fixed [#5501](https://jira.percona.com/browse/PS-5501).

Other bugs fixed:
[#5243](https://jira.percona.com/browse/PS-5243),
[#5484](https://jira.percona.com/browse/PS-5484),
[#5512](https://jira.percona.com/browse/PS-5512),
[#5523](https://jira.percona.com/browse/PS-5523),
[#5536](https://jira.percona.com/browse/PS-5536),
[#5550](https://jira.percona.com/browse/PS-5550),
[#5570](https://jira.percona.com/browse/PS-5570),
[#5578](https://jira.percona.com/browse/PS-5578),
[#5441](https://jira.percona.com/browse/PS-5441),
[#5442](https://jira.percona.com/browse/PS-5442),
[#5456](https://jira.percona.com/browse/PS-5456),
[#5462](https://jira.percona.com/browse/PS-5462),
[#5487](https://jira.percona.com/browse/PS-5487),
[#5489](https://jira.percona.com/browse/PS-5489),
[#5520](https://jira.percona.com/browse/PS-5520), and
[#5560](https://jira.percona.com/browse/PS-5560).
