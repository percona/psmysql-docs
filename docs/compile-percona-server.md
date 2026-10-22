# Compile Percona Server for MySQL from source

The following instructions install Percona Server for MySQL {{vers}} on your system.

## When to use this guide

Compiling from source is an advanced installation method. Prefer repository packages (APT or DNF) or binary tarballs unless you need a custom or debug build.

Use the compile guide when you need a custom or debug build from source (for example, to test patches or build with non-default options).

For RPM, DEB, or repeatable production builds, use Percona automated packaging tooling. The tooling installs dependencies and produces installable packages. See [Build APT packages](build-apt-packages.md), [Install Percona Server for MySQL from repositories](installation.md), and the Percona Server source repository.


!!! warning

    A manual source build does not match the performance or security profile of official Percona binaries. Release builds use Profile-Guided Optimization (PGO), Link-Time Optimization (LTO), and hardened compiler flags.

Treat a custom-compiled binary as suitable for development or testing, not as a drop-in production replacement for official packages.

## Installation prerequisites

This section lists packages and toolchain versions for a source build. The list extends the [MySQL 8.4 Source Installation Prerequisites](https://dev.mysql.com/doc/refman/8.4/en/source-installation-prerequisites.html). The extension covers Percona-specific features (for example, XtraDB, MyRocks, and custom components).

Install packages in the following order:
{.power-number}

1. Foundation (toolchain)

2. Baseline (system libraries)

3. Percona layer (optional features you need)

### Dependency hierarchy

Prerequisites fall into three layers. Install the foundation and baseline first. Add the Percona layer according to the features you enable.

The three layers are:

* Foundation — Toolchain: CMake 3.15 or newer, GCC 11.3 or newer (or a Clang version supported by the source), Bison. Without these minimum versions, the build can fail immediately.

* Baseline — System libraries: OpenSSL, ncurses, libudev, libaio. These are required for a basic build.

* Percona layer — Feature libraries: zstd, lz4, snappy, gflags, and others for MyRocks and XtraDB. Install development packages for each component you enable. CMake may need explicit flags (for example, `-DWITH_ZSTD=system`) to use system libraries.

!!! note

    You must install development packages (`-devel` on RHEL, `-dev` on Debian and Ubuntu). Runtime packages do not include headers or link libraries. The lists in the following sections may not cover every storage engine or CMake option. Run CMake once before a long build. Fix any missing-dependency messages first.

### Hardware requirements

A full source build of Percona Server {{vers}} needs substantial CPU and memory.

Resource guidelines:

* Each parallel compile job can use about 2–4 GB RAM.

* The final link step can use several GB at once.

* If the machine has too little RAM (for example, a 2 GB VPS), the compiler or linker may run out of memory. The build may produce "Internal Compiler Error" or similar failures.

* Use at least 8 GB RAM for a parallel build (for example, `make -j4`).

* If RAM is limited, use a single-threaded build (`make`) and a large swap file.

* The source tree, build directory, and install can use tens of GB of disk space. Ensure you have enough free space before starting.

### Toolchain (foundation)

Percona Server {{vers}} requires C++20. The CMake build sets `-std=c++20` and `cxx_std_20`. You need CMake 3.15 or newer and GCC 11.3 or newer (or a Clang version that implements C++20 as documented for {{vers}}). Default packages on older stable distros (for example, RHEL 8, Ubuntu 20.04) can be too old. Verify compiler and CMake versions before building.

Verify each component:

* CMake 3.15 or newer. Run `cmake --version`. If the distro package is older, install a newer CMake (for example, from a module, a kit, or the upstream installer).

* GCC 11.3 or newer (or a Clang version documented for {{vers}}). Run `gcc --version` or `g++ --version`. If the distro GCC is too old, install a newer toolchain. Software Collections and newer distros are common sources.

On older LTS distros (for example, RHEL 7 or 8 with the default toolchain), install a newer compiler or use a supported distribution.

#### Use a non-default compiler

If the system default compiler is too old, point CMake at a newer GCC or Clang. Set `CC` and `CXX` before running CMake. Example:

```shell
export CC=/opt/rh/gcc-toolset-11/root/usr/bin/gcc
export CXX=/opt/rh/gcc-toolset-11/root/usr/bin/g++
```

CMake uses `CC` and `CXX` for configuration and compilation.

### Required packages (baseline)

Install the following development packages before running CMake. You then avoid missing-library errors during configuration. Development packages provide headers and link libraries. Runtime-only packages are not enough for building.

Install on RHEL, Rocky, or Alma (package manager: `dnf` or `yum`):

```shell
dnf install cmake gcc gcc-c++ ncurses-devel openssl-devel libudev-devel libaio-devel bison
```

Install on Debian or Ubuntu (package manager: `apt`):

```shell
apt install cmake gcc g++ libncurses-dev libssl-dev libudev-dev libaio-dev bison
```

Package purposes:

* cmake — Build system generator. Minimum 3.15; verify with `cmake --version`. Default packages on RHEL 8 or Ubuntu 20.04 may be older; upgrade if needed.

* gcc / g++ — C and C++ compiler. Minimum GCC 11.3 for {{vers}}; verify with `gcc --version`. Use a newer toolchain on older distros if the default is too old.

* ncurses — Terminal library (ncurses-devel / libncurses-dev).

* openssl — SSL/TLS (openssl-devel / libssl-dev).

* libudev — Device manager library (libudev-devel / libudev-dev).

* libaio — Asynchronous I/O (libaio-devel / libaio-dev).

* bison — Parser generator.

#### Full feature set (all Percona features)

Install a complete package set to reduce CMake dependency surprises. The set covers baseline plus common Percona features (PAM, zlib, zstd, lz4, gflags, snappy). Run one of the following commands, then run CMake. You can still enable or disable features via CMake options.

Install on RHEL, Rocky Linux, or AlmaLinux:

```shell
dnf install cmake gcc gcc-c++ ncurses-devel openssl-devel libudev-devel libaio-devel bison pam-devel zlib-devel libzstd-devel lz4-devel gflags-devel snappy-devel
```

Install on Debian or Ubuntu:

```shell
apt install cmake gcc g++ libncurses-dev libssl-dev libudev-dev libaio-dev bison libpam0g-dev zlib1g-dev libzstd-dev liblz4-dev libgflags-dev libsnappy-dev
```

If CMake still reports a missing dependency, add the corresponding `-devel` or `-dev` package for your distribution and re-run CMake.

### Boost

Percona Server {{vers}} bundles Boost 1.84.0 in `extra/boost/boost_1_84_0`. CMake always uses that copy. There are no `DOWNLOAD_BOOST` or `WITH_BOOST` options, and configuration does not need network access for Boost. Do not install a system Boost or pass Boost-related CMake flags. If the bundled headers are missing or not exactly 1.84, CMake stops with a fatal error.

### Optional features and Percona-specific components (Percona layer)

Depending on the CMake options you enable, additional development packages may be required. Install the `-devel` (RHEL) or `-dev` (Debian and Ubuntu) packages so CMake can find headers and libraries.

#### System vs bundled libraries

For some components (for example, zstd and lz4), CMake can use a system library or a bundled copy.

!!! note

    Pass flags such as `-DWITH_ZSTD=system` or `-DWITH_LZ4=system` when the distro library is compatible. The OS package manager then owns updates. Use the bundled default when the system library is too old or missing. CMake does not always select system libraries without an explicit flag. The build may skip the feature or bundle a copy instead. See the Percona Server source and CMake options for valid flags.

Optional components and typical packages:

* PAM authentication — Building with the PAM plugin (`-DWITH_PAM=ON`) typically requires the PAM development package (for example, `pam-devel` on RHEL, `libpam0g-dev` on Debian/Ubuntu).

* zlib — Required for compression support. Often already satisfied by the baseline list. If CMake reports a missing zlib, install the development package (for example, `zlib-devel` on RHEL, `zlib1g-dev` on Debian/Ubuntu).

* zstd, lz4 — Compression libraries used by Percona features. Install the development packages (for example, `libzstd-devel`, `lz4-devel` on RHEL; `libzstd-dev`, `liblz4-dev` on Debian/Ubuntu). Use CMake flags such as `-DWITH_ZSTD=system` and `-DWITH_LZ4=system` if the build expects to use system libraries.

* MyRocks (RocksDB) — MyRocks builds may need libgflags and libsnappy. On RHEL, install `gflags-devel` and `snappy-devel`. On Debian and Ubuntu, install `libgflags-dev` and `libsnappy-dev`. The exact set is in the Percona Server source. If CMake reports "library not found", check the source repository or CMake configuration.

The optional-components list may not include every package for every storage engine or option. Run CMake once before a long build. Fix any missing-dependency or configuration messages first. The [MySQL 8.4 Source Installation Prerequisites](https://dev.mysql.com/doc/refman/8.4/en/source-installation-prerequisites.html) page lists more optional dependencies. The final list for your build is in the Percona Server source tree and the CMake output.

If CMake reports "library not found" for a dependency, check the lists in the preceding sections first. If the package is not listed, check the Percona Server source repository or CMake configuration.


## Install location and overwrite risk

The default install prefix is `/usr/local/mysql` (`CMAKE_INSTALL_PREFIX`). Installing to the default prefix can overwrite or conflict with a package-managed Percona Server or MySQL installation.

To avoid overwriting package-managed installations, set a custom prefix at configure time. Use `-DCMAKE_INSTALL_PREFIX` for `make install`. Example:

```shell
mkdir build && cd build && cmake .. -DFORCE_INSOURCE_BUILD=1 -DCMAKE_INSTALL_PREFIX=/opt/percona-server-{{vers}}
```

For staged installs (for example, into a package root), set `DESTDIR` when installing. The install layout replicates the full prefix under `DESTDIR`.

!!! note

    If your prefix is `/opt/percona-server-{{vers}}` and `DESTDIR` is `/tmp/stage`, the `mysqld` binary is not at `/tmp/stage/bin/mysqld`. The binary is at `/tmp/stage/opt/percona-server-{{vers}}/bin/mysqld`. Searching only under `/tmp/stage/` can look like a failed install. Plan packaging and copy steps around `DESTDIR` plus your prefix.


```shell
make -j4 install DESTDIR=/path/to/package/root
```

## Obtain the source

You can build from a Git clone when the build machine has network access to GitHub. You can also build from a source tarball. A source tarball is the standard approach on air-gapped or proxy-restricted build servers. See [Install Percona Server for MySQL from a source tarball](source-tarball.md) and [Install with binary tarballs](binary-tarball-install.md) for package-based alternatives.

### Build from a source tarball (offline or restricted network)

Many enterprise build servers cannot run `git clone` (proxy restrictions, no outbound access, or no git). In that case, obtain a source tarball on a machine that can download or build the tarball. Transfer the tarball to the build machine, then configure and build there.

Obtain the source using one of the following methods:

* Download a Percona Server source tarball from [Percona downloads](https://www.percona.com/downloads/Percona-Server-{{vers}}). Transfer that tarball to the build machine.

* On a machine that can reach GitHub, clone the repository (including submodules) and copy the tree to the build machine. Do not run CMake or `make dist` only to produce source. That configure-and-build flow compiles a binary and is more work than you need to transfer source.

On the build machine, extract the tarball or unpack the copied tree. From the extracted tree, run `mkdir build && cd build && cmake .. -DFORCE_INSOURCE_BUILD=1`, then `make` and `make install`. The following sections describe the same flow.

No git is required on the build machine if you use a source tarball.

### Build from the Git source tree

Percona uses the [Github :octicons-link-external-16:](https://github.com/) revision control system for development. To build from git you need `git` installed. The build machine must reach GitHub or a mirror.

Fetch the latest Percona Server for MySQL {{vers}} sources. A shallow clone avoids downloading full repository history:


```shell
git clone --branch {{vers}} --depth 1 https://github.com/percona/percona-server.git
cd percona-server
git submodule update --init
```

If you need full history (for example, for commit inspection), use a full clone and check out the branch:


```shell
git clone https://github.com/percona/percona-server.git
cd percona-server
git checkout {{vers}}
git submodule update --init
```

After you fetch the repository or extract a tarball, configure and build Percona Server for MySQL.


## Configure the build

Run CMake to configure the build. You can specify build options as for a normal MySQL build.

!!! note

    `-DFEATURE_SET=community` is not supported in {{vers}}. If you use `-DFEATURE_SET=community`, CMake will report: *Manually-specified variables were not used by the project: FEATURE_SET*.

Out-of-source build is the only supported approach. Keep the source tree separate from build artifacts. When the `build` directory is under the source tree, pass `-DFORCE_INSOURCE_BUILD=1`.

* Source tree — The clean repository directory containing the pristine source files. Do not run `cmake` directly inside the source tree.

* Build directory — A separate, disposable directory where object files and compilation configurations are processed. Delete the build directory at any time to reset the build environment.

* Install prefix — The destination where operational binaries, libraries, and support files are installed (for example, `/opt/percona-server-{{vers}}`).

From the repository root, use the following exact sequence:

```shell
mkdir build && cd build && cmake .. -DFORCE_INSOURCE_BUILD=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release
```

Do not run `cmake .` in the source root. That command writes generated files into the source tree and is hard to undo safely.

On newer platforms or distros, if you hit compilation errors that are
Linux-distro dependent, add `-DWITH_PACKAGE_FLAGS=OFF`:

```shell
mkdir build && cd build && cmake .. -DFORCE_INSOURCE_BUILD=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DWITH_PACKAGE_FLAGS=OFF
```

### Recovery from a contaminated source tree

If you ran `cmake .` in the source root by mistake, CMake and build artifacts are in the source tree. `make clean` does not fully reset CMake state.

Safest recovery: remove only known generated files. You then avoid touching local patches or config. From the repository root, remove `CMakeCache.txt`, the `CMakeFiles/` directory, `cmake_install.cmake`, and `Makefile`. Remove any other CMake-generated paths in the root. After that, run the out-of-source sequence again.


!!! warning

    `git clean -xfd` permanently deletes every untracked and ignored file, including uncommitted work. Use the command only when you are certain no local changes must be kept. Prefer manual removal of generated files in the repository root.


With an out-of-source build, recovery is simpler. Delete the build directory (for example, `rm -rf build`). Run `mkdir build && cd build && cmake .. -DFORCE_INSOURCE_BUILD=1` again. The source tree stays unchanged.


## Compile from source

Compile using make from the build directory. Do not use `make -j$(nproc)`.

Each parallel compile job can use about 2–4 GB RAM. The final `mysqld` link can spike to 4 GB or more in one job. Core count does not reduce that spike.

!!! note

    On a 32-core host with 16 GB RAM, `make -j32` often triggers swap or OOM kills. Cap jobs at the smaller of (RAM in GB ÷ 2) and 8. With 8 GB RAM, use `make -j4` or lower. With 16 GB or more, `make -j8` is a safe upper bound. When in doubt, use `make -j2` or plain `make`.


```shell
make -j4
```

If the OOM killer stops the build, reduce parallel jobs (for example, `make -j2`). You can also run plain `make` with no `-j`.


Install (use the same `-j` value as for the build, or a lower one if install fails due to memory):

```shell
make -j4 install
```

## Initialize and start the server

The guide does not end at `make install`. The job is not done until the database is running. You must initialize the data directory and start the server. Then use the temporary root password to log in.

### Initialize the data directory

Create a data directory and give ownership to the user that will run the server (for example, `mysql`). Then run `mysqld --initialize` with `--basedir` and `--datadir` set to your install prefix and chosen datadir path. Example (adjust the datadir path and user to match your system):

```shell
mkdir -p /var/lib/mysql-custom
chown mysql:mysql /var/lib/mysql-custom
/opt/percona-server-{{vers}}/bin/mysqld --initialize --user=mysql --basedir=/opt/percona-server-{{vers}} --datadir=/var/lib/mysql-custom
```

You must find the temporary root password after initialization. `mysqld --initialize` writes a one-time `root@localhost` password to the error log. The log is usually in the datadir (for example, `/var/lib/mysql-custom/hostname.err`). Without that password, you cannot log in as `root`. Open the error log. Search for "temporary password" or `root@localhost`. Use that password to connect and change the password. See [Post-installation](post-installation.md) for full steps.


To skip the temporary password (less secure), use `--initialize-insecure` instead of `--initialize`. Then `root@localhost` has no password until you set one.

### Start the server

Package installations provide a systemd unit (or init script) for the default binary path. A custom-prefix install (for example, `/opt/percona-server-{{vers}}`) is not managed by that unit.

!!! note

    Create or adapt a systemd unit (or init script) for a custom prefix. Set `ExecStart` to your `mysqld` path (for example, `/opt/percona-server-{{vers}}/bin/mysqld`). Set `basedir` and `datadir` to match your layout. Without that unit, the service manager will not start your build. See distribution documentation for systemd services and [Post-installation](post-installation.md).


## Maintaining a source build

A source build does not receive package-manager updates (`dnf update` / `apt upgrade`). Official packages apply security updates automatically; a custom build is a snapshot, so you must track Percona releases, pull or replace the source, rebuild, and reinstall when a CVE or new release affects your version. From the repository root, pull the latest changes and rebuild (adjust `-j` if needed). The commands use Bash `&&` chains. On PowerShell before version 7, run each line separately:

```shell
git pull
git submodule update
cd build
cmake .. -DFORCE_INSOURCE_BUILD=1
make -j4
make install
```

Applying updates: Obtain fresh source (for example, `git pull` and `git submodule update` in a clone, or a new source tarball). Then choose one of the following paths:

* Incremental build: After a pull with no CMake option changes, re-run `make` and `make install` from the existing build directory. You do not need to delete the build directory or re-run CMake. Use this path for security and minor updates.

* Full reconfigure: After CMake option changes, branch switches, or odd errors after pull, remove the build directory (`rm -rf build`). Run `mkdir build && cd build && cmake .. -DFORCE_INSOURCE_BUILD=1` with the same options. Then `make` and `make install`.


Keep configuration files (for example, `my.cnf`) and data directories outside the install prefix. Reinstalling then overwrites only the binaries and leaves your config and data intact.

Use a stable custom prefix and config/datadir paths so upgrades are predictable.

## See also

* [Install Percona Server for MySQL from repositories](installation.md) — Package-based installation.

* [Install Percona Server for MySQL from a source tarball](source-tarball.md) — Offline or restricted-network installs.

* [Install with binary tarballs](binary-tarball-install.md) — Alternative to compiling from source.

* [Build APT packages](build-apt-packages.md) — Repeatable packaging workflows.

* [Post-installation](post-installation.md) — Initialize, start, and test the server.

* [MySQL 8.4 Source Installation Prerequisites](https://dev.mysql.com/doc/refman/8.4/en/source-installation-prerequisites.html) — Upstream baseline reference.
