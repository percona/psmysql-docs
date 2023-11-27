# Install the Audit Log Filter

The `plugin_dir` system variable defines the component library location. If needed, at server startup, set the `plugin_dir` variable.

In the `share` directory, locate the `audit_log_filter_linux_install.sql `script.

At the time you run the script, you can select the database used to store the JSON filter tables. 

* If the component is loaded, the installation script takes the database name from the `audit_log_filter.database` variable
* If the component is not loaded, but passes the `-D db_name` to the mysql client when the installation script runs, uses the `db_name`.
* If the component is not loaded and the `-D` option is not provided, the installation script creates the required tables in the default database name `mysql`.

You can also designate a different database with the `audit_log_filter.database` system variable. The database name cannot be NULL or exceed 64 characters. If the database name is invalid, the audit log filter tables are not found.

To install the component, run the following command:

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://component_audit_log_filter';
```

Find more information in the [INSTALL COMPONENT](install-component.md) document.

After the installation, you can use the `--audit_log_filter` option when restarting the server. To prevent the server from not running the plugin use `--audit_log_filter` with either the `FORCE` or the `FORCE_PLUS_PERMANENT` values.

To upgrade from `audit_log_filter` plugin in Percona Server 8.0 to `component_audit_log_filter` component in Percona Server {{vers}}, do the [manual upgrade](upgrade-components.md).
