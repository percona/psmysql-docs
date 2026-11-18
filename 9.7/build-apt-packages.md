> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Build APT packages

If you wish to build your own Debian/Ubuntu (dpkg) packages of Percona Server for MySQL, you first need to start with a source tarball, either from the Percona website or by generating your own by following the instructions above ([Installing Percona Server for MySQL from the Git Source Tree](https://docs.percona.com/percona-server/9.7/source-tarball.html)).

Extract the source tarball:

```
tar xfz Percona-Server-9.7.2-3-Linux.x86_64.ssl102.tar.gz
cd Percona-Server-9.7.2-3
```

Copy the Debian packaging in the directory that Debian expects it to be in:

```
cp -ap build-ps/debian debian
```

Update the changelog for your distribution (here we update for the unstable distribution - sid), setting the version number appropriately. The trailing one in the version number is the revision of the Debian packaging.

```
dch -D unstable --force-distribution -v "8.0.13-3-1" "Update to 8.0.13-3"
```

Build the Debian source package:

```
dpkg-buildpackage -S
```

Use sbuild to build the binary package in a chroot:

```
sbuild -d sid percona-server-9.7_9.7.2-3.dsc
```

You can give different distribution options to `dch` and `sbuild` to build binary packages for all Debian and Ubuntu releases.

Note

[PAM Authentication Plugin](https://docs.percona.com/percona-server/9.7/pam-plugin.html) is not built with the server by default. In order to build the Percona Server for MySQL with PAM plugin, an additional option `-DWITH_PAM=ON` should be used.
