# Build DEB packages from source

Build custom DEB packages when you need specific configuration options, patches, or want to create packages for distribution. This process compiles Percona Server from source code and creates installable DEB files.

## When to build from source

Advantages:

 Enables custom compilation flags and configuration options

* Allows integration of custom patches or modifications

* Creates packages tailored for specific hardware or requirements

* Provides control over included features and dependencies

Disadvantages:

* Requires significant build time and system resources

* Demands expertise in Debian packaging and build tools

* Creates maintenance overhead for updates and security patches

* May introduce stability risks from custom modifications

## Prerequisites

Skills needed: Software development, packaging knowledge, build tools

Install the required build tools and dependencies:

```{.bash data-prompt="$"}
$ sudo apt install build-essential devscripts debhelper sbuild
$ sudo apt build-dep percona-server-server
```

## Build process

Start with a source tarball from the Percona website or generate your own following the Git source tree installation instructions.

Extract the source tarball:

```{.bash data-prompt="$"}
$ tar xfz Percona-Server-{{release}}-Linux.x86_64.tar.gz
$ cd Percona-Server-{{release}}
```

Copy the Debian packaging files to the expected directory structure:

```{.bash data-prompt="$"}
$ cp -ap build-ps/debian debian
```

Update the changelog for your target distribution. This example updates for the unstable distribution (sid) and sets the version number. The trailing number represents the Debian packaging revision:

```{.bash data-prompt="$"}
$ dch -D unstable --force-distribution -v "{{release}}-1" "Update to {{release}}"
```

Build the Debian source package:

```{.bash data-prompt="$"}
$ dpkg-buildpackage -S
```

Use sbuild to create the binary package in a clean chroot environment:

```{.bash data-prompt="$"}
$ sbuild -d sid percona-server-8.4_{{release}}.dsc
```

!!! note

    The PAM Authentication Plugin does not build with the server by default. Add the `-DWITH_PAM=ON` option to build Percona Server for MySQL with PAM plugin support.

## Distribution compatibility

Pass different distribution options to `dch` and `sbuild` commands to build binary packages for various Debian and Ubuntu releases. Replace `sid` with your target distribution codename (such as `bookworm`, `jammy`, or `focal`).