# Use the Key Management Interoperability Protocol (KMIP)

Percona Server for MySQL supports the [OASIS Key Management Interoperability Protocol (KMIP)](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). This implementation was tested with the [PyKMIP server](https://pykmip.readthedocs.io/en/latest/server.html) and the [HashiCorp Vault Enterprise KMIP Secrets Engine](https://www.vaultproject.io/docs/secrets/kmip).

KMIP enables communication between key management systems and the database server. The protocol can do the following:

* Streamline encryption key management

* Eliminate redundant key management processes

## Component installation

--8<--- "keyring-components-installation.md"

For more information, see [Installing and Uninstalling Components].

The following is an example of a global manifest file that does not use local manifests:

```json
{
 "read_local_manifest": false,
 "components": "file://component_keyring_kmip"
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
 "components": "file://component_keyring_kmip"
}
```

The configuration settings are either in a global configuration file or a local configuration file. The settings are the same. 

??? example "Example of a configuration file in JSON format"

     ```json
     {
      "server_addr": "127.0.0.1",
      "server_port": "5696",
      "client_ca": "client_certificate.pem",
      "client_key": "client_key.pem",
      "server_ca": "root_certificate.pem"
     }
     ```

For more information, see [Keyring Component installation].

[Installing and Uninstalling Components]: https://dev.mysql.com/doc/refman/{{vers}}/en/component-loading.html
[Keyring Component installation]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html
