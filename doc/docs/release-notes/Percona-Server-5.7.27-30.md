# *Percona Server for MySQL* 5.7.27-30 (2019-08-22)

Percona is glad to announce the release of *Percona Server for MySQL* 5.7.27-30 on August 22, 2019. Downloads are available [here](http://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.27-30/)
and from the Percona Software Repositories.

This release is based on [MySQL 5.7.27](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-27.html) and includes all the bug fixes in it. *Percona Server for MySQL* 5.7.27-30 is now the current GA
(Generally Available) release in the 5.7 series.

All software developed by Percona is open-source and free.

!!! note

    If you’re currently using *Percona Server for MySQL* 5.7, Percona recommends upgrading to this version of 5.7 prior to upgrading to *Percona Server for MySQL* 8.0.

## Bugs Fixed

* Parallel doublewrite buffer writes must crash the server on an I/O error occurs. Bug fixed [#5678](https://jira.percona.com/browse/PS-5678).

* On a server with two million or more tables using foreign keys and AUTOINC columns, the shutdown may take a measurable length of time. Bug fixed [#5639](https://jira.percona.com/browse/PS-5639). (Upstream [#95895](http://bugs.mysql.com/bug.php?id=95895))

* If large pages are enabled on the MySQL side, the maximum size for `innodb_buffer_pool_chunk_size` is effectively limited to 4GB. Bug fixed [#5517](https://jira.percona.com/browse/PS-5517). (Upstream [#94747](http://bugs.mysql.com/bug.php?id=94747))

* The TokuDB hot backup library continually dumps TRACE information to the Server error log. The user cannot enable or disable the dump of this information. Bug fixed [#4850](https://jira.percona.com/browse/PS-4850).

* The TokuDBBackupPlugin is optional at cmake time. Bug fixed [#5748](https://jira.percona.com/browse/PS-5748).

* A multi-table `DELETE` with a foreign key breaks replication. Bug fixed [#3845](https://jira.percona.com/browse/PS-3845).

* A `TRUNCATE` with any table and interfacing with Adaptive Hash Index (AHI) can cause server stalls due to the interaction with AHI, whether the AHI is enabled or not. Bug fixed [#5576](https://jira.percona.com/browse/PS-5576). (Upstream [#94610](http://bugs.mysql.com/bug.php?id=94610))

* In specific configurations and with `log_slow_verbosity` set to log InnoDB statistics, memory usage increases while running a stored procedure.  Bug fixed [#5581](https://jira.percona.com/browse/PS-5581).

* Thread Pool functionality to track network I/O was disabled.  Bug fixed [#5723](https://jira.percona.com/browse/PS-5723).

* When Adaptive Hash Index (AHI) is enabled or disabled, there is an AHI overhead during DDL operations. Bug fixed [#5747](https://jira.percona.com/browse/PS-5747).

* An instance started with the default values but setting the redo-log to encrypt without specifying the keyring plugin parameters does not fail or throw an error. Bug fixed [#5476](https://jira.percona.com/browse/PS-5476).

* Setting the encryption to `ON` for the system tablespace generates the encryption key and encrypts system temporary tablespace pages. Resetting encryption to `OFF` , all subsequent pages are written to the temporary tablespace without encryption. To allow any encrypted tables to be decrypted, the generated keys are not erased. Modifying the `innodb_temp_tablespace_encrypt` does not affect file-per-table temporary tables. This type of table is encrypted if `ENCRYPTION` =’Y’ is set during the table creation. Bug fixed [#5736](https://jira.percona.com/browse/PS-5736).

* After resetting the  `innodb_temp_tablespace_encrypt` to `OFF` during runtime, the subsequent file-per-table temporary tables continue to be encrypted. Bug fixed [#5734](https://jira.percona.com/browse/PS-5734).

Other bugs fixed:
[#5752](https://jira.percona.com/browse/PS-5752),
[#5749](https://jira.percona.com/browse/PS-5749),
[#5746](https://jira.percona.com/browse/PS-5746),
[#5744](https://jira.percona.com/browse/PS-5744),
[#5743](https://jira.percona.com/browse/PS-5743),
[#5742](https://jira.percona.com/browse/PS-5742),
[#5740](https://jira.percona.com/browse/PS-5740),
[#5695](https://jira.percona.com/browse/PS-5695),
[#5681](https://jira.percona.com/browse/PS-5681),
[#5669](https://jira.percona.com/browse/PS-5669),
[#5645](https://jira.percona.com/browse/PS-5645),
[#5638](https://jira.percona.com/browse/PS-5638),
[#5593](https://jira.percona.com/browse/PS-5593),
[#5532](https://jira.percona.com/browse/PS-5532),
[#5790](https://jira.percona.com/browse/PS-5790),
[#5812](https://jira.percona.com/browse/PS-5812),
[#3970](https://jira.percona.com/browse/PS-3970),
[#5696](https://jira.percona.com/browse/PS-5696),
[#5689](https://jira.percona.com/browse/PS-5689),
[#5146](https://jira.percona.com/browse/PS-5146),
[#5715](https://jira.percona.com/browse/PS-5715),
[#5791](https://jira.percona.com/browse/PS-5791),
[#5662](https://jira.percona.com/browse/PS-5662),
[#5420](https://jira.percona.com/browse/PS-5420),
[#5149](https://jira.percona.com/browse/PS-5149),
[#5686](https://jira.percona.com/browse/PS-5686),
[#5688](https://jira.percona.com/browse/PS-5688),
[#5697](https://jira.percona.com/browse/PS-5697),
[#5716](https://jira.percona.com/browse/PS-5716),
[#5725](https://jira.percona.com/browse/PS-5725),
[#5773](https://jira.percona.com/browse/PS-5773),
[#5775](https://jira.percona.com/browse/PS-5775),
[#5820](https://jira.percona.com/browse/PS-5820), and
[#5839](https://jira.percona.com/browse/PS-5839).