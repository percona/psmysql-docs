# Upgrading using Standalone Packages

## DEB-based distributions


1. Make a full backup (or dump if possible) of your database. Move the database configuration file, `my.cnf`, to another direction to save it.


2. Stop the server with `/etc/init.d/mysql stop`.


3. Remove the installed packages with their dependencies: `apt-get autoremove percona-server percona-client`


4. Do the required modifications in the database configuration file `my.cnf`.


5. Download the following packages for your architecture:


* `percona-server-server`


* `percona-server-client`


* `percona-server-common`


* `libperconaserverclient21`

The following example will download Percona Server for MySQL 8.0.29-21 release
packages for *Debian* 11.0:

	```shell
	$ wget https://downloads.percona.com/downloads/Percona-Server-LATEST/Percona-Server-8.0.29-21/binary/debian/bullseye/x86_64/Percona-Server-8.0.29-21-rc59f87d2854-bullseye-x86_64-bundle.tar
	```

1. Unpack the bundle to get the packages: `tar xvf Percona-Server-8.0.29-21-rc59f87d2854-bullseye-x86_64-bundle.tar`

After you unpack the bundle, you should see the following packages:

```
$ ls *.deb

llibperconaserverclient21-dev_8.0.29-21-1.bullseye_amd64.deb  
percona-server-dbg_8.0.29-21-1.bullseye_amd64.deb
libperconaserverclient21_8.0.29-21-1.bullseye_amd64.deb      
percona-server-rocksdb_8.0.29-21-1.bullseye_amd64.deb
percona-mysql-router_8.0.29-21-1.bullseye_amd64.deb
percona-server-server_8.0.29-21-1.bullseye_amd64.deb
percona-server-client_8.0.29-21-1.bullseye_amd64.deb     
percona-server-source_8.0.29-21-1.bullseye_amd64.deb
percona-server-common_8.0.29-21-1.bullseye_amd64.deb     
percona-server-test_8.0.29-21-1.bullseye_amd64.deb

```


1. Install *Percona Server for MySQL*:

```
$ sudo dpkg -i *.deb
```

This will install all the packages from the bundle. Another option is to
download/specify only the packages you need for running *Percona Server for MySQL*
installation (`libperconaserverclient21_8.0.13-3.stretch_amd64.deb`,
`percona-server-client-8.0.13-3.stretch_amd64.deb`,
`percona-server-common-8.0.13-3.stretch_amd64.deb`, and
`percona-server-server-8.0.13-3.stretch_amd64.deb`. Optionally you can
install `percona-server-tokudb-8.0.13-3.stretch_amd64.deb` if you want
*TokuDB* storage engine).

**WARNING**: When installing packages manually, you must resolve all the dependencies and install missing packages yourself. At least
the following packages should be installed before installing *Percona Server for MySQL* 8.0:
\* `libmecab2`,
\* `libjemalloc1`,
\* `zlib1g-dev`,
\* `libaio1`.


1. Running the upgrade:

Starting with Percona Server 8.0.16-7, the **mysql_upgrade** is deprecated. The functionality was moved to the mysqld binary which automatically runs the upgrade process, if needed. If you attempt to run mysql_upgrade, no operation happens and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

If you are upgrading to a *Percona Server for MySQL* version before 8.0.16-7, the installation script will *NOT* run automatically **mysql_upgrade**. You must run the **mysql_upgrade** manually.

```
$ mysql_upgrade

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


1. Restart the service with `service mysql restart`.

After the service has been successfully restarted you can use the new *Percona Server for MySQL* 8.0.

## RPM-based distributions


1. Make a full backup (or dump if possible) of your database. Move the database configuration file, `my.cnf`, to another direction to save it.


2. Stop the server with `/etc/init.d/mysql stop`.


3. Check the installed packages:

	```shell
	$ rpm -qa | grep percona-server
	```
	The output could be similar to the following:
	
	```text
	percona-server-shared-8.0.29-21.1.el8.x86_64
	percona-server-shared-compat-8.0.29-21.1.el8.x86_64
	percona-server-client-8.0.29-21.1.el8.x86_64
	percona-server-server-8.0.29-21.1.el8.x86_64
	```

	You may have the `shared-compat` package, which is required for compatibility.


1. Remove the packages without dependencies with `rpm -qa | grep percona-server | xargs rpm -e --nodeps`.

	It is important that you remove the packages without dependencies as many packages may
	depend on these (as they replace `mysql`) and will be removed if omitted.
	
	Substitute `grep ‘^mysql-‘` for `grep ‘Percona-Server’` in the previous command and
	remove the listed packages.

7. Download the packages of the desired series for your architecture from the
[download page](http://www.percona.com/downloads/Percona-Server-8.0/). The
easiest way is to download the bundle which contains all the packages. The following
example will download *Percona Server for MySQL* 8.0.13-3 release packages for *CentOS* 7:

	```shell
	$ wget https://downloads.percona.com/downloads/Percona-Server-LATEST/Percona-Server-8.0.29-21/binary/redhat/8/x86_64/Percona-Server-8.0.29-21-rc59f87d2854-el8-x86_64-bundle.tar
	```


1. Unpack the bundle to get the packages

	```shell
	$ tar xvf Percona-Server-8.0.29-21-rc59f87d2854-el8-x86_64-bundle.tar
	```
	
	After you unpack the bundle, you should see the following packages: `ls \*.rpm`


1. Install *Percona Server for MySQL*:

	```shell
	$ rpm -ivh percona-server-server-8.0.29-21.1.el8.x86_64.rpm \
	> percona-server-client-8.0.29-21.1.el8.x86_64.rpm \
	> percona-server-shared-8.0.29-21.1.el8.x86_64.rpm \
	> percona-server-shared-compat-8.0.29-21.1.el8.x86_64.rpm
	```
	
	This command will install only packages required to run the *Percona Server for MySQL*
	8.0. Optionally you can install the TokuDB storage engine by
	adding the `percona-server-tokudb-8.0.13-3.el7.x86_64.rpm` to the command
	above. You can find more information on how to install and enable the *TokuDB*
	storage in the TokuDB Installation guide.


1. You can install all the packages (for debugging, testing, etc.) with `rpm -ivh \*.rpm`.

	!!! note
	
	    When manually installing packages, you must resolve all the dependencies and install missing ones.


1. Modify your configuration file, `my.cnf`, and install the plugins if necessary. If you are using the *TokuDB* storage engine you must comment out all the *TokuDB* specific variables in your configuration file(s) before starting the server, otherwise, the server will not start. *RHEL*/*CentOS* 7 automatically backs up the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After the upgrade/install process completes you can move the old configuration file back (after you remove all the unsupported system variables).


2. As the schema of the grant table has changed, the server must be started without reading them with `service mysql start`.


3. Running the upgrade:

	Starting with Percona Server 8.0.16-7, the **mysql_upgrade** is deprecated. The functionality was moved to the mysqld binary which automatically runs the upgrade process if needed. If you attempt to run mysql_upgrade, no operation happens and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)
	
	If you are upgrading to a *Percona Server for MySQL* version before 8.0.16-7, run
	**mysql_upgrade** to migrate to the new grant tables. **mysql_upgrade** will
	rebuild the required indexes and do the required modifications.


1. Restart the server with `service mysql restart`.

	After the service has been successfully restarted you can use the new *Percona Server for MySQL* 8.0.
