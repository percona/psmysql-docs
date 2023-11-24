# Install from Percona Software repository

Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [download page](https://www.percona.com/downloads/Percona-Server-{{vers}}/). The
Percona yum repository supports popular RPM-based
operating systems. The easiest way to install the Percona RPM repository is to install an RPM
that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

## Supported platforms

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

## Red Hat Certified

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

## Limitations

The RPM packages for Red Hat Enterprise Linux 7 and the compatible derivatives do not support TLSv1.3, as it requires OpenSSL 1.1.1, which is currently not available on this platform.

## Install

Install from Percona Software Repository
For more information on the Percona Software repositories and configuring Percona Repositories with percona-release, see the Percona Software Repositories Documentation. Run the following commands as a `root` user or with sudo.

=== "Install on Red Hat 7"

    ```{.bash data-prompt="$"}
    $ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    $ sudo percona-release enable-only {{pkg}} release
    $ sudo percona-release enable tools release
    $ sudo yum install percona-server-server
    ```
=== "Install on Red Hat 8 or later"

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

You must install the Percona repository first if the installation has not been done already.
