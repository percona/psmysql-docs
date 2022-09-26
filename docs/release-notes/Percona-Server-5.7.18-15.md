# Percona Server for MySQL 5.7.18-15 (2017-05-26)

Percona is glad to announce the GA (Generally Available) release of *Percona Server for MySQL* 5.7.18-15 on May 26, 2017 (Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.18-15/)
and from the Percona Software Repositories).

Based on [MySQL 5.7.18](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-18.html), including
all the bug fixes in it, *Percona Server for MySQL* 5.7.18-15 is the current GA release
in the *Percona Server for MySQL* 5.7 series. All of Percona’s software is open-source
and free, all the details of the release can be found in the [5.7.18-15
milestone at
Launchpad](https://launchpad.net/percona-server/+milestone/5.7.18-15)

## Bugs Fixed

The server could crash when querying the partitioning table with a single partition.
Bug fixed [#1657941](https://bugs.launchpad.net/percona-server/+bug/1657941) (upstream [#76418](http://bugs.mysql.com/bug.php?id=76418)).

Running a query on the InnoDB table with [ngram full-text parser](https://dev.mysql.com/doc/refman/5.7/en/fulltext-search-ngram.html) and a `LIMIT` clause could lead to a server crash. Bug fixed [#1679025](https://bugs.launchpad.net/percona-server/+bug/1679025)
(upstream [#85835](http://bugs.mysql.com/bug.php?id=85835)).
