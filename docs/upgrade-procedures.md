# Upgrade procedures for {{vers}}

[Need expert guidance for your Percona Server upgrade? Percona Support is here to help.](https://www.percona.com/services/support)

This document provides step-by-step procedures for upgrading Percona Server for MySQL using either Percona repositories (recommended) or standalone packages.

Before beginning the upgrade process:

1. Complete the [upgrade checklist](./upgrade-checklist-8.4.md) pre-upgrade checks.
2. Create a full backup (or dump if possible) of your database.
3. Back up your database configuration file (`my.cnf`) to a safe location, then modify it as needed (for example, remove deprecated variables, update settings for {{vers}}) before stopping the server.
4. Stop the server using the appropriate command for your system:

    ```{.bash}
    sudo systemctl stop mysql
    ```

!!! warning "Critical"

    Always test the upgrade process in a non-production environment first. For detailed upgrade procedures or if you encounter any issues during this process, our [Percona Support team](https://www.percona.com/services/support) is available to assist you.

## Using Percona repositories (recommended)

We recommend using the Percona repositories to upgrade your server. This method automatically handles dependencies and simplifies the upgrade process.

Find the instructions on how to enable the repositories in the following documents:

* [Percona APT Repository](./apt-repo.md)
* [Percona RPM Repository](./yum-repo.md)

=== "DEB-based distributions"

    Run the following commands as root or use the `sudo` command.

    1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, `my.cnf`, to another directory as a backup. If the configuration file is not backed up, it may be overwritten during the upgrade.

    2. Stop the server with the appropriate command for your system:
   
        ```{.bash}
        sudo systemctl stop mysql
        ```

    3. Modify the database configuration file, `my.cnf`, as needed (for example, remove deprecated variables, update settings for {{vers}}).

    4. Install Percona Server for MySQL:

        ```{.bash}
        sudo apt update
        sudo apt install curl
        curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb 
        sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
        sudo apt update
        sudo percona-release setup {{pkg}}
        sudo apt install percona-server-server
        ```

    5. Install the storage engine packages.

        If you used the MyRocks storage engine in Percona Server for MySQL {{vers}}, install the `percona-server-rocksdb` package:

        ```{.bash}
        sudo apt install percona-server-rocksdb
        ```

    6. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    7. Restart the service:

        ```{.bash}
        sudo systemctl restart mysql
        ```

    After the service has been successfully restarted, you can use the new Percona Server for MySQL {{vers}}.

=== "RPM-based distributions"

    Run the following commands as root or use the `sudo` command.

    1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, for example, `my.cnf`, to another directory to save it.

    2. Stop the server with the appropriate command for your system:
   
        ```{.bash}
        sudo systemctl stop mysql
        ```

    3. Check your installed packages:

        ```{.bash}
        rpm -qa | grep Percona-Server
        ```

    4. Remove only the packages without dependencies and leave dependent packages. The command does not prompt for confirmation:

        ```{.bash}
        rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
        ```

    5. Remove the mysql-related packages:

        ```{.bash}
        rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
        ```

    6. Install the `percona-server-server` package:

        ```{.bash}
        sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
        sudo percona-release setup {{pkg}}
        sudo yum install percona-server-server
        ```

    7. Install the storage engine packages.

        If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package:

        ```{.bash}
        sudo yum install percona-server-rocksdb
        ```

    8. Modify your configuration file, `my.cnf`, as needed (for example, remove deprecated variables, update settings for {{vers}}). If you were using plugins that have been replaced by components in {{vers}}, plan the transition to components. See [Upgrade from plugins to components](./upgrade-components.md) for details.

    9. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    10. Restart the server:

        ```{.bash}
        sudo systemctl restart mysql
        ```

    After the service has been successfully restarted, you can use the Percona Server for MySQL {{vers}}.

## Using standalone packages

Use this method when you cannot use repositories or need to install from manually downloaded packages. This method requires you to manually resolve dependencies.

=== "Debian-derived distributions"

    1. Remove the installed packages with their dependencies:

        ```{.bash}
        sudo apt autoremove percona-server percona-client
        ```

    2. Do the required modifications in the database configuration file `my.cnf`.

    3. Download the following packages for your architecture:

        * `percona-server-server`
        * `percona-server-client`
        * `percona-server-common`
        * `libperconaserverclient21`

        The following example downloads Percona Server for MySQL {{release}} packages for Debian 11.0:

        ```{.bash}
        wget https://downloads.percona.com/downloads/Percona-Server-innovative-release/Percona-Server-{{release}}/binary/debian/bullseye/x86_64/Percona-Server-{{release}}-r582ebeef-bullseye-x86_64-bundle.tar
        ```

    4. Unpack the bundle to get the packages:

        ```{.bash}
        tar xvf Percona-Server-{{release}}-r582ebeef-bullseye-x86_64-bundle.tar
        ```

        After you unpack the bundle, you should see the following packages:

        ```{.bash}
        ls *.deb
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            libperconaserverclient21-dev_{{release}}.bullseye_amd64.deb  
            percona-server-dbg_{{release}}.bullseye_amd64.deb
            libperconaserverclient21_{{release}}.bullseye_amd64.deb      
            percona-server-rocksdb_{{release}}.bullseye_amd64.deb
            percona-mysql-router_{{release}}.bullseye_amd64.deb
            percona-server-server_{{release}}.bullseye_amd64.deb
            percona-server-client_{{release}}.bullseye_amd64.deb     
            percona-server-source_{{release}}.bullseye_amd64.deb
            percona-server-common_{{release}}.bullseye_amd64.deb     
            percona-server-test_{{release}}.bullseye_amd64.deb
            ```

    5. Install Percona Server for MySQL:

        ```{.bash}
        sudo dpkg -i *.deb
        ```

        This command installs the packages from the bundle. Another option is to download or specify only the packages you need for running Percona Server for MySQL installation (`libperconaserverclient21_{{release}}.bullseye_amd64.deb`, `percona-server-client_{{release}}.bullseye_amd64.deb`, `percona-server-common_{{release}}.bullseye_amd64.deb`, and `percona-server-server_{{release}}.bullseye_amd64.deb`).

        !!! warning

            When installing packages manually, you must resolve all the dependencies and install missing packages yourself. At least the following packages should be installed before installing Percona Server for MySQL {{release}}:
            * `libmecab2`
            * `libjemalloc1`
            * `zlib1g-dev`
            * `libaio1`

    6. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    7. Restart the service:

        ```{.bash}
        sudo service mysql restart
        ```

    After the service has been successfully restarted, use the new Percona Server for MySQL {{release}}.

=== "Red Hat-derived distributions"

    1. Check the installed packages:

        ```{.bash}
        rpm -qa | grep percona-server
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            percona-server-shared-{{release}}.el9.x86_64
            percona-server-shared-compat-{{release}}.el9.x86_64
            percona-server-client-{{release}}.el9.x86_64
            percona-server-server-{{release}}.el9.x86_64
            ```

        You may have the `shared-compat` package, which is required for compatibility.

    2. Remove the packages without dependencies:

        ```{.bash}
        rpm -qa | grep percona-server | xargs rpm -e --nodeps
        ```

        It is important that you remove the packages without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.

        To remove the listed packages, run:

        ```{.bash}
        rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
        ```

    3. Download the packages of the desired series for your architecture from the [download page](https://www.percona.com/downloads). The easiest way is to download the bundle which contains all the packages. The following example downloads Percona Server for MySQL {{release}} packages for RHEL 9:

        ```{.bash}
        wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/redhat/9/x86_64/Percona-Server-{{release}}-r9927a2fb-el9-x86_64-bundle.tar
        ```

    4. Unpack the bundle to get the packages:

        ```{.bash}
        tar xvf Percona-Server-{{release}}-r9927a2fb-el9-x86_64-bundle.tar
        ```

        After you unpack the bundle, you should see the following packages:

        ```{.bash}
        ls *.rpm
        ```

    5. Install Percona Server for MySQL:

        ```{.bash}
        sudo rpm -ivh percona-server-server-{{release}}.el9.x86_64.rpm \
        percona-server-client-{{release}}.el9.x86_64.rpm \
        percona-server-shared-{{release}}.el9.x86_64.rpm \
        percona-server-shared-compat-{{release}}.el9.x86_64.rpm
        ```

        This command installs only packages required to run the Percona Server for MySQL {{release}}.

        You can install all the packages (for debugging, testing, etc.) with:

        ```{.bash}
        sudo rpm -ivh *.rpm
        ```

        !!! note

            When manually installing packages, you must resolve all the dependencies and install missing ones.

    6. Modify your configuration file, `my.cnf`, as needed (for example, remove deprecated variables, update settings for {{vers}}). If you were using plugins that have been replaced by components in {{vers}}, plan the transition to components. See [Upgrade from plugins to components](./upgrade-components.md) for details.

        RHEL or derivatives automatically backs up the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After the upgrade/install process completes, you can restore your configuration from the backup (after removing all unsupported system variables).

    7. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    8. Restart the server:

        ```{.bash}
        sudo service mysql restart
        ```

    After the service has been successfully restarted, you can use the new Percona Server for MySQL {{release}}.

## Post-upgrade validation

After completing the upgrade, follow the post-upgrade validation steps in the [upgrade checklist](./upgrade-checklist-8.4.md#post-upgrade-validation).

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade checklist for {{vers}}](./upgrade-checklist-8.4.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Downgrade options](./downgrade.md)
* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)
* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md)
* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)

