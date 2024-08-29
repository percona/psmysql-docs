# Install from Percona Software repository

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [download page](https://www.percona.com/downloads/Percona-Server-{{vers}}/). The
Percona yum repository supports popular RPM-based
operating systems. The easiest way to install the Percona RPM repository is to install an RPM
that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

We gather [Telemetry data] in the Percona packages and Docker images.

## Supported platforms

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## Red Hat Certified

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

## ARM support

The RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the `aarch64.rpm` extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

## Install

To install using the Percona Software repository, run the following commands either as a `root` user or, as in the example, using `sudo`.

    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    $ sudo percona-release enable-only {{pkg}} release
    $ sudo percona-release enable tools release
    $ sudo yum install percona-server-server
    ```

## Available storage engines

Percona Server for MySQL {{vers}} comes with the `MyRocks` storage engine. This storage engine is installed as a plugin. For information on how to install and configure MyRocks, refer to the [Percona MyRocks Installation Guide](install-myrocks.md).

### Percona yum Testing repository

Percona offers pre-release builds from our testing repository. To
subscribe to the testing repository, you enable the testing
repository in `/etc/yum.repos.d/percona-release.repo`. To do so,
set both `percona-testing-$basearch` and `percona-testing-noarch`
to `enabled = 1` (Note that there are three sections in this file:
release, testing, and experimental - in this case, it is the second section that requires updating).


[Telemetry data]: telemetry.md
