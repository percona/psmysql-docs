# Use an RPM repository to install Percona Server for MySQL {{vers}}

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [Percona downloads] page. 

The Percona yum repository supports popular RPM-based operating systems. The easiest way to install the Percona RPM repository is to install an RPM that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

Specific information on the supported platforms, products, and versions is described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<--- "get-help-snip.md"

## Prerequisites

Before installing Percona Server for MySQL, ensure you have the following:

### Required permissions

* `sudo` access: You need administrator privileges to install packages and configure system services

* Root access: Some commands require root privileges or sudo access

### Package verification

The packages are signed with GPG keys for security. The installation process automatically handles key verification, but you can manually verify packages if needed.

!!! note "Security Note"
    Always download packages from official Percona repositories to ensure authenticity and security.

## Red Hat certified

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

## ARM support

The RPM builds contain ARM packages with the `aarch64.rpm` extension.

## Limitations

RHEL 8+ and other EL8+ systems enable the MySQL module by default. This module hides the Percona-provided packages and the module must be disabled to make these packages visible.


## Percona Server for MySQL PRO

--8<--- "pro-build-announcement.md"

[Install Percona Server for MySQL Pro](install-pro.md){.md-button}

## Unattended installations

--8<-- "install-flag.md"

## Install using DNF (RHEL 8+)

DNF is the default package manager for RHEL 8 and newer systems. To install Percona Server for MySQL using DNF, follow these steps:
{.power-number}

1. Verify that the MySQL module is currently enabled on your system:

	```{.bash data-prompt="$"}
	$ sudo dnf module list mysql
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

1. If needed, If the module is listed as [e]nabled, it can cause conflicts with Percona's packages. You must reset the module to its default state before proceeding.

	```{.bash data-prompt="$"}
	$ sudo dnf module disable mysql
	```

	??? example "Expected output"

		```{.text .no-copy}
        Last metadata expiration check: 0:33:11 ago on Fri Aug 29 14:37:35 2025.
        Dependencies resolved.
        Nothing to do.
        Complete!
		```

        The dnf module `reset` command is used to return a module to its initial state, effectively disabling it. If the module was not enabled to begin with (as shown in the dnf module list output without [e]), this command will have "Nothing to do," which is the expected and desired result. You can then proceed with your installation.

2. Install the Percona repository package:

	```{.bash data-prompt="$"}
	$ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
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

	* Check your internet connection

	* Verify the URL is accessible: `curl -I https://repo.percona.com/yum/percona-release-latest.noarch.rpm`

	* Ensure you have sufficient disk space: `df -h`

3. Enable the Percona Server for MySQL repository:

	```{.bash data-prompt="$"}
	$ sudo percona-release enable-only {{pkg}} release
	```

	??? example "Expected output"

		```{.text .no-copy}
        * Disabling all Percona Repositories
        * Enabling the Percona Server for MySQL - PS 8.4- repository
        <*> All done!
		```

	If this step fails:

	* Check if percona-release is properly installed: `which percona-release`

	* Verify the package name is correct for your version

	* Check for any error messages in the output

4. Install the server package:

	```{.bash data-prompt="$"}
	$ sudo yum install percona-server-server
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

	* Check available packages: `yum search percona-server`

	* Ensure the repository is properly configured

	* Check for package conflicts with existing MySQL installations

	* Review error messages for specific issues

See [Configuring Percona repositories with `percona-release`](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

## Install using YUM (RHEL 7 and older)

YUM is the package manager for RHEL 7 and older systems. To install Percona Server for MySQL using YUM, follow these steps:
{.power-number}

1. Install the Percona repository package:

	```{.bash data-prompt="$"}
	$ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	```

	??? example "Expected output"

		```{.text .no-copy}
		Loaded plugins: fastestmirror, langpacks
		Loading mirror speeds from cached hostfile
		percona-release-latest.noarch.rpm                                                                  | 15 kB  00:00:00
		Examining /var/tmp/yum-root-12345/percona-release-latest.noarch.rpm: percona-release-1.0-27.noarch
		Marking /var/tmp/yum-root-12345/percona-release-latest.noarch.rpm to be installed
		Resolving Dependencies
		--> Running transaction check
		---> Package percona-release.noarch 0:1.0-27 will be installed
		--> Finished Dependency Resolution
		Dependencies Resolved
		================================================================================
		Package                    Architecture  Version        Repository        Size
		================================================================================
		Installing:
		 percona-release           noarch        1.0-27         @commandline      15 k
		================================================================================
		Total download size: 15 k
		Installed size: 15 k
		Is this ok [y/N]: y
		Downloading packages:
		Running transaction check
		Running transaction test
		Transaction test succeeded.
		Running transaction
		  Installing : percona-release-1.0-27.noarch                                              1/1
		  Verifying  : percona-release-1.0-27.noarch                                              1/1
		Installed:
		  percona-release.noarch 0:1.0-27
		Complete!
		```

	If this step fails:

	* Check your internet connection

	* Verify the URL is accessible: `curl -I https://repo.percona.com/yum/percona-release-latest.noarch.rpm`

	* Ensure you have sufficient disk space: `df -h`

2. Enable the Percona Server for MySQL repository:

	```{.bash data-prompt="$"}
	$ sudo percona-release enable-only {{pkg}} release
	$ sudo percona-release enable tools release
	```

	??? example "Expected output"

		```{.text .no-copy}
		* Enabling Percona Server for MySQL 8.4 LTS repository
		* Enabling Percona Tools repository
		* Running yum update...
		Loaded plugins: fastestmirror, langpacks
		Loading mirror speeds from cached hostfile
		All packages are up to date.
		```

	If this step fails:

	* Check if percona-release is properly installed: `which percona-release`

	* Verify the package name is correct for your version

	* Check for any error messages in the output

3. Install the server package:

	```{.bash data-prompt="$"}
	$ sudo yum install percona-server-server
	```

	??? example "Expected output"

		```{.text .no-copy}
		Loaded plugins: fastestmirror, langpacks
		Loading mirror speeds from cached hostfile
		Resolving Dependencies
		--> Running transaction check
		---> Package percona-server-server.x86_64 0:8.4.5-5.el7 will be installed
		--> Finished Dependency Resolution
		Dependencies Resolved
		================================================================================
		Package                    Architecture  Version        Repository        Size
		================================================================================
		Installing:
		 percona-server-server     x86_64        8.4.5-5.el7    percona-release   45 M
		================================================================================
		Total download size: 45 M
		Installed size: 234 M
		Is this ok [y/N]: y
		Downloading packages:
		Running transaction check
		Running transaction test
		Transaction test succeeded.
		Running transaction
		  Installing : percona-server-server-8.4.5-5.el7.x86_64                              1/1
		  Verifying  : percona-server-server-8.4.5-5.el7.x86_64                              1/1
		Installed:
		  percona-server-server.x86_64 0:8.4.5-5.el7
		Complete!
		```

	If this step fails:

	* Check available packages: `yum search percona-server`

	* Ensure the repository is properly configured

	* Check for package conflicts with existing MySQL installations

	* Review error messages for specific issues

--8<--- "storage-engines.md"

## Next steps

After successful installation, see [Post-installation](post-installation.md) for detailed steps to configure and secure your Percona Server for MySQL installation.

## Install Percona Toolkit UDFs (optional)

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

### UDFs installed

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
	* Running yum update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
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
$ sudo yum update
```

??? example "Expected output"

	```{.text .no-copy}
	* Disabling Percona testing repository
	* Running yum update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```

[Percona downloads]: https://www.percona.com/downloads/Percona-Server-{{vers}}/

[Telemetry data]: telemetry.md
