# Downgrade Percona Server for MySQL

A downgrade from Percona Server for MySQL 8.0 to 5.7 is not supported.

A downgrade from a Percona Server for MySQL 8.0 version to an earlier 8.0 version is not supported. 

Percona does not test a downgrade operation between versions.

Each release of Percona Server for MySQL 8.0 can contain significant changes that are not backward-compatible. Restoring a backup to an earlier version may fail, for example, if your code uses a feature that does not exist in an earlier version.

Before you [upgrade to the latest release](./upgrade.md), do the following:

* Make a full backup of your data and test the backup

* Thoroughly test in a staging environment

[MySQL 8 Minor Version Upgrades Are ONE-WAY Only](https://www.percona.com/blog/2020/01/10/mysql-8-minor-version-upgrades-are-one-way-only/)