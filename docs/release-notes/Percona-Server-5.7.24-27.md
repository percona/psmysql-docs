# Percona Server for MySQL 5.7.24-27 (2018-12-18)

Percona is glad to announce the release of *Percona Server for MySQL* 5.7.24-27 on
December 18, 2018. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.24-27/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.24](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-24.html)
and includes all the bug fixes in it. *Percona Server for MySQL* 5.7.24-27 is
now the current GA (Generally Available) release in the 5.7 series.

All software developed by Percona is open-source and free.

!!! note

    If you’re currently using *Percona Server for MySQL* 5.7, Percona recommends upgrading to this version of 5.7 prior to upgrading to *Percona Server for MySQL* 8.0.

## Bugs Fixed

* When uninstalling *Percona Server for MySQL* packages on *CentOS 7* default
configuration file `my.cnf` would get removed as well. This fix
makes the backup of the configuration file instead of removing it.
Bug fixed [#5092](https://jira.percona.com/browse/PS-5092).

