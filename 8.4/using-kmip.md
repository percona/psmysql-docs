> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Use the Key Management Interoperability Protocol (KMIP)

Percona Server for MySQL supports the [OASIS Key Management Interoperability Protocol (KMIP)](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html) . Percona has validated the KMIP implementation against the following servers:

- [PyKMIP server](https://pykmip.readthedocs.io/en/latest/server.html)
- [HashiCorp Vault Enterprise KMIP Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/kmip)
- [Thales CipherTrust Manager](https://cpl.thalesgroup.com/encryption/ciphertrust-manager)
- [Fortanix Data Security Manager](https://www.fortanix.com/products/data-security-manager)

KMIP enables communication between key management systems and the database server. The protocol provides the following capabilities:

- Centralized storage and lifecycle management for encryption keys
- Standardized key exchange between databases and key management systems

## Component installation

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

For more information, see [Installing and Uninstalling Components](https://dev.mysql.com/doc/refman/8.4/en/component-loading.html) .

The following example shows a global manifest file that does not use local manifests:

```json
{
 "read_local_manifest": false,
 "components": "file://component_keyring_kmip"
}
```

The following example shows a global manifest file that references a local manifest file:

```json
{
 "read_local_manifest": true
}
```

The following example shows a local manifest file:

```json
{
 "components": "file://component_keyring_kmip"
}
```

Both global and local configuration files use the same settings. The following example shows a configuration file:

```json
{
 "server_addr": "127.0.0.1",
 "server_port": "5696",
 "client_ca": "client_certificate.pem",
 "client_key": "client_key.pem",
 "server_ca": "root_certificate.pem",
 "object_group": "",
 "max_objects": 65535,
 "kmip_timeout_ms": 5000,
 "tls_peer_verification": false,
 "tls_hostname_verification": false
}
```

### Configuration options

The configuration file for the KMIP keyring supports the following options:

| Option                      | Type    | Required | Default | Description                                                                                                                       |
| --------------------------- | ------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `server_addr`               | string  | Yes      | —       | Hostname or IP address of the KMIP server                                                                                         |
| `server_port`               | string  | Yes      | —       | TCP port of the KMIP server, for example `"5696"`                                                                                 |
| `client_ca`                 | string  | Yes      | —       | Path to the client certificate presented to the KMIP server, in Privacy-Enhanced Mail (PEM) format                                |
| `client_key`                | string  | Yes      | —       | Path to the client private key that matches `client_ca`, in PEM format                                                            |
| `server_ca`                 | string  | Yes      | —       | Path to the certificate authority (CA) certificate that verifies the KMIP server, in PEM format                                   |
| `object_group`              | string  | No       | `""`    | KMIP object group used to register and enumerate objects; an empty value disables grouping                                        |
| `max_objects`               | integer | No       | `65535` | Maximum objects retrieved per object type in one locate operation. Applies to symmetric keys and secret data                      |
| `kmip_timeout_ms`           | integer | No       | `5000`  | KMIP connection timeout in milliseconds                                                                                           |
| `tls_peer_verification`     | boolean | No       | `false` | When `true`, verifies the Transport Layer Security (TLS) certificate of the KMIP server against `server_ca`                       |
| `tls_hostname_verification` | boolean | No       | `false` | When `true`, verifies `server_addr` against the Subject Alternative Name (SAN) or Common Name (CN) of the KMIP server certificate |

#### TLS verification

Both `tls_peer_verification` and `tls_hostname_verification` default to `false` for backward compatibility. Enable both options in production deployments. The KMIP keyring backend then rejects connections to KMIP servers that present an untrusted or mismatched certificate.

To enable peer verification, set `server_ca` to the certificate authority that signed the KMIP server certificate. To enable hostname verification, set `server_addr` to match the SAN or CN of the KMIP server certificate.

### KMIP object state requirements

The KMIP keyring backend loads only objects in the `ACTIVE` state. Loadable objects include symmetric keys and secret data. The backend ignores objects in the `PRE_ACTIVE`, `DEACTIVATED`, `COMPROMISED`, or `DESTROYED` states. The backend activates each key or secret during registration.

Important

Activate any `PRE_ACTIVE` keys on the KMIP server before you start Percona Server for MySQL. Otherwise, Percona Server for MySQL cannot load those keys.

Use the KMIP `Activate` operation through the management interface of your KMIP server. Supported interfaces include a web console, a command-line tool, or a KMIP client library. For exact steps, see the documentation for your KMIP server.

### Supported AES key sizes

The KMIP keyring backend accepts these Advanced Encryption Standard (AES) key sizes:

| AES key size | Length in bytes |
| ------------ | --------------- |
| 128 bits     | 16              |
| 192 bits     | 24              |
| 256 bits     | 32              |

The KMIP keyring backend rejects AES keys of any other length. The `keyring_udf` plugin returns `ER_KEYRING_UDF_KEYRING_SERVICE_ERROR` for requests that specify a non-standard key size.

Important

Review any scripts or tooling that use non-standard AES key sizes before you upgrade.

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
- [Use the Amazon Key Management Service (AWS KMS)](https://docs.percona.com/percona-server/8.4/using-amz-kms.md)
- [Data at rest encryption](https://docs.percona.com/percona-server/8.4/data-at-rest-encryption.md)
