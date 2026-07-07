# Install Percona Server for MySQL

Before installing, read the [Percona Server for MySQL {{vers}} Release notes](release-notes/release-notes-index.md).

We gather [Telemetry data] in the Percona packages and Docker images.

## Install Percona Server for MySQL from repositories

Percona provides repositories for yum (`RPM` packages for Red Hat) and apt (`.deb` packages for Ubuntu and Debian) for software such as Percona Server for MySQL, Percona XtraBackup, and Percona Toolkit. This makes it easy to install and update your software and its dependencies through your operating system’s package manager. This is the recommended way of installing where possible.

The following guides describe the installation process for using the official Percona repositories for the `.deb` and `.rpm` packages.

[Install Percona Server for MySQL on Debian and Ubuntu](apt-repo.md){.md-button}        [Install Percona Server for MySQL on Red Hat Enterprise Linux](yum-repo.md){.md-button}

Starting with [Percona Server for MySQL 8.4.10-10](release-notes/8.4.10-10.md), packages may be PGO or non-PGO builds depending on your platform. See [Profile-Guided Optimization (PGO) and non-PGO builds](pgo.md) for benefits, considerations, and which build you receive.

## Other installation methods

[Install Percona Server for MySQL from Binaries](binary-tarball-install.md){.md-button} <br>       [Compile Percona Server for MySQL from Source](source-tarball.md){.md-button} <br>       [Run Percona Server for MySQL in a Docker container](docker.md){.md-button} 

[Telemetry data]: telemetry.md
