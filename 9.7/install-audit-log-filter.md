> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install the audit log filter

## Installation script

Run `audit_log_filter_linux_install.sql` from the server `share` directory. The script creates the audit tables and then installs the component.

### Prerequisites

`plugin_dir` locates the component library. Set the variable at startup when the default path is wrong.

### Database selection

By default, the script runs against the `mysql` database. To use a different database, set [`audit_log_filter.database`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html#audit_log_filterdatabase) at server startup before running the install script.

### Install the component

Use either approach:

- Option 1: Run the script from the command line with the `-D mysql` option:

  ```
  mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
  ```

- Option 2: Connect to the `mysql` database and run the script interactively:

  ```
  use mysql;
  source /path/to/mysql/share/audit_log_filter_linux_install.sql;
  ```

  Replace `/path/to/mysql/share/` with the path to the server installation’s `share` directory. For package installations, the script is in `/usr/share/mysql/` on Debian and Ubuntu, and in `/usr/share/percona-server/` on RHEL-based distributions.

### Verify installation

Confirm the audit tables exist:

```
show tables in mysql like 'aud%';
```

Expected output

```
+------------------------+
| Tables_in_mysql (aud%) |
+------------------------+
| audit_log_filter       |
| audit_log_user         |
+------------------------+
2 rows in set (0.00 sec)
```

## Alternative: INSTALL COMPONENT method

`INSTALL COMPONENT` loads the binary only. The statement does not create tables, so filter UDFs fail until you run the install script.

```
INSTALL COMPONENT 'file://component_audit_log_filter';
```

The URN must include the `component_` prefix. `file://audit_log_filter` fails to load the component.

### Verify component installation

Confirm the component row exists:

```
select * from mysql.component;
```

Expected output

```
+--------------+--------------------+------------------------------------+
| component_id | component_group_id | component_urn                      |
+--------------+--------------------+------------------------------------+
|            1 |                  1 | file://component_percona_telemetry |
|            2 |                  2 | file://component_audit_log_filter  |
+--------------+--------------------+------------------------------------+
2 rows in set (0.00 sec)
```

### Test filter functionality

Exercise a filter UDF:

```
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
```

Expected output

```
+---------------------------------------------------------------------+
| audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}') |
+---------------------------------------------------------------------+
| ERROR: Failed to check filtering rule name existence                |
+---------------------------------------------------------------------+
1 row in set (0.00 sec)
```

Note

The error appears when the component loads without the tables. Run `audit_log_filter_linux_install.sql` first.

### Fix missing tables

When the component is installed but tables are missing, run the install script against `mysql`:

```
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Or interactively:

```
use mysql;
source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

The script adds the tables and does not reinstall the component.

## Additional information

When you are replacing an existing audit plugin (the legacy `audit_log` plugin or the transitional `audit_log_filter` plugin) with the component, see [Migrate to the audit log filter component](https://docs.percona.com/percona-server/9.7/migrate-to-audit-log-filter-component.html) for the variable mapping, policy translation, and a worked example. The general plugin-to-component framing appears in [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.html).

## Additional reading

- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.html)
- [Audit Log Filter quickstart](https://docs.percona.com/percona-server/9.7/audit-log-filter-quickstart.html)
- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html)
- [Uninstall Audit Log Filter](https://docs.percona.com/percona-server/9.7/uninstall-audit-log-filter.html)
- [Upgrade components](https://docs.percona.com/percona-server/9.7/upgrade-components.html)
- [Upgrade Percona Server for MySQL](https://docs.percona.com/percona-server/9.7/upgrade.html)

Review [Get help from Percona](https://docs.percona.com/percona-server/9.7/get-help.html) for ways that we can work with you.
