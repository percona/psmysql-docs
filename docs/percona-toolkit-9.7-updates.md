# Percona Toolkit updates for {{vers}}

Percona Toolkit is updated to support MySQL {{vers}}. The updates address terminology, deprecations, and authentication improvements. If your automation or runbooks use these tools, plan toolkit updates with the database upgrade.

For underlying Percona Toolkit guidance, see [Percona Toolkit Documentation :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/index.html).

## Required Percona Toolkit version

Use Percona Toolkit 3.7.0 or later when working with {{vers}}. The 3.7.0 series added support for MySQL 8.4 client libraries. Later 3.7.x releases extend the data source name (DSN) Secure Sockets Layer (SSL) options and address security advisories.

Take the following actions.

* Confirm that each deployed tool reports version 3.7.0 or higher when invoked with `--version`.

* For first-time installations, install the most recent 3.7.x release available in the Percona repositories.

* Track the [Percona Toolkit release notes :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/release_notes.html) for security and compatibility updates.

## Tools relevant to a {{vers}} upgrade

The following table maps upgrade phases to Percona Toolkit tools that support each phase.

| Phase | Tool | Purpose |
|---|---|---|
| Pre-upgrade snapshot | `pt-mysql-summary` | Capture the source server state for baseline and triage |
| Pre-upgrade snapshot | `pt-show-grants` | Export user accounts and privileges as portable SQL |
| Configuration audit | `pt-config-diff` | Compare `my.cnf` settings across source, target, and replicas |
| Query compatibility | `pt-upgrade` | Replay source logs against the {{vers}} candidate. Report row, warning, and timing differences |
| Schema preparation | `pt-online-schema-change` | Apply column or index changes online before the upgrade window |
| Replication consistency | `pt-table-checksum` | Compute consistency checksums on the source and replicas |
| Replication reconciliation | `pt-table-sync` | Reconcile rows after `pt-table-checksum` reports drift |
| Replication topology | `pt-replica-find` | Discover the topology before each rolling-upgrade step |
| Replication recovery | `pt-replica-restart` | Restart replication after recoverable errors |
| Incident response | `pt-stalk` | Collect diagnostic data on upgrade-related issues |

## Terminology alignment

Toolkit commands and output use SOURCE and REPLICA terminology, consistent with MySQL {{vers}}.

## Renamed tools

The following tools are renamed.

* `pt-slave-find` is renamed to `pt-replica-find`.

* `pt-slave-restart` is renamed to `pt-replica-restart`.

The rename landed in Percona Toolkit 3.5.0. Aliases with the original names remain for a transition period. Update scripts and runbooks to the renamed tools.

## Deprecated tool

`pt-slave-delay` is deprecated and does not support MySQL {{vers}}. Use built-in delayed replication instead.

To configure delayed replication, run the following statement against the replica.

```sql
CHANGE REPLICATION SOURCE TO SOURCE_DELAY = <SECONDS>;
```

Combine `SOURCE_DELAY` with `START REPLICA` to apply or resume the delay. The setting persists across replica restarts.

## Authentication and SSL

The following authentication and SSL updates apply to recent Percona Toolkit releases.

* SSL and Transport Layer Security (TLS) handling is improved. Tools accept SSL options through the DSN field.

* Support for the `caching_sha2_password` and `sha256_password` authentication plugins is improved.

* For {{vers}}, configure clients to use `caching_sha2_password` because the server-side `mysql_native_password` plugin is removed.

## What to change in your environment

Apply the following changes when upgrading to {{vers}}.

* Upgrade Percona Toolkit to 3.7.0 or higher before starting the database upgrade.

* Remove dependencies on `pt-slave-delay`. Replace the dependency with built-in delayed replication.

* Update automation and scripts. Replace `pt-slave-find` with `pt-replica-find`, and replace `pt-slave-restart` with `pt-replica-restart`.

* Validate toolkit connectivity using your TLS settings and supported authentication plugins.

* For each tool used in production, run `--version` and confirm the output matches the deployed release.

## Further reading

The following Percona Server for MySQL pages cover upgrade-related topics.

* [Downgrade options](./downgrade.md)

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)
