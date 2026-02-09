# MySQL 9.7 technical migration overview

MySQL 9 minor releases remove legacy plugins and change defaults for security and replication. Database administrators must align accounts, configuration files, and replication topology before they upgrade.

Use [upgrade overview](upgrade.md), [installation](installation.md), and [upgrade procedures](upgrade-procedures.md) with the following migration overview when you upgrade.
You move from MySQL 8.4 Long-Term Support (LTS) toward Percona Server for MySQL 9.7.
Percona behavior can differ from Oracle MySQL Community Edition.
Read [release notes](release-notes/release-notes-index.md) for your build.

The following sections group changes by functional area.
Percona Server for MySQL 9.7 is the first public MySQL 9 LTS release covered here.
Each section states impact, replacement options, and required actions where they apply.

## Review breaking changes before upgrade

Address the following items before you upgrade production servers.

High-impact items:

* `mysql_native_password` authentication plugin is removed.

* Migrate all accounts to a supported plugin (for example, `caching_sha2_password`) before upgrade, or authentication fails.

* `gtid_mode` and `enforce_gtid_consistency` default to `ON`.

* You must set Global Transaction Identifier (GTID) options explicitly when replication still uses file names and positions only.

* `keyring_file` plugin is removed.

* Migrate to a supported keyring component before upgrade, or the server may fail to start.

## Authentication and accounts

### Migrate off `mysql_native_password`

Percona Server for MySQL 9.7 removes the `mysql_native_password` plugin and related server options.

Impact:

* Accounts that still use `mysql_native_password` cannot authenticate against the upgraded server.

* Clients without `CLIENT_PLUGIN_AUTH` support receive rejection during handshake.

* Server removes `--mysql-native-password`, `--mysql-native-password-proxy-users`, and `default_authentication_plugin`.

* Removal applies to the server process only.

* Client libraries can still use `mysql_native_password` against older MySQL 8.0 or 5.7 servers.

Replacement:

* Use `caching_sha2_password` or another supported authentication plugin.

* The default plugin for accounts you create is `caching_sha2_password` in MySQL 8.4 and later.

Action:

* List accounts and applications that still reference `mysql_native_password`.

* Migrate each account to a supported plugin before you upgrade the server.

Example statement:

```sql
ALTER USER '<USERNAME>'@'<HOST>'
IDENTIFIED WITH caching_sha2_password BY '<PASSWORD>';
```

* Delete references to removed authentication options and variables from configuration files and scripts before upgrade.

### Configure caching SHA-2 storage format

The following variables control caching SHA-2 password storage format options in MySQL 9.7.

* `caching_sha2_password_storage_format` and `caching_sha2_password_enforce_storage_format` support PBKDF2 storage with `caching_sha2_password`.

* See [Caching SHA-2 pluggable authentication](https://dev.mysql.com/doc/refman/9.7/en/caching-sha2-pluggable-authentication.html).

### Replace deprecated `FLUSH PRIVILEGES` usage

MySQL 9.7 deprecates `FLUSH PRIVILEGES` and related administration paths.

Impact:

* `FLUSH PRIVILEGES` emits warnings.

* `FLUSH_PRIVILEGES` privilege, `mysqladmin flush-privileges`, and `mysqladmin reload` are deprecated.

Replacement:

* Follow privilege-load behavior in the MySQL Reference Manual for the target version.

Action:

* Update scripts, automation, and runbooks that still call deprecated flush commands.

## Replication and Global Transaction Identifiers (GTID)

### Configure GTID defaults

Replication behavior depends on Global Transaction Identifier (GTID) variables.
Incorrect defaults cause most upgrade failures in mixed topologies.

Impact:

* `gtid_mode` defaults to `ON` in MySQL 9.7.

* `enforce_gtid_consistency` defaults to `ON`.

* Non-GTID replication can fail to start unless you set variables explicitly.

* `enforce_gtid_consistency=ON` blocks certain non-deterministic statements inside transactions.

* Some packages apply `OFF_PERMISSIVE` transition states during upgrade.

* Until GTID migration completes, set explicit `gtid_mode=OFF` and `enforce_gtid_consistency=OFF` when needed.

Replacement:

* Adopt GTID-based replication, or set GTID variables off before you start the upgraded server.

Action:

* If you do not use GTID yet, add the following lines to configuration before upgrade:

```text
gtid_mode=OFF
enforce_gtid_consistency=OFF
```

* Review application SQL and stored programs for `enforce_gtid_consistency=ON` violations.

### Set `replica_parallel_workers` minimum

MySQL 9.7 disallows `replica_parallel_workers=0`.

Impact:

* Minimum value is `1`.

* Default became `4` in MySQL 8.0.30 and later.

* Only setups that set `0` for single-threaded apply encounter the minimum.

Replacement:

* Use `replica_parallel_workers=1` for single-threaded apply, or omit the variable to keep the default.

Action:

* Change `replica_parallel_workers=0` to `1`, or delete the line to restore the default, before upgrade.

### Replace removed Group Replication and semisync variables

MySQL 9.7 removes several replication variables.
Semisynchronous replication moves from plugins to components.

Impact:

* `group_replication_allow_local_lower_version_join` is removed.

* `replica_parallel_type` and `slave_parallel_type` are removed.

* Legacy semisynchronous plugins `semisync_master.so` and `semisync_slave.so` are removed.

* `rpl_semi_sync_*` variables are removed.

* Semisynchronous replication remains available through replacement components.

Replacement:

* Use Semisynchronous Replication Source and Replica components for semisync behavior.

Action:

* Delete removed variables from configuration and monitoring.

* Install and configure semisync components as documented in the MySQL Reference Manual.

### Configure replication across versions

Community Server 9.7 exposes the following replication-related settings.

* `replica_allow_higher_version_source` controls replication from a higher-version source to a lower replica.

* Use `replica_allow_higher_version_source` during staged upgrades.

* See [Replication options (replica)](https://dev.mysql.com/doc/refman/9.7/en/replication-options-replica.html).

* See [MySQL 9.7.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

* `object_policy_flush_interval_seconds` refreshes the object policy cache on secondaries and replicas.

* See Section 1.5 in the MySQL 9.7 manual.

## Plugins and components

### Remove `--early-plugin-load`

MySQL 9.7 removes the `--early-plugin-load` server option.

Impact:

* Configuration files that still contain `--early-plugin-load` can prevent startup.

Replacement:

* Load functionality through supported components and the component manifest (for example, `mysqld.my`).

Action:

* Search configuration paths for `--early-plugin-load` and delete those lines.

* Move required behavior to components when the manual documents migration steps.

### Migrate from `keyring_file` to `component_keyring_file`

Migration requires a component manifest.
You cannot convert the plugin with a single `my.cnf` edit.

Impact:

* MySQL 9.7 omits the `keyring_file` plugin binary.

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

### Migrate Connection Control to the component

Connection Control plugins are removed from MySQL 9.7.

Impact:

* Both Connection Control plugins leave the distribution.

Replacement:

* Install `component_connection_control` through `INSTALL COMPONENT` syntax.

Action:

* Replace plugins with the component.

* Update monitoring queries that read deprecated Information Schema tables.

### Remove Version Tokens usage

MySQL 9.7 removes the Version Tokens plugin.

Impact:

* Functions, privileges, and variables for Version Tokens disappear with the plugin.

Replacement:

* Oracle provides no direct substitute inside the server.

Action:

* Delete Version Tokens references from configuration and application code before upgrade.

### Install components that Community Edition includes

Community Server 9.7 includes components that once required MySQL Enterprise Edition only.

The following list orders components alphabetically by name:

* Group Replication Flow Control Statistics component

* Group Replication Primary Election component

* Group Replication Resource Manager component

* Replication Applier Metrics component

* Telemetry component

See [MySQL 9.7.0 release notes, Component notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

## InnoDB and storage configuration

### Remove deprecated InnoDB variables

MySQL 9.7 removes legacy InnoDB sizing variables.
Redo and undo sizing follow variables documented for MySQL 9.7.

Impact:

The following variables are removed:

* `innodb_log_file_size`

* `innodb_log_files_in_group`

* `innodb_undo_tablespaces`

Replacement:

| Removed variable | MySQL 9.7 approach |
| --- | --- |
| `innodb_log_file_size` | `innodb_redo_log_capacity` |
| `innodb_log_files_in_group` | Automatic management |
| `innodb_undo_tablespaces` | Automatic undo management |

Action:

* Delete removed variables from option files.

* Read redo and undo chapters in the MySQL Reference Manual for the target version.

### Configure InnoDB redo writers and binary log history

Default behavior depends on `innodb_log_writer_threads`:

* When binary logging is off, default follows logical CPU count.

* When binary logging is on, defaults follow CPU count rules documented for MySQL 9.7.

The `binlog_transaction_dependency_history_size` default is 1,000,000 in MySQL 9.7.

The maximum is 10,000,000 in MySQL 9.7.

Existing explicit values stay unchanged.

### Read CPU limits from cgroup `cpuset`

InnoDB reads logical CPU counts from `cpuset` cgroup limits when those limits exist.

* See InnoDB notes in [MySQL 9.7.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

## SQL, schemas, and client behavior

### Fix `IGNORE` with scalar subqueries

`IGNORE` no longer hides `ER_SUBQUERY_NO_1_ROW` when a scalar subquery returns more than one row.

Impact:

* `INSERT IGNORE`, `UPDATE IGNORE`, and `DELETE IGNORE` can fail where they succeeded before.

Replacement:

* Restrict scalar subqueries to zero or one row.

Action:

* Audit application SQL and stored routines; correct logic or remove unsafe `IGNORE` usage.

### Enforce inline foreign keys

MySQL 9.7 enforces inline foreign key syntax that older releases parsed but ignored.

Impact:

* Invalid inline foreign keys become errors instead of silent acceptance.

Action:

* Compare schemas and generated Data Definition Language (DDL) against intended constraints.

### Review foreign key cascade handling

The following variable toggles foreign key cascade execution in MySQL 9.7.

* `enable_cascade_triggers` controls foreign key cascade execution path in MySQL 9.7.

* Oracle deprecated the variable in the same release.

* Follow the MySQL 9.7 manual for supported behavior after upgrade.

### Plan migration from `MD5()` and `SHA1()` in SQL

MySQL 9.7 deprecates the `MD5()` and `SHA1()` SQL functions.
Legacy applications that compute hashes in SQL often break first.

Impact:

* Deprecation applies to the SQL functions `MD5()` and `SHA1()`.

* Functions still run, but Oracle may remove them in a later release.

* PHP and Java stacks that call these functions in SQL need review.

Replacement:

* Call `SHA2()` in SQL, or compute hashes in the application.

Action:

* Audit procedures, triggers, and application SQL.

* Migrate off `MD5()` and `SHA1()` when compliance allows.

### Adjust mysql client `\G` and `\C` usage

The mysql client accepts `\G` (vertical output) and `\C` (clear) only at the end of a statement.

Impact:

* Scripts that place `\G` or `\C` in the middle of a statement can fail or print unexpected output.

Replacement:

* Place `\G` and `\C` only after a complete statement, or split commands into separate invocations.

Action:

* Audit shell scripts, automation, and `mysql -e` batches; fix mid-statement tokens.

### Recognize atomic DDL for databases

`CREATE DATABASE` and `DROP DATABASE` run as atomic, crash-safe operations.

Impact:

* Correct usage does not change; behavior improves for crash recovery.

Action:

* No change required.

### Run Data Manipulation Language (DML) on JSON duality views

Community Server 9.7 supports `INSERT`, `UPDATE`, and `DELETE` on JSON duality views.

See [DML operations on JSON duality views](https://dev.mysql.com/doc/refman/9.7/en/json-duality-views-updatable.html).

### Toggle the hypergraph optimizer

Community Server 9.7 exposes the hypergraph optimizer through `optimizer_switch`.

Scope includes session, global, persisted, and statement hints.

See [MySQL 9.7.0 release notes, Optimizer](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

## Clone, packaging, and Oracle documentation

### Use Clone across consecutive LTS releases

Clone supports donor and recipient pairs on consecutive LTS releases above 9.7.0.

Read [Clone plugin limitations](https://dev.mysql.com/doc/refman/9.7/en/clone-plugin-limitations.html).

Read [Remote cloning prerequisites](https://dev.mysql.com/doc/refman/9.7/en/clone-plugin-remote.html) before you rely on Clone for upgrades.

### Review OpenSSL packaging

Builds that bundle OpenSSL link a refreshed library.

* See packaging notes in [MySQL 9.7.0 release notes](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/news-9-7-0.html).

### Reconcile Oracle documentation about removals

Section 1.5 of the MySQL 9.7 Reference Manual lists zero options or variables removed only in MySQL 9.7.

Compare [What Is New in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html) with Section 1.5.

Nutshell removal lists can repeat items that Oracle documented in unreleased intermediate versions.

Reference: [Server options and variables added, deprecated, or removed in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/added-deprecated-removed.html).

### External manuals for MySQL 9.7

Oracle publishes the following manuals for MySQL 9.7 Community Server in alphabetical order by title.

* [MySQL 9.7 Reference Manual](https://dev.mysql.com/doc/refman/9.7/en/)

* [MySQL 9.7 release notes index](https://dev.mysql.com/doc/relnotes/mysql/9.7/en/)

* [Server and status variables in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/added-deprecated-removed.html)

* [What Is New in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/mysql-nutshell.html)

## Defaults and tuning guidance

Global Transaction Identifier (GTID) defaults differ from MySQL 8.4.

| Variable | Default in MySQL 9.7 | Default in MySQL 8.4 |
| --- | --- | --- |
| `gtid_mode` | `ON` | `OFF` |
| `enforce_gtid_consistency` | `ON` | `OFF` |

## Pre-upgrade checklist

Run the following checks in a non-production environment first.

* Delete deprecated variables, options, and plugins from configuration.

* Confirm authentication plugins and migrate accounts off `mysql_native_password`.

* Document replication topology and Global Transaction Identifier (GTID) strategy.

* Validate InnoDB redo and undo settings against the target manual.

* Execute test upgrades, replication failover, and backup restore drills before production cutover.

For upgrade sequencing, return to [upgrade overview](upgrade.md) and [upgrade strategies](upgrade-strategies.md).
