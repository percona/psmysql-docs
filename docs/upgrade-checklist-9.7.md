# Upgrade checklist for {{vers}}

Thorough preparation and validation reduce risk more than any cutover tactic. Use this checklist to guide your upgrade from 8.4 to {{vers}}. Validate each item in staging before upgrading production.

## Pre-upgrade checks

Complete these checks before starting the upgrade process.

### Authentication and connectivity

Impact:

--8<--- "authentication-9x-overview.md:1:1"

Action:

- [ ] Inventory accounts and applications that still use `mysql_native_password`.

- [ ] Verify that drivers and clients support `caching_sha2_password` and TLS when your environment requires encrypted connections.

- [ ] Plan account migration to `caching_sha2_password` before cutover. MySQL 9.x does not provide temporary native-password compatibility on the server.

- [ ] See [Authentication methods](./authentication-methods.md).

### Replication and operational scripts

Impact: {{vers}} removes MASTER and SLAVE syntax. The removed syntax causes syntax errors at runtime. Use SOURCE and REPLICA commands instead.

Action:

- [ ] Search scripts and update calls to use `START REPLICA`, `SHOW REPLICA STATUS`, and `CHANGE REPLICATION SOURCE TO`.

- [ ] Validate Orchestrator and other HA tooling versions for {{vers}} syntax.

- [ ] Update Percona Toolkit calls. Replace `pt-slave-find` with `pt-replica-find`. Replace `pt-slave-restart` with `pt-replica-restart`. Remove `pt-slave-delay` usage.

- [ ] See: [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

### Removed features and variables

Impact: {{vers}} removes several legacy statements, status counters, variables, and functions.

Action:

- [ ] Replace MASTER and SLAVE statements and counters with SOURCE and REPLICA equivalents.

- [ ] Migrate from `expire_logs_days` to `binlog_expire_logs_seconds`.

- [ ] Replace `WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()` with `WAIT_FOR_EXECUTED_GTID_SET()`.

- [ ] Remove dependencies on built-in memcached variables and APIs.

### Reserved keywords in identifiers

Impact: New reserved words such as `MANUAL`, `PARALLEL`, `QUALIFY`, and `TABLESAMPLE` can break schemas and queries.

Action:

- [ ] Scan object names and queries for unquoted usage. Quote or rename identifiers as needed.

- [ ] See [Keywords and reserved words in MySQL {{vers}} :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keywords.html) for the complete list of reserved keywords.

### Schema constraints

Impact: {{vers}} does not allow `AUTO_INCREMENT` on `FLOAT` or `DOUBLE` columns.

Action:

- [ ] Identify any `FLOAT` or `DOUBLE` columns that use `AUTO_INCREMENT`. Convert these columns to integer types before upgrade.

### Backup and recovery rehearsal

Action:

- [ ] Take a hot backup with Percona XtraBackup. Document the restore steps and timings.

- [ ] Restore the backup into a clean {{vers}} environment. Validate server startup and the metadata upgrade.

- [ ] See [Backup and restore overview](./backup-restore-overview.md).

### Behavior comparison and testing

Action:

- [ ] Use `pt-upgrade` to compare query plans and behavior between 8.4 and {{vers}}.

- [ ] Run application smoke and load tests against a restored {{vers}} copy.

### Rollback feasibility

Action:

- [ ] Define a rollback path. For example, keep the 8.4 environment on standby. As an alternative, validate point-in-time recovery to 8.4-compatible readers when applicable.

- [ ] Confirm cutover and rollback runbooks with approvers.

## Post-upgrade validation

Run these checks immediately after upgrading from 8.4 to {{vers}} and before widening traffic.

### Connectivity and authentication

- [ ] Verify application logins for every service account.

- [ ] Confirm that new account creations default to `caching_sha2_password`.

### Replication health (if applicable)

- [ ] Confirm that `SHOW REPLICA STATUS` reports healthy IO and SQL threads.

- [ ] Exercise planned failover and change-source procedures.

### Spatial indexes

- [ ] Re-create any spatial indexes dropped before the upgrade.

- [ ] Run integrity checks such as `CHECK TABLE ... EXTENDED`. Run representative spatial queries to verify index health.

### Workload and performance baselines

- [ ] Re-run baseline queries and workload tests. Compare latency and throughput against the 8.4 baseline.

- [ ] Review changes in {{vers}} defaults that affect performance, including optimizer costing, redo and undo handling, and IO settings. Tune as needed.

### Logs and observability

- [ ] Review error logs and warnings after startup and during smoke tests.

- [ ] Inspect Performance Schema metrics and application SLOs for regressions.

### Backup and recovery

- [ ] Take a fresh full backup with Percona XtraBackup.

- [ ] Optional: run a spot restore test to validate recovery on {{vers}}.

## Further reading

- [Upgrade overview](./upgrade.md)

- [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

- [Upgrade strategies](./upgrade-strategies.md)

- [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

- [Upgrade from plugins to components](./upgrade-components.md)

- [Downgrade options](./downgrade.md)

- [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)
