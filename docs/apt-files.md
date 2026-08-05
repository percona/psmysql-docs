# DEB repository package list - Percona Server for MySQL {{vers}}

In Percona Server for MySQL 9.7.1-1 only, APT packaging was reorganized to align more closely with upstream MySQL. Several packages were split into separate components, which may affect upgrades and dependency resolution. The table below lists packages for earlier releases; see the [9.7.1-1 release notes](release-notes/9.7.1-1.md) for the updated package list.

| Package Name | Description |
|---------------|-------------|
| libperconaserverclient22 | The shared client library used by Percona Server and MySQL client programs. Applications that connect to MySQL servers dynamically link to this library. |
| libperconaserverclient22-dev | Development headers and static libraries for building software that links against libperconaserverclient22. Needed when compiling client applications using the MySQL C API. |
| percona-mysql-router | A lightweight middleware that routes connections between applications and backend MySQL or Percona Server instances. Used in high availability and cluster setups. |
| percona-server-client | The command-line client utilities, including mysql, mysqldump, and related tools for interacting with a Percona Server instance. |
| percona-server-common | Common configuration files, character sets, and data shared among multiple Percona Server packages. Installed automatically as a dependency. |
| percona-server-dbg | Debug symbols for the Percona Server binaries. Useful for developers or support teams when diagnosing crashes or profiling performance. |
| percona-server-rocksdb | The RocksDB storage engine plugin for Percona Server, providing high-performance key-value storage optimized for fast writes. |
| percona-server-server | The main Percona Server daemon (mysqld) and supporting files. This is the actual database server that runs and manages data. |
| percona-server-source | The source code package for Percona Server, often used for auditing, compliance, or custom builds. |
| percona-server-test | A suite of functional and regression tests used to verify server correctness and compatibility. Useful for QA or CI environments. |
| percona-telemetry-agent | A lightweight agent that collects anonymous usage and performance data to help Percona improve the product. Optional; can be disabled if desired. |