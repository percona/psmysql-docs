> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Percona Toolkit updates for 8.4

Percona Toolkit has been updated to support MySQL 8.4, addressing terminology, deprecations, and authentication improvements. If your automation or runbooks use these tools, plan updates alongside the database upgrade.

## Terminology alignment

- Toolkit commands and output now use SOURCE/REPLICA terminology consistent with MySQL 8.4.

## Renamed tools

- `pt-slave-find` → `pt-replica-find`
- `pt-slave-restart` → `pt-replica-restart`

Aliases with the old names remain for a transition period; update scripts and runbooks to the new names.

## Deprecated tool

- `pt-slave-delay` is deprecated and does not support MySQL 8.4. Use built-in delayed replication features instead.

## Authentication and SSL

- Enhanced SSL/TLS handling and improved support for `caching_sha2_password` and `sha256_password` authentication plugins.

## What to change in your environment

- Update automation and scripts: replace `pt-slave-find` with `pt-replica-find`, and `pt-slave-restart` with `pt-replica-restart`.
- Remove dependencies on `pt-slave-delay`; use native delayed replication features instead.
- Validate Toolkit connectivity using your TLS settings and modern authentication plugins.

## Further reading

- [Upgrade overview](https://docs.percona.com/percona-server/8.4/upgrade.html)
- [Upgrade checklist for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.html)
- [Upgrade procedures for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-procedures.html)
- [Upgrade strategies](https://docs.percona.com/percona-server/8.4/upgrade-strategies.html)
- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/8.4/mysql-upgrade-paths.html)
- [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html)
- [Downgrade options](https://docs.percona.com/percona-server/8.4/downgrade.html)
- [Breaking and incompatible changes in 8.4](https://docs.percona.com/percona-server/8.4/8.4-breaking-changes.html)
- [Compatibility and removed items in 8.4](https://docs.percona.com/percona-server/8.4/8.4-compatibility-and-removed-items.html)
- [Defaults and tuning guidance for 8.4](https://docs.percona.com/percona-server/8.4/8.4-defaults-and-tuning.html)
