---
title: Install the audit log filter
description: The recommended way to install the component is to use the `audit_log_filter_linux_install.
slug: install-audit-log-filter
category: Install
stability: stable
technical_preview: false
tags:
- audit-log
- installation
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Install the audit log filter

## Installation script

The recommended way to install the component is to use the `audit_log_filter_linux_install.sql` script, located in the `share` directory, which creates the required tables before installing the component.

### Prerequisites

The `plugin_dir` system variable defines the component library location. If needed, set the `plugin_dir` variable at server startup.

### Database selection

The script determines the target database using the following priority:

* If the component is already loaded, the script uses the database name from the `audit_log_filter.database` variable

* If the component is not loaded, but you pass the `-D db_name` option to the mysql client when running the script, it uses the specified `db_name`

* If the component is not loaded and no `-D` option is provided, you must specify the `mysql` database when running the script

You can also designate a different database with the `audit_log_filter.database` system variable. The database name cannot be NULL or exceed 64 characters. If the database name is invalid, the audit log filter tables are not found.

### Install the component

To install the component using the script, you must specify the `mysql` database. You can do this in two ways:

* Option 1: Run the script from the command line with the `-D mysql` option:

    ```{.bash data-prompt="$"}
    mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
    ```

* Option 2: Connect to `mysql` database and run the script interactively:

    ```{.bash data-prompt="mysql>"}
    mysql> use mysql;
    mysql> source /path/to/mysql/share/audit_log_filter_linux_install.sql;
    ```

    Replace `/path/to/mysql/share/` with the actual path to your MySQL installation's share directory.

### Verify installation

After running the script, verify that the required tables are created:

```{.bash data-prompt="mysql>"}
mysql> show tables in mysql like 'aud%';
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------+
    | Tables_in_mysql (aud%) |
    +------------------------+
    | audit_log_filter       |
    | audit_log_user         |
    +------------------------+
    2 rows in set (0.00 sec)
    ```

## Alternative: INSTALL COMPONENT method

You can also install the component using the `INSTALL COMPONENT` command, but this method does not create the required tables and will cause filter operations to fail.

```mysql
INSTALL COMPONENT 'file://audit_log_filter'
```

### Verify component installation

Check that the component is properly installed:

```{.bash data-prompt="mysql>"}
mysql> select * from mysql.component;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------+--------------------+------------------------------------+
    | component_id | component_group_id | component_urn                      |
    +--------------+--------------------+------------------------------------+
    |            1 |                  1 | file://component_percona_telemetry |
    |            2 |                  2 | file://component_audit_log_filter  |
    +--------------+--------------------+------------------------------------+
    2 rows in set (0.00 sec)
    ```

### Test filter functionality

Test that the audit log filter is working correctly:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------------------------------------------------+
    | audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}') |
    +---------------------------------------------------------------------+
    | ERROR: Failed to check filtering rule name existence                |
    +---------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

!!! note

    This error occurs when the component is installed without the required tables. Using the SQL script prevents this issue.

### Fix missing tables

If you have already installed the audit log component but are missing the required tables, you can run the `audit_log_filter_linux_install.sql` script to create the audit tables in the `mysql` database:

```{.bash data-prompt="$"}
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Or interactively:

```{.bash data-prompt="mysql>"}
mysql> use mysql;
mysql> source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

This operation creates the missing tables without reinstalling the component.

## Additional information

To upgrade from `audit_log_filter` plugin in Percona Server 8.4 to `component_audit_log_filter` component in Percona Server {{vers}}, do the [manual upgrade](upgrade-components.md).

--8<--- "get-help-snip.md"