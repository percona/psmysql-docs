# *Percona Server for MySQL* 5.7.26-29 (2019-05-27)

Percona is glad to announce the release of *Percona Server for MySQL* 5.7.26-29 on
May 27, 2019. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.26-29/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.26](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-26.html)
and includes all the bug fixes in it. *Percona Server for MySQL* 5.7.26-29 is
now the current GA (Generally Available) release in the 5.7 series.

## New Features

* New variable `Audit_log_buffer_size_overflow` status variable has been implemented to track when an Audit Log Plugin entry was either dropped or written directly to the file due to its size being bigger than `audit_log_buffer_size` variable.

## Bugs Fixed

* TokuDB storage engine would assert on load when used with jemalloc 5.x. Bug fixed [#5406](https://jira.percona.com/browse/PS-5406).

* A read-write workload on compressed InnoDB tables could cause an assertion error. Bug fixed [#3581](https://jira.percona.com/browse/PS-3581).

* Using TokuDB or MyRocks native partitioning and `index_merge` access method could lead to a server crash. Bugs fixed [#5206](https://jira.percona.com/browse/PS-5206), [#5562](https://jira.percona.com/browse/PS-5562).

* A stack buffer overrun could happen if the redo log encryption with key rotation was enabled. Bug fixed [#5305](https://jira.percona.com/browse/PS-5305).

* TokuDB and MyRocks native partitioning handler objects were allocated from a wrong memory allocator. Memory was released only on shutdown and concurrent access to global memory allocator caused memory corruptions and therefore
crashes. Bugs fixed [#5508](https://jira.percona.com/browse/PS-5508), [#5525](https://jira.percona.com/browse/PS-5525).

* Enabling redo log encryption resulted in redo log being written unencrypted. Bug fixed [#5547](https://jira.percona.com/browse/PS-5547).

* If there are multiple row versions in InnoDB, reading one row from PK may have O(N) complexity and reading from secondary keys may have O(N^2) complexity. Bugs fixed [#4712](https://jira.percona.com/browse/PS-4712), [#5450](https://jira.percona.com/browse/PS-5450) (upstream [#84958](http://bugs.mysql.com/bug.php?id=84958)).

* Setting the `log_slow_verbosity` to include `innodb` value and
enabling the `slow_query_log` could lead to a server crash. Bug fixed [#4933](https://jira.percona.com/browse/PS-4933).

* The page cleaner could sleep for long time when the system clock was adjusted to an earlier point in time. Bug fixed [#5221](https://jira.percona.com/browse/PS-5221) (upstream [#93708](http://bugs.mysql.com/bug.php?id=93708)).

* Executing `SHOW BINLOG EVENT` from an invalid position could result in a segmentation fault on 32bit machines. Bug fixed [#5243](https://jira.percona.com/browse/PS-5243).

* `BLOB` entries in the binary log could become corrupted in case when a database with `Blackhole` tables served as an
intermediate binary log server in a replication chain. Bug fixed
[#5353](https://jira.percona.com/browse/PS-5353) (upstream [#93917](http://bugs.mysql.com/bug.php?id=93917)).

* When Audit Log Plugin was enabled, the server could use a lot of memory when handling large queries.  Bug fixed [#5395](https://jira.percona.com/browse/PS-5395).

* XtraDB changed page tracking was missing pages changed by the in-place DDL.
Bug fixed [#5447](https://jira.percona.com/browse/PS-5447).

*  The `innodb_encrypt_tables` variable accepted `FORCE` option only
inside quotes as a string. Bug fixed [#5538](https://jira.percona.com/browse/PS-5538).

* Enabling redo log encryption and XtraDB changed page tracking together would result in the error log flooded with decryption errors. Bug fixed [#5541](https://jira.percona.com/browse/PS-5541).

* System keyring keys initialization wasn’t thread safe. Bugs fixed [#5554](https://jira.percona.com/browse/PS-5554).

* when using the Docker image, if the root passwords set in the mounted
`.cnf` file and the one specified with `MYSQL_ROOT_PASSWORD`
are different, password from the `MYSQL_ROOT_PASSWORD` will be used.
Bug fixed [#5573](https://jira.percona.com/browse/PS-5573).

* Long running `ALTER TABLE ADD INDEX` could cause a `semaphore wait > 600`
assertion. Bug fixed [#3410](https://jira.percona.com/browse/PS-3410) (upstream [#82940](http://bugs.mysql.com/bug.php?id=82940)).

Other bugs fixed:
[#5007](https://jira.percona.com/browse/PS-5007) (upstream [#93164](http://bugs.mysql.com/bug.php?id=93164)),
[#5018](https://jira.percona.com/browse/PS-5018),
[#5561](https://jira.percona.com/browse/PS-5561),
[#5570](https://jira.percona.com/browse/PS-5570),
[#5578](https://jira.percona.com/browse/PS-5578),
[#5610](https://jira.percona.com/browse/PS-5610),
[#5441](https://jira.percona.com/browse/PS-5441), and
[#5442](https://jira.percona.com/browse/PS-5442).

This release also contains the fixes for the following security issues:
CVE-2019-2632, CVE-2019-1559, CVE-2019-2628, CVE-2019-2581, CVE-2019-2683,
CVE-2019-2592, CVE-2019-262, and CVE-2019-2614.

