# Install the audit log filter

## Installation script

Run `audit_log_filter_linux_install.sql` from the server `share` directory. The script creates the audit tables, then installs the component.

### Prerequisites

`plugin_dir` locates the component library; set it at startup if the default path is wrong.

### Database selection

The script picks the target database in this order:

* If the component is already loaded, the script uses the database name from the `audit_log_filter.database` variable

* If the component is not loaded, but you pass the `-D db_name` option to the mysql client when running the script, the script uses the specified `db_name`

* If the component is not loaded and no `-D` option is provided, you must specify the `mysql` database when running the script

You can also point the component at another database with `audit_log_filter.database`. The name must be non-`NULL`, at most 64 characters, and valid—otherwise the server cannot open the audit log filter tables.

### Install the component

By default, the script runs against the `mysql` database. Use either approach:

* Option 1: Run the script from the command line with the `-D mysql` option:

    ```shell
    mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
    ```

* Option 2: Connect to `mysql` database and run the script interactively:

    ```sql
    use mysql;
    source /path/to/mysql/share/audit_log_filter_linux_install.sql;
    ```

    Replace `/path/to/mysql/share/` with the actual path to your server installation’s `share` directory.

### Verify the audit tables exist

Confirm the audit tables exist:

```sql
show tables in mysql like 'aud%';
```

A clean install lists two rows for `audit_log_filter` and `audit_log_user`. Other tables matching `aud%` in the `mysql` schema can also appear in the output; the install is successful as long as both `audit_log_filter` and `audit_log_user` are present.

??? example "Expected output on a clean install"

    ```{.text .no-copy}
    +------------------------+
    | Tables_in_mysql (aud%) |
    +------------------------+
    | audit_log_filter       |
    | audit_log_user         |
    +------------------------+
    ```

## Alternative: INSTALL COMPONENT method

`INSTALL COMPONENT` loads the binary only—it does not create tables, so filter UDFs fail until you run the install script.

```mysql
INSTALL COMPONENT 'file://component_audit_log_filter';
```

The URN must include the `component_` prefix. `file://audit_log_filter` fails to load the component.

### Verify the component is registered

Confirm the component row exists:

```sql
select * from mysql.component;
```

Look for a row whose `component_urn` is `file://component_audit_log_filter`. Other components (for example `component_percona_telemetry`) can appear in the same result; the row count and column values depend on which other components the instance has loaded.

??? example "Example output"

    ```{.text .no-copy}
    +--------------+--------------------+------------------------------------+
    | component_id | component_group_id | component_urn                      |
    +--------------+--------------------+------------------------------------+
    |            1 |                  1 | file://component_percona_telemetry |
    |            2 |                  2 | file://component_audit_log_filter  |
    +--------------+--------------------+------------------------------------+
    ```

### Detect missing tables

Exercise a filter UDF to confirm the audit tables exist. The call fails when the component loads without them:

```sql
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
```

??? example "Expected output when tables are missing"

    ```{.text .no-copy}
    +---------------------------------------------------------------------+
    | audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}') |
    +---------------------------------------------------------------------+
    | ERROR: Failed to check filtering rule name existence                |
    +---------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

!!! note

    This error indicates that the component is loaded without the tables. Run `audit_log_filter_linux_install.sql` first.

### Fix missing tables

If the component is installed but tables are missing, run the install script against `mysql`:

```shell
mysql -u root -p -D mysql < /path/to/mysql/share/audit_log_filter_linux_install.sql
```

Or interactively:

```sql
use mysql;
source /path/to/mysql/share/audit_log_filter_linux_install.sql;
```

The script adds the tables and does not reinstall the component.

## Post-install verification

The following check applies to both install paths. Run it after the install script completes or after recovering from a missing-tables state.

Define a catch-all filter and bind it to the default account pattern. Both calls are required. `audit_log_filter_set_filter()` stores the filter definition in `mysql.audit_log_filter`. `audit_log_filter_set_user()` assigns it to a login pattern in `mysql.audit_log_user`. A filter that is defined but unassigned never reaches a session.

```sql
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
SELECT audit_log_filter_set_user('%', 'log_all');
SELECT audit_log_filter_flush();
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------------------------------------------------+
    | audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}') |
    +---------------------------------------------------------------------+
    | OK                                                                  |
    +---------------------------------------------------------------------+
    +-------------------------------------+
    | audit_log_filter_set_user('%', 'log_all') |
    +-------------------------------------+
    | OK                                  |
    +-------------------------------------+
    +--------------------------+
    | audit_log_filter_flush() |
    +--------------------------+
    | OK                       |
    +--------------------------+
    ```

The `%` account pattern is the default-row fallback the component uses when no more specific row in `mysql.audit_log_user` matches the session account. For per-account assignment, replace `%` with a `user_name@host_name` pattern. For details, see [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name) and [Which audit_log_user row applies](filter-audit-log-filter-files.md#which-audit_log_user-row-applies).

## Additional information

If you are replacing an existing audit plugin (the legacy `audit_log` plugin or the transitional `audit_log_filter` plugin) with the component, see [Migrate to the audit log filter component](migrate-to-audit-log-filter-component.md) for the variable mapping, policy translation, and a worked example. The general plugin-to-component framing is in [Upgrade from plugins to components](upgrade-components.md).

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter quickstart](audit-log-filter-quickstart.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
* [Uninstall Audit Log Filter](uninstall-audit-log-filter.md)
* [Upgrade components](upgrade-components.md)
* [Upgrade Percona Server for MySQL](upgrade.md)

--8<--- "get-help-snip.md"
