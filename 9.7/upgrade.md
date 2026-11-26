> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Upgrade from 8.4 to 9.7 overview

**Topic type**: Concept

Review [Get help from Percona](https://docs.percona.com/percona-server/9.7/get-help.md) for ways that we can work with you.

[Need expert guidance for your upgrade? Percona Support can assist](https://www.percona.com/services/expert-support/) .

## Why upgrade to Percona Server for MySQL 9.7?

Moving from 8.4 Long-Term Support (LTS) to 9.7 is more than a version bump. Updated defaults, deprecated options, and behavior changes can affect performance and break existing scripts. Treat the upgrade as a project. Plan the steps, select a method that fits your downtime window, and verify the result.

## Identify the benefits of upgrading

The following table lists the main benefits.

| Benefit                | What it means for you                                                  |
| ---------------------- | ---------------------------------------------------------------------- |
| Security fixes         | Patches close known vulnerabilities and protect data from attacks.     |
| Additional features    | Improved performance, reliability, and capability.                     |
| Less manual effort     | Automation handles routine tasks without hands-on intervention.        |
| Lower operational cost | Improved efficiency and scalability reduce day-to-day operations cost. |

## Assess the risks of staying on an older version

The following table summarizes the risks.

| Risk                       | Potential impact                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| Security exposure          | Without recent patches, attackers can breach, corrupt, or destroy data.                                |
| Feature stagnation         | Missing capabilities slow performance and increase outage frequency.                                   |
| Reduced support            | Older versions receive less vendor assistance, which lengthens troubleshooting.                        |
| Compatibility problems     | Hardware, operating system releases, or third-party applications may not work with an outdated server. |
| Unplanned upgrade pressure | Hardware or operating system failures can force a rushed upgrade and increase error risk.              |

[Concerned about these risks? Percona Support can help assess and mitigate them](https://www.percona.com/services/expert-support/) .

## Understand what the upgrade process changes

A 9.7 restart against an existing data directory runs an automatic two-phase upgrade. The phases run inside the server with no user action required. The split lets the server start with a current data dictionary even when other tasks remain.

| Phase                   | Scope                                                                                                  | What the server does                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Data dictionary upgrade | The data dictionary tables in the `mysql` schema, the Performance Schema, and the `INFORMATION_SCHEMA` | Creates dictionary tables with current definitions, copies metadata across, and atomically replaces the prior tables   |
| Server upgrade          | The system tables in `mysql`, the `sys` schema, and all user schemas                                   | Runs `CHECK TABLE ... FOR UPGRADE` on each table, repairs as needed, and stamps each table with the 9.7 version number |

The data dictionary upgrade always runs first. The server tracks two versions in the data dictionary: the data dictionary version and the server (MySQL) version. The server upgrades any part that lags the 9.7 expected versions.

The `--upgrade` server option controls the automatic upgrade behavior at startup.

| Mode             | Behavior                                                                                                                                                                                              |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AUTO` (default) | Run any out-of-date upgrade tasks across both phases                                                                                                                                                  |
| `NONE`           | Skip both phases. The server exits with an error if the data dictionary requires an upgrade                                                                                                           |
| `MINIMAL`        | Run the data dictionary upgrade only. Group Replication cannot start after a MINIMAL upgrade because system tables remain stale                                                                       |
| `FORCE`          | Run the data dictionary upgrade, then force the server upgrade across every schema. Use the mode to re-create missing system tables, such as help tables or time zone tables. Expect a longer startup |

The server upgrade locks each table during processing. Plan a maintenance window that fits the largest tables in the schema. Time zone tables are not refreshed automatically. Reload the tables with `mysql_tzinfo_to_sql` if your applications depend on time zone names.

For underlying MySQL guidance, see [What the MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/9.7/en/upgrading-what-is-upgraded.html) .

## Run the upgrade workflow

The following steps describe the upgrade workflow from 8.4 to 9.7.

### Step 1: Review what changed

Review the following resources to understand behavior changes, removed features, and toolkit impacts:

- [Percona Toolkit updates for 9.7](https://docs.percona.com/percona-server/9.7/percona-toolkit-9.7-updates.md) describes toolkit changes
- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/9.7/mysql-upgrade-paths.md) confirms supported upgrade paths
- [Keywords and Reserved Words in MySQL 9.7](https://dev.mysql.com/doc/refman/9.7/en/keywords.html) lists reserved words that break unquoted identifiers

### Step 2: Complete pre-upgrade preparation

Work through the pre-upgrade checks in the [upgrade checklist](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md). The pre-upgrade checks cover the following topics:

- Authentication methods and client compatibility
- Backup and restore procedures
- Configuration defaults
- Plugin-to-component transitions, if applicable
- Removed features and variables
- Replication script updates (`MASTER`/`SLAVE` to `SOURCE`/`REPLICA` syntax)

### Step 3: Choose your upgrade strategy

Select an upgrade method that fits your environment:

- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/9.7/mysql-upgrade-paths.md) confirms supported upgrade paths
- [Upgrade strategies](https://docs.percona.com/percona-server/9.7/upgrade-strategies.md) covers in-place, logical dump and restore, side-by-side, MySQL Clone, and rolling-replication methods

### Step 4: Run the upgrade

Follow the procedures in [Upgrade procedures for 9.7](https://docs.percona.com/percona-server/9.7/upgrade-procedures.md). The procedures cover repository-based and standalone package upgrades.

### Step 5: Validate the upgrade

Complete the post-upgrade validation in the [upgrade checklist](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md#post-upgrade-validation). The validation steps cover the following topics:

- Backup and recovery testing
- Connectivity and authentication
- Logs and metrics
- Performance baselines
- Replication health, if applicable
- Spatial index re-creation

## Reduce upgrade risk

The following tools help reduce upgrade risk before you run the production upgrade:

- A full dry-run workflow exercises every step. Create a backup, restore on 9.7, run smoke and load tests, validate, and practice rollback.
- [Percona XtraBackup](https://www.percona.com/software/mysql-database/percona-xtrabackup) creates hot backups for restore testing.
- [`pt-upgrade`](https://docs.percona.com/percona-toolkit/pt-upgrade.html) compares query plans between Percona Server 8.4 and 9.7.

These tools surface regressions early and confirm a reliable fallback plan.

## Test before production

Configure a sandbox and run the upgrade there first. The sandbox is essential for a successful migration.

Data loss risk

Percona Server for MySQL 9.7 does not provide a supported in-place downgrade to an earlier major version. Plan the rollback path before the upgrade. The most reliable rollback is to restore a backup taken before the upgrade. Logical dump and load, or replication into the older version, are also supported.

Operations in 9.7 can change data formats, which breaks binary compatibility with older versions. The safest approach is to provision a fresh server on the older version and reload your data. Do not expect a one-step undo of the upgrade. See [Downgrade options](https://docs.percona.com/percona-server/9.7/downgrade.md) for more details.

We recommend upgrading to the most recent LTS release for security, performance, and full support.

[Need personalized support during your upgrade? Contact Percona Support for a detailed migration plan](https://www.percona.com/services/expert-support/) .

## Further reading

The following Percona Server for MySQL pages cover upgrade-related topics:

- [Downgrade options](https://docs.percona.com/percona-server/9.7/downgrade.md)
- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/9.7/mysql-upgrade-paths.md)
- [Percona Toolkit updates for 9.7](https://docs.percona.com/percona-server/9.7/percona-toolkit-9.7-updates.md)
- [Upgrade checklist for 9.7](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md)
- [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md)
- [Upgrade procedures for 9.7](https://docs.percona.com/percona-server/9.7/upgrade-procedures.md)
- [Upgrade strategies](https://docs.percona.com/percona-server/9.7/upgrade-strategies.md)

### Additional MySQL documentation

The following MySQL documentation pages cover the upgrade process:

- [Before You Begin](https://dev.mysql.com/doc/refman/9.7/en/upgrade-before-you-begin.html)
- [Percona Server for MySQL 9.7 Release notes](https://docs.percona.com/percona-server/9.7/release-notes/release-notes-index.md)
- [Preparing your Installation for Upgrade](https://dev.mysql.com/doc/refman/9.7/en/upgrade-prerequisites.html)
- [Rebuilding or Repairing Tables or Indexes](https://dev.mysql.com/doc/refman/9.7/en/rebuilding-tables.html)
- [Upgrade Paths](https://dev.mysql.com/doc/refman/9.7/en/upgrade-paths.html)
- [Upgrade Troubleshooting](https://dev.mysql.com/doc/refman/9.7/en/upgrade-troubleshooting.html)
- [Upgrading MySQL](https://dev.mysql.com/doc/refman/9.7/en/upgrading.html)
- [What the MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/9.7/en/upgrading-what-is-upgraded.html)

For additional reading, review the [Percona blog](https://www.percona.com/blog/) for upgrade information.
