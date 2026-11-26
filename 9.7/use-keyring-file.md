> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Use the keyring file component

The `component_keyring_file` component stores encryption keys in a local file on the server filesystem. Percona Server for MySQL uses this component for [data at rest encryption](https://docs.percona.com/percona-server/9.7/data-at-rest-encryption.md), including InnoDB tablespace encryption and encrypted redo and undo logs. Other server features that need a keyring, such as the audit log filter component, can also use it.

In Percona Server for MySQL 9.7, the supported keyring model is component-based. The legacy `keyring_file` plugin is not available.

Important

Percona Server for MySQL 9.7 does not support the `keyring_file` plugin. Use `component_keyring_file` instead.

Enable only one keyring at a time. Do not load legacy keyring plugins (such as `keyring_file` or `keyring_vault`) together with a keyring component.

If you already have data encrypted with a legacy keyring plugin, plan a migration before switching to the component keyring. Keys and encrypted data from the old plugin are not readable by the new component without migration. See [Upgrade components](https://docs.percona.com/percona-server/9.7/upgrade-components.md) and [Get Started with component keyring](https://docs.percona.com/percona-server/9.7/quickstart-component-keyring.md).

For a step-by-step setup walkthrough, see [Get Started with component keyring](https://docs.percona.com/percona-server/9.7/quickstart-component-keyring.md).

A keyring component loads at server startup from a manifest file. The component reads a JSON configuration file during initialization. Do not load a keyring component with `INSTALL COMPONENT`. InnoDB needs the keyring before the `mysql.component` table is available.

## Available keyring components

Percona Server provides the following keyring components:

| Component                 | Backend                                                |
| ------------------------- | ------------------------------------------------------ |
| `component_keyring_file`  | Local file on disk                                     |
| `component_keyring_kmip`  | Key Management Interoperability Protocol (KMIP) server |
| `component_keyring_kms`   | Cloud Key Management Service (KMS)                     |
| `component_keyring_vault` | HashiCorp Vault                                        |

Each component uses the same manifest mechanism. Each component reads its own configuration file. The name of the configuration file matches the component name with a `.cnf`

Create a global manifest file named `mysqld.my` in the directory that contains the `mysqld` binary. For multiple instances on one host, create a local manifest file with the same name in each data directory.

If the manifest file does not exist, the server does not load the keyring component. During startup, the server reads the global manifest from the installation directory. The global manifest can list the component directly or point to a local manifest in the data directory.

## Manifest files

The manifest is a JavaScript Object Notation (JSON) object with the following fields:

| Field                 | Type    | Required    | Description                                                                                                                                                          |
| --------------------- | ------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `components`          | string  | Conditional | URL-style locator for the component to load. The format is `file://<component_name>`. Required when the manifest declares the component directly.                    |
| `read_local_manifest` | boolean | No          | When `true`, the global manifest delegates to the local manifest in the data directory. When `false` or absent, the global manifest declares the component directly. |

### Manifest examples

Replace `<component_name>` in the following examples with one of the components in [Available keyring components](#available-keyring-components).

The following example shows a global manifest that loads a component directly:

```json
{
  "components": "file://<component_name>"
}
```

The following example shows a global manifest that delegates to the local manifest:

```json
{
  "read_local_manifest": true
}
```

The following example shows a local manifest:

```json
{
  "components": "file://<component_name>"
}
```

### Manifest locations

Percona Server reads two manifest files at startup:

| Manifest        | Location                                        | Purpose                                                                                       |
| --------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Global manifest | The directory that contains the `mysqld` binary | Default manifest for the server installation                                                  |
| Local manifest  | Data directory                                  | Per-instance override for hosts that run multiple instances with different keyring components |

Both files use the name `mysqld.my`. The global manifest declares the component directly or delegates to the local manifest.

### Why the manifest is the only supported load path

The keyring must load before `InnoDB` opens an encrypted page. Any mechanism that depends on the Structured Query Language (SQL) layer therefore loads the keyring too late.

A `mysqld` startup proceeds in the following order:

1. `mysqld` parses startup configuration and reads the manifest file from the server installation directory.
1. The server loads each component named in the manifest.
1. `InnoDB` initializes, replays the redo log, and opens tablespaces.
1. The SQL layer accepts connections.

The keyring must load between steps 1 and 3. The following table explains why each alternative mechanism fails to load the keyring within this window:

| Mechanism                                                                               | Reason for failure                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`INSTALL COMPONENT`](https://docs.percona.com/percona-server/9.7/install-component.md) | The statement runs as SQL and cannot execute until step 4. The registration record lives in `mysql.component`, an `InnoDB` table that the server reads only after `InnoDB` initializes. The system tablespace cannot decrypt without the keyring, which creates a circular dependency. Crash recovery also runs before the SQL layer, so the encrypted redo log must remain readable without SQL. |
| `--early-plugin-load`                                                                   | The flag applies to legacy keyring plugins, not components. Plugins and components load through separate subsystems. The flag cannot locate component entry points.                                                                                                                                                                                                                               |

A component registered through `INSTALL COMPONENT` on a running server does not persist across restarts. On the next restart, `InnoDB` cannot unwrap tablespace keys because no manifest file exists on disk. A missing or malformed `mysqld.my` therefore prevents startup for any instance with encrypted tablespaces.

## Install a keyring component

To install a keyring component:

1. Stop the `mysqld` process.
1. Create the manifest file at the chosen location. Use one of the examples in [Manifest examples](#manifest-examples) as a template.
1. Create the configuration file in the same directory as the manifest that declares the component. The name of the configuration file matches the component name with a `.cnf` extension.
1. Populate the configuration file with parameters for the chosen component. The required parameters depend on the component.
1. Set the file ownership of the manifest file and the configuration file to the `mysql` user.
1. Restrict read access on the configuration file to the `mysql` user. The configuration file may contain credentials.
1. Start the `mysqld` process.

## Verify the installation

Connect to the server and run the following query:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

The query returns one row per status field. The `Component_status` field reports `Active` when the component loaded. The `Component_status` field reports `Disabled` when the component failed to load. Inspect the server error log to identify the cause of any failure.

## Operate the keyring

### Rotate the master key

The InnoDB master key wraps the tablespace keys that protect data on disk. Rotate the master key on a scheduled cadence. Scheduled rotation limits the volume of data wrapped by any single master key. See [Data at Rest Encryption](https://docs.percona.com/percona-server/9.7/data-at-rest-encryption.md) for the role of the master key.

Run the following statement to rotate the master key:

```sql
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

The statement generates a master key and stores the key in the keyring. The server then wraps subsequent tablespace keys with the stored key.

The rotation operation is fast. The server does not re-encrypt the tablespace data.

Earlier master keys must remain in the keyring. Deleting an earlier master key prevents the server from reading data that was wrapped with that key.

For required privileges and the full rotation procedure, see [Rotate the master encryption key](https://docs.percona.com/percona-server/9.7/rotate-master-key.md).

### Monitor the keyring

Use the query in [Verify the installation](#verify-the-installation) to inspect the keyring at runtime. Configure alerts on `Component_status` transitions to `Disabled`. Watch the server error log for keyring-related errors. The server writes manifest parse errors, configuration parse errors, and backend connection errors to the error log.

### Back up and restore

A backup of an encrypted tablespace requires keyring access on the destination host. The destination host must read the same key material that encrypted the backup.

The following table summarizes the keyring requirement for each backend:

| Backend                   | Backup requirement                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `component_keyring_file`  | Copy the keyring file alongside the data backup. The destination host must read the same key material.              |
| `component_keyring_vault` | Configure the destination host to authenticate with the same Vault server and access the same `secret_mount_point`. |
| `component_keyring_kmip`  | Configure the destination host to authenticate with the same KMIP server and access the same key namespace.         |
| `component_keyring_kms`   | Configure the destination host with credentials and permissions for the same cloud KMS keys.                        |

Test a restore on a separate host before relying on the backup. A restore that runs on the original host can succeed even when the keyring configuration is incorrect.

## Replace or remove a keyring component

To replace a keyring component:

1. Stop the `mysqld` process.
1. Edit the manifest file to reference the replacement component.
1. Create the configuration file for the replacement component.
1. Start the `mysqld` process.

To remove the keyring:

1. Confirm that no encrypted tablespaces exist on the server. A server with encrypted tablespaces cannot start without a keyring.
1. Stop the `mysqld` process.
1. Delete the manifest file.
1. Start the `mysqld` process.

Warning

Configure exactly one keyring per server instance. Percona Server does not support multiple keyring plugins, multiple keyring components, or any combination of plugin and component. Such configurations risk data loss.

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

- `read_local_config` [optional] — use only in the global configuration file. Indicates whether the component should read configuration from a local file in the data directory. Allowed values are `true` or `false`. If you omit this option, the component uses only the global configuration file.

  When `read_local_config` appears in the global file along with other items, the component evaluates it first:

  - `false` — the component uses the other items in the global file and ignores the local configuration file.
  - `true` — the component ignores the other items in the global file and reads the local configuration file instead.

- `path` — the full path to the keyring data file. The component creates this file on first use if it does not exist. The directory must exist and be writable by the MySQL server user. Use a dedicated directory with restricted permissions, not the data directory itself.

- `read_only` [optional] — when `true`, the keyring cannot be modified at runtime (no new keys and no key removal). The default is `false`. Set `read_only` to `true` on replicas or read-only nodes where keys should not change.

Example of a configuration file in JSON format

```json
{
  "path": "/var/lib/mysql-keyring/component_keyring_file",
  "read_only": false
}
```

Protect the keyring data file

The file at `path` holds the keys that decrypt your data. Restrict filesystem access to the keyring directory and include the keyring file in your backup and restore procedures.

If the keyring file is lost, corrupted, or replaced, encrypted tablespaces, redo logs, and undo logs that depend on those keys are **unrecoverable**. Do not delete or manually edit the keyring file to rotate keys. Use [Rotate the master encryption key](https://docs.percona.com/percona-server/9.7/rotate-master-key.md) instead.

## Verify the component is loaded

After a restart, confirm that the keyring is active:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

When the component loaded successfully, the result includes:

| STATUS_KEY       | Expected value                                   |
| ---------------- | ------------------------------------------------ |
| Component_name   | `component_keyring_file`                         |
| Component_status | `Active`                                         |
| Data_file        | The `path` value from your configuration file    |
| Read_only        | `Yes` or `No`, matching your `read_only` setting |

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

An `Active` status means the keyring is ready. It does not mean your data is encrypted yet. Enable encryption separately for tables, tablespaces, and logs. See [Data at Rest Encryption](https://docs.percona.com/percona-server/9.7/data-at-rest-encryption.md).

If the server starts but the component is missing or inactive, check the error log (`SELECT @@log_error;`) for JSON syntax errors in the manifest or configuration file, missing component libraries in `@@plugin_dir`, or permission problems on the manifest, configuration, or keyring paths.

## Use the keyring with encryption

With `component_keyring_file` active, you can enable transparent data encryption (TDE) for:

- Individual tables and schema defaults — see [Encrypt file-per-table tablespace](https://docs.percona.com/percona-server/9.7/encrypt-file-per-table-tablespace.md) and [Encrypt schema or general tablespace](https://docs.percona.com/percona-server/9.7/encrypt-tablespaces.md)
- The system tablespace — see [Encrypt system tablespace](https://docs.percona.com/percona-server/9.7/encrypt-system-tablespace.md)
- Redo and undo logs — see [Log encryption](https://docs.percona.com/percona-server/9.7/encrypt-logs.md)
- Binary and relay logs — see [Encrypt binary log files and relay log files](https://docs.percona.com/percona-server/9.7/encrypt-binary-relay-log-files.md)

To confirm encryption settings after you enable them, see [Verify encryption](https://docs.percona.com/percona-server/9.7/verify-encryption.md).

## Operational notes

- **Backups** — back up the keyring file together with encrypted data. Restoring encrypted tablespaces or logs without the matching keyring file fails.
- **Cloning and migration** — when you move an instance to new hardware or copy a datadir, copy the keyring file to the new host before starting the server with encrypted data.
- **Percona XtraDB Cluster (PXC)** — the keyring file is not replicated. Copy the keyring file from the bootstrap node to other nodes before they start with encrypted data.
- **Master key rotation** — use `ALTER INSTANCE ROTATE INNODB MASTER KEY` to rotate the InnoDB master key. See [Rotate the master encryption key](https://docs.percona.com/percona-server/9.7/rotate-master-key.md).
- **Permissions** — the MySQL server user needs read access to the manifest and configuration files and read/write access to the keyring directory. A typical layout is `root:root` with mode `644` on the manifest, `640` on the configuration file, and `750` on the keyring directory owned by the MySQL user.

## Uninstall the component

To stop using the file keyring:

1. Remove or rename the manifest entry for `file://component_keyring_file` in `mysqld.my`.
1. Remove or rename `component_keyring_file.cnf`.
1. Restart the server.

Do not delete the keyring data file if any data on the instance was encrypted with it. You need that file to decrypt existing encrypted tablespaces and logs.

See also

[Keyring components overview](https://docs.percona.com/percona-server/9.7/keyring-components-plugins-overview.md)

[Get Started with component keyring](https://docs.percona.com/percona-server/9.7/quickstart-component-keyring.md)

[Data at Rest Encryption](https://docs.percona.com/percona-server/9.7/data-at-rest-encryption.md)

[Upgrade components](https://docs.percona.com/percona-server/9.7/upgrade-components.md)

[Rotate the master encryption key](https://docs.percona.com/percona-server/9.7/rotate-master-key.md)
