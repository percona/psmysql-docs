# Installing Percona Server for MySQL 5.7 from a Binary Tarball

!!! note

    The following instructions install Percona Server for MySQL 5.7.
    The instructions to install [Percona Server for MySQL 8.0 are available at this location](https://docs.percona.com/percona-server/latest/installation.html#installing-percona-server-from-a-binary-tarball).

## Download a {{post}} binary tarball

Version {{release}} contains fixes as part of the [MySQL 5.7 post-EOL support from Percona], available to customers.

Community members can [build this release from the source].

You can download the binary tarball for Percona Server for MySQL release in the {{post}} program using your `CLIENTID` and `TOKEN`.

| Type    | Name                                                                |Description         |
|---------|---------------------------------------------------------------------|--------------------|
| Full    | Percona-Server-&lt;release&gt;/private/[CLIENTID]-[TOKEN]/Percona-Server-5.7/Percona-Server-&lt;release&gt;/binary/tarball/Percona-Server-&lt;release&gt;-Linux.x86_64.glibc2.17.tar.gz   | Contains binaries, libraries, test files, and debug symbols   |
| Minimal | Percona-Server-&lt;release&gt;/private/[CLIENTID]-[TOKEN]/Percona-Server-5.7/Percona-Server-&lt;release&gt;-Linux.x86_64.glibc2.12-minimal.tar.gz | Contains binaries, and libraries but does not include test files, or debug symbols. |

Fetch and extract the correct binary tarball using your `CLIENTID` and `TOKEN`. For example, for Oracle Linux 9, use the following command:

```{.bash data-prompt="$"}
 $ wget https://repo.percona.com/private/[CLIENTID-[TOKEN]/Percona-Server-5.7/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.17.tar.gz 
```

## Types and names of binary tarballs

In _Percona Server for MySQL_ 5.7.31-34 and later, the multiple binary
tarballs are replaced with the following:

| Type    | Name                                                                |Description         |
|---------|---------------------------------------------------------------------|--------------------|
| Full    | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.12.tar.gz  | Contains binaries, libraries, test files, and debug symbols   |
| Minimal | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.12-minimal.tar.gz | Contains binaries, and libraries but does not include test files, or debug symbols. |

Select the Percona Server for MySQL 5.7 version number and type of tarball for 
your installation. Both binary tarballs support all distributions.

In Percona Server for MySQL before 5.7.31-34, multiple tarballs are provided 
based on the OpenSSL library available in the distribution:

*   ssl100 - for Debian prior to 9 and Ubuntu prior to 14.04 versions (`libssl.so.1.0.0 => /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0`);

*   ssl101 - for _CentOS_ 6 and _CentOS_ 7 (`libssl.so.10 => /usr/lib64/libssl.so.10`);

*   ssl102 - for _Debian_ 9 and _Ubuntu_ versions starting from 14.04 (`libssl.so.1.1 => /usr/lib/libssl.so.1.1`);

*   ssl1:111 - for _CentOS_ 8 and _RedHat_ 8 (`libssl.so.1.1 => /usr/lib64/libssl.so.1.1.1b`);

You can download the binary tarballs from the [`Linux - Generic`
section](https://www.percona.com/downloads) on the download page. See [download instructions](download-instructions.md)

Fetch the correct binary tarball. The example fetches Percona Server
for MySQL 5.7.38-41 for Debian 10:

```shell
$ wget https://downloads.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.38-41/binary/debian/buster/x86_64/Percona-Server-5.7.38-41-rda46e5474f9-buster-x86_64-bundle.tar
```

[MySQL 5.7 Post-EOL Support from Percona]: https://www.percona.com/post-mysql-5-7-eol-support

[build this release from the source]: git-source-tree.md
