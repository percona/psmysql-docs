# Install Percona Server for MySQL 8.0 from a binary tarball

A binary tarball contains a group of files, including the source code, bundled together into one file using the `tar` command and compressed using `gzip`. 

See the list of the [binary tarball available based on the Percona Server for MySQL version](binary-tarball-names.md) to select the right tarball for your environment.
    
You can download the binary tarballs from the `Linux - Generic` [section](https://www.percona.com/downloads) on the download page.

Fetch and extract the correct binary tarball. For example, for Debian 10:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.26-16/binary/tarball/Percona-Server-8.0.26-16-Linux.x86_64.glibc2.12.tar.gz
```

## Install Percona Server for MySQL Pro from a binary tarball

You can download the required binary tarball for Percona Server for MySQL Pro using your `CLIENTID` and `TOKEN` in the following link https://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/tarballs/.

Fetch and extract the correct binary tarball using your `CLIENTID` and `TOKEN`. For example, for Oracle Linux 9:

```{.bash data-prompt="$"}
wget https://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/tarballs/Percona-Server-8.0.35-27/Percona-Server-Pro-8.0.35-27-Linux.x86_64.glibc2.34-debug.tar.gz
```
