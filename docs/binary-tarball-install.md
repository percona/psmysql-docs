# Install Percona Server for MySQL {{vers}} from a binary tarball

A binary tarball is one file that contains the server binaries and support files. The `tar` command bundles the files, and `gzip` compresses them.

Use a binary tarball in the following cases:

- You need to run more than one version of Percona Server for MySQL on the same host

- Percona does not provide a package for your Linux distribution

For all other cases, use [APT](apt-repo.md) or [DNF](yum-repo.md) packages.

This page installs the glibc 2.35 tarball on Ubuntu 26.04 (`x86_64`). For other operating systems, select a tarball on the [binary tarball file names](binary-tarball-names.md) page. Package names for other libraries are on the [Operating system libraries](os-libraries.md) page.

Generic binary tarballs are built for `x86_64`. Percona publishes ARM64 (`aarch64`) builds as [APT](apt-repo.md) and [DNF](yum-repo.md) packages, as [Docker](docker.md) images (use the `{{arm_tag}}` tag), and as [source](compile-percona-server.md) that you can compile on the target host.

## Install on Ubuntu 26.04

1. Install the OpenSSL library the server needs to start:

    ```shell
    sudo apt install libssl3t64
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Upgrading:
          libssl3t64  openssl  openssl-provider-legacy

        Summary:
          Upgrading: 3, Installing: 0, Removing: 0, Not Upgrading: 62
          Download size: 4031 kB
          Space needed: 2048 B / 99.6 GB available

        Continue? [Y/n] y
        ```

2. Create the `mysql` group and user. The account has no login shell:

    ```shell
    sudo groupadd mysql
    sudo useradd -r -g mysql -s /bin/false mysql
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

3. Download the tarball and its checksum file:

    ```shell
    wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz
    wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz.sha256sum
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        --2026-10-28 05:14:03--  https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-11/binary/tarball/Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz
        Resolving downloads.percona.com (downloads.percona.com)... 15.204.182.114
        Connecting to downloads.percona.com (downloads.percona.com)|15.204.182.114|:443... connected.
        HTTP request sent, awaiting response... 200 OK
        Length: 1463302946 (1.4G) [application/gzip]
        Saving to: ‘Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz’
        ...
        2026-10-28 05:15:21 (74.9 MB/s) - ‘Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz.sha256sum’ saved [121/121]
        ```

4. Verify the tarball:

    ```shell
    sha256sum -c Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz.sha256sum
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Percona-Server-8.4.11-11-Linux.x86_64.glibc2.35.tar.gz: OK
        ```

5. Extract the tarball and create the `/usr/local/mysql` link:

    ```shell
    sudo tar -xzf Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz -C /usr/local
    sudo ln -s /usr/local/Percona-Server-{{release}}-Linux.x86_64.glibc2.35 /usr/local/mysql
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

    The files under `/usr/local/mysql` stay owned by `root`.

6. Create the data directory and give it to the `mysql` user:

    ```shell
    sudo mkdir -p /var/lib/mysql
    sudo chown mysql:mysql /var/lib/mysql
    sudo chmod 750 /var/lib/mysql
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

7. Initialize the data directory:

    ```shell
    sudo -u mysql /usr/local/mysql/bin/mysqld --initialize --datadir=/var/lib/mysql --log-error=/var/lib/mysql/error.log
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

8. Read the temporary password for `root@localhost` from the error log:

    ```shell
    sudo grep 'temporary password' /var/lib/mysql/error.log
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        2026-10-28T12:38:09.636475Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: <temporary password>
        ```

    Copy the password. You need it for the login step.

9. Open the systemd unit file:

    ```shell
    sudo nano /etc/systemd/system/mysqld.service
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

10. Paste the following configuration into the editor. Press `Ctrl+O`, then `Enter`, to save the file. Press `Ctrl+X` to close `nano`.

    ```ini
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

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

11. Load the new unit file:

    ```shell
    sudo systemctl daemon-reload
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        No output
        ```

12. Start the server and enable it at boot:

    ```shell
    sudo systemctl enable --now mysqld
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Created symlink /etc/systemd/system/multi-user.target.wants/mysqld.service → /etc/systemd/system/mysqld.service.
        ```

13. Log in with the temporary password:

    ```shell
    /usr/local/mysql/bin/mysql -u root -p -S /var/run/mysqld/mysqld.sock
    ```


   ## Troubleshoot the installation

   If `systemctl enable --now mysqld` fails or the login returns `ERROR 2002`, the server is not running. Check:

   sudo systemctl status mysqld --no-pager
   sudo tail -30 /var/lib/mysql/error.log

   | Symptom | Cause |
   |---|---|
   | `status=203/EXEC` | `ExecStart` path is wrong, or the `/usr/local/mysql` link is missing |
   | `ERROR 2002 ... mysqld.sock (2)` | The server is not running, or the client and server use different socket paths |
   | `--initialize` fails on a non-empty directory | Remove the data directory contents and run step 7 again |
   
For the next tasks, see [Quickstart - First five minutes (security and stability)](first-five-minutes.md).
