# Use the Amazon Key Management Service (AWS KMS)

Percona Server for MySQL supports the [Amazon Key Management Service (AWS KMS)](https://aws.amazon.com/kms/). Percona Server
generates the keyring keys. Amazon Web Services (AWS) encrypts the keyring data.

The AWS KMS lets you create and manage cryptographic keys across AWS services. For more information, see the
[AWS Key Management Service Documentation](https://docs.aws.amazon.com/kms/).

To use the AWS KMS component, do the following:

* Have an AWS user account. This account has an access key and a secret key.

* Create a KMS key ID. The KMS key can then be referenced in the configuration
either by its ID, alias (the key can have any number of aliases), or ARN.

## Component installation

--8<--- "keyring-components-installation.md"

For more information, see [Installing and Uninstalling Components].

The following example is a global manifest file that does not use local
manifests:

```json
{
 "read_local_manifest": false,
 "components": "file://component_keyring_kms"
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
 "components": "file://component_keyring_kms"
}
```

The configuration settings are either in a global configuration file or a local
configuration file. The settings are the same.

The KMS configuration file has the following options:

* read_local_config

* path - the location of the JSON keyring database file.

* read_only - if true, the keyring cannot be modified.

* kms_key - the identifier of an AWS KMS master key. The user must create this key before creating the manifest file. The identifier can be one of the
following:

    * UUID

    * Alias

    * ARN

For more information, see [Finding the key ID and key ARN](https://docs.aws.amazon.com/kms/latest/developerguide/find-cmk-id-arn.html).

* region - the AWS where the KMS is stored. Any HTTP request connect to this region.

* auth_key - an AWS user authentication key. The user must have access to the KMS key.

* secret_access_key - the secret key (API “password”) for the AWS user.

!!! note

    The configuration file contains authentication information. Only the MySQL process should be able to read this file.

??? example "Example of a configuration file in JSON format"

     ```json
     {
      "read_local_config": "true/false",
      "path": "/usr/local/mysql/keyring-mysql/aws-keyring-data",
      "region": "eu-central-1",
      "kms_key": "UUID, alias or ARN as displayed by the KMS console",
      "auth_key": "AWS user key",
      "secret_access_key": "AWS user secret key"
     }
     ```

For more information, see [Keyring Component installation].

[Installing and Uninstalling Components]: https://dev.mysql.com/doc/refman/{{vers}}/en/component-loading.html
[Keyring Component installation]: https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html
