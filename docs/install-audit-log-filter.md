# Install the Audit Log Filter

The feature is in [tech preview](glossary.md#tech-preview).

The `plugin_dir` system variable defines the plugin library location. If needed, at server startup, set the `plugin_dir` variable.

When upgrading a MySQL installation, plugins are not automatically upgraded. You may need to manually load the plugin after the MySQL upgrade.

In the `share` directory, locate the `audit_log_filter_linux_install.sql `script.

Implemented in 8.0.34, at the time you run the script, you can select the database used to store the JSON filter tables. 

* If the plugin is loaded, the installation script takes the database name from the `audit_log_filter_database` variable
* If the plugin is not loaded, but passes the `-D db_name` to the mysql client when the installation script runs, uses the `db_name`.
* If the plugin is not loaded and the `-D` option is not provided, the installation script creates the required tables in the default database name `mysql`.

You can also designate a different database with the `audit_log_filter_database` system variable. The database name cannot be NULL or exceed 64 characters. If the database name is invalid, the audit log filter tables are not found.

With 8.0.34 and higher, use this command:


```{.bash data-prompt="$"}
$ mysql -u -D database -p < audit_log_filter_linux_install.sql
```

To verify the plugin installation, run the following command:

```{.bash data-prompt="mysql>"}
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE `audit%';
```

??? example "Expected output"

    ```text
    +--------------------+---------------+
    | PLUGIN_NAME        | PLUGIN_STATUS |
    +--------------------+---------------+
    | audit_log_filter   | ACTIVE        |
    +--------------------+---------------+
    ```

After the installation, you can use the `--audit_log_filter` option when restarting the server. To prevent the server from not running the plugin use `--audit_log_filter` with either the `FORCE` or the `FORCE_PLUS_PERMANENT` values.
