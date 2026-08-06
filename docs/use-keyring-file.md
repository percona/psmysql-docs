# Use the keyring file component

The `keyring_file` component is part of the component-based MySQL infrastructure which extends the server capabilities.

!!! important

    Percona Server for MySQL {{vers}} does not support the `keyring_file` plugin.

See the MySQL documentation on the [component installation :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html) and on the [keyring_file component usage :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-file-component.html) for more information.

--8<--- "keyring-components-installation.md"

An example of a manifest and a configuration file is the following:

An example of `./bin/mysqld.my`:

```json
{
    "components": "file://component_keyring_file"
}
```

An example of `/lib/plugin/component_keyring_file.cnf`:

```json
{
    "path": "/var/lib/mysql-keyring/keyring_file", "read_only": false
}
```

--8<--- "keyring-components-verification.md"

## Related topics

* [Keyring components overview](keyring-components-plugins-overview.md)

* [Use the keyring vault component](use-keyring-vault-component.md)

* [Use the Key Management Interoperability Protocol (KMIP)](using-kmip.md)

* [Use the Amazon Key Management Service (AWS KMS)](using-amz-kms.md)

* [Data at rest encryption](data-at-rest-encryption.md)
