# DEB repository package list - Percona Server for MySQL {{vers}}

| Package Name | Description |
|---------------|-------------|
| libperconaserverclient24 | The shared client library used by Percona Server and MySQL client programs. Applications that connect to MySQL servers dynamically link to this library.|
| libperconaserverclient24-dev | Development headers and static libraries for building software that links against libperconaserverclient24. Needed when compiling client applications using the MySQL C API. |
| percona-client | Transitional metapackage that depends on percona-server-client, kept for compatibility with scripts and dependency chains that reference the older package name. |
| percona-mysql-router | A lightweight middleware that routes connections between applications and backend MySQL or Percona Server instances. Used in high availability and cluster setups. |
| percona-server | Metapackage that depends on percona-server-server, provided for compatibility with earlier installation instructions and dependency chains. |
| percona-server-client-core | The core client-side binaries and libraries required to connect to a Percona Server instance.|
| percona-server-client-plugins | Client-side authentication and connection plugins (for example, caching_sha2_password support) used by the client utilities.|
| percona-server-client | The command-line client utilities, including mysql, mysqldump, and related tools for interacting with a Percona Server instance. Depends on percona-server-client-core and percona-server-client-plugins. |
| percona-server-common | Common configuration files, character sets, and data shared among multiple Percona Server packages. Installed automatically as a dependency. |
| percona-server-js | Support for server-side JavaScript stored programs in Percona Server. |
| percona-server-rocksdb | The RocksDB storage engine plugin for Percona Server, providing high-performance key-value storage optimized for fast writes. |
| percona-server-server-core | The core Percona Server daemon (mysqld) binaries required to run the database server.|
| percona-server-server | The main Percona Server daemon and supporting files, including systemd service configuration. Now depends on percona-server-server-core. |
| percona-server-source | The source code package for Percona Server, often used for auditing, compliance, or custom builds. |
| percona-server-test | A suite of functional and regression tests used to verify server correctness and compatibility. Useful for QA or CI environments. |
| percona-telemetry-agent | A lightweight agent that collects anonymous usage and performance data to help Percona improve the product. Installed as a mandatory dependency of Percona Server packages; can be disabled after installation. |
| percona-testsuite | Metapackage that depends on percona-server-test, provided for compatibility with earlier installation instructions and dependency chains. |
