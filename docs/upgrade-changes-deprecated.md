# Deprecated in MySQL 8.0

The utf8mb3 character set is deprecated. Please use utf8mb4 instead. The utf8mb3 character set is valid in MySQL 8.0, however, it is recommended to use utf8mb4 for the improved Unicode support. Review [Migrating to utf8mb4: Things to consider] for more information.

The `caching_sha2_password` is the default authentication plugin in MySQL 8.0 and provides a superset of the capabilities of the `sha256_password` authentication plugin. The `sha256_password` is deprecated. The new default authentication plugin 'caching_sha2_password' offers more secure password hashing and improved client connection authentication than the previously used 'mysql_native_password'.
The existing users that are created with `mysql_native_password` plugin can still be used and logged in to the DB. The new users will be created with `caching_sha2_password` plugin if you don't change the default authentication plugin.

The mysql_upgrade client is deprecated because its capabilities for upgrading the system tables in the mysql system schema and objects in other schemas have been moved into the MySQL server.
As of MySQL 8.0.16, the server performs all tasks previously handled by mysql_upgrade.
The upgrade process automatically starts by running a new MySQL binary with an older data directory. 
The mysql_upgrade_info file, which creates a text file in the data directory and used to store the MySQL version number.
In data_directory, new InnoDB files are created. 

After installing a new MySQL version, the server now automatically performs all necessary upgrade tasks at the next startup and is not dependent on the DBA invoking mysql_upgrade.

In addition, the server updates the contents of the help tables (something `mysql_upgrade` did not do). 
A new [upgrade option] provides control over how the server performs automatic data dictionary and server upgrade operations at startup. The validate_password plugin has been reimplemented to use the server component infrastructure. The plugin form of validate_password is still available but is deprecated.

The ENGINE clause for the ALTER TABLESPACE and DROP TABLESPACE statements.
The PAD_CHAR_TO_FULL_LENGTH SQL mode.
AUTO_INCREMENT support is deprecated for columns of type FLOAT and DOUBLE (and any synonyms). Consider removing the AUTO_INCREMENT attribute from such columns, or convert them to an integer type.
The UNSIGNED attribute is deprecated for columns of type FLOAT, DOUBLE, and DECIMAL (and any synonyms). Consider using a simple CHECK constraint instead for such columns.
FLOAT(M,D) and DOUBLE(M,D) syntax to specify the number of digits for columns of type FLOAT and DOUBLE (and any synonyms) is a nonstandard MySQL extension. This syntax is deprecated.
The nonstandard C-style &&, ||, and ! operators that are synonyms for the standard SQL AND, OR, and NOT operators, respectively, are deprecated. Applications that use the nonstandard operators should be adjusted to use the standard operators.

The relay_log_info_file system variable and –master-info-file option are deprecated. Previously, these were used to specify the name of the relay log info log and master info log when relay_log_info_repository=FILE and master_info_repository=FILE were set, but those settings have been deprecated. The use of files for the relay log info log and master info log has been superseded by crash-safe slave tables, which are the default in MySQL 8.0.
The use of the MYSQL_PWD environment variable to specify a MySQL password is deprecated.


[Migrating to utf8mb4: Things to consider]: https://www.percona.com/blog/migrating-to-utf8mb4-things-to-consider/

[upgrade option]: https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_upgrade
