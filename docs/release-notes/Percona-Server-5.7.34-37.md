# Percona Server for MySQL 5.7.34-37 (2021-05-26)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/5.7/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.34-37
includes all the features and bug fixes available in
[MySQL 5.7.34 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-34.html)
in addition to enterprise-grade features developed by Percona.

## Bugs Fixed

* [PS-4497](https://jira.percona.com/browse/PS-4497): Incorrect option error message for mysqlbinlog

* [PS-7498](https://jira.percona.com/browse/PS-7498): Prevent the replication coordinator thread stuck in Waiting until MASTER_DELAY seconds after master executed event while handling partial relay log transactions. (Upstream [#102647](http://bugs.mysql.com/bug.php?id=102647))

* [PS-7578](https://jira.percona.com/browse/PS-7578): Replication failure with UPDATE when replica server has a PK and the source does not. (Upstream [#102628](http://bugs.mysql.com/bug.php?id=102628))

* [PS-7593](https://jira.percona.com/browse/PS-7593): When changing the tx-isolation on a session, after a transaction has executed, the change is not honored and may cause a service failure. (Upstream [#102831](http://bugs.mysql.com/bug.php?id=102831))

* [PS-7657](https://jira.percona.com/browse/PS-7657): An update query executed against partition tables with compressed columns can cause an unexpected server exit.
