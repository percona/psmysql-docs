# Install Percona Server for MySQL {{vers}} from a binary tarball

A binary tarball contains a group of files, including the source code, bundled together into one file using the `tar` command and compressed using `gzip`. 

See the list of the [binary tarball available based on the Percona Server for MySQL version](binary-tarball-names.md) to select the right tarball for your environment.
    
You can download the binary tarballs from the `Linux - Generic` [section] on the download page.

Fetch and extract the correct binary tarball. For example for *Debian 10*:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.12.tar.gz
```

[section]: https://www.percona.com/downloads/Percona-Server-{{vers}}/LATEST/binary/tarball/