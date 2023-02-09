# Percona Server for MySQL 8.0.12-2rc1

Following the [alpha release announced earlier](https://www.percona.com/blog/2018/09/27/announcement-alpha-build-of-percona-server-8-0/),
Percona announces the release candidate of *Percona Server for MySQL* 8.0.12-2rc1 on
October 31, 2018. Download the latest version from the Percona web site or the
Percona Software Repositories.

This release is based on *MySQL* 8.0.12 and includes all bug fixes in it. It is
a *Release Candidate* quality release and it is not intended for
production. If you want a high quality, Generally Available release, use the
current Stable version (the most recent stable release at the time of writing in
the 5.7 series is 5.7.23-23).

Percona provides completely open-source and free software.

## Installation

As this is a release candidate, installation is performed by enabling the
testing repository and installing the software via your package manager.  For
Debian based distributions, see [apt installation instructions](https://www.percona.com/doc/percona-server/8.0/installation/apt_repo.html);
for RPM based distributions. see [yum installation instructions](https://www.percona.com/doc/percona-server/8.0/installation/yum_repo.html).
Note that in both cases after installing the current percona-release package,
you’ll need to enable the testing repository in order to install *Percona Server for MySQL*
for MySQL 8.0.12-2rc1.  For manual installations, you can download from the
[testing repository directly through our website](https://www.percona.com/downloads/TESTING/Percona-Server-80-rc1/).

## New Features


* [#4550](https://jira.percona.com/browse/PS-4550): Native Partitioning support for MyRocks storage engine


* [#3911](https://jira.percona.com/browse/PS-3911): Native Partitioning support for TokuDB storage engine


* [#4946](https://jira.percona.com/browse/PS-4946): Add an option to prevent implicit creation of column family in
MyRocks


* [#4839](https://jira.percona.com/browse/PS-4839): Better default configuration for MyRocks and TokuDB


* InnoDB changed page tracking has been rewritten to account for redo logging
changes in MySQL 8.0.11.  This fixes fast incremental backups for PS 8.0


* [#4434](https://jira.percona.com/browse/PS-4434): TokuDB ROW_FORMAT clause has been removed, compression may be
set by using the session variable `tokudb_row_format` instead.

## Improvements


* Several packaging changes to bring Percona packages more in line with
upstream, including split repositories. As you’ll note from our instructions
above we now ship a tool with our release packages to help manage this.

## Bugs Fixed


* [#4785](https://jira.percona.com/browse/PS-4785): Setting version_suffix to **NULL** could lead to
*handle_fatal_signal* (sig=11) in *Sys_var_version::global_value_ptr*


* [#4788](https://jira.percona.com/browse/PS-4788): Setting *log_slow_verbosity* and enabling the *slow_query_log*
could lead to a server crash


* [#4937](https://jira.percona.com/browse/PS-4937): Any index comment generated a new column family in MyRocks


* [#1107](https://jira.percona.com/browse/PS-1107): Binlog could be corrupted when *tmpdir* got full


* [#1549](https://jira.percona.com/browse/PS-1549): Server side prepared statements lead to a potential
off-by-second timestamp on slaves


* [#4937](https://jira.percona.com/browse/PS-4937): `rocksdb_update_cf_options` was useless when specified in
my.cnf or on command line.


* [#4705](https://jira.percona.com/browse/PS-4705): The server could crash on snapshot size check in RocksDB


* [#4791](https://jira.percona.com/browse/PS-4791): SQL injection on slave due to non-quoting in binlogged
`ROLLBACK TO SAVEPOINT`


* [#4953](https://jira.percona.com/browse/PS-4953): *rocksdb.truncate_table3* was unstable

Other bugs fixed:


* [#4811](https://jira.percona.com/browse/PS-4811): 5.7 Merge and fixup for old DB-937 introduces possible
regression


* [#4885](https://jira.percona.com/browse/PS-4885): `Using ALTER ... ROW_FORMAT=TOKUDB_QUICKLZ` lead to InnoDB:
Assertion failure: `ha_innodb.cc:12198:m_form->s->row_type ==
m_create_info->row_type`


* Numerous testsuite failures/crashes

## Upcoming Features


* New encryption features in *Percona Server for MySQL* 5.7 will be ported forward to *Percona Server for MySQL* 8.0


* Adding back in [column compression with custom data dictionaries](https://www.percona.com/doc/percona-server/8.0/flexibility/compressed_columns.html)
and expanded fast index creation.
