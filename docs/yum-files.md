---
title: Yum repository package list - Percona Server for MySQL {{vers}}
description: '| Package Name | Description | |---------------|-------------| | percona-icu-data-files
  | Provides ICU (International Components for Unicode) data files required by Percona
  Server for locale, collatio.'
slug: yum-files
category: Install
stability: stable
technical_preview: false
tags:
- centos
- percona-server
- rhel
- yum
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Yum repository package list - Percona Server for MySQL {{vers}}


| Package Name | Description |
|---------------|-------------|
| percona-icu-data-files | Provides ICU (International Components for Unicode) data files required by Percona Server for locale, collation, and Unicode character set support. |
| percona-mysql-router | A lightweight routing middleware that directs client connections to backend MySQL or Percona Server instances, often used in high availability setups. |
| percona-mysql-router-debuginfo | Debug symbols for `percona-mysql-router`, used for troubleshooting or analyzing router crashes and performance issues. |
| percona-server-client | Command-line client utilities for connecting to and managing MySQL/Percona Server instances, including tools like `mysql` and `mysqldump`. |
| percona-server-client-debuginfo | Debug symbols for the client utilities, useful for diagnosing crashes or debugging client-related issues. |
| percona-server-debuginfo | Debug symbols for the main Percona Server binaries, required when debugging or profiling the server process. |
| percona-server-debugsource | Source code corresponding to the debug build of Percona Server, used for in-depth debugging and code-level analysis. |
| percona-server-devel | Development files and headers for building applications that link against Percona Server client libraries. |
| percona-server-rocksdb | The RocksDB storage engine plugin, providing high-performance key-value storage optimized for write-heavy workloads. |
| percona-server-rocksdb-debuginfo | Debug symbols for the RocksDB plugin, useful for diagnosing issues or profiling RocksDB engine performance. |
| percona-server-server | The main Percona Server daemon (`mysqld`) and associated server-side components for database management and operations. |
| percona-server-server-debuginfo | Debug symbols for the Percona Server daemon, enabling developers to trace or debug server-level issues. |
| percona-server-shared | Shared libraries used by both the Percona Server and client utilities, providing common functionality and APIs. |
| percona-server-shared-debuginfo | Debug symbols for the shared libraries, useful for debugging applications that depend on these libraries. |
| percona-server-test | A collection of tests used to verify the correctness and stability of Percona Server, typically used in QA or CI environments. |
| percona-server-test-debuginfo | Debug symbols for the test suite, aiding developers in diagnosing issues encountered during test runs. |
| percona-telemetry-agent | A lightweight agent that collects anonymous usage and performance data to help Percona improve its products. Optional and can be disabled. |