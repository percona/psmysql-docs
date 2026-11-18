> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Percona Server for MySQL 8.4 - Documentation

This documentation is for the latest release: Percona Server for MySQL 8.4.11-12 ([Release Notes](https://docs.percona.com/percona-server/8.4/release-notes/8.4.11-12.html)).

Percona Server for MySQL is a freely available, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior and optimized performance, greater scalability and availability, enhanced backups, and increased visibility and instrumentation.

Thousands of enterprises trust Percona Server for MySQL to provide better performance and concurrency for their most demanding workloads.

## New to Percona?

Start here to choose your installation path.

1. Are you building a High Availability (HA) Cluster?

   - Yes → Use Percona Distribution for MySQL. For a multi-node HA cluster, Percona XtraDB Cluster (PXC) is the clustered database; PDPS includes the server or PXC plus tested versions of HAProxy, ProxySQL, Orchestrator, and XtraBackup.
   - No → Go to step 2.

1. Do you just need a drop-in replacement for MySQL?

   - Yes → Use Percona Server for MySQL. It is lightweight and focuses on the core engine performance.

1. Is your operating system (OS) very new?

   - Check → Verify support on the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) page.

1. Are you deploying on Kubernetes (a platform for running containerized applications)?

   - Yes → Use [Percona Operator for MySQL](https://docs.percona.com/percona-operator-for-mysql/ps/) (for Percona Server for MySQL) or [Percona Operator for MySQL based on Percona XtraDB Cluster (PXC)](https://docs.percona.com/percona-operator-for-mysql/pxc/) (for a clustered, high-availability setup). Operators automate deployment, scaling, backups, and failover on Kubernetes.
   - No → Not sure? [Learn more about the differences](https://docs.percona.com/percona-server/8.4/ps-or-pdps.html) to compare options.

[Learn more about the differences →](https://docs.percona.com/percona-server/8.4/ps-or-pdps.html)

## For Monitoring and Management

Percona Monitoring and Management (PMM) monitors and provides actionable performance data for MySQL variants, including Percona Server for MySQL, Percona XtraDB Cluster, Oracle MySQL Community Edition, Oracle MySQL Enterprise Edition, and MariaDB. PMM captures metrics and data for the InnoDB, XtraDB, and MyRocks storage engines, and has specialized dashboards for specific engine details.

[Get started with PMM](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html) .

Review [Get help from Percona](https://docs.percona.com/percona-server/8.4/get-help.html) for ways that we can work with you.

## Quickstart guide

Get started quickly with our Quickstart guide.

[Quickstart guide](https://docs.percona.com/percona-server/8.4/quickstart-overview.html)

### Installation guides

Find the best installation solution with our step-by-step installation instructions.

[Installation instructions](https://docs.percona.com/percona-server/8.4/installation.html)

### Upgrade instructions

Upgrade your Percona Server for MySQL installation with our comprehensive upgrade guides.

[Upgrade instructions](https://docs.percona.com/percona-server/8.4/upgrade.html)

## Audit Log Filter component

Learn about the Audit Log Filter component that allows you to monitor, log, and block a connection or query actively executed on the selected server.

[Audit Log Filter](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.html)
