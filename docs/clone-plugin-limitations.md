# Clone plugin limitations

The clone plugin clones instances within the same series only. It clones from version 8.0.37 to 8.0.42, but not from 8.0 to 8.4. Before the 8.0.37 version, it requires matching point release numbers.

Before version 8.0.27, the clone plugin blocks DDL on the donor and recipient during cloning. This block includes `TRUNCATE TABLE`. Use dedicated donor instances to work around this limitation. DML continues during cloning.

From the 8.0.27 version, the clone plugin allows concurrent DDL on the donor by default. The `clone_block_ddl` variable controls this limit.

The clone plugin clones from a donor to a hotfix instance of the same version from 8.0.26 version onward.

The clone plugin clones one MySQL instance at a time. It does not clone multiple instances in one operation.

The clone plugin does not support the X Protocol port (mysqlx_port) for remote cloning.

The clone plugin does not clone MySQL server configurations. The recipient keeps its own settings.

The clone plugin does not clone binary logs.

The clone plugin clones InnoDB data only. It clones other storage engine tables, like MyISAM and CSV, as empty tables.

The clone plugin does not support connections to the donor through MySQL Router.

Local cloning does not clone general tablespaces created with absolute paths. This prevents file path conflicts.
