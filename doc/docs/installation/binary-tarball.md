# Installing _Percona Server for MySQL_ from a Binary Tarball

In _Percona Server for MySQL_ 5.7.31-34 and later, the multiple binary 
tarballs are replaced with the following:

| Type    | Name                                                                  | Description                                                                        |
|---------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Full    | Percona-Server-<version number>-Linux.x86_64.glibc2.12.tar.gz         | Contains binaries, libraries, test files, and debug symbols                        |
| Minimal | Percona-Server-<version number>-Linux.x86_64.glibc2.12-minimal.tar.gz | Contains binaries, and libraries but does not include test files, or debug symbols |

Select the _Percona Server for MySQL_ 5.7 version number and type of tarball for your installation. Both binary tarballs support all distributions.

In _Percona Server for MySQL_ before 5.7.31-34, multiple tarballs are provided based on the _OpenSSL_ library available in the distribution:

> *   ssl100 - for _Debian_ prior to 9 and _Ubuntu_ prior to 14.04 versions (`libssl.so.1.0.0 => /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0`);
>     
> *   ssl101 - for _CentOS_ 6 and _CentOS_ 7 (`libssl.so.10 => /usr/lib64/libssl.so.10`);
>     
> *   ssl102 - for _Debian_ 9 and _Ubuntu_ versions starting from 14.04 (`libssl.so.1.1 => /usr/lib/libssl.so.1.1`);
>     
> *   ssl1:111 - for _CentOS_ 8 and _RedHat_ 8 (`libssl.so.1.1 => /usr/lib64/libssl.so.1.1.1b`);
>     

You can download the binary tarballs from the [`Linux - Generic` 
section](https://www.percona.com/downloads/Percona-Server-5.7/LATEST/binary/tarball/) on the download page.

Fetch the correct binary tarball. The example fetches Percona Server 
for MySQL 5.7.38-41 for Debian 10:

```shell
$ wget https://downloads.percona.com/downloads/Percona-Server-5.7/Percona-Server-5.7.38-41/binary/debian/buster/x86_64/Percona-Server-5.7.38-41-rda46e5474f9-buster-x86_64-bundle.tar
```