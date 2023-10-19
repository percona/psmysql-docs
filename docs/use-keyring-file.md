# Use the keyring file component or keyring file plugin

## Use the keyring file plugin

Percona Server for MySQL supports the keyring_file plugin that stores the keyring data locally.

!!! warning

    The `keyring_file` plugin should not be used for regulatory compliance.

To install the plugin, follow the [installing and uninstalling plugins] instructions.

### Load the keyring plugin

You should load the plugin at server startup with the `--early-plugin-load` option to enable keyrings.

We recommend that you load the plugin in the configuration file to facilitate recovery for encrypted tables. Also, the redo log encryption and the undo log encryption cannot be used without `--early-plugin-load`. The normal plugin load happens too late at startup.

To load the keyring_file plugin, run the following command:

```{.bash data-prompt="$"}
$ mysqld --early-plugin-load="keyring_file=keyring_file.so"
```

If a server starts with different plugins loaded early, the `--early-plugin-load` option should contain the plugin names in a double-quoted list with each plugin name separated by a semicolon. The use of double quotes ensures the semicolons do not create issues when the list is executed in a script.

## Use the keyring file component

The `keyring_file` component is part of the component-based MySQL infrastructure which extends the server capabilities.

See the MySQL documentation on the [component installation] and on the [keyring_file component usage] for more information.

--8<--- "keyring-components-installation.md"

An example of a manifest and a configuration file is the following:

An example of `./bin/mysqld.my`:

```json
{
    "components": "file://component_keyring_file"
}
```

An example of `/lib/plugin/component_keyring_file.cnf`:

```json
{
    "path": "/var/lib/mysql-keyring/keyring_file", "read_only": false
}
```

[component installation]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html
[keyring_file component usage]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-file-component.html
[installing and uninstalling plugins]: https://dev.mysql.com/doc/refman/{{vers}}/en/plugin-loading.html