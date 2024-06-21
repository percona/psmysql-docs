# Install from Percona Software repository

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [download page](https://www.percona.com/downloads). 

The Percona yum repository supports popular RPM-based
operating systems. The easiest way to install the Percona RPM repository is to install an RPM configuring yum and installing the [Percona GPG key](https://repo.percona.com/yum/PERCONA-PACKAGING-KEY).

We gather [Telemetry data] in the Percona packages and Docker images.

## Version changes

Starting with Percona Server 8.0.33-25, the RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the `aarch64.rpm` extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

## Supported platforms

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## Red Hat Certified

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

## Limitations

The RPM packages for Red Hat Enterprise Linux 7 and the compatible derivatives do not support TLSv1.3. This version requires OpenSSL 1.1.1, which is currently unavailable on this platform.

## Install

Install from Percona Software Repository
For more information on the Percona Software repositories and configuring Percona Repositories with `percona-release`, see the [Percona Software Repositories Documentation]. Run the following commands as a `root` user or with sudo.

=== "Install on Red Hat 7"

    The first command uses `yum` to install the Percona repository from the Percona website. The second command enables the `ps-80` release series of the Percona Server. The third command allows the `tools` repository. This repository contains additional Percona software. The fourth command installs Percona Server for MySQL.
    
    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    $ sudo percona-release enable-only ps-80 release
    $ sudo percona-release enable tools release
    $ sudo yum install percona-server-server
    ```
=== "Install on Red Hat 8 or later"

     The first command uses `yum` to install the Percona repository from the Percona website. The second command uses the `percona-release` script to set up the `ps-80` release series of Percona Server. The third command installs Percona Server for MySQL.

    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    $ sudo percona-release setup ps-80
    $ sudo yum install percona-server-server
    ```

## Available storage engines

Percona Server for MySQL 8.0 comes with the TokuDB storage engine and MyRocks storage engine. These storage engines are installed as plugins.

Percona Server for MySQL 8.0.28-19 (2022-05-12)and higher do not support the TokuDB storage engine. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. For more information, see [TokuDB version changes].

For information on how to install and configure TokuDB, refer to the [TokuDB Installation guide].

For information on how to install and configure MyRocks, refer to the [Percona MyRocks Installation guide].

### Percona yum Testing repository

Percona offers pre-release builds from our testing repository.

To subscribe to the testing repository, you enable the testing
repository in `/etc/yum.repos.d/percona-release.repo` by updating the second section, 'testing' and set both `percona-testing-$basearch` and `percona-testing-noarch` to `enabled = 1`. 

There are three sections in this file: 

* release

* testing

* experimental

You must install the Percona repository first if the installation has not been done already.

[Telemetry data]: telemetry.md
[Percona Software Repositories Documentation]: https://docs.percona.com/percona-software-repositories/index.html

[TokuDB version changes]: tokudb-version-changes.md
[TokuDB Installation guide]: tokudb-installation.md
[Percona MyRocks Installation guide]: install-myrocks.md