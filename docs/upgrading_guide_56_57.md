# Percona Server In-Place Upgrading Guide: From 5.6 to 5.7

In-place upgrades are those which are done using the existing data in the server. Generally speaking, this is stopping the server, installing the new server and starting it with the same data files. While they may not be suitable for high-complexity environments, they may be adequate for many scenarios.

The following is a summary of the more relevant changes in the 5.7 series. It’s strongly recommended to that you read the following guides as they contain the list of incompatible changes that could cause automatic upgrade to fail:

> 
> * [Changed in Percona Server 5.7](changed_in_57.md)


> * [Upgrading MySQL](http://dev.mysql.com/doc/refman/5.7/en/upgrading.html)


> * [Upgrading from MySQL 5.6 to 5.7](http://dev.mysql.com/doc/refman/5.7/en/upgrading-from-previous-series.html)

!!! warning

    Upgrade from 5.6 to 5.7 on a crashed instance is not recommended. If the server instance has crashed, crash recovery should be run before proceeding with the upgrade.


