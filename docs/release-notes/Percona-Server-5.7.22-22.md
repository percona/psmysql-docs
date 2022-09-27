# Percona Server 5.7.22-22 (2018-05-31)

Percona is glad to announce the release of Percona Server 5.7.22-22
on May 31, 2018. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.22-22/) and from the Percona Software Repositories.

This release is based on [MySQL 5.7.22](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-22.html) and includes all the bug fixes in it. *Percona Server for MySQL* 5.7.22-22 is now the current GA
(Generally Available) release in the 5.7 series.

All software developed by Percona is open-source and free.

## New Features

* A new `--encrypt-tmp-files` option turns on encryption for the temporary
files which  *Percona Server for MySQL* may create on disk for filesort, binary log
transactional caches and Group Replication caches.

## Bugs Fixed

* Executing the `SHOW GLOBAL STATUS` expression could cause “data drift” on
global status variables in case of a query rollback: the variable, being by
its nature a counter and allowing only an increase, could return to its
previous value. Bug fixed [#3951](https://jira.percona.com/browse/PS-3951) (upstream [#90351](http://bugs.mysql.com/bug.php?id=90351)).

* NUMA support was improved in *Percona Server for MySQL*, reverting upstream
implementation back to the original one, due to the upstream variant
being less effective in memory allocation. Now
[innodb_numa_interleave](http://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_numa_interleave)
variable not only enables NUMA interleave memory policy for the
InnoDB buffer pool allocation, but forces NUMA interleaved
allocation at the buffer pool initialization time. Bug fixed
[#3967](https://jira.percona.com/browse/PS-3967).

* `audit_log_include_accounts` variable did not take effect if
placed in `my.cnf` configuration file, while still working as intended if
set dynamically. Bug fixed [#3867](https://jira.percona.com/browse/PS-3867).

* A `key_block_size` value was set automatically by the Improved MEMORY
Storage Engine, which resulted in warnings when changing the engine type to
InnoDB, and constantly growing `key_block_size` during alter operations.
Bugs fixed [#3936](https://jira.percona.com/browse/PS-3936), [#3940](https://jira.percona.com/browse/PS-3940), and [#3943](https://jira.percona.com/browse/PS-3943).

* Fixes were introduced to remove GCC 8 compilation warnings for the
*Percona Server for MySQL* build. Bug fixed [#3950](https://jira.percona.com/browse/PS-3950).

* An InnoDB Memcached Plugin code clean-up was backported from MySQL 8.0. Bug
fixed [#4506](https://jira.percona.com/browse/PS-4506).

* *Percona Server for MySQL* could not be built with `-DWITH_LZ4=system` option on
Ubuntu 14.04 (Trusty) because of too old LZ4 packages. Bug fixed
[#3842](https://jira.percona.com/browse/PS-3842).

* A regression brought during TokuDB code clean-up in `5.7.21-21` was
causing assertion in cases when the FT layer returns an error during an alter
table operation. Bug fixed [#4294](https://jira.percona.com/browse/PS-4294).

## MyRocks Changes and Fixes

* `UPDATE` statements were returning incorrect results because of not making
a full table scan on tables with unique secondary index. Bug fixed
[#4495](https://jira.percona.com/browse/PS-4495) (upstream [Facebook/mysql-5.6#830](https://github.com/facebook/mysql-5.6/issues/830)).

## Other Bugs Fixed

* [#4451](https://jira.percona.com/browse/PS-4451) "Implement better compression algo testing"

* [#4469](https://jira.percona.com/browse/PS-4469) "variable use out of scope bug in get_last_key test detected by
ASAN in clang 6"

* [#4470](https://jira.percona.com/browse/PS-4470) "the cachetable-simple-pin-nonblocking-cheap test occasionally
fails due to a locking conflict with the cachetable evictor"

* [#4488](https://jira.percona.com/browse/PS-4488) "\`-Werror\` is always disabled for \`innodb_memcached\`"

* [#1114](https://jira.percona.com/browse/PS-1114) "Assertion \`inited == INDEX' failed"

* [#1130](https://jira.percona.com/browse/PS-1130) "RBR Replication with concurrent XA in READ-COMMITTED takes
supremum pseudo-records and breaks replication"
