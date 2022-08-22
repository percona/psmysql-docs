
# Upgrading using the Percona repositories

The easiest and recommended way of installing - where possible - is by using the Percona repositories.


## `DEB`-based distributions

**NOTE**: Following commands will need to be run either as a root user or with **sudo**.

Having done the full backup (or dump if possible), stop the server:

```shell
$ service mysql stop
```

and proceed to do the modifications needed in your configuration file, as explained at the beginning of this guide.

**NOTE**: If you’re running *Debian*/*Ubuntu* system with [systemd](http://freedesktop.org/wiki/Software/systemd/) as the default system and service manager you can invoke the above command with **systemctl** instead of **service**. Currently, both are supported.

Then install the new server with:

```shell
$ apt install percona-server-server-5.7
```

If you’re using Percona Server for MySQL 5.6 with TokuDB you’ll need to specify the TokuDB package as well:

```shell
$ apt install percona-server-server-5.7 percona-server-tokudb-5.7
```

The installation script will *NOT* run automatically **mysql_upgrade** as it was the case in previous versions. You’ll need to run the command manually and restart the service after it’s finished.

```shell
$ mysql_upgrade
```
The output should be similar to the following:

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
Restart the service.

```shell
$ service mysql restart
```

Note that this procedure is the same for upgrading from MySQL 5.6 or 5.7 to Percona Server for MySQL 5.7.

## `RPM`-based distributions

**NOTE**: Following commands will need to be run either as a root user or with **sudo**.

Having done the full backup (and dump if possible), stop the server:

**NOTE**: If you’re running *RHEL*/*CentOS* system with [systemd](http://freedesktop.org/wiki/Software/systemd/) as the default system and service manager you can invoke the above command with **systemctl** instead of **service**. Currently, both are supported.

```shell
$ service mysql stop
```

Check your installed packages with:

```shell
$ rpm -qa | grep Percona-Server
```

The output should be similar to the following: 

```text
Percona-Server-shared-56-5.6.28-rel76.1.el7.x86_64
Percona-Server-server-56-5.6.28-rel76.1.el7.x86_64
Percona-Server-devel-56-5.6.28-rel76.1.el7.x86_64
Percona-Server-client-56-5.6.28-rel76.1.el7.x86_64
Percona-Server-test-56-5.6.28-rel76.1.el7.x86_64
Percona-Server-56-debuginfo-5.6.28-rel76.1.el7.x86_64
```

After checking, proceed to remove them without dependencies:

```shell
$ rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
```

It is important that you remove it without dependencies as many 
packages may depend on these packages, since they replace `mysql`, and 
will be 
removed if omitted.

Note that this procedure is the same for upgrading from MySQL 5.6 or 5.7 to Percona Server for MySQL 5.7: just grep `'^mysql-'` instead of `Percona-Server` and remove them.

Install `Percona-Server-server-57`:

```shell
$ yum install Percona-Server-server-57
```

Percona Server for MySQL 5.6 with TokuDB, specify the TokuDB package as 
well when doing the upgrade:

```shell
$ yum install Percona-Server-server-57 Percona-Server-tokudb-57
```

Once installed, proceed to modify your configuration file - `my.cnf` - and reinstall the plugins if necessary.

**NOTE**: If you’re using TokuDB storage engine you’ll need to comment out all the TokuDB specific variables in your configuration file(s) before starting the server, otherwise server won’t be able to start. *RHEL*/*CentOS* 7 automatically backs up the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After upgrade/install process completes you can move the old configuration file back (after you remove all the unsupported system variables).

You can now start the `mysql` service:

```shell
$ service mysql start
```

and use `mysql_upgrade` to migrate to the new grant tables, it will rebuild the indexes needed and do the modifications needed:

**NOTE**: If you’re using TokuDB storage engine, re-enable the storage 
engine plugin by running the: `ps-admin --enable-tokudb` before running `mysql_upgrade` otherwise you’ll get errors.

```shell
$ mysql_upgrade
```

The output should be similar to the following:

```text
Checking if update is needed.
Checking server version.
Running queries to upgrade MySQL server.
Checking system database.
mysql.columns_priv                                 OK
mysql.db                                           OK
...
Upgrade process completed successfully.
Checking if update is needed.
```

Once this is done, just restart the server as usual:

```shell
$ service mysql restart
```

After the service has been successfully restarted you can use the new Percona Server for MySQL 5.7.
