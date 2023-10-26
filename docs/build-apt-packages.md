# Build APT packages

If you wish to build your own Debian/Ubuntu (dpkg) packages of Percona Server for MySQL,
you first need to start with a source tarball, either from the Percona
website or by generating your own by following the instructions above ([Installing Percona Server for MySQL from the Git Source Tree](source-tarball.md)).

Extract the source tarball:

```{.bash data-prompt="$"}
$ tar xfz Percona-Server-{{release}}-Linux.x86_64.ssl102.tar.gz
$ cd Percona-Server-{{release}}
```

Copy the Debian packaging in the directory that Debian expects it to be in:

```{.bash data-prompt="$"}
$ cp -ap build-ps/debian debian
```
<!-- Do we need this part --->
Update the changelog for your distribution (here we update for the unstable
distribution - sid), setting the version number appropriately. The trailing one
in the version number is the revision of the Debian packaging.

```{.bash data-prompt="$"}
$ dch -D unstable --force-distribution -v "8.0.13-3-1" "Update to 8.0.13-3"
```

Build the Debian source package:

```{.bash data-prompt="$"}
$ dpkg-buildpackage -S
```

Use sbuild to build the binary package in a chroot:

```{.bash data-prompt="$"}
$ sbuild -d sid percona-server-{{vers}}_{{release}}.dsc
```

You can give different distribution options to `dch` and `sbuild` to build binary
packages for all Debian and Ubuntu releases.

!!! note

    [PAM Authentication Plugin](pam-plugin.md) is not built with the server by default. In order to build the Percona Server for MySQL with PAM plugin, an additional option `-DWITH_PAM=ON` should be used.
