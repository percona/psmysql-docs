# Percona Server for MySQL 5.7.35-38 (2021-08-18)

* **Installation**  [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/5.7/installation.html)

[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 5.7.35-38
includes all the features and bug fixes available in
[MySQL 5.7.35 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-35.html)
in addition to [enterprise-grade features](https://www.percona.com/software/mysql-database/percona-server/feature-comparison) developed by Percona.

## Bugs Fixed

* [PS-1346](https://jira.percona.com/browse/PS-1346): LP #1163232: Anomaly with `opt_log_slow_slave_statements`.

* [PS-1344](https://jira.percona.com/browse/PS-1344): LP #1160436: The `log_slow_statement` is called unconditionally

* [PS-7582](https://jira.percona.com/browse/PS-7582): Segmentation fault with the data masking plugin

* [PS-1108](https://jira.percona.com/browse/PS-1108): LP #1704163: Changing a column from uncompressed to compressed for JSON crashes the server

* [PS-2433](https://jira.percona.com/browse/PS-2433): LP #1234346: Include a timestamp in the slow query log file when initializing a new file

* [PS-1955](https://jira.percona.com/browse/PS-1955): LP #1088529: The `log_slow_verbosity` help text missing the “minimal”, “standard”, and “full” options

* [PS-1116](https://jira.percona.com/browse/PS-1116): LP #1719506: Audit plugin reports “command_class=error” for server-side prepared statements.

* [PS-7755](https://jira.percona.com/browse/PS-7755): InnoDB: tried to purge `non-delete-marked` record (Upstream [#86485](http://bugs.mysql.com/bug.php?id=86485)).

* [PS-6802](https://jira.percona.com/browse/PS-6802): Configure fails with make-4.3 with CMake Error at storage/rocksdb/CMakeLists.txt:152 (STRING) (Thanks to user whissi for reporting this issue)

* [PS-1659](https://jira.percona.com/browse/PS-1659): LP #1508909: Connect without proxy information hangs if `proxy_protocol_networks` is enabled

* [PS-7746](https://jira.percona.com/browse/PS-7746): Possible double call to free_share() in ha_innobase::open()
