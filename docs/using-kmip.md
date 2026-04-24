# Use the Key Management Interoperability Protocol (KMIP)

Percona Server for MySQL supports the [OASIS Key Management Interoperability Protocol (KMIP) :octicons-link-external-16:](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). Percona has validated the KMIP implementation against the following servers:

* [PyKMIP server :octicons-link-external-16:](https://pykmip.readthedocs.io/en/latest/server.html)

* [HashiCorp Vault Enterprise KMIP Secrets Engine :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/secrets/kmip)

* [Thales CipherTrust Manager :octicons-link-external-16:](https://cpl.thalesgroup.com/encryption/ciphertrust-manager)

* [Fortanix Data Security Manager :octicons-link-external-16:](https://www.fortanix.com/products/data-security-manager)

KMIP enables communication between key management systems and the database server. The protocol provides the following capabilities:

* Centralized storage and lifecycle management for encryption keys

* Standardized key exchange between databases and key management systems

## Component installation

--8<--- "keyring-components-installation.md"

For more information, see [Installing and Uninstalling Components :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/component-loading.html).

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

| Option | Type | Required | Default | Description |
|---|---|---|---|---|
| `server_addr` | string | Yes | — | Hostname or IP address of the KMIP server |
| `server_port` | string | Yes | — | TCP port of the KMIP server, for example `"5696"` |
| `client_ca` | string | Yes | — | Path to the client certificate presented to the KMIP server, in Privacy-Enhanced Mail (PEM) format |
| `client_key` | string | Yes | — | Path to the client private key that matches `client_ca`, in PEM format |
| `server_ca` | string | Yes | — | Path to the certificate authority (CA) certificate that verifies the KMIP server, in PEM format |
| `object_group` | string | No | `""` | KMIP object group used to register and enumerate objects; an empty value disables grouping |
| `max_objects` | integer | No | `65535` | Maximum objects retrieved per object type in one locate operation. Applies to symmetric keys and secret data |
| `kmip_timeout_ms` | integer | No | `5000` | KMIP connection timeout in milliseconds |
| `tls_peer_verification` | boolean | No | `false` | When `true`, verifies the Transport Layer Security (TLS) certificate of the KMIP server against `server_ca` |
| `tls_hostname_verification` | boolean | No | `false` | When `true`, verifies `server_addr` against the Subject Alternative Name (SAN) or Common Name (CN) of the KMIP server certificate |

#### TLS verification

Both `tls_peer_verification` and `tls_hostname_verification` default to `false` for backward compatibility. Enable both options in production deployments. The KMIP keyring backend then rejects connections to KMIP servers that present an untrusted or mismatched certificate.

To enable peer verification, set `server_ca` to the certificate authority that signed the KMIP server certificate. To enable hostname verification, set `server_addr` to match the SAN or CN of the KMIP server certificate.

### KMIP object state requirements

The KMIP keyring backend loads only objects in the `ACTIVE` state. Loadable objects include symmetric keys and secret data. The backend ignores objects in the `PRE_ACTIVE`, `DEACTIVATED`, `COMPROMISED`, or `DESTROYED` states. The backend activates each key or secret during registration.

!!! important

    Activate any `PRE_ACTIVE` keys on the KMIP server before you start Percona Server for MySQL. Otherwise, Percona Server for MySQL cannot load those keys.

    Use the KMIP `Activate` operation through the management interface of your KMIP server. Supported interfaces include a web console, a command-line tool, or a KMIP client library. For exact steps, see the documentation for your KMIP server.

### Supported AES key sizes

The KMIP keyring backend accepts these Advanced Encryption Standard (AES) key sizes:

| AES key size | Length in bytes |
|---|---|
| 128 bits | 16 |
| 192 bits | 24 |
| 256 bits | 32 |

The KMIP keyring backend rejects AES keys of any other length. The `keyring_udf` plugin returns `ER_KEYRING_UDF_KEYRING_SERVICE_ERROR` for requests that specify a non-standard key size.

!!! important

    Review any scripts or tooling that use non-standard AES key sizes before you upgrade.

--8<--- "keyring-components-verification.md"

## Related topics

* [Keyring components overview](keyring-components-plugins-overview.md)

* [Use the keyring file component](use-keyring-file.md)

* [Use the keyring vault component](use-keyring-vault-component.md)

* [Use the Amazon Key Management Service (AWS KMS)](using-amz-kms.md)

* [Data at rest encryption](data-at-rest-encryption.md)
