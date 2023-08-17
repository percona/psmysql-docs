# Upgrade using the Percona repositories

Upgrading using the Percona repositories is the easiest and recommended way.

Find the instructions on how to enable the repositories in the following documents:

* [Percona APT Repository](apt-repo.md)

* [Percona RPM Repository](yum-repo.md)


## DEB-based distributions

Run the following commands as root or by using the **sudo** command.


1. Make a full backup (or dump if possible) of your database. Move the database configuration file, `my.cnf`, to another direction to save it.


2. Stop the server with `/etc/init.d/mysql stop`.

    !!! note

        If you are running *Debian*/*Ubuntu* system with [systemd](https:/freedesktop.org/wiki/Software/systemd/) as the default system and service manager, you can invoke the above command with **systemctl**instead of **service**. Currently, both are supported.


3. Do the required modifications in the database configuration file `my.cnf`.


4. Install *Percona Server for MySQL*:

    ```{.bash data-prompt="$"}
    $ sudo dpkg -i *.deb
    ```

5. Enable the repository:

    ```{.bash data-prompt="$"}
    $ percona-release enable ps-80 release
    $ apt-get update
    ```

6. Install the server package:

    ```{.bash data-prompt="$"}
    $ apt-get install percona-server-server
    ```

7. Install the storage engine packages.

    *TokuDB* is deprecated and removed in [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md#id3). For more information, see [TokuDB Introduction](tokudb-intro.md). If you used the *TokuDB* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-tokudb` package:

    ```{.bash data-prompt="$"}
    $ apt install percona-server-tokudb
    ```

    If you used the *MyRocks* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-rocksdb` package:

    ```{.bash data-prompt="$"}
    $ apt install percona-server-rocksdb
    ```

8. Running the upgrade:

    Starting with *Percona Server for MySQL* 8.0.16-7, the **mysql_upgrade** is deprecated. The functionality was moved to the mysqld binary which automatically runs the upgrade process if needed. If you attempt to run mysql_upgrade, no operation starts and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

    If you are upgrading to a *Percona Server for MySQL* version before 8.0.16-7, the installation script will *NOT* run automatically **mysql_upgrade**. You must run the **mysql_upgrade** manually.

    ```{.bash data-prompt="$"}
    $ mysql_upgrade
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
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

    ```{.bash data-prompt="$"}
    $ sudo systemctl restart mysqld
    ```
After the service has been successfully restarted you can use the new *Percona Server for MySQL* 8.0.

## RPM-based distributions

Run the following commands as root or by using the **sudo** command.


1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, for example, `my.cnf`, to another directory to save it.


2. Stop the server with `/etc/init.d/mysql stop`.

	!!! note

        If you are running *RHEL*/*CentOS* system with [systemd](https:freedesktop.org/wiki/Software/systemd/) as the default system and service manager you can invoke the above command with **systemctl** instead of **service**. Currently, both are supported.


3. Check your installed packages with `rpm -qa | grep Percona-Server`.


4. Remove the packages without dependencies. This command only removes the specified packages and leaves any dependent packages. The command does not prompt for confirmation:

	```{.bash data-prompt="$"}
	$ rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
	```

	It is important to remove the packages without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.
	
	Substitute `grep ‘^mysql-‘` for `grep ‘Percona-Server’` in the previous command and remove the listed packages.


5. Install the `percona-server-server` package:

	```{.bash data-prompt="$"}
	$ yum install percona-server-server
	```

6. Install the storage engine packages.

	*TokuDB* is deprecated and removed in [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md#id3). For more information, see TokuDB Introduction. If you used *TokuDB* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-tokudb` package:

	```{.bash data-prompt="$"}
	$ yum install percona-server-tokudb
	```

	If you used the *MyRocks* storage engine in *Percona Server for MySQL* 5.7, install the `percona-server-rocksdb` package:

	```{.bash data-prompt="$"}
	$ apt-get install percona-server-rocksdb
	```

7. Modify your configuration file, `my.cnf`, and reinstall the plugins if necessary.

	!!! note
	
	    If you are using the *TokuDB* storage engine you must comment out all the *TokuDB* specific variables in your configuration file(s) before starting the server, otherwise, the server is not able to start. *RHEL*/*CentOS*  automatically creates a backup of the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After the upgrade/install process completes and after you have removed any unsupported system variables,  you can move the old configuration file back.


8. Running the upgrade
	
	Starting with Percona Server 8.0.16-7, the **mysql_upgrade** is deprecated. The functionality was moved to the mysqld binary which automatically runs the upgrade process if needed. If you attempt to run mysql_upgrade, no operation happens and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)
	
	If you are upgrading to a *Percona Server for MySQL* version before 8.0.16-7, you can start the mysql service using **service mysql start**. Use **mysql_upgrade** to migrate to the new grant tables. The **mysql_upgrade** rebuilds the required indexes and does the required modifications:
	
	```{.bash data-prompt="$"}
	$ mysql_upgrade
	```

9. Restart the service.
	
	```{.bash data-prompt="$"}
	$ systemctl mysql restart`.
	```
	
After the service has been successfully restarted you can use the *Percona Server for MySQL* 8.0.
