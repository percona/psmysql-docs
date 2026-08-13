# Keyring components overview

Percona Server supports a keyring that enables internal server components to store sensitive information securely for later retrieval.

!!! warning

    Enable only one keyring component at a time for each server instance. Enabling multiple keyring components is not supported and may result in data loss.

Percona Server supports the following keyring components:

[Get Started with component keyring](quickstart-component-keyring.md){.md-button}

[Use the keyring file component](use-keyring-file.md){.md-button}

[Use the keyring vault component](use-keyring-vault-component.md){.md-button}

[Use the Key Management Interoperability Protocol (KMIP)](using-amz-kms.md){.md-button}

[Use the Amazon Key Management Service (AWS KMS)](using-kmip.md){.md-button}
