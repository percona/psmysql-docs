# Upgrade strategies

**Topic type**: Concept

For critical production systems, consider engaging [Percona Support :octicons-link-external-16:](https://www.percona.com/services/expert-support/) to assist with your upgrade. Our experts can help you complete a smooth transition and minimize risk during this sensitive operation.

The following strategies cover most {{vers}} upgrade scenarios. Combine the prep steps in [Upgrade procedures for {{vers}}](./upgrade-procedures.md) with the strategy that matches your environment.

For underlying MySQL guidance, see [Upgrading or Downgrading a Replication Topology :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/replication-upgrade.html).

## Downgrade options

Review the [Downgrade options](./downgrade.md) to confirm that your downgrade path is supported.

## Choose an upgrade strategy

Use the following table to choose the strategy that matches your downtime budget, risk tolerance, and infrastructure constraints.

| Strategy | Downtime | Risk | Infrastructure cost | Best for |
|---|---|---|---|---|
| In-place | Short to moderate, equal to restart and metadata upgrade time | Higher, due to shared data directory and limited rollback | Low | Same-platform upgrades on a single host or where parallel hardware is unavailable |
| Logical dump and restore | Moderate to high, scaled to data size | Moderate, with clean metadata at the cost of dump and load time | Low to moderate | Cross-platform moves, storage-engine consolidations, and clean rebuilds |
| Side-by-side with cutover | Minimal, only at cutover | Lower, with a defined fallback until fail-forward | High, requires parallel hardware | Critical production systems with the smallest tolerable outage |
| MySQL Clone | Minimal, only at cutover | Lower, with a fast physical snapshot | Moderate, requires a recipient server | Provisioning a {{vers}} replica from a same Long-Term Support (LTS) donor at scale |
| Rolling upgrade in a replication topology | Per-node restart only | Lower, with replicas absorbing traffic | Low if replicas already exist | Existing replication topologies where the source remains available |

For supported upgrade paths and methods, see [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md).

## Upgrade in place

An in-place upgrade replaces binaries on the same host and restarts on the existing data directory. The strategy is the fastest binary swap and requires no parallel hardware.

The procedure halts the server, replaces packages, and starts {{vers}} against the same data files. Configure a slow shutdown by setting `innodb_fast_shutdown=0` before stopping. A slow shutdown leaves InnoDB in a state that is safe across releases.

Take the following actions before the upgrade:

* Verify a backup and test a restore.

* Complete the [upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md).

* Run `XA RECOVER` against the source server. Commit or rollback any uncommitted XA transactions.

The in-place strategy has the following trade-offs:

* Downtime equals the restart and metadata upgrade time.

* The rollback path is limited because the data directory remains in place.

* Infrastructure cost is lower than parallel-environment options.

Rollback path: stop the server, restore the verified backup, then revert the binaries. Test the rollback in staging.

For step-by-step commands, see [Upgrade procedures for {{vers}}](./upgrade-procedures.md).

## Use logical dump and restore

A logical upgrade exports Structured Query Language (SQL) from the source server. The export reloads into a fresh {{vers}} server. The path produces clean metadata at the cost of a longer maintenance window.

Take the following actions before the upgrade:

* Size the maintenance window to your data volume. Test the dump and restore time on a representative sample.

* Provision capacity for parallel dump and restore on the target host.

* Run `mysqlcheck --check-upgrade` and resolve any reported issues.

The logical strategy has the following trade-offs:

* Downtime is long and scales with data size.

* The target is clean and inherits no carryover from the source data directory.

* The strategy supports cross-platform and cross-storage-engine moves.

Rollback path: keep the source server available until validation completes. Redirect traffic back to the source if the {{vers}} server fails validation.

For step-by-step commands, see [Perform a logical upgrade with mysqldump](./upgrade-procedures.md#perform-a-logical-upgrade-with-mysqldump).

## Run a side-by-side migration with controlled cutover

A side-by-side migration runs the source and {{vers}} environments in parallel and redirects traffic at a single cutover. The strategy provides the smallest outage and the cleanest rollback at the cost of parallel infrastructure.

Take the following actions to build the parallel environment:

* Match the production environment in server count, hardware specifications, and operating system.

* Install Percona Server for MySQL {{vers}} on the parallel hardware.

* Recover the production data into the parallel environment. Verify configuration parity with `pt-config-diff`.

* Configure replication from the source to the parallel environment.

* Validate the workload on the parallel replicas. Rehearse failover.

Take the following actions at cutover:

* Halt writes on the source. Allow replicas to apply remaining transactions.

* Promote {{vers}} as the primary write target.

* Redirect traffic with a Virtual IP (VIP) address or a Domain Name System (DNS) update.

After traffic lands on {{vers}} and validation completes, decommission the source environment.

The side-by-side strategy has the following trade-offs:

* Infrastructure cost is highest during the migration window.

* The strategy requires a single cutover window.

* Database, hardware, and operating system upgrades can land in the same window.

Rollback path: before fail-forward, redirect traffic back to the source. Resume writes on the source.

## Use MySQL Clone for provisioning

MySQL Clone provides a physical InnoDB snapshot from a donor server to a recipient. The recipient receives a fully functional data directory. Cloning is a fast way to provision a {{vers}} replica from a same-LTS donor.

Cloning supports two operation modes:

* Local clone: the donor and recipient run on the same host. The clone produces a directory copy on local storage.

* Remote clone: the donor and recipient run on separate hosts. The clone transfers data over the network. The recipient receives schemas, tablespaces, and data-dictionary metadata from the donor.

The clone operation also extracts replication coordinates from the donor and applies the coordinates on the recipient. The recipient can join replication without replaying the full transaction history. Cloning a large dataset is faster than synchronizing through replication alone.

Take the following actions to use clone for upgrade provisioning:

* Match the donor and recipient on the same LTS series. Cross-LTS clone is not supported.

* Install the clone plugin on both donor and recipient.

* Grant `BACKUP_ADMIN` on the donor and `CLONE_ADMIN` on the recipient.

* Run the clone, start the recipient, and validate the data.

For details, see [The Clone Plugin :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/clone-plugin.html).

## Run a rolling upgrade in a replication topology

A rolling upgrade rolls each server in a replication topology through the procedure in turn. Replication continues during the rollout. Replicas absorb traffic while the source upgrades.

Replication supports an older source paired with a later replica, but not the inverse. Upgrade replicas first and then upgrade the source. A replica at an earlier release cannot process transactions from a source at a later release.

The procedure has the following stages.

1. Upgrade replicas one at a time. For each replica, follow the [single-server procedure](./upgrade-procedures.md). Restart replication with `START REPLICA` after each upgrade.

2. For multi-tier topologies, upgrade replicas farthest from the source first. Work bottom-up.

3. After all replicas are on {{vers}}, switch over. Stop writes on the source. Wait for at least one replica to apply all transactions. Promote that replica as the source.

4. Upgrade the previous source as a single server. Reinsert the upgraded server into the topology.

Multi-source replication has a stricter constraint. A multi-source topology supports at most two MySQL versions concurrently. Plan the rollout to keep the active versions to two or fewer at any time.

For the canonical procedure, see [Upgrading or Downgrading a Replication Topology :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/replication-upgrade.html).

## Further reading

The following Percona Server for MySQL pages cover upgrade-related topics:

* [Downgrade options](./downgrade.md)

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
