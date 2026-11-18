> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Install Percona Server for MySQL

Before installing, read the [Percona Server for MySQL 8.4 Release notes](https://docs.percona.com/percona-server/8.4/release-notes/release-notes-index.html).

We gather [Telemetry data](https://docs.percona.com/percona-server/8.4/telemetry.html) in the Percona packages and Docker images.

## Install Percona Server for MySQL from repositories

Percona provides repositories for yum (`RPM` packages for Red Hat) and apt (`.deb` packages for Ubuntu and Debian) for software such as Percona Server for MySQL, Percona XtraBackup, and Percona Toolkit. This makes it easy to install and update your software and its dependencies through your operating system’s package manager. This is the recommended way of installing where possible.

The following guides describe the installation process for using the official Percona repositories for the `.deb` and `.rpm` packages.

[Install Percona Server for MySQL on Debian and Ubuntu](https://docs.percona.com/percona-server/8.4/apt-repo.html) [Install Percona Server for MySQL on Red Hat Enterprise Linux](https://docs.percona.com/percona-server/8.4/yum-repo.html)

Starting with [Percona Server for MySQL 8.4.10-10](https://docs.percona.com/percona-server/8.4/release-notes/8.4.10-10.html), packages may be PGO or non-PGO builds depending on your platform. See [Profile-Guided Optimization (PGO) and non-PGO builds](https://docs.percona.com/percona-server/8.4/pgo.html) for benefits, considerations, and which build you receive.

## Other installation methods

[Install Percona Server for MySQL from Binaries](https://docs.percona.com/percona-server/8.4/binary-tarball-install.html)\
[Compile Percona Server for MySQL from Source](https://docs.percona.com/percona-server/8.4/source-tarball.html)\
[Run Percona Server for MySQL in a Docker container](https://docs.percona.com/percona-server/8.4/docker.html)
