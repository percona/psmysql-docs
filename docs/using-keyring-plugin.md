# Use the keyring_plugin

You can benefit from using the `keyring_plugin` or `keyring_component` in several ways. Some of the advantages are:

- You can securely store sensitive information such as encryption keys, passwords, or credentials for later retrieval by internal server components and plugins.

- You can choose from different keyring backends such as local files, [KMIP servers], [Amazon Web Services], or HashiCorp Vault.

- You can use keyring functions to manage your keys, such as creating, reading, updating, or deleting them.




## Install the plugin

Percona Server for MySQL may use either of the following plugins:

* keyring_file stores the keyring data locally

* keyring_vault provides an interface for the database with a HashiCorp Vault server to store key and secure encryption keys.

!!! note

    Do not use the `keyring_file` plugin for regulatory compliance.

You can install the plugin using the [`INSTALL PLUGIN`] statement or add the plugin to the plugin-load option in the my.cnf file.

## Load the keyring plugin

You should load the plugin at server startup to enable keyrings with the `-early-plugin-load` option. We recommend that you load the plugin in the configuration file to facilitate recovery for encrypted tables. Also, you cannot use the redo log encryption, and the undo log encryption without `--early-plugin-load`. The normal plugin load happens too late in startup. Change the keyring_vault extension, “.so,” and the vault configuration file location to match your operating system if needed.

If a server starts with multiple plugins loaded early, the `--early-plugin-load` option should contain the plugin names in a double-quoted list, separating each plugin name by a semicolon. The double quotes ensure the semicolons do not create issues when executing the list in a script.

!!! warning 

    Enable only one keyring plugin at a time. Enabling multiple keyring plugins is not supported and may result in data loss.

To use the keyring_vault, you can add this option to your configuration file:

```text
[mysqld]
early-plugin-load="keyring_vault=keyring_vault.so"
loose-keyring_vault_config="/home/mysql/keyring_vault.conf"
```

You could also run the following command, which loads the keyring_file plugin:

```{.bash data-prompt="$"}
$ mysqld --early-plugin-load="keyring_file=keyring_file.so"
```



This plugin supports the SQL interface for keyring key management described in the [General-Purpose Keyring Key-Management Functions](https://dev.mysql.com/doc/refman/8.0/en/keyring-functions-general-purpose.html)
manual.
The plugin library contains user-defined keyring functions allowing access to the internal keyring service functions. To enable the functions, you
must enable the `keyring_udf` plugin:

```{.bash data-prompt="mysql>"}
mysql> INSTALL PLUGIN keyring_udf SONAME 'keyring_udf.so';
```

Deleting a user-created key is only possible using the `keyring_udf` plugin. This plugin deletes the key from the in-memory hash map and the Vault server.
You cannot delete system keys, such as the master key.

You must install the `keyring_udf` plugin to use user-defined functions. Attempting to use these functions without the `keyring_udf` plugin generates an error.


## 

[KMIP servers]: using-kmip.md
[Amazon Web Services]: using-amz-kms.md
[`INSTALL PLUGIN`]: https://dev.mysql.com/doc/refman/8.0/en/plugin-loading.html