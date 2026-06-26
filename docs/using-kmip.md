# Use the Key Management Interoperability Protocol (KMIP)

Percona Server for MySQL supports the [OASIS Key Management Interoperability Protocol (KMIP) :octicons-link-external-16:](https://docs.oasis-open.org/kmip/kmip-spec/v2.0/os/kmip-spec-v2.0-os.html). This implementation was tested with:
- [PyKMIP server :octicons-link-external-16:](https://pykmip.readthedocs.io/en/latest/server.html)
- [HashiCorp Vault Enterprise KMIP Secrets Engine :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/secrets/kmip)
- [Thales CipherTrust Manager :octicons-link-external-16:](https://cpl.thalesgroup.com/encryption/ciphertrust-manager)
- [Fortanix Data Security Manager :octicons-link-external-16:](https://www.fortanix.com/products/data-security-manager)

KMIP enables communication between key management systems and the database server. The protocol can do the following:

* Streamline encryption key management

* Eliminate redundant key management processes

## Component installation

--8<--- "keyring-components-installation.md"

For more information, see [Installing and Uninstalling Components :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/component-loading.html).

--8<--- "keyring-manifest-examples.md:57:82" 

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

For more information, see [Keyring Component installation :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html).
