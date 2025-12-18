---
title: Files in packages built for Percona Server for MySQL Pro
description: '| Package                      | Contains                                                                                                                                                               .'
slug: pro-files
since: '8.4'
until: null
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Files in packages built for Percona Server for MySQL Pro

--8<--- "pro-build-announcement.md"

## Files in the DEB package

| Package                      | Contains                                                                                                                                                                        |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| percona-server-server-pro    | The database server itself, the mysqld binary and associated files.  |
| percona-server-pro-common    | The files common to the server and client.                           |
| percona-server-client-pro    | The command line client.                                             |
| percona-server-test-pro      | The database test suite.                                             |
| percona-server-pro-source    | The server source.                                                   |
| percona-mysql-router-pro     | The mysql router.                                                    |
| percona-server-rocksdb-pro   | The files for rocksdb installation.                                  |
| percona-server-pro-dbg       | The debug symbols.                                                   |

## Files in the RPM package

| Package                      | Contains                                                                                                                                                                        |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| percona-server-server-pro    | The database server itself, the mysqld binary and associated files.  |
| percona-server-client-pro    | The command line client.                                             |
| percona-server-test-pro      | The database test suite.                                             |
| percona-server-rocksdb-pro   | The files for rocksdb installation.                                  |
| percona-mysql-router-pro     | The mysql router.                                                    |
| percona-server-shared-pro    | Client shared library.                                               |
| percona-server-pro-debuginfo | The debug symbols.                                                   |
| percona-server-devel-pro     | Header files needed to compile software using the client library.    |

## Next steps

[Install Percona Server for MySQL Pro](install-pro.md){.md-button}