# Install Percona Server for MySQL {{vers}} using downloaded DEB packages

Download the packages from [Percona Product Downloads :octicons-link-external-16:](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

The following example downloads *Percona Server for MySQL* {{release}} release `x86_64` packages for Ubuntu 22.04:
{.power-number}

1. Use `wget` to download the tar file:

    The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads :octicons-link-external-16:](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](download-instructions.md).

    ```shell
    wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/debian/jammy/x86_64/Percona-Server-{{release}}-<revision-identifier>-jammy-x86_64-bundle.tar
    ```

2. Unpack the download to get the packages:

    ```shell
    tar xvf Percona-Server-{{release}}-<revision-identifier>-jammy-x86_64-bundle.tar
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
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

3. Install Percona Server for MySQL using `dpkg`. Run this command as root or use the sudo command:

    ```shell
    sudo dpkg -i *.deb
    ```

!!! warning

    When installing packages manually like this, you’ll need to resolve all the dependencies and install missing packages yourself. The following packages will need to be installed before you can manually install Percona Server: `mysql-common`, `libjemalloc1`, `libaio1`, and `libmecab2`.
