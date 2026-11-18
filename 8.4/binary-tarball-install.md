> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Install Percona Server for MySQL 8.4 from a binary tarball

A binary tarball is one file that contains the server binaries and support files. The `tar` command bundles the files, and `gzip` compresses them.

Use a binary tarball in the following cases:

- You need to run more than one version of Percona Server for MySQL on the same host
- Percona does not provide a package for your Linux distribution

For all other cases, use [APT](https://docs.percona.com/percona-server/8.4/apt-repo.html) or [DNF](https://docs.percona.com/percona-server/8.4/yum-repo.html) packages.

This page installs the glibc 2.35 tarball on Ubuntu 26.04 (`x86_64`). For other operating systems, select a tarball on the [binary tarball file names](https://docs.percona.com/percona-server/8.4/binary-tarball-names.html) page. Package names for other libraries are on the [Operating system libraries](https://docs.percona.com/percona-server/8.4/os-libraries.html) page.

Generic binary tarballs are built for `x86_64`. Percona publishes ARM64 (`aarch64`) builds as [APT](https://docs.percona.com/percona-server/8.4/apt-repo.html) and [DNF](https://docs.percona.com/percona-server/8.4/yum-repo.html) packages, as [Docker](https://docs.percona.com/percona-server/8.4/docker.html) images (use the `8.4.12-arm64` tag), and as [source](https://docs.percona.com/percona-server/8.4/compile-percona-server.html) that you can compile on the target host.

## Install on Ubuntu 26.04

1. Install the OpenSSL library the server needs to start:

   ```
   sudo apt install libssl3t64
   ```

   Expected output

   ```
   Upgrading:
     libssl3t64  openssl  openssl-provider-legacy

   Summary:
     Upgrading: 3, Installing: 0, Removing: 0, Not Upgrading: 62
     Download size: 4031 kB
     Space needed: 2048 B / 99.6 GB available

   Continue? [Y/n] y
   ```

1. Create the `mysql` group and user. The account has no login shell:

   ```
   sudo groupadd mysql
   sudo useradd -r -g mysql -s /bin/false mysql
   ```

   Expected output

   ```
   No output
   ```

1. Download the tarball and its checksum file:

   ```
   wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-12/binary/tarball/Percona-Server-8.4.11-12-Linux.x86_64.glibc2.35.tar.gz
   wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-12/binary/tarball/Percona-Server-8.4.11-12-Linux.x86_64.glibc2.35.tar.gz.sha256sum
   ```

   Expected output

   ```
   --2026-10-28 05:14:03--  https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-11/binary/tarball/Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz
   Resolving downloads.percona.com (downloads.percona.com)... 15.204.182.114
   Connecting to downloads.percona.com (downloads.percona.com)|15.204.182.114|:443... connected.
   HTTP request sent, awaiting response... 200 OK
   Length: 1463302946 (1.4G) [application/gzip]
   Saving to: ‘Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz’
   ...
   2026-10-28 05:15:21 (74.9 MB/s) - ‘Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz.sha256sum’ saved [121/121]
   ```

1. Verify the tarball:

   ```
   sha256sum -c Percona-Server-8.4.11-12-Linux.x86_64.glibc2.35.tar.gz.sha256sum
   ```

   Expected output

   ```
   Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz: OK
   ```

1. Extract the tarball and create the `/usr/local/mysql` link:

   ```
   sudo tar -xzf Percona-Server-8.4.11-12-Linux.x86_64.glibc2.35.tar.gz -C /usr/local
   sudo ln -s /usr/local/Percona-Server-8.4.11-12-Linux.x86_64.glibc2.35 /usr/local/mysql
   ```

   Expected output

   ```
   No output
   ```

   The files under `/usr/local/mysql` stay owned by `root`.

1. Create the data directory and give it to the `mysql` user:

   ```
   sudo mkdir -p /var/lib/mysql
   sudo chown mysql:mysql /var/lib/mysql
   sudo chmod 750 /var/lib/mysql
   ```

   Expected output

   ```
   No output
   ```

1. Initialize the data directory:

   ```
   sudo -u mysql /usr/local/mysql/bin/mysqld --initialize --datadir=/var/lib/mysql --log-error=/var/lib/mysql/error.log
   ```

   Expected output

   ```
   No output
   ```

1. Read the temporary password for `root@localhost` from the error log:

   ```
   sudo grep 'temporary password' /var/lib/mysql/error.log
   ```

   Expected output

   ```
   2026-10-28T12:38:09.636475Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: <temporary password>
   ```

   Copy the password. You need it for the login step.

1. Open the systemd unit file:

   ```
   sudo nano /etc/systemd/system/mysqld.service
   ```

   Expected output

   ```
   No output
   ```

1. Paste the following configuration into the editor. Press `Ctrl+O`, then `Enter`, to save the file. Press `Ctrl+X` to close `nano`.

   ```
   [Unit]
   Description=Percona Server for MySQL
   After=network.target

   [Service]
   User=mysql
   Group=mysql
   ExecStart=/usr/local/mysql/bin/mysqld --datadir=/var/lib/mysql --socket=/var/run/mysqld/mysqld.sock --log-error=/var/lib/mysql/error.log
   RuntimeDirectory=mysqld
   LimitNOFILE=65535
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

   Expected output

   ```
   No output
   ```

1. Load the new unit file:

   ```
   sudo systemctl daemon-reload
   ```

   Expected output

   ```
   No output
   ```

1. Start the server and enable it at boot:

   ```
   sudo systemctl enable --now mysqld
   ```

   Expected output

   ```
   Created symlink /etc/systemd/system/multi-user.target.wants/mysqld.service → /etc/systemd/system/mysqld.service.
   ```

1. Log in with the temporary password:

   ```
   /usr/local/mysql/bin/mysql -u root -p -S /var/run/mysqld/mysqld.sock
   ```

## Troubleshoot the installation

If `systemctl enable --now mysqld` fails or the login returns `ERROR 2002`, the server is not running. Check:

sudo systemctl status mysqld –no-pager sudo tail -30 /var/lib/mysql/error.log

| Symptom                                       | Cause                                                                          |
| --------------------------------------------- | ------------------------------------------------------------------------------ |
| `status=203/EXEC`                             | `ExecStart` path is wrong, or the `/usr/local/mysql` link is missing           |
| `ERROR 2002 ... mysqld.sock (2)`              | The server is not running, or the client and server use different socket paths |
| `--initialize` fails on a non-empty directory | Remove the data directory contents and run step 7 again                        |

For the next tasks, see [Quickstart - First five minutes (security and stability)](https://docs.percona.com/percona-server/8.4/first-five-minutes.html).
