# Removed in MySQL 8.0

The `innodb_locks_unsafe_for_binlog` system variable is removed. The `READ COMMITTED` isolation level provides similar functionality.

Using `GRANT` to create users. Instead, use `CREATE USER`. Following this practice makes the `NO_AUTO_CREATE_USER` SQL mode immaterial for `GRANT` statements, so it too is removed, and an error now is written to the server log when the presence of this value for the `sql_mode` option in the options file prevents mysqld from starting. 

Using `GRANT` to modify account properties other than privilege assignments. This includes authentication, SSL, and resource-limit properties. Instead, establish such properties at account-creation time with `CREATE USER` or modify them afterward with `ALTER USER`.

IDENTIFIED BY PASSWORD ‘auth_string’ syntax for CREATE USER and GRANT. Instead, use IDENTIFIED WITH auth_plugin AS ‘auth_string’ for CREATE USER and ALTER USER, where the ‘auth_string’ value is in a format compatible with the named plugin. 

The PASSWORD() function. 
Additionally, PASSWORD() removal means that SET PASSWORD … = PASSWORD(‘auth_string’) syntax is no longer available.
The old_passwords system variable.

The query cache was removed. Removal includes the following:
The FLUSH QUERY CACHE and RESET QUERY CACHE statements.
These system variables: query_cache_limit, query_cache_min_res_unit, query_cache_size, query_cache_type, query_cache_wlock_invalidate.
These status variables: Qcache_free_blocks, Qcache_free_memory, Qcache_hits, Qcache_inserts, Qcache_lowmem_prunes, Qcache_not_cached, Qcache_queries_in_cache, Qcache_total_blocks.

The removal of the query cache also removed the following thread states: 

* `checking privileges on cached query`
* `checking query cache for a query`
* `invalidating query cache entries`
* `sending cached result to the client`
* `storing result in the query cache`
* `Waiting for query cache lock`

The `tx_isolation` and `tx_read_only` system variables have been removed. Use transaction_isolation and transaction_read_only instead.

The `sync_frm` system variable is removed because .frm files are obsolete.

The secure_auth system variable and –secure-auth client option have been removed. The MYSQL_SECURE_AUTH option for the mysql_options() C API function was removed.
The log_warnings system variable and –log-warnings server option have been removed. Use the log_error_verbosity system variable instead.
The global scope for the sql_log_bin system variable was removed. sql_log_bin has session scope only, and applications that rely on accessing @@GLOBAL.sql_log_bin should be adjusted.
The unused date_format, datetime_format, time_format, and max_tmp_tables system variables are removed.
The deprecated ASC or DESC qualifiers for GROUP BY clauses are removed. Queries that previously relied on GROUP BY sorting may produce results that differ from previous MySQL versions. To produce a given sort order, provide an ORDER BY clause.
The parser no longer treats N as a synonym for NULL in SQL statements. Use NULL instead. This change does not affect text file import or export operations performed with LOAD DATA or SELECT … INTO OUTFILE, for which NULL continues to be represented by N. 
The client-side –ssl and –ssl-verify-server-cert options have been removed. Use –ssl-mode=REQUIRED instead of –ssl=1 or –enable-ssl. Use –ssl-mode=DISABLED instead of –ssl=0, –skip-ssl, or –disable-ssl. Use –ssl-mode=VERIFY_IDENTITY instead of –ssl-verify-server-cert options.
The mysql_install_db program has been removed from MySQL distributions. Data directory initialization should be performed by invoking mysqld with the –initialize or –initialize-insecure option instead. In addition, the –bootstrap option for mysqld that was used by mysql_install_db was removed, and the INSTALL_SCRIPTDIR CMake option that controlled the installation location for mysql_install_db was removed.
The mysql_plugin utility was removed. Alternatives include loading plugins at server startup using the –plugin-load or –plugin-load-add option, or at runtime using the INSTALL PLUGIN statement.

The `resolveip` utility is removed. `nslookup`, host, or dig can be used instead.

Review [Features removed in MySQL 8.0] for more information

[Features removed in MySQL 8.0]: https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals
