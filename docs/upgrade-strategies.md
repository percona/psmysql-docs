# Upgrade strategies

For critical production systems, consider engaging [Percona Support](https://www.percona.com/services/support) to assist with your upgrade process. Our experts can help ensure a smooth transition and minimize potential risks during this sensitive operation.

## Downgrade options

Review the [Downgrade options](downgrade.md) to ensure that your downgrade path is supported.

## In-place upgrade

Use the in-place upgrade strategy only as a last resort. This approach involves shutting down the server and replacing the server binaries or packages with new ones. The new server version then starts using the existing data directory. Configure the server to perform a slow shutdown by setting `innodb_fast_shutdown=0` before shutting down.

The benefits are:

* Lower infrastructure costs compared to creating a new environment, though nodes require testing.

* Ability to complete an upgrade over weeks with cool-down periods between reader node upgrades.

* Requires a failover of production traffic, and achieving minimal downtime demands robust high-availability tools.

If you use XA transactions with InnoDB, running `XA RECOVER` before upgrading checks for uncommitted XA transactions. If results are returned, either commit or rollback the XA transactions by issuing an `XA COMMIT` or `XA ROLLBACK` statement.

## New environment with cut over

Upgrading with a new environment involves provisioning a duplicate environment with the same number of servers with the same hardware specs and same operating system as the current production nodes.

On the newly provided hardware, the target MySQL version will be installed. The new environment will be set up, and the production data will be recovered. Remember that you can use pt-config-diff to verify MySQL configurations. 

Replication from the current source to the newly built environment will be established.
At cutover time, all writes on the current source will be halted, and the application traffic will need to be redirected to the new source. The cutover can be done using a Virtual IP address or manually redirecting the application itself. Once writes are being received on the new environment, you are in a fail forward situation, and the old environment can be torn down.

The new environment strategy has the following pros and cons:

* Additional infrastructure cost since a new environment must be built.

* Ability to upgrade both the OS and the DBMS at the same time.

* Allows upgrade of hardware easily.

* Requires only a single cutover window.

## 8.0 → {{vers}} migration methods

Choose the approach that matches your downtime budget, risk tolerance, and rollback needs. Always rehearse in a non-production environment first.

> **Note**: For a complete overview of supported upgrade paths and methods, see [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md).

### In-place upgrade (stop/replace/start)

Downtime: short to moderate

Risk: higher (shared data directory; fewer rollback options)

Use when: the environment is simple, downtime is acceptable, and you have strong backups and validation.

Prerequisites:

* Complete [Upgrade checklist](./upgrade-checklist-8.4.md) pre-upgrade checks
* Set `innodb_fast_shutdown=0` for a clean shutdown
* Verified backup and restore

Rollback: restore backup and revert binaries.

### Logical dump and restore (clean rebuild)

Downtime: moderate to high (data size dependent)

Risk: moderate (clean metadata; slower for large datasets)

Use when: you want a pristine {{vers}} instance and can accept longer downtime.

Prerequisites:

* Sufficient capacity for parallel dump/restore
* Application maintenance window sized to data volume

Rollback: keep 8.0 online until validation completes; redirect traffic back if needed.

### Side-by-side with replication and controlled cutover

Downtime: minimal (cutover only)

Risk: lower (new environment; defined fallback until fail-forward)

Use when: you need the smallest outage and can provision a parallel environment.

Prerequisites:

* Build a new {{vers}} environment; establish replication from 8.0
* Validate workload on the replica(s) and rehearse failover

Cutover: stop writes on 8.0, allow replica to catch up, redirect traffic (VIP/DNS), then promote {{vers}}.

Rollback: if issues arise before fail-forward, redirect traffic back to 8.0 and resume writes.

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade checklist for {{vers}}](./upgrade-checklist-8.4.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Downgrade options](./downgrade.md)
* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)
* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md)
* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)
