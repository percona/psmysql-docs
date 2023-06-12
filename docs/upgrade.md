# Upgrade from 5.7 to 8.0 overview

Upgrading your server to 8.0 has the following benefits:

| Benefits | Description |
| --- | --- |
| Security fixes | These patches and updates protect your data from cyberattacks and address vulnerabilities or bugs in the database software.|
| New or improved features | You have access to new or improved features which enhance the functionality, performance, and availability of the database. |
| Reduced labor | You can automate some routine tasks. |
| Relevance | Your customers and stakeholders have changing needs and expectations. Using the latest version can help to deliver solutions faster. |
| Reduced operational costs | An upgraded database server can help reduce your operational costs because the server has improved efficiency and scalability. |

Not upgrading your database can have the following risks:

| Risks | Description |
| --- | --- |
| Security risks | Your database server is vulnerable to cyberattacks because you do not receive security fixes. These attacks can result in data breaches, data loss, and data corruption. These actions can harm the organization's reputation and lose money. |
| Service risks | You do not benefit from new or improved features. This risk may cause poor user experience, reduced productivity, and increased downtime. |
| Support risks | You are limited in support access. This risk can result in longer resolution times, unresolved issues, and higher support costs. |
| Compatibility risks | You can experience compatibility issues with hardware, operating system, or applications since the older version is not supported on newer platforms. At some point, the database server is no longer supportable. |
| Failure risk | A failure in either hardware, operating system or application may force an upgrade at the wrong time. |


Create a test environment to verify the upgrade before you upgrade the production servers. The test environment is crucial to the success of the upgrade. There is no supported [downgrade procedure](./downgrade.md). You can try to [replicate from an 8.0 version to 5.7](https://www.percona.com/blog/replicating-mysql-8-0-mysql-5-7/) or restore a backup.

[Several tools](./upgrade-pt.md) in the [Percona Toolkit](https://docs.percona.com/percona-toolkit/) can help with the upgrade process.

We recommend upgrading to the latest version. The following topics describe the major changes from 5.7 to 8.0:

* [General changes](./upgrade-changes-general.md)
* [InnoDB changes](./upgrade-changes-innodb.md)
* [Security and account management changes](./upgrade-changes-secure.md)
* [Deprecated in 8.0](./upgrade-changes-deprecated.md)
* [Removed in 8.0](./upgrade-changes-removed.md)

Review the documentation for other changes between 5.7 to 8.0.

Review [Upgrade Strategies](./upgrade-strategies.md) for an overview of the major strategies.

The following list summarizes a number of the changes in the 8.0 series and has useful guides that can help you perform a smooth upgrade. We strongly recommend reading this information:

* [Upgrading MySQL](https://dev.mysql.com/doc/refman/8.0/en/upgrading.html)

* [Before You Begin](https://dev.mysql.com/doc/refman/8.0/en/upgrade-before-you-begin.html)

* [Upgrade Paths](https://dev.mysql.com/doc/refman/8.0/en/upgrade-paths.html)

* [Changes in MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.html)

* [Preparing your Installation for Upgrade](https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.html)

* [MySQL 8 Minor Version Upgrades Are ONE-WAY Only](https://www.percona.com/blog/2020/01/10/mysql-8-minor-version-upgrades-are-one-way-only/)

* [Percona Utilities That Make Major MySQL Version Upgrades Easier](https://www.percona.com/blog/percona-utilities-that-make-major-mysql-version-upgrades-easier/)

* [Percona Server for MySQL 8.0 Release notes](https://docs.percona.com/percona-server/latest/release-notes/release-notes_index.html)

* [Upgrade Troubleshooting](https://dev.mysql.com/doc/refman/8.0/en/upgrade-troubleshooting.html)

* [Rebuilding or Repairing Tables or Indexes](https://dev.mysql.com/doc/refman/8.0/en/rebuilding-tables.html)

Review other [Percona blogs](https://www.percona.com/blog/) that contain upgrade information.

Implemented in release Percona Server for MySQL 8.0.15-5, *Percona Server for MySQL* uses the upstream
implementation of binary log file encryption and relay log file encryption.


