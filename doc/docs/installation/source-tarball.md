#Installing _Percona Server for MySQL_ 5.7 from a Source Tarball

!!! note

    The following instructions install Percona Server for MySQL 5.7 from a source tarball. 
    The instructions to install [Percona Server for MySQL 8.0 from a source tarball are available at this location](https://docs.percona.com/percona-server/latest/installation.html#installing-from-source-tarball).


Fetch and extract the source tarball from [Percona Downloads](https://www.percona.com/downloads/Percona-Server-5.7/LATEST/). The 
following example downloads and extracts Percona Server for MySQL 5.7.
38-41 on Ubuntu 22.04:

```shell
$ wget https://downloads.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.38-41/binary/debian/focal/x86_64/Percona-Server-5.7.38-41-rda46e5474f9-focal-x86_64-bundle.tar
```

The output lists the downloaded file:

```text
...
Saving to: 'Percona-Server-5.7.38-41-rda46e5474f9-focal-x86_64-bundle.tar'
```

Extract the tar file:

```shell
$ tar xvf Percona-Server-5.7.38-41-rda46e5474f9-focal-x86_64-bundle.tar
```
The output lists the files:

```text
libperconaserverclient20_5.7.38-41-1.focal_amd64.deb
libperconaserverclient20-dev_5.7.38-41-1.focal_amd64.deb
percona-server-5.7-dbg_5.7.38-41-1.focal_amd64.deb
percona-server-client-5.7_5.7.38-41-1.focal_amd64.deb
percona-server-common-5.7_5.7.38-41-1.focal_amd64.deb
percona-server-rocksdb-5.7_5.7.38-41-1.focal_amd64.deb
percona-server-server-5.7_5.7.38-41-1.focal_amd64.deb
percona-server-source-5.7_5.7.38-41-1.focal_amd64.deb
percona-server-test-5.7_5.7.38-41-1.focal_amd64.deb
percona-server-tokudb-5.7_5.7.38-41-1.focal_amd64.deb
```
Follow the instructions in Compiling Percona Server for MySQL from 
Source to complete the installation.