# Install the Audit Log Filter

## Installation script

The recommended way to install the plugin is to use the `audit_log_filter_linux_install.sql` script, located in the share directory, which creates the required tables before installing the plugin.

### Prerequisites

The `plugin_dir` system variable defines the plugin library location. When you need a custom location, set the `plugin_dir` variable at server startup.

### Database selection

The script determines the target database using the following priority:

1. When the plugin is already loaded, the script uses the database name from the `audit_log_filter_database` variable

2. When the plugin is not loaded, but you pass the `-D db_name` option to the mysql client when running the script, the script uses the specified `db_name`

3. When the plugin is not loaded and no `-D` option is provided, you must specify the `mysql` database when running the script

You can also designate a different database with the `audit_log_filter_database` system variable. The database name cannot be NULL or exceed 64 characters. When the database name is invalid, the audit log filter tables are not found.

### Install the component

To install the plugin using the script, you must specify the `mysql` database. You can do this in two ways:

Option 1: Run the script from the command line with the `-D mysql` option:

```bash
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Option 2: Connect to `mysql` database and run the script interactively:

```sql
mysql> use mysql;
mysql> source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

Replace `/path/to/mysql/share/` with the actual path to your MySQL installation's share directory.

### Verify installation

After you run the script, verify that the required tables are created:

```sql
mysql> show tables in mysql like 'aud%';
```

Expected output:

```
+------------------------+
| Tables_in_mysql (aud%) |
+------------------------+
| audit_log_filter       |
| audit_log_user         |
+------------------------+
2 rows in set (0.00 sec)
```

## Alternative: INSTALL PLUGIN method

You can also install the plugin using the `INSTALL PLUGIN` command, but this method does not create the required tables and will cause filter operations to fail.

### Verify plugin installation

Check that the plugin is properly installed:

```sql
mysql> SHOW PLUGINS LIKE 'audit_log_filter';
```

Expected output:

```
+-------------------+----------+--------------------+
| Name              | Status   | Type               |
+-------------------+----------+--------------------+
| audit_log_filter  | ACTIVE   | AUDIT              |
+-------------------+----------+--------------------+
1 row in set (0.00 sec)
```

### Test filter functionality

Test that the audit log filter is working correctly:

```sql
mysql> SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
```

Expected output:

```
+---------------------------------------------------------------------+
| audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}') |
+---------------------------------------------------------------------+
| ERROR: Failed to check filtering rule name existence                |
+---------------------------------------------------------------------+
1 row in set (0.00 sec)
```

!!! note

    This error occurs when the plugin is installed without the required tables. Using the SQL script prevents this issue.

### Fix missing tables

When you have already installed the audit log plugin but are missing the required tables, you can run the `audit_log_filter_linux_install.sql` script to create the audit tables in the `mysql` database:

```bash
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Or interactively:

```sql
mysql> use mysql;
mysql> source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

This operation creates the missing tables without reinstalling the plugin.

## Additional information

For information about upgrading the audit log filter plugin, see the upgrade documentation.

## References

[Audit Log Filter Overview](audit-log-filter-overview.md)

[Audit Log Filter Variables & Functions](audit-log-filter-variables.md)
