> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install Percona Server for MySQL

Before installing, read the [Percona Server for MySQL 9.7 Release notes](https://docs.percona.com/percona-server/9.7/release-notes/release-notes-index.md).

We gather [Telemetry data](https://docs.percona.com/percona-server/9.7/telemetry.md) in the Percona packages and Docker images.

## Install Percona Server for MySQL from repositories

Percona provides repositories for yum (`RPM` packages for Red Hat) and apt (`.deb` packages for Ubuntu and Debian) for software such as Percona Server for MySQL, Percona XtraBackup, and Percona Toolkit. This makes it easy to install and update your software and its dependencies through your operating system’s package manager. This is the recommended way of installing where possible.

The following guides describe the installation process for using the official Percona repositories for the `.deb` and `.rpm` packages.

[Install Percona Server for MySQL on Debian and Ubuntu](https://docs.percona.com/percona-server/9.7/apt-repo.md) [Install Percona Server for MySQL on Red Hat Enterprise Linux](https://docs.percona.com/percona-server/9.7/yum-repo.md)

Starting with [Percona Server for MySQL 9.7.1-1](https://docs.percona.com/percona-server/9.7/release-notes/9.7.1-1.md), packages may be PGO or non-PGO builds depending on your platform. See [Profile-Guided Optimization (PGO) and non-PGO builds](https://docs.percona.com/percona-server/9.7/pgo.md) for benefits, considerations, and which build you receive.

Percona Server for MySQL 9.7 LTS supports installation through APT, DNF, and YUM packages.

See the [MySQL 9.7 technical migration overview](https://docs.percona.com/percona-server/9.7/whats-new-mysql-9.md) for breaking changes, compatibility, removed items, defaults, and tuning.

## Other installation methods

[Install Percona Server for MySQL from Binaries](https://docs.percona.com/percona-server/9.7/binary-tarball-install.md)\
[Compile Percona Server for MySQL from Source](https://docs.percona.com/percona-server/9.7/source-tarball.md)\
[Run Percona Server for MySQL in a Docker container](https://docs.percona.com/percona-server/9.7/docker.md)
