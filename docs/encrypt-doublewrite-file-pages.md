---
title: Encrypt doublewrite file pages
description: InnoDB encrypts doublewrite file pages associated with encrypted tablespaces
  automatically. Doublewrite files can contain the following page types:.
slug: encrypt-doublewrite-file-pages
category: Secure
stability: stable
technical_preview: false
tags:
- encryption
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Encrypt doublewrite file pages

InnoDB encrypts doublewrite file pages associated with encrypted tablespaces automatically. Doublewrite files can contain the following page types:

* Unencrypted
* Uncompressed
* Encrypted
* Compressed