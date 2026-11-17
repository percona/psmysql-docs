# Install Percona Server for MySQL {{vers}} from a binary tarball

A binary tarball contains a group of files, including the source code, bundled together into one file using the `tar` command and compressed using `gzip`. 

See the list of the [binary tarball available based on the Percona Server for MySQL version](binary-tarball-names.md) to select the right tarball for your environment.
    
You can download the binary tarballs from the `Linux - Generic` [section :octicons-link-external-16:](https://www.percona.com/downloads/Percona-Server-{{vers}}/LATEST/binary/tarball/) on the download page.

Fetch and extract the correct binary tarball. For example for Ubuntu 22.04:

```shell
wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz
```

Extract the tarball into the `/usr/local` directory:

```shell
sudo tar -xzf Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz -C /usr/local
```

Create a symbolic link so that the default location `/usr/local/mysql` points to the extracted directory:

```shell
sudo ln -s /usr/local/Percona-Server-{{release}}-Linux.x86_64.glibc2.35 /usr/local/mysql
```

## After extraction

The tarball does not create the `mysql` user, initialize the data directory, or start the server. To run Percona Server for MySQL, you must:

1. Create the `mysql` group and the `mysql` user.

2. Initialize the data directory with `bin/mysqld --initialize --user=mysql`.

3. Start the server with `bin/mysqld_safe --user=mysql`.

The server refuses to run as the operating system `root` user unless you pass the `--user=mysql` option.

For step-by-step instructions, see [Post-installation](post-installation.md).
