# Percona Server for MySQL 8.0.21-12 (2020-10-13)

* **Installation** [Installing Percona Server for MySQL](https://www.percona.com/doc/percona-server/8.0/installation.html)


[Percona Server for MySQL](https://www.percona.com/software/mysql-database/percona-server) 8.0.21-12
includes all the features and bug fixes available in
[MySQL 8.0.21 Community Edition](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-21.html)
in addition to enterprise-grade features developed by Percona.

This release fixes the security vulnerability [CVE-2020-26542](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-26542).

## Improvements


* [PS-7132](https://jira.percona.com/browse/PS-7132): Make default value of rocksdb_wal_recovery_mode compatible with InnoDB


* [PS-7245](https://jira.percona.com/browse/PS-7245): Block enable/disable redo log with lock tables for backup


* [PS-5730](https://jira.percona.com/browse/PS-5730): Change SELECT rotate_system_key to ALTER INSTANCE for percona system key rotation.


* [PS-7297](https://jira.percona.com/browse/PS-7297): Modify MTR test to prevent proxy_protocol_admin_port test failure on 8.0.21


* [PS-7114](https://jira.percona.com/browse/PS-7114): Enhance crash artifacts (core dumps and stack traces) to provide additional information to the operator


* [PS-5635](https://jira.percona.com/browse/PS-5635): Introduce crypt_schema 2 for better error checking in encryption threads.

## Bugs Fixed


* [PS-7203](https://jira.percona.com/browse/PS-7203): Fix audit plugin memory leak on replicas when opening tables


* [PS-6067](https://jira.percona.com/browse/PS-6067): Provide a fix for upstream bug #97001 in Percona Server (Upstream [#97001](http://bugs.mysql.com/bug.php?id=97001))


* [PS-7325](https://jira.percona.com/browse/PS-7325): Modify SELECT to correct situation when data is missing from MyRocks table when GROUP BY is used


* [PS-7275](https://jira.percona.com/browse/PS-7275): Add variable Innodb_checkpoint_max_age


* [PS-7232](https://jira.percona.com/browse/PS-7232): Modified Multithreaded Replica to correct the exhausted slave_transaction_retries when replica has slave_preserve_commit_order enabled (Upstream [#99440](http://bugs.mysql.com/bug.php?id=99440))


* [PS-7231](https://jira.percona.com/browse/PS-7231): Modify Slave_transaction::retry_transaction() to call mysql_errno() only when thd->is_error() is true


* [PS-7221](https://jira.percona.com/browse/PS-7221): Modify get_int_sort_key_for_item_inline to return UTC string (Upstream [#100402](http://bugs.mysql.com/bug.php?id=100402))


* [PS-7143](https://jira.percona.com/browse/PS-7143): Suppress deadlock check for ACL Cache MDL lock to prevent server freeze


* [PS-7076](https://jira.percona.com/browse/PS-7076): Modify to not update Cardinality after setting tokudb_cardinality_scale_percent


* [PS-7025](https://jira.percona.com/browse/PS-7025): Fix reading ahead of insert buffer pages by dispatching of buffered AIO transfers (Upstream [#100086](http://bugs.mysql.com/bug.php?id=100086))


* [PS-7010](https://jira.percona.com/browse/PS-7010): Modify to Lock buffer blocks before sanity check in btr_cur_latch_leaves


* [PS-6995](https://jira.percona.com/browse/PS-6995): Introduce a new optimizer switch to allow the user to reduce the cost of a range scan to determine best execution plan for Primary Key lookup


* [PS-7279](https://jira.percona.com/browse/PS-7279): Modify to notify when BuildID: Not Available in case the server has been compiled with –build-id=none


* [PS-7220](https://jira.percona.com/browse/PS-7220): Fix activity counter update in purge coordinator and workers


* [PS-7169](https://jira.percona.com/browse/PS-7169): Set rocksdb_validate_tables to disabled RocksDB while upgrading the server from 5.7 to 8.0.20


* [PS-5741](https://jira.percona.com/browse/PS-5741): Correct format for use of memset_s in keyring_vault


* [PS-5323](https://jira.percona.com/browse/PS-5323): Align Keyring encryption with Master Key encryption


* [PS-7363](https://jira.percona.com/browse/PS-7363): Modify to release locks on failure to prevent deadlock with LTFB + DROP UNDO TABLESPACE


* [PS-7360](https://jira.percona.com/browse/PS-7360): Modify clang-4.0 compilation to correct failure from ‘-Winconsistent-missing-destructor-override’


* [PS-7359](https://jira.percona.com/browse/PS-7359): Stabilize innodb.check_ibd_filesize_16k MTR test


* [PS-7353](https://jira.percona.com/browse/PS-7353): Modify LDAP connection to server to be static to prevent connection failures which will lock mysqld


* [PS-7352](https://jira.percona.com/browse/PS-7352): Correct typo in authentication_ldap_simple_ca_path to correct crash of mysqld


* [PS-7340](https://jira.percona.com/browse/PS-7340): Add validation of default_table_encryption to confirm keyring plugin is loaded before changing modes


* [PS-7338](https://jira.percona.com/browse/PS-7338): Set set crypt_data based on encryption status of destination table


* [PS-7328](https://jira.percona.com/browse/PS-7328): Block create/alter/drop/undo truncation while backup lock is available and hold lock until operation is completed


* [PS-7322](https://jira.percona.com/browse/PS-7322): Modify the right mask length calculation to handle up to string length for Data Masking


* [PS-7321](https://jira.percona.com/browse/PS-7321): Correct Random Number Generator to create only 15 or 16 digit number in Data Masking


* [PS-7309](https://jira.percona.com/browse/PS-7309): Modify gen_range() to support negative numbers in Data Masking


* [PS-7308](https://jira.percona.com/browse/PS-7308): Modify limit gen_dictionary_load() to load files only from the secure-file-priv dir when secure-file-priv dir is set in Data Masking


* [PS-7307](https://jira.percona.com/browse/PS-7307): Modify Data masking UDFs to display output using Latin1 character set


* [PS-7296](https://jira.percona.com/browse/PS-7296): Fix online log tracking initialization to properly process existing bitmap files


* [PS-7289](https://jira.percona.com/browse/PS-7289): Restrict innodb encryption threads to 255 and add min/max values


* [PS-7270](https://jira.percona.com/browse/PS-7270): Fix admin_port to accept non-proxied connections when proxy_protocol_networks=’\*’


* [PS-7234](https://jira.percona.com/browse/PS-7234): Modify PS minimal tarballs to remove COPYING.AGPLv3


* [PS-7226](https://jira.percona.com/browse/PS-7226): Modify LDAP Plugin to enhance logging and test cases


* [PS-7191](https://jira.percona.com/browse/PS-7191): Correct documentation for PS variable default_table_encryption


* [PS-7147](https://jira.percona.com/browse/PS-7147): Modified Relay_log_info::cannot_safely_rollback() to handle null pointer


* [PS-7140](https://jira.percona.com/browse/PS-7140): Correct processing to apply crypt redo logs


* [PS-7120](https://jira.percona.com/browse/PS-7120): Handle doublewrite buffer encryption for keyring key tablespaces


* [PS-7119](https://jira.percona.com/browse/PS-7119): Correct Tests of encryption.innodb_encryption_aborted_rotation\* to prevent failure


* [PS-6987](https://jira.percona.com/browse/PS-6987): Modify to allow value of default_table_encryption to be changed only when encryption_threads are off


* [PS-7284](https://jira.percona.com/browse/PS-7284): Fix failing test innodb.percona_changed_page_bmp_requests_debug
