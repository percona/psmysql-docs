# Percona Server for MySQL 8.0.15-5

*Percona* announces the release of *Percona Server for MySQL* 8.0.15-5 on March 15, 2019
(downloads are available [here](https://www.percona.com/downloads/Percona-Server-8.0/) and from the [Percona
Software Repositories](https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries)).

This release includes fixes to bugs found in previous releases of *Percona Server for MySQL* 8.0.

Starting from the release `8.0.15-5` , *Percona Server for MySQL* uses the upstream
implementation of binary log encryption. The variable `encrypt_binlog` is
removed and the related command line option `--encrypt_binlog` is not
supported. It is important that you remove the `encrypt_binlog` variable from
your configuration file before you attempt to upgrade from either another
release in the *Percona Server for MySQL* 8.0 series or *Percona Server for MySQL*
5.7. Otherwise, a server boot error reports an unknown
variable. The implemented binary log encryption is compatible with the old
format: the binary log encrypted in a previous version of MySQL 8.0 series or
Percona Server for MySQL are supported.

This release is based on *MySQL* 8.0.14 and 8.0.15. It includes all
bug fixes in these releases. *Percona Server for MySQL* Percona Server for MySQL 8.0.14 was skipped.

*Percona Server for MySQL* 8.0.15-5 is now the current GA release in the 8.0
series. All of *Percona*’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the [features available in MySQL 8.0
Community Edition](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html) in addition to
enterprise-grade features developed by Percona.  For a list of highlighted
features from both MySQL 8.0 and Percona Server for MySQL 8.0, please see the
[GA release announcement](https://www.percona.com/blog/2018/12/21/announcing-general-availability-of-percona-server-for-mysql-8-0/).

**NOTE**: If you are upgrading from 5.7 to 8.0, please ensure that you read the
[upgrade guide](https://docs.percona.com/percona-server/8.0/upgrade.html) and
the document [Changed in Percona Server for MySQL 8.0](https://www.percona.com/doc/percona-server/8.0/changed_in_version.html).

## Bugs Fixed


* The audit log produced time stamps inconsistent with the ISO8601 standard. Bug
fixed [#226](https://jira.percona.com/browse/PS-226).


* FLUSH commands written to the binary log could cause errors in case of
replication. Bug fixed [#1827](https://jira.percona.com/browse/PS-1827) (upstream [#88720](http://bugs.mysql.com/bug.php?id=88720)).


* When audit_plugin was enabled, the server could use a lot of memory when
handling large queries.  Bug fixed [#5395](https://jira.percona.com/browse/PS-5395).


* The page cleaner could sleep for long time when the system clock was adjusted
to an earlier point in time. Bug fixed [#5221](https://jira.percona.com/browse/PS-5221) (upstream [#93708](http://bugs.mysql.com/bug.php?id=93708)).


* In some cases, the MyRocks storage engine could crash without triggering
the crash recovery. Bug fixed [#5366](https://jira.percona.com/browse/PS-5366).


* In some cases, when it failed to read from a file, InnoDB did not inform the
name of the file in the related error message. Bug fixed [#2455](https://jira.percona.com/browse/PS-2455)
(upstream [#76020](http://bugs.mysql.com/bug.php?id=76020)).


* The `ACCESS_DENIED` field of the `information_schema.user_statistics`
table was not updated correctly. Bugs fixed [#3956](https://jira.percona.com/browse/PS-3956), [#4996](https://jira.percona.com/browse/PS-4996).


* `MyRocks` could crash while running `START TRANSACTION WITH
CONSISTENT SNAPSHOT` if other transactions were in specific states. Bug fixed
[#4705](https://jira.percona.com/browse/PS-4705).


* In some cases, the server using the the `MyRocks` storage engine could
crash when TTL (Time to Live) was defined on a table. Bug fixed [#4911](https://jira.percona.com/browse/PS-4911).


* MyRocks incorrectly processed transactions in which multiple statements
had to be rolled back. Bug fixed [#5219](https://jira.percona.com/browse/PS-5219).


* A stack buffer overrun could happen if the redo log encryption with
key rotation was enabled. Bug fixed [#5305](https://jira.percona.com/browse/PS-5305).


* The TokuDB storage engine would assert on load when used with jemalloc 5.x. Bug fixed [#5406](https://jira.percona.com/browse/PS-5406).

Other bugs fixed:
[#4106](https://jira.percona.com/browse/PS-4106),
[#4107](https://jira.percona.com/browse/PS-4107),
[#4108](https://jira.percona.com/browse/PS-4108),
[#4121](https://jira.percona.com/browse/PS-4121),
[#4474](https://jira.percona.com/browse/PS-4474),
[#4640](https://jira.percona.com/browse/PS-4640),
[#5055](https://jira.percona.com/browse/PS-5055),
[#5218](https://jira.percona.com/browse/PS-5218),
[#5328](https://jira.percona.com/browse/PS-5328),
[#5369](https://jira.percona.com/browse/PS-5369).
