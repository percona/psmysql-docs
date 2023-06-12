# General changes

MySQL now incorporates a transactional data dictionary that stores information about database objects.

An atomic DDL statement combines the data dictionary updates, storage engine operations, and binary log writes associated with a DDL operation into a single, atomic transaction.

The MySQL server now automatically performs all necessary upgrade tasks at the next startup to upgrade the system tables in the mysql schema, as well as objects in other schemas such as the sys schema and user schemas. It is no longer required to manually invoke mysql_upgrade as of version 8.0.16.

MySQL Server now supports SSL session reuse by default with a timeout setting that maintains a session cache that establishes the period a client is permitted to request session reuse for new connections.

MySQL now supports the creation and management of resource groups, and permits assigning threads running within the server to particular groups so that threads execute according to the resources available to the group.

MySQL table encryption can now be managed globally by defining and enforcing encryption defaults. The `default_table_encryption` variable defines an encryption default for newly created schemas and general tablespace. These defaults are enforced by enabling the `table_encryption_privilege_check` variable.

The default character set has changed from `latin1` to `utf8mb4`. The `utf8mb4` character set has several new collations available.

MySQL supports the use of expressions as default values for the BLOB, TEXT, GEOMETRY, and JSON data types.

MySQL now has a backup lock that permits DMLs during an online backup while preventing operations that could result in an inconsistent snapshot.

MySQL Server now permits a TCP/IP port to be configured specifically for administrative connections. This administration port is available even when max_connections connections are already established on the primary port.

MySQL Server now supports invisible indexes which are not used by the optimizer, and makes it possible to test the effect of removing an index without actually removing it.

MySQL Server now has a Document Store for developing both SQL and NoSQL document applications using a single database.

MySQL 8.0 makes it possible to persist global, dynamic server variables using the `SET PERSIST` command instead of the usual `SET GLOBAL` one.
