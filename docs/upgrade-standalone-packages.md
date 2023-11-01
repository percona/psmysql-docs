# Upgrade using Standalone Packages


Make a full backup (or dump if possible) of your database. Move the database configuration file, `my.cnf`, to another direction to save it. Stop the server with `/etc/init.d/mysql stop`.

=== "Debian-derived distribution"

    1. Remove the installed packages with their dependencies: `sudo apt autoremove percona-server percona-client`

    2. Do the required modifications in the database configuration file `my.cnf`.

    3. Download the following packages for your architecture:

        * `percona-server-server`

        * `percona-server-client`

        * `percona-server-common`

        * `libperconaserverclient21`

        The following example will download Percona Server for MySQL 8.0.29-21 release
        packages for Debian 11.0:

        ```{.bash data-prompt="$"}
        $ wget https://downloads.percona.com/downloads/Percona-Server-LATEST/Percona-Server-8.0.29-21/binary/debian/bullseye/x86_64/Percona-Server-8.0.29-21-rc59f87d2854-bullseye-x86_64-bundle.tar
        ```

    4. Unpack the bundle to get the packages: `tar xvf Percona-Server-8.0.29-21-rc59f87d2854-bullseye-x86_64-bundle.tar`.
    
        After you unpack the bundle, you should see the following packages:

        ```{.bash data-prompt="$"}
        $ ls *.deb
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
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

    5. Install Percona Server for MySQL:

        ```{.bash data-prompt="$"}
        $ sudo dpkg -i *.deb
        ```

        This command installs the packages from the bundle. Another option is to
        download or specify only the packages you need for running Percona Server for MySQL
        installation (`libperconaserverclient21-dev_8.0.29-21-1.bullseye_amd64.deb`,
        `percona-server-client-8.0.29-21-1.bullseye_amd64.deb`,
        `percona-server-common-8.0.29-21-1.bullseye_amd64.deb`, and
        `percona-server-server-8.0.29-21-1.bullseye_amd64.deb`. 

        !!! warning

            When installing packages manually, you must resolve all the dependencies and install missing packages yourself. At least
            the following packages should be installed before installing Percona Server for MySQL 8.0:
            \* `libmecab2`,
            \* `libjemalloc1`,
            \* `zlib1g-dev`,
            \* `libaio1`.

    6. Running the upgrade:

        Starting with `Percona Server 8.0.16-7`, `mysql_upgrade` is deprecated. The functionality moved to the mysqld binary which automatically runs the upgrade process, if needed. If you attempt to run `mysql_upgrade`, no operation happens and the following message appears: “The mysql_upgrade client is now deprecated. The actions executed by the upgrade client are now done by the server.” To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

        If you are upgrading to a Percona Server for MySQL version before 8.0.16-7, the installation script does not run automatically `mysql_upgrade`. You must run `mysql_upgrade` manually.

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

    7.  Restart the service with `service mysql restart`. After the service has been successfully restarted use the new Percona Server for MySQL 8.0.

=== "Red Hat-derived distributions"

    1. Check the installed packages:

        ```{.bash data-prompt="$"}
        $ rpm -qa | grep percona-server
        ```
        
        ??? example "Expected output"

            ```{.text .no-copy}
            percona-server-shared-8.0.29-21.1.el8.x86_64
            percona-server-shared-compat-8.0.29-21.1.el8.x86_64
            percona-server-client-8.0.29-21.1.el8.x86_64
            percona-server-server-8.0.29-21.1.el8.x86_64
            ```

        You may have the `shared-compat` package, which is required for compatibility.

    2. Remove the packages without dependencies with `rpm -qa | grep percona-server | xargs rpm -e --nodeps`.

        It is important that you remove the packages without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.
        
        To remove the listed packages, run:

        ```{.bash data-prompt="$"}
        $ rpm -qa | grep '^mysql-'| xargs rpm -e --nodeps`
        ```

    3. Download the packages of the desired series for your architecture from the [download page](https://www.percona.com/downloads/Percona-Server-8.0/). The easiest way is to download the bundle which contains all the packages. The following example downloads Percona Server for MySQL 8.0.29-21 release packages for CentOS 8:

        ```{.bash data-prompt="$"}
        $ wget https://downloads.percona.com/downloads/Percona-Server-LATEST/Percona-Server-8.0.29-21/binary/redhat/8/x86_64/Percona-Server-8.0.29-21-rc59f87d2854-el8-x86_64-bundle.tar
        ```

    4. Unpack the bundle to get the packages

        ```{.bash data-prompt="$"}
        $ tar xvf Percona-Server-8.0.29-21-rc59f87d2854-el8-x86_64-bundle.tar
        ```

        After you unpack the bundle, you should see the following packages: `ls \*.rpm`

    5. Install Percona Server for MySQL:

        ```{.bash data-prompt="$"}
        $ sudo rpm -ivh percona-server-server-8.0.29-21.1.el8.x86_64.rpm \
        > percona-server-client-8.0.29-21.1.el8.x86_64.rpm \
        > percona-server-shared-8.0.29-21.1.el8.x86_64.rpm \
        > percona-server-shared-compat-8.0.29-21.1.el8.x86_64.rpm
        ```
        
        This command installs only packages required to run the Percona Server for MySQL
        8.0.

    6. You can install all the packages (for debugging, testing, etc.) with `sudo rpm -ivh \*.rpm`.

        !!! note
        
            When manually installing packages, you must resolve all the dependencies and install missing ones.

    7. Modify your configuration file, `my.cnf`, and install the plugins if necessary. If you are using the TokuDB storage engine you must comment out all the TokuDB specific variables in your configuration file(s) before starting the server, otherwise, the server will not start. 

    RHEL/CentOS automatically backs up the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After the upgrade/install process completes you can move the old configuration file back (after you remove all the unsupported system variables).

    8. The schema of the grant table has changed, the server must be started without reading the grants. Add a line to my.cnf in the [mysqld] section,
    
    ```{.text .no-copy}
    [mysqld]
    skip-grant-tables
    ```
    
     Restart the mysql server with `service mysql start`. 

    9.  Running the upgrade:

        Starting with Percona Server for MySQL 8.0.16-7, `mysql_upgrade` is deprecated. After this version, no operation occurs and this utility generates a message. The mysqld binary automatically runs the upgrade process if needed. 

        To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

        If you are upgrading to a Percona Server for MySQL version before 8.0.16-7, run
        `mysql_upgrade` to migrate to the new grant tables and 
        rebuild the required indexes and do the required modifications.

    10. Restart the server with `service mysql restart`. After the service has been successfully restarted you can use the new Percona Server for MySQL 8.0.
