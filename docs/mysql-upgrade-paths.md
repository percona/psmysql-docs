# MySQL upgrade paths and supported methods

Percona Server for MySQL follows the upstream MySQL Long-Term Support (LTS) release cadence. Choose a supported upgrade path based on the source version, the target version, and the release model in use.

## Before you choose a path

Confirm the following before you select a path or method:

* Review the upstream [MySQL release model](https://dev.mysql.com/doc/refman/9.7/en/mysql-releases.html). LTS versions receive eight or more years of support and target production use. Percona Server for MySQL ships LTS releases only.

* Take a verified physical backup with `xtrabackup` from Percona XtraBackup or a logical backup with `mysqldump`. Capture the `mysql` system database, the data directory, and the server configuration. The backup is the supported rollback path across an LTS boundary.

* Run the [Upgrade Checker Utility](https://dev.mysql.com/doc/mysql-shell/9.7/en/mysql-shell-utilities-upgrade.html) in MySQL Shell. The `util.checkForServerUpgrade()` function reports incompatibilities you must fix before you upgrade.

* Test query compatibility with `pt-upgrade` from Percona Toolkit. The tool replays a query workload against the source and the target server and reports behavioral differences.

* Audit Percona-specific components before the upgrade. Verify a {{vers}}-compatible build exists for the audit log, data masking, keyring, and custom Structured Query Language (SQL) plugins.

* Plan a maintenance window or a rolling upgrade that matches the method you select.

!!! important "Plan for rollback"
    A downgrade across an LTS boundary is not supported. Restore the pre-upgrade backup if you must roll back. Verify the backup is restorable before you start. For supported in-series downgrades, refer to [Downgrade options](./downgrade.md).

## Identify a supported upgrade path

The following table lists the supported paths from common source versions to {{vers}}. Bug-fix releases and hot fixes within an LTS series count as individual releases.

| Upgrade path | Path examples | Supported methods |
| --- | --- | --- |
| Upgrade within an LTS series | {{vers}}.0 to {{vers}}.x | In-place, logical dump and load, replication, MySQL Clone |
| Upgrade from one LTS series to the next LTS series | 8.4.x LTS to {{vers}} LTS | In-place, logical dump and load, replication |
| Migrate from upstream MySQL Innovation to a Percona Server LTS series | 9.x Innovation to {{vers}} LTS | In-place, logical dump and load, replication |
| Upgrade from MySQL 5.7 to a later LTS release | 5.7.x to 8.0.x to 8.4.x to {{vers}} | In-place, logical dump and load, replication |

## Confirm path-specific constraints

The following constraints affect path selection:

* LTS series cannot be skipped. To upgrade from MySQL 5.7 to {{vers}}, upgrade to 8.0, then 8.4, then {{vers}}.

* Land on the latest release in each LTS series before crossing to the next series. The trailing patches in each series carry the upgrade-readiness fixes the next series expects.

* MySQL Clone applies only within the same release series. Use MySQL Clone for same-series provisioning, not as a cross-series upgrade method.

* Replication is supported across most paths but enforces a strict source-version constraint. Refer to [Upgrade strategies](./upgrade-strategies.md) for the replicas-first rule.

* An in-place upgrade requires a supported operating system on the source and target releases. Upgrade the operating system first if the current platform is not supported by {{vers}}.

## Choose an upgrade method

The following list compares the supported single-server methods:

* An in-place upgrade replaces the server binaries against the existing data directory. The method delivers the shortest downtime for same-host upgrades and offers no fast rollback.

* A logical dump and load exports SQL from the source server and reloads the data into a fresh {{vers}} server. The method handles the broadest version skew and takes longer for large datasets.

* MySQL Clone copies a consistent physical snapshot from a donor to a recipient. The method requires the same major series and provisions replicas quickly.

* A replication-based upgrade rolls each server in a topology through the rolling upgrade scheme. The method delivers the lowest downtime for high-availability (HA) deployments at the cost of additional infrastructure.

For procedural detail, refer to [Upgrade procedures for {{vers}}](./upgrade-procedures.md) and [Upgrade strategies](./upgrade-strategies.md).

## Upgrade replication topologies

Upgrade a replication topology one server at a time under the rolling upgrade scheme. The scheme applies one of the supported single-server methods per server.

Apply the following rules during a topology upgrade:

* Upgrade replicas before the source. An older source can replicate to a later replica. A later source cannot replicate to an older replica.

* Promote a fully upgraded replica to source after you upgrade every replica. The original source then becomes a replica. Upgrade the original source last.

* Limit cross-source skew to one major version when a replica connects to multiple upstream sources.

For complete guidance, refer to [Upgrade strategies](./upgrade-strategies.md) and the upstream [Upgrading or Downgrading a Replication Topology](https://dev.mysql.com/doc/refman/9.7/en/replication-upgrade.html) documentation.

## Further reading

The following Percona Server for MySQL pages cover related topics:

* [Downgrade options](./downgrade.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)
