# MySQL 9.7 technical migration overview

MySQL 9 minor releases remove legacy plugins and change defaults for security and replication. Database administrators must align accounts, configuration files, and replication topology before they upgrade.

Use this overview alongside the [upgrade overview](upgrade.md), [installation](installation.md) guide, and [upgrade procedures](upgrade-procedures.md).

You move from MySQL 8.4 Long-Term Support (LTS) toward Percona Server for MySQL 9.7. Percona behavior can differ from Oracle MySQL Community Edition.

Read the [release notes](release-notes/release-notes-index.md) for your build.

The following sections group incompatible changes by feature area, describe MySQL 9.7 Community Server behavior, and provide a pre-upgrade checklist.

## Review breaking changes before upgrade

Address the following items before you upgrade production servers.

High-impact items:

* `mysql_native_password` authentication plugin is removed.

* Migrate all accounts to a supported plugin (for example, `caching_sha2_password`) before upgrade, or authentication fails.

* `gtid_mode` and `enforce_gtid_consistency` default to `ON`.

* You must set Global Transaction Identifier (GTID) options explicitly when replication still uses file names and positions only.

* `keyring_file` plugin is removed.

* Migrate to a supported keyring component before upgrade, or the server may fail to start.

Each subsection states impact, replacement options, and required actions.

## Authentication and accounts

### Remove `mysql_native_password`

Oracle removed the `mysql_native_password` plugin and related server options in MySQL 9.0. Percona Server for MySQL 9.7 includes this change.

Impact:

* Accounts that still use `mysql_native_password` cannot authenticate against a MySQL 9.0 and later server.

* Clients without `CLIENT_PLUGIN_AUTH` support receive rejection during handshake.

* Server removes `--mysql-native-password`, `--mysql-native-password-proxy-users`, and `default_authentication_plugin`.

* The removal affects only the MySQL 9.0 and later server process.

* Client libraries can still use `mysql_native_password` against older MySQL 8.0 or 5.7 servers.

Replacement:

* Use `caching_sha2_password` or another supported authentication plugin.

* The default plugin for accounts you create is `caching_sha2_password` in MySQL 8.4 and later.

Action:

* List accounts and applications that still reference `mysql_native_password`.

* Migrate each account to a supported plugin before you upgrade the server.

* Delete references to removed authentication options and variables from configuration files and scripts before upgrade.

Example statement:

```sql
ALTER USER '<USERNAME>'@'<HOST>'
IDENTIFIED WITH caching_sha2_password BY '<PASSWORD>';
```

### Configure caching SHA-2 storage format

MySQL 9.7 Community Server exposes the following variables for caching SHA-2 password storage:

* `caching_sha2_password_storage_format`

* `caching_sha2_password_enforce_storage_format`

These variables support PBKDF2 storage with `caching_sha2_password`.

See [Caching SHA-2 pluggable authentication](https://dev.mysql.com/doc/refman/9.7/en/caching-sha2-pluggable-authentication.html).

## Replication and GTID

Replication behavior depends on Global Transaction Identifier (GTID) variables. Incorrect defaults cause most upgrade failures in mixed topologies.

### Configure GTID defaults

Oracle changed GTID defaults in MySQL 9.0. Percona Server for MySQL 9.7 includes this change.

Impact:

* `gtid_mode` defaults to `ON` in MySQL 9.0 and later.

* `enforce_gtid_consistency` defaults to `ON`.

* Non-GTID replication can fail to start unless you set variables explicitly.

* `enforce_gtid_consistency=ON` blocks certain non-deterministic statements inside transactions.

* Some packages apply `OFF_PERMISSIVE` transition states during upgrade.

* Until GTID migration completes, set explicit `gtid_mode=OFF` and `enforce_gtid_consistency=OFF` when needed.

Replacement:

* Adopt GTID-based replication or set GTID variables off before you start the upgraded server.

Action:

* If you do not use GTID yet, add the following lines to configuration before upgrade:

```text
gtid_mode=OFF
enforce_gtid_consistency=OFF
```

* Review application SQL and stored programs for `enforce_gtid_consistency=ON` violations.

| Variable                   | Default in MySQL 9.0 and later | Default before 9.0 |
| -------------------------- | ------------------------------ | ------------------ |
| `gtid_mode`                | `ON`                           | `OFF`              |
| `enforce_gtid_consistency` | `ON`                           | `OFF`              |

### Set `replica_parallel_workers` minimum

Oracle disallows `replica_parallel_workers=0` starting in MySQL 9.3. Percona Server for MySQL 9.7 includes this change.

Impact:

* Minimum value is `1`.

* Default became `4` in MySQL 8.0.30 and later.

* Setups that use `replica_parallel_workers=0` for single-threaded apply must change before upgrade.

Replacement:

* Use `replica_parallel_workers=1` for single-threaded apply or omit the variable to keep the default.

Action:

* Before upgrade, change `replica_parallel_workers=0` to `1` or delete the line to restore the default.

### Replace removed Group Replication and semisync variables

Oracle removed several replication variables in MySQL 9.5. Semisynchronous replication moved from plugins to components. Percona Server for MySQL 9.7 includes this change.

Impact:

* `group_replication_allow_local_lower_version_join` is removed.

* `replica_parallel_type` and `slave_parallel_type` are removed.

* MySQL 9.5 removes the legacy semisynchronous plugins `semisync_master.so` and `semisync_slave.so`.

* `rpl_semi_sync_*` variables are removed.

* Semisynchronous replication remains available through replacement components.

Replacement:

* Use the Semisynchronous Replication Source and Replica components for semisync behavior.

Action:

* Delete removed variables from configuration and monitoring.

* Install and configure semisync components as documented in the MySQL Reference Manual.

### Configure replication across versions

MySQL 9.7 Community Server exposes the following replication-related settings:

* `replica_allow_higher_version_source` controls replication from a higher-version source to a lower replica. Use this variable during staged upgrades.

* `object_policy_flush_interval_seconds` refreshes the object policy cache on secondaries and replicas.

References:

* [Replication options (replica)](https://dev.mysql.com/doc/refman/9.7/en/replication-options-replica.html)

* [MySQL 9.7.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html)

## Keyring and encryption

### Migrate from `keyring_file` to `component_keyring_file`

Migration requires a component manifest. You cannot convert the plugin with a single `my.cnf` edit.

Oracle removed the `keyring_file` plugin in MySQL 9.2. Percona Server for MySQL 9.7 includes this change.

Impact:

* The MySQL 9.2 distribution omits the `keyring_file` plugin binary.

* Startup fails when configuration still loads the plugin.

Replacement:

* Install `component_keyring_file` for file-based keyring storage.

* Configure the component through a JSON manifest.

* Use files such as `component_keyring_file.cnf` or the manifest registry.

* Do not rely on legacy plugin variables in `my.cnf` alone.

Action:

* Create and initialize the component manifest before upgrade.

* Move keyring data into the component layout that the manual specifies.

* Remove `keyring_file` directives from `my.cnf` and other option files before upgrade.

## Plugins, components, and extensions

### Remove `--early-plugin-load`

Oracle removed the `--early-plugin-load` server option in MySQL 9.1. Percona Server for MySQL 9.7 includes this change.

Impact:

* Configuration files that still contain `--early-plugin-load` can prevent startup.

Replacement:

* Load functionality through supported components and the component manifest (for example, `mysqld.my`).

Action:

* Search configuration paths for `--early-plugin-load` and delete those lines.

* Move required behavior to components when the manual documents migration steps.

### Migrate Connection Control to the component

Oracle deprecated the Connection Control plugins and removed them after MySQL 9.2. Percona Server for MySQL 9.7 includes this change.

Impact:

* Oracle removes both Connection Control plugins from the distribution after MySQL 9.2.

Replacement:

* Install `component_connection_control` through `INSTALL COMPONENT` syntax.

Action:

* Replace the plugins with the component.

* Update monitoring queries that read deprecated Information Schema tables.

### Remove Version Tokens usage

Oracle deprecated Version Tokens in MySQL 9.2 and removed the plugin in MySQL 9.3. Percona Server for MySQL 9.7 includes this change.

Impact:

* MySQL 9.3 removes functions, privileges, and variables associated with Version Tokens.

Replacement:

* Oracle provides no direct substitute inside the server.

Action:

* Delete Version Tokens references from configuration and application code before upgrade.

### Install components that Community Edition includes

MySQL 9.7 Community Server includes components that once required MySQL Enterprise Edition only.

The following list orders components alphabetically by name:

* Group Replication Flow Control Statistics component

* Group Replication Primary Election component

* Group Replication Resource Manager component

* Replication Applier Metrics component

* Telemetry component

See [MySQL 9.7.0 release notes, Component notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

## InnoDB and storage

### Remove deprecated InnoDB variables

Oracle removed legacy InnoDB sizing variables in MySQL 9.3. Redo and undo sizing follow variables documented for MySQL 9.7. Percona Server for MySQL 9.7 includes this change.

Impact:

The following variables are removed:

* `innodb_log_file_size`

* `innodb_log_files_in_group`

* `innodb_undo_tablespaces`

Replacement:

| Removed variable          | MySQL 9.7 approach          |
| ------------------------- | --------------------------- |
| `innodb_log_file_size`    | `innodb_redo_log_capacity`  |
| `innodb_log_files_in_group` | Automatic management      |
| `innodb_undo_tablespaces` | Automatic undo management   |

Action:

* Delete removed variables from option files.

* Read redo and undo chapters in the MySQL Reference Manual for the target version.

### Configure InnoDB redo writers and binary log history

Oracle changed default behavior in MySQL 9.5 and later. Percona Server for MySQL 9.7 includes this change.

Default behavior depends on `innodb_log_writer_threads`:

* When binary logging is off, the default follows logical CPU count.

* When binary logging is on, defaults match MySQL 9.4 rules for large CPU counts.

The `binlog_transaction_dependency_history_size` default is 1,000,000 in MySQL 9.5.0 and later. The maximum is 10,000,000.

Existing explicit values stay unchanged.

### Recognize atomic DDL for databases

`CREATE DATABASE` and `DROP DATABASE` run as atomic, crash-safe operations.

Oracle introduced this behavior in MySQL 9.1. Percona Server for MySQL 9.7 includes this change.

Impact:

* Correct usage does not change; behavior improves for crash recovery.

Action:

* No change required

## SQL and schema behavior

### Fix `IGNORE` with scalar subqueries

`IGNORE` no longer hides `ER_SUBQUERY_NO_1_ROW` when a scalar subquery returns more than one row.

Oracle introduced this behavior in MySQL 9.0. Percona Server for MySQL 9.7 includes this change.

Impact:

* `INSERT IGNORE`, `UPDATE IGNORE`, and `DELETE IGNORE` can fail where they succeeded before.

Replacement:

* Restrict scalar subqueries to zero or one row.

Action:

* Audit application SQL and stored routines.

* Correct the logic or remove unsafe `IGNORE` usage.

### Enforce inline foreign keys

Oracle enforces inline foreign key syntax that older releases parsed but ignored.

Oracle introduced this enforcement in MySQL 9.0. Percona Server for MySQL 9.7 includes this change.

Impact:

* MySQL 9.0 rejects invalid inline foreign keys as errors.

Action:

* Compare schemas and generated Data Definition Language (DDL) against intended constraints.

### Plan migration from `MD5()` and `SHA1()` in SQL

Oracle deprecates the `MD5()` and `SHA1()` SQL functions in MySQL 9.4. Legacy applications that compute hashes in SQL face the highest risk of breakage.

Impact:

* Deprecation applies to the SQL functions `MD5()` and `SHA1()`.

* Functions still execute, but Oracle may remove them in a later release.

* PHP and Java stacks that call these functions in SQL need review.

Replacement:

* Call `SHA2()` in SQL or compute hashes in the application.

Action:

* Audit procedures, triggers, and application SQL.

* Replace `MD5()` and `SHA1()` calls when compliance allows.

### Review foreign key cascade handling

The variable `enable_cascade_triggers` controls the foreign key cascade execution path in MySQL 9.7 Community Server. Oracle deprecated the variable in the same release.

Follow the MySQL 9.7 manual for supported behavior after upgrade.

### Run Data Manipulation Language (DML) on JSON duality views

MySQL 9.7 Community Server supports `INSERT`, `UPDATE`, and `DELETE` on JSON duality views.

See [DML operations on JSON duality views](https://dev.mysql.com/doc/refman/9.7/en/json-duality-views-updatable.html).

## Client tools and administration

### Adjust mysql client `\G` and `\C` usage

The `mysql` client accepts `\G` (vertical output) and `\C` (clear) only at the end of a statement.

Oracle introduced this restriction in MySQL 9.1. Percona Server for MySQL 9.7 includes this change.

Impact:

* Scripts that place `\G` or `\C` in the middle of a statement can fail or print unexpected output.

Replacement:

* Place `\G` and `\C` only after a complete statement or split commands into separate invocations.

Action:

* Audit shell scripts, automation, and `mysql -e` batches.

* Fix mid-statement tokens.

### Replace deprecated `FLUSH PRIVILEGES` usage

Oracle deprecates `FLUSH PRIVILEGES` and related administration paths in MySQL 9.2. Percona Server for MySQL 9.7 includes this change.

Impact:

* `FLUSH PRIVILEGES` emits warnings.

* `FLUSH_PRIVILEGES` privilege, `mysqladmin flush-privileges`, and `mysqladmin reload` are deprecated.

Replacement:

* Follow privilege-load behavior in the MySQL Reference Manual for the target version.

Action:

* Update scripts, automation, and runbooks that still call deprecated flush commands.

## What changed in MySQL 9.7 Community Server

The following statements describe Oracle MySQL Community Server 9.7 only.

Percona Server for MySQL can differ. Read the Percona release notes for your build.

### Cross-reference MySQL 9.7 removal lists

Section 1.5 of the MySQL 9.7 Reference Manual lists no options or variables removed only in MySQL 9.7. Compare [What Is New in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html) with Section 1.5. Nutshell removal lists can repeat changes first documented in earlier MySQL 9 minor releases.

Reference: [Server options and variables added, deprecated, or removed in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/added-deprecated-removed.html).

### Toggle the hypergraph optimizer

Community Server 9.7 exposes the hypergraph optimizer through `optimizer_switch`. Scope includes session, global, persisted, and statement hints.

See [MySQL 9.7.0 release notes, Optimizer](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

### Use Clone across consecutive LTS releases

Clone supports donor and recipient pairs on consecutive LTS releases later than 9.7.0.

Read [Clone plugin limitations](https://dev.mysql.com/doc/refman/9.7/en/clone-plugin-limitations.html). Read [Remote cloning prerequisites](https://dev.mysql.com/doc/refman/9.7/en/clone-plugin-remote.html) before you rely on Clone for upgrades.

### Packaging and resource limits

Review package builds and runtime resource behavior from the following notes:

* Builds that bundle OpenSSL link a refreshed library. See packaging notes in [MySQL 9.7.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

* InnoDB reads logical CPU counts from `cpuset` cgroup limits when those limits exist. See InnoDB notes in the [MySQL 9.7.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

### External manuals for MySQL 9.7

Oracle publishes the following manuals for MySQL 9.7 Community Server, listed alphabetically by title:

* [MySQL 9.7 Reference Manual](https://dev.mysql.com/doc/refman/9.7/en/)

* [MySQL 9.7 release notes index](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/)

* [Server and status variables in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/added-deprecated-removed.html)

* [What Is New in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html)

## What changed in Percona Server for MySQL 9.7

The following changes apply to Percona Server for MySQL 9.7 only. Oracle MySQL Community Server does not include these items.

### Removed `SEQUENCE_TABLE()` in favor of `PERCONA_SEQUENCE_TABLE()`

Percona Server for MySQL 8.4 deprecated `SEQUENCE_TABLE()`. Percona Server for MySQL 9.7 removes the function.

Impact:

* Queries that call `SEQUENCE_TABLE(n)` fail on 9.7 servers.

* Stored routines, views, and applications that reference `SEQUENCE_TABLE()` break after upgrade.

Replacement:

* Use `PERCONA_SEQUENCE_TABLE(n)`. The replacement returns the same single-column virtual table.

Action:

* Search application code, stored routines, and scripts for `SEQUENCE_TABLE(` occurrences.

* Replace each call with `PERCONA_SEQUENCE_TABLE(` before you upgrade.

See [`PERCONA_SEQUENCE_TABLE(n)` function](percona-sequence-table.md) for syntax and examples.

## Pre-upgrade checklist

Run the following checks in a non-production environment first.

### Authentication and accounts

* Confirm authentication plugins and migrate accounts off `mysql_native_password`.

### Replication and GTID

* Document replication topology and Global Transaction Identifier (GTID) strategy.

* Delete removed replication and semisync variables from configuration.

* Change `replica_parallel_workers=0` to `1` or remove the setting.

### Keyring and encryption

* Migrate from `keyring_file` to a supported keyring component.

### Plugins, components, and extensions

* Delete deprecated variables, options, and plugins from configuration.

* Remove `--early-plugin-load` from option files.

* Replace Connection Control plugins with `component_connection_control`.

* Delete Version Tokens references from configuration and application code.

### InnoDB and storage

* Validate InnoDB redo and undo settings against the target manual.

* Delete removed InnoDB sizing variables from option files.

### SQL and schema behavior

* Audit application SQL for `IGNORE` with scalar subqueries, inline foreign keys, and `MD5()` or `SHA1()` usage.

### Percona-specific

* Replace `SEQUENCE_TABLE()` calls with `PERCONA_SEQUENCE_TABLE()` in application code, stored routines, and scripts.

### Final validation

* Execute test upgrades, replication failover, and backup restore drills before production cutover.

For upgrade sequencing, return to the [upgrade overview](upgrade.md) and [upgrade strategies](upgrade-strategies.md).
