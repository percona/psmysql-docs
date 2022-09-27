# Percona Server 5.7.19-17 (2017-08-31)

Percona is glad to announce the release of Percona Server 5.7.19-17
on August 31, 2017.
Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.19-17/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.19](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-19.html)
and includes all the bug fixes in it.
Percona Server 5.7.19-17 is now the current GA release in the 5.7 series.
All software developed by Percona is open-source and free.
Details of this release can be found in the [5.7.19-17 milestone on Launchpad](https://launchpad.net/percona-server/+milestone/5.7.19-17).

!!! note

    Red Hat Enterprise Linux 5 (including CentOS 5 and other derivatives), Ubuntu 12.04, and older versions are no longer supported by Percona software. The reason for this announcement is that these platforms have reached the end of life, will not receive updates, and are not recommended for use in production.

## New Features


* Included the Percona MyRocks storage engine

!!! note

    MyRocks for Percona Server is currently experimental and not recommended for production deployments until further notice. You are encouraged to try it in a testing environment and provide feedback or report bugs.


* [#1708087](https://bugs.launchpad.net/percona-server/+bug/1708087): Added the `mysql-helpers` script to handle checking for missing `datadir` during startup.
Also fixes [#1635364](https://bugs.launchpad.net/percona-server/+bug/1635364).

## Platform Support


* Stopped providing packages for Ubuntu 12.04 due to its end of life.

## Bugs Fixed


* [#1669414](https://bugs.launchpad.net/percona-server/+bug/1669414): Fixed handling of failure to set `O_DIRECT` on parallel doublewrite buffer file.

* [#1705729](https://bugs.launchpad.net/percona-server/+bug/1705729): Fixed the `postinst` script
to correctly locate the `datadir`.
Also fixes [#1698019](https://bugs.launchpad.net/percona-server/+bug/1698019).

* [#1709811](https://bugs.launchpad.net/percona-server/+bug/1709811): Fixed `yum upgrade` to not enable the `mysqld` service
if it was disabled before the upgrade.


* [#1709834](https://bugs.launchpad.net/percona-server/+bug/1709834): Fixed the `mysqld_safe` script
to correctly locate the `basedir`.


* Other fixes: [#1698996](https://bugs.launchpad.net/percona-server/+bug/1698996), [#1706055](https://bugs.launchpad.net/percona-server/+bug/1706055), [#1706262](https://bugs.launchpad.net/percona-server/+bug/1706262), [#1706981](https://bugs.launchpad.net/percona-server/+bug/1706981),
[#1686340](https://bugs.launchpad.net/percona-server/+bug/1686340) (upstream [#86799](http://bugs.mysql.com/bug.php?id=86799)), [#1654256](https://bugs.launchpad.net/percona-server/+bug/1654256) (upstream
[#84640](http://bugs.mysql.com/bug.php?id=84640)), and [#1651941](https://bugs.launchpad.net/percona-server/+bug/1651941) (upstream [#84442](http://bugs.mysql.com/bug.php?id=84442)).

## TokuDB Changes


* [TDB-70](https://jira.percona.com/browse/TDB-70): Removed redundant `fsync` of TokuDB redo log
during binlog group commit flush stage.
This fixes the issue that prevented TokuDB to run in reduced durability mode
when the binlog was enabled.


* [TDB-72](https://jira.percona.com/browse/TDB-72): Fixed issue when renaming a table
with non-alphanumeric characters in its name.
