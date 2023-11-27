# Keyring components and plugins overview

Percona Server supports a keyring that enables internal server components and plugins to store sensitive information securely for later retrieval.

!!! warning

    Enable only one keyring plugin or one keyring component at a time for each server instance. Enabling multiple keyring plugins or keyring components or mixing keyring plugins or keyring components is not supported and may result in data loss.

Percona Server supports the following keyring components and plugins:

[Use the keyring file component or plugin :material-arrow-right:](use-keyring-file.md){.md-button}

[Use the keyring vault component :material-arrow-right:](use-keyring-vault-component.md){.md-button}

[Use the Key Management Interoperability Protocol (KMIP) :material-arrow-right:](using-amz-kms.md){.md-button}

[Use the Amazon Key Management Service (AWS KMS) :material-arrow-right:](using-kmip.md){.md-button}
