# Use the keyring vault component

The `keyring_vault` component connects Percona Server to a [HashiCorp Vault :octicons-link-external-16:](https://www.hashicorp.com/en/products/vault) server. The component stores and retrieves the encryption keys that protect data at rest.

--8<--- "keyring-components-installation.md"

## Configure the keyring vault component

The configuration settings live in either a global configuration file or a local configuration file.

The component connects to the [HashiCorp Vault server :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/get-vault) over Hypertext Transfer Protocol Secure (HTTPS) for production deployments. The component also accepts plain `http://` URLs for development. Prepare the certificate and key files for the secure connection. Each Vault server instance requires three artifacts:

- An organizational Certificate Authority (CA)

- A private vault key

- A server certificate signed by the CA

You can generate the artifacts with [OpenSSL :octicons-link-external-16:](https://docs.openssl.org/master/) or reuse existing files. The key files contain sensitive material. Store the key files and the password for each key in a secure location.

You can also [build a CA inside Vault :octicons-link-external-16:](https://developer.hashicorp.com/vault/tutorials/pki/pki-engine) and then issue a Vault server certificate from that CA.

### Configuration parameters

The `component_keyring_vault.cnf` file contains required and optional parameters.

#### Required parameters

* `secret_mount_point` — the mount point name where `keyring_vault` stores the keys.

* `token` — a token issued by the Vault server.

* `vault_url` — the address of the Vault server. The address must start with `http://` or `https://`. Use `https://` for production traffic. Use `http://` only for development. The component follows HTTP redirects returned by Vault. This behavior supports cluster setups where a load balancer redirects clients to the active Vault node.

#### Optional parameters

The component checks the value of `read_local_config` before any other parameter.

* `read_local_config` — Default: `false`. Declares whether the component reads the local configuration file. Use this parameter only in the global configuration file. The allowed values are `true` or `false`.

    `false` — the component processes the other parameters in the global configuration file and ignores the local configuration file.

    `true` — the component ignores the other parameters in the global configuration file and reads the local configuration file.

* `secret_mount_point_version` — Default: `AUTO`. The Key-Value (KV) Secrets Engine version (`kv` or `kv-v2`). The allowed values are `AUTO`, `1`, and `2`.

* `timeout` — Default: 15. The duration in seconds applied to both the connection phase and the total operation. The allowed range is 0 through 86400. Set the value to 0 to wait indefinitely.

* `vault_ca` — Default: unset (fallback to the host trust store). The path to the CA certificate that signed the certificate of the Vault server. Set this parameter when the host does not trust the CA of the Vault server. The component always verifies the peer certificate and the hostname when `vault_url` uses `https://`.

The component trims leading and trailing whitespace from each parameter value before parsing.

Run `SELECT * FROM performance_schema.keyring_component_status` to inspect the loaded configuration. The view reports each parameter value and the `Active` or `Disabled` status. The view also reports the component identity fields: `Component_name`, `Author`, `License`, `Implementation_name`, and `Version`.

#### Example configuration

The following example shows a `component_keyring_vault.cnf` file in JSON format with sample values for each parameter.

```json
{
  "timeout": 15,
  "vault_url": "https://vault.public.com:8202",
  "secret_mount_point": "secret",
  "secret_mount_point_version": "AUTO",
  "token": "{randomly-generated-alphanumeric-string}",
  "vault_ca": "/data/keyring_vault_confs/vault_ca.crt"
}
```

!!! warning

    Each `secret_mount_point` must serve only one Percona Server instance. Multiple servers that share a `secret_mount_point` write to the same Vault namespace. The shared namespace exposes the following risks:

    | Risk | Mechanism |
    |---|---|
    | Permanent data loss | Key writes from one server can overwrite key writes from another server. Overwritten keys cannot decrypt previously encrypted data. Cloned servers that retain a source `server_uuid` collide on InnoDB master-key names. User-named keys created through the keyring UDF surface collide on any duplicate name. |
    | Unauthorized key disclosure | Every server with access to the shared mount point can read every key stored by every other server. The component applies no per-server scoping inside the mount. |
    | Iteration noise | The keyring metadata iterator returns all keys under the mount, including keys owned by other servers. Rotation and audit tooling sees foreign keys. |

    Assign a unique `secret_mount_point` to each Percona Server instance.

The component fetches the key type and data from the Vault server on the first request for that key.

#### Validation rules

The component validates each parameter at startup. The following table lists the rejected configurations and their effects:

| Condition | Result |
|---|---|
| `secret_mount_point` ends with `/` | The component fails to initialize. |
| `secret_mount_point` starts with `/` | The component fails to initialize. |
| `timeout` exceeds 86400 | The component fails to initialize. |
| `vault_ca` is set together with an `http://` `vault_url` | The component fails to initialize. |
| `vault_url` does not start with `http://` or `https://` | The component fails to initialize. |
| `vault_url` uses `https://` but `vault_ca` is unset | The component logs an error and falls back to the host trust store for certificate validation. |

### `secret_mount_point_version` values

The `secret_mount_point_version` parameter accepts one of the following values:

| Value | Description |
|---|---|
| `1` | Works with `KV Secrets Engine - Version 1 (kv)`. The component uses `secret_mount_point` directly when forming key operation URLs. For example, the URL for a key named `skey` is `<vault_url>/v1/<secret_mount_point>/skey`. |
| `2` | Works with `KV Secrets Engine - Version 2 (kv-v2)`. Initialization splits the `secret_mount_point` parameter into two parts:<ul><li>`mount_point_path` — the mount path under which the Vault server secret was created</li><li>`directory_path` — a virtual directory suffix that creates virtual namespaces under the same real mount point</li></ul> The component uses both parts to form key access URLs, for example `<vault_url>/v1/<mount_point_path>/data/<directory_path>/skey`. |
| `AUTO` | The component probes the secrets engine to detect `kv` or `kv-v2`. The component then either uses `secret_mount_point` directly or splits the parameter into a mount point path and a directory path. See [Auto-detection algorithm](#auto-detection-algorithm). |
| Not listed | The component behaves as if `secret_mount_point_version` is set to `AUTO`. |

The component fails to initialize for any other value. Numeric values other than `1` or `2` produce an error. Non-numeric values other than `AUTO` produce a separate error.

A version mismatch causes one of the following failures:

| Configured value | Actual engine version | Result |
|---|---|---|
| `2` | `kv` (Version 1) | The component runs auto-detection during initialization to confirm the configured value. The component fails to initialize when the probe finds no `kv-v2` mount. The error message reads `Auto-detected mount point version is not the same as specified in 'secret_mount_point_version'`. |
| `1` | `kv-v2` (Version 2) | The component initializes, but every keyring operation fails. |

#### Auto-detection algorithm

The component runs the auto-detection probe during initialization in two cases:

* `secret_mount_point_version` is set to `AUTO`.

* `secret_mount_point_version` is set to `2`.

The probe walks `secret_mount_point` from the longest prefix to the shortest. The probe queries the Vault metadata configuration endpoint for each prefix. The first prefix that returns a `kv-v2` response defines the mount point path. The remainder of `secret_mount_point` becomes the directory path. The component falls back to `kv` when no prefix returns `kv-v2`.

The probe writes one informational message per prefix to the server log. The messages identify successful matches, unreadable responses, and rejected prefixes.

### Upgrade from Vault Secrets Engine Version 1 to Version 2

Use either of the following methods to upgrade from Version 1 to Version 2:

* Set `secret_mount_point_version` to `AUTO` in the `keyring_vault` configuration file on every Percona Server, or omit the parameter. The `AUTO` value triggers autodetection during component initialization.

* Set `secret_mount_point_version` to `2` to ensure each component initializes only after the upgrade from `kv` to `kv-v2` completes.

!!! note

    The `keyring_vault` component does not use the built-in key versioning of `kv-v2`. The component encodes each version into the keyring key name.

## Services exposed by the component

The `keyring_vault` component implements the following services for keyring operations. Other components and the server core consume these services to manage keys backed by Vault:

| Service | Purpose |
|---|---|
| `keyring_aes` | Performs Advanced Encryption Standard (AES) encryption and decryption with keys stored in Vault. |
| `keyring_component_metadata_query` | Reports the component metadata, including the loaded configuration values. |
| `keyring_component_status` | Reports the component status. |
| `keyring_generator` | Generates keys on demand and stores the keys in Vault. |
| `keyring_keys_metadata_iterator` | Iterates over key metadata for inspection. |
| `keyring_load` | Loads the keyring during server startup and reloads on demand. |
| `keyring_reader_with_status` | Reads keys and exposes the read status. |
| `keyring_writer` | Writes keys to Vault. |

The `keyring_aes` service supports server-side encryption at rest. The service also supports the AES user-defined functions (UDFs) when paired with the encryption UDF component.

## Operate the vault component

This shared section covers rotation, monitoring, and backup procedures that apply to every keyring component. The following notes describe behaviors that are specific to `keyring_vault`.

### Master key rotation

Each `ALTER INSTANCE ROTATE INNODB MASTER KEY` statement writes a new master key entry to Vault under the configured `secret_mount_point`. The previous key remains in Vault history when `secret_mount_point_version` is `2` or when the AUTO probe identifies a `kv-v2` mount. The component contacts Vault during the rotation, so a slow or unreachable Vault delays statement completion. Schedule rotation during a low-load window.

### Monitoring fields

Compare the values returned by `performance_schema.keyring_component_status` against `component_keyring_vault.cnf` to detect drift in `vault_url`, `secret_mount_point`, `vault_ca`, and `secret_mount_point_version`. Watch the server error log for `HTTP 403` (token expiration) and `HTTP 503` (sealed Vault). Configure alerts on both patterns.

### Backup and restore considerations

A Vault-backed restore requires the following on the destination host:

* Network reachability to the same Vault server, with valid name resolution and certificate trust.

* A valid token with read access to the configured `secret_mount_point`.

* A `server_uuid` distinct from the source host. A duplicated `server_uuid` triggers the data-loss case described in [Configure the keyring vault component](#configure-the-keyring-vault-component).

* `kv-v2` history retention that covers the time between backup and restore. A backup taken before a master-key rotation cannot decrypt tablespaces written after the rotation unless the post-rotation key remains in Vault history.

## See also

* [Data at Rest Encryption](data-at-rest-encryption.md) describes how Percona Server uses the keyring to protect tablespace data.

* [Get Started with component keyring](quickstart-component-keyring.md) walks through a minimal setup.

* [Keyring components overview](keyring-components-plugins-overview.md) compares the available keyring components.

--8<--- "keyring-components-verification.md"

!!! admonition "See also"

    [Hashicorp Documentation: Installing Vault :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/get-vault)

    [Hashicorp Documentation: Production Hardening :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/concepts/production-hardening)

## Related topics

* [Keyring components overview](keyring-components-plugins-overview.md)

* [Use the keyring file component](use-keyring-file.md)

* [Use the Key Management Interoperability Protocol (KMIP)](using-kmip.md)

* [Use the Amazon Key Management Service (AWS KMS)](using-amz-kms.md)

* [Data at rest encryption](data-at-rest-encryption.md)
* [Maintain the Vault connection](maintain-vault-connection.md) covers token expiration, token renewal patterns, and Vault seal handling.

* [Rotate the master encryption key](rotate-master-key.md) covers the full rotation procedure and required privileges.
