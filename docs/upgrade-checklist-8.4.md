# Upgrade checklist for {{vers}}

Thorough preparation and validation reduce risk more than any cutover tactic. Use this checklist to guide your upgrade from 8.0 to {{vers}}, validating each item in staging before upgrading production.

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
- [ ] See: [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)

### Removed features and variables

**Impact**: Several legacy statements, status counters, variables, and functions are removed in {{vers}}.

**Action**:

- [ ] Replace MASTER/SLAVE statements and counters with SOURCE/REPLICA equivalents.
- [ ] Migrate from `expire_logs_days` to `binlog_expire_logs_seconds`.
- [ ] Replace `WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()` with `WAIT_FOR_EXECUTED_GTID_SET()`.
- [ ] Remove dependencies on built-in memcached variables/APIs.
- [ ] See: [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)

### Configuration file

**Impact**: The server upgrades the data dictionary first and validates the configuration afterwards. If the configuration file still contains an option that was removed in {{vers}}, the first start of {{vers}} aborts with `[ERROR] [MY-000067] [Server] unknown variable ...` **after** the data directory has already been upgraded. The 8.0 server can no longer start this data directory; to go back, you must restore the backup.

**Action**:

- [ ] Before the first start of {{vers}}, remove the options that no longer exist from the configuration file, for example, `default_authentication_plugin`, `expire_logs_days`, `transaction_write_set_extraction`, `binlog_transaction_dependency_tracking`, `master_info_repository`, and `log_bin_use_v1_row_events`. See [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md).
- [ ] Validate the configuration with the {{vers}} `mysqld` binary before the first start. The command checks the options without touching the data directory. It prints `unknown variable` and exits with a non-zero code if an option is not supported:

    ```shell
    sudo mysqld --validate-config --user=mysql
    ```

    The RPM packages do not start the server, so you can run the command after you install the {{vers}} packages and before you start the server. The DEB packages start the server during `apt install`, so validate the configuration on a staging host with {{vers}} installed first.

- [ ] Install MySQL Shell {{vers}} before you run the upgrade checker. MySQL Shell is the `percona-mysql-shell` package in the Percona Server for MySQL {{vers}} repository. Configure that repository with [Use an APT repository to install Percona Server for MySQL {{vers}}](./apt-repo.md) or [Install using DNF](./yum-repo.md) when `percona-release` is not already installed.

    When the {{vers}} repository is already enabled, install only the Shell package:

    On Debian or Ubuntu:

    ```shell
    sudo apt install percona-mysql-shell
    ```

    On RHEL or derivatives:

    ```shell
    sudo dnf install percona-mysql-shell
    ```

    On a host that still runs 8.0, enable the {{vers}} repository for this package, install `percona-mysql-shell`, and disable that repository again. The server packages stay on 8.0 until the [upgrade procedures](./upgrade-procedures.md).

    On Debian or Ubuntu:

    ```shell
    sudo percona-release enable {{pkg}} release --scheme https
    sudo apt update
    sudo apt install percona-mysql-shell
    sudo percona-release disable {{pkg}} release
    ```

    On RHEL or derivatives:

    ```shell
    sudo percona-release enable {{pkg}} release
    sudo dnf install percona-mysql-shell
    sudo percona-release disable {{pkg}} release
    ```

- [ ] Run the MySQL Shell upgrade checker and pass your configuration file with `--config-path`. Without this option, the checker does not check the configuration file:

    ```shell
    mysqlsh -- util check-for-server-upgrade root@localhost:3306 --target-version={{tag}} --config-path=/etc/my.cnf
    ```

    On Debian and Ubuntu, the server configuration is in `/etc/mysql/mysql.conf.d/mysqld.cnf`.

### Reserved keywords in identifiers

**Impact**: New reserved words (for example, `MANUAL`, `PARALLEL`, `QUALIFY`, `TABLESAMPLE`) can break schemas and queries.

**Action**:

- [ ] Scan object names and queries for unquoted usage; quote or rename as needed.
- [ ] See: [Keywords and Reserved Words in MySQL {{vers}} :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keywords.html) for the complete list of reserved keywords.


### Schema constraints

**Impact**: `AUTO_INCREMENT` is not allowed on `FLOAT`/`DOUBLE`.

**Action**:

- [ ] Identify and convert any `FLOAT`/`DOUBLE` `AUTO_INCREMENT` columns to integer types prior to upgrade.

### Configuration defaults review

**Impact**: {{vers}} changes several InnoDB defaults for modern hardware; old 8.0 configs may not be optimal and can cause behavior changes.

**Action**:

- [ ] Compare your overrides to {{vers}} defaults; remove obsolete settings and re-evaluate IO/log parameters.
- [ ] If `innodb_numa_interleave=OFF`, set `innodb_buffer_pool_populate=OFF` in 8.4.11 to keep 8.4.10 pre-faulting behavior. See [NUMA interleave and buffer pool populate](./8.4-defaults-and-tuning.md#numa-interleave-and-buffer-pool-populate).
- [ ] See: [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)

### Spatial indexes

**Impact**: A known issue can corrupt a spatial index (R-Tree index) in MySQL 8.4.0 through 8.4.3. The corruption is triggered when an `UPDATE` that slightly changes a geometry's MBR (Minimum Bounding Rectangle) is immediately followed by a `DELETE` of the same row. This issue is fixed in 8.4.4 and later.

**Action**:

- [ ] If upgrading to 8.4.0-8.4.3, drop spatial indexes before upgrade (document which ones for post-upgrade re-creation) as a precautionary measure.
- [ ] If upgrading to 8.4.4 or later, this issue is fixed; spatial indexes can remain in place.
- [ ] Plan to re-create any spatial indexes dropped pre-upgrade after upgrade completion.
- [ ] See: [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md#spatial-indexes) for detailed information and workarounds.

### Backup and recovery rehearsal

**Action**:

- [ ] Take a hot backup of the 8.0 data directory with Percona XtraBackup 8.0 and record the restore steps and timings. The package is `percona-xtrabackup-80`. Percona XtraBackup 8.4 backs up {{vers}} servers; see [Percona XtraBackup compatibility](./8.4-compatibility-and-removed-items.md#percona-xtrabackup-pxb).

    On Debian or Ubuntu:

    ```shell
    sudo percona-release enable pxb-80 release --scheme https
    sudo apt update
    sudo apt install percona-xtrabackup-80
    ```

    On RHEL or derivatives:

    ```shell
    sudo percona-release enable pxb-80 release
    sudo dnf install percona-xtrabackup-80
    ```

    `xtrabackup` reads the server settings from the configuration file. Use an empty target directory:

    ```shell
    sudo xtrabackup --backup --target-dir=/data/backups/ps-8.0
    ```

- [ ] Restore that backup into a clean {{vers}} environment and confirm the server starts and finishes the metadata upgrade.
- [ ] See: [Backup and restore overview](./backup-restore-overview.md) and [Create a full backup :octicons-link-external-16:](https://docs.percona.com/percona-xtrabackup/8.0/create-full-backup.html).

### Behavior comparison and testing

**Action**:

- [ ] Use `pt-upgrade` to compare query plans/behavior between 8.0 and {{vers}}.
- [ ] Run application smoke and load tests against a restored {{vers}} copy.

### Plugins to components transitions

**Impact**: Some 8.0 plugins are removed or replaced by components in {{vers}}.

**Action**:

- [ ] If a component exists in 8.0 (for example, data masking), transition in 8.0 before upgrading.
- [ ] If the 8.0 server uses the `keyring_file` plugin, migrate the keys to `component_keyring_file` in 8.0 before upgrading. {{vers}} does not include the plugin. With encrypted tables, the first {{vers}} start aborts with `Encryption can't find master key` after the upgrade has started. See [Migrate from the keyring_file plugin to component_keyring_file](./upgrade-components.md#migrate-from-the-keyring_file-plugin-to-component_keyring_file).
- [ ] Plan configuration changes from plugin variables/`--early-plugin-load` to component manifests/config files.
- [ ] See: [Upgrade from plugins to components](./upgrade-components.md)

### Rollback feasibility

**Action**:

- [ ] Define a rollback path (for example, keep 8.0 environment on standby or validate point-in-time recovery to 8.0-compatible readers if applicable).
- [ ] Confirm cutover/rollback runbooks with approvers.

## Post-upgrade validation

Run these checks immediately after upgrading from 8.0 to {{vers}} and before widening traffic.

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
- [ ] See: [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)

### Logs and observability

- [ ] Review error logs and warnings post-startup and during smoke tests.
- [ ] Inspect Performance Schema metrics and application SLOs for regressions.

### Backup and recovery

- [ ] Take a fresh full backup with Percona XtraBackup 8.4. Install `percona-xtrabackup-84` from the `pxb-84` repository, then write the upgraded data directory to an empty target directory.

    On Debian or Ubuntu:

    ```shell
    sudo percona-release enable pxb-84 release --scheme https
    sudo apt update
    sudo apt install percona-xtrabackup-84
    ```

    On RHEL or derivatives:

    ```shell
    sudo percona-release enable pxb-84 release
    sudo dnf install percona-xtrabackup-84
    ```

    `xtrabackup` reads the server settings from the configuration file. Use an empty target directory:

    ```shell
    sudo xtrabackup --backup --target-dir=/data/backups/ps-8.4
    ```

- [ ] Optionally perform a spot restore test to validate recovery on {{vers}}.

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Downgrade options](./downgrade.md)
* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)
* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md)
* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)

