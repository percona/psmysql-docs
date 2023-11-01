# Install Percona Server for MySQL 8.0 using downloaded DEB packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

The following example downloads Percona Server for MySQL 8.0.31-23 release packages for Debian 10:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.31-23/binary/debian/buster/x86_64/Percona-Server-8.0.31-23-r71449379-buster-x86_64-bundle.tar
```

Unpack the download to get the packages:

```{.bash data-prompt="$"}
$ tar xvf Percona-Server-8.0.31-23-r71449379-buster-x86_64-bundle.tar
```
??? example "Expected output"

    ```text
    libperconaserverclient21_8.0.31-23-1.buster_amd64.deb
    libperconaserverclient21-dev_8.0.31-23-1.buster_amd64.deb
    percona-mysql-router_8.0.31-23-1.buster_amd64.deb
    percona-server-client_8.0.31-23-1.buster_amd64.deb
    percona-server-common_8.0.31-23-1.buster_amd64.deb
    percona-server-dbg_8.0.31-23-1.buster_amd64.deb
    percona-server-rocksdb_8.0.31-23-1.buster_amd64.deb
    percona-server-server_8.0.31-23-1.buster_amd64.deb
    percona-server-source_8.0.31-23-1.buster_amd64.deb
    percona-server-test_8.0.31-23-1.buster_amd64.deb
    ```

Install Percona Server for MySQL using `dpkg`. Run this command as root or use the sudo command:

```{.bash data-prompt="$"}
$ sudo dpkg -i *.deb
```

!!! note

    Percona Server for MySQL 8.0 comes with the TokuDB storage engine. You can find more information on how to install and enable the TokuDB storage in the TokuDB Installation guide.

	Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. For more information, see the TokuDB Introduction.

!!! warning

    When installing packages manually like this, you’ll need to resolve all the dependencies and install missing packages yourself. The following packages will need to be installed before you can manually install Percona Server: `mysql-common`, `libjemalloc1`, `libaio1`, and `libmecab2`.
