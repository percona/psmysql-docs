# Percona Toolkit updates for {{vers}}

Percona Toolkit has been updated to support MySQL {{vers}}, addressing terminology, deprecations, and authentication improvements. If your automation or runbooks use these tools, plan updates alongside the database upgrade.

## Terminology alignment

* Toolkit commands and output now use SOURCE/REPLICA terminology consistent with MySQL {{vers}}.

## Renamed tools

* `pt-slave-find` → `pt-replica-find`
* `pt-slave-restart` → `pt-replica-restart`

Aliases with the old names remain for a transition period; update scripts and runbooks to the new names.

## Deprecated tool

* `pt-slave-delay` is deprecated and does not support MySQL {{vers}}. Use built-in delayed replication features instead.

## Authentication and SSL

* Enhanced SSL/TLS handling and improved support for `caching_sha2_password` and `sha256_password` authentication plugins.

## What to change in your environment

* Update automation and scripts: replace `pt-slave-find` with `pt-replica-find`, and `pt-slave-restart` with `pt-replica-restart`.
* Remove dependencies on `pt-slave-delay`; use native delayed replication features instead.
* Validate Toolkit connectivity using your TLS settings and modern authentication plugins.

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Downgrade options](./downgrade.md)

