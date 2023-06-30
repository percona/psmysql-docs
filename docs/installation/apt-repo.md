# Use an APT repository to install Percona Server for MySQL 8.0

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [Percona downloads](https://www.percona.com/downloads/Percona-Server-8.0/) page.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).


## Install Percona Server for MySQL using APT

The following code sample updates the repositories, downloads, installs, updates the repositories, sets up the repository, and installs latest version of Percona Server for MySQL:

	```{.bash data-prompt="$"}
	$ sudo apt update
        $ sudo apt install curl
        $ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
        $ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
        $ sudo apt update
        $ sudo percona-release setup ps80
        $ sudo apt install percona-server-server
	```
 
See [Configuring Percona repositories with `percona-release`](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

{% include './snippets/install/_storage-engines.md'%}

Percona Server for MySQL contains user-defined functions from [Percona Toolkit](https://docs.percona.com/percona-toolkit/). These user-defined functions provide faster checksums. For more details on the user-defined functions, see [Percona Toolkit UDF functions](https://www.percona.com/doc/percona-server/8.0/management/udf_percona_toolkit.html).

After the installation completes, run the following commands to create these functions:

```mysql
mysql -e "CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'"
mysql -e "CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'"
mysql -e "CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'"
```

## Install the Percona Testing repository using APT

Percona offers pre-release builds from the testing repository. To enable it, run
percona-release with the `testing` argument. Run the following command as root or use the sudo command:

```{.bash data-prompt="$"}
$ sudo percona-release enable ps80 testing
```

These builds should not be run in production. This build may not contain all of the features available in the final release. The features may change without notice.

