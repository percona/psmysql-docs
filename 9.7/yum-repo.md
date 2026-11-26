> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install using DNF

Installation method

This guide documents the standard operating system (OS) installation on Red Hat Package Manager (RPM)-based systems. Supported distributions include Red Hat Enterprise Linux (RHEL), CentOS, and Rocky Linux. The procedure uses Dandified YUM (DNF). The Percona Server for MySQL software repositories and the [Percona downloads](https://www.percona.com/downloads) page provide the required packages. DNF replaces YUM on RHEL 8 and later. The `yum` commands continue to work because the system aliases them to `dnf`.

Containerized deployments use separate guides:

- For Docker containers, see [Running Percona Server for MySQL in a Docker Container](https://docs.percona.com/percona-server/9.7/docker.md).
- For Kubernetes deployments, see [Percona Operator for MySQL based on Percona Server for MySQL](https://docs.percona.com/percona-operator-for-mysql/ps/) or [Percona Operator for MySQL based on Percona XtraDB Cluster](https://docs.percona.com/percona-operator-for-mysql/pxc/).

The `percona-release` tool is a command-line utility that simplifies the management and installation of Percona software packages, providing access to the latest versions and ensuring consistency across environments. For more information, refer to the [Percona Software Repositories Documentation](https://docs.percona.com/percona-software-repositories/index.html).

We gather [Telemetry data](https://docs.percona.com/percona-server/9.7/telemetry.md) in the Percona packages and Docker images.

Review [Get help from Percona](https://docs.percona.com/percona-server/9.7/get-help.md) for ways that we can work with you.

## Prerequisites

Review the following requirements before you start the installation.

### Required permissions

Package installation and service configuration require `sudo` access or root access. The commands in this guide use `sudo`. You can run the commands as the root user instead.

### Package verification

Percona signs all packages with GNU Privacy Guard (GPG) keys. The installation process installs the [Percona GPG key](https://repo.percona.com/yum/PERCONA-PACKAGING-KEY) and verifies signatures automatically. You can verify packages manually when required.

Security note

Always download packages from the official Percona repositories to confirm authenticity.

## Limitations

On RHEL 8 and derivatives (Oracle Linux 8, Rocky Linux 8, AlmaLinux 8), the AppStream `mysql` module hides the Percona-provided packages. This happens even when the module stream is only the default stream (`[d]`) and is not explicitly enabled (`[e]`). Disable the module before you install.

Checking the MySQL module

The need to disable the `mysql` module depends on the major version of your operating system:

| Operating system        | `sudo dnf -y module disable mysql`                                                                                         |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| RHEL 8 and derivatives  | Required. Without it, `dnf install percona-server-server` fails with `All matches were filtered out by modular filtering`. |
| RHEL 9 and derivatives  | Not needed. The default `mysql` stream does not hide Percona packages. Running the command is harmless.                    |
| RHEL 10 and derivatives | Skip this step. RHEL 10 has no `mysql` module, and the command fails with `missing groups or modules: mysql`.              |

## Install using DNF (RHEL 8 and later)

Standard OS installation

The following steps install Percona Server for MySQL directly on the host operating system using DNF. The procedure applies to standard OS installations, not to Kubernetes pods or containerized environments.

All commands in this guide use `sudo` for privilege elevation. Follow these steps:

1. On RHEL 8 and RHEL 9 and their derivatives, check the MySQL module on your system. On RHEL 10, skip this step and step 2.

   ```shell
   sudo dnf module list mysql
   ```

   Expected output on Rocky Linux 8

   ```text
   Name  Stream  Profiles           Summary
   mysql 8.0 [d] client, server [d] MySQL Module
   mysql 8.4     client, server [d] MySQL Module

   Hint: [d]efault, [e]nabled, [x]disabled, [i]nstalled
   ```

   Expected output on Rocky Linux 9

   ```text
   Name       Stream      Profiles                            Summary
   mysql      8.4         api, client, filter, server [d]     MySQL Module

   Hint: [d]efault, [e]nabled, [x]disabled, [i]nstalled
   ```

   The `[d]` marker next to the stream indicates the default stream. On RHEL 8, a default stream hides the Percona packages in the same way as an enabled (`[e]`) stream.

1. On RHEL 8 and derivatives, disable the MySQL module. This step is required on RHEL 8 even if step 1 shows only the `[d]` marker. On RHEL 9 the step is not needed. On RHEL 10 skip the step because the command fails.

   ```shell
   sudo dnf -y module disable mysql
   ```

   Expected output on Rocky Linux 8

   ```text
   Dependencies resolved.
   ================================================================================
    Package           Architecture     Version             Repository         Size
   ================================================================================
   Disabling modules:
    mysql

   Transaction Summary
   ================================================================================

   Complete!
   ```

   After the command completes, `sudo dnf module list mysql` shows the `[x]` (disabled) marker for the `mysql` streams.

1. Install the Percona repository package:

   ```shell
   sudo dnf install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   ```

   Expected output

   ```text
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

   - Check your internet connection.
   - Verify that the URL is accessible: `curl -I https://repo.percona.com/yum/percona-release-latest.noarch.rpm`
   - Confirm that the system has sufficient disk space: `df -h`

1. Enable the Percona Server for MySQL repository:

   ```shell
   sudo percona-release enable-only ps-97-lts release
   ```

   Expected output

   ```text
   * Disabling all Percona Repositories
   * Enabling the Percona Server for MySQL - PS 9.7- repository
   <*> All done!
   ```

   If this step fails, take the following actions:

   - Check that `percona-release` is installed: `which percona-release`
   - Verify that the package name is correct for your version.
   - Review the command output for error messages.

1. Install the server package:

   ```shell
   sudo dnf install percona-server-server
   ```

   Expected output

   ```text
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

   - List available packages: `dnf search percona-server`.
   - Verify that the repository configuration is correct.
   - Check for package conflicts with existing MySQL installations.
   - Review error messages for specific issues.

See [Configuring Percona repositories with `percona-release`](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

[Post-installation configuration](https://docs.percona.com/percona-server/9.7/post-installation.md)

Percona Server for MySQL 9.7.x comes with the MyRocks storage engine. This storage engine is installed as a plugin. For information on installing and configuring MyRocks, refer to the [Percona MyRocks Installation Guide](https://docs.percona.com/percona-server/9.7/install-myrocks.md).

## Unattended installations

The `-y` flag automatically confirms all actions without asking for user input. This makes running commands smoother, especially in situations where you can’t or don’t want to interact, like during unattended installations or automated scripts. However, keep in mind that using the `-y` flag skips confirmation prompts, which means you won’t have a chance to review any changes before they’re made. So, it’s best to use this flag only when you’re sure about the command you’re executing.

The `-y` flag applies to `percona-release setup`. With `percona-release` 1.0-34, `percona-release setup ps-97-lts` disables all Percona repositories but does not enable the Percona Server for MySQL 9.7 repository. For unattended installations, enable the repository with `enable-only` instead:

```shell
percona-release enable-only ps-97-lts release
```

## Next steps

After installation completes, see [Post-installation](https://docs.percona.com/percona-server/9.7/post-installation.md) for steps to configure and secure your Percona Server for MySQL installation.

## Additional information

The following sections describe certifications, hardware architecture support, and platform compatibility.

### Red Hat certified

Red Hat certifies Percona Server for MySQL on Red Hat Enterprise Linux 8. The certification confirms operating system interoperability and adherence to common security practices. Percona Server appears in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/112055).

### ARM support

The RPM builds contain Advanced RISC Machine (ARM) packages that use the `aarch64.rpm` extension.

### Supported platforms

The [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) document lists supported platforms, products, and versions.

## Install Percona Toolkit UDFs (optional)

User-defined functions (UDFs) extend MySQL with custom functions. Percona Server for MySQL includes UDFs from [Percona Toolkit](https://docs.percona.com/percona-toolkit/) for data integrity checks and performance monitoring. The following table lists the UDFs that provide faster checksum calculations:

| Function      | Description                                      |
| ------------- | ------------------------------------------------ |
| `fnv_64`      | Fast 64-bit hash function                        |
| `fnv1a_64`    | Variant of `fnv_64` with improved distribution   |
| `murmur_hash` | High-performance non-cryptographic hash function |

To install the functions after the server installation, run the following command:

```sql
INSTALL COMPONENT 'file://component_percona_udf';
```

Expected output

```text
Query OK, 0 rows affected (0.01 sec)
```

### Verify the UDF installation

The functions become available for use in SQL queries. For example: `SELECT fnv_64('test_string');`

For detailed information, see [Percona Toolkit UDF functions](https://docs.percona.com/percona-server/9.7/udf-percona-toolkit.md).

## Install the Percona testing repository (advanced users only)

Do not use testing repositories in production environments. Testing builds are pre-release versions that may contain bugs or incomplete features.

Percona offers pre-release builds from the testing repository for advanced users who want to complete the following actions:

- Evaluate upcoming improvements.
- Provide feedback on development versions.
- Test features before the official release.

To enable the testing repository, run the following command:

```shell
sudo percona-release enable ps-97-lts testing
```

Expected output

```text
* Enabling Percona Server for MySQL 9.7 testing repository
* Running dnf update...
Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
All packages are up to date.
```

The testing repository has the following limitations:

- Features can change without notice.
- Percona does not provide production support for testing builds.
- The repository may contain experimental or incomplete functionality.
- The repository may exclude features from the final release.

To disable the testing repository and return to stable releases, run the following commands:

```shell
sudo percona-release disable testing
sudo dnf update
```

Expected output

```text
* Disabling Percona testing repository
* Running dnf update...
Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
All packages are up to date.
```
