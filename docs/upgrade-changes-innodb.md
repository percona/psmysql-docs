# InnoDB changes

The maximum auto-increment counter value is now persistent across server restarts.

When encountering index tree corruption, InnoDB writes a corruption flag to the redo log, which makes the corruption flag crash-safe.

A new dynamic variable, `innodb_deadlock_detect`, may be used to disable deadlock detection.

InnoDB temporary tables are now created in the shared temporary tablespace, `ibtmp1`.

System tables and data dictionary tables are now created in a single InnoDB tablespace file named `mysql.ibd` in the MySQL data directory.

By default, undo logs now reside in two undo tablespaces, not in the system tablespace, and are created when the MySQL instance is initialized.

The new `innodb_dedicated_server` variable, disabled by default, can be used to have InnoDB automatically configure several options based on detected server memory.

Tablespace files can be moved or restored to a new location while the server is offline using the `innodb_directories` option.
