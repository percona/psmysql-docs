
A keyring component loads at server startup from a manifest file. The component reads a JSON configuration file during initialization. Do not load a keyring component with `INSTALL COMPONENT`. InnoDB needs the keyring before the `mysql.component` table is available.


## Available keyring components

Percona Server provides the following keyring components:

| Component | Backend |
|---|---|
| `component_keyring_file` | Local file on disk |
| `component_keyring_kmip` | Key Management Interoperability Protocol (KMIP) server |
| `component_keyring_kms` | Cloud Key Management Service (KMS) |
| `component_keyring_vault` | HashiCorp Vault |

Each component uses the same manifest mechanism. Each component reads its own configuration file. The name of the configuration file matches the component name with a `.cnf`

Create a global manifest file named `mysqld.my` in the directory that contains the `mysqld` binary. For multiple instances on one host, create a local manifest file with the same name in each data directory.

If the manifest file does not exist, the server does not load the keyring component. During startup, the server reads the global manifest from the installation directory. The global manifest can list the component directly or point to a local manifest in the data directory.
## Manifest files

The manifest is a JavaScript Object Notation (JSON) object with the following fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `components` | string | Conditional | URL-style locator for the component to load. The format is `file://<component_name>`. Required when the manifest declares the component directly. |
| `read_local_manifest` | boolean | No | When `true`, the global manifest delegates to the local manifest in the data directory. When `false` or absent, the global manifest declares the component directly. |

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

| Manifest | Location | Purpose |
|---|---|---|
| Global manifest | The directory that contains the `mysqld` binary | Default manifest for the server installation |
| Local manifest | Data directory | Per-instance override for hosts that run multiple instances with different keyring components |

Both files use the name `mysqld.my`. The global manifest declares the component directly or delegates to the local manifest.

### Why the manifest is the only supported load path

The keyring must load before `InnoDB` opens an encrypted page. Any mechanism that depends on the Structured Query Language (SQL) layer therefore loads the keyring too late.

A `mysqld` startup proceeds in the following order:

1. `mysqld` parses startup configuration and reads the manifest file from the server installation directory.

2. The server loads each component named in the manifest.

3. `InnoDB` initializes, replays the redo log, and opens tablespaces.

4. The SQL layer accepts connections.

The keyring must load between steps 1 and 3. The following table explains why each alternative mechanism fails to load the keyring within this window:

| Mechanism | Reason for failure |
|---|---|
| [`INSTALL COMPONENT`](install-component.md) | The statement runs as SQL and cannot execute until step 4. The registration record lives in `mysql.component`, an `InnoDB` table that the server reads only after `InnoDB` initializes. The system tablespace cannot decrypt without the keyring, which creates a circular dependency. Crash recovery also runs before the SQL layer, so the encrypted redo log must remain readable without SQL. |
| `--early-plugin-load` | The flag applies to legacy keyring plugins, not components. Plugins and components load through separate subsystems. The flag cannot locate component entry points. |

A component registered through `INSTALL COMPONENT` on a running server does not persist across restarts. On the next restart, `InnoDB` cannot unwrap tablespace keys because no manifest file exists on disk. A missing or malformed `mysqld.my` therefore prevents startup for any instance with encrypted tablespaces.

## Install a keyring component

To install a keyring component:

1. Stop the `mysqld` process.

2. Create the manifest file at the chosen location. Use one of the examples in [Manifest examples](#manifest-examples) as a template.

3. Create the configuration file in the same directory as the manifest that declares the component. The name of the configuration file matches the component name with a `.cnf` extension.

4. Populate the configuration file with parameters for the chosen component. The required parameters depend on the component.

5. Set the file ownership of the manifest file and the configuration file to the `mysql` user.

6. Restrict read access on the configuration file to the `mysql` user. The configuration file may contain credentials.

7. Start the `mysqld` process.

## Verify the installation

Connect to the server and run the following query:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

The query returns one row per status field. The `Component_status` field reports `Active` when the component loaded. The `Component_status` field reports `Disabled` when the component failed to load. Inspect the server error log to identify the cause of any failure.

## Operate the keyring

### Rotate the master key

The InnoDB master key wraps the tablespace keys that protect data on disk. Rotate the master key on a scheduled cadence. Scheduled rotation limits the volume of data wrapped by any single master key. See [Data at Rest Encryption](data-at-rest-encryption.md) for the role of the master key.

Run the following statement to rotate the master key:

```sql
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

The statement generates a master key and stores the key in the keyring. The server then wraps subsequent tablespace keys with the stored key.

The rotation operation is fast. The server does not re-encrypt the tablespace data.

Earlier master keys must remain in the keyring. Deleting an earlier master key prevents the server from reading data that was wrapped with that key.

For required privileges and the full rotation procedure, see [Rotate the master encryption key](rotate-master-key.md).

### Monitor the keyring

Use the query in [Verify the installation](#verify-the-installation) to inspect the keyring at runtime. Configure alerts on `Component_status` transitions to `Disabled`. Watch the server error log for keyring-related errors. The server writes manifest parse errors, configuration parse errors, and backend connection errors to the error log.

### Back up and restore

A backup of an encrypted tablespace requires keyring access on the destination host. The destination host must read the same key material that encrypted the backup.

The following table summarizes the keyring requirement for each backend:

| Backend | Backup requirement |
|---|---|
| `component_keyring_file` | Copy the keyring file alongside the data backup. The destination host must read the same key material. |
| `component_keyring_vault` | Configure the destination host to authenticate with the same Vault server and access the same `secret_mount_point`. |
| `component_keyring_kmip` | Configure the destination host to authenticate with the same KMIP server and access the same key namespace. |
| `component_keyring_kms` | Configure the destination host with credentials and permissions for the same cloud KMS keys. |

Test a restore on a separate host before relying on the backup. A restore that runs on the original host can succeed even when the keyring configuration is incorrect.

## Replace or remove a keyring component

To replace a keyring component:

1. Stop the `mysqld` process.

2. Edit the manifest file to reference the replacement component.

3. Create the configuration file for the replacement component.

4. Start the `mysqld` process.

To remove the keyring:

1. Confirm that no encrypted tablespaces exist on the server. A server with encrypted tablespaces cannot start without a keyring.

2. Stop the `mysqld` process.

3. Delete the manifest file.

4. Start the `mysqld` process.

!!! warning

    Configure exactly one keyring per server instance. Percona Server does not support multiple keyring plugins, multiple keyring components, or any combination of plugin and component. Such configurations risk data loss.
