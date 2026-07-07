# Use the Amazon Key Management Service (AWS KMS)

Percona Server for MySQL supports the [Amazon Key Management Service (AWS KMS) :octicons-link-external-16:](https://aws.amazon.com/kms/). Percona Server generates the keyring keys. Amazon Web Services (AWS) encrypts the keyring data.

The AWS KMS lets you create and manage cryptographic keys across AWS services. For more information, see the [AWS Key Management Service Documentation :octicons-link-external-16:](https://docs.aws.amazon.com/kms/).

## Prerequisites

Complete the following before you install the AWS KMS component:

* Create an AWS user with an access key and a secret key.

* Create a KMS key. Reference the key by its identifier, alias, or Amazon Resource Name (ARN). Each key can have any number of aliases.

--8<--- "keyring-components-installation.md"

For more information, see [Installing and uninstalling components :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/component-loading.html).

## Configuration settings

The configuration settings live in either a global configuration file or a local configuration file.

### Configuration parameters

The `component_keyring_kms.cnf` file contains the following parameters:

* `read_local_config [optional]` — declares whether the component reads the local configuration file. Use this parameter only in the global configuration file. The allowed values are `true` or `false`.

* `path` — the path to the keyring file on the local host. The file uses JSON format.

* `read_only [optional]` — when `true`, the component prevents runtime changes to the keyring. The default value is `false`.

* `kms_key` — the identifier of an AWS KMS master key. Create the key before you create the manifest file. The identifier accepts one of the following formats:

    * Universally Unique Identifier (UUID)

    * Alias

    * Amazon Resource Name (ARN)

    For more information, see [Finding the key ID and key ARN :octicons-link-external-16:](https://docs.aws.amazon.com/kms/latest/developerguide/find-cmk-id-arn.html).

* `region` — the AWS region that hosts the KMS key. Each Hypertext Transfer Protocol (HTTP) request connects to this region.

* `auth_key` — the access key for the AWS user. The user must have permission to access the KMS key.

* `secret_access_key` — the secret key for the AWS user.

!!! warning

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

--8<--- "keyring-components-verification.md"

## Related topics

* [Keyring components overview](keyring-components-plugins-overview.md)

* [Use the keyring file component](use-keyring-file.md)

* [Use the keyring vault component](use-keyring-vault-component.md)

* [Use the Key Management Interoperability Protocol (KMIP)](using-kmip.md)

* [Data at rest encryption](data-at-rest-encryption.md)
For more information, see [Keyring component installation :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html).
