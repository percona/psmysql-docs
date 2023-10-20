# Updated supported features

The following is a list of the latest supported features:

* Percona Server for MySQLsupports `SELECT FOR UPDATE SKIP LOCKED/NOWAIT`. The transaction isolation level must be `READ COMMITTED`.

* Percona Server for MySQL adds the ability to cancel ongoing manual compactions. The cancel methods are the following:

    * Using either Control+C (from a session) or KILL (from another session) for client sessions running manual compactions by `SET GLOBAL rocksdb_compact_cf (variable)`.

    * Using a global variable `rocksdb_cancel_manual_compactions` to cancel all ongoing manual compactions.

* Percona Server for MySQL adds supported for [Generated Columns](https://dev.mysql.com/doc/refman/8.0/en/create-table-generated-columns.html) and index are supported.

* Percona Server for MySQL adds support for [explicit DEFAULT value expressions](https://dev.mysql.com/doc/refman/8.0/en/data-type-defaults.html). 
