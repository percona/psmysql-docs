# Choose Between Percona Server for MySQL and Percona Distribution for MySQL

When setting up Percona repositories, you must choose between two primary paths: Percona Server for MySQL or Percona Distribution for MySQL. While they share the same core database engine, they are designed for different operational scopes.

To read more about Percona Distribution for MySQL, see the [Percona Distribution for MySQL 8.4 :octicons-link-external-16:](https://docs.percona.com/percona-distribution-for-mysql/8.4/) documentation.

## Check Platform Support

Before choosing a repository, verify that your operating system version is supported for that specific product.

Review the [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-support-lifecycle#mysql) page to confirm support for your platform and version.

## Comparison Overview

| Feature | Percona Server for MySQL (`ps-8.4`) | Percona Distribution for MySQL (`pdps-8.4`) |
| --- | --- | --- |
| Primary Goal | A performance-enhanced, drop-in replacement for MySQL Community Edition. | A curated collection of components tested together as a complete enterprise stack. |
| Included Components | Database server, client, and essential plugins. | Database server, Percona XtraBackup, HAProxy, ProxySQL, and Orchestrator. |
| Release Cycle | Follows the MySQL Community release cadence. | Follows a coordinated release cycle where all bundled components are validated for inter-compatibility. |
| Ideal For | Standalone instances or simple primary/replica setups. | High Availability (HA) clusters and mission-critical enterprise environments. |

## Which one should I install?

### Percona Server for MySQL (`ps-8.4`)

Choose this if any of the following conditions apply:

* Wanting a minimal footprint focused solely on the database engine.

* Managing your own infrastructure components (backups, proxies, or orchestration) independently.

* Requiring the latest performance patches and features available in Percona Server but not needing a bundled ecosystem.

### Percona Distribution for MySQL (`pdps-8.4`)

Choose this if any of the following conditions apply:

* Deploying a High Availability (HA) environment (e.g., using Percona XtraDB Cluster).

* Wanting Percona to guarantee that the specific versions of the server, proxy, and backup tools provided are fully compatible and tested as a single unit.

* Preferring a single repository entry-point that provides all the tools required for a full production lifecycle (Server + Backups + Management).

## Installation

For information on installing your choice, review the following:

* [Install Percona Server for MySQL 8.4](installation.md)

* [Install Percona Distribution for MySQL 8.4 :octicons-link-external-16:](https://docs.percona.com/percona-distribution-for-mysql/8.4/installing.html)
