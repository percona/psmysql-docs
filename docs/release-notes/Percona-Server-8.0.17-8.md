# Percona Server for MySQL 8.0.17-8

*Percona* announces the release of *Percona Server for MySQL* 8.0.17-8 on October 30, 2019
(downloads are available [here](https://www.percona.com/downloads/Percona-Server-8.0/) and from the
[Percona Software Repositories](https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries)).

This release includes fixes to bugs found in previous releases of *Percona Server for MySQL* 8.0.

*Percona Server for MySQL* 8.0.17-8 is now the current GA release in the 8.0 series. All
of *Percona*’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the [features available in MySQL
8.0.17 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-17.html) in
addition to enterprise-grade features developed by Percona.

## New Features

*Percona Server for MySQL* has implemented the ability to have a *MySQL*
Utility user who has system access to do administrative tasks but limited
access to user schemas. The user is invisible to other users. This feature is
especially useful to those who are operating *MySQL* as a Service. This feature
has the same functionality as the utility user in earlier versions and has been
delay-ported to version 8.0.

*Percona Server for MySQL* has implemented [data masking](https://docs.percona.com/percona-server/8.0/data-masking-overview.html) .

## Bugs Fixed


* Changed the default of innodb_empty_free_list_algorithm to
`backoff`. Bugs fixed [#5881](https://jira.percona.com/browse/PS-5881)


* When the Adaptive Hash Index (AHI) was enabled or disabled, there was an AHI
overhead during DDL operations. Bugs fixed [#5747](https://jira.percona.com/browse/PS-5747).


* An upgrade to Percona Server for MySQL 8.0.16-7 with encrypted tablespace fails on
innodb_dynamic_metadata. Bugs fixed [#5874](https://jira.percona.com/browse/PS-5874).


* The `rocksdb.ttl_primary` test case sometimes fails. Bugs fixed
[#5722](https://jira.percona.com/browse/PS-5722) (Louis Hust)


* The `rocksdb.ns_snapshot_read_committed` test case sometimes fails. Bugs
fixed [#5798](https://jira.percona.com/browse/PS-5798) (Louis Hust).


* During a binlogging replication event, if the master crashes after the
multi-threaded slave has begun copying to the slave’s relay log and before the
process has completed, a `STOP SLAVE` on the slave takes longer than expected.
Bugs fixed [#5824](https://jira.percona.com/browse/PS-5824).


* The purpose of the [sql_require_primary_key](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)
option is to avoid replication performance issues. Temporary tables are not
replicated. The option cannot be used with temporary tables. Bugs fixed
[#5931](https://jira.percona.com/browse/PS-5931).


* When using `skip-innodb_doublewrite` in my.cnf, a parallel doublewrite
buffer is still created. Bugs fixed [#3411](https://jira.percona.com/browse/PS-3411).


* The metadata for every InnoDB table contains encryption information, either a
‘Y’ or an ‘N’ value based on the ENCRYPTION clause or the
default_table_encryption value. You are unable to switch the storage
engine from InnoDB to MyRocks because MyRocks does not support the ENCRYPTION
clause. Bugs fixed [#5865](https://jira.percona.com/browse/PS-5865).


* MyRocks does not allow index condition pushdown optimization for specific data
types, such as `varchar`.  Bugs fixed [#5024](https://jira.percona.com/browse/PS-5024).

Other bugs fixed: [#5880](https://jira.percona.com/browse/PS-5880), [#5838](https://jira.percona.com/browse/PS-5838), [#5682](https://jira.percona.com/browse/PS-5682),
[#5979](https://jira.percona.com/browse/PS-5979), [#5793](https://jira.percona.com/browse/PS-5793), [#6020](https://jira.percona.com/browse/PS-6020), [#5327](https://jira.percona.com/browse/PS-5327),
[#5839](https://jira.percona.com/browse/PS-5839), [#5933](https://jira.percona.com/browse/PS-5933), [#5939](https://jira.percona.com/browse/PS-5939), [#5659](https://jira.percona.com/browse/PS-5659), [#5924](https://jira.percona.com/browse/PS-5924),
[#5926](https://jira.percona.com/browse/PS-5926), [#5925](https://jira.percona.com/browse/PS-5925), [#5875](https://jira.percona.com/browse/PS-5875), [#5533](https://jira.percona.com/browse/PS-5533),
[#5867](https://jira.percona.com/browse/PS-5867), [#5864](https://jira.percona.com/browse/PS-5864), [#5760](https://jira.percona.com/browse/PS-5760), [#5909](https://jira.percona.com/browse/PS-5909), [#5985](https://jira.percona.com/browse/PS-5985),
[#5941](https://jira.percona.com/browse/PS-5941), [#5954](https://jira.percona.com/browse/PS-5954), [#5790](https://jira.percona.com/browse/PS-5790), and [#5593](https://jira.percona.com/browse/PS-5593).
