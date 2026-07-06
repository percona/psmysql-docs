# Install Percona Server for MySQL 8.0 from a binary tarball

A binary tarball contains a group of files, including the server binaries and support files, bundled together into one file using the `tar` command and compressed using `gzip`.

!!! note "{{post}}"

    Customers with {{post}} download binary tarballs from the private Percona repository. See [Download a {{eol}} binary tarball](tarball-eol.md).

See the list of [binary tarballs available based on the Percona Server for MySQL version](binary-tarball-names.md) to select the right tarball for your environment.
    
You can download the binary tarballs from the `Linux - Generic` [section :octicons-link-external-16:](https://www.percona.com/downloads) on the download page.

Fetch and extract the correct binary tarball. For example, for Ubuntu 22.04:

Download the tarball:

```shell
wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz
```

??? example "Expected output"

    ```{.text .no-copy}
    --2024-01-15 10:00:00--  https://downloads.percona.com/...
    Saving to: 'Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz'
    Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz   100%[=================>]  xxx MB  xx.x MB/s    in xx s
    2024-01-15 10:00:xx (xx.x MB/s) - 'Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz' saved [xxxxxx/xxxxxx]
    ```

Extract the tarball:

```shell
tar -xzf Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz
```

??? example "Expected output"

    ```{.text .no-copy}
    (No output on success.)
    ```

Change into the extracted directory:

```shell
cd Percona-Server-{{release}}-Linux.x86_64.glibc2.35
```

??? example "Expected output"

    ```{.text .no-copy}
    (No output on success.)
    ```

## After extraction

The tarball does not start the server for you. To run Percona Server you must:

1. Initialize the data directory (once) using the server executable `bin/mysqld` with `--initialize` or `--initialize-insecure`.

2. Start the server (for example with `bin/mysqld_safe` or by configuring a systemd service).

The server executable is `bin/mysqld` inside the extracted directory. Do not run it for normal operation until the data directory has been initialized.

For step-by-step instructions (including creating a data directory, initializing it, starting the server, and optional boot-time setup), see [Post-installation](post-installation.md). If you did not install under `/usr/local/mysql`, use your extraction directory instead (for example, `cd /path/to/Percona-Server-{{release}}-Linux.x86_64.glibc2.35` then `bin/mysqld --initialize`).

<!-- ## Install Percona Server for MySQL Pro from a binary tarball

You can download the required binary tarball for Percona Server for MySQL Pro using your `CLIENTID` and `TOKEN` in the following link https://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/tarballs/.

Fetch and extract the correct binary tarball using your `CLIENTID` and `TOKEN`. For example, for Oracle Linux 9:

```{.bash data-prompt="$"}
wget https://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/tarballs/Percona-Server-{{pro_release}}/Percona-Server-Pro-{{pro_release}}-Linux.x86_64.glibc2.34-debug.tar.gz
``` -->
