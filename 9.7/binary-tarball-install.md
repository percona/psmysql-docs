> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install Percona Server for MySQL 9.7 from a binary tarball

A binary tarball contains a group of files, including the source code, bundled together into one file using the `tar` command and compressed using `gzip`.

See the list of the [binary tarball available based on the Percona Server for MySQL version](https://docs.percona.com/percona-server/9.7/binary-tarball-names.html) to select the right tarball for your environment.

You can download the binary tarballs from the `Linux - Generic` [section](https://www.percona.com/downloads/Percona-Server-9.7/LATEST/binary/tarball/) on the download page.

Fetch and extract the correct binary tarball. For example for Ubuntu 22.04:

```
wget https://downloads.percona.com/downloads/Percona-Server-9.7/Percona-Server-9.7.2-3/binary/tarball/Percona-Server-9.7.2-3-Linux.x86_64.glibc2.35.tar.gz
```

Extract the tarball into the `/usr/local` directory:

```
sudo tar -xzf Percona-Server-9.7.2-3-Linux.x86_64.glibc2.35.tar.gz -C /usr/local
```

Create a symbolic link so that the default location `/usr/local/mysql` points to the extracted directory:

```
sudo ln -s /usr/local/Percona-Server-9.7.2-3-Linux.x86_64.glibc2.35 /usr/local/mysql
```

## After extraction

The tarball does not create the `mysql` user, initialize the data directory, or start the server. To run Percona Server for MySQL, you must:

1. Create the `mysql` group and the `mysql` user.
1. Initialize the data directory with `bin/mysqld --initialize --user=mysql`.
1. Start the server with `bin/mysqld_safe --user=mysql`.

The server refuses to run as the operating system `root` user unless you pass the `--user=mysql` option.

For step-by-step instructions, see [Post-installation](https://docs.percona.com/percona-server/9.7/post-installation.html).
