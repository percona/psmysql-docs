# Upgrade checklist for {{vers}}

Thorough preparation and validation reduce risk more than any cutover tactic. Use this checklist to guide your upgrade from 8.4 to {{vers}}, validating each item in staging before upgrading production.

## Pre-upgrade checks

Complete these checks before starting the upgrade process.

### Authentication and connectivity

**Impact**: `mysql_native_password` is disabled by default in {{vers}}; `default_authentication_plugin` is removed. New accounts default to `caching_sha2_password`. The `mysql_native_password` plugin can still be loaded using `--mysql-native-password=ON` if needed, but it will be completely removed in the MySQL 9.x series.

**Action**:

- [ ] Inventory accounts and applications that still use `mysql_native_password`.
- [ ] Verify drivers/clients support `caching_sha2_password` and TLS as configured.
- [ ] Plan account migration to `caching_sha2_password`. If temporary compatibility is needed, `--mysql-native-password=ON` can be used, but plan migration as this plugin will be removed in future versions.
- [ ] See: [authentication methods](./authentication-methods.md)

### Replication and operational scripts

**Impact**: MASTER/SLAVE syntax is removed and will cause syntax errors if used; use SOURCE/REPLICA commands.

**Action**:

- [ ] Search and update scripts: `START REPLICA`, `SHOW REPLICA STATUS`, `CHANGE REPLICATION SOURCE TO`.
- [ ] Validate Orchestrator/HA tooling versions for {{vers}} syntax.
- [ ] Update Percona Toolkit calls: replace `pt-slave-find` with `pt-replica-find`, and `pt-slave-restart` with `pt-replica-restart`; remove `pt-slave-delay` usage.
- [ ] See: [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

### Removed features and variables

**Impact**: Several legacy statements, status counters, variables, and functions are removed in {{vers}}.

**Action**:

- [ ] Replace MASTER/SLAVE statements and counters with SOURCE/REPLICA equivalents.
- [ ] Migrate from `expire_logs_days` to `binlog_expire_logs_seconds`.
- [ ] Replace `WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()` with `WAIT_FOR_EXECUTED_GTID_SET()`.
- [ ] Remove dependencies on built-in memcached variables/APIs.

### Reserved keywords in identifiers

**Impact**: New reserved words (for example, `MANUAL`, `PARALLEL`, `QUALIFY`, `TABLESAMPLE`) can break schemas and queries.

**Action**:

- [ ] Scan object names and queries for unquoted usage; quote or rename as needed.
- [ ] See: [Keywords and Reserved Words in MySQL {{vers}} :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keywords.html) for the complete list of reserved keywords.


### Schema constraints

**Impact**: `AUTO_INCREMENT` is not allowed on `FLOAT`/`DOUBLE`.

**Action**:

- [ ] Identify and convert any `FLOAT`/`DOUBLE` `AUTO_INCREMENT` columns to integer types prior to upgrade.

### Backup and recovery rehearsal

**Action**:

- [ ] Take a hot backup with Percona XtraBackup; document restore steps and timings.
- [ ] Restore into a clean {{vers}} environment; validate startup and metadata upgrade.
- [ ] See: [Backup and restore overview](./backup-restore-overview.md)

### Behavior comparison and testing

**Action**:

- [ ] Use `pt-upgrade` to compare query plans/behavior between 8.4 and {{vers}}.
- [ ] Run application smoke and load tests against a restored {{vers}} copy.

### Rollback feasibility

**Action**:

- [ ] Define a rollback path (for example, keep 8.4 environment on standby or validate point-in-time recovery to 8.4-compatible readers if applicable).
- [ ] Confirm cutover/rollback runbooks with approvers.

## Post-upgrade validation

Run these checks immediately after upgrading from 8.4 to {{vers}} and before widening traffic.

### Connectivity and authentication

- [ ] Verify application logins for every service account.
- [ ] Confirm new account creations default to `caching_sha2_password` as expected.

### Replication health (if applicable)

- [ ] Confirm `SHOW REPLICA STATUS` reports healthy IO/SQL threads.
- [ ] Exercise planned failover and change-source procedures.

### Spatial indexes

- [ ] Re-create any spatial indexes dropped pre-upgrade.
- [ ] Run integrity checks (for example, `CHECK TABLE ... EXTENDED`) and representative spatial queries to verify index health.

### Workload and performance baselines

- [ ] Re-run baseline queries and workload tests; compare latency and throughput.
- [ ] Review changes in {{vers}} defaults that can affect performance (optimizer/costing, redo/undo, IO settings) and tune as needed.

### Logs and observability

- [ ] Review error logs and warnings post-startup and during smoke tests.
- [ ] Inspect Performance Schema metrics and application SLOs for regressions.

### Backup and recovery

- [ ] Take a fresh full backup with Percona XtraBackup.
- [ ] Optionally perform a spot restore test to validate recovery on {{vers}}.

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Downgrade options](./downgrade.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)
