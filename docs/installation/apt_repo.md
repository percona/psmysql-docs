# Use an APT repository to install Percona Server for MySQL 8.0

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [Percona downloads](http://www.percona.com/downloads/Percona-Server-8.0/) page.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).


## Install Percona Server for MySQL from Percona `apt` repository

1. Install `GnuPG`, the GNU Privacy Guard:

	```shell
	$ sudo apt install gnupg2 curl
	```
	
2. Fetch the repository packages from Percona web:

	```shell
	$ wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb
	```

3. Install the downloaded package with `dpkg`. To do that, run the following commands as root or with sudo:

	```
	$ sudo dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb
	```
    
4. Once you install this package, the Percona repositories should be added. You
can check the repository setup in the
`/etc/apt/sources.list.d/percona-original-release.list` file.

5. Enable the repository:

	```
	$ sudo percona-release setup ps80
	```

6. After that, you can install the server package:

	```
	$ sudo apt install percona-server-server
	```

!!! note

    Percona Server for MySQL 8.0 comes with the TokuDB storage engine and MyRocks storage engine. These storage engines are installed as plugins.

	Starting with [Percona Server for MySQL 8.0.28-19 (2022-05-12)](../release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. For more information, see [TokuDB Introduction](../tokudb/tokudb_intro.md).
	
	For information on how to install and configure TokuDB, refer to the [TokuDB Installation guide](../tokudb/tokudb_installation.md).
	
	For information on how to install and configure MyRocks, refer to the [Percona MyRocks Installation Guide](../myrocks/install.md).

Percona Server for MySQL contains several useful User Defined Functions (UDF) from Percona Toolkit. After the installation completes, run the following commands to create these functions:

```mysql
mysql -e "CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'"
mysql -e "CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'"
mysql -e "CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'"
```

For more details on the UDFs, see [Percona Toolkit UDFS](https://www.percona.com/doc/percona-server/8.0/management/udf_percona_toolkit.html).

### Percona `apt` Testing repository

Percona offers pre-release builds from the testing repository. To enable it, run
percona-release with the `testing` argument. Run this command as root or by using the sudo command.

```shell
$ sudo percona-release enable ps80 testing
```


