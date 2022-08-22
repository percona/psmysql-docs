# Percona Server 5.7.23-23 (2018-09-12)

Percona is glad to announce the release of Percona Server 5.7.23-23 on
September 12, 2018. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.23-23/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.23](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-23.html)
and includes all the bug fixes in it. *Percona Server for MySQL* 5.7.23-23 is
now the current GA (Generally Available) release in the 5.7 series.

All software developed by Percona is open-source and free.

## New Features

* The `max_binlog_files` variable is deprecated and replaced with
the `binlog_space_limit` variable. The behavior of `binlog_space_limit` is consistent with the variable `relay-log-space-limit` used for relay logs; both variables have the
same semantics. For more information, see [#275](https://jira.percona.com/browse/PS-275).

* Starting with 5.7.23-23, it is possible to encrypt all data in the InnoDB
system tablespace and in the parallel double write buffer. A new variable `innodb_sys_tablespace_encrypt` is introduced to encrypt the system
tablespace. This feature is considered **ALPHA** quality. The encryption of
the parallel double write buffer file is controlled by the variable `innodb_parallel_dblwr_encrypt`. Both variables are `OFF` by
default. For more information, see [#3822](https://jira.percona.com/browse/PS-3822).

* Changing the `rocksdb_update_cf_options` value returns any warnings and errors to the
client instead of printing them to the server error log. For more information,
see [#4258](https://jira.percona.com/browse/PS-4258).

* `rocksdb_number_stat_computers` and `rocksdb_rate_limit_delay_millis` variables have been removed. For
more information, see [#4780](https://jira.percona.com/browse/PS-4780).

* A number of new variables were introduced for MyRocks: `rocksdb_rows_filtered` to show the number of rows filtered out for
TTL in MyRocks tables, `rocksdb_bulk_load_allow_sk` to allow adding
secondary keys using the bulk loading feature, `rocksdb_error_on_suboptimal_collation` toggling warning or error
in case of an index creation on a char field where the table has a sub-optimal
collation, `rocksdb_stats_recalc_rate` specifying the number of
indexes to recalculate per second, `rocksdb_commit_time_batch_for_recovery`
toggler of writing the
commit time write batch into the database,
and `rocksdb_write_policy` specifying when two-phase commit data are
actually written into the database.

## Bugs Fixed

* The statement `SELECT...ORDER BY` produced inconsistent results with the
`euckr` charset or `euckr_bin` collation. Bug fixed [#4513](https://jira.percona.com/browse/PS-4513)
(upstream [#91091](http://bugs.mysql.com/bug.php?id=91091)).

* InnoDB statistics could incorrectly report zeros in the slow query log. Bug fixed [#3828](https://jira.percona.com/browse/PS-3828).

* With the FIPS mode enabled and performance_schema=off, the instance crashed
when running the `CREATE VIEW` command. Bug fixed [#3840](https://jira.percona.com/browse/PS-3840).

* The soft limit of the core file size was set incorrectly starting with Percona Server for MySQL `5.7.21-20`. Bug fixed [#4479](https://jira.percona.com/browse/PS-4479).

* The option `innodb-optimize-keys` could fail when a dumped table has two
columns such that the name of one of them contains the other as as a prefix and
is defined with the AUTO_INCREMENT attribute. Bug fixed [#4524](https://jira.percona.com/browse/PS-4524).

* When `innodb_temp_tablespace_encrypt` was set to `ON` the `CREATE TABLE`
command could ignore the value of the `ENCRYPTION` option. Bug fixed
[#4565](https://jira.percona.com/browse/PS-4565).

* If `FLUSH STATUS` was run from a different session, a statement could be
counted twice in `GLOBAL STATUS`. Bug fixed [#4570](https://jira.percona.com/browse/PS-4570) (upstream
[#91541](http://bugs.mysql.com/bug.php?id=91541)).

* In some cases, it was not possible to set the `flush_caches` variable on systems that use systemd. Bug fixed [#3796](https://jira.percona.com/browse/PS-3796).

* A message in the MyRocks log file did not clearly inform whether fast CRC32
was supported. Bug fixed [#3988](https://jira.percona.com/browse/PS-3988).

* `mysqld` could not be started on Ubuntu if the database recovery had taken
longer than ten minutes. Bug fixed [#4546](https://jira.percona.com/browse/PS-4546) (upstream [#91423](http://bugs.mysql.com/bug.php?id=91423)).

* The ALTER TABLE command was slow when the number of dirty pages was high. Bug fixed
[#3702](https://jira.percona.com/browse/PS-3702).

* Setting the global variable `version_suffix` to NULL could
lead to a server crash. Bug fixed [#4785](https://jira.percona.com/browse/PS-4785).

* When more space was added to the data partition after the error that the disk
partition was full, MyRocks could ignore data update commands. Bug fixed
[#4706](https://jira.percona.com/browse/PS-4706).

## Other Bugs Fixed

* [#4620](https://jira.percona.com/browse/PS-4620) "Enable encryption of temporary tablespace from foreground thread"

* [#4727](https://jira.percona.com/browse/PS-4727) "intrinsic temp table behaviour shouldn't depend on innodb_encrypt_tables"

* [#4046](https://jira.percona.com/browse/PS-4046) "Ship assert failure: 'res == 0' (bulk loader)"

* [#3851](https://jira.percona.com/browse/PS-3851) "Percona Ver 5.6.39-83.1 Failing assertion: sym_node->table != NULL"

* [#4533](https://jira.percona.com/browse/PS-4533) "audit_log MTR tests should refer to include files without parent directories"

* [#4619](https://jira.percona.com/browse/PS-4619) "main.flush_read_lock fails with timeout in wait_condition.inc."

* [#4561](https://jira.percona.com/browse/PS-4561) "Read after free at Binlog_crypt_data::load_latest_binlog_key()"

* [#4587](https://jira.percona.com/browse/PS-4587) "ROCKSDB_INCLUDE_RFR macro in wrong file"