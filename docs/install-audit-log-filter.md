# Install the audit log filter

## Installation script

The recommended way to install the component is to use the `audit_log_filter_linux_install.sql` script, located in the `share` directory, which creates the required tables before installing the component.

### What the script does

When you run the `audit_log_filter_linux_install.sql` script, it performs the following operations:

1. Creates the `mysql.audit_log_filter` table: This table stores filter definitions. Each filter has a name and a JSON definition that specifies which events to log or block.

2. Creates the `mysql.audit_log_user` table: This table stores user account assignments. It links user accounts (user@host combinations) to specific filter names.

3. Installs the component: The script executes `INSTALL COMPONENT 'file://audit_log_filter'` to load the audit log filter component into the MySQL server.

4. Verifies the installation: The script ensures that both tables are created successfully and the component is properly installed.

The script can be run safely multiple times: if the component is already installed, it will not reinstall it. If the tables already exist, it will not recreate them.

For detailed information about the table structures and column definitions, see [Audit Log Filter tables](audit-log-filter-overview.md#audit-log-filter-tables) in the overview.

### Prerequisites

The `plugin_dir` system variable defines the component library location. If needed, set the `plugin_dir` variable at server startup.

### Database selection

The script determines the target database using the following priority:

* If the component is already loaded, the script uses the database name from the `audit_log_filter.database` variable

* If the component is not loaded, but you pass the `-D db_name` option to the mysql client when running the script, it uses the specified `db_name`

* If the component is not loaded and no `-D` option is provided, you must specify the `mysql` database when running the script

You can also designate a different database with the `audit_log_filter.database` system variable. The database name cannot be NULL or exceed 64 characters. If the database name is invalid, the audit log filter tables are not found.

### Install the component

To install the component using the script, you must specify the `mysql` database. You can specify the `mysql` database in two ways:

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

For detailed information about these tables, including column definitions and how to modify them, see [Audit Log Filter tables](audit-log-filter-overview.md#audit-log-filter-tables) in the overview.

## Alternative: INSTALL COMPONENT method

You can also install the component using the `INSTALL COMPONENT` command, but the `INSTALL COMPONENT` method does not create the required tables and will cause filter operations to fail.

```sql
INSTALL COMPONENT 'file://audit_log_filter'
```

### Verify component installation

Check that the component is properly installed:

```sql
select * from mysql.component;
```

??? example "Expected output"

    ```text
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

```sql
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
```

??? example "Expected output"

    ```text
    +---------------------------------------------------------------------+
    | audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}') |
    +---------------------------------------------------------------------+
    | ERROR: Failed to check filtering rule name existence                |
    +---------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

!!! note

    This error occurs when the component is installed without the required tables. Using the SQL script prevents this error.

### Fix missing tables

If you have already installed the audit log component but are missing the required tables, you can run the `audit_log_filter_linux_install.sql` script to create the audit tables in the `mysql` database:

```shell
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Or interactively:

```sql
USE mysql;
source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

Running the script creates the missing tables without reinstalling the component.

## Choosing a database for audit tables

By default, audit log filter tables are created in the `mysql` system database. You can use a different database if needed.

### When to use a non-default database

Consider using a custom database when:

* You want to separate audit tables from system tables

* You have specific backup/restore requirements

* You need different replication configuration

* Compliance requirements specify separate database

### Setting a custom database

Before installation:

```sql
-- Set custom database at server startup
-- Add to my.cnf:
[mysqld]
audit_log_filter.database=audit_db
```

After installation:
Changing the database requires:

1. Creating new database

2. Migrating tables

3. Updating configuration

4. Restarting server

### Database limitations

Constraints:

* Database name cannot be NULL

* Database name cannot exceed 64 characters

* Database must exist before component installation

* Invalid database name prevents component from working

### Migration between databases

Procedure:

1. Create new database

2. Export tables from old database

3. Import tables to new database

4. Update `audit_log_filter.database` variable

5. Restart server

6. Verify component works with new database

## Post-installation configuration

After installing the audit log filter component, configure it for your environment.

### Step 1: Create your first filter

Simple filter to log all events:

```sql
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
```

Filter to log only connections:

```sql
SELECT audit_log_filter_set_filter('log_connections', '{
  "filter": {
    "class": {
      "name": "connection"
    }
  }
}');
```

### Step 2: Assign filter to users

Assign to default account (all users):

```sql
SELECT audit_log_filter_set_user('%', 'log_all');
```

Assign to specific user:

```sql
SELECT audit_log_filter_set_user('admin@localhost', 'log_all');
```

Assign with wildcard (8.4.4+):

```sql
SELECT audit_log_filter_set_user('user@192.168.%', 'log_all');
```

### Step 3: Test filter functionality

Verify filter is working:

```sql
-- Check filters
SELECT * FROM mysql.audit_log_filter;

-- Check user assignments
SELECT * FROM mysql.audit_log_user;

-- Test by executing a query
SELECT 1;

-- Check audit log file (if format is JSON)
SELECT audit_log_read();
```

### Step 4: Configure log management

Set rotation size:

```sql
SET GLOBAL audit_log_filter.rotate_on_size = 1073741824; -- 1GB
```

Set pruning:

```sql
-- Size-based pruning (10GB total)
SET GLOBAL audit_log_filter.max_size = 10737418240;

-- Time-based pruning (30 days)
SET GLOBAL audit_log_filter.prune_seconds = 2592000;
```

### Step 5: Optional security configuration

Enable encryption:

```sql
-- Install keyring component first
INSTALL COMPONENT 'file://component_keyring_file';

-- Set encryption password
SELECT audit_log_encryption_password_set('secure_password');

-- Enable encryption (requires restart)
SET GLOBAL audit_log_filter.encryption = 'AES';
```

Enable compression:

```sql
SET GLOBAL audit_log_filter.compression = 'GZIP';
-- Requires restart
```

## Upgrading from 8.0 plugin

If you're upgrading from Percona Server 8.0 with the audit log filter plugin, follow these steps.

### Prerequisites

1. Backup current configuration:

   * Document all `audit_log_*` variables

   * Export filter definitions if using plugin filters

   * Backup `mysql.audit_log_filter` and `mysql.audit_log_user` tables

2. Review plugin configuration:

   ```sql
   -- Check if plugin is installed
   SELECT * FROM INFORMATION_SCHEMA.PLUGINS 
   WHERE PLUGIN_NAME LIKE 'audit%';
   
   -- Document current variables
   SHOW VARIABLES LIKE 'audit_log%';
   ```

### Upgrade procedure

1. Install component:

   ```bash
   mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
   ```

2. Verify installation:

   ```sql
   SELECT * FROM mysql.component WHERE component_urn LIKE '%audit_log_filter%';
   SHOW TABLES IN mysql LIKE 'audit%';
   ```

3. Migrate filter definitions:

   * Convert old include/exclude variables to JSON filters

   * See [Migration Guide](audit-log-filter-migration.md) for details

   * Create new filters using `audit_log_filter_set_filter()`

4. Update variable names:

   * Change `audit_log_filter_*` to `audit_log_filter.*`

   * Update configuration files (my.cnf)

   * Remove deprecated plugin variables

5. Test functionality:

   * Verify filters work correctly

   * Check that events are being logged

   * Verify log rotation and pruning

6. Remove old plugin (optional):

   ```sql
   UNINSTALL PLUGIN audit_log_filter;
   ```

### Common upgrade issues

Issue: Filters not working

* Cause: Tables not created or component not loaded

* Solution: Run installation script, verify component is installed

Issue: Variables not recognized

* Cause: Using old plugin variable names

* Solution: Update to component variable names (`audit_log_filter.*`)

Issue: Permission errors

* Cause: Missing `AUDIT_ADMIN` privilege

* Solution: Grant `AUDIT_ADMIN` privilege to users

For complete migration instructions, see [Migration Guide](audit-log-filter-migration.md).

## Additional information

To upgrade from `audit_log_filter` plugin in Percona Server 8.0 to `component_audit_log_filter` component in Percona Server 8.4, do the [manual upgrade](upgrade-components.md).

--8<--- "get-help-snip.md"
