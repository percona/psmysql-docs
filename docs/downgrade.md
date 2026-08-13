# Downgrade Percona Server for MySQL

**Topic type**: Concept

--8<--- "get-help-snip.md"

[Need help planning a downgrade? Percona Support can assist :octicons-link-external-16:](https://www.percona.com/services/expert-support/).

## Before you downgrade

Review the following prerequisites before starting a downgrade:

* Understand the Percona Server for MySQL release model. Percona ships Long-Term Support (LTS) releases and bug-fix releases within each LTS series.

* Treat hot fixes as separate releases when you plan a downgrade.

* For a replication topology, perform a rolling downgrade. Apply a single-server method to each server in turn.

* Take a verified backup before any downgrade attempt.

* Do not attempt to downgrade below 8.4. Earlier paths are not supported.

For the underlying MySQL guidance, see [Downgrading MySQL :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/downgrading.html).

## Identify a supported downgrade path

The following table summarizes supported downgrade paths from {{vers}} LTS.

| Downgrade path | Example | Supported methods | Notes |
|---|---|---|---|
| Within the same LTS series | {{vers}}.y LTS to {{vers}}.x LTS | In-place, logical dump and load, MySQL Clone, or replication | Same-LTS downgrades have the most flexibility. |
| To the previous LTS series | {{vers}}.x LTS to 8.4.y | Logical dump and load, or replication | Use this path as a rollback only. The data must contain no features from the upgraded version. |

!!! important "Rollback constraint"

    Cross-series paths fit a rollback scenario only. If you have run any feature unique to {{vers}} against the data, do not use a cross-series downgrade. Restore from a pre-upgrade backup instead.

## Choose a downgrade method

The following methods support the paths in [Identify a supported downgrade path](#identify-a-supported-downgrade-path):

* In-place: stop the server, replace binaries, and restart with the existing data directory. Available within the same LTS series only.

* Logical dump and load: export the data with `mysqldump` and load the dump into the older version.

* MySQL Clone: clone data between servers within the same LTS series.

* Replication: configure replication from {{vers}} to the older version, validate the replica, and cut traffic over.

For cutover and validation guidance during a downgrade, see [Upgrade strategies](./upgrade-strategies.md).

## Assess downgrade risks

!!! warning "Data loss risk"

    A failed downgrade can corrupt or destroy data. Create and verify a backup before any downgrade attempt. Restore the backup if the downgrade encounters issues.

The following table lists the risks of downgrading.

| Risk | Description |
|---|---|
| Data loss | Data loss is possible if the downgrade encounters issues. Create a backup of your data before attempting a downgrade. |
| Incompatibility | Features used in the upgraded version can cause incompatibility. |
| Performance | Downgrading can reduce performance. |
| Security | Older versions lack security updates available in upgraded versions, which can increase exposure. |

## Further reading

The following Percona Server for MySQL pages cover related topics:

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)
