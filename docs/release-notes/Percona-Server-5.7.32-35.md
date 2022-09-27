# Percona Server for MySQL 5.7.32-35 (2020-11-24)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/5.7/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.32-35
includes all the features and bug fixes available in
[MySQL 5.7.32 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-32.html)
in addition to enterprise-grade features developed by Percona.

## New Features

* [PS-7238](https://jira.percona.com/browse/PS-7238): Backport Data Masking plugin to 5.7 (Thanks to user Surenda Kumar Gupta for reporting this issue)

## Bugs Fixed

* [PS-7346](https://jira.percona.com/browse/PS-7346): Correct the buffer calculation for the audit plugin used when large queries are executed(PS-5395).

* [PS-7232](https://jira.percona.com/browse/PS-7232): Modify Multithreaded Replica to correct the exhausted slave_transaction_retries when replica has slave_preserve_commit_order enabled (Upstream [#99440](http://bugs.mysql.com/bug.php?id=99440))

* [PS-7231](https://jira.percona.com/browse/PS-7231): Modify Slave_transaction::retry_transaction() to call mysql_errno() only when thd->is_error() is true

* [PS-7304](https://jira.percona.com/browse/PS-7304): Correct package to include coredumper.a as a dependency of libperconaserverclient20-dev (Thanks to user Martin for reporting this issue)

* [PS-7289](https://jira.percona.com/browse/PS-7289): Restrict innodb encryption threads to 255 and add min/max values

* [PS-7270](https://jira.percona.com/browse/PS-7270): Fix admin_port to accept non-proxied connections when proxy_protocol_networks=’\*’
