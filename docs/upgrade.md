# Upgrade from 8.0 to {{vers}} overview

--8<--- "get-help-snip.md"

[Need expert guidance for your upgrade? Percona Support is ready to assist you every step of the way :octicons-link-external-16:](https://www.percona.com/services/support).

<!-- Update this doc to be valid for 9.7-->

## Why upgrade to Percona Server for MySQL {{vers}} LTS

Long‑Term Support (LTS) releases focus on stability, predictable security patches, and a clearly defined maintenance horizon—essential qualities for production databases. Moving from 8.0 to 8.4 isn’t just a simple version bump: new defaults, deprecated options, and behavior changes can affect performance and break existing scripts. Treat the upgrade as a small project: plan the steps, pick the method that matches your downtime window, and verify the result.

## Benefits of upgrading to Percona Server for MySQL 8.4

| Benefit              | What it means for you                                                                 |
|-----------------------|----------------------------------------------------------------------------------------|
| Security fixes        | Patches close known vulnerabilities, keeping your data safe from attacks.             |
| New or enhanced features | Access to functionality that improves performance, reliability, and overall capability. |
| Less manual effort    | Automation tools let you handle routine tasks without hands-on intervention.          |
| Stay relevant         | The latest version helps you meet evolving customer expectations and deliver solutions more quickly. |
| Lower operational cost | Improved efficiency, and scalability translate into cheaper day-to-day operations.     |

## Risks of staying on an older version


| Risk                    | Potential impact                                                                                                                 |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Security exposure        | Without the latest patches, attackers can breach, corrupt, or destroy data, harming reputation and causing financial loss.       |
| Feature stagnation       | Missing new capabilities can lead to slower performance, lower productivity, and more frequent outages.                          |
| Reduced support          | Older versions receive less vendor assistance, resulting in longer troubleshooting times and higher support expenses.            |
| Compatibility problems   | New hardware, operating system releases, or third-party applications may not work with an outdated Percona Server version, eventually leaving the server unsupported. |
| Unplanned upgrade pressure | Unexpected hardware or OS failures can force a rushed upgrade, increasing the chance of errors.                                |

[Concerned about these risks? 
Percona Support can help assess and mitigate them :octicons-link-external-16:](https://www.percona.com/services/support).


## Upgrade workflow

Follow this step-by-step workflow to plan and execute your upgrade from 8.0 to {{vers}}:

### Step 1: Understand what's changing

Review these documents to understand breaking changes, removed features, and compatibility issues:

* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md) - Review behavioral changes, removed features, and removed variables that may affect your applications

* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md) - Verify third-party tool compatibility

* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md) - Understand configuration changes that may impact performance

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md) - Review toolkit changes if you use Percona Toolkit

### Step 2: Complete pre-upgrade preparation

Work through the pre-upgrade checks in the [upgrade checklist](./upgrade-checklist-8.4.md). This includes:

* Verifying authentication methods and client compatibility

* Updating replication scripts (MASTER/SLAVE → SOURCE/REPLICA syntax)

* Identifying and addressing removed features or variables

* Reviewing configuration defaults

* Testing backups and restore procedures

* Planning plugin-to-component transitions (if applicable)

### Step 3: Choose your upgrade strategy

Select the upgrade method that best fits your environment:

* [Upgrade strategies](./upgrade-strategies.md) - Overview of in-place, logical dump/restore, and side-by-side methods

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md) - Verify your upgrade path is supported

### Step 4: Execute the upgrade

Follow the step-by-step procedures for your chosen method:

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md) - Detailed procedures for repository-based or standalone package upgrades

### Step 5: Validate the upgrade

After completing the upgrade, complete the post-upgrade validation steps in the [upgrade checklist](./upgrade-checklist-8.4.md#post-upgrade-validation). These steps include:

* Verifying connectivity and authentication

* Checking replication health (if applicable)

* Re-creating spatial indexes

* Validating performance baselines

* Reviewing logs and metrics

* Testing backup and recovery

### Additional reference materials

* [Upgrade from plugins to components](./upgrade-components.md) - Guide for migrating from plugins to components

* [Downgrade options](./downgrade.md) - Information about downgrading if needed

### Tooling to de-risk your upgrade

* [`pt-upgrade` :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/pt-upgrade.html) – compares query plans and execution behavior between Percona Server 8.0 and {{vers}}

* [Percona XtraBackup :octicons-link-external-16:](https://www.percona.com/software/mysql-database/percona-xtrabackup)  – creates hot backups and lets you test restores without downtime.

* A full dry-run workflow - backup → restore on 8.4 → run smoke/load tests → validate → practice rollback.

These purpose‑built tools let you spot regressions early and ensure a reliable fallback plan.

## Test environment is mandatory

Set up a sandbox and run the upgrade there first. This isolated environment is essential for a successful migration. If you ever need to revert to the previous version, note that there is no fully supported in-place [downgrade procedure](./downgrade.md) from Percona Server for MySQL 8.4 to an earlier major version. The most reliable rollback method is to restore a backup taken before the upgrade, or to use a logical dump/load or replication into the older version. Because binary compatibility may not be preserved when new features or data-format changes have been applied, the safest approach is to provision a fresh instance of the older version and reload your data, rather than expecting a simple “undo” of the upgrade.

We strongly advise upgrading to the latest LTS release (Percona Server for MySQL {{vers}}) to stay secure, performant, and fully supported.


[Need personalized support during your upgrade? Contact Percona Support for a detailed migration plan :octicons-link-external-16:](https://www.percona.com/services/support).

## Further reading

Review these upgrade-related documents:

* [Upgrade checklist for {{vers}}](./upgrade-checklist-8.4.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Downgrade options](./downgrade.md)

* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)

* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md)

* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)

### Additional MySQL documentation

The following list summarizes a number of the changes in the 8.0 series and has useful guides that can help you perform a smooth upgrade. We strongly recommend reading this information:

* [Upgrading MySQL :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading.html)

* [Before You Begin :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-before-you-begin.html)

* [Upgrade Paths :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-paths.html)

* [Changes in MySQL 8.0 :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-from-previous-series.html)

* [Preparing your Installation for Upgrade :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-prerequisites.html)

* [Percona Server for MySQL {{vers}} Release notes :octicons-link-external-16:](https://docs.percona.com/percona-server/latest/release-notes/release-notes_index.html)

* [Upgrade Troubleshooting :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-troubleshooting.html)

* [Rebuilding or Repairing Tables or Indexes :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/rebuilding-tables.html)

Review other [Percona blogs :octicons-link-external-16:](https://www.percona.com/blog/) that contain upgrade information.

