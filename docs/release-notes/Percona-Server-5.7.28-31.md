# Percona Server for MySQL 5.7.28-31 (2019-11-13)

Percona is glad to announce the release of *Percona Server for MySQL* 5.7.28-31 on November 13, 2019. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.28-31/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.28](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-28.html) and includes all the bug fixes in it. *Percona Server for MySQL* 5.7.28-31 is now the current GA
(Generally Available) release in the 5.7 series.

All software developed by Percona is open-source and free.

!!! note

    If you’re currently using *Percona Server for MySQL* 5.7, Percona recommends upgrading to this version of 5.7 prior to upgrading to *Percona Server for MySQL* 8.0.

## Bugs Fixed

* When using skip-innodb_doublewrite in my.cnf, a parallel doublewrite buffer is still created. Bugs fixed [#3411](https://jira.percona.com/browse/PS-3411).

* During a binlogging replication event, if the master crashes after the multi-threaded slave has begun copying to the slave’s relay log and before the process has completed, a STOP SLAVE on the slave takes longer than expected. Bug fixed [#5824](https://jira.percona.com/browse/PS-5824).

* If [pam_krb5](https://docs.oracle.com/cd/E88353_01/html/E37853/pam-krb5-7.html) is configured to allow the user to change their password, and the password expired, the server crashed after receiving the new password. Bug fixed [#6023](https://jira.percona.com/browse/PS-6023).

Other bugs fixed:
[#5859](https://jira.percona.com/browse/PS-5859),
[#5910](https://jira.percona.com/browse/PS-5910),
[#5966](https://jira.percona.com/browse/PS-5966),
[#4784](https://jira.percona.com/browse/PS-4784),
[#5216](https://jira.percona.com/browse/PS-5216),
[#5327](https://jira.percona.com/browse/PS-5327),
[#5584](https://jira.percona.com/browse/PS-5584),
[#5642](https://jira.percona.com/browse/PS-5642),
[#5659](https://jira.percona.com/browse/PS-5659),
[#5754](https://jira.percona.com/browse/PS-5754),
[#5761](https://jira.percona.com/browse/PS-5761),
[#5797](https://jira.percona.com/browse/PS-5797),
[#5875](https://jira.percona.com/browse/PS-5875),
[#5933](https://jira.percona.com/browse/PS-5933),
[#5941](https://jira.percona.com/browse/PS-5941),
[#5997](https://jira.percona.com/browse/PS-5997),
[#6050](https://jira.percona.com/browse/PS-6050),
[#6052](https://jira.percona.com/browse/PS-6052),
[#3345](https://jira.percona.com/browse/PS-3345), and
[#5585](https://jira.percona.com/browse/PS-5585)

## Known Issues

* [#5783](https://jira.percona.com/browse/PS-5783): The length of time and resources required for a MySQL query execution increased with a large number of table partitions. Limiting the Estimation of Records in a Query describes the experimental options added to prevent index scans on the partitions and return a specified number of values.
