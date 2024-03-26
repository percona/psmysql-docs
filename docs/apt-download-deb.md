# Install Percona Server for MySQL 8.0 using downloaded DEB packages

When installing packages manually, you must resolve all the dependencies and install missing packages yourself. You must install the following packages before manually installing Percona Server:

* `mysql-common`

* `libjemalloc1`

* `libaio1`

* `libmecab2`.

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

1. The following example uses `Wget` to download the Percona Server 8.0 bundle from the specified URL. The bundle is a tar archive containing the Percona Server 8.0.31-23 binary for Debian Buster (x86_64 architecture):

    ```{.bash data-prompt="$"}
    $ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.31-23/binary/debian/buster/x86_64/Percona-Server-8.0.31-23-r71449379-buster-x86_64-bundle.tar
    ```

2. The command line instruction uses the `tar` command to extract files from a tarball (a type of compressed file). The `tar` command is a Unix utility that stores and extracts files from an archive file known as a tarfile. 

    The `xvf` option combines three separate options: `x`, `v`, and `f`. 

    * `x` extract the files from the archive

    * `v` verbose - print the file names as they are extracted

    * `f` file - use the following argument as the name of the archive file

    The following command extracts the contents of the  `Percona-Server-8.0.31-23-r71449379-buster-x86_64-bundle.tar` file and prints the file names.

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

3. Install Percona Server for MySQL using the `dpkg` utility to install Debian (.deb) packages. The installation requires either root or the `sudo` command. `sudo` allows you to run programs with the security privileges of another user, usually as the superuser.

    `dpkg` is a package manager for Debian-based systems and can install, remove, and provide information about `.deb` packages. 

    The `-i` option tells `dpkg` to install the package.

    The `*.deb` is a wildcard that matches any file in the current directory that ends with the `.deb` extension. 


    ```{.bash data-prompt="$"}
    $ sudo dpkg -i *.deb
    ```

Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. For more information, see the [TokuDB Introduction](tokudb-intro.md) and [TokuDB changes by Percona Server for MySQL version](tokudb-version-changes.md). 


