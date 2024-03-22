# Use an APT repository to install Percona Server for MySQL 8.0

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [Percona downloads](https://www.percona.com/downloads/Percona-Server-8.0/) page.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

We gather [Telemetry data] in the Percona packages and Docker images.

## Install Percona Server for MySQL using APT

1. This command line instruction uses the `apt` command to update the package lists for upgrades and new package installations.

	*	`sudo` is a command that allows you to run programs with the security privileges of another user, by default, as the superuser. Updating the package lists typically requires superuser or 'root' privileges.

	*	`apt` is a command-line interface that handles package management in Debian and its derivatives. 

	* `update` option resynchronizes the package index files from the sources specified in the system's `sources.list` file. You should run this command regularly to get the latest package updates.


	```{.bash data-prompt="$"}
	$ sudo apt update
	```

2. This command line instruction uses superuser privileges to install the `curl` package using the `apt` package manager. `curl` is a command-line tool used to transfer data using various network protocols.

	```{.bash data-prompt="$"}
	$ sudo apt install curl
	```
	
3. This command line instruction uses `curl` to download the `percona-release_latest.generic_all.deb` file from the `https://repo.percona.com/apt` location.

	The `-0` option saves the downloaded file with the same name used in the URL.

	```{.bash data-prompt="$"}
	$ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
	```

4. The following command uses the `apt` command to install multiple packages. `gnupg2` is the GNU Privacy Guard that provides cryptographic privacy and authentication. `lsb-release` is a Linux utility that provides certain Linux Standard Base (LSB) and distribution-specific information. `./percona-release_latest.generic_all.deb` is a Debian package in the current directory. 


	```{.bash data-prompt="$"}
	$ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
	```
    

5. The following command uses superuser privileges to update the package lists from the repositories so that the system knows about the latest versions of packages and their dependencies.

	```{.bash data-prompt="$"}
	$ sudo apt update
	```

6. This command line instruction uses `percona-release` command, a tool provided by Percona, to set up a specific Percona Server version. 

	```{.bash data-prompt="$"}
	$ sudo percona-release setup ps80
	```

7. You can check the repository setup for the Percona original release list in `/etc/apt/sources.list.d/percona-original-release.list`. The APT system uses this file to know where to find updates and new packages for Percona software.

8. This command uses the `apt` command to install the `percona-server-server` package.

	```{.bash data-prompt="$"}
	$ sudo apt install percona-server-server
	```

See [Configuring Percona repositories with `percona-release`](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.


Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. For more information, see the [TokuDB Introduction](tokudb-intro.md) and [TokuDB version changes](tokudb-version-changes.md). 

Percona Server for MySQL contains user-defined functions from the [Percona Toolkit](https://docs.percona.com/percona-toolkit/). These user-defined functions provide faster checksums. For more details on the user-defined functions, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

After the installation completes, run the following commands to create these functions:

```mysql
mysql -e "CREATE FUNCTION fnv1a_64 RETURNS INTEGER SONAME 'libfnv1a_udf.so'"
mysql -e "CREATE FUNCTION fnv_64 RETURNS INTEGER SONAME 'libfnv_udf.so'"
mysql -e "CREATE FUNCTION murmur_hash RETURNS INTEGER SONAME 'libmurmur_udf.so'"
```

## Install the Percona Testing repository using APT

Percona offers pre-release builds from the testing repository. As a superuser, run `percona-release` with the `testing` argument to enable it.

```{.bash data-prompt="$"}
$ sudo percona-release enable ps80 testing
```

Do not run testing repository builds in production. The build may not contain all the features available in the final release and may change without notice.

[Telemetry data]: telemetry.md
