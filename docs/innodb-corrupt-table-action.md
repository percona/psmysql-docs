# Handle corrupted tables

When a server subsystem tries to access a corrupted table,
the server may crash.
If this outcome is not desirable when a corrupted table is encountered,
set the new system innodb_corrupt_table_action variable
to a value which allows the ongoing operation to continue
without crashing the server.

The server error log registers attempts to access corrupted table pages.

### Interacting with the innodb_force_recovery variable

The innodb_corrupt_table_action variable
may work in conjunction with the innodb_force_recovery variable
which considerably reduces
the effect of *InnoDB* subsystems
running in the background.

If the innodb_force_recovery option is <4, corrupted pages are lost and the server may continue to run due to the innodb_corrupt_table_action variable having a non-default value.

For more information about the innodb_force_recovery variable,
see [Forcing InnoDB Recovery](https://dev.mysql.com/doc/refman/5.5/en/forcing-innodb-recovery.html)
from the MySQL Reference Manual.

This feature adds a system variable.


## System variables

### `innodb_corrupt_table_action`

| Option       | Description           |
|--------------|-----------------------|
| Command-line | Yes                   |
| Config file  | Yes                   |
| Scope        | Global                |
| Dynamic      | Yes                   |
| Data type    | ULONG                 |
| Default      | assert                |
| Range        | assert, warn, salvage |

* Enabling `innodb_file_per_table` and using the `assert` value creates an assertion failure which causes *XtraDB* to intentionally crash the server. This action is expected when detecting corrupted data in a single-table tablespace.

* Enabling `innodb_file_per_table` and using the `warn` value causes *XtraDB* to pass the table corruption as `corrupt table` instead of crashing the server. Detecting the file as corrupt also disables the file I/O for that data file, except for the deletion operation.

* Enabling `innodb_file_per_table` and using the `salvage` value causes *XtraDB* to allow read access to the corrupted tablespace but ignores any corrupted pages.
