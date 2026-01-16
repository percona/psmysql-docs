# Migrating from 8.0 Plugin to 8.4 Component

This guide helps you migrate from the Percona Server 8.0 audit log filter plugin to the 8.4 audit log filter component.

## Overview of changes

### Architecture change

8.0: Audit log filter was implemented as a plugin

* Installed via `INSTALL PLUGIN`

* Plugin-specific variables and functions

* Coexisted with older `audit_log` plugin

8.4: Audit log filter is implemented as a component

* Installed via `INSTALL COMPONENT`

* Component-based variables (`audit_log_filter.*`)

* Plugin was replaced by the component in 8.4

### Key differences

| Aspect | 8.0 Plugin | 8.4 Component |
|--------|-----------|---------------|
| Installation | `INSTALL PLUGIN` | `INSTALL COMPONENT` or installation script |
| Variables | `audit_log_filter_*` (underscore) | `audit_log_filter.*` (dot notation) |
| Format | OLD, NEW, JSON, CSV | OLD, NEW, JSON (CSV removed) |
| Wildcards | Limited support | Full support in 8.4.4+ |
| Functions | Plugin functions | Component functions (similar names) |

### Removed features

* CSV format: No longer available in 8.4

* Plugin installation method: `INSTALL PLUGIN` no longer works

### Note about the deprecated audit_log plugin

In Percona Server for MySQL 8.4.7-7 and later, the older `audit_log` plugin (not to be confused with `audit_log_filter`) has been reintroduced but is marked as deprecated and will be removed in a future release. The `audit_log_filter` component is the recommended replacement for both:

* The `audit_log_filter` plugin (replaced in 8.4)
* The deprecated `audit_log` plugin (deprecated in 8.4.7-7)

If you are currently using the deprecated `audit_log` plugin, you should migrate to the `audit_log_filter` component. The component provides equivalent functionality with enhanced flexibility, performance, and filtering capabilities.

**Important:** Do not install both the `audit_log` plugin and the `audit_log_filter` component simultaneously. They use different configuration variables and options, and running both can cause conflicts.

## Pre-migration checklist

Before starting migration, complete these steps:


- [ ] Backup current configuration
  * Document all `audit_log_*` variables

  * Export filter definitions from `mysql.audit_log_filter` table

  * Export user assignments from `mysql.audit_log_user` table

  * Backup configuration files (my.cnf)

- [ ] Review current setup

  * List all active filters

  * Document user filter assignments

  * Note any custom configurations

  * Identify CSV format usage (if any)

- [ ] Plan migration

  * Schedule maintenance window

  * Plan for server restart (required)

  * Prepare rollback procedure

  * Test in non-production environment first

- [ ] Verify prerequisites

  * Percona Server 8.4 is installed

  * Installation script is available

  * Required privileges are available

  * Sufficient disk space for logs

## Step-by-step migration procedure

### Step 1: Backup current configuration

Export filter definitions:

```sql
-- Connect to 8.0 server
SELECT * FROM mysql.audit_log_filter INTO OUTFILE '/tmp/audit_filters_backup.txt';
SELECT * FROM mysql.audit_log_user INTO OUTFILE '/tmp/audit_users_backup.txt';
```

Document variables:

```sql
SHOW VARIABLES LIKE 'audit_log%';
-- Save output to file
```

Backup configuration files:

```bash
cp /etc/mysql/my.cnf /etc/mysql/my.cnf.backup
```

### Step 2: Install 8.4 component

Using installation script (recommended):

```bash
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Verify installation:

```sql
-- Check component is installed
SELECT * FROM mysql.component WHERE component_urn LIKE '%audit_log_filter%';

-- Verify tables exist
SHOW TABLES IN mysql LIKE 'audit%';
```

### Step 3: Convert variable names

Update all variable names from plugin format to component format.

Variable name mapping:

| 8.0 Plugin Variable | 8.4 Component Variable | Notes |
|---------------------|------------------------|-------|
| `audit_log_filter_database` | `audit_log_filter.database` | Database for tables |
| `audit_log_filter_file` | `audit_log_filter.file` | Log file name |
| `audit_log_filter_format` | `audit_log_filter.format` | Log format (CSV removed) |
| `audit_log_filter_rotate_on_size` | `audit_log_filter.rotate_on_size` | Rotation size |
| `audit_log_filter_buffer_size` | `audit_log_filter.buffer_size` | Buffer size |

Update configuration file:
```ini
# Old 8.0 format
audit_log_filter_database=mysql
audit_log_filter_file=audit_filter.log
audit_log_filter_format=NEW

# New 8.4 format
audit_log_filter.database=mysql
audit_log_filter.file=audit_filter.log
audit_log_filter.format=NEW
```

### Step 4: Convert include/exclude variables to JSON filters

If you used `audit_log_include_*` or `audit_log_exclude_*` variables, convert them to JSON filters.

Example conversion:

8.0 Configuration:
```ini
audit_log_include_accounts = admin@localhost, dba@%
audit_log_exclude_databases = test, temp
audit_log_include_commands = SELECT, INSERT, UPDATE, DELETE
```

8.4 JSON Filter:
```json
{
  "filter": {
    "class": [
      {
        "name": "general",
        "user": ["admin", "dba"],
        "database": ["test", "temp"],
        "negate": true,
        "event": [{"name": "command"}]
      }
    ]
  }
}
```

Create filter:
```sql
SELECT audit_log_filter_set_filter('migrated_filter', '{
  "filter": {
    "class": [
      {
        "name": "general",
        "user": ["admin", "dba"],
        "database": ["test", "temp"],
        "negate": true,
        "event": [{"name": "command"}]
      }
    ]
  }
}');
```

See [Filter Migration Guide](filter-audit-log-filter-files.md#translating-80-includeexclude-variables-to-json-filters) for detailed conversion examples.

### Step 5: Migrate existing filters

If you have existing filters in `mysql.audit_log_filter` table:

Option 1: Filters are compatible (recommended)

* If filters are already in JSON format, they should work as-is

* Verify filters after migration

* Test functionality

Option 2: Recreate filters

* Export filter definitions

* Recreate using `audit_log_filter_set_filter()`

* Verify each filter works correctly

Migrate user assignments:
```sql
-- Reassign filters to users
-- Use data from backup or mysql.audit_log_user table

SELECT audit_log_filter_set_user('admin@localhost', 'filter_name');
SELECT audit_log_filter_set_user('user@%', 'filter_name');
```

### Step 6: Handle CSV format (if used)

If you were using CSV format in 8.0:

Options:


1. Switch to JSON format (recommended for programmatic access)

2. Switch to NEW XML format (human-readable)

3. Switch to OLD XML format (compatibility)

Migration:
```sql
-- Change format to JSON
SET GLOBAL audit_log_filter.format = 'JSON';
SET GLOBAL audit_log_filter.file = 'audit_filter.json';
-- Restart server
```

Note: Old CSV format files cannot be converted. Only new logs use the new format.

### Step 7: Update wildcard usage (8.4.4+)

If you're on 8.4.4 or later, you can use wildcards in `audit_log_filter_set_user()`:

```sql
-- Old method (specific hosts)
SELECT audit_log_filter_set_user('user@192.168.1.1', 'filter');
SELECT audit_log_filter_set_user('user@192.168.1.2', 'filter');

-- New method (wildcard - 8.4.4+)
SELECT audit_log_filter_set_user('user@192.168.1.%', 'filter');
```

### Step 8: Test functionality

Verify filters work:
```sql
-- Check filters
SELECT * FROM mysql.audit_log_filter;

-- Check user assignments
SELECT * FROM mysql.audit_log_user;

-- Test filter
SELECT audit_log_filter_set_filter('test_filter', '{"filter": {"log": true}}');
SELECT audit_log_filter_set_user('%', 'test_filter');

-- Execute test query
SELECT 1;

-- Verify logging (if JSON format)
SELECT audit_log_read();
```

Verify log rotation:
```sql
-- Check rotation settings
SHOW VARIABLES LIKE 'audit_log_filter.rotate_on_size';

-- Test manual rotation
SELECT audit_log_rotate();
```

### Step 9: Remove old plugin (optional)

If the old plugin is still installed:

```sql
-- Check if plugin exists
SELECT * FROM INFORMATION_SCHEMA.PLUGINS 
WHERE PLUGIN_NAME LIKE 'audit_log_filter';

-- Uninstall plugin (if present)
UNINSTALL PLUGIN audit_log_filter;
```

Note: The plugin may have been automatically removed during 8.4 upgrade.

### Step 10: Restart server

Required for:

* Variable changes (format, file, database, etc.)

* Component activation

* Configuration changes

```bash
# Restart MySQL server
systemctl restart mysql
# Or
service mysql restart
```

Verify after restart:
```sql
-- Check component is loaded
SELECT * FROM mysql.component WHERE component_urn LIKE '%audit_log_filter%';

-- Check variables
SHOW VARIABLES LIKE 'audit_log_filter.%';

-- Test functionality
SELECT audit_log_filter_set_filter('test', '{"filter": {"log": true}}');
```

## Configuration mapping reference

### Variable name changes

| 8.0 Plugin | 8.4 Component | Change Required |
|-----------|---------------|-----------------|
| `audit_log_filter_database` | `audit_log_filter.database` | Yes - change underscore to dot |
| `audit_log_filter_file` | `audit_log_filter.file` | Yes - change underscore to dot |
| `audit_log_filter_format` | `audit_log_filter.format` | Yes - change underscore to dot |
| `audit_log_filter_rotate_on_size` | `audit_log_filter.rotate_on_size` | Yes - change underscore to dot |
| `audit_log_filter_buffer_size` | `audit_log_filter.buffer_size` | Yes - change underscore to dot |

### Removed variables

These plugin variables are no longer available in 8.4:

* `audit_log_include_accounts` → Use JSON filters with `user` field

* `audit_log_exclude_accounts` → Use JSON filters with `user` field and `negate: true`

* `audit_log_include_commands` → Use JSON filters with `event: {"name": "command"}`

* `audit_log_exclude_commands` → Use JSON filters with `event` and `negate: true`

* `audit_log_include_databases` → Use JSON filters with `database` field

* `audit_log_exclude_databases` → Use JSON filters with `database` field and `negate: true`

### Function name changes

Function names remain the same, but behavior may differ:

* `audit_log_filter_set_filter()` - Same name, same behavior

* `audit_log_filter_set_user()` - Same name, enhanced wildcard support in 8.4.4+

* `audit_log_filter_flush()` - Same name, same behavior

* `audit_log_filter_remove_filter()` - Same name, same behavior

* `audit_log_filter_remove_user()` - Same name, same behavior

## Common migration issues

### Issue: Filters not working after migration

Symptoms:

* Filters are created but events are not logged

* Functions return errors

Causes:

* Component not properly installed

* Tables not created

* Missing privileges

Solutions:
1. Verify component installation:
   ```sql
   SELECT * FROM mysql.component WHERE component_urn LIKE '%audit_log_filter%';
   ```

2. Verify tables exist:
   ```sql
   SHOW TABLES IN mysql LIKE 'audit%';
   ```

3. Re-run installation script if needed:
   ```bash
   mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
   ```

4. Check privileges:
   ```sql
   GRANT AUDIT_ADMIN ON *.* TO 'user'@'host';
   ```

### Issue: Variables not recognized

Symptoms:

* Server doesn't recognize variable names

* Configuration errors

Causes:

* Using old plugin variable names (underscore format)

* Variable not updated in configuration file

Solutions:
1. Update variable names to component format (dot notation)
2. Update my.cnf or other configuration files
3. Restart server after changes

### Issue: CSV format not available

Symptoms:

* Error when setting format to CSV

* CSV format option missing

Causes:

* CSV format was removed in 8.4

Solutions:
1. Choose alternative format:

   * JSON (recommended for programmatic access)

   * NEW XML (human-readable)

   * OLD XML (compatibility)

2. Update configuration:
   ```sql
   SET GLOBAL audit_log_filter.format = 'JSON';
   SET GLOBAL audit_log_filter.file = 'audit_filter.json';
   ```

3. Restart server

### Issue: Permission errors

Symptoms:

* `ERROR 1227 (42000): Access denied`

* Cannot create or modify filters

Causes:

* Missing `AUDIT_ADMIN` privilege

* User doesn't have required permissions

Solutions:
```sql
-- Grant required privilege
GRANT AUDIT_ADMIN ON *.* TO 'user'@'host';
FLUSH PRIVILEGES;
```

### Issue: Filters not replicating correctly

Symptoms:

* Filters work on source but not replica

* Replicated filters not active

Causes:

* Tables replicate but filters don't activate automatically

* Missing `audit_log_filter_flush()` on replica

Solutions:
1. On replica, call flush after replication:
   ```sql
   SELECT audit_log_filter_flush();
   ```

2. Or configure replication to ignore audit tables:
   ```ini
   replicate-ignore-table=mysql.audit_log_filter
   replicate-ignore-table=mysql.audit_log_user
   ```

## Rollback procedure

The audit log filter plugin is not available in 8.4, so rollback to the plugin is not possible. If migration fails or causes issues, use one of these approaches:

### Option 1: Fix component configuration (recommended)

Instead of rolling back, fix the component configuration:

1. Review error messages and logs to identify the issue

2. Correct the configuration:

   * Fix variable names (ensure dot notation is used)

   * Recreate filters if needed

   * Verify user assignments

3. Restart the server if configuration changes require it

4. Verify functionality:

   * Test filters work

   * Verify logging occurs

   * Check variables are recognized

### Option 2: Downgrade to 8.0 (if necessary)

If you must use the plugin version, downgrade to Percona Server 8.0:

**Prerequisites:**

* Backup of current 8.4 configuration

* Access to 8.0 installation

* Plan for downtime during downgrade

**Downgrade steps:**

1. Uninstall the component:

   ```sql
   UNINSTALL COMPONENT 'file://audit_log_filter';
   ```

2. Restore old configuration:

   * Restore my.cnf from backup

   * Restore filter definitions if needed

3. Downgrade to Percona Server 8.0 following standard downgrade procedures

4. Reinstall the audit log filter plugin:

   ```sql
   INSTALL PLUGIN audit_log_filter SONAME 'audit_log_filter.so';
   ```

5. Verify functionality:

   * Test filters work

   * Verify logging occurs

   * Check variables are recognized

**Note:** Downgrading is complex and may cause data compatibility issues. Fixing the component configuration is strongly recommended instead.

## Post-migration verification

After migration, verify everything works correctly:


- [ ] Component is installed and loaded

- [ ] Tables exist and are accessible

- [ ] Variables are recognized (dot notation)

- [ ] Filters can be created

- [ ] Filters can be assigned to users

- [ ] Events are being logged

- [ ] Log rotation works

- [ ] Log reading works (if JSON format)

- [ ] Performance is acceptable

- [ ] No errors in error log

## Additional resources

* [Audit Log Filter Overview](audit-log-filter-overview.md)

* [Writing Filter Definitions](write-filter-definitions.md)

* [Filter Functions](filter-audit-log-filter-files.md)

* [Component Upgrade Guide](upgrade-components.md)

--8<--- "get-help-snip.md"
