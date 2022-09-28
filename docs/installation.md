# Installing Percona Server for MySQL 8.0.29-21

This page provides information on how you can install *Percona Server for MySQL*. The following options are available:


* [Installing Percona Server for MySQL from Repositories](#installing-percona-server-for-mysql-from-repositories) (recommended)


* Installing *Percona Server for MySQL* from Downloaded [rpm](installation/yum_repo.md#standalone-rpm) or [apt](installation/apt_repo.md#standalone-deb) Packages


* [Installing Percona Server for MySQL from a Binary Tarball](#installing-percona-server-for-mysql-from-a-binary-tarball)


* [Installing Percona Server for MySQL from a Source Tarball](#installing-percona-server-for-mysql-from-a-source-tarball)


* [Installing Percona Server for MySQL from the Git Source Tree](#installing-percona-server-for-mysql-from-the-git-source-tree)


* [Compiling Percona Server for MySQL from Source](#compiling-percona-server-for-mysql-from-source)

Before installing, you might want to read the [Percona Server for MySQL 8.0 Release notes](release-notes/release-notes_index.md).

## Installing *Percona Server for MySQL* from Repositories

*Percona* provides repositories for **yum** (`RPM` packages for *Red Hat*, *CentOS* and *Amazon Linux AMI*) and **apt** (`.deb` packages for *Ubuntu* and *Debian*) for software such as *Percona Server for MySQL*, *Percona XtraBackup*, and *Percona Toolkit*. This makes it easy to install and update your software and its dependencies through your operating system’s package manager. This is the recommended way of installing where possible.

The following guides describe the installation process for using the official Percona repositories for the `.deb` and `.rpm` packages.


* [Installing *Percona Server for MySQL* on *Debian* and *Ubuntu*](installation/apt_repo.md)


* [Installing *Percona Server for MySQL* on Red Hat Enterprise Linux and CentOS](installation/yum_repo.md)


## Installing *Percona Server for MySQL* from a Binary Tarball

In *Percona Server for MySQL* 8.0.20-11 and later, select the **Percona Server for MySQL** 8.0 version number and the type of tarball for your installation. The multiple binary tarballs from earlier versions have been replaced with the following:

| Type    | Name                                                                        | Operating systems                                                  | Description                                                                       |
|---------|-----------------------------------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Full    | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.12.tar.gz         | Built for CentOS 6                                                 | Contains binaries, libraries, test files, and debug symbols                       |
| Minimal | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.12-minimal.tar.gz | Built for CentOS 6                                                 | Contains binaries and libraries but does not include test files, or debug symbols |
| Full    | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.17.tar.gz         | Compatible with any supported operating system except for CentOS 6 | Contains binaries, libraries, test files, and debug symbols                       |
| Minimal | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.17-minimal.tar.gz | Compatible with any supported operating system except for CentOS 6 | Contains binaries and libraries but does not include test files or debug symbols  |

Implemented in *Percona for MySQL* 8.0.26-16, the following binary tarballs
are available for the MyRocks ZenFS installation. See [Installing and configuring Percona Server for MySQL with ZenFS support](myrocks/zenfs.md#zenfs) for more information and the installation procedure.

| Type    | Name                                                                              | Description                                                                          |
|---------|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Full    | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.31-zenfs.tar.gz         | Contains the binaries, libraries, test files, and debug symbols                      |
| Minimal | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.31-zenfs-minimal.tar.gz | Contains the binaries and libraries but does not include test files or debug symbols |

At this time, you can enable the ZenFS plugin in the following distributions:

| Distribution Name | Notes                                                                                             |
|-------------------|---------------------------------------------------------------------------------------------------|
| Debian 11.1       | Able to run the ZenFS plugin                                                                      |
| Ubuntu 20.04.3    | Requires the 5.11 HWE kernel patched with the allow blk-zoned ioctls without CAPT_SYS_ADMIN patch |

If you do not enable the ZenFS functionality on Ubuntu 20.04, the binaries with ZenFS support can run on the standard 5.4 kernel. [Other Linux distributions](https://zonedstorage.io/docs/distributions/linux/) are adding support for ZenFS, but Percona does not provide installation packages for those distributions.

In *Percona Server for MySQL* before 8.0.20-11, multiple tarballs are provided based on the  *OpenSSL* library available in the distribution:

> 
> * ssl100 - for *Debian* prior to 9 and *Ubuntu* prior to 14.04 versions (`libssl.so.1.0.0 => /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0`);


> * ssl102 - for *Debian* 9 and *Ubuntu* versions starting from 14.04 (`libssl.so.1.1 => /usr/lib/libssl.sl.1.1`)


> * ssl101 - for *CentOS* 6 and *CentOS* 7 (`libssl.so.10 => /usr/lib64/libssl.so.10`);


> * ssl102 - for *CentOS* 8 and *RedHat* 8  (`libssl.so.1.1 => /usr/lib/libssl.so.1.1.1b`);

You can download the binary tarballs from the `Linux - Generic` [section](https://www.percona.com/downloads/Percona-Server-8.0/LATEST/binary/tarball/) on the download page.

Fetch and extract the correct binary tarball. For example for *Debian 10*:

```shell
$ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.26-16/binary/tarball/Percona-Server-8.0.26-16-Linux.x86_64.glibc2.12.tar.gz
```

## Installing *Percona Server for MySQL* from a Source Tarball

Fetch and extract the source tarball. For example:

```shell
$ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.26-16/binary/tarball/Percona-Server-8.0.26-16-Linux.x86_64.glibc2.12.tar.gz
$ tar xfz Percona-Server-8.0.26-16-Linux.x86_64.glibc2.12.tar.gz
```

Next, follow the instructions in [Compiling Percona Server for MySQL from Source](#compiling-percona-server-for-mysql-from-source) below.

## Installing *Percona Server for MySQL* from the Git Source Tree

Percona uses the [Github](http://github.com/) revision
control system for development. To build the latest *Percona Server for MySQL*
from the source tree, you will need `git` installed on your system.

You can now fetch the latest *Percona Server for MySQL* 8.0 sources.

```shell
$ git clone https://github.com/percona/percona-server.git
$ cd percona-server
$ git checkout 8.0
$ git submodule init
$ git submodule update
```

If you are going to be making changes to *Percona Server for MySQL* 8.0 and wanting
to distribute the resulting work, you can generate a new source tarball
(exactly the same way as we do for release):

```shell
$ cmake .
$ make dist
```

Next, follow the instructions in [Compiling Percona Server for MySQL from Source](#compiling-percona-server-for-mysql-from-source) below.

## Compiling *Percona Server for MySQL* from Source

After either fetching the source repository or extracting a source tarball
(from Percona or one you generated yourself), you will now need to
configure and build *Percona Server for MySQL*.

First, run CMake to configure the build. Here you can specify all the normal
build options as you do for a normal *MySQL* build. Depending on what
options you wish to compile *Percona Server for MySQL* with, you may need other
libraries installed on your system. Here is an example using a
configure line similar to the options that Percona uses to produce
binaries:

```shell
$ cmake . -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DFEATURE_SET=community
```

Now, compile using make

```shell
$ make
```

Install:

```shell
$ make install
```

*Percona Server for MySQL* 8.0 will now be installed on your system.

## Building *Percona Server for MySQL* Debian/Ubuntu packages

If you wish to build your own Debian/Ubuntu (dpkg) packages of *Percona Server for MySQL*,
you first need to start with a source tarball, either from the Percona
website or by generating your own by following the instructions above ([Installing Percona Server for MySQL from the Git Source Tree](installation.md#source-from-git)).

Extract the source tarball:

```shell
$ tar xfz Percona-Server-8.0.13-3-Linux.x86_64.ssl102.tar.gz
$ cd Percona-Server-8.0.13-3
```

Copy the Debian packaging in the directory that Debian expects it to be in:

```shell
$ cp -ap build-ps/debian debian
```

Update the changelog for your distribution (here we update for the unstable
distribution - sid), setting the version number appropriately. The trailing one
in the version number is the revision of the Debian packaging.

```shell
$ dch -D unstable --force-distribution -v "8.0.13-3-1" "Update to 8.0.13-3"
```

Build the Debian source package:

```shell
$ dpkg-buildpackage -S
```

Use sbuild to build the binary package in a chroot:

```shell
$ sbuild -d sid percona-server-8.0_8.0.13-3-1.dsc
```

You can give different distribution options to `dch` and `sbuild` to build binary
packages for all Debian and Ubuntu releases.

!!! note

    [PAM Authentication Plugin](security/pam_plugin.md#pam-plugin) is not built with the server by default. In order to build the *Percona Server for MySQL* with PAM plugin, an additional option `-DWITH_PAM=ON` should be used.
