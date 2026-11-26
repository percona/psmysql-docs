> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Upgrade procedures for 9.7

**Topic type**: Task

[Need expert guidance for your Percona Server upgrade? Percona Support can help](https://www.percona.com/services/expert-support/) .

Use the following procedures to upgrade Percona Server for MySQL. The procedures cover Percona repositories (recommended), standalone packages, and both in-place and logical paths. For underlying MySQL guidance, see [Upgrading MySQL Binary or Package-based Installations on Unix/Linux](https://dev.mysql.com/doc/refman/9.7/en/upgrade-binary-package.html) .

Critical

Always test the upgrade in a non-production environment first. For detailed procedures or troubleshooting, contact our [Percona Support team](https://www.percona.com/services/expert-support/) .

## Choose an upgrade method

Two methods apply to most 9.7 environments. Use the following table to choose the method that matches your downtime budget and data size.

| Method   | Description                                                                                       | Downtime                                          | Best for                                                                           |
| -------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------- |
| In-place | Stop the source server, replace binaries or packages, then restart on the existing data directory | Short, equal to restart and metadata upgrade time | Same-platform upgrades within Percona Server for MySQL                             |
| Logical  | Export SQL from the source server, install 9.7 on a clean target, then load the dump              | Long, scaled to data size                         | Cross-platform moves, storage-engine consolidations, or dump-based reorganizations |

For a parallel environment with controlled cutover, see [Upgrade strategies](https://docs.percona.com/percona-server/9.7/upgrade-strategies.md).

## Prepare for the upgrade

Complete the following pre-flight steps before any procedure on this page.

1. Complete the pre-upgrade items in the [upgrade checklist for 9.7](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md).

1. Create a full backup or dump of your database. Verify the backup by restoring into a clean test environment.

1. Save a copy of the database configuration file (`my.cnf`) to a safe location.

1. Edit the configuration file before stopping the server. Remove options that 9.7 no longer supports, such as `mysql_native_password=ON`, `plugin-load-add=audit_log.so`, and the `audit_log_*` options of the removed `audit_log` plugin. Update other settings for 9.7 as needed.

   Warning

   The 9.7 server upgrades the data dictionary before it rejects unknown options. An option that 9.7 does not support aborts the first start with `[ERROR] [MY-000067] [Server] unknown variable '<option>'` after the data directory has already been upgraded. The previous version can no longer start on that data directory. Only a restore from backup returns you to the previous version.

   Validate the configuration file with the 9.7 `mysqld` binary before the first start of 9.7. The check reads the configuration, reports unknown options, and exits without starting the server or modifying the data directory. A valid configuration returns exit status `0`:

   ```shell
   sudo mysqld --validate-config --user=mysql
   ```

   On Debian and Ubuntu, installing the 9.7 packages starts the server immediately. Run the check before the production upgrade on a staging host that runs 9.7, with a copy of the production configuration file. To check a specific file, add `--defaults-file=<path>` as the first option.

1. Run `XA RECOVER` against the source server. Commit or rollback any uncommitted XA transactions before continuing.

   ```sql
   XA RECOVER;
   ```

1. If `innodb_fast_shutdown` is set to `2` (cold shutdown), reset to `1` or `0` before stopping. A fast or slow shutdown leaves InnoDB undo logs and data files in a state that is safe across releases.

   ```sql
   SET GLOBAL innodb_fast_shutdown = 0;
   ```

1. Stop the server with the appropriate command for your system.

   ```shell
   sudo systemctl stop mysql
   ```

If your prior installation comprises multiple Red Hat Package Manager (RPM) packages, upgrade every related package together. A partial upgrade leaves mismatched binaries.

## Upgrade with Percona repositories (recommended)

The Percona repositories handle dependencies automatically and reduce upgrade complexity. The following documents describe how to enable the repositories:

- [Percona APT Repository](https://docs.percona.com/percona-server/9.7/apt-repo.md)
- [Percona RPM Repository](https://docs.percona.com/percona-server/9.7/yum-repo.md)

**DEB-based distributions**

Run the following commands as root or with `sudo`.

1. Create a full backup or dump of your database. Save a copy of the database configuration file, `my.cnf`, to another directory. Without a backup, the upgrade may overwrite the file.

1. Stop the server with the appropriate command for your system.

   ```shell
   sudo systemctl stop mysql
   ```

1. Modify the database configuration file, `my.cnf`, as needed. Remove options that 9.7 no longer supports and update settings for 9.7. The package installation in the next step starts the server, so validate the configuration with the 9.7 binary beforehand. See [Prepare for the upgrade](#prepare-for-the-upgrade).

1. Install Percona Server for MySQL. The `percona-release enable-only` command disables the repository of the previous version and enables the 9.7 repository. Before you run `apt install`, check that `apt-cache policy percona-server-server` shows a 9.7 candidate version.

   ```shell
   sudo apt update
   sudo apt install curl
   curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
   sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
   sudo percona-release enable-only ps-97-lts release
   sudo apt update
   sudo apt install percona-server-server
   ```

1. Install the storage engine packages.

   If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package.

   ```shell
   sudo apt install percona-server-rocksdb
   ```

1. The `mysqld` binary runs the upgrade process automatically on first start. The server creates the data dictionary and refreshes the Performance Schema, INFORMATION_SCHEMA, and `sys` databases. The server then removes obsolete `.frm` files. For details, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/9.7/en/upgrading-what-is-upgraded.html) .

1. Restart the service.

   ```shell
   sudo systemctl restart mysql
   ```

After a successful restart, you can use Percona Server for MySQL 9.7.

**RPM-based distributions**

Run the following commands as root or with `sudo`.

1. Create a full backup or dump of your database. Save a copy of the database configuration file, `my.cnf`, to another directory.

1. Stop the server with the appropriate command for your system.

   ```shell
   sudo systemctl stop mysql
   ```

1. Check your installed Percona packages. Percona Server for MySQL 8.x and later packages use lowercase names (`percona-server-*`). Do not remove these packages; the following steps upgrade them in place.

   ```shell
   rpm -qa | grep -i percona-server
   ```

1. Check for `mysql`-prefixed packages from another vendor.

   ```shell
   rpm -qa | grep '^mysql-'
   ```

1. If the previous step lists packages, remove them without dependencies. The command does not prompt for confirmation. If the list is empty, skip this step.

   ```shell
   rpm -qa | grep '^mysql-' | xargs -r rpm -e --nodeps
   ```

1. Install the `percona-server-server` package. The `percona-release enable-only` command disables the repository of the previous version and enables the 9.7 repository. Before you run `yum install`, check that `sudo dnf repolist | grep ps-97-lts` lists the `ps-97-lts-release-<arch>` repository.

   ```shell
   sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   sudo percona-release enable-only ps-97-lts release
   sudo yum install percona-server-server
   ```

   Installing `percona-server-server` upgrades only the server package. Upgrade the remaining Percona packages so that the client, shared libraries, and ICU data files match the server. This command also installs new dependencies, such as `percona-server-client-plugins`.

   ```shell
   sudo dnf upgrade 'percona-*'
   ```

   Confirm that every `percona-server-*` package shows the new version.

   ```shell
   rpm -qa | grep -i percona-server
   ```

1. Install the storage engine packages.

   If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package.

   ```shell
   sudo yum install percona-server-rocksdb
   ```

1. Modify your configuration file, `my.cnf`, as needed. For example, remove deprecated variables and update settings for 9.7. If you used plugins replaced by components in 9.7, plan the transition. See [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md) for details.

   Before the first start, validate the configuration with the 9.7 binary. The command must not report errors. See [Prepare for the upgrade](#prepare-for-the-upgrade).

   ```shell
   sudo mysqld --validate-config --user=mysql
   ```

1. The `mysqld` binary runs the upgrade process automatically on first start. The server creates the data dictionary and refreshes the Performance Schema, INFORMATION_SCHEMA, and `sys` databases. The server then removes obsolete `.frm` files. For details, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/9.7/en/upgrading-what-is-upgraded.html) .

1. Restart the server.

   ```shell
   sudo systemctl restart mysql
   ```

After a successful restart, you can use Percona Server for MySQL 9.7.

## Upgrade with standalone packages

Use standalone packages when repositories are unavailable, or when you must install from manually downloaded packages. Standalone installs require you to resolve dependencies yourself.

**Debian-derived distributions**

1. Remove the installed packages with their dependencies.

   ```shell
   sudo apt autoremove percona-server percona-client
   ```

1. Modify the database configuration file, `my.cnf`, as needed.

1. Download the following packages for your architecture.

   - `libperconaserverclient21`
   - `percona-server-client`
   - `percona-server-common`
   - `percona-server-server`

   The following example downloads Percona Server for MySQL 9.7.2-3 packages for Debian 11.0.

   ```shell
   wget https://downloads.percona.com/downloads/Percona-Server-innovative-release/Percona-Server-9.7.2-3/binary/debian/bullseye/x86_64/Percona-Server-9.7.2-3-r582ebeef-bullseye-x86_64-bundle.tar
   ```

1. Unpack the bundle to get the packages.

   ```shell
   tar xvf Percona-Server-9.7.2-3-r582ebeef-bullseye-x86_64-bundle.tar
   ```

   After unpacking, you should see the following packages.

   ```shell
   ls *.deb
   ```

   Expected output

   ```text
   libperconaserverclient21-dev_9.7.2-3.bullseye_amd64.deb
   percona-server-dbg_9.7.2-3.bullseye_amd64.deb
   libperconaserverclient21_9.7.2-3.bullseye_amd64.deb
   percona-server-rocksdb_9.7.2-3.bullseye_amd64.deb
   percona-mysql-router_9.7.2-3.bullseye_amd64.deb
   percona-server-server_9.7.2-3.bullseye_amd64.deb
   percona-server-client_9.7.2-3.bullseye_amd64.deb
   percona-server-source_9.7.2-3.bullseye_amd64.deb
   percona-server-common_9.7.2-3.bullseye_amd64.deb
   percona-server-test_9.7.2-3.bullseye_amd64.deb
   ```

1. Install Percona Server for MySQL.

   ```shell
   sudo dpkg -i *.deb
   ```

   The command installs all packages from the bundle. You can also install only the packages required to run Percona Server for MySQL.

   - `libperconaserverclient21_9.7.2-3.bullseye_amd64.deb`
   - `percona-server-client_9.7.2-3.bullseye_amd64.deb`
   - `percona-server-common_9.7.2-3.bullseye_amd64.deb`
   - `percona-server-server_9.7.2-3.bullseye_amd64.deb`

   Warning

   When you install packages manually, you must resolve all dependencies and install missing packages yourself. Install the following packages before installing Percona Server for MySQL 9.7.2-3.

   - `libaio1`
   - `libjemalloc1`
   - `libmecab2`
   - `zlib1g-dev`

1. The `mysqld` binary runs the upgrade process automatically on first start. For more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/9.7/en/upgrading-what-is-upgraded.html) .

1. Restart the service.

   ```shell
   sudo service mysql restart
   ```

After a successful restart, use Percona Server for MySQL 9.7.2-3.

**Red Hat-derived distributions**

1. Check the installed packages.

   ```shell
   rpm -qa | grep percona-server
   ```

   Expected output

   ```text
   percona-server-shared-9.7.2-3.el9.x86_64
   percona-server-shared-compat-9.7.2-3.el9.x86_64
   percona-server-client-9.7.2-3.el9.x86_64
   percona-server-server-9.7.2-3.el9.x86_64
   ```

   The `shared-compat` package may also be present, which is required for compatibility.

1. Remove the packages without dependencies.

   ```shell
   rpm -qa | grep percona-server | xargs rpm -e --nodeps
   ```

   Use `--nodeps` because the Percona Server packages share dependencies. Without `--nodeps`, removing one package removes related packages.

   Run the following command to remove `mysql`-prefixed packages.

   ```shell
   rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
   ```

1. Download the packages for your architecture from the [download page](https://www.percona.com/downloads) . The bundle includes all packages and is the recommended option. The following example downloads Percona Server for MySQL 9.7.2-3 packages for Red Hat Enterprise Linux (RHEL) 9.

   ```shell
   wget https://downloads.percona.com/downloads/Percona-Server-9.7/Percona-Server-9.7.2-3/binary/redhat/9/x86_64/Percona-Server-9.7.2-3-r9927a2fb-el9-x86_64-bundle.tar
   ```

1. Unpack the bundle to get the packages.

   ```shell
   tar xvf Percona-Server-9.7.2-3-r9927a2fb-el9-x86_64-bundle.tar
   ```

   After unpacking, you should see the available packages.

   ```shell
   ls *.rpm
   ```

1. Install Percona Server for MySQL.

   ```shell
   sudo rpm -ivh percona-server-server-9.7.2-3.el9.x86_64.rpm \
   percona-server-client-9.7.2-3.el9.x86_64.rpm \
   percona-server-shared-9.7.2-3.el9.x86_64.rpm \
   percona-server-shared-compat-9.7.2-3.el9.x86_64.rpm
   ```

   The command installs only the packages required to run Percona Server for MySQL 9.7.2-3.

   Run the following command to install all packages, including debugging and testing packages.

   ```shell
   sudo rpm -ivh *.rpm
   ```

   Note

   When you install packages manually, you must resolve all dependencies and install missing packages.

1. Modify your configuration file, `my.cnf`, as needed. For example, remove deprecated variables and update settings for 9.7. If you used plugins replaced by components in 9.7, plan the transition. See [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md) for details.

   RHEL and its derivatives copy the previous configuration file to `/etc/my.cnf.rpmsave`. The package install also adds the default `my.cnf`. After the upgrade or install completes, restore your configuration from the saved copy. Remove any unsupported system variables before restoring.

   Before the first start, validate the configuration with the 9.7 binary. The command must not report errors. See [Prepare for the upgrade](#prepare-for-the-upgrade).

   ```shell
   sudo mysqld --validate-config --user=mysql
   ```

1. The `mysqld` binary runs the upgrade process automatically on first start. For more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/9.7/en/upgrading-what-is-upgraded.html) .

1. Restart the server.

   ```shell
   sudo service mysql restart
   ```

After a successful restart, you can use Percona Server for MySQL 9.7.2-3.

## Perform a logical upgrade with mysqldump

Use a logical upgrade when an in-place upgrade is not viable. Examples include cross-platform migrations and storage-engine consolidations. The logical path exports SQL from the source server and loads the SQL into a fresh 9.7 server.

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

1. Stop the source server.

   ```shell
   mysqladmin -u root -p shutdown
   ```

1. Install Percona Server for MySQL 9.7 on a clean host or a separate path. Use the procedure in [Upgrade with Percona repositories (recommended)](#upgrade-with-percona-repositories-recommended) or [Upgrade with standalone packages](#upgrade-with-standalone-packages).

1. Initialize a fresh data directory for 9.7.

   ```shell
   mysqld --initialize --datadir=/var/lib/mysql-9.7
   ```

   Capture the temporary `root` password from standard error or the error log.

1. Start the 9.7 server with the fresh data directory.

   ```shell
   mysqld_safe --user=mysql --datadir=/var/lib/mysql-9.7 &
   ```

1. Connect with the temporary password and reset the `root` account.

   ```sql
   ALTER USER USER() IDENTIFIED BY '<NEW_ROOT_PASSWORD>';
   ```

1. Load the dump file into the 9.7 server.

   ```shell
   mysql -u root -p --force < data-for-upgrade.sql
   ```

1. Restart with `--upgrade=FORCE` to finish data dictionary tasks.

   ```shell
   mysqladmin -u root -p shutdown
   mysqld_safe --user=mysql --datadir=/var/lib/mysql-9.7 --upgrade=FORCE &
   ```

Global Transaction Identifier (GTID) interaction

Do not load a dump file that contains the `mysql` system database when `gtid_mode=ON`. The `mysqldump` output issues data manipulation statements against `MyISAM` system tables. These statements conflict with the GTID requirement for transactional storage. Disable GTID functionality during the load or take the dump without system tables.

## Validate after upgrading

After completing the upgrade, follow the post-upgrade validation steps in the [upgrade checklist](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md#post-upgrade-validation).

The upgrade does not refresh time zone tables. Reload the tables with `mysql_tzinfo_to_sql` if your applications depend on time zone names.

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

## Troubleshoot upgrade failures

The following table maps common upgrade failure modes to the corrective action.

| Symptom                                                                  | Diagnosis                                                                                    | Solution                                                                                                                                                                                                             |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The 9.7 server fails the metadata upgrade and reverts the data directory | A schema problem flagged during pre-upgrade checks was not resolved                          | Remove the redo log files (`ib_logfile*`) from the data directory. Start the source server on the same data directory. Fix the schema. Perform a slow shutdown with `innodb_fast_shutdown=0`, then retry the upgrade |
| `mysqld` does not start after binary replacement                         | A stale `my.cnf` from the prior installation is still in effect                              | Run `mysqld --print-defaults` to inspect the active defaults. Replace or repair the configuration file, then retry start                                                                                             |
| Compiled client programs report “Commands out of sync” or core dump      | Programs are linked against the prior client headers and shared library                      | Recompile programs against the 9.7 headers (`mysql.h`) and the 9.7 shared client library. Note the major version change in the library file name                                                                     |
| A loadable function and a built-in function share a name                 | The 9.7 server provides a built-in function that collides with an existing loadable function | Run `DROP FUNCTION <NAME>`. Recreate the function with `CREATE FUNCTION` under a non-conflicting name                                                                                                                |
| Encrypted InnoDB tablespaces fail to open                                | The keyring component or plugin is not loaded early in the startup sequence                  | Configure the keyring through a manifest file (`mysqld.my`). See [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md)                                             |

For schema-readiness checks before the upgrade, see [Upgrade checklist for 9.7](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md).

## Further reading

The following Percona Server for MySQL pages cover upgrade-related topics:

- [Downgrade options](https://docs.percona.com/percona-server/9.7/downgrade.md)
- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/9.7/mysql-upgrade-paths.md)
- [Percona Toolkit updates for 9.7](https://docs.percona.com/percona-server/9.7/percona-toolkit-9.7-updates.md)
- [Upgrade checklist for 9.7](https://docs.percona.com/percona-server/9.7/upgrade-checklist-9.7.md)
- [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md)
- [Upgrade overview](https://docs.percona.com/percona-server/9.7/upgrade.md)
- [Upgrade strategies](https://docs.percona.com/percona-server/9.7/upgrade-strategies.md)
