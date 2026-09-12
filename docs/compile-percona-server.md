# Compile Percona Server for MySQL from source

This page is a task guide for installing Percona Server for MySQL {{vers}} by compiling from source.

The following instructions install Percona Server for MySQL {{vers}} on your system.

## When to use this guide

Compiling from source is an advanced installation method. Prefer repository packages (APT or DNF) or binary tarballs unless you need a custom or debug build.

Use the compile guide when you need a custom or debug build from source (for example, to test patches or build with non-default options).

For RPM, DEB, or repeatable production builds, use Percona automated packaging tooling. The tooling installs dependencies and produces installable packages. See [Build APT packages](build-apt-packages.md), [Install Percona Server for MySQL from repositories](installation.md), and the Percona Server source repository.


!!! warning

    A manual source build does not match the performance or security profile of official Percona binaries. Release builds use Profile-Guided Optimization (PGO), Link-Time Optimization (LTO), and hardened compiler flags.

Treat a custom-compiled binary as suitable for development or testing, not as a drop-in production replacement for official packages.

## Installation prerequisites

The build requires a fixed set of dependencies. Install the packages for your platform before running CMake. Configuration and compilation then succeed without discovering missing libraries one at a time.

Toolchain requirements for Percona Server {{vers}}:

* Percona Server {{vers}} uses modern C++ and requires a minimum glibc version and a modern linker (binutils).

* Do not assume a modern GCC (for example, 11+) implies a modern binutils. The linker resolves C++20 symbols. An old linker can fail the build after hours of compilation.

* On many systems a newer GCC comes from a side-repo (for example, Software Collections). The system linker may stay old. Check both the compiler and the linker.


Glibc version check:

* Run `ldd --version`. If the version is less than 2.28, the build will fail. Upgrade your OS or use a Docker container with a modern base.

Linker version check:

* Run `ld -v` (or `ld.bfd -v`). If the version is less than 2.30, C++20 symbol resolution will fail. Install a newer binutils package.

On older LTS distros (for example, RHEL 7 or 8 with default or SCL toolchain), late failures are often glibc or linker related. Use a distribution and toolchain Percona documents as supported for {{vers}}.


Install baseline packages on RHEL, Rocky, or Alma (package manager: `dnf` or `yum`):

```shell
dnf install cmake gcc gcc-c++ ncurses-devel openssl-devel libudev-devel libaio-devel bison wget curl
```

Install baseline packages on Debian or Ubuntu (package manager: `apt`):

```shell
apt install cmake gcc g++ libncurses-dev libssl-dev libudev-dev libaio-dev bison wget curl
```

If you use `-DDOWNLOAD_BOOST=1`, install `wget` or `curl`. The build machine needs network access during configuration. Without network access, configuration can fail with a download error unrelated to C++. The package lists include both tools so a minimal host has at least one.

Additional packages may be required for optional features (for example, PAM, zlib, MyRocks). See [Percona Server for MySQL {{vers}} source installation prerequisites](source-installation-prerequisites.md) for the Percona-specific list. The [MySQL 8.4 Source Installation Prerequisites](https://dev.mysql.com/doc/refman/8.4/en/source-installation-prerequisites.html) page is the upstream baseline reference.


If CMake reports "library not found" for a dependency, check the prerequisites doc first. If the package is not listed, check the Percona Server source repository or CMake configuration.


## Install location and overwrite risk

The default install prefix is `/usr/local/mysql` (`CMAKE_INSTALL_PREFIX`). Installing to the default prefix can overwrite or conflict with a package-managed Percona Server or MySQL installation.

To avoid overwriting package-managed installations, set a custom prefix at configure time. Use that prefix consistently for `make install`:

```shell
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DCMAKE_INSTALL_PREFIX=/opt/percona-server-{{vers}}
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

Obtain a tarball using one of the following methods:

* Download a Percona Server source tarball from [Percona downloads](https://www.percona.com/downloads/Percona-Server-{{vers}}).

* On a machine with a full clone, generate a tarball from an out-of-source build:

```shell
mkdir build && cd build
cmake ..
make dist
```

See the exception in [Build from the Git source tree](#build-from-the-git-source-tree) if `make dist` must run from the repository root.

On the build machine, extract the tarball. Create a build directory inside the extracted tree. Run `cmake ..` from that directory, then `make` and `make install`. The following sections describe the same out-of-source flow.


No git is required on the build machine.

### Build from the Git source tree

Percona uses the [Github :octicons-link-external-16:](https://github.com/) revision control system for development. To build from git you need `git` installed. The build machine must reach GitHub or a mirror.

Fetch the latest Percona Server for MySQL {{vers}} sources. A shallow clone avoids downloading full repository history:


```shell
git clone --branch {{vers}} --depth 1 https://github.com/percona/percona-server.git
cd percona-server
git submodule update --init
```

If you need full history (for example, for `make dist` or commit inspection), use a full clone and check out the branch:


```shell
git clone https://github.com/percona/percona-server.git
cd percona-server
git checkout {{vers}}
git submodule update --init
```

If you modify Percona Server for MySQL {{vers}} and plan to distribute the work, generate a source tarball the same way Percona does for releases:

```shell
mkdir build && cd build
cmake ..
make dist
```

!!! note

    If `make dist` fails from the build directory, some upstream versions require the repository root. In that case only, run `cmake .` and `make dist` from the root. Remove generated files (`CMakeCache.txt`, `CMakeFiles/`, `Makefile`, `cmake_install.cmake`). See [Recovery from a contaminated source tree](#recovery-from-a-contaminated-source-tree).


After you fetch the repository or extract a tarball, configure and build Percona Server for MySQL.


## Configure the build

Run CMake to configure the build. You can specify build options as for a normal MySQL build.

!!! note

    `-DFEATURE_SET=community` is not supported in {{vers}}. If you use
`-DFEATURE_SET=community`, CMake will report: *Manually-specified variables were not used by the project:
FEATURE_SET*.

Boost version requirements:

Percona Server {{vers}} requires a specific Boost version (defined in the source tree). If the system Boost differs from the tree (for example, 1.8x when the tree expects 1.77), CMake fails or produces an incompatible build.

!!! note

    Do not pass `-DDOWNLOAD_BOOST=1` and `-DWITH_BOOST=/path/to/boost` in the same CMake command. See [source installation prerequisites](source-installation-prerequisites.md#boost) for Option A and Option B.

To avoid version mismatches, use one of the following options:

* Let CMake download Boost: add `-DDOWNLOAD_BOOST=1` to the `cmake` command. You need `wget` or `curl` and network access during configuration. On air-gapped or container hosts, use a local Boost (the next option) instead.

* Use a local Boost tree: add `-DWITH_BOOST=/path/to/boost`. The path must match the version required by the source.


Do not rely on a single hardcoded Boost path or version in documentation. Check the source or CMake output for the exact version required.

Out-of-source build is the only supported approach. Keep the source tree separate from build artifacts:

* Source tree — The clean repository directory containing the pristine source files. Do not run `cmake` directly inside the source tree.

* Build directory — A separate, disposable directory where object files and compilation configurations are processed. Delete the build directory at any time to reset the build environment.

* Install prefix — The destination where operational binaries, libraries, and support files are installed (for example, `/opt/percona-server-{{vers}}`).

From the repository root, use the following exact sequence:

```shell
mkdir build && cd build && cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release
```

Do not run `cmake .` in the source root. That command writes generated files into the source tree and is hard to undo safely.

If CMake reports a Boost version mismatch, add `-DDOWNLOAD_BOOST=1` to the `cmake` command so the correct Boost is downloaded automatically.

On newer platforms or distros, if you hit compilation errors that are
Linux-distro dependent, add `-DWITH_PACKAGE_FLAGS=OFF`:

```shell
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DWITH_PACKAGE_FLAGS=OFF
```

### Recovery from a contaminated source tree

If you ran `cmake .` in the source root by mistake, CMake and build artifacts are in the source tree. `make clean` does not fully reset CMake state.

Safest recovery: remove only known generated files. You then avoid touching local patches or config. From the repository root, remove `CMakeCache.txt`, the `CMakeFiles/` directory, `cmake_install.cmake`, and `Makefile`. Remove any other CMake-generated paths in the root. After that, run the out-of-source sequence again.


!!! warning

    `git clean -xfd` permanently deletes every untracked and ignored file, including uncommitted work. Use the command only when you are certain no local changes must be kept. Prefer manual removal of generated files in the repository root.


With an out-of-source build, recovery is simpler. Delete the build directory (for example, `rm -rf build`). Run `mkdir build && cd build && cmake ..` again. The source tree stays unchanged.


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

By building from source you opt out of package-manager updates (`dnf update` / `apt upgrade`). You become the release engineer and your own security officer. Track Percona security and release announcements. Re-pull, re-patch, and re-compile when CVEs or releases affect your version.

!!! note

    A source build is a snapshot in time. Without ongoing patches, you run known-vulnerable software after CVE publication. Official packages receive security updates automatically. Use the following maintenance checklist.


### Maintenance checklist

Complete these tasks on a regular schedule:

* Security patching: From the repository root, pull the latest changes and rebuild. Then reinstall (adjust `-j` if needed). The commands use Bash `&&` chains. On PowerShell before version 7, run each line separately:


```shell
git pull
git submodule update
cd build
cmake ..
make -j4
make install
```

Applying updates: Obtain fresh source (for example, `git pull` and `git submodule update` in a clone, or a new source tarball). Then choose one of the following paths:

* Incremental build: After a pull with no CMake option changes, re-run `make` and `make install` from the existing build directory. You do not need to delete the build directory or re-run CMake. Use this path for security and minor updates.

* Full reconfigure: After CMake option changes, branch switches, or odd errors after pull, remove the build directory (`rm -rf build`). Run `mkdir build && cd build && cmake ..` with the same options. Then `make` and `make install`.


Keep configuration files (for example, `my.cnf`) and data directories outside the install prefix. Reinstalling then overwrites only the binaries and leaves your config and data intact.

Use a stable custom prefix and config/datadir paths so upgrades are predictable.
