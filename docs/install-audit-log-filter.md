# Install the audit log filter

## Installation script

Run `audit_log_filter_linux_install.sql` from the server `share` directory. The script creates the audit tables and then installs the component.

### Prerequisites

`plugin_dir` locates the component library. Set the variable at startup when the default path is wrong.

### Database selection

By default, the script runs against the `mysql` database. To use a different database, set [`audit_log_filter.database`](audit-log-filter-variables.md#audit_log_filterdatabase) at server startup before running the install script.

### Install the component

Use either approach:

* Option 1: Run the script from the command line with the `-D mysql` option:

    ```shell
    mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
    ```

* Option 2: Connect to the `mysql` database and run the script interactively:

    ```sql
    use mysql;
    source /path/to/mysql/share/audit_log_filter_linux_install.sql;
    ```

    Replace `/path/to/mysql/share/` with the path to the server installation's `share` directory.

### Verify installation

Confirm the audit tables exist:

```sql
show tables in mysql like 'aud%';
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

`INSTALL COMPONENT` loads the binary only. The statement does not create tables, so filter UDFs fail until you run the install script.

```mysql
INSTALL COMPONENT 'file://component_audit_log_filter';
```

The URN must include the `component_` prefix. `file://audit_log_filter` fails to load the component.

### Verify component installation

Confirm the component row exists:

```sql
select * from mysql.component;
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

Exercise a filter UDF:

```sql
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
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

    The error appears when the component loads without the tables. Run `audit_log_filter_linux_install.sql` first.

### Fix missing tables

When the component is installed but tables are missing, run the install script against `mysql`:

```shell
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Or interactively:

```sql
use mysql;
source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

The script adds the tables and does not reinstall the component.

## Additional information

When you are replacing an existing audit plugin (the legacy `audit_log` plugin or the transitional `audit_log_filter` plugin) with the component, see [Migrate to the audit log filter component](migrate-to-audit-log-filter-component.md) for the variable mapping, policy translation, and a worked example. The general plugin-to-component framing appears in [Upgrade from plugins to components](upgrade-components.md).

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Audit Log Filter quickstart](audit-log-filter-quickstart.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)

* [Uninstall Audit Log Filter](uninstall-audit-log-filter.md)

* [Upgrade components](upgrade-components.md)

* [Upgrade Percona Server for MySQL](upgrade.md)

--8<--- "get-help-snip.md"
