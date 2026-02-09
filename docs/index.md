# Percona Server for MySQL {{vers}} - Documentation

!!! note ""

    This documentation is for the latest release: Percona Server for MySQL {{release}} ([Release Notes](release-notes/{{release}}.md)).

Percona Server for MySQL is a freely available, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior and optimized performance, greater scalability and availability, enhanced backups, and increased visibility and instrumentation.

Thousands of enterprises trust Percona Server for MySQL to provide better performance and concurrency for their most demanding workloads.

## ![Percona](_static/percona-favicon.ico) New to Percona?

Start here to choose your installation path.

1. Are you building a High Availability (HA) Cluster?
   * Yes → Use Percona Distribution for MySQL. For a multi-node HA cluster, Percona XtraDB Cluster (PXC) is the clustered database; PDPS includes the server or PXC plus tested versions of HAProxy, ProxySQL, Orchestrator, and XtraBackup.
   * No → Go to step 2.

2. Do you just need a drop-in replacement for MySQL?
   * Yes → Use Percona Server for MySQL. It is lightweight and focuses on the core engine performance.

3. Is your operating system (OS) very new?
   * Check → Verify support on the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) page.

4. Are you deploying on Kubernetes (a platform for running containerized applications)?
   * Yes → Use [Percona Operator for MySQL](https://docs.percona.com/percona-operator-for-mysql/ps/) (for Percona Server for MySQL) or [Percona Operator for MySQL based on Percona XtraDB Cluster (PXC)](https://docs.percona.com/percona-operator-for-mysql/pxc/) (for a clustered, high-availability setup). Operators automate deployment, scaling, backups, and failover on Kubernetes.
   * No → Not sure? [Learn more about the differences](ps-or-pdps.md) to compare options.

[Learn more about the differences →](ps-or-pdps.md)

## For Monitoring and Management

Percona Monitoring and Management (PMM) monitors and provides actionable performance data for MySQL variants, including Percona Server for MySQL, Percona XtraDB Cluster, Oracle MySQL Community Edition, Oracle MySQL Enterprise Edition, and MariaDB. PMM captures metrics and data for the InnoDB, XtraDB, and MyRocks storage engines, and has specialized dashboards for specific engine details.

[Get started with PMM :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html).

--8<--- "get-help-snip.md"

<div data-grid markdown><div data-banner markdown>

## :material-progress-download: Quickstart guide { .title }

Get started quickly with our Quickstart guide.

[Quickstart guide](quickstart-overview.md){ .md-button }

</div><div data-banner markdown>

### :material-progress-download: Installation guides { .title }

Find the best installation solution with our step-by-step installation instructions.

[Installation instructions](installation.md){ .md-button }

</div><div data-banner markdown>

### :material-arrow-up: Upgrade instructions { .title }

Upgrade your Percona Server for MySQL installation with our comprehensive upgrade guides.

[Upgrade instructions](upgrade.md){ .md-button }

</div><div data-banner markdown>

### :material-information-outline: Planning for MySQL 9.7 LTS? { .title }

Evaluate or plan a move to Percona Server for MySQL 9.7 LTS (for example, from APT, DNF, or YUM packages).

See [What's New in MySQL 9.7: Technical Migration Overview](whats-new-mysql-9.md) for breaking changes, compatibility, removed items, and defaults and tuning.

</div><div data-banner markdown>

## :fontawesome-solid-gears: Audit Log Filter component { .title }

Learn about the Audit Log Filter component that allows you to monitor, log, and block a connection or query actively executed on the selected server.

[Audit Log Filter](audit-log-filter-overview.md){ .md-button}

</div>
</div>
