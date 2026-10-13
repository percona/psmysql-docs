# Install Percona Server for MySQL from a source tarball

Fetch and extract the source tarball. For example:

```shell
wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/source/tarball/percona-server-{{release}}.tar.gz
```

Unpack the download to get the source code:

```shell
tar xfz percona-server-{{release}}.tar.gz
cd percona-server-{{release}}
```

To complete the installation, follow the instructions in [Compile Percona Server for MySQL from Source](compile-percona-server.md).
