# Installing Percona Server for MySQL 5.7 on Red Hat Enterprise Linux and CentOS

!!! note

    The following instructions install Percona Server for MySQL 5.7 using the Yum repository. 
    The instructions to install [Percona Server for MySQL 8.0 using the Yum repository are available at this location](https://docs.percona.com/percona-server/latest/installation/yum_repo.html).

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [download page](http://www.percona.com/downloads/Percona-Server-5.7/). The Percona **yum** repository supports popular *RPM*-based operating systems, including the *Amazon Linux AMI*.

The easiest way to install the *Percona Yum* repository is to install an *RPM* that configures **yum** and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

**NOTE**: The RPM packages for Red Hat Enterprise Linux 7 (and compatible derivatives) do not support TLSv1.3, as it requires OpenSSL 1.1.1, which is currently not available on this platform.

## What’s in each RPM package?

Each of the Percona Server for MySQL RPM packages have a particular purpose.

The `Percona-Server-server-57` package contains the server itself (the `mysqld` binary).

The `Percona-Server-57-debuginfo` package contains debug symbols for the server.

The `Percona-Server-client-57` package contains the command line client.

The `Percona-Server-devel-57` package contains the header files needed to compile software using the client library.

The `Percona-Server-shared-57` package includes the client shared library.

The `Percona-Server-shared-compat` package includes shared libraries for software compiled against old versions of the client library. Following libraries are included in this package: `libmysqlclient.so.12`, `libmysqlclient.so.14`, `libmysqlclient.so.15`, `libmysqlclient.so.16`, and `libmysqlclient.so.18`.

The `Percona-Server-test-57` package includes the test suite for Percona Server for MySQL.

## Installing Percona Server for MySQL from Percona `yum` repository


1. Install the Percona repository

You can install Percona yum repository by running the following command as a
`root` user or with sudo:

>$ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm

2. RHEL 8 and other EL8 systems enable the MySQL module by default.
> This module hides the Percona-provided packages and the module must be 
> disabled to make these packages visible. 
> The following command disables the module:
> 
> ```shell
> $ sudo yum module disable mysql
> ```


3. Enable the Percona Server 5.7 repository:

```shell
# percona-release setup ps57
```
The output should resemble the following:

```text
* Disabling all Percona Repositories
* Enabling the Percona Server 5.7 repository
* Enabling the Percona XtraBackup 2.4 repository
```


4. Test the repository. Make sure packages are available from the 
   repository by executing the 
`yum list` command. We filter the results by the version number:

```
$ yum list | grep 5.7.38-41.1
```

The output should be similar to the following:

```text
...
Percona-Server-57-debuginfo.x86_64                     5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-57-debugsource.x86_64                   5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-client-57-debuginfo.x86_64              5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-rocksdb-57.x86_64                       5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-rocksdb-57-debuginfo.x86_64             5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-server-57-debuginfo.x86_64              5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-shared-57-debuginfo.x86_64              5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-shared-compat-57.x86_64                 5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-test-57-debuginfo.x86_64                5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-tokudb-57.x86_64                        5.7.38-41.1.el8                                           percona-release-x86_64
Percona-Server-tokudb-57-debuginfo.x86_64              5.7.38-41.1.el8                                           percona-release-x86_64
...
```


5. Install the packages. You can install _Percona Server for MySQL_ by 
   running the following command:

```shell
> $ yum install Percona-Server-server-57
```

**NOTE**: Percona Server for MySQL 5.7 comes with the TokuDB storage engine. You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

### Percona yum Testing repository

Percona offers pre-release builds from our testing repository. To subscribe to the testing repository, you’ll need to enable the testing repository in `/etc/yum.repos.d/percona-release.repo`. To do so, set both `percona-testing-$basearch` and `percona-testing-noarch` to `enabled = 1` (Note that there are 3 sections in this file: release, testing and experimental - in this case it is the second section that requires updating). **NOTE:** You’ll need to install the Percona repository first (ref above) if this hasn’t been done already.

## Installing Percona Server for MySQL using downloaded rpm packages


1. Download the packages of the desired series for your architecture from the [download page](http://www.percona.com/downloads/Percona-Server-5.7/). The easiest way is to download bundle which contains all the packages. Following example will download Percona Server for MySQL 5.7.31-34 release packages for *CentOS* 7:

```
$ wget https://www.percona.com/downloads/Percona-Server-5.
7/Percona-Server-5.7.31-34/binary/redhat/7/x86_64/Percona-Server-5.7.31-34-r2e68637-el7-x86_64-bundle.tar
```


2. You should then unpack the bundle to get the packages:

```
$ tar xvf Percona-Server-5.7.31-34-r2e68637-el7-x86_64-bundle.tar
```

After you unpack the bundle you should see the following packages:

```shell
$ ls *.rpm
```
The output should be similar to the following:
```text
Percona-Server-57-debuginfo-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-client-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-devel-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-rocksdb-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-server-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-shared-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-shared-compat-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-test-57-5.7.31-34.1.el7.x86_64.rpm
Percona-Server-tokudb-57-5.7.31-34.1.el7.x86_64.rpm
```


3. Run the following command to Percona Server for 
   MySQL 5.7:

```shell
$ rpm -ivh Percona-Server-server-57-5.7.31-34.1.el7.x86_64.rpm \
Percona-Server-client-57-5.7.31-34.1.el7.x86_64.rpm \
Percona-Server-shared-57-5.7.31-34.1.el7.x86_64.rpm
```

This will install only packages required to run the Percona Server for MySQL 5.7.

Optionally, you can install either the TokuDB storage engine, adding `Percona-Server-tokudb-57-5.7.31-34.1.el7.x86_64.rpm`  or the MyRocks storage engine, adding `Percona-Server-rocksdb-57-5.7.31-34.1.el7.x86_64.rpm` to the install command.

You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

You can find more information on how to install and enable the MyRocks storage engine in the Percona MyRocks Installation Guide guide.

To install all the packages (for debugging, testing, etc.) run the 
following command:

```
$ rpm -ivh *.rpm
```

**NOTE**: When installing packages manually, you must resolve all dependencies and install any missing packages.

The following table lists the default locations for files:

|Files|Location|
|--- |--- |
|mysqld server|/usr/bin|
|Configuration|/etc/my.cnf|
|Data directory|/var/lib/mysql|
|Logs|/var/log/mysqld.log|

You can use the following command to locate the Data directory:

```shell
$ grep datadir /etc/my.cnf
```
The output should resemble the following:
```text
datadir=/var/lib/mysql
```

## Running Percona Server for MySQL

**NOTE**: *RHEL* 7 and *CentOS* 7 come with [systemd](http://freedesktop.org/wiki/Software/systemd/) as the default system and service manager so you can invoke all the above commands with `sytemctl` instead of `service`. Currently both are supported.


1. Starting the service

Percona Server for MySQL does not start automatically on *RHEL* and *CentOS* after
the installation. Start the server by running the following command:

```shell
$ service mysql start
```


2. Confirm that service is running by running the following command:


```shell
$ service mysql status
```


3. Stop the service by running the following command:

```shell
$ service mysql stop
```


4. Restart the service by running the following command:

```shell
$ service mysql restart
```

**NOTE**: The *RHEL* 8 distributions and derivatives have added [system-wide cryptographic policies component](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening). This component allows the configuration of cryptographic subsystems.

## Uninstalling Percona Server for MySQL

To completely uninstall Percona Server for MySQL you must remove all the 
installed packages and data files.


1. Stop the Percona Server for MySQL service

```shell
$ service mysql stop
```


2. Remove the packages

```shell
$ yum remove Percona-Server*
```


3. Remove the data and configuration files:

**WARNING**: This command removes all the packages and deletes all the 
data files (databases, tables, logs, etc.). Take a 
backup in case you need the data.

```shell
$ rm -rf /var/lib/mysql
$ rm -f /etc/my.cnf
```


