> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Upgrade procedures for 8.4

[Need expert guidance for your Percona Server upgrade? Percona Support is here to help](https://www.percona.com/services/support) .

This document provides step-by-step procedures for upgrading Percona Server for MySQL using either Percona repositories (recommended) or standalone packages.

Before beginning the upgrade process:

1. Complete the [upgrade checklist](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.html) pre-upgrade checks.

1. Create a full backup (or dump if possible) of your database.

1. Back up your database configuration file (`my.cnf`) to a safe location, then modify it as needed (for example, remove deprecated variables, update settings for 8.4) before stopping the server.

1. Stop the server using the appropriate command for your system:

   ```
   sudo systemctl stop mysql
   ```

Remove removed options before the first start of 8.4

The server upgrades the data dictionary first and validates the configuration afterwards. If `my.cnf` still contains an option that was removed in 8.4 (for example, `default_authentication_plugin` or `transaction_write_set_extraction`), the first start aborts with `unknown variable ...` after the data directory has already been upgraded. The previous version can no longer start it, and only a restore from the backup goes back.

Validate the configuration with the 8.4 `mysqld` binary before the first start:

```
sudo mysqld --validate-config --user=mysql
```

The command does not touch the data directory. It reports `unknown variable` and exits with a non-zero code if an option is not supported. The DEB packages start the server during `apt install`, so on Debian and Ubuntu, validate the configuration on a staging host with 8.4 installed. See the [upgrade checklist](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.html#configuration-file).

Critical

Always test the upgrade process in a non-production environment first. For detailed upgrade procedures or if you encounter any issues during this process, our [Percona Support team](https://www.percona.com/services/support) is available to assist you.

## Using Percona repositories (recommended)

We recommend using the Percona repositories to upgrade your server. This method automatically handles dependencies and simplifies the upgrade process.

Find the instructions on how to enable the repositories in the following documents:

- [Percona APT Repository](https://docs.percona.com/percona-server/8.4/apt-repo.html)
- [Percona RPM Repository](https://docs.percona.com/percona-server/8.4/yum-repo.html)

**DEB-based distributions**

Run the following commands as root or use the `sudo` command.

1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, `my.cnf`, to another directory as a backup. If the configuration file is not backed up, it may be overwritten during the upgrade.

1. Stop the server with the appropriate command for your system:

   ```
   sudo systemctl stop mysql
   ```

1. Modify the database configuration file, `my.cnf`, as needed (for example, remove deprecated variables, update settings for 8.4).

1. Install Percona Server for MySQL:

   ```
   sudo apt update
   sudo apt install curl
   curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb 
   sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
   sudo apt update
   sudo percona-release setup ps-84-lts
   sudo apt install percona-server-server
   ```

1. Install the storage engine packages.

   If you used the MyRocks storage engine in Percona Server for MySQL 8.4, install the `percona-server-rocksdb` package:

   ```
   sudo apt install percona-server-rocksdb
   ```

1. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/8.4/en/upgrading-what-is-upgraded.html) .

1. Restart the service:

   ```
   sudo systemctl restart mysql
   ```

After the service has been successfully restarted, you can use the new Percona Server for MySQL 8.4.

**RPM-based distributions**

Run the following commands as root or use the `sudo` command.

1. Make a full backup (or dump if possible) of your database. Copy the database configuration file, for example, `my.cnf`, to another directory to save it.

1. Stop the server with the appropriate command for your system:

   ```
   sudo systemctl stop mysql
   ```

1. Check your installed packages:

   ```
   rpm -qa | grep -i percona-server
   ```

1. Enable the Percona Server for MySQL 8.4 repository. The `percona-release setup` command disables the repository of the previous series:

   ```
   sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   sudo percona-release setup ps-84-lts
   ```

1. Upgrade all installed Percona packages together. Running `yum install percona-server-server` upgrades only the server package and leaves the client, shared libraries, and ICU data files on the old version:

   ```
   sudo dnf upgrade 'percona-*'
   ```

1. Verify that every package listed by the following command shows the 8.4 version:

   ```
   rpm -qa | grep -i percona-server
   ```

1. Install the storage engine packages.

   If you used the MyRocks storage engine in the previous version, install the `percona-server-rocksdb` package:

   ```
   sudo yum install percona-server-rocksdb
   ```

1. Modify your configuration file, `my.cnf`, as needed (for example, remove deprecated variables, update settings for 8.4). If you were using plugins that have been replaced by components in 8.4, plan the transition to components. See [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html) for details.

1. Validate the configuration with the new `mysqld` binary before you start the server. If the command reports `unknown variable`, remove that option from the configuration file and run the command again:

   ```
   sudo mysqld --validate-config --user=mysql
   ```

   The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/8.4/en/upgrading-what-is-upgraded.html) .

1. Restart the server:

   ```
   sudo systemctl restart mysql
   ```

After the service has been successfully restarted, you can use the Percona Server for MySQL 8.4.

## Using standalone packages

Use this method when you cannot use repositories or need to install from manually downloaded packages. This method requires you to manually resolve dependencies.

**Debian-derived distributions**

1. Remove the installed packages with their dependencies:

   ```
   sudo apt autoremove percona-server percona-client
   ```

1. Do the required modifications in the database configuration file `my.cnf`.

1. Download the following packages for your architecture:

   - `percona-server-server`
   - `percona-server-client`
   - `percona-server-common`
   - `libperconaserverclient21`

   The following example downloads Percona Server for MySQL 8.4.11-12 packages for Debian 12.0:

   ```
   wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-12/binary/debian/bookworm/x86_64/Percona-Server-8.4.11-12-r57878ff8-bookworm-x86_64-bundle.tar
   ```

1. Unpack the bundle to get the packages:

   ```
   tar xvf Percona-Server-8.4.11-12-r57878ff8-bookworm-x86_64-bundle.tar
   ```

   After you unpack the bundle, you should see the following packages:

   ```
   ls *.deb
   ```

   Expected output

   ```
   libperconaserverclient21-dev_8.4.11-12.bookworm_amd64.deb
   percona-server-dbg_8.4.11-12.bookworm_amd64.deb
   libperconaserverclient21_8.4.11-12.bookworm_amd64.deb      
   percona-server-rocksdb_8.4.11-12.bookworm_amd64.deb
   percona-mysql-router_8.4.11-12.bookworm_amd64.deb
   percona-server-server_8.4.11-12.bookworm_amd64.deb
   percona-server-client_8.4.11-12.bookworm_amd64.deb
   percona-server-source_8.4.11-12.bookworm_amd64.deb
   percona-server-common_8.4.11-12.bookworm_amd64.deb
   percona-server-test_8.4.11-12.bookworm_amd64.deb
   ```

1. Install Percona Server for MySQL:

   ```
   sudo dpkg -i *.deb
   ```

   This command installs the packages from the bundle. Another option is to download or specify only the packages you need for running Percona Server for MySQL installation (`libperconaserverclient21_8.4.11-12.bookworm_amd64.deb`, `percona-server-client_8.4.11-12.bookworm_amd64.deb`, `percona-server-common_8.4.11-12.bookworm_amd64.deb`, and `percona-server-server_8.4.11-12.bookworm_amd64.deb`).

   Warning

   When installing packages manually, you must resolve all the dependencies and install missing packages yourself. At least the following packages should be installed before installing Percona Server for MySQL 8.4.11-12: * `libmecab2` * `libjemalloc1` * `zlib1g-dev` * `libaio1`

1. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/8.4/en/upgrading-what-is-upgraded.html) .

1. Restart the service:

   ```
   sudo service mysql restart
   ```

After the service has been successfully restarted, use the new Percona Server for MySQL 8.4.11-12.

**Red Hat-derived distributions**

1. Check the installed packages:

   ```
   rpm -qa | grep percona-server
   ```

   Expected output

   ```
   percona-server-shared-8.4.11-12.el9.x86_64
   percona-server-shared-compat-8.4.11-12.el9.x86_64
   percona-server-client-8.4.11-12.el9.x86_64
   percona-server-server-8.4.11-12.el9.x86_64
   ```

   You may have the `shared-compat` package, which is required for compatibility.

1. Remove the packages without dependencies:

   ```
   rpm -qa | grep percona-server | xargs rpm -e --nodeps
   ```

   It is important that you remove the packages without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.

   To remove the listed packages, run:

   ```
   rpm -qa | grep '^mysql-' | xargs rpm -e --nodeps
   ```

1. Download the packages of the desired series for your architecture from the [download page](https://www.percona.com/downloads) . The easiest way is to download the bundle which contains all the packages. The following example downloads Percona Server for MySQL 8.4.11-12 packages for RHEL 9:

   ```
   wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-12/binary/redhat/9/x86_64/Percona-Server-8.4.11-12-r9927a2fb-el9-x86_64-bundle.tar
   ```

1. Unpack the bundle to get the packages:

   ```
   tar xvf Percona-Server-8.4.11-12-r9927a2fb-el9-x86_64-bundle.tar
   ```

   After you unpack the bundle, you should see the following packages:

   ```
   ls *.rpm
   ```

1. Install Percona Server for MySQL:

   ```
   sudo rpm -ivh percona-server-server-8.4.11-12.el9.x86_64.rpm \
   percona-server-client-8.4.11-12.el9.x86_64.rpm \
   percona-server-shared-8.4.11-12.el9.x86_64.rpm \
   percona-server-shared-compat-8.4.11-12.el9.x86_64.rpm
   ```

   This command installs only packages required to run the Percona Server for MySQL 8.4.11-12.

   You can install all the packages (for debugging, testing, etc.) with:

   ```
   sudo rpm -ivh *.rpm
   ```

   Note

   When manually installing packages, you must resolve all the dependencies and install missing ones.

1. Modify your configuration file, `my.cnf`, as needed (for example, remove deprecated variables, update settings for 8.4). If you were using plugins that have been replaced by components in 8.4, plan the transition to components. See [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html) for details.

   RHEL or derivatives automatically backs up the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After the upgrade/install process completes, you can restore your configuration from the backup (after removing all unsupported system variables).

1. The mysqld binary automatically runs the upgrade process if needed. To find more information, see [MySQL Upgrade Process](https://dev.mysql.com/doc/refman/8.4/en/upgrading-what-is-upgraded.html) .

1. Restart the server:

   ```
   sudo service mysql restart
   ```

After the service has been successfully restarted, you can use the new Percona Server for MySQL 8.4.11-12.

## Post-upgrade validation

After completing the upgrade, follow the post-upgrade validation steps in the [upgrade checklist](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.html#post-upgrade-validation).

## Further reading

- [Upgrade overview](https://docs.percona.com/percona-server/8.4/upgrade.html)
- [Upgrade checklist for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.html)
- [Upgrade strategies](https://docs.percona.com/percona-server/8.4/upgrade-strategies.html)
- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/8.4/mysql-upgrade-paths.html)
- [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html)
- [Downgrade options](https://docs.percona.com/percona-server/8.4/downgrade.html)
- [Breaking and incompatible changes in 8.4](https://docs.percona.com/percona-server/8.4/8.4-breaking-changes.html)
- [Compatibility and removed items in 8.4](https://docs.percona.com/percona-server/8.4/8.4-compatibility-and-removed-items.html)
- [Defaults and tuning guidance for 8.4](https://docs.percona.com/percona-server/8.4/8.4-defaults-and-tuning.html)
- [Percona Toolkit updates for 8.4](https://docs.percona.com/percona-server/8.4/percona-toolkit-8.4-updates.html)
