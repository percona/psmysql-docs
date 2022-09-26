# Installing Percona Server for MySQL on Debian and Ubuntu

Ready-to-use packages are available from the *Percona Server for MySQL* software
repositories and the [Percona downloads](http://www.percona.com/downloads/Percona-Server-8.0/) page.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## What’s in each DEB package?

| Package                      | Contains                                                                                                                                                                        |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| percona-server-server   | The database server itself, the mysqld binary and associated files.                                                                                                             |
| percona-server-common        | The files common to the server and client.                                                                                                                                      |
| percona-server-client        | The command line client.                                                                                                                                                        |
| percona-server-dbg           | Debug symbols for the server.                                                                                                                                                   |
| percona-server-test          | The database test suite.                                                                                                                                                        |
| percona-server-source        | The server source.                                                                                                                                                              |
| libperconaserverclient21-dev | Header files needed to compile software to use the client library.                                                                                                              |
| libperconaserverclient21     | The client-shared library. The version is incremented when there is an ABI change that requires software using the client library to be recompiled or its source code modified. |

## Installing *Percona Server for MySQL* from Percona `apt` repository


1. Install `GnuPG`, the GNU Privacy Guard:

	```shell
	$ sudo apt install gnupg2 curl
	```


2. Fetch the repository packages from Percona web:

	```shell
	$ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
	```


3. Install the downloaded package with **dpkg**. To do that, run the following commands as root or with **sudo**:

	```
	$ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
	```


4. Once you install this package the Percona repositories should be added. You
can check the repository setup in the
`/etc/apt/sources.list.d/percona-original-release.list` file.


5. Enable the repository:

	```
	$ sudo percona-release setup ps80
	```


6. After that you can install the server package:

	```
	$ sudo apt install percona-server-server
	```

!!! note

    Percona Server for MySQL 8.0 comes with the TokuDB storage engine and MyRocks storage engine. These storage engines are installed as plugins.

Starting with [Percona Server for MySQL 8.0.28-19 (2022-05-12)](../release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. For more information, see [TokuDB Introduction](../tokudb/tokudb_intro.md).

For information on how to install and configure *TokuDB*, refer to the [TokuDB Installation guide](../tokudb/tokudb_installation.md).

For information on how to install and configure *MyRocks*, refer to the [Percona MyRocks Installation Guide](../myrocks/install.md).

*Percona Server for MySQL* contains several useful User Defined Functions (UDF) from Percona Toolkit. After the installation completes, run the following commands to create these functions:

```mysql
mysql -e "CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'"
mysql -e "CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'"
mysql -e "CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'"
```

For more details on the UDFs, see [Percona Toolkit UDFS](https://www.percona.com/doc/percona-server/8.0/management/udf_percona_toolkit.html).

### Percona `apt` Testing repository

Percona offers pre-release builds from the testing repository. To enable it, run
**percona-release** with the `testing` argument. Run this command as root or by using the **sudo** command.

```shell
$ sudo percona-release enable ps80 testing
```

### Apt-Pinning the packages

Pinning allows you to stay on a release and get packages from a different version. In some cases, you can pin selected packages and avoid accidentally upgrading all the packages. 

 The pinning takes place in the `preference` file. To pin a package, set the `Pin-Priority` to higher numbers. 
 
 Make a new file `/etc/apt/preferences.d/00percona.pref`. For example, add the following to the `preference` file:

```text
Package: *
Pin: release o=Percona Development Team
Pin-Priority: 1001
```

For more information about the pinning, you can check the official [debian wiki](http://wiki.debian.org/AptPreferences).

## Installing *Percona Server for MySQL* using downloaded deb packages

Download the packages of the desired series for your architecture from the
[Percona downloads](http://www.percona.com/downloads/Percona-Server-8.0/) page. The easiest way is to download the bundle which contains
all the packages. The following example downloads [Percona Server for MySQL 8.0.13-3](../release-notes/Percona-Server-8.0.13-3.md)


 release packages for Debian 9.0 (stretch):

```
$ wget https://www.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.13-3/binary/debian/stretch/x86_64/percona-server-8.0.13-3-r63dafaf-stretch-x86_64-bundle.tar
```

You should then unpack the bundle to get the packages:

```
$ tar xvf percona-server-8.0.13-3-r63dafaf-stretch-x86_64-bundle.tar
```

After you unpack the bundle you should see the following packages:

```
$ ls *.deb
```

Now, you can install *Percona Server for MySQL* using **dpkg**. Run this command as root or by using the **sudo** command

```
$ sudo dpkg -i *.deb
```

This will install all the packages from the bundle. Another option is to
download/specify only the packages you need for running *Percona Server for MySQL*
installation (`libperconaserverclient21_8.0.13-3-1.stretch_amd64.deb`,
`percona-server-client_8.0.13-3-1.stretch_amd64.deb`,
`percona-server-common_8.0.13-3-1.stretch_amd64.deb`, and
`percona-server-server_8.0.13-3-1.stretch_amd64.deb`. Optionally, you can install
`percona-server-tokudb_8.0.13-3-1.stretch_amd64.deb` if you want the *TokuDB*
storage engine).

!!! note

    *Percona Server for MySQL* 8.0 comes with the TokuDB storage engine. You can find more information on how to install and enable the *TokuDB* storage in the TokuDB Installation guide.

Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. For more information, see TokuDB Introduction.

!!! warning

    When installing packages manually like this, you’ll need to make sure to resolve all the dependencies and install missing packages yourself. Following packages will need to be installed before you can manually install Percona Server: `mysql-common`, `libjemalloc1`, `libaio1`, and `libmecab2`

## Running *Percona Server for MySQL*

*Percona Server for MySQL* stores the data files in `/var/lib/mysql/` by
default. You can find the configuration file that is used to manage *Percona Server for MySQL* in `/etc/mysql/my.cnf`.

!!! note

    *Debian* and *Ubuntu* installation doesn’t automatically create a special `debian-sys-maint` user which can be used by the control scripts to control the *Percona Server for MySQL* `mysqld` and `mysqld_safe` services which was the case with previous *Percona Server for MySQL* versions. If you still require this user you’ll need to create it manually.

Run the following commands as root or by using the **sudo** command


1. Starting the service

	*Percona Server for MySQL* is started automatically after it gets installed unless it
	encounters errors during the installation process. You can also manually
	start it by running: `service mysql start`


2. Confirming that service is running. You can check the service status by
	running: `service mysql status`


3. Stopping the service

	You can stop the service by running: `service mysql stop`


4. Restarting the service. `service mysql restart`

!!! note

    Debian 9.0 (stretch) and Ubuntu 18.04 LTS (bionic) come with [systemd](http://freedesktop.org/wiki/Software/systemd/) as the default system and service manager. You can invoke all the above commands with `systemctl` instead of `service`. Currently, both are supported.

## Working with AppArmor

For information on AppArmor, see [Working with AppArmor](../security/apparmor.md).

## Uninstalling *Percona Server for MySQL*

To uninstall *Percona Server for MySQL* you’ll need to remove all the installed
packages. Removing packages with apt remove does not remove the
configuration and data files. Removing the packages with apt purge does remove the packages with configuration files and data files (all
the databases). Depending on your needs you can choose which command better
suits you.


1. Stop the *Percona Server for MySQL* service: `service mysql stop`


2. Remove the packages


    1. Remove the packages. This will leave the data files (databases, tables, logs, configuration, etc.) behind. In case you don’t need them you’ll need to remove them manually: `apt remove percona-server\*`


    2. Purge the packages. This command removes all the packages and deletes all the data files (databases, tables, logs, and so on.): `apt purge percona-server\*`


