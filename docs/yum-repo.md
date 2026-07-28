# Install using DNF

!!! important "Installation method"

    This guide documents the standard operating system (OS) installation on Red Hat Package Manager (RPM)-based systems. Supported distributions include Red Hat Enterprise Linux (RHEL), CentOS, and Rocky Linux. The procedure uses Dandified YUM (DNF). The Percona Server for MySQL software repositories and the [Percona downloads] page provide the required packages. DNF replaces YUM on RHEL 8 and later. The `yum` commands continue to work because the system aliases them to `dnf`.

    Containerized deployments use separate guides:

    * For Docker containers, see [Running Percona Server for MySQL in a Docker Container](docker.md).

    * For Kubernetes deployments, see [Percona Operator for MySQL based on Percona Server for MySQL](https://docs.percona.com/percona-operator-for-mysql/ps/) or [Percona Operator for MySQL based on Percona XtraDB Cluster](https://docs.percona.com/percona-operator-for-mysql/pxc/).


--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<-- "get-help-snip.md"

## Prerequisites

Review the following requirements before you start the installation.

### Required permissions

Package installation and service configuration require `sudo` access or root access. The commands in this guide use `sudo`. You can run the commands as the root user instead.

### Package verification

Percona signs all packages with GNU Privacy Guard (GPG) keys. The installation process installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona) and verifies signatures automatically. You can verify packages manually when required.

!!! note "Security note"

    Always download packages from the official Percona repositories to confirm authenticity.

## Limitations

RHEL 8 and later systems enable the MySQL module by default. The module hides the Percona-provided packages. Disable the module to make the Percona packages visible.

!!! important "Checking the MySQL module"

    RHEL 8 and later systems enable the MySQL module by default. The module can hide or conflict with Percona packages. The first installation step in the following section checks whether the module is enabled. An `[e]` marker indicates that you must disable the module before proceeding. A `[d]` marker indicates the default stream and allows you to proceed.

## Install using DNF (RHEL 8 and later)

!!! note "Standard OS installation"

    The following steps install Percona Server for MySQL directly on the host operating system using DNF. The procedure applies to standard OS installations, not to Kubernetes pods or containerized environments.

All commands in this guide use `sudo` for privilege elevation. Follow these steps:
{.power-number}

1. Verify whether the MySQL module is enabled on your system:

	```shell
	sudo dnf module list mysql
	```

	??? example "Expected output"

		```{.text .no-copy}
		Rocky Linux 9 - BaseOS                     2.2 MB/s | 2.6 MB     00:01
		Rocky Linux 9 - AppStream                  3.7 MB/s | 8.2 MB     00:02
		Rocky Linux 9 - Extras                      35 kB/s |  18 kB     00:00
		Rocky Linux 9 - AppStream
		Name       Stream      Profiles                            Summary
		mysql      8.4         api, client, filter, server [d]     MySQL Module

		Hint: [d]efault, [e]nabled, [x]disabled, [i]nstalled
		```

	The `[d]` marker next to the server profile indicates the default stream. A module is enabled only when an `[e]` marker is present. An `[e]` marker indicates that the module is active.

2. Disable the MySQL module if step 1 lists the module as `[e]`-enabled. The MySQL module conflicts with Percona packages. Run the following command:

	```shell
	sudo dnf module disable mysql
	```

	??? example "Expected output"

		```{.text .no-copy}
		Last metadata expiration check: 0:33:11 ago on Fri Aug 29 14:37:35 2025.
		Dependencies resolved.
		Nothing to do.
		Complete!
		```

	The `dnf module disable` command disables the MySQL module. When the module is not enabled, the command returns `Nothing to do`. This output is expected. Proceed with the installation.

3. Install the Percona repository package:

	```shell
	sudo dnf install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	```

	??? example "Expected output"

		```{.text .no-copy}
		Last metadata expiration check: 1:04:21 ago on Fri Aug 29 14:37:35 2025.
        percona-release-latest.noarch.rpm           69 kB/s |  28 kB     00:00    
        Dependencies resolved.
        ===========================================================================
        Package               Architecture Version       Repository          Size
        ===========================================================================
        Installing:
        percona-release       noarch       1.0-32        @commandline        28 k

        Transaction Summary
        ===========================================================================
        Install  1 Package
        ...
		Installed:
        percona-release-1.0-32.noarch                                            

        Complete!
		```

	If this step fails, take the following actions:

	* Check your internet connection.

	* Verify that the URL is accessible: `curl -I https://repo.percona.com/yum/percona-release-latest.noarch.rpm`

	* Confirm that the system has sufficient disk space: `df -h`

4. Enable the Percona Server for MySQL repository:

	```shell
	sudo percona-release enable-only {{pkg}} release
	```

	??? example "Expected output"

		```{.text .no-copy}
		* Disabling all Percona Repositories
		* Enabling the Percona Server for MySQL - PS 9.7- repository
		<*> All done!
		```

	If this step fails, take the following actions:

	* Check that `percona-release` is installed: `which percona-release`

	* Verify that the package name is correct for your version.

	* Review the command output for error messages.

5. Install the server package:

	```shell
	sudo dnf install percona-server-server
	```

	??? example "Expected output"

		```{.text .no-copy}
		Percona Release release/noarch YUM reposit 6.0 kB/s | 2.5 kB     00:00
		Percona Server for MySQL - PS 9.7- release 1.5 MB/s | 2.4 MB     00:01
		Percona Telemetry release/aarch64 YUM repo 6.8 kB/s | 2.7 kB     00:00
		Dependencies resolved.
		===========================================================================
		Package                 Arch    Version                  Repository  Size
		===========================================================================
		Installing:
		percona-server-server   aarch64 9.7.0-0.el9              ps-97-lts-release-aarch64
		...
		systemd-252-51.el9_6.1.aarch64
		systemd-pam-252-51.el9_6.1.aarch64
		systemd-rpm-macros-252-51.el9_6.1.noarch

		Complete!
		```

	If this step fails, take the following actions:

	* List available packages: `dnf search percona-server`.

	* Verify that the repository configuration is correct.

	* Check for package conflicts with existing MySQL installations.

	* Review error messages for specific issues.

See [Configuring Percona repositories with `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

[Post-installation configuration](post-installation.md){.md-button}

--8<-- "storage-engines.md"

## Unattended installations

--8<-- "install-flag.md"

## Next steps

After installation completes, see [Post-installation](post-installation.md) for steps to configure and secure your Percona Server for MySQL installation.

## Additional information

The following sections describe certifications, hardware architecture support, and platform compatibility.

### Red Hat certified

Red Hat certifies Percona Server for MySQL on Red Hat Enterprise Linux 8. The certification confirms operating system interoperability and adherence to common security practices. Percona Server appears in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

### ARM support

The RPM builds contain Advanced RISC Machine (ARM) packages that use the `aarch64.rpm` extension.

### Supported platforms

The [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) document lists supported platforms, products, and versions.

## Install Percona Toolkit UDFs (optional)

User-defined functions (UDFs) extend MySQL with custom functions. Percona Server for MySQL includes UDFs from [Percona Toolkit :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/) for data integrity checks and performance monitoring. The following table lists the UDFs that provide faster checksum calculations:

| Function | Description |
|---|---|
| `fnv_64` | Fast 64-bit hash function |
| `fnv1a_64` | Variant of `fnv_64` with improved distribution |
| `murmur_hash` | High-performance non-cryptographic hash function |

To install the functions after the server installation, run the following command:

```sql
INSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"

	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

### Verify the UDF installation

The functions become available for use in SQL queries. For example: `SELECT fnv_64('test_string');`

For detailed information, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

## Install the Percona testing repository (advanced users only)

Do not use testing repositories in production environments. Testing builds are pre-release versions that may contain bugs or incomplete features.

Percona offers pre-release builds from the testing repository for advanced users who want to complete the following actions:

* Evaluate upcoming improvements.

* Provide feedback on development versions.

* Test features before the official release.

To enable the testing repository, run the following command:

```shell
sudo percona-release enable {{pkg}} testing
```

??? example "Expected output"

	```{.text .no-copy}
	* Enabling Percona Server for MySQL {{vers}} testing repository
	* Running dnf update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```

The testing repository has the following limitations:

* Features can change without notice.

* Percona does not provide production support for testing builds.

* The repository may contain experimental or incomplete functionality.

* The repository may exclude features from the final release.

To disable the testing repository and return to stable releases, run the following commands:

```shell
sudo percona-release disable testing
sudo dnf update
```

??? example "Expected output"

	```{.text .no-copy}
	* Disabling Percona testing repository
	* Running dnf update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```

[Telemetry data]: telemetry.md
