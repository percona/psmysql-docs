# Build from RPM packages

This guide provides step-by-step instructions for building Percona Server for MySQL from source and packaging it as an RPM package. The guide covers setting up the build environment, downloading the source code, creating a SPEC file, building the RPM package, and verifying the installation.

## Prerequisites

Install the required build dependencies:

```{.bash data-prompt="$"}
# Install build dependencies
$ sudo yum groupinstall "Development Tools"
$ sudo yum install \
    cmake \
    openssl-devel \
    libaio-devel \
    ncurses-devel \
    boost-devel \
    rpmdevtools \
    rpmlint \
    systemd-devel \
    vim-common
```

On newer RHEL-based distributions, use the `dnf` package manager:

```{.bash data-prompt="$"}
# Install build dependencies
$ sudo dnf groupinstall "Development Tools"
$ sudo dnf install \
    cmake \
    openssl-devel \
    libaio-devel \
    ncurses-devel \
    boost-devel \
    rpmdevtools \
    rpmlint \
    systemd-devel \
    vim-common
``` 

The `yum groupinstall` command installs a group of development tools using the yum package manager. The "Development Tools" group includes essential compilers, debuggers, and other tools required for building software.

The `yum install` command installs additional packages required for building Percona Server for MySQL. These packages include CMake, OpenSSL development libraries, libaio development libraries, ncurses development libraries, Boost development libraries, rpmdevtools, rpmlint, systemd development libraries, and vim-common.

## Setup RPM build environment

These commands set up the necessary directory structure for building RPM packages.

```{.bash data-prompt="$"}
# Create RPM build directory structure
$ rpmdev-setuptree
```

```text
# Directory structure created:
# ~/rpmbuild/
# ├── BUILD
# ├── RPMS
# ├── SOURCES
# ├── SPECS
# └── SRPMS
```

The `rpmdev-setuptree` command creates the necessary directory structure for building RPM packages. The structure includes the following directories:

* `BUILD`: Where the build process takes place.

* `RPMS`: Where the finished RPM packages are stored.

* `SOURCES`: Where the source tarballs and other sources are stored.

* `SPECS`: Where the SPEC files are stored.

* `SRPMS`: Where the source RPM packages are stored.

## Download and prepare source

These commands help you download the necessary source files and libraries required to build Percona Server for MySQL.

```{.bash data-prompt="$"}
# Download Percona Server source
$ cd ~/rpmbuild/SOURCES
$ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-{{release}}/source/tarball/percona-server-{{tag}}.tar.gz
```

Change to the `SOURCES` directory within your rpmbuild environment using the cd command. Then, use the `wget` command to download the Percona Server source tarball from the specified URL. This tarball contains the source code needed to build Percona Server.

```{.bash data-prompt="$"}
# Download boost if not included
$ wget https://boostorg.jfrog.io/artifactory/main/release/1.77.0/source/boost_1_77_0.tar.gz
```

Use the `wget` command to download the Boost library tarball from the specified URL. Boost provides a set of libraries that help with various programming tasks, and you need it for building Percona Server if it's not already included in the source.

## Create SPEC file

This SPEC file automates the process of building, installing, and packaging Percona Server for MySQL into an RPM package, ensuring that all necessary steps and dependencies are properly managed.

Create `~/rpmbuild/SPECS/percona-server-8.0.spec`:

```text
%define mysql_version {{tag}}
%define rpm_version {{tag}}

Name:           percona-server
Version:        %{mysql_version}
Release:        1%{?dist}
Summary:        Percona Server for MySQL
License:        GPL-2.0

Source0:        percona-server-%{mysql_version}.tar.gz
Source1:        boost_1_77_0.tar.gz

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  libaio-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  boost-devel

%description
Percona Server for MySQL is a free, fully compatible, enhanced, and open source drop-in replacement for MySQL.

%prep
%setup -q -n percona-server-%{mysql_version}

%build
mkdir build
cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DINSTALL_LAYOUT=RPM \
    -DWITH_SSL=system \
    -DWITH_BOOST=../../boost_1_77_0 \
    -DWITH_SYSTEMD=1

make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%files
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*
%{_datadir}/*
%{_sysconfdir}/*
%{_unitdir}/*

%post
/sbin/ldconfig
%systemd_post mysqld.service

%preun
%systemd_preun mysqld.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart mysqld.service
```

The provided SPEC file outlines the instructions to build and package Percona Server for MySQL as an RPM package. Here's a breakdown of what each section does:

1. **Definitions**:
    ```plaintext
    %define mysql_version 8.0.40
    %define rpm_version 8.0.40
    ```
    These lines define variables for the MySQL and RPM version numbers.

2. **Package Information**:
    ```plaintext
    Name:           percona-server
    Version:        %{mysql_version}
    Release:        1%{?dist}
    Summary:        Percona Server for MySQL
    License:        GPL-2.0
    ```
    This section provides metadata about the package, including its name, version, release number, summary, and license.

3. **Sources**:
    ```plaintext
    Source0:        percona-server-%{mysql_version}.tar.gz
    Source1:        boost_1_77_0.tar.gz
    ```
    These lines specify the source tarballs needed to build the package.

4. **Build Requirements**:
    ```plaintext
    BuildRequires:  cmake
    BuildRequires:  openssl-devel
    BuildRequires:  libaio-devel
    BuildRequires:  ncurses-devel
    BuildRequires:  systemd-devel
    BuildRequires:  boost-devel
    ```
    This section lists the packages required to build the software.

5. **Description**:
    ```plaintext
    %description
    Percona Server for MySQL is a free, fully compatible, enhanced, and open source drop-in replacement for MySQL.
    ```
    A brief description of the package.

6. **Preparation**:
    ```plaintext
    %prep
    %setup -q -n percona-server-%{mysql_version}
    ```
    This section sets up the build environment by extracting the source tarball.

7. **Build**:
    ```plaintext
    %build
    mkdir build
    cd build
    cmake .. \
        -DCMAKE_INSTALL_PREFIX=/usr \
        -DINSTALL_LAYOUT=RPM \
        -DWITH_SSL=system \
        -DWITH_BOOST=../../boost_1_77_0 \
        -DWITH_SYSTEMD=1
    make %{?_smp_mflags}
    ```
    This section compiles the software using CMake and Make, with specific build options.

8. **Installation**:
    ```plaintext
    %install
    cd build
    make DESTDIR=%{buildroot} install
    ```
    This section installs the compiled software into a build root directory.

9. **Files**:
    ```plaintext
    %files
    %{_bindir}/*
    %{_sbindir}/*
    %{_libdir}/*
    %{_datadir}/*
    %{_sysconfdir}/*
    %{_unitdir}/*
    ```
    This section lists the files and directories included in the package.

10. **Post-Installation and Pre-Uninstallation Scripts**:
    ```plaintext
    %post
    /sbin/ldconfig
    %systemd_post mysqld.service

    %preun
    %systemd_preun mysqld.service

    %postun
    /sbin/ldconfig
    %systemd_postun_with_restart mysqld.service
    ```
    These scripts handle tasks to be performed after installation and before and after uninstallation, such as updating the shared library cache and managing the `mysqld` service with systemd.


## Build RPM package

These commands help you build and verify RPM packages from a downloaded Percona Server for MySQL tar file. The first command builds the package, while the second command checks the directory to confirm that the packages are created successfully.

```{.bash data-prompt="$"}
# Build the RPM package
$ cd ~/rpmbuild
rpmbuild -ba SPECS/percona-server-8.0.spec
```

First, change to the rpmbuild directory with the `cd` command. Then, use the `rpmbuild -ba` command to build the RPM package based on the percona-server-8.0.spec file located in the SPECS directory. The `-ba` option tells rpmbuild to build both the binary and source RPM packages.

```{.bash data-prompt="$"}
# Check for built packages
$ ls -l RPMS/x86_64/
```

This command lists the contents of the RPMS/x86_64 directory to verify that the built RPM packages are present. The `ls -l` command lists the files in the directory, and the `RPMS/x86_64/` argument specifies the directory to list.

## Important build configuration options

These CMAKE options help configure the build process according to your specific requirements, ensuring that the software is installed and functions correctly on your system.

- `-DCMAKE_INSTALL_PREFIX=/usr`: Installation directory
- `-DINSTALL_LAYOUT=RPM`: RPM-specific installation layout
- `-DWITH_SSL=system`: Use system OpenSSL
- `-DWITH_BOOST`: Path to Boost library
- `-DWITH_SYSTEMD=1`: Enable systemd support

These commands are CMake options used to customize the build process for your project. Here is what each one does:

| Option                        | Description                                                                                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| **`-DCMAKE_INSTALL_PREFIX=/usr`**  | This option sets the installation directory to `/usr`. When you install the software, the files will be placed in the `/usr` directory.                    |
| **`-DINSTALL_LAYOUT=RPM`**         | This option specifies the installation layout for RPM packages. It ensures that the files are organized in a way that is compatible with RPM packaging standards. |
| **`-DWITH_SSL=system`**            | This option tells CMake to use the system's OpenSSL library. Instead of compiling and using a separate OpenSSL library, it will use the one already installed on your system. |
| **`-DWITH_BOOST`**                 | This option sets the path to the Boost library. It ensures that CMake can find and use the Boost libraries during the build process.                      |
| **`-DWITH_SYSTEMD=1`**             | This option enables support for systemd, the system and service manager for Linux operating systems. It allows the software to integrate with systemd for service management. |


## Verify

These commands help you verify the integrity of the RPM package and check for any dependencies, and ensures a smooth installation process.

```{.bash data-prompt="$"}
# Check RPM package integrity
$ rpm -Kv RPMS/x86_64/percona-server-*.rpm
```

This command verifies the integrity of the built RPM package. The `-K` option stands for check, and `-v` is for verbose output.

```{.bash data-prompt="$"}
# Check package dependencies
$ rpm -qpR RPMS/x86_64/percona-server-*.rpm
```

This command lists the dependencies required by the built RPM package. The `-qpR` option queries the package for its dependencies.

## Install

These steps help you install and verify the Percona Server package on your system, and ensures everything is set up correctly.

```{.bash data-prompt="$"}
# Install built package
$ sudo rpm -ivh RPMS/x86_64/percona-server-*.rpm
```

This command installs the built Percona Server package. The `-i` option stands for install, `-v` for verbose, and -h shows hash marks as the package installs. Using `sudo` ensures you have the necessary administrative privileges.

# Check the installation

```{.bash data-prompt="$"}
$ rpm -qa | grep percona-server
$ mysqld --version
```

This command has the following options:

`rpm -qa | grep percona-server`: This command lists all installed packages and filters the list to show only those related to Percona Server. The `rpm -qa` command queries all installed RPM packages, and `grep percona-server` searches for Percona Server entries.

`mysqld --version`: This command displays the installed version of the MySQL server, confirming the successful installation of Percona Server.

## Troubleshoot

The following are common issues encountered during the RPM build process:


| Issue               | Troubleshooting Steps                                                                                                                                   |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Missing dependencies** | ```bash $ # Install additional dependencies if needed sudo yum-builddep SPECS/percona-server-8.0.spec ```                                                |
| **Build failures**        | - Check build logs in `~/rpmbuild/BUILD/` <br> - Verify all build dependencies are installed <br> - Ensure enough disk space is available |
| **Version mismatches**    | - Double-check version numbers in SPEC file <br> - Verify source tarball version matches SPEC file                                                  |

