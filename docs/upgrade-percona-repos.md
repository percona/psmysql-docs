# Upgrade using the Percona repositories

We recommend using the Percona repositories to upgrade your server.

Find the instructions on how to enable the repositories in the following documents:

* [Percona APT Repository](apt-repo.md)

* [Percona RPM Repository](yum-repo.md)

If you used the TokuDB storage engine in Percona Server for MySQL 5.7, we recommend that you migrate to either MyRocks or InnoDB, verify the migration, and then upgrade to 8.0. Percona Server for MySQL 8.0.29 removed the TokuDB storage engine.

=== "DEB-based distributions"

    Run the following commands as root or use the `sudo` command.


    1. Make a full backup (or dump if possible) of your database. Move the database configuration file, `my.cnf`, to another directory to save it. If the configuration file is not moved, it can be overwritten.


    2. Stop the server with the appropriate command for your system:
   
       ```{.bash data-prompt="$"}
       systemctl stop mysql`
       ```

    3. Modify the database configuration file, `my.cnf`, as needed.

    4. Install Percona Server for MySQL:

        ```{.bash data-prompt="$"}
        $ sudo apt update
        $ sudo apt install curl
        $ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb 
        $ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
        $ sudo apt update
        $ sudo percona-release setup ps80
        $ sudo apt install percona-server-server
        ```

    5. Install the storage engine packages.

        [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md#id3) removes TokuDB. For more information, see [TokuDB Introduction](tokudb-intro.md). 
        
        If you used the TokuDB storage engine in Percona Server for MySQL 5.7, we recommend that you migrate to either MyRocks or InnoDB, verify the migration, and then upgrade to 8.0.

        If you used the MyRocks storage engine in Percona Server for MySQL 5.7, install the `percona-server-rocksdb` package:

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-server-rocksdb
        ```

    6. Running the upgrade:

        Starting with Percona Server for MySQL 8.0.16-7, `mysql_upgrade` is deprecated. After this version, no operation occurs and this utility generates a message. The mysqld binary automatically runs the upgrade process if needed. 

        To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

        If you are upgrading to a Percona Server for MySQL version before 8.0.16-7, the installation script does not automatically run `mysql_upgrade`. Run `mysql_upgrade` manually.

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

    7. Restart the service 

        ```{.bash data-prompt="$"}
        $ sudo systemctl restart mysqld
        ```
    After the service has been successfully restarted you can use the new Percona Server for MySQL 8.0.

=== "RPM-based distributions"

    Run the following commands as root or use the sudo command.


    1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, for example, `my.cnf`, to another directory to save it.


    2. Stop the server with the appropriate command for your system:
   
        ```{.bash data-prompt="$"}
        $ systemctl stop mysql`
        ```


    3. Check your installed packages with `rpm -qa | grep Percona-Server`.


    4. Remove the packages without dependencies. This command only removes the specified packages and leaves any dependent packages. The command does not prompt for confirmation:

         ```{.bash data-prompt="$"}
         $ rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
         ```

        It is important to remove the packages without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.
        
        To remove the listed packages, run:

         ```{.bash data-prompt="$"}
         $ rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
         ```


    5. Install the `percona-server-server` package:

         ```{.bash data-prompt="$"}
         $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
        $ sudo percona-release setup ps80
        $ sudo yum install percona-server-server
         ```

    6. Install the storage engine packages.
        [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md#id3) removes TokuDB. For more information, see [TokuDB Introduction](tokudb-intro.md).
        
        If you used the TokuDB storage engine in Percona Server for MySQL 5.7, we recommend that you migrate to either MyRocks or InnoDB, verify the migration, and then upgrade to 8.0.

        If you used the MyRocks storage engine in Percona Server for MySQL 5.7, install the `percona-server-rocksdb` package:

         ```{.bash data-prompt="$"}
         $ yum install percona-server-rocksdb
         ```

    7. Modify your configuration file, `my.cnf`, and reinstall the plugins if necessary.


    2. Running the upgrade
        
        Starting with Percona Server for MySQL 8.0.16-7, `mysql_upgrade` is deprecated. After this version, no operation occurs and this utility generates a message. The mysqld binary automatically runs the upgrade process if needed. 

        To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/8.0/en/upgrading-what-is-upgraded.html)

        If you are upgrading to a Percona Server for MySQL version before 8.0.16-7, you can start the mysql service using `service mysql start`. Use `mysql_upgrade` to migrate to the new grant tables. The `mysql_upgrade` rebuilds the required indexes and does the required modifications:
        
        ```{.bash data-prompt="$"}
        $ mysql_upgrade
        ```

    3. Restart the service.
        
        ```{.bash data-prompt="$"}
        $ systemctl mysql restart`.
        ```
        
    After the service has been successfully restarted you can use the Percona Server for MySQL 8.0.
