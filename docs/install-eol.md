# Install {{eol}} packages

Version {{release}} contains fixes as part of [{{post}}], a paid service for subscribers.

Community members can [build this release from the source](compile-percona-server.md) from publicly available source code, which is released quarterly.

For instructions for binary tarballs, see [Download a {{eol}} binary tarball](tarball-eol.md).

## Procedure

1. Request access to the {{post}} repository from [Percona Support](https://www.percona.com/services/support/mysql-support) to receive the client ID and the access token needed to download the packages.

2. Configure the repository and install Percona Server for MySQL packages

    === "Using apt (Debian, Ubuntu)"

        1. Download the Percona `gpg` key:

            ```{.bash .data-prompt="$"}
            $ wget https://github.com/percona/percona-repositories/raw/main/deb/percona-keyring.gpg
            ```

        2. Add the Percona `gpg` key to `trusted.gpg.d` directory:

            ```{.bash .data-prompt="$"}
            $ sudo cp percona-keyring.gpg /etc/apt/trusted.gpg.d/
            ```

        3. Create the `/etc/apt/sources.list.d/post-eol.list` configuration file with the following contents with your [CLIENTID] and [TOKEN].

            To get the `OPERATING_SYSTEM` value, run `lsb_release -sc`.

            ```ini title="/etc/apt/sources.list.d/post-eol.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-eol/apt/ OPERATING_SYSTEM main
            ```

        4. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

        5. Install Percona Server for MySQL packages

            ```{.bash .data-prompt="$"}
            $ sudo apt install -y percona-server-server
            ```

            Install other required packages.

    === "Using yum (RHEL and other yum-based derivatives)"

        1. Create the `/etc/yum.repos.d/post-eol.repo` configuration file with the following contents with your [CLIENTID] and [TOKEN].

            ```ini title="/etc/yum.repos.d/post-eol.repo"
            baseurl=http://repo.percona.com/private/[Clientid]-[Token]/ps-80-eol/yum/release/$releasever/RPMS/x86_64
            enabled=1
            gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
            ```

        2. Install Percona Server for MySQL packages

            ```{.bash .data-prompt="$"}
            $ sudo yum install -y percona-server-server
            ```

[{{post}}]: https://www.percona.com/mysql-8-0-eol-support/
