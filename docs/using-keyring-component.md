# Use the keyring_vault component

The keyring_vault component is a keyring component that communicates with **HashiCorp Vault** for back end storage. It enables MySQL server components and plugins to securely store sensitive information such as encryption keys. To use it, you need to install the component, configure the Vault server, and set the required system variables. 

Some of the advantages of using the keyring_vault component are:

- It provides a centralized and secure way to manage keys across multiple MySQL servers.
- It supports key rotation and migration without downtime or data loss.
- It integrates with Vault's authentication and authorization mechanisms, such as AppRole.

Some of the disadvantages of using the keyring_vault component are:

- It requires an additional dependency on the Vault server, which may introduce network latency or availability issues.
- It may not be compatible with some MySQL features that rely on local keyring storage, such as binary log encryption or clone plugin.

## Use the keyring_file component

The `keyring_file`` component stores encryption keys in a file on the server host. Use the component to enable encryption features such as tablespace encryption, redo log encryption, and binary log encryption.

Some advantages of using the keyring_file component are:

- Easy to set up and use

- Supports secure storage for persisted system variable values

Some disadvantages of using the keyring_file component are:

- Cannot be used as a regulatory compliance solution. Security standards such as PCI and FIPS require using key management systems to secure, manage, and protect encryption keys in key vaults or hardware security modules (HSMs)

- Does not protect the keyring file from unauthorized access or tampering

- Compromising the keyring file allows the decryption of encrypted data by an attacker

- Does not support multiple server instances using different keyring files. You must use a local configuration file for each instance.

To use this component, you need to install and configure the component using a manifest file and a configuration file. See [keyring component installation](https://dev.mysql.com/doc/refman/8.0/en/keyring-component-installation.html) for information.
