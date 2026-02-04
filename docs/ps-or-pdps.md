# Choose your path: Percona Server for MySQL, Percona Distribution for MySQL, or Percona Operators

When setting up Percona repositories (online locations where installable software packages are stored), you must choose between two primary paths: Percona Server for MySQL (PS) or Percona Distribution for MySQL (PDPS). Both ship the same Percona Server for MySQL 8.4 database server; PDPS adds a curated set of surrounding components (backup, proxy, orchestration) tested together. They are designed for different operational scopes.

The labels `ps-8.4` and `pdps-8.4` are repository identifiers (short names for the repository you enable). You use them when enabling the Percona repository—for example, with the `percona-release` setup tool or in the configuration for your system’s package manager (the tool that installs software: apt on Debian/Ubuntu, yum or dnf on Red Hat–style systems). The number (8.4) matches the MySQL major version.

To read more about Percona Distribution for MySQL, see the [Percona Distribution for MySQL 8.4 :octicons-link-external-16:](https://docs.percona.com/percona-distribution-for-mysql/8.4/) documentation.

## Check Platform Support

Before choosing a repository, verify that your operating system (OS) version is supported for that specific product. Review the [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) page to confirm support for your platform and version. If your OS is not listed (for example, a very new Linux distribution such as a recently released Ubuntu or Debian), use a supported platform or wait until support is added.

## Comparison Overview

| Feature | Percona Server for MySQL (`ps-8.4`) | Percona Distribution for MySQL (`pdps-8.4`) | Percona Operators |
| --- | --- | --- | --- |
| Primary Goal | A performance-enhanced, drop-in replacement for MySQL Community Edition. | A curated collection of components tested together as a complete enterprise stack. | Kubernetes-native deployment and lifecycle management for Percona Server for MySQL or Percona XtraDB Cluster (PXC). |
| Included Components | Database server, client, and essential plugins. | Database server, Percona XtraBackup (backup), HAProxy and ProxySQL (traffic and query routing), and Orchestrator (replication management). | Operator plus database pods; backup, proxy, and orchestration vary by Operator (PS or PXC). |
| Release Cycle | Follows the MySQL Community release cadence. | Follows a coordinated release cycle where all bundled components are validated for inter-compatibility. | Follows Operator release cadence; deploys supported PS or PXC versions. |
| Ideal For | Standalone instances or simple primary/replica setups (one server accepts writes; others hold read-only copies). | High Availability (HA) clusters—systems that keep running even if one server or component fails—and mission-critical enterprise environments. | Kubernetes and cloud-native environments; automated failover, scaling, and backups. |

[Percona XtraDB Cluster (PXC) :octicons-link-external-16:](https://docs.percona.com/percona-xtradb-cluster/) is a high-availability clustered database based on MySQL; multiple nodes stay in sync so the cluster keeps running if one node fails. It is a different product from Percona Server for MySQL (which is a single-server database).

## Which one should I install?

Need High Availability (HA) or a single supported stack (server, proxy, backup)? Choose Percona Distribution for MySQL (PDPS). Deploying on Kubernetes? See Percona Operators below. Otherwise, choose Percona Server for MySQL (PS).

### Percona Server for MySQL (`ps-8.4`)

Choose this if any of the following conditions apply:

* Wanting a minimal footprint focused solely on the database engine.

* Managing your own infrastructure components (backups, proxies, or orchestration) independently.

* Requiring the latest performance patches and features available in Percona Server but not needing a bundled ecosystem.

### Percona Distribution for MySQL (`pdps-8.4`)

Choose this if any of the following conditions apply:

* Deploying a High Availability (HA) environment (for example, using Percona XtraDB Cluster).

* Wanting a curated, version-aligned stack where the server, proxy, and backup tools are validated for compatibility as a single unit.

* Preferring a single repository entry-point that provides all the tools required for a full production lifecycle (Server + Backups + Management).

If you need only some components (for example, XtraBackup or ProxySQL) with Percona Server for MySQL, you can install those separately; PDPS is for users who want one supported, integrated stack.

## Deploying on Kubernetes?

If you run your workloads on Kubernetes (a platform for running containerized applications), use Percona Operators instead of the repository-based installation. Operators automate deployment, scaling, backups, and failover on Kubernetes.

* [Percona Operator for MySQL :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-mysql/ps/) — for Percona Server for MySQL
* [Percona Operator for MySQL based on Percona XtraDB Cluster (PXC) :octicons-link-external-16:](https://docs.percona.com/percona-operator-for-mysql/pxc/) — for a clustered, high-availability setup

## Next steps

Percona Server for MySQL

* [Quickstart guide](quickstart-overview.md)

* [Install Percona Server for MySQL 8.4](installation.md)

Percona Distribution for MySQL

* [Percona Distribution for MySQL 8.4 documentation :octicons-link-external-16:](https://docs.percona.com/percona-distribution-for-mysql/8.4/)
* [Install Percona Distribution for MySQL 8.4 :octicons-link-external-16:](https://docs.percona.com/percona-distribution-for-mysql/8.4/installing.html)
