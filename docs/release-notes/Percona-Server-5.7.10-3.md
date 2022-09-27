# Percona Server for MySQL 5.7.10-3 (2016-02-23)

Percona is glad to announce the first GA (Generally Available) release of
*Percona Server for MySQL* 5.7.10-3 on February 23rd, 2016 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.10-3/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.10](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-10.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.10-3 is the current Generally
Available release in the *Percona Server for MySQL* 5.7 series. All of Percona’s
software is open-source and free, all the details of the release can be found
in the [5.7.10-3 milestone at Launchpad](https://launchpad.net/percona-server/+milestone/5.7.10-3)

## New Features

A complete list of changes between *Percona Server for MySQL* 5.6 and 5.7 can be seen in Changed in Percona Server 5.7.

*Percona Server for MySQL* has implemented a multi-threaded asynchronous LRU flusher. This work also allows to safely use of the `backoff` value for the `innodb_empty_free_list_algorithm` server system variable, and its default has been changed accordingly.

## Known Issues

In *Percona Server for MySQL* 5.7 [super_read_only](https://www.percona.com/doc/percona-server/5.6/management/super_read_only.html)
feature has been replaced with upstream implementation. There are currently
two known issues compared to *Percona Server for MySQL* 5.6 implementation:


* Bug [#78963](http://bugs.mysql.com/bug.php?id=78963), `super_read_only` aborts `STOP SLAVE` if variable `relay_log_info_repository` is set to `TABLE`
which could lead to a server crash in Debug builds.

* Bug [#79328](http://bugs.mysql.com/bug.php?id=79328), `super_read_only` set as a server option has no effect.

InnoDB crash recovery might fail if `innodb_flush_method` is set
to `ALL_O_DIRECT`. The workaround is to set this variable to a different
value before starting up the crashed instance (bug [#1529885](https://bugs.launchpad.net/percona-server/+bug/1529885)).

## Bugs Fixed

*Percona Server for MySQL* `5.7.10-1` didn’t write the initial root password into the log file `/var/log/mysqld.log` during the installation on
*CentOS 6*. Bug fixed [#1541769](https://bugs.launchpad.net/percona-server/+bug/1541769).

The cardinality of partitioned TokuDB tables became inaccurate after the changes introduced by the TokuDB Background ANALYZE TABLE feature in *Percona Server for MySQL* `5.7.10-1`. Bug fixed [#925](https://tokutek.atlassian.net/browse/DB-925).

Running the `TRUNCATE TABLE` while TokuDB Background ANALYZE TABLE is
enabled could lead to a server crash once analyze job tries to access the
truncated table. Bug fixed [#938](https://tokutek.atlassian.net/browse/DB-938).

Percona TokuBackup would fail with an unclear error if the backup process found
`mysqld_safe.pid` file (owned by root) inside the `datadir`. Fixed by excluding the `pid` file by default. Bug fixed [#125](https://tokutek.atlassian.net/browse/BACKUP-125).

The PAM Authentication Plugin build warning has been fixed. Bug fixed [#1541601](https://bugs.launchpad.net/percona-server/+bug/1541601).
