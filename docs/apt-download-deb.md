# Install Percona Server for MySQL {{vers}} using downloaded DEB packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

The following example downloads Percona Server for MySQL {{release}} release packages for Debian 10:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/debian/buster/x86_64/Percona-Server-{{release}}-r71449379-buster-x86_64-bundle.tar
```

Unpack the download to get the packages:

```{.bash data-prompt="$"}
$ tar xvf Percona-Server-{{release}}-r71449379-buster-x86_64-bundle.tar
```
??? example "Expected output"

    ```text
    libperconaserverclient21_{{release}}-1.buster_amd64.deb
    libperconaserverclient21-dev_{{release}}-1.buster_amd64.deb
    percona-mysql-router_{{release}}-1.buster_amd64.deb
    percona-server-client_{{release}}-1.buster_amd64.deb
    percona-server-common_{{release}}-1.buster_amd64.deb
    percona-server-dbg_{{release}}-1.buster_amd64.deb
    percona-server-rocksdb_{{release}}-1.buster_amd64.deb
    percona-server-server_{{release}}-1.buster_amd64.deb
    percona-server-source_{{release}}-1.buster_amd64.deb
    percona-server-test_{{release}}-1.buster_amd64.deb
    ```

Install Percona Server for MySQL using `dpkg`. Run this command as root or use the sudo command:

```{.bash data-prompt="$"}
$ sudo dpkg -i *.deb
```

!!! warning

    When installing packages manually like this, you’ll need to resolve all the dependencies and install missing packages yourself. The following packages will need to be installed before you can manually install Percona Server: `mysql-common`, `libjemalloc1`, `libaio1`, and `libmecab2`.
