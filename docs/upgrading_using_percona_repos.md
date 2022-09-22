# Upgrading using the Percona repositories

Upgrading using the Percona repositories is the easiest and recommended way.

Find the instructions on how to enable the repositories in the following documents:


* Percona APT Repository


* Percona YUM Repository

## DEB-based distributions

Run the following commands as root or by using the **sudo** command.


1. Make a full backup (or dump if possible) of your database. Move the database configuration file, `my.cnf`, to another direction to save it.


2. Stop the server with `/etc/init.d/mysql stop`.

!!! note

    If you are running *Debian*/*Ubuntu* system with [systemd](http:/freedesktop.org/wiki/Software/systemd/) as the default system and service manager, you can invoke the above command with **systemctl**instead of **service**. Currently, both are supported.


1. Do the required modifications in the database configuration file `my.cnf`.


2. Install *Percona Server for MySQL*:

```shell
$ sudo dpkg -i *.deb
```


1. Enable the repository:

```shell
$ percona-release enable ps-80 release
$ apt-get update
```


1. Install the server package:

```shell
$ apt-get install percona-server-server
```


1. Install the storage engine packages.

*TokuDB* is deprecated and removed in [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.html#id3). For more information, see [TokuDB Introduction](tokudb/intro.md). If you used the *TokuDB* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-tokudb` package:

```shell
$ apt install percona-server-tokudb
```

If you used the *MyRocks* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-rocksdb` package:

```shell
$ apt install percona-server-rocksdb
```

1. Running the upgrade:

Starting with *Percona Server for MySQL* 8.0.16-7, the **mysql_upgrade** is deprecated. The functionality was moved to the mysqld binary which automatically runs the upgrade process if needed. If you attempt to run mysql_upgrade, no operation starts and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

If you are upgrading to a *Percona Server for MySQL* version before 8.0.16-7, the installation script will *NOT* run automatically **mysql_upgrade**. You must run the **mysql_upgrade** manually.

```shell
  $ mysql_upgrade
```

The output should look like the following:

```text
  Checking if update is needed.
  Checking server version.
  Running queries to upgrade MySQL server.
  Checking system database.
  mysql.columns_priv                                 OK
  mysql.db                                           OK
  mysql.engine_cost                                  OK
  ...
  Upgrade process completed successfully.
  Checking if update is needed.
```

9. Restart the service 

```shell
$ sudo systemctl restart mysqld
```

After the service has been successfully restarted you can use the new *Percona Server for MySQL* 8.0.

## RPM-based distributions

Run the following commands as root or by using the **sudo** command.


1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, for example, `my.cnf`, to another directory to save it.


2. Stop the server with `/etc/init.d/mysql stop`.

	!!! note

        If you are running *RHEL*/*CentOS* system with [systemd](http: freedesktop.org/wiki/Software/systemd/) as the default system and service manager you can invoke the above command with **systemctl** instead of **service**. Currently, both are supported.


1. Check your installed packages with `rpm -qa | grep Percona-Server`.


1. Remove the packages without dependencies. This command only removes the specified packages and leaves any dependent packages. The command does not prompt for confirmation:

	```shell
	$ rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
	```

	It is important to remove the packages without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.
	
	Substitute `grep ‘^mysql-‘` for `grep ‘Percona-Server’` in the previous command and remove the listed packages.


1. Install the `percona-server-server` package:

	```shell
	$ yum install percona-server-server
	```

1. Install the storage engine packages.

	*TokuDB* is deprecated and removed in [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.html#id3). For more information, see TokuDB Introduction. If you used *TokuDB* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-tokudb` package:

	```shell
	$ yum install percona-server-tokudb
	```

	If you used the *MyRocks* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-rocksdb` package:

	```shell
	$ apt-get install percona-server-rocksdb
	```

1. Modify your configuration file, `my.cnf`, and reinstall the plugins if necessary.

	!!! note
	
	    If you are using the *TokuDB* storage engine you must comment out all the *TokuDB* specific variables in your configuration file(s) before starting the server, otherwise, the server is not able to start. *RHEL*/*CentOS*  automatically creates a backup of the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After the upgrade/install process completes and after you have removed any unsupported system variables,  you can move the old configuration file back.


	1. Running the upgrade
	
	Starting with Percona Server 8.0.16-7, the **mysql_upgrade** is deprecated. The functionality was moved to the mysqld binary which automatically runs the upgrade process if needed. If you attempt to run mysql_upgrade, no operation happens and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)
	
	If you are upgrading to a *Percona Server for MySQL* version before 8.0.16-7, you can start the mysql service using **service mysql start**. Use **mysql_upgrade** to migrate to the new grant tables. The **mysql_upgrade** rebuilds the required indexes and does the required modifications:
	
	```shell
	$ mysql_upgrade
	```
1. Restart the service.
	
	```shell
	 $ systemctl mysql restart`.
	```
	
After the service has been successfully restarted you can use the *Percona Server for MySQL* 8.0.
