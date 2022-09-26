# Percona Server for MySQL 8.0.18-9

*Percona* announces the release of *Percona Server for MySQL* 8.0.18-9 on December 11, 2019 (downloads are available [here](https://www.percona.com/downloads/Percona-Server-8.0/) and from the [Percona Software Repositories](https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries)).

This release includes fixes to bugs found in previous releases of *Percona Server for MySQL* 8.0.

*Percona Server for MySQL* 8.0.18-9 is now the current GA release in the 8.0 series. All
of *Percona*’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the [features available in MySQL
8.0.18 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-18.html) in
addition to enterprise-grade features developed by Percona.

## Bugs Fixed


* Setting the `none` value for slow_query_log_use_global_control
generates an error. Bugs fixed [#5813](https://jira.percona.com/browse/PS-5813).


* If [pam_krb5](https://docs.oracle.com/cd/E88353_01/html/E37853/pam-krb5-7.html) allows the
user to change their password, and the password expired, a new password may
cause a server exit. Bug fixed [#6023](https://jira.percona.com/browse/PS-6023).


* An incorrect assertion was triggered if any temporary tables should be logged
to binlog. This event may cause a server exit. Bug fixed [#5181](https://jira.percona.com/browse/PS-5181).


* The Handler failed to trigger on Error 1049, SQLSTATE 42000, or plain
sqlexception. Bug fixed [#6094](https://jira.percona.com/browse/PS-6094). (Upstream [#97682](http://bugs.mysql.com/bug.php?id=97682))


* When executing `SHOW GLOBAL STATUS`, the variables may return incorrect
values. Bug fixed [#5966](https://jira.percona.com/browse/PS-5966).


* The memory storage engine detected an incorrect `full` condition even
though the space contained reusable memory chunks released by deleted
records and the space could be reused. Bug fixed [#1469](https://jira.percona.com/browse/PS-1469).

Other bugs fixed:

[#6051](https://jira.percona.com/browse/PS-6051),
[#5876](https://jira.percona.com/browse/PS-5876),
[#5996](https://jira.percona.com/browse/PS-5996),
[#6021](https://jira.percona.com/browse/PS-6021),
[#6052](https://jira.percona.com/browse/PS-6052),
[#4775](https://jira.percona.com/browse/PS-4775),
[#5836](https://jira.percona.com/browse/PS-5836) (Upstream [#96449](http://bugs.mysql.com/bug.php?id=96449)),
[#6123](https://jira.percona.com/browse/PS-6123),
[#5819](https://jira.percona.com/browse/PS-5819),
[#5836](https://jira.percona.com/browse/PS-5836),
[#6054](https://jira.percona.com/browse/PS-6054),
[#6056](https://jira.percona.com/browse/PS-6056),
[#6058](https://jira.percona.com/browse/PS-6058),
[#6078](https://jira.percona.com/browse/PS-6078),
[#6057](https://jira.percona.com/browse/PS-6057),
[#6111](https://jira.percona.com/browse/PS-6111), and
[#6073](https://jira.percona.com/browse/PS-6073).
