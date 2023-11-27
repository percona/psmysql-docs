# Upgrade using the Percona repositories

We recommend using the Percona repositories to upgrade your server.

Find the instructions on how to enable the repositories in the following documents:

* [Percona APT Repository](apt-repo.md)

* [Percona RPM Repository](yum-repo.md)


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
        $ curl -0 https://repo.percona.com/apt/percona-release_latest.generic_all.deb 
        $ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
        $ sudo apt update
        $ sudo percona-release setup  {{pkg}}
        $ sudo apt install percona-server-server
        ```

    5. Install the storage engine packages.

        If you used the MyRocks storage engine in Percona Server for MySQL {{vers}}, install the `percona-server-rocksdb` package:

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-server-rocksdb
        ```

    6. Running the upgrade:

        The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html)

    7. Restart the service 

        ```{.bash data-prompt="$"}
        $ sudo systemctl restart mysqld
        ```
    After the service has been successfully restarted you can use the new Percona Server for MySQL {{vers}}.

=== "RPM-based distributions"

    Run the following commands as root or use the sudo command.


    1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, for example, `my.cnf`, to another directory to save it.


    2. Stop the server with the appropriate command for your system:
   
        ```{.bash data-prompt="$"}
        $ systemctl stop mysql`
        ```

    3. Check your installed packages with `rpm -qa | grep Percona-Server`.

    4. Remove only the packages without dependencies and leave dependent packages. The command does not prompt for confirmation:

         ```{.bash data-prompt="$"}
         $ rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
         ```

    5. Remove the mysql-related packages, run:

         ```{.bash data-prompt="$"}
         $ rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
         ```


    6. Install the `percona-server-server` package:

         ```{.bash data-prompt="$"}
         $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
         $ sudo percona-release setup {{pkg}}
         $ sudo yum install percona-server-server
         ```

    7. Install the storage engine packages.

        If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package:

         ```{.bash data-prompt="$"}
         $ yum install percona-server-rocksdb
         ```

    8. Modify your configuration file, `my.cnf`, and reinstall the plugins if necessary.


    2. Running the upgrade
        
        The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process Upgrades](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html)

    Restart the server and you can use the Percona Server for MySQL {{vers}}.
