
# Upgrading using Standalone Packages

You can also upgrade to _Percona Server for MySQL_ using standalone 
packages.

## DEB-based distributions

After taking a full backup and dump, if possible, stop the server:

```shell
$ sudo /etc/init.d/mysql stop
```

Remove the installed packages with their dependencies:

```shell
$ sudo apt autoremove percona-server-server-5.6 percona-server-client-5.6
```

Once removed, proceed to do the modifications needed in your 
configuration file. 

Then, download the following packages for your architecture:

> 
> * `percona-server-server-5.7`


> * `percona-server-client-5.7`


> * `percona-server-common-5.7`


> * `libperconaserverclient20`

Following example will download Percona Server for MySQL Percona Server for MySQL 5.7.10-3 release packages for *Debian* 8.0:

```shell
$ wget https://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.10-3/binary/debian/jessie/x86_64/Percona-Server-5.7.10-3-r63dafaf-jessie-x86_64-bundle.tar
```

You should then unpack the bundle to get the packages:

```shell
$ tar xvf Percona-Server-5.7.10-3-r63dafaf-jessie-x86_64-bundle.tar
```

After you unpack the bundle, run `ls` to view the available packages:

```shell
$ ls *.deb
```
The output should be similar to the following:

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

**NOTE**: Percona Server for MySQL 5.7 comes with the TokuDB storage engine. You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

**WARNING**: When installing packages manually, resolve all the 
dependencies and install any missing packages. The following 
packages should be installed before installing Percona Server for MySQL 5.7: `libmecab2`, `libjemalloc1`, `zlib1g-dev`, and `libaio1`.

The installation script will not run automatically **mysql_upgrade**, so you’ll need to run it yourself and restart the service afterwards.

### RPM-based distributions

Having done the full backup (and dump if possible), stop the server:

```shell
$ service mysql stop
```

and check your installed packages:

```shell
$ rpm -qa | grep Percona-Server
```
The output should be similar to the following:

```text
Percona-Server-shared-56-5.6.28-rel76.1.el6.x86_64
Percona-Server-server-56-5.6.28-rel76.1.el6.x86_64
Percona-Server-client-56-5.6.28-rel76.1.el6.x86_64
Percona-Server-tokudb-56-5.6.28-rel76.1.el6.x86_64
```

You may have a fourth, `shared-compat`, which is for compatibility purposes.

After checked that, proceed to remove them without dependencies:

```shell
$ rpm -qa | grep Percona-Server | xargs rpm -e --nodeps
```

It is important that you remove it without dependencies as many packages may depend on these (as they replace `mysql`) and will be removed if omitted.

Note that this procedure is the same for upgrading from MySQL 5.6 to Percona Server for MySQL 5.7, just grep `'^mysql-'` instead of `Percona-Server` and remove them.

Download the packages of the desired series for your architecture from the [download page](http://www.percona.com/downloads/Percona-Server-5.7/). The easiest way is to download bundle which contains all the packages. Following example will download Percona Server for MySQL 5.7.10-3 release packages for *CentOS* 7:

```shell
$ wget https://www.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.10-3/binary/redhat/7/x86_64/Percona-Server-5.7.10-3-r63dafaf-el7-x86_64-bundle.tar
```

You should then unpack the bundle to get the packages:

```shell
$ tar xvf Percona-Server-5.7.10-3-r63dafaf-el7-x86_64-bundle.tar
```

After you unpack the bundle you should see the following packages:

```shell
$ ls *.rpm
```
The output should be similar to the following:

```text
Percona-Server-57-debuginfo-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-client-57-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-devel-57-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-server-57-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-shared-57-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-shared-compat-57-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-test-57-5.7.10-3.1.el7.x86_64.rpm
Percona-Server-tokudb-57-5.7.10-3.1.el7.x86_64.rpm
```

Now you can install Percona Server for MySQL 5.7 by running:

```shell
rpm -ivh Percona-Server-server-57-5.7.10-3.1.el7.x86_64.rpm \
Percona-Server-client-57-5.7.10-3.1.el7.x86_64.rpm \
Percona-Server-shared-57-5.7.10-3.1.el7.x86_64.rpm
```

This will install only packages required to run the Percona Server for MySQL 5.7. Optionally you can install TokuDB storage engine by adding the `Percona-Server-tokudb-57-5.7.10-3.1.el7.x86_64.rpm` to the command above. You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

To install all the packages (for debugging, testing, etc.) you should run:

```shell
$ rpm -ivh *.rpm
```

**NOTE**: When installing packages manually like this, you’ll need to make sure to resolve all the dependencies and install missing packages yourself.

Once installed, proceed to modify your configuration file - `my.cnf` - and install the plugins if necessary. If you’re using TokuDB storage engine you’ll need to comment out all the TokuDB specific variables in your configuration file(s) before starting the server, otherwise server won’t be able to start. *RHEL*/*CentOS* 7 automatically backs up the previous configuration file to `/etc/my.cnf.rpmsave` and installs the default `my.cnf`. After upgrade/install process completes you can move the old configuration file back (after you remove all the unsupported system variables).

As the schema of the grant table has changed, the server must be started without reading them:

```shell
$ service mysql start
```

and use `mysql_upgrade` to migrate to the new grant tables, it will rebuild the indexes needed and do the modifications needed:

**NOTE**: If you’re using TokuDB storage engine you’ll need re-enable the storage engine plugin by running the: `ps-admin --enable-tokudb` before running `mysql_upgrade` otherwise you’ll get errors.

```shel
$ mysql_upgrade
```

After this is done, just restart the server as usual:

```shell
$ service mysql restart
```
