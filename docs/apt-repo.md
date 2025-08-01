# Install Percona Server for MySQL {{vers}} Using APT on Debian/Ubuntu 

Percona provides ready-to-use packages for Percona Server for MySQL 8.4 through its APT repositories, offering seamless updates and dependency resolution for Debian-based systems.

If you need help with installation or configuration, [Percona Support](https://www.percona.com/services/support) is available to assist you.

Specific information on the supported platforms, products, and versions are available in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

Percona packages and Docker images collect anonymous telemetry data to improve product quality. For details on what is collected and how to opt out, see [Telemetry in Percona Server for MySQL].



## ARM support

Percona Server for MySQL 8.4 includes native support for the ARM64 (aarch64) architecture in its DEB packages. These packages are available for Ubuntu starting with version 20.04 and for Debian starting with version 11.


## Install Percona Server for MySQL using APT

To install Percona Server for MySQL using APT, do the following steps:
{.power-number}

1. Update the package index and install `curl`:

	```{.bash data-prompt="$"}
	$ sudo apt update && sudo apt install curl
	```

2. Download the `percona-release` repository package:

	```{.bash data-prompt="$"}
	$ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
	```

3. Install the package with `apt` as root or with sudo:

	```{.bash data-prompt="$"}
	$ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
	```
    
4. Refresh the package index:

	```{.bash data-prompt="$"}
	$ sudo apt update
	```

5. Enable the Percona Server for MySQL {{vers}} repository:

	```{.bash data-prompt="$"}
	$ sudo percona-release enable-only {{pkg}} release
	$ sudo percona-release enable tools release
	```

6. [Optional] You can check the repository setup for the Percona original release list in ```cat /etc/apt/sources.list.d/percona-original-release.list```. 

8. Install the server:

	```{.bash data-prompt="$"}
	$ sudo apt install percona-server-server
	```

See [Configuring Percona repositories with `percona-release`](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

--8<--- "storage-engines.md"

Percona Server for MySQL includes user-defined functions (UDFs) from [Percona Toolkit](https://docs.percona.com/percona-toolkit/) for faster checksum calculations. Learn more in [Percona Toolkit UDF functions](udf-percona-toolkit.md).

Once the installation completes, execute the following command to install these functions:

```{.bash data-prompt="mysql>"}
mysql> -e "INSTALL COMPONENT 'file://component_percona_udf'"
```

## Install the Percona Testing repository using APT

Percona offers pre-release builds from the testing repository. To enable it, run
percona-release with the `testing` argument. Run the following command as root or use the sudo command:

```{.bash data-prompt="$"}
$ sudo percona-release enable {{pkg}} testing
```

These builds should not be run in production. This build may not contain all of the features available in the final release. The features may change without notice.

[Percona downloads]: https://www.percona.com/downloads/Percona-Server-{{vers}}/

[Telemetry in Percona Server for MySQL]: telemetry.md