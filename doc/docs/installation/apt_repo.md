# Installing Percona Server for MySQL 5.7 on Debian and Ubuntu

!!! note

    The following instructions install Percona Server for MySQL 5.7. 
    The instructions to install [Percona Server for MySQL 8.0 are available at this location](https://docs.percona.com/percona-server/latest/installation/apt_repo.html).

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [download page](http://www.percona.com/downloads/Percona-Server-5.7/).

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## What’s in each DEB package?

The `percona-server-server-5.7` package contains the database server itself, the `mysqld` binary and associated files.

The `percona-server-common-5.7` package contains files common to the server and client.

The `percona-server-client-5.7` package contains the command line client.

The `percona-server-5.7-dbg` package contains debug symbols for the server.

The `percona-server-test-5.7` package contains the database test suite.

The `percona-server-source-5.7` package contains the server source.

The `libperconaserverclient20-dev` package contains header files needed to compile software to use the client library.

The `libperconaserverclient20` package contains the client shared library. The `18.1` is a reference to the version of the shared library. The version is incremented when there is a ABI change that requires software using the client library to be recompiled or its source code modified.

## Installing Percona Server for MySQL from Percona `apt` repository

1. Update package repositories:

```shell
$ sudo apt update
```

2. Install `GnuPG`, the GNU Privacy Guard:

```shell
$ sudo apt install gnupg2
```

3. Fetch the repository packages from Percona web:

```shell
$ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
```

4. Install the downloaded package with **dpkg**. To do that, run the following commands as root or with **sudo**:

```shell
$ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
```

  Once you install this package, the Percona repositories should be added. You can check the repository setup in the `/etc/apt/sources.list.d/percona-original-release.list` file.

5. Remember to update the local cache:

```shell
$ sudo apt update
```

Once you install this package the Percona repositories should be added. You can check the repository setup in the `/etc/apt/sources.list.d/percona-release.list` file.

6. After that you can install the server package:

```shell
$ sudo apt install percona-server-server-5.7
```

!!! note

    Percona Server for MySQL 5.7 comes with the TokuDB storage engine and MyRocks storage engine. These storage engines are installed as plugin.

For information on how to install and configure TokuDB, refer to the TokuDB Installation guide.

For information on how to install and configure MyRocks, refer to the Percona MyRocks Installation Guide guide.

The Percona Server for MySQL distribution contains several useful User Defined Functions (UDF) from Percona Toolkit. After the installation completes, run the following commands to create these functions:

```shell
$ mysql -e "CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'"
$ mysql -e "CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'"
$ mysql -e "CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'"
```

For more details on the UDFs, see [Percona Toolkit UDFS](https://www.percona.com/doc/percona-server/5.7/management/udf_percona_toolkit.html).

### Percona `apt` Testing repository

Percona offers pre-release builds from the testing repository. To enable it, run
**percona-release** with the `testing` argument. Run this command as root or by using the **sudo** command.

```shell
$ sudo percona-release enable original testing
```

### Apt-Pinning the packages

In some cases, you might need to [pin](https://wiki.debian.org/AptConfiguration?action=show&redirect=AptPinning) the selected packages to avoid upgrades from the distribution repositories. Create a new file `/etc/apt/preferences.d/00percona.pref` and add the following lines:

```text
Package: *
Pin: release o=Percona Development Team
Pin-Priority: 1001
```

## Installing Percona Server for MySQL using downloaded deb packages

Download the packages of the desired series for your architecture from the [download page](http://www.percona.com/downloads/Percona-Server-5.7/). The easiest way is to download bundle which contains all the packages. Following example will download Percona Server for MySQL Percona Server for MySQL 5.7.10-3 release packages for *Debian* 8.0:

```shell
$ wget https://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.10-3/binary/debian/jessie/x86_64/Percona-Server-5.7.10-3-r63dafaf-jessie-x86_64-bundle.tar
```

You should then unpack the bundle to get the packages:

```shell
$ tar xvf Percona-Server-5.7.10-3-r63dafaf-jessie-x86_64-bundle.tar
```

After you unpack the bundle you should see the following packages:

```shell
$ ls *.deb
```

The output could be this:

```text
libperconaserverclient20-dev_5.7.10-3-1.jessie_amd64.deb
libperconaserverclient20_5.7.10-3-1.jessie_amd64.deb
percona-server-5.7-dbg_5.7.10-3-1.jessie_amd64.deb
percona-server-client-5.7_5.7.10-3-1.jessie_amd64.deb
percona-server-common-5.7_5.7.10-3-1.jessie_amd64.deb
percona-server-server-5.7_5.7.10-3-1.jessie_amd64.deb
percona-server-source-5.7_5.7.10-3-1.jessie_amd64.deb
percona-server-test-5.7_5.7.10-3-1.jessie_amd64.deb
percona-server-tokudb-5.7_5.7.10-3-1.jessie_amd64.deb
```

Now you can install Percona Server for MySQL by running:

```shell
$ sudo dpkg -i *.deb
```

This will install all the packages from the bundle. Another option is to download/specify only the packages you need for running Percona Server for MySQL installation (`libperconaserverclient20_5.7.10-3-1.jessie_amd64.deb`, `percona-server-client-5.7_5.7.10-3-1.jessie_amd64.deb`, `percona-server-common-5.7_5.7.10-3-1.jessie_amd64.deb`, and `percona-server-server-5.7_5.7.10-3-1.jessie_amd64.deb`. Optionally you can install `percona-server-tokudb-5.7_5.7.10-3-1.jessie_amd64.deb` if you want TokuDB storage engine).

!!! note

    Percona Server for MySQL 5.7 comes with the TokuDB storage engine. You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

!!! warning

    When installing packages manually like this, you’ll need to make sure to resolve all the dependencies and install missing packages yourself. Following packages will need to be installed before you can manually install Percona Server: `mysql-common`, `libjemalloc1`, `libaio1` and `libmecab2`

### AppArmor settings

AppArmor is a kernel-integrated system which controls how applications access the file system by creating application profiles. If the installation of MySQL adds an AppArmor profile, you can find the profile in the following locations:

* /etc/apparmor.d/usr.sbin.mysqld

* /etc/apparmor.d/local/usr.sbin.mysqld

The `local` version contains only comments. Add any changes specific for the server to the `local` file.

The `usr.sbin.mysqld` file has the following settings:

```text
#include <tunables/global>

/usr/sbin/mysqld {
  ...
  # Allow data dir access
  /var/lib/mysql/ r,
  /var/lib/mysql/** rwk,

  # Allow data files dir access
    /var/lib/mysql-files/ r,
    /var/lib/mysql-files/** rwk,

  # Allow keyring dir access
    /var/lib/mysql-keyring/ r,
    /var/lib/mysql-keyring/** rwk,

  # Allow log file access
    /var/log/mysql/ r,
    /var/log/mysql/** rw,
  ...
}
```

The settings govern how the files are accessed. For example, the data file directory access gives read (r) access to a directory and read, write, and lock access (rwk) to all directories and files underneath `/mysql/`.

You should download the apparmor-utils package when you are working with existing AppArmor profiles. The utilities allow you to edit a profile without stopping AppArmor or removing the profile.

Before you edit a profile, change the profile to `complain` mode:

```shell
$ aa-complain /usr/sbin/mysqld
```

The output could be the following:

```text
setting /usr/sbin/mysqld to complain mode
```

In complain mode, you can edit the profile to add settings because you have relocated the data directory: `/<volume>/dev/percona/data`:

```text
    /<volume>/percona/data/ r,
    /<volume>/percona/data/** rwk,


You may need to reload AppArmor or reload the specific AppArmor profile to apply the changes.
```

You can also modify the `/etc/apparmor.d/tunables/alias` file as follows:

```shell
$ alias /var/lib/mysql -/volume/percona/data/
```

To reload one profile, run the following command:

```shell
$ sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.mysqld
```

Restart AppArmor with the following command:

```shell
$ sudo systemctl restart apparmor
```

You can also disable AppArmor, but this action is not recommended. For earlier Ubuntu systems, prior to 16.04, use the following command:

```shell
$ sudo systemctl stop apparmor
$ sudo update-rc.d -f apparmor remove
```

For later Ubuntu systems, use the following:

```shell
$ sudo sudo systemctl stop apparmor
$ sudo systemctl disable apparmor
```

The following table lists the default locations for files:

| Files | Location |
| --- | --- |
| mysqld server | /usr/sbin |
| Configuration | /etc/mysql/my.cnf |
| Data directory | /var/lib/mysql |
| Logs | /var/log/mysql |

!!! note

    *Debian* and *Ubuntu* installation does not automatically create a special `debian-sys-maint` user which can be used by the control scripts to control the Percona Server for MySQL `mysqld` and `mysqld_safe` services like it was the case with previous Percona Server for MySQL versions. If you still require this user you must create the user manually.

## Running Percona Server for MySQL

The following procedure runs the Percona Server for MySQL:

1. Starting the service

Percona Server for MySQL starts automatically after installation unless the server
encounters errors during the installation process. You can also manually
start it by running the following command:

```shell
$ sudo service mysql start
```

2. Confirming the service is running

You can verify the service status by running the following command:

```shell
$ service mysql status
```

3. Stopping the service

You can stop the service by running the following command:

```shell
S sudo service mysql stop
```

4. Restarting the service

You can restart the service by running the following command:

```shell
S sudo service mysql restart
```

!!! note

    *Debian* 8.0 (jessie) and *Ubuntu* 16.04(Xenial) come with [systemd](http://freedesktop.org/wiki/Software/systemd/) as the default system and service manager so you can invoke all the above commands with `sytemctl` instead of `service`. Currently, both are supported.

## Uninstalling Percona Server for MySQL

To uninstall Percona Server for MySQL, you must remove all of the installed packages.

You have the following options:

* Removing packages with **apt remove** leaves the configuration and data files.

* Removing the packages with **apt purge** removes all the packages with configuration files and data files (all the databases).

Depending on your needs, you can choose which command better suits you.

1. Stop the Percona Server for MySQL service

```shell
$ sudo service mysql stop
```

2. Remove the packages

    1. Remove the packages. This option does not delete the configuration or data files. If you do not require these files, you must delete each file manually.

    ```shell
    $ sudo apt remove 'percona-server*'
    ```

    1. Purge the packages. This option deletes packages, configuration, and data files. The option does not delete any configuration or data files stored in your home directory. You may need to delete some files manually.

    ```shell
    $ sudo apt purge 'percona-server*'
    $ sudo apt autoremove -y
    $ sudo apt autoclean
    $ sudo rm -rf /etc/mysql
    ```

!!! note

    In a regular expression, the `\*` (asterisk) matches zero or more of the preceding item. The single quotes prevent the shell from misinterpreting the asterisk as a shell command.

If you do not plan to upgrade, run the following commands to remove the data directory location:

```shell
$ rm -rf /var/lib/mysql
$ rm -rf /var/log/mysql
$ sudo apt purge percona-server*
```
