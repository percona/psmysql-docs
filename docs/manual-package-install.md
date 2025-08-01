# Install Percona Server for MySQL from a Local Package File

You can install Percona Server for MySQL without using an online repository. This method uses a package file that you download directly from the Percona website and then install locally with your system’s package manager.

## Why install from a local package file

Installing from a local file provides control over the exact package version. This method works well in environments without internet access or when administrators prefer to manage package distribution internally.

This method is commonly used when you need:

* A specific version that is not available in the standard repositories

* Installation in offline/air-gapped environments

* Direct control over package sources for security or compliance reasons

* Installation before the package is available through normal repository channels

## Steps to install

1. Download the package file

    Go to [Percona Software Downloads](https://www.percona.com/downloads/).  Select the desired version of Percona Server for MySQL. Choose the package format that matches your operating system:

    * `.deb` for Debian-based distributions, such as Ubuntu

    * `.rpm` for Red Hat-based distributions, such as CentOS, AlmaLinux, or Rocky Linux

    Save the file to a directory on your local system.

    An example for a Debian 12 ARM64 system:

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-{{release}}/binary/debian/bookworm/aarch64/percona-server-server_{{release}}-1.bookworm_arm64.deb
    ```

    An example for Red Hat Enterprise Linux (RHEL) ARM64 system:

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-{{release}}/binary/redhat/9/aarch64/percona-server-server-{{release}}.1.el9.aarch64.rpm
    ```

2. Install the package file

    Use your system’s package manager to process the local file.

    For Debian-based systems:

    ```{.bash data-prompt="$"}
    $ sudo apt install ./percona-server-server_{{release}}-1.bookworm_aarch64.deb
    ```

    For Red Hat Enterprise Linux-based systems:

    ```{.bash data-prompt="$"}
    $ sudo dnf install percona-server-server-{{release}}-1.el9.aarch64.rpm
    ```

    The package manager verifies dependencies and installs the software from the local file.

## Troubleshooting missing dependencies

If the package manager reports missing dependencies:

* Review the error message to identify the missing packages.

* Download the missing packages from a trusted source.

* Install the missing packages locally using the same package manager.

An example for Debian 12 system:

```{.bash data-prompt="$"}
$ sudo apt install ./libexample_1.2.3-1_aarch64.deb
```

An example for RHEL 9 system:

```{.bash data-prompt="$"}
$ sudo dnf install libexample-1.2.3-1.el9.aarch64.rpm
```

Repeat the installation of Percona Server for MySQL after resolving all dependencies.

## Verify the installation

After installing, verify that Percona Server for MySQL is installed and running.

Check the installed version:

```{.bash data-prompt="$"}
$ mysql --version
```

Check the service status:

```{.bash data-prompt="$"}
$ sudo systemctl status mysql
```

If the service is running, the output includes ```active (running)```.

### If the service is not running

If systemctl shows that the MySQL service is inactive or failed:

* Review recent log messages for errors

* Check the MySQL error log, usually located in `/var/log/mysql/` or `/var/log/mysqld.log`.

* Start the service manually:

    ```{.bash data-prompt="$"}
    $ sudo systemctl start mysql
    ```

If the service still does not start, investigate configuration issues, missing dependencies, or port conflicts.