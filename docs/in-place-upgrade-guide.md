# Percona Server for MySQL in-place upgrade guide: from 5.7 to 8.0

!!! important

    An in-place upgrade is not recommended. Use a [replication upgrade](https://docs.percona.com/percona-xtradb-cluster/8.0/howtos/upgrade_guide.html).

An in-place upgrade involves shutting down the 5.7 server, and replacing the server binaries, or packages, with new ones. At this point the new server version can be started on the existing data directory. If the new version is less than 8.0.16, you should run `mysql_upgrade`. Note that the server should be configured to perform a slow shutdown by setting `innodb_fast_shutdown=0` prior to shutdown. While an in-place upgrade may not be suitable for all environments, especially those environments with many variables to consider, the upgrade should work in most cases.

The benefits are:

* Less additional infrastructure cost compared to a new environment, but nodes must be tested.
* An upgrade can be completed over weeks with cool-down periods between reader node upgrades.
* Requires a failover of production traffic, and for minimal downtime you must have good high-availability tools.

Before you start the upgrade process, it is recommended to make a full backup of your database.
Copy the database configuration file, for example, `my.cnf`, to another directory to save it.

!!! warning

    Do not upgrade from 5.7 to 8.0 on a crashed instance. If the server instance has crashed, run the crash recovery before proceeding with the upgrade.

The `encrypt-binlog` variable is
removed, and the related command-line option `–encrypt-binlog` is not
supported. It is important to remove the `encrypt-binlog` variable from your
configuration file before you attempt to upgrade either from another release
in the *Percona Server for MySQL* 8.0 series or from *Percona Server for MySQL* 5.7.
Otherwise, a server boot error is generated and reports an unknown
variable.

The implemented binary log file encryption is compatible with the older
format. The encrypted binary log file used in a previous version of MySQL 8.0
series or Percona Server for MySQL series is supported.



You can select one of the following ways to upgrade *Percona Server for MySQL* from 5.7 to 8.0:

* Upgrade with the Percona repositories

* Upgrade from systems that use the MyRocks or TokuDB Storage Engine and Partitioned Tables

* Upgrade with standalone packages
