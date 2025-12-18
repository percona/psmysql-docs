---
title: Use an APT repository to install Percona Server for MySQL {{vers}}
description: Ready-to-use packages are available from the Percona Server for MySQL
  software repositories and the [Percona downloads] page.
slug: apt-repo
category: Install
stability: tech-preview
technical_preview: true
tags:
- apt
- debian
- percona-server
- tech-preview
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Use an APT repository to install Percona Server for MySQL {{vers}}

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [Percona downloads] page.

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<--- "get-help-snip.md"

Before proceeding with the installation, make sure you have one of the following:

* `sudo` access: Administrator privileges are necessary for installing packages and configuring system services.

* Root access: Certain commands will require root privileges or `sudo` access.

## ARM support

Percona supports DEB builds with ARM packages with the `aarch64.rpm` extension.

## Unattended installations

--8<-- "install-flag.md"

## Install Percona Server for MySQL using APT

To install Percona Server for MySQL using APT, follow these steps:
{.power-number}

1. Update the package repositories:

	```{.bash data-prompt="$"}
	$ sudo apt update
	```

	??? example "Expected output"

		```{.text .no-copy}
		Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
		Get:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
		Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
		Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [119 kB]
		Fetched 238 kB in 2s (119 kB/s)
		Reading package lists... Done
		Building dependency tree... Done
		Reading state information... Done
		All packages are up to date.
		```

	If this step fails:

	* Check your internet connection

	* Ensure your system can reach Ubuntu/Debian repositories

	* Try running `sudo apt update --fix-missing`

2. `curl` allows you to download files from the internet using command line. Install the `curl` download utility if needed:

	

	```{.bash data-prompt="$"}
	$ sudo apt install curl
	```

	??? example "Expected output"

		```{.text .no-copy}
		Reading package lists... Done
		Building dependency tree... Done
		Reading state information... Done
		The following NEW packages will be installed:
		  curl
		0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
		Need to get 185 kB of archives.
		After this operation, 504 kB of additional disk space will be used.
		Do you want to continue? [Y/n] y
		Get:1 http://us.archive.ubuntu.com/ubuntu jammy/main amd64 curl amd64 7.81.0-1ubuntu1.15 [185 kB]
		Fetched 185 kB in 1s (185 kB/s)
		Selecting previously unselected package curl.
		(Reading database ... 123456 files and directories currently installed.)
		Preparing to unpack .../curl_7.81.0-1ubuntu1.15_amd64.deb ...
		Unpacking curl (7.81.0-1ubuntu1.15) ...
		Setting up curl (7.81.0-1ubuntu1.15) ...
		Processing triggers for man-db (2.10.2-1) ...
		```

	If this step fails:

	* The `curl` package might already be installed

	* Check if you have internet connectivity

	* Try running `which curl` to see if it's already available

3. Download the `percona-release` repository package:

	```{.bash data-prompt="$"}
	$ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
	```

	??? example "Expected output"

		```{.text .no-copy}
		  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
		                                 Dload  Upload   Total   Spent    Left  Speed
		100 15.2k  100 15.2k    0     0  15.2k      0  0:00:01  0:00:01 --:--:-- 15.2k
		```

	If this step fails:

	* Check your internet connection

	* Verify the URL is accessible: `curl -I https://repo.percona.com/apt/percona-release_latest.generic_all.deb`

	* Try downloading from a different network if possible

4. `gnupg2` provides encryption and digital signature verification for package security. `lsb-release` provides information about your Linux distribution. These packages are required dependencies for the Percona repository setup. Install the downloaded package with `apt` as root or with sudo:

	

	```{.bash data-prompt="$"}
	$ sudo apt install gnupg2 lsb-release ./percona-release_latest.generic_all.deb
	```

	??? example "Expected output"

		```{.text .no-copy}
		Reading package lists... Done
		Building dependency tree... Done
		Reading state information... Done
		The following NEW packages will be installed:
		  gnupg2 lsb-release percona-release
		The following packages will be upgraded:
		  (none)
		0 upgraded, 3 newly installed, 0 to remove and 0 not upgraded.
		Need to get 1,245 kB of archives.
		After this operation, 3,456 kB of additional disk space will be used.
		Do you want to continue? [Y/n] y
		Get:1 http://us.archive.ubuntu.com/ubuntu jammy/main amd64 gnupg2 amd64 2.2.27-3ubuntu2.1 [1,234 kB]
		Get:2 http://us.archive.ubuntu.com/ubuntu jammy/main amd64 lsb-release all 11.1.0ubuntu4 [11.0 kB]
		Get:3 ./percona-release_latest.generic_all.deb percona-release all 1.0-27.generic [15.2 kB]
		Fetched 1,245 kB in 2s (622 kB/s)
		Selecting previously unselected package gnupg2.
		(Reading database ... 123456 files and directories currently installed.)
		Preparing to unpack .../gnupg2_2.2.27-3ubuntu2.1_amd64.deb ...
		Unpacking gnupg2 (2.2.27-3ubuntu2.1) ...
		Selecting previously unselected package lsb-release.
		Preparing to unpack .../lsb-release_11.1.0ubuntu4_all.deb ...
		Unpacking lsb-release (11.1.0ubuntu4) ...
		Selecting previously unselected package percona-release.
		Preparing to unpack .../percona-release_latest.generic_all.deb ...
		Unpacking percona-release (1.0-27.generic) ...
		Setting up gnupg2 (2.2.27-3ubuntu2.1) ...
		Setting up lsb-release (11.1.0ubuntu4) ...
		Setting up percona-release (1.0-27.generic) ...
		Processing triggers for man-db (2.10.2-1) ...
		```

	If this step fails:

	* Ensure the downloaded file exists: `ls -la percona-release_latest.generic_all.deb`

	* Check if the file is corrupted by downloading again

	* Verify you have sufficient disk space: `df -h`

5. Refresh the local cache to update the package information:

	```{.bash data-prompt="$"}
	$ sudo apt update
	```

	??? example "Expected output"

		```{.text .no-copy}
		Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
		Get:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
		Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
		Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [119 kB]
		Get:5 https://repo.percona.com/apt jammy InRelease [15.2 kB]
		Fetched 253 kB in 2s (126 kB/s)
		Reading package lists... Done
		Building dependency tree... Done
		Reading state information... Done
		All packages are up to date.
		```

	If this step fails:

	* The repository might not be properly configured

	* Check repository status: `sudo apt update 2>&1 | grep -i percona`

	* Try running the percona-release setup again

6. Use `percona-release` to set up the repository for the Percona Server for MySQL {{vers}} version:

	```{.bash data-prompt="$"}
	$ sudo percona-release enable-only {{pkg}} release
	$ sudo percona-release enable tools release
	```

	??? example "Expected output"

		```{.text .no-copy}
		* Enabling Percona Server for MySQL 8.4 LTS repository
		* Enabling Percona Tools repository
		* Running apt-get update...
		Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
		Get:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
		Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
		Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [119 kB]
		Get:5 https://repo.percona.com/apt jammy InRelease [15.2 kB]
		Fetched 253 kB in 2s (126 kB/s)
		Reading package lists... Done
		Building dependency tree... Done
		Reading state information... Done
		All packages are up to date.
		```

	If this step fails:

	* Check if percona-release is properly installed: `which percona-release`

	* Verify the package name is correct for your version

	* Check for any error messages in the output

7. You can check the repository setup for the Percona original release list in `/etc/apt/sources.list.d/percona-original-release.list`. 

8. Install the server package with the `percona-release` command:

	```{.bash data-prompt="$"}
	$ sudo apt install percona-server-server
	```

	??? example "Expected output"

		```{.text .no-copy}
		Reading package lists... Done
		Building dependency tree... Done
		Reading state information... Done
		The following NEW packages will be installed:
		  percona-server-server
		The following packages will be upgraded:
		  (none)
		0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
		Need to get 45.2 MB of archives.
		After this operation, 234 MB of additional disk space will be used.
		Do you want to continue? [Y/n] y
		Get:1 https://repo.percona.com/apt jammy/main amd64 percona-server-server amd64 8.4.5-5.jammy [45.2 MB]
		Fetched 45.2 MB in 15s (3.01 MB/s)
		Selecting previously unselected package percona-server-server.
		(Reading database ... 123456 files and directories currently installed.)
		Preparing to unpack .../percona-server-server_8.4.5-5.jammy_amd64.deb ...
		Unpacking percona-server-server (8.4.5-5.jammy) ...
		Setting up percona-server-server (8.4.5-5.jammy) ...
		Processing triggers for man-db (2.10.2-1) ...
		Processing triggers for systemd (249.11-0ubuntu3.12) ...
		```

	If this step fails:

	* Check available packages: `apt search percona-server`

	* Ensure the repository is properly configured

	* Check for package conflicts with existing MySQL installations

	* Review error messages for specific issues

See [Configuring Percona repositories with `percona-release`](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

--8<--- "storage-engines.md"

## Next Steps

After successful installation, see [Post-installation](post-installation.md) for detailed steps to configure and secure your Percona Server for MySQL installation.

## Install Percona Toolkit UDFs (Optional)

Percona Server for MySQL includes user-defined functions (UDFs) from [Percona Toolkit](https://docs.percona.com/percona-toolkit/). These UDFs provide faster checksum calculations:

* `fnv_64`: Fast hash function

* `fnv1a_64`: Alternative fast hash function  

* `murmur_hash`: High-performance hash function

User-Defined Functions (UDFs) are custom functions you can add to MySQL to extend its capabilities. These particular UDFs are useful for data integrity checks and performance monitoring.

To install these functions after installation:

```{.sql data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"

	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

You can now use these functions in your SQL queries. For example: `SELECT fnv_64('test_string');`

For detailed information about these functions, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

## Install the Percona testing repository (advanced users only)

Do not use testing repositories in production environments. Testing builds are pre-release versions that may contain bugs or incomplete features.

Percona offers pre-release builds from the testing repository for advanced users who want to:

* Test new features before official release

* Evaluate upcoming improvements

* Provide feedback on development versions

To enable the testing repository:

```{.bash data-prompt="$"}
$ sudo percona-release enable {{pkg}} testing
```

??? example "Expected output"

	```{.text .no-copy}
	* Enabling Percona Server for MySQL 8.4 LTS testing repository
	* Running apt-get update...
	Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
	Get:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
	Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
	Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [119 kB]
	Get:5 https://repo.percona.com/apt jammy InRelease [15.2 kB]
	Fetched 253 kB in 2s (126 kB/s)
	Reading package lists... Done
	Building dependency tree... Done
	Reading state information... Done
	All packages are up to date.
	```

Please be aware of the following limitations when using the testing repository:

* Features may change without notice

* Not all features from the final release may be included

* May contain experimental or incomplete functionality

* No production support for testing builds

To disable the testing repository and return to stable releases:

```{.bash data-prompt="$"}
$ sudo percona-release disable testing
$ sudo apt update
```

??? example "Expected output"

	```{.text .no-copy}
	* Disabling Percona testing repository
	* Running apt-get update...
	Hit:1 http://us.archive.ubuntu.com/ubuntu jammy InRelease
	Get:2 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
	Hit:3 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease
	Get:4 http://security.ubuntu.com/ubuntu jammy-security InRelease [119 kB]
	Get:5 https://repo.percona.com/apt jammy InRelease [15.2 kB]
	Fetched 253 kB in 2s (126 kB/s)
	Reading package lists... Done
	Building dependency tree... Done
	Reading state information... Done
	All packages are up to date.
	```

[Percona downloads]: https://www.percona.com/downloads/Percona-Server-{{vers}}/

[Telemetry data]: telemetry.md