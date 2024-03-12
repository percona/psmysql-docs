# Install Percona Server for MySQL from a source tarball

Fetch and extract the source tarball. For example:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-Server-innovative-release/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz
```

Unpack the download to get the packages:

```{.bash data-prompt="$"}
$ tar xfz Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz
```

To complete the installation, follow the instructions in [Compile Percona Server for MySQL from Source](compile-percona-server.md).
