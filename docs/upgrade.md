# Upgrade from 8.0 to {{vers}} overview

Upgrading your server to {{vers}} has the following benefits:

| Benefits | Description |
| --- | --- |
| Security fixes | These patches and updates protect your data from cyberattacks and address vulnerabilities or bugs in the database software.|
| New or improved features | You have access to new or improved features that enhance the functionality, performance, and availability of the database. |
| Reduced labor | You can automate some routine tasks. |
| Relevance | Your customers and stakeholders have changing needs and expectations. Using the latest version can help to deliver solutions faster. |
| Reduced operational costs | An upgraded database server can help reduce your operational costs because the server has improved efficiency and scalability. |

Not upgrading your database can have the following risks:

| Risks | Description |
| --- | --- |
| Security risks | Your database server is vulnerable to cyberattacks because you do not receive security fixes. These attacks can result in data breaches, data loss, and data corruption. These actions can harm the organization's reputation and lose money. |
| Service risks | You do not benefit from new or improved features. This risk may cause poor user experience, reduced productivity, and increased downtime. |
| Support risks | You are limited in support access. This risk can result in longer resolution times, unresolved issues, and higher support costs. |
| Compatibility risks | You can experience compatibility issues with hardware, operating systems, or applications since the older version is not supported on newer platforms. At some point, the database server is no longer supportable. |
| Failure risk | A failure in either hardware, operating system, or application may force an upgrade at the wrong time. |

Create a test environment to verify the upgrade before you upgrade the production servers. The test environment is crucial to the success of the upgrade. There is no supported [downgrade procedure](./downgrade.md). You can try to replicate from an {{vers}} version to an 8.0 version or restore a backup.

[Several tools](The `pt-upgrade` tool](https://docs.percona.com/percona-toolkit/pt-upgrade.html) in the [Percona Toolkit](https://docs.percona.com/percona-toolkit/) can help with the upgrade process.

We recommend upgrading to the latest version.

Review the documentation for other changes between 8.0 to {{vers}}.

Review [Upgrade Strategies](./upgrade-strategies.md) for an overview of the major strategies.

The following list summarizes a number of the changes in the 8.0 series and has useful guides that can help you perform a smooth upgrade. We strongly recommend reading this information:

* [Upgrading MySQL](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading.html)

* [Before You Begin](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-before-you-begin.html)

* [Upgrade Paths](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-paths.html)

* [Changes in MySQL 8.0](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-from-previous-series.html)

* [Preparing your Installation for Upgrade](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-prerequisites.html)

* [Percona Server for MySQL {{vers}} Release notes](https://docs.percona.com/percona-server/latest/release-notes/release-notes_index.html)

* [Upgrade Troubleshooting](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-troubleshooting.html)

* [Rebuilding or Repairing Tables or Indexes](https://dev.mysql.com/doc/refman/{{vers}}/en/rebuilding-tables.html)

Review other [Percona blogs](https://www.percona.com/blog/) that contain upgrade information.
