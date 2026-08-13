# Use the keyring file component

The `component_keyring_file` component stores encryption keys in a local file on the server filesystem. Percona Server for MySQL uses this component for [data at rest encryption](data-at-rest-encryption.md), including InnoDB tablespace encryption and encrypted redo and undo logs. Other server features that need a keyring, such as the audit log filter component, can also use it.

In Percona Server for MySQL {{vers}}, the supported keyring model is component-based. The legacy `keyring_file` plugin is not available.

!!! important

    Percona Server for MySQL {{vers}} does not support the `keyring_file` plugin. Use `component_keyring_file` instead.

    Enable only one keyring at a time. Do not load legacy keyring plugins (such as `keyring_file` or `keyring_vault`) together with a keyring component.

    If you already have data encrypted with a legacy keyring plugin, plan a migration before switching to the component keyring. Keys and encrypted data from the old plugin are not readable by the new component without migration. See [Upgrade components](upgrade-components.md) and [Get Started with component keyring](quickstart-component-keyring.md).

For a step-by-step setup walkthrough, see [Get Started with component keyring](quickstart-component-keyring.md).

--8<--- "keyring-components-installation.md"

## Manifest file

The manifest tells the server to load `component_keyring_file` at startup. Create a file named `mysqld.my` in JSON format.

The server reads a global manifest from the directory that contains the `mysqld` binary. The path depends on your install method. Package installs on Linux often use `/usr/sbin/mysqld.my`. Tarball installs, containers, and custom builds may use another directory. Confirm the `mysqld` binary location before you create the manifest. You can also use a local manifest in the data directory when multiple instances on the same host need different keyring components.

The following example is a global manifest file that does not use local manifests:

```json
{
  "read_local_manifest": false,
  "components": "file://component_keyring_file"
}
```

The following is an example of a global manifest file that points to a local manifest file:

```json
{
  "read_local_manifest": true
}
```

The following is an example of a local manifest file:

```json
{
  "components": "file://component_keyring_file"
}
```

When `read_local_manifest` is `true`, the global manifest contains only that setting. The server reads the component list from `mysqld.my` in the data directory.

After you create or change a manifest, restart the server. Loading a keyring component from a manifest is not supported at runtime with `INSTALL COMPONENT`; InnoDB needs the keyring during startup.

## Configuration file

The component reads settings from a JSON configuration file named `component_keyring_file.cnf`.

By default, the global configuration file is in the plugin directory. Confirm the path with:

```sql
SELECT @@plugin_dir;
```

Typical locations are `/usr/lib64/mysql/plugin` on RHEL-style systems and `/usr/lib/mysql/plugin` on Debian and Ubuntu.

You can also place a local configuration file in the data directory when `read_local_config` is enabled in the global file. This pattern is useful when several server instances share one installation but need separate keyring files.

The configuration settings are either in a global configuration file or a local configuration file.

The `component_keyring_file.cnf` file supports the following options:

* `read_local_config` [optional] — use only in the global configuration file. Indicates whether the component should read configuration from a local file in the data directory. Allowed values are `true` or `false`. If you omit this option, the component uses only the global configuration file.

    When `read_local_config` appears in the global file along with other items, the component evaluates it first:

    * `false` — the component uses the other items in the global file and ignores the local configuration file.

    * `true` — the component ignores the other items in the global file and reads the local configuration file instead.

* `path` — the full path to the keyring data file. The component creates this file on first use if it does not exist. The directory must exist and be writable by the MySQL server user. Use a dedicated directory with restricted permissions, not the data directory itself.

* `read_only` [optional] — when `true`, the keyring cannot be modified at runtime (no new keys and no key removal). The default is `false`. Set `read_only` to `true` on replicas or read-only nodes where keys should not change.

??? example "Example of a configuration file in JSON format"

     ```json
     {
       "path": "/var/lib/mysql-keyring/component_keyring_file",
       "read_only": false
     }
     ```

!!! warning "Protect the keyring data file"

    The file at `path` holds the keys that decrypt your data. Restrict filesystem access to the keyring directory and include the keyring file in your backup and restore procedures.

    If the keyring file is lost, corrupted, or replaced, encrypted tablespaces, redo logs, and undo logs that depend on those keys are **unrecoverable**. Do not delete or manually edit the keyring file to rotate keys. Use [Rotate the master encryption key](rotate-master-key.md) instead.

## Verify the component is loaded

After a restart, confirm that the keyring is active:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

When the component loaded successfully, the result includes:

| STATUS_KEY       | Expected value                                      |
|------------------|-----------------------------------------------------|
| Component_name   | `component_keyring_file`                            |
| Component_status | `Active`                                            |
| Data_file        | The `path` value from your configuration file       |
| Read_only        | `Yes` or `No`, matching your `read_only` setting    |

Example:

```text
+---------------------+-----------------------------------------------+
| STATUS_KEY          | STATUS_VALUE                                  |
+---------------------+-----------------------------------------------+
| Component_name      | component_keyring_file                        |
| Component_status    | Active                                        |
| Data_file           | /var/lib/mysql-keyring/component_keyring_file |
| Read_only           | No                                            |
+---------------------+-----------------------------------------------+
```

An `Active` status means the keyring is ready. It does not mean your data is encrypted yet. Enable encryption separately for tables, tablespaces, and logs. See [Data at Rest Encryption](data-at-rest-encryption.md).

If the server starts but the component is missing or inactive, check the error log (`SELECT @@log_error;`) for JSON syntax errors in the manifest or configuration file, missing component libraries in `@@plugin_dir`, or permission problems on the manifest, configuration, or keyring paths.

## Use the keyring with encryption

With `component_keyring_file` active, you can enable transparent data encryption (TDE) for:

* Individual tables and schema defaults — see [Encrypt file-per-table tablespace](encrypt-file-per-table-tablespace.md) and [Encrypt schema or general tablespace](encrypt-tablespaces.md)
* The system tablespace — see [Encrypt system tablespace](encrypt-system-tablespace.md)
* Redo and undo logs — see [Log encryption](encrypt-logs.md)
* Binary and relay logs — see [Encrypt binary log files and relay log files](encrypt-binary-relay-log-files.md)

To confirm encryption settings after you enable them, see [Verify encryption](verify-encryption.md).

## Operational notes

* **Backups** — back up the keyring file together with encrypted data. Restoring encrypted tablespaces or logs without the matching keyring file fails.

* **Cloning and migration** — when you move an instance to new hardware or copy a datadir, copy the keyring file to the new host before starting the server with encrypted data.

* **Percona XtraDB Cluster (PXC)** — the keyring file is not replicated. Copy the keyring file from the bootstrap node to other nodes before they start with encrypted data.

* **Master key rotation** — use `ALTER INSTANCE ROTATE INNODB MASTER KEY` to rotate the InnoDB master key. See [Rotate the master encryption key](rotate-master-key.md).

* **Permissions** — the MySQL server user needs read access to the manifest and configuration files and read/write access to the keyring directory. A typical layout is `root:root` with mode `644` on the manifest, `640` on the configuration file, and `750` on the keyring directory owned by the MySQL user.

## Uninstall the component

To stop using the file keyring:

1. Remove or rename the manifest entry for `file://component_keyring_file` in `mysqld.my`.
2. Remove or rename `component_keyring_file.cnf`.
3. Restart the server.

Do not delete the keyring data file if any data on the instance was encrypted with it. You need that file to decrypt existing encrypted tablespaces and logs.

!!! admonition "See also"

    [Keyring components overview](keyring-components-plugins-overview.md)

    [Get Started with component keyring](quickstart-component-keyring.md)

    [Data at Rest Encryption](data-at-rest-encryption.md)

    [Upgrade components](upgrade-components.md)

    [Rotate the master encryption key](rotate-master-key.md)
