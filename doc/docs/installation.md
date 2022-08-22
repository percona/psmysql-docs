# Installing *Percona Server for MySQL* 5.7


Before installing, you might want to read the Percona Server for MySQL 5.7 Release notes.

## Installing *Percona Server for MySQL* from Repositories

Percona provides repositories for **yum** (`RPM` packages for *Red Hat*, *CentOS* and *Amazon Linux AMI*) and **apt** (`.deb` packages for *Ubuntu* and *Debian*) for software such as *Percona Server for MySQL*, *Percona XtraBackup*, and *Percona Toolkit*. This makes it easy to install and update your software and its dependencies through your operating system’s package manager. This is the recommended way of installing where possible.

Following guides describe the installation process for using the official Percona repositories for `.deb` and `.rpm` packages.


* Installing Percona Server for MySQL on *Debian* and *Ubuntu*


* Installing Percona Server for MySQL on Red Hat Enterprise Linux and CentOS







## Building *Percona Server for MySQL* Debian/Ubuntu packages

If you wish to build your own Percona Server Debian/Ubuntu (dpkg) packages,
you first need to start with a source tarball, either from the Percona
website or by generating your own by following the instructions above(
Installing Percona Server for MySQL from the Git Source Tree).

Extract the source tarball:

```
$ tar xfz percona-server-5.7.10-3.tar.gz
$ cd percona-server-5.7.10-3
```

Put the debian packaging in the directory that Debian expects it to be in:

```
$ cp -ap build-ps/debian debian
```

Update the changelog for your distribution (here we update for the unstable
distribution - sid), setting the version number appropriately. The trailing one
in the version number is the revision of the Debian packaging.

```
$ dch -D unstable --force-distribution -v "5.7.10-3-1" "Update to 5.7.10-3"
```

Build the Debian source package:

```
$ dpkg-buildpackage -S
```

Use sbuild to build the binary package in a chroot:

```
$ sbuild -d sid percona-server-5.7_5.7.10_3-1.dsc
```

You can give different distribution options to dch and sbuild to build binary
packages for all Debian and Ubuntu releases.

**NOTE**: PAM Authentication Plugin is not built with the server by default. In order to build the Percona Server with PAM plugin, additional option `-DWITH_PAM=ON` should be used.
