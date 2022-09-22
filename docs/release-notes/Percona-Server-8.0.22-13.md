# Percona Server for MySQL 8.0.22-13 (2020-12-14)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/8.0/installation.html)


[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.22-13
includes all the features and bug fixes available in
[MySQL 8.0.22 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-22.html)
in addition to enterprise-grade features developed by Percona.

## New Features


* [PS-7162](https://jira.percona.com/browse/PS-7162): Implement user-defined functions for Point-in-time Recovery in PXC operator

## Improvements


* [PS-7348](https://jira.percona.com/browse/PS-7348): Create a set of C++ classes/macros that would simplify the creation of new user-defined functions

## Bugs Fixed


* [PS-7346](https://jira.percona.com/browse/PS-7346): Correct the buffer calculation for the audit plugin used when large queries are executed(PS-5395).


* [PS-7300](https://jira.percona.com/browse/PS-7300): Modify Session temporary tablespace truncation on connection disconnect to reduce high CPU usage (Upstream [#98869](http://bugs.mysql.com/bug.php?id=98869))


* [PS-7304](https://jira.percona.com/browse/PS-7304): Correct package to include coredumper.a as a dependency of libperconaserverclient20-dev (Thanks to user Martin for reporting this issue)


* [PS-7236](https://jira.percona.com/browse/PS-7236): Correct grouping by GROUP BY processing with timezone (Thanks to user larrabee for reporting this issue) (Upstream [#101105](http://bugs.mysql.com/bug.php?id=101105))


* [PS-7286](https://jira.percona.com/browse/PS-7286): Modify to check for boundaries for encryption_key_id


* [PS-7317](https://jira.percona.com/browse/PS-7317): Add explicit_default_counter=10000 to innodb.table_encrypt_\* MTR tests
