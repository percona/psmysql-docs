# Percona Server for MySQL {{vers}} source installation prerequisites

This page is a reference guide for source-build packages and toolchain versions. The list extends the [MySQL 8.4 Source Installation Prerequisites](https://dev.mysql.com/doc/refman/8.4/en/source-installation-prerequisites.html). The extension covers Percona-specific features (for example, XtraDB, MyRocks, and custom components).

Reading this page: Use this document together with [Compile Percona Server for MySQL from source](compile-percona-server.md). Install packages in the following order:
{.power-number}

1. Foundation (toolchain)

2. Baseline (system libraries)

3. Percona layer (optional features you need)

!!! note

    By building from source you become your own release engineer. You must re-pull and re-patch when CVE advisories affect your version. If you skip that work, you run known-vulnerable software. Official packages receive security updates automatically. See [Maintaining a source build](compile-percona-server.md#maintaining-a-source-build). See also [installation from repositories](installation.md) and [Post-installation](post-installation.md).

## Dependency hierarchy

Prerequisites fall into three layers. Install the foundation and baseline first. Add the Percona layer according to the features you enable.

The three layers are:

* Foundation — Toolchain: CMake 3.15 or newer, GCC 11.3 or newer (or a Clang version supported by the source), Bison. Without these minimum versions, the build can fail immediately.

* Baseline — System libraries: OpenSSL, ncurses, libudev, libaio. These are required for a basic build.

* Percona layer — Feature libraries: zstd, lz4, snappy, gflags, and others for MyRocks and XtraDB. Install development packages for each component you enable. CMake may need explicit flags (for example, `-DWITH_ZSTD=system`) to use system libraries.

!!! note

    You must install development packages (`-devel` on RHEL, `-dev` on Debian and Ubuntu). Runtime packages do not include headers or link libraries. The lists in the following sections may not cover every storage engine or CMake option. Run CMake once before a long build. Fix any missing-dependency messages first.


## Hardware requirements

A full source build of Percona Server {{vers}} needs substantial CPU and memory.

Resource guidelines:

* Each parallel compile job can use about 2–4 GB RAM.

* The final link step can use several GB at once.

* If the machine has too little RAM (for example, a 2 GB VPS), the compiler or linker may run out of memory. The build may produce "Internal Compiler Error" or similar failures.

* Use at least 8 GB RAM for a parallel build (for example, `make -j4`).

* If RAM is limited, use a single-threaded build (`make`) and a large swap file.

* The source tree, build directory, and install can use tens of GB of disk space. Ensure you have enough free space before starting.

## Toolchain (foundation)

Percona Server {{vers}} uses modern C++. The build requires minimum toolchain versions. Default packages on older stable distros (for example, RHEL 8, Ubuntu 20.04) can be too old. The build will fail. Verify versions before building.

Verify each component:

* CMake 3.15 or newer. Run `cmake --version`. If the distro package is older, install a newer CMake (for example, from a module, a kit, or the upstream installer).

* GCC 11.3 or newer (or a Clang version documented for {{vers}}). Run `gcc --version` or `g++ --version`. If the distro GCC is too old, install a newer toolchain. Software Collections and newer distros are common sources. Update binutils with the compiler. An old linker with a new GCC causes late link failures.

* A minimum glibc version. Run `ldd --version` and compare to the version required for {{vers}} (see release notes or build documentation). On older LTS distros, glibc can be too old. The build fails in the link phase.

* A modern linker (binutils). Run `ld --version` or `ld.bfd --version`. Ensure the linker meets the requirement for {{vers}}.

Use a distribution and full toolchain that Percona documents as supported for {{vers}}.

### Use a non-default compiler

If the system default compiler is too old, point CMake at a newer GCC or Clang. Set `CC` and `CXX` before running CMake. Example:

```shell
export CC=/opt/rh/gcc-toolset-11/root/usr/bin/gcc
export CXX=/opt/rh/gcc-toolset-11/root/usr/bin/g++
```

CMake uses `CC` and `CXX` for configuration and compilation. If the linker is in a non-default path, set `LDFLAGS` or the matching CMake variable.


## Required packages (baseline)

Install the following development packages before running CMake. You then avoid missing-library errors during configuration. Development packages provide headers and link libraries. Runtime-only packages are not enough for building.

Install on RHEL, Rocky Linux, or AlmaLinux (package manager: `dnf` or `yum`):

```shell
dnf install cmake gcc gcc-c++ ncurses-devel openssl-devel libudev-devel libaio-devel bison wget curl
```

Install on Debian or Ubuntu (package manager: `apt`):

```shell
apt install cmake gcc g++ libncurses-dev libssl-dev libudev-dev libaio-dev bison wget curl
```

Package purposes:

* cmake — Build system generator. Minimum 3.15; verify with `cmake --version`. Default packages on RHEL 8 or Ubuntu 20.04 may be older; upgrade if needed.

* gcc / g++ — C and C++ compiler. Minimum GCC 11.3 for {{vers}}; verify with `gcc --version`. Use a newer toolchain on older distros if the default is too old.

* ncurses — Terminal library (ncurses-devel / libncurses-dev).

* openssl — SSL/TLS (openssl-devel / libssl-dev).

* libudev — Device manager library (libudev-devel / libudev-dev).

* libaio — Asynchronous I/O (libaio-devel / libaio-dev).

* bison — Parser generator.

* wget, curl — Required for Option A in the Boost section. Install at least one. The build machine needs network access during CMake configuration.


### Full feature set (all Percona features)

Install a complete package set to reduce CMake dependency surprises. The set covers baseline plus common Percona features (PAM, zlib, zstd, lz4, gflags, snappy). Run one of the following commands, then run CMake. You can still enable or disable features via CMake options.

Install on RHEL, Rocky Linux, or AlmaLinux:

```shell
dnf install cmake gcc gcc-c++ ncurses-devel openssl-devel libudev-devel libaio-devel bison wget curl pam-devel zlib-devel libzstd-devel lz4-devel gflags-devel snappy-devel
```

Install on Debian or Ubuntu:

```shell
apt install cmake gcc g++ libncurses-dev libssl-dev libudev-dev libaio-dev bison wget curl libpam0g-dev zlib1g-dev libzstd-dev liblz4-dev libgflags-dev libsnappy-dev
```

If CMake still reports a missing dependency, add the corresponding -devel or -dev package for your distribution and re-run CMake.

## Boost

Percona Server {{vers}} requires a specific Boost version (defined in the source tree). Choose one approach only.

!!! note

    Do not pass `-DDOWNLOAD_BOOST=1` and `-DWITH_BOOST=/path/to/boost` in the same CMake command. CMake may download one version while headers come from another path. The build can fail hours later with missing Boost headers.

Choose one of the following options:

* Option A — CMake downloads Boost: add `-DDOWNLOAD_BOOST=1` to the CMake command. CMake downloads the correct Boost during configuration. You need `wget` or `curl` and network access. Use Option A when the build host has internet access.

* Option B — You provide Boost: install the required Boost version and pass `-DWITH_BOOST=/path/to/boost` to CMake. Use Option B on air-gapped hosts or when Boost is already installed. Use either Option A or Option B, not both.


Check the source or CMake output for the exact Boost version required. Do not rely on a single hardcoded version in documentation.

## Optional features and Percona-specific components (Percona layer)

Depending on the CMake options you enable, additional development packages may be required. Install the `-devel` (RHEL) or `-dev` (Debian and Ubuntu) packages so CMake can find headers and libraries.

### System vs bundled libraries

For some components (for example, zstd and lz4), CMake can use a system library or a bundled copy.

!!! note

    Pass flags such as `-DWITH_ZSTD=system` or `-DWITH_LZ4=system` when the distro library is compatible. The OS package manager then owns updates. Use the bundled default when the system library is too old or missing. CMake does not always select system libraries without an explicit flag. The build may skip the feature or bundle a copy instead. See the Percona Server source and CMake options for valid flags.


Optional components and typical packages:

* PAM authentication — Building with the PAM plugin (`-DWITH_PAM=ON`) typically requires the PAM development package (for example, `pam-devel` on RHEL, `libpam0g-dev` on Debian/Ubuntu).

* zlib — Required for compression support. Often already satisfied by the baseline list. If CMake reports a missing zlib, install the development package (for example, `zlib-devel` on RHEL, `zlib1g-dev` on Debian/Ubuntu).

* zstd, lz4 — Compression libraries used by Percona features. Install the development packages (for example, `libzstd-devel`, `lz4-devel` on RHEL; `libzstd-dev`, `liblz4-dev` on Debian/Ubuntu). Use CMake flags such as `-DWITH_ZSTD=system` and `-DWITH_LZ4=system` if the build expects to use system libraries.

* MyRocks (RocksDB) — MyRocks builds may need libgflags and libsnappy. On RHEL, install `gflags-devel` and `snappy-devel`. On Debian and Ubuntu, install `libgflags-dev` and `libsnappy-dev`. The exact set is in the Percona Server source. If CMake reports "library not found", check the source repository or CMake configuration.

The optional-components list may not include every package for every storage engine or option. Run CMake once before a long build. Fix any missing-dependency or configuration messages first. The MySQL 8.4 upstream prerequisites page lists more optional dependencies. The final list for your build is in the Percona Server source tree and the CMake output.


## See also

* [Compile Percona Server for MySQL from source](compile-percona-server.md) — Configure, build, and install steps.

* [Install Percona Server for MySQL from repositories](installation.md) — Package-based installation.

* [Install Percona Server for MySQL from a source tarball](source-tarball.md) — Offline or restricted-network installs.

* [Install with binary tarballs](binary-tarball-install.md) — Alternative to compiling from source.

* [Build APT packages](build-apt-packages.md) — Repeatable packaging workflows.

* [MySQL 8.4 Source Installation Prerequisites](https://dev.mysql.com/doc/refman/8.4/en/source-installation-prerequisites.html) — Upstream baseline reference.
