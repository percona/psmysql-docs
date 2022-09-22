# Percona Server for MySQL 8.0.16-7

*Percona* announces the release of *Percona Server for MySQL* 8.0.16-7 on August 15, 2019
(downloads are available [here](https://www.percona.com/downloads/Percona-Server-8.0/) and from the [Percona
Software Repositories](https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries)).
This release includes fixes to bugs found in previous releases of *Percona Server for MySQL* 8.0.
*Percona Server for MySQL* 8.0.16-7 is now the current GA release in the 8.0
series. All of *Percona*’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the [features and bug fixes available in MySQL 8.0.16
Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-16.html) in addition to
enterprise-grade features developed by Percona.

## Encryption Features General Availability (GA)


* Encrypting Temporary Files


* Encrypting the Undo Tablespace


* Encrypting the System Tablespace


* default_table_encryption =OFF/ON


* `table_encryption_privilege_check`=OFF/ON


* Encrypting the Redo Log files for master key encryption only


* Merge-sort-encryption


* Encrypting Doublewrite Buffers

## Bugs Fixed


* Parallel doublewrite buffer writes must crash the server on an I/O error occurs. Bug fixed [#5678](https://jira.percona.com/browse/PS-5678).


* After resetting the innodb_temp_tablespace_encrypt to `OFF` during runtime the subsequent file-per-table temporary tables continue to be encrypted. Bug fixed [#5734](https://jira.percona.com/browse/PS-5734).


* Setting the encryption to `ON` for the system tablespace generates an encryption key and encrypts system temporary tablespace pages. Resetting the encryption to `OFF`, all subsequent pages are written to the temporary tablespace without encryption. To allow any encrypted tables to be decrypted, the generated keys are not erased. Modifying the innodb_temp_tablespace_encrypt does not affect file-per-table temporary tables. This type of table is encrypted if `ENCRYPTION` =’Y’ is set during table creation. Bug fixed [#5736](https://jira.percona.com/browse/PS-5736).


* An instance started with the default values but setting the redo-log without specifying the keyring plugin parameters does not fail or throw an error. Bug fixed [#5476](https://jira.percona.com/browse/PS-5476).


* The rocksdb_large_prefix allows index key prefixes up to 3072 bytes. The default value is changed to `TRUE` to match the behavior of the innodb_large_prefix. [#5655](https://jira.percona.com/browse/PS-5655).


* On a server with a large number of tables, a shutdown may take a measurable length of time. Bug fixed [#5639](https://jira.percona.com/browse/PS-5639).


* The changed page tracking uses the LOG flag during read operations. The redo log encryption may attempt to decrypt pages with a specific bit set and fail. This failure generates error messages. A NO_ENCRYPTION flag lets the read process safely disable decryption errors in this case. Bug fixed [#5541](https://jira.percona.com/browse/PS-5541).


* If large pages are enabled on MySQL side, the maximum size for innodb_buffer_pool_chunk_size is effectively limited to 4GB. Bug fixed [#5517](https://jira.percona.com/browse/PS-5517). (Upstream [94747](https://bugs.mysql.com/bug.php?id=94747))


* The TokuDB hot backup library continually dumps TRACE information to the server error log. The user cannot enable or disable the dump of this information. Bug fixed [#4850](https://jira.percona.com/browse/PS-4850).

Other bugs fixed:
[#5688](https://jira.percona.com/browse/PS-5688),
[#5723](https://jira.percona.com/browse/PS-5723),
[#5695](https://jira.percona.com/browse/PS-5695),
[#5749](https://jira.percona.com/browse/PS-5749),
[#5752](https://jira.percona.com/browse/PS-5752),
[#5610](https://jira.percona.com/browse/PS-5610),
[#5689](https://jira.percona.com/browse/PS-5689),
[#5645](https://jira.percona.com/browse/PS-5645),
[#5734](https://jira.percona.com/browse/PS-5734),
[#5772](https://jira.percona.com/browse/PS-5772),
[#5753](https://jira.percona.com/browse/PS-5753),
[#5129](https://jira.percona.com/browse/PS-5129),
[#5102](https://jira.percona.com/browse/PS-5102),
[#5681](https://jira.percona.com/browse/PS-5681),
[#5686](https://jira.percona.com/browse/PS-5686),
[#5681](https://jira.percona.com/browse/PS-5681),
[#5310](https://jira.percona.com/browse/PS-5310),
[#5713](https://jira.percona.com/browse/PS-5713),
[#5007](https://jira.percona.com/browse/PS-5007),
[#5102](https://jira.percona.com/browse/PS-5102),
[#5129](https://jira.percona.com/browse/PS-5129),
[#5130](https://jira.percona.com/browse/PS-5130),
[#5149](https://jira.percona.com/browse/PS-5149),
[#5696](https://jira.percona.com/browse/PS-5696),
[#3845](https://jira.percona.com/browse/PS-3845),
[#5149](https://jira.percona.com/browse/PS-5149),
[#5581](https://jira.percona.com/browse/PS-5581),
[#5652](https://jira.percona.com/browse/PS-5652),
[#5662](https://jira.percona.com/browse/PS-5662),
[#5697](https://jira.percona.com/browse/PS-5697),
[#5775](https://jira.percona.com/browse/PS-5775),
[#5668](https://jira.percona.com/browse/PS-5668),
[#5752](https://jira.percona.com/browse/PS-5752),
[#5782](https://jira.percona.com/browse/PS-5782),
[#5767](https://jira.percona.com/browse/PS-5767),
[#5669](https://jira.percona.com/browse/PS-5669),
[#5753](https://jira.percona.com/browse/PS-5753),
[#5696](https://jira.percona.com/browse/PS-5696),
[#5803](https://jira.percona.com/browse/PS-5803),
[#5804](https://jira.percona.com/browse/PS-5804),
[#5820](https://jira.percona.com/browse/PS-5820),
[#5827](https://jira.percona.com/browse/PS-5827),
[#5835](https://jira.percona.com/browse/PS-5835),
[#5724](https://jira.percona.com/browse/PS-5724),
[#5767](https://jira.percona.com/browse/PS-5767),
[#5782](https://jira.percona.com/browse/PS-5782),
[#5794](https://jira.percona.com/browse/PS-5794),
[#5796](https://jira.percona.com/browse/PS-5796),
[#5746](https://jira.percona.com/browse/PS-5746) and,
[#5748](https://jira.percona.com/browse/PS-5748).

## Known Issues


* [#5865](https://jira.percona.com/browse/PS-5865): *Percona Server for MySQL* 8.0.16-7 does not support encryption for the MyRocks storage engine. An attempt to move any table from InnoDB to [MyRocks](https://www.percona.com/doc/percona-server/LATEST/myrocks/limitations.html) fails as MyRocks currently sees all InnoDB tables as being encrypted.
