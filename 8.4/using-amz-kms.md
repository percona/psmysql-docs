> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Use the Amazon Key Management Service (AWS KMS)

Percona Server for MySQL supports the [Amazon Key Management Service (AWS KMS)](https://aws.amazon.com/kms/) . Percona Server generates the keyring keys. Amazon Web Services (AWS) encrypts the keyring data.

The AWS KMS lets you create and manage cryptographic keys across AWS services. For more information, see the [AWS Key Management Service Documentation](https://docs.aws.amazon.com/kms/) .

## Prerequisites

Complete the following before you install the AWS KMS component:

- Create an AWS user with an access key and a secret key.
- Create a KMS key. Reference the key by its identifier, alias, or Amazon Resource Name (ARN). Each key can have any number of aliases.

Install a keyring component through a manifest file. During startup, the server reads the manifest. Each component reads a corresponding configuration file during initialization.

Do not load keyring components with either of the following methods:

| Method                        | Why it fails                                                                                              |
| ----------------------------- | --------------------------------------------------------------------------------------------------------- |
| `--early-plugin-load` option  | Loads plugins only, not components                                                                        |
| `INSTALL COMPONENT` statement | Registers components in the `mysql.component` table, which the server loads after `InnoDB` initialization |

Components that `InnoDB` requires at startup must load earlier.

Create a global manifest file named `mysqld.my` in the installation directory. Optionally, create a local manifest file with the same name in a data directory.

To install a keyring component, complete the following steps:

1. Write a manifest in valid JSON format

Each component uses the same manifest mechanism. Each component reads its own configuration file. The name of the configuration file matches the component name with a `.cnf` extension. For example, `component_keyring_vault` reads `component_keyring_vault.cnf`.

## Manifest files

### Manifest fields

The manifest is a JavaScript Object Notation (JSON) object with the following fields:

| Field                 | Type    | Required    | Description                                                                                                                                                          |
| --------------------- | ------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `components`          | string  | Conditional | URL-style locator for the component to load. The format is `file://<component_name>`. Required when the manifest declares the component directly.                    |
| `read_local_manifest` | boolean | No          | When `true`, the global manifest delegates to the local manifest in the data directory. When `false` or absent, the global manifest declares the component directly. |

### Manifest examples

Replace `<component_name>` in the following examples with one of the available components.

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
| [`INSTALL COMPONENT`](https://docs.percona.com/percona-server/8.4/install-component.md) | The statement runs as SQL and cannot execute until step 4. The registration record lives in `mysql.component`, an `InnoDB` table that the server reads only after `InnoDB` initializes. The system tablespace cannot decrypt without the keyring, which creates a circular dependency. Crash recovery also runs before the SQL layer, so the encrypted redo log must remain readable without SQL. |
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

The InnoDB master key wraps the tablespace keys that protect data on disk. Rotate the master key on a scheduled cadence to limit the volume of data wrapped by any single master key.

Run the following statement to rotate the master key:

```sql
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

The statement generates a master key and stores the key in the keyring. The server then wraps subsequent tablespace keys with the stored key.

The rotation operation is fast. The server does not re-encrypt the tablespace data.

Earlier master keys must remain in the keyring. Deleting an earlier master key prevents the server from reading data that was wrapped with that key.

For required privileges and the full rotation procedure, see [Rotate the master encryption key](https://docs.percona.com/percona-server/8.4/rotate-master-key.md).

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

For more information, see [Installing and uninstalling components](https://dev.mysql.com/doc/refman/8.4/en/component-loading.html) .

## Configuration settings

The configuration settings live in either a global configuration file or a local configuration file.

### Configuration parameters

The `component_keyring_kms.cnf` file contains the following parameters:

- `read_local_config [optional]` — declares whether the component reads the local configuration file. Use this parameter only in the global configuration file. The allowed values are `true` or `false`.

- `path` — the path to the keyring file on the local host. The file uses JSON format.

- `read_only [optional]` — when `true`, the component prevents runtime changes to the keyring. The default value is `false`.

- `kms_key` — the identifier of an AWS KMS master key. Create the key before you create the manifest file. The identifier accepts one of the following formats:

  - Universally Unique Identifier (UUID)
  - Alias
  - Amazon Resource Name (ARN)

  For more information, see [Finding the key ID and key ARN](https://docs.aws.amazon.com/kms/latest/developerguide/find-cmk-id-arn.html) .

- `region` — the AWS region that hosts the KMS key. Each Hypertext Transfer Protocol (HTTP) request connects to this region.

- `auth_key` — the access key for the AWS user. The user must have permission to access the KMS key.

- `secret_access_key` — the secret key for the AWS user.

Warning

The configuration file contains authentication credentials. Restrict read access on the file to the `mysql` user.

#### Example configuration

The following example shows a `component_keyring_kms.cnf` file in JSON format with placeholder values. Replace each placeholder with the value for the target AWS KMS deployment.

```json
{
  "read_local_config": false,
  "path": "/usr/local/mysql/keyring-mysql/aws-keyring-data",
  "region": "<AWS_REGION>",
  "kms_key": "<KMS_KEY_IDENTIFIER>",
  "auth_key": "<AWS_USER_ACCESS_KEY>",
  "secret_access_key": "<AWS_USER_SECRET_ACCESS_KEY>"
}
```

## Verify the keyring component

After you start Percona Server for MySQL, confirm that the keyring component loaded and initialized. Query the `performance_schema.keyring_component_status` table:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

The query returns one row for each status key that the loaded component reports. The `Component_status` row indicates the result of initialization:

| `Component_status` value | Meaning                                                                               | Recovery                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `Active`                 | The component loaded and initialized successfully                                     | None                                                                                                  |
| `Disabled`               | The component loaded but failed to initialize, typically due to a configuration error | Review the server error log, correct the configuration file, then run `ALTER INSTANCE RELOAD KEYRING` |

If a keyring component fails to load entirely, the server does not start. Check the server error log for diagnostic messages.

For the complete list of status keys that each component reports, see [keyring_component_status Table](https://dev.mysql.com/doc/refman/%7B%7Bvers%7D%7D/en/performance-schema-keyring-component-status-table.html) in the MySQL Reference Manual.

## Related topics

- [Keyring components overview](https://docs.percona.com/percona-server/8.4/keyring-components-plugins-overview.md)
- [Use the keyring file component](https://docs.percona.com/percona-server/8.4/use-keyring-file.md)
- [Use the keyring vault component](https://docs.percona.com/percona-server/8.4/use-keyring-vault-component.md)
- [Use the Key Management Interoperability Protocol (KMIP)](https://docs.percona.com/percona-server/8.4/using-kmip.md)
- [Data at rest encryption](https://docs.percona.com/percona-server/8.4/data-at-rest-encryption.md) For more information, see [Keyring component installation](https://dev.mysql.com/doc/refman/8.4/en/keyring-component-installation.html) .
