# Use an APT repository to install Percona Server for MySQL {{vers}}

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [Percona downloads :octicons-link-external-16:](https://www.percona.com/downloads/Percona-Server-{{vers}}/) page.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<--- "get-help-snip.md"

## Version changes

Percona supports DEB builds with ARM packages with the `arm64.deb` extension on supported Debian and Ubuntu releases.

## Unattended installations

--8<-- "install-flag.md"

## Install Percona Server for MySQL using APT

Run the following commands as a `root` user or with sudo:

```shell
sudo apt update
sudo apt install curl
curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
sudo apt update
sudo percona-release enable-only {{pkg}} release
sudo apt install percona-server-server
```

In MySQL 8.4, the `mysql_native_password` plugin is no longer loaded by default. When the package manager prompts you during installation, you must follow the choices and steps in [Configure authentication](#configure-authentication). If you choose legacy authentication but do not enable the plugin in configuration, clients may be unable to connect or the service may fail to start.

The following sections provide detailed explanations for each step:

1. This command updates the package lists for upgrades and new package installations. `sudo` runs the command with superuser privileges; `apt update` resynchronizes the package index files from the sources in your system's `sources.list`.

	```shell
	sudo apt update
	```

2. This command installs the `curl` package. `curl` is a command-line tool used to transfer data over networks and is required to download the Percona repository package.

	```shell
	sudo apt install curl
	```

3. This command downloads the `percona-release_latest.generic_all.deb` file from the Percona APT repository. The `-O` option saves the file with the same name as in the URL.

	```shell
	curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
	```

4. This command installs `gnupg2` (for package signature verification), `lsb-release` (for distribution information), and the downloaded Percona release package. Together they configure the Percona APT repository on your system.

	```shell
	sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
	```

5. This command refreshes the package lists so the system recognizes the newly enabled Percona repository and the latest package versions.

	```shell
	sudo apt update
	```

6. This command enables the Percona Server for MySQL {{vers}} release repository. It configures `apt` to install packages from the Percona repository.

	```shell
	sudo percona-release enable-only {{pkg}} release
	```

7. You can verify the repository setup by checking the Percona release list in `/etc/apt/sources.list.d/percona-original-release.list`.

8. This command installs the `percona-server-server` package. During installation, the package manager will prompt you to select the default authentication plugin; follow the [Configure authentication](#configure-authentication) section below.

	```shell
	sudo apt install percona-server-server
	```

### Configure authentication

During the installation process, the package manager will prompt you to select the default authentication plugin.

!!! warning "Important Change in MySQL 8.4"

	Percona Server for MySQL 8.4 inherits the upstream change where the `mysql_native_password` plugin is **disabled by default**.

=== "Option 1: Recommended (Strong Password Encryption)"

	**Select this option if you are setting up a new server or using modern application drivers.**

	This uses the `caching_sha2_password` plugin, providing superior security and performance. No further configuration is required.

=== "Option 2: Legacy (Native Password)"

	**Select this option only if you must support legacy applications that cannot be updated.**

	If you choose this option, you **must** manually enable the plugin after installation, or the server will fail to authenticate users using this method.

	1. Open your configuration file (for example, `/etc/mysql/mysql.conf.d/mysqld.cnf`).

	2. Add the following to the `[mysqld]` section:
		```ini
		[mysqld]
		mysql-native-password=ON
		```

	3. Restart the service:
		```bash
		sudo systemctl restart mysql
		```

See [Configuring Percona repositories with `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

--8<--- "storage-engines.md"

## Next Steps

After successful installation:

* [Post-installation](post-installation.md) — Configure and secure your Percona Server for MySQL installation.

* [First five minutes after installation](first-five-minutes.md) — Security and stability steps to take right after install (secure the server, create an admin user, enable logging, verify backup path).

* [Next steps](quickstart-next-steps.md) — Ideas for what to do next (backup, monitoring, data types, and related Percona products).

## Install Percona Toolkit UDFs (Optional)

Percona Server for MySQL includes user-defined functions (UDFs) from [Percona Toolkit :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/). 

These UDFs provide faster checksum calculations. Install the component if you use tools that need the component (for example, `pt-table-checksum`) or need fast fingerprinting to compare tables or distribute rows across servers.

Use these functions for high-speed checksumming and sharding. [Learn more about UDF Use Cases →](udf-percona-toolkit.md)

* `fnv_64`: Fast hash function

* `fnv1a_64`: Alternative fast hash function  

* `murmur_hash`: High-performance hash function

User-Defined Functions (UDFs) are custom functions you can add to MySQL to extend its capabilities.
 These particular UDFs are useful for data integrity checks and performance monitoring. They are delivered as a MySQL component—one command loads all of them.

To load the component after installation:

```{.sql data-prompt="mysql>"}
INSTALL COMPONENT 'file://component_percona_udf';
```


??? example "Expected output"

	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

Once loaded, each function takes a value (a string or number) and returns a numeric fingerprint of that value—the same input always produces the same result, which is useful for checksums and sharding. You can use them in expressions, `WHERE` clauses, or to generate shard keys. For example, pass a string to `fnv_64()` and the function returns a number:

```{.sql data-prompt="mysql>"}
SELECT fnv_64('test_string');
```


??? example "Expected output"

	```{.text .no-copy}
	+----------------------+
	| fnv_64('test_string') |
	+----------------------+
	|   13528473474361592478 |
	+----------------------+
	```

For detailed information about these functions, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

## Install the Percona testing repository using APT

Percona offers pre-release builds from the testing repository. As a superuser, run `percona-release` with the `testing` argument to enable it:

```shell
sudo percona-release enable {{pkg}} testing
```

Do not run testing repository builds in production. The build may not contain all the features available in the final release and may change without notice.

[Telemetry data]: telemetry.md