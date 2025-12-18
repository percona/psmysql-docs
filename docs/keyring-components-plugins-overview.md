---
title: Keyring components overview
description: Percona Server supports a keyring that enables internal server components
  to store sensitive information securely for later retrieval.
slug: keyring-components-plugins-overview
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Keyring components overview

Percona Server supports a keyring that enables internal server components to store sensitive information securely for later retrieval.

!!! warning

    Enable only one keyring component at a time for each server instance. Enabling multiple keyring components is not supported and may result in data loss.

Percona Server supports the following keyring components:

[Use the keyring file component](use-keyring-file.md){.md-button}

[Use the keyring vault component](use-keyring-vault-component.md){.md-button}

[Use the Key Management Interoperability Protocol (KMIP)](using-amz-kms.md){.md-button}

[Use the Amazon Key Management Service (AWS KMS)](using-kmip.md){.md-button}