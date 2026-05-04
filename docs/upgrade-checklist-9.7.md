# Upgrade checklist for {{vers}}

**Topic type**: Task

Thorough preparation reduces upgrade risk more than any cutover tactic. Use the following checklist to guide your upgrade from 8.4 Long-Term Support (LTS) to {{vers}}. Validate each item in staging before upgrading production.

For underlying MySQL guidance, see [Upgrading MySQL :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading.html).

## Pre-upgrade checks

Complete the following checks before starting the upgrade.

### Review changes in {{vers}}

Read the release notes and the canonical change lists before any other action. The lists identify deprecations and removals that may force application changes.

Take the following actions:

* [ ] Read [What Is New in MySQL {{vers}} :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/mysql-nutshell.html). Identify deprecations and removals that affect your workload.

* [ ] Read the [MySQL {{vers}} Release Notes :octicons-link-external-16:](https://dev.mysql.com/doc/relnotes/mysql/{{vers}}/en/) for fixes and behavior changes.

* [ ] Read the [Percona Server for MySQL {{vers}} Release notes :octicons-link-external-16:](https://docs.percona.com/percona-server/latest/release-notes/release-notes_index.html).

* [ ] Read [Server and Status Variables and Options Added, Deprecated, or Removed in MySQL {{vers}} :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/added-deprecated-removed.html).

### Verify your backup

A verified backup is the only supported fallback. {{vers}} does not support downgrades between releases or below 8.4 LTS.

Take the following actions:

* [ ] Take a hot backup with Percona XtraBackup. Include the `mysql` system database, the data dictionary, and system tables.

* [ ] Verify the backup by restoring into a clean test environment. Validate startup and table access.

* [ ] Document restore steps and timings. Confirm the runbook with approvers.

* [ ] See [Backup and restore overview](./backup-restore-overview.md).

### Check upgrade compatibility

Run an automated incompatibility scan before any other action. Resolve every issue the scan reports.

Take the following actions:

* [ ] Run the MySQL Shell upgrade checker utility (`util.checkForServerUpgrade()`) against the source server. Target {{vers}} as the destination.

* [ ] Resolve all reported issues. Re-run the utility until the report is clean.

* [ ] Repeat the check after schema changes during preparation.

### Validate schema and data-dictionary readiness

The data-dictionary upgrade fails if specific schema problems exist. Validate the source server using the following commands and queries.

Take the following actions:

* [ ] Run `mysqlcheck -u root -p --all-databases --check-upgrade`. Resolve every reported error.

* [ ] Confirm no tables use obsolete data types or functions.

* [ ] Confirm no orphan `.frm` files remain in the data directory.

* [ ] Confirm every trigger has a valid definer and creation context. Inspect the trigger attributes through `SHOW TRIGGERS` or `INFORMATION_SCHEMA.TRIGGERS`. Verify `character_set_client`, `collation_connection`, and `Database Collation`. Dump and restore any trigger that fails the check.

* [ ] Identify partitioned tables on engines without native partitioning. Convert each table to InnoDB, or remove partitioning, before upgrading.

    ```sql
    SELECT TABLE_SCHEMA, TABLE_NAME
      FROM INFORMATION_SCHEMA.TABLES
      WHERE ENGINE NOT IN ('innodb', 'ndbcluster')
        AND CREATE_OPTIONS LIKE '%partitioned%';
    ```

* [ ] Confirm no foreign key constraint name exceeds 64 characters. Drop and recreate any over-length constraint with a shorter name.

* [ ] Confirm no view defines explicit column names longer than 64 characters.

* [ ] Confirm no `ENUM` or `SET` column element exceeds 255 characters or 1020 bytes.

* [ ] Confirm no table in the `mysql` system database collides with a {{vers}} data dictionary table name.

* [ ] Confirm `sql_mode` contains no obsolete Structured Query Language (SQL) modes. Obsolete modes block server start on {{vers}}.

### Rebuild flagged tables

Some upgrades require table rebuilds. Rebuilds correct collation issues, refresh character-set indexes, or repair corruption that `CHECK TABLE` reports.

Take the following actions:

* [ ] If `mysqlcheck` or `CHECK TABLE` reports that a table requires an upgrade, rebuild the table.

* [ ] For InnoDB tables flagged for upgrade, use the dump and reload method. Dump with `mysqldump` on the source release. Reload with `mysql` after the upgrade.

* [ ] For MyISAM, ARCHIVE, or CSV tables, run `REPAIR TABLE` or `mysqlcheck --repair` on the source release.

* [ ] For collation or character-set changes that affect indexes, rebuild the table with `ALTER TABLE <TABLE_NAME> ENGINE = <STORAGE_ENGINE>`. Use the existing engine value.

* [ ] See [Rebuilding or Repairing Tables or Indexes :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/rebuilding-tables.html) for details.

### Audit reserved keywords in identifiers

Additional reserved words can break schemas and queries. Examples include `MANUAL`, `PARALLEL`, `QUALIFY`, and `TABLESAMPLE`.

Take the following actions:

* [ ] Scan object names and queries for unquoted usage. Quote or rename as needed.

* [ ] See [Keywords and Reserved Words in MySQL {{vers}} :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keywords.html) for the complete list.

### Migrate authentication and connectivity

Impact: The server-side `mysql_native_password` authentication plugin is removed in {{vers}}. The `default_authentication_plugin` system variable, the `--mysql-native-password` server option, and the `--mysql-native-password-proxy-users` server option are also removed. Accounts created in {{vers}} default to `caching_sha2_password`. The client-side `mysql_native_password` plugin remains for backward compatibility with older clients.

Take the following actions:

* [ ] Inventory accounts and applications that still use `mysql_native_password`.

* [ ] Verify that drivers and clients support `caching_sha2_password` and Transport Layer Security (TLS) as configured.

* [ ] Plan account migration to `caching_sha2_password`.

* [ ] Migrate every `mysql_native_password` account before you upgrade. {{vers}} provides no server-side option to re-enable the removed plugin.

* [ ] See [Authentication methods](./authentication-methods.md).

### Update replication syntax and operational scripts

Impact: `MASTER` and `SLAVE` syntax is removed and causes syntax errors. Use `SOURCE` and `REPLICA` commands.

Take the following actions:

* [ ] Search for and update scripts that use `START REPLICA`, `SHOW REPLICA STATUS`, and `CHANGE REPLICATION SOURCE TO`.

* [ ] Validate Orchestrator and other high-availability (HA) tooling versions for {{vers}} syntax.

* [ ] Update Percona Toolkit calls. Replace `pt-slave-find` with `pt-replica-find`. Replace `pt-slave-restart` with `pt-replica-restart`. Remove `pt-slave-delay` usage.

* [ ] For replication topologies, plan a rolling upgrade. Apply a single-server method to each server in turn.

* [ ] See [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md).

### Replace removed features and variables

Impact: Several legacy statements, status counters, variables, and functions are removed in {{vers}}.

Take the following actions:

* [ ] Migrate from `expire_logs_days` to `binlog_expire_logs_seconds`.

* [ ] Remove dependencies on built-in memcached variables and APIs.

* [ ] Replace `WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()` with `WAIT_FOR_EXECUTED_GTID_SET()`.

* [ ] Replace `MASTER` and `SLAVE` statements and counters with `SOURCE` and `REPLICA` equivalents.

* [ ] Audit `my.cnf` for removed startup options and system variables. Update or delete the entries.

### Resolve schema constraint violations

Impact: `AUTO_INCREMENT` is not allowed on `FLOAT` or `DOUBLE` columns.

Take the following actions:

* [ ] Identify any `FLOAT` or `DOUBLE` `AUTO_INCREMENT` columns. Convert the columns to integer types before the upgrade.

### Shut down the source server cleanly

Impact: An in-place upgrade requires a clean shutdown of the source server with redo logs flushed.

Take the following actions:

* [ ] Set `innodb_fast_shutdown=0` and stop the source server through your service manager.

* [ ] If the source server crashed, restart on the source release. Perform a clean shutdown before retrying the upgrade.

* [ ] Confirm no leftover redo log files block restart on the source release.

### Confirm operating system support

Impact: An in-place upgrade requires a {{vers}}-supported operating system. Mismatched platforms force a side-by-side migration.

Take the following actions:

* [ ] Confirm that the host distribution version is supported for {{vers}}.

* [ ] If the host needs an operating system upgrade, plan a side-by-side migration with cutover. See [Upgrade strategies](./upgrade-strategies.md).

### Compare behavior and run tests

Behavioral parity between releases reduces post-upgrade incident risk. Compare query plans, smoke-test the application, and run the source and target in parallel.

Take the following actions:

* [ ] Restore production data into a {{vers}} test server. Run application smoke tests against the server.

* [ ] Use `pt-upgrade` to compare query plans and behavior between 8.4 and {{vers}}.

* [ ] Run load tests at production scale. Capture latency, throughput, and resource use.

* [ ] Run the source and target releases in parallel during the test phase.

### Capture performance baselines

Pre-upgrade baselines define the comparison set for post-upgrade validation. Record latency, throughput, processor, and input/output (IO) measurements before any binary change.

Take the following actions:

* [ ] Capture latency, throughput, and processor and IO baselines on the source release.

* [ ] Document expected regression sources for follow-up investigation. Examples include optimizer changes, character-set changes, stronger encryption, stronger authentication, and additional memory.

### Confirm rollback feasibility

A documented rollback path is the supported fallback when an upgrade fails. Define the path and confirm the runbook before the maintenance window opens.

Take the following actions:

* [ ] Define a rollback path. For example, retain the source environment on standby. Validate point-in-time recovery into a source-compatible reader if applicable.

* [ ] Confirm cutover and rollback runbooks with approvers.

## Post-upgrade validation

Run the following checks immediately after upgrading to {{vers}} and before widening traffic.

### Verify connectivity and authentication

Authentication defaults change in {{vers}}. Confirm that service accounts and external clients connect with the {{vers}} defaults before widening traffic.

Take the following actions:

* [ ] Confirm that accounts created after the upgrade default to `caching_sha2_password`.

* [ ] Verify application logins for every service account.

* [ ] Verify TLS handshakes for every external client.

### Verify replication health (if applicable)

Replication threads and topology coordination must restart cleanly after the upgrade. Validate thread state, failover, and Global Transaction Identifier (GTID) consistency across the topology.

Take the following actions:

* [ ] Confirm that `SHOW REPLICA STATUS` reports healthy IO and SQL threads.

* [ ] Exercise planned failover and change-source procedures.

* [ ] Validate GTID state across the topology.

### Restore spatial indexes

Re-create and verify any spatial indexes that you dropped during preparation.

Take the following actions:

* [ ] Re-create any spatial indexes that you dropped before the upgrade.

* [ ] Run integrity checks. Use `CHECK TABLE ... EXTENDED` and representative spatial queries to verify index health.

### Reload time zone data

The upgrade does not refresh time zone tables. Reload the tables if your applications depend on time zone names.

Take the following actions:

* [ ] Reload time zone tables with `mysql_tzinfo_to_sql`.

    ```shell
    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
    ```

* [ ] Verify that `SELECT @@time_zone;` and named time zone queries return expected values.

### Validate language interfaces and connectors

Client libraries and application drivers must match the {{vers}} authentication and protocol defaults.

Take the following actions:

* [ ] Rebuild language bindings against {{vers}} client libraries. Examples include the Perl `DBD::mysql` module and PHP MySQL extensions.

* [ ] Update application drivers to releases that support `caching_sha2_password`.

* [ ] Run application unit and integration tests against the upgraded server.

### Compare workload and performance baselines

Post-upgrade baseline comparison surfaces regressions caused by {{vers}} default changes. Re-run the baseline workload and review the {{vers}} defaults.

Take the following actions:

* [ ] Re-run baseline queries and workload tests. Compare latency and throughput against the pre-upgrade baseline.

* [ ] Review changes in {{vers}} defaults that can affect performance. Examples include optimizer and costing, redo and undo, and IO settings. Tune as needed.

### Review logs and observability

Server error logs and observability dashboards expose startup problems and post-upgrade regressions.

Take the following actions:

* [ ] Inspect Performance Schema metrics and Service-Level Objectives (SLO) dashboards for regressions.

* [ ] Review error logs and warnings after startup and during smoke tests.

### Validate backup and recovery

A fresh backup on the upgraded release confirms recovery on {{vers}}. The fresh backup replaces the pre-upgrade backup as the operational baseline.

Take the following actions:

* [ ] Optionally, perform a spot restore test to validate recovery on {{vers}}.

* [ ] Take a fresh full backup with Percona XtraBackup once the server is stable.

## Further reading

The following Percona Server for MySQL pages cover upgrade-related topics:

* [Downgrade options](./downgrade.md)

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)
