# Install from Percona Software repository

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [download page :octicons-link-external-16:](https://www.percona.com/downloads). 

The Percona yum repository supports popular RPM-based
operating systems. The easiest way to install the Percona RPM repository is to install an RPM configuring yum and installing the [Percona GPG key :octicons-link-external-16:](https://repo.percona.com/yum/PERCONA-PACKAGING-KEY).

We gather [Telemetry data] in the Percona packages and Docker images.

Review [Get more help](get-help.md) for ways that we can work with you.

### Version changes 

Starting with Percona Server 8.0.33-25, the RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the `aarch64.rpm` extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

### Supported platforms

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

### Red Hat Certified

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog :octicons-link-external-16:](https://catalog.redhat.com/software/applications/detail/112055).

<!-- ### Percona Server for MySQL PRO 

--8<--- "pro-build-announcement.md"

[Install Percona Server for MySQL Pro](install-pro.md){.md-button} -->

## Install Percona Server for MySQL from Percona `yum` repository

For more information on the Percona Software repositories and configuring Percona Repositories with `percona-release`, see the [Percona Software Repositories Documentation :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/index.html). Run the following commands as a `root` user or with sudo.

!!! note "RHEL 8 and EL8 systems"
    RHEL 8 and other EL8 systems enable the MySQL module by default. This module hides the Percona-provided packages and the module must be disabled before installing Percona Server for MySQL. The installation instructions for RHEL 8 or later include this step.

<!-- === "Install on Red Hat 7"

    The first command uses `yum` to install the Percona repository from the Percona website. The second enables the `ps-80` release series of Percona Server; the third installs Percona Server for MySQL.
    
    ```{.bash}
    sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    sudo percona-release enable-only ps-80 release
    sudo yum install percona-server-server
    ```

Note: Red Hat Enterprise Linux 7 reached End of Life (EOL) on June 30, 2024. This information has been moved to archive-docs/legacy-platforms.md -->

=== "Install on Red Hat 8 or later"

     RHEL 8 and other EL8 systems enable the MySQL module by default, which hides the Percona-provided packages. The first command disables this module. The second command uses `yum` to install the Percona repository from the Percona website. The third command uses the `percona-release` script to set up the `ps-80` release series of Percona Server. The fourth command installs Percona Server for MySQL.

    ```{.bash}
    sudo yum module disable mysql
    sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    sudo percona-release setup ps-80
    sudo yum install percona-server-server
    ```

## Available storage engines

Percona Server for MySQL 8.0 includes the MyRocks storage engine, which is installed as a plugin. For information on how to install and configure MyRocks, refer to the [Percona MyRocks Installation guide](install-myrocks.md).

!!! note "TokuDB storage engine"
    Starting with Percona Server for MySQL 8.0.28-19 (released 2022-05-12), the TokuDB storage engine has been removed from the installation packages and disabled in binary builds. For earlier versions or if you need TokuDB functionality, see the [TokuDB version changes](tokudb-version-changes.md) and [TokuDB Installation guide](tokudb-installation.md) for more information.

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

[TokuDB version changes]: tokudb-version-changes.md
[TokuDB Installation guide]: tokudb-installation.md
[Percona MyRocks Installation guide]: install-myrocks.md