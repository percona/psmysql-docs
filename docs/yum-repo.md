# Install using DNF

!!! important "Installation Method"
    This guide describes **standard OS installation** on RPM-based operating systems (RHEL, CentOS, Rocky Linux, etc.) using DNF. Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [Percona downloads] page. On RHEL 8+ systems, DNF has superseded YUM, but `yum` commands continue to work as they are aliased to `dnf`.
    
    **For containerized deployments:**

    * For Docker containers, see [Running Percona Server for MySQL in a Docker Container](docker.md).

    * For Kubernetes deployments, refer to the documentation for [Percona Operator based on Percona Server for MySQL](https://docs.percona.com/percona-operator-for-mysql/ps/) or [Percona Operator based on Percona XtraDB Cluster](https://docs.percona.com/percona-operator-for-mysql/pxc/).


--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<-- "get-help-snip.md"

## Prerequisites

### Required permissions

You need either `sudo` access or root access to install packages and configure system services. The installation commands in this guide use `sudo`, but you can run them as the root user if you prefer.

### Package verification

The packages are signed with GPG keys for security. The installation process automatically installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona) and handles key verification, but you can manually verify packages if needed.

!!! note "Security Note"
    Always download packages from official Percona repositories to ensure authenticity and security.



## Limitations

RHEL 8+ and other EL8+ systems enable the MySQL module by default. This module hides the Percona-provided packages and the module must be disabled to make these packages visible.

!!! important "Checking the MySQL Module"
    RHEL 8+ systems enable the MySQL module by default, which can hide or conflict with Percona's packages. The first installation step below shows you how to check if the module is enabled. If you see an **[e]** marker, you must disable the module before proceeding. If you only see **[d]** (default), you can proceed.

## Install using DNF (RHEL 8+)

!!! note "Standard OS Installation"
    The following steps install Percona Server for MySQL directly on the host operating system using DNF. These instructions are for standard OS installations, not for Kubernetes pods or containerized environments.

All commands in this guide use `sudo` for privilege elevation. Follow these steps:
{.power-number}

1. Verify that the MySQL module is currently enabled on your system:

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

        The [d] next to the server profile indicates that this is the default stream. A module is only considered enabled if an [e] is present. If you see [e], it means the module is active.

2. [Optional] If the module is listed as [e]nabled, it can cause conflicts with Percona's packages. You must disable the module before proceeding.

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

        The `dnf module disable` command disables the MySQL module. If the module was not enabled to begin with (as shown in the dnf module list output without [e]), this command will display "Nothing to do," which is the expected result. You can then proceed with your installation.

2. Install the Percona repository package:

	```shell
	sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
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

	If this step fails:

	* Check your internet connection.

	* Verify the URL is accessible: `curl -I https://repo.percona.com/yum/percona-release-latest.noarch.rpm`

	* Ensure you have sufficient disk space: `df -h`

3. Enable the Percona Server for MySQL repository:

	```shell
	sudo percona-release enable-only {{pkg}} release
	```

	??? example "Expected output"

		```{.text .no-copy}
        * Disabling all Percona Repositories
        * Enabling the Percona Server for MySQL - PS 8.4- repository
        <*> All done!
		```

	If this step fails:

	* Check if percona-release is properly installed: `which percona-release`

	* Verify the package name is correct for your version.

	* Check for any error messages in the output.

4. Install the server package:

	```shell
	sudo yum install percona-server-server
	```

	??? example "Expected output"

		```{.text .no-copy}
		Percona Release release/noarch YUM reposit 6.0 kB/s | 2.5 kB     00:00    
        Percona Server for MySQL - PS 8.4- release 1.5 MB/s | 2.4 MB     00:01    
        Percona Telemetry release/aarch64 YUM repo 6.8 kB/s | 2.7 kB     00:00    
        Dependencies resolved.
        ===========================================================================
        Package                 Arch    Version                  Repository  Size
        ===========================================================================
        Installing:
        percona-server-server   aarch64 8.4.5-5.1.el9            ps-84-lts-release-aarch64
        ...
		systemd-252-51.el9_6.1.aarch64                                           
        systemd-pam-252-51.el9_6.1.aarch64                                       
        systemd-rpm-macros-252-51.el9_6.1.noarch                                 

        Complete!
		```

	If this step fails:

	* Check available packages: `yum search percona-server`.

	* Ensure the repository is properly configured.

	* Check for package conflicts with existing MySQL installations.

	* Review error messages for specific issues.

See [Configuring Percona repositories with `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

[Post-installation configuration](post-installation.md){.md-button}

--8<-- "storage-engines.md"

## Unattended installations

--8<-- "install-flag.md"

## Next steps

After a successful installation, refer to the [Post-installation](post-installation.md) documentation for detailed steps to configure and secure your Percona Server for MySQL installation.

## Additional information

### Red Hat certified

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices, as well as successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

### ARM support

The RPM builds contain ARM packages with the `aarch64.rpm` extension.

### Supported platforms

Specific information on the supported platforms, products, and versions ican be found in the [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) document.

## Install Percona Toolkit UDFs (optional)

Percona Server for MySQL includes user-defined functions (UDFs) from [Percona Toolkit :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/). These UDFs provide faster checksum calculations:

* `fnv_64`: Fast hash function

* `fnv1a_64`: Alternative fast hash function  

* `murmur_hash`: High-performance hash function

User-defined functions (UDFs) are custom functions you can add to MySQL to extend its capabilities. These particular UDFs are useful for data integrity checks and performance monitoring.

To install these functions after installation:

```sql
INSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"

	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

### UDFs installed

You can now use these functions in your SQL queries. For example: `SELECT fnv_64('test_string');`

For detailed information about these functions, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

## Install the Percona testing repository (advanced users only)


Do not use testing repositories in production environments. Testing builds are pre-release versions that may contain bugs or incomplete features.

Percona offers pre-release builds from the testing repository for advanced users who want to:

* Test new features before official release.

* Evaluate upcoming improvements.

* Provide feedback on development versions.

To enable the testing repository:

```shell
sudo percona-release enable {{pkg}} testing
```

??? example "Expected output"

	```{.text .no-copy}
	* Enabling Percona Server for MySQL 8.4 LTS testing repository
	* Running yum update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```

Please be aware of the following limitations when using the testing repository:

* Features may change without notice.

* Not all features from the final release may be included.

* May contain experimental or incomplete functionality

* No production support for testing builds

To disable the testing repository and return to stable releases:

```shell
sudo percona-release disable testing
sudo yum update
```

??? example "Expected output"

	```{.text .no-copy}
	* Disabling Percona testing repository
	* Running yum update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```

[Telemetry data]: telemetry.md
