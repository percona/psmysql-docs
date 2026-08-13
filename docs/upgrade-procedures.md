# Upgrade procedures for {{vers}}

**Topic type**: Task

[Need expert guidance for your Percona Server upgrade? Percona Support can help :octicons-link-external-16:](https://www.percona.com/services/expert-support/).

Use the following procedures to upgrade Percona Server for MySQL. The procedures cover Percona repositories (recommended), standalone packages, and both in-place and logical paths. For underlying MySQL guidance, see [Upgrading MySQL Binary or Package-based Installations on Unix/Linux :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrade-binary-package.html).

!!! warning "Critical"

    Always test the upgrade in a non-production environment first. For detailed procedures or troubleshooting, contact our [Percona Support team :octicons-link-external-16:](https://www.percona.com/services/expert-support/).

## Choose an upgrade method

Two methods apply to most {{vers}} environments. Use the following table to choose the method that matches your downtime budget and data size.

| Method | Description | Downtime | Best for |
|---|---|---|---|
| In-place | Stop the source server, replace binaries or packages, then restart on the existing data directory | Short, equal to restart and metadata upgrade time | Same-platform upgrades within Percona Server for MySQL |
| Logical | Export SQL from the source server, install {{vers}} on a clean target, then load the dump | Long, scaled to data size | Cross-platform moves, storage-engine consolidations, or dump-based reorganizations |

For a parallel environment with controlled cutover, see [Upgrade strategies](./upgrade-strategies.md).

## Prepare for the upgrade

Complete the following pre-flight steps before any procedure on this page.

1. Complete the pre-upgrade items in the [upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md).

2. Create a full backup or dump of your database. Verify the backup by restoring into a clean test environment.

3. Save a copy of the database configuration file (`my.cnf`) to a safe location.

4. Edit the configuration file before stopping the server. For example, remove deprecated variables and update settings for {{vers}}.

5. Run `XA RECOVER` against the source server. Commit or rollback any uncommitted XA transactions before continuing.

    ```sql
    XA RECOVER;
    ```

6. If `innodb_fast_shutdown` is set to `2` (cold shutdown), reset to `1` or `0` before stopping. A fast or slow shutdown leaves InnoDB undo logs and data files in a state that is safe across releases.

    ```sql
    SET GLOBAL innodb_fast_shutdown = 0;
    ```

7. Stop the server with the appropriate command for your system.

    ```shell
    sudo systemctl stop mysql
    ```

If your prior installation comprises multiple Red Hat Package Manager (RPM) packages, upgrade every related package together. A partial upgrade leaves mismatched binaries.

## Upgrade with Percona repositories (recommended)

The Percona repositories handle dependencies automatically and reduce upgrade complexity. The following documents describe how to enable the repositories:

* [Percona APT Repository](./apt-repo.md)

* [Percona RPM Repository](./yum-repo.md)

=== "DEB-based distributions"

    Run the following commands as root or with `sudo`.

    1. Create a full backup or dump of your database. Save a copy of the database configuration file, `my.cnf`, to another directory. Without a backup, the upgrade may overwrite the file.

    2. Stop the server with the appropriate command for your system.

        ```shell
        sudo systemctl stop mysql
        ```

    3. Modify the database configuration file, `my.cnf`, as needed. For example, remove deprecated variables and update settings for {{vers}}.

    4. Install Percona Server for MySQL.

        ```shell
        sudo apt update
        sudo apt install curl
        curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
        sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
        sudo apt update
        sudo percona-release setup {{pkg}}
        sudo apt install percona-server-server
        ```

    5. Install the storage engine packages.

        If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package.

        ```shell
        sudo apt install percona-server-rocksdb
        ```

    6. The `mysqld` binary runs the upgrade process automatically on first start. The server creates the data dictionary and refreshes the Performance Schema, INFORMATION_SCHEMA, and `sys` databases. The server then removes obsolete `.frm` files. For details, see [MySQL Upgrade Process :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    7. Restart the service.

        ```shell
        sudo systemctl restart mysql
        ```

    After a successful restart, you can use Percona Server for MySQL {{vers}}.

=== "RPM-based distributions"

    Run the following commands as root or with `sudo`.

    1. Create a full backup or dump of your database. Save a copy of the database configuration file, `my.cnf`, to another directory.

    2. Stop the server with the appropriate command for your system.

        ```shell
        sudo systemctl stop mysql
        ```

    3. Check your installed packages.

        ```shell
        rpm -qa | grep Percona-Server
        ```

    4. Remove the packages without dependencies. The command does not prompt for confirmation.

        ```shell
        rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
        ```

    5. Remove the `mysql`-prefixed packages.

        ```shell
        rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
        ```

    6. Install the `percona-server-server` package.

        ```shell
        sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
        sudo percona-release setup {{pkg}}
        sudo yum install percona-server-server
        ```

    7. Install the storage engine packages.

        If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package.

        ```shell
        sudo yum install percona-server-rocksdb
        ```

    8. Modify your configuration file, `my.cnf`, as needed. For example, remove deprecated variables and update settings for {{vers}}. If you used plugins replaced by components in {{vers}}, plan the transition. See [Upgrade from plugins to components](./upgrade-components.md) for details.

    9. The `mysqld` binary runs the upgrade process automatically on first start. The server creates the data dictionary and refreshes the Performance Schema, INFORMATION_SCHEMA, and `sys` databases. The server then removes obsolete `.frm` files. For details, see [MySQL Upgrade Process :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    10. Restart the server.

        ```shell
        sudo systemctl restart mysql
        ```

    After a successful restart, you can use Percona Server for MySQL {{vers}}.

## Upgrade with standalone packages

Use standalone packages when repositories are unavailable, or when you must install from manually downloaded packages. Standalone installs require you to resolve dependencies yourself.

=== "Debian-derived distributions"

    1. Remove the installed packages with their dependencies.

        ```shell
        sudo apt autoremove percona-server percona-client
        ```

    2. Modify the database configuration file, `my.cnf`, as needed.

    3. Download the following packages for your architecture.

        * `libperconaserverclient21`

        * `percona-server-client`

        * `percona-server-common`

        * `percona-server-server`

        The following example downloads Percona Server for MySQL {{release}} packages for Debian 11.0.

        ```shell
        wget https://downloads.percona.com/downloads/Percona-Server-innovative-release/Percona-Server-{{release}}/binary/debian/bullseye/x86_64/Percona-Server-{{release}}-r582ebeef-bullseye-x86_64-bundle.tar
        ```

    4. Unpack the bundle to get the packages.

        ```shell
        tar xvf Percona-Server-{{release}}-r582ebeef-bullseye-x86_64-bundle.tar
        ```

        After unpacking, you should see the following packages.

        ```shell
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

    5. Install Percona Server for MySQL.

        ```shell
        sudo dpkg -i *.deb
        ```

        The command installs all packages from the bundle. You can also install only the packages required to run Percona Server for MySQL.

        * `libperconaserverclient21_{{release}}.bullseye_amd64.deb`

        * `percona-server-client_{{release}}.bullseye_amd64.deb`

        * `percona-server-common_{{release}}.bullseye_amd64.deb`

        * `percona-server-server_{{release}}.bullseye_amd64.deb`

        !!! warning

            When you install packages manually, you must resolve all dependencies and install missing packages yourself. Install the following packages before installing Percona Server for MySQL {{release}}.

            * `libaio1`

            * `libjemalloc1`

            * `libmecab2`

            * `zlib1g-dev`

    6. The `mysqld` binary runs the upgrade process automatically on first start. For more information, see [MySQL Upgrade Process :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    7. Restart the service.

        ```shell
        sudo service mysql restart
        ```

    After a successful restart, use Percona Server for MySQL {{release}}.

=== "Red Hat-derived distributions"

    1. Check the installed packages.

        ```shell
        rpm -qa | grep percona-server
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            percona-server-shared-{{release}}.el9.x86_64
            percona-server-shared-compat-{{release}}.el9.x86_64
            percona-server-client-{{release}}.el9.x86_64
            percona-server-server-{{release}}.el9.x86_64
            ```

        The `shared-compat` package may also be present, which is required for compatibility.

    2. Remove the packages without dependencies.

        ```shell
        rpm -qa | grep percona-server | xargs rpm -e --nodeps
        ```

        Use `--nodeps` because the Percona Server packages share dependencies. Without `--nodeps`, removing one package removes related packages.

        Run the following command to remove `mysql`-prefixed packages.

        ```shell
        rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
        ```

    3. Download the packages for your architecture from the [download page :octicons-link-external-16:](https://www.percona.com/downloads). The bundle includes all packages and is the recommended option. The following example downloads Percona Server for MySQL {{release}} packages for Red Hat Enterprise Linux (RHEL) 9.

        ```shell
        wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/redhat/9/x86_64/Percona-Server-{{release}}-r9927a2fb-el9-x86_64-bundle.tar
        ```

    4. Unpack the bundle to get the packages.

        ```shell
        tar xvf Percona-Server-{{release}}-r9927a2fb-el9-x86_64-bundle.tar
        ```

        After unpacking, you should see the available packages.

        ```shell
        ls *.rpm
        ```

    5. Install Percona Server for MySQL.

        ```shell
        sudo rpm -ivh percona-server-server-{{release}}.el9.x86_64.rpm \
        percona-server-client-{{release}}.el9.x86_64.rpm \
        percona-server-shared-{{release}}.el9.x86_64.rpm \
        percona-server-shared-compat-{{release}}.el9.x86_64.rpm
        ```

        The command installs only the packages required to run Percona Server for MySQL {{release}}.

        Run the following command to install all packages, including debugging and testing packages.

        ```shell
        sudo rpm -ivh *.rpm
        ```

        !!! note

            When you install packages manually, you must resolve all dependencies and install missing packages.

    6. Modify your configuration file, `my.cnf`, as needed. For example, remove deprecated variables and update settings for {{vers}}. If you used plugins replaced by components in {{vers}}, plan the transition. See [Upgrade from plugins to components](./upgrade-components.md) for details.

        RHEL and its derivatives copy the previous configuration file to `/etc/my.cnf.rpmsave`. The package install also adds the default `my.cnf`. After the upgrade or install completes, restore your configuration from the saved copy. Remove any unsupported system variables before restoring.

    7. The `mysqld` binary runs the upgrade process automatically on first start. For more information, see [MySQL Upgrade Process :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/upgrading-what-is-upgraded.html).

    8. Restart the server.

        ```shell
        sudo service mysql restart
        ```

    After a successful restart, you can use Percona Server for MySQL {{release}}.

## Perform a logical upgrade with mysqldump

Use a logical upgrade when an in-place upgrade is not viable. Examples include cross-platform migrations and storage-engine consolidations. The logical path exports SQL from the source server and loads the SQL into a fresh {{vers}} server.

Run the following procedure on the source and target hosts.

1. Export the source database. Include `--routines`, `--events`, and `--all-databases` so that stored programs and the `mysql` system database appear in the dump.

    ```shell
    mysqldump -u root -p \
      --add-drop-table \
      --routines \
      --events \
      --all-databases \
      --force > data-for-upgrade.sql
    ```

2. Stop the source server.

    ```shell
    mysqladmin -u root -p shutdown
    ```

3. Install Percona Server for MySQL {{vers}} on a clean host or a separate path. Use the procedure in [Upgrade with Percona repositories (recommended)](#upgrade-with-percona-repositories-recommended) or [Upgrade with standalone packages](#upgrade-with-standalone-packages).

4. Initialize a fresh data directory for {{vers}}.

    ```shell
    mysqld --initialize --datadir=/var/lib/mysql-{{vers}}
    ```

    Capture the temporary `root` password from standard error or the error log.

5. Start the {{vers}} server with the fresh data directory.

    ```shell
    mysqld_safe --user=mysql --datadir=/var/lib/mysql-{{vers}} &
    ```

6. Connect with the temporary password and reset the `root` account.

    ```sql
    ALTER USER USER() IDENTIFIED BY '<NEW_ROOT_PASSWORD>';
    ```

7. Load the dump file into the {{vers}} server.

    ```shell
    mysql -u root -p --force < data-for-upgrade.sql
    ```

8. Restart with `--upgrade=FORCE` to finish data dictionary tasks.

    ```shell
    mysqladmin -u root -p shutdown
    mysqld_safe --user=mysql --datadir=/var/lib/mysql-{{vers}} --upgrade=FORCE &
    ```

!!! warning "Global Transaction Identifier (GTID) interaction"

    Do not load a dump file that contains the `mysql` system database when `gtid_mode=ON`. The `mysqldump` output issues data manipulation statements against `MyISAM` system tables. These statements conflict with the GTID requirement for transactional storage. Disable GTID functionality during the load or take the dump without system tables.

## Validate after upgrading

After completing the upgrade, follow the post-upgrade validation steps in the [upgrade checklist](./upgrade-checklist-9.7.md#post-upgrade-validation).

The upgrade does not refresh time zone tables. Reload the tables with `mysql_tzinfo_to_sql` if your applications depend on time zone names.

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

## Troubleshoot upgrade failures

The following table maps common upgrade failure modes to the corrective action.

| Symptom | Diagnosis | Solution |
|---|---|---|
| The {{vers}} server fails the metadata upgrade and reverts the data directory | A schema problem flagged during pre-upgrade checks was not resolved | Remove the redo log files (`ib_logfile*`) from the data directory. Start the source server on the same data directory. Fix the schema. Perform a slow shutdown with `innodb_fast_shutdown=0`, then retry the upgrade |
| `mysqld` does not start after binary replacement | A stale `my.cnf` from the prior installation is still in effect | Run `mysqld --print-defaults` to inspect the active defaults. Replace or repair the configuration file, then retry start |
| Compiled client programs report "Commands out of sync" or core dump | Programs are linked against the prior client headers and shared library | Recompile programs against the {{vers}} headers (`mysql.h`) and the {{vers}} shared client library. Note the major version change in the library file name |
| A loadable function and a built-in function share a name | The {{vers}} server provides a built-in function that collides with an existing loadable function | Run `DROP FUNCTION <NAME>`. Recreate the function with `CREATE FUNCTION` under a non-conflicting name |
| Encrypted InnoDB tablespaces fail to open | The keyring component or plugin is not loaded early in the startup sequence | Configure the keyring through a manifest file (`mysqld.my`). See [Upgrade from plugins to components](./upgrade-components.md) |

For schema-readiness checks before the upgrade, see [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md).

## Further reading

The following Percona Server for MySQL pages cover upgrade-related topics:

* [Downgrade options](./downgrade.md)

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade strategies](./upgrade-strategies.md)
