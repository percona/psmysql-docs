---
title: Uninstall Percona Server for MySQL {{vers}} using the APT package manager
description: To uninstall Percona Server for MySQL you’ll need to remove all the installed
  packages. Removing packages with apt remove does not remove the configuration and
  data files.
slug: apt-uninstall-server
category: Install
stability: stable
technical_preview: false
tags:
- apt
- debian
- installation
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Uninstall Percona Server for MySQL {{vers}} using the APT package manager

To uninstall Percona Server for MySQL you’ll need to remove all the installed
packages. Removing packages with apt remove does not remove the
configuration and data files. Removing the packages with apt purge does remove the packages with configuration files and data files (all
the databases). Depending on your needs you can choose which command better
suits you.

1. Stop the Percona Server for MySQL service: `service mysql stop`

2. Remove the packages

    1. Remove the packages. This will leave the data files (databases, tables, logs, configuration, etc.) behind. In case you don’t need them you’ll need to remove them manually: `apt remove percona-server\`

    2. Purge the packages. This command removes all the packages and deletes all the data files (databases, tables, logs, and so on.): `apt purge percona-server\`