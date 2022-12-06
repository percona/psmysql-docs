# Install Percona Server for MySQL 8.0 using downloaded DEB packages

Download the packages of the desired series for your architecture from the
[Percona downloads](http://www.percona.com/downloads/Percona-Server-8.0/) page. The easiest way is to download the bundle, which contains
all the packages. The following example downloads [Percona Server for MySQL 8.0.13-3](../release-notes/Percona-Server-8.0.13-3.md) release packages for Debian 9.0 (stretch):

```
$ wget https://www.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.13-3/binary/debian/stretch/x86_64/percona-server-8.0.13-3-r63dafaf-stretch-x86_64-bundle.tar
```

It would help if you then unpacked the bundle to get the packages:

```
$ tar xvf percona-server-8.0.13-3-r63dafaf-stretch-x86_64-bundle.tar
```

After you unpack the bundle, you should see the following packages:

```
$ ls .deb
```

Now, you can install Percona Server for MySQL using `dpkg`. Run this command as root or use the sudo command:

```
$ sudo dpkg -i .deb
```

This will install all the packages from the bundle. Another option is to
download/specify only the packages you need for running Percona Server for MySQL
installation (`libperconaserverclient21_8.0.13-3-1.stretch_amd64.deb`,
`percona-server-client_8.0.13-3-1.stretch_amd64.deb`,
`percona-server-common_8.0.13-3-1.stretch_amd64.deb`, and
`percona-server-server_8.0.13-3-1.stretch_amd64.deb`. Optionally, you can install
`percona-server-tokudb_8.0.13-3-1.stretch_amd64.deb` if you want the TokuDB
storage engine).

!!! note

    Percona Server for MySQL 8.0 comes with the TokuDB storage engine. You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

	Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. For more information, see the TokuDB Introduction.

!!! warning

    When installing packages manually like this, you’ll need to resolve all the dependencies and install missing packages yourself. The following packages will need to be installed before you can manually install Percona Server: `mysql-common`, `libjemalloc1`, `libaio1`, and `libmecab2`.
