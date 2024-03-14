# Install {{post}} releases

This document provides guidelines on installing Percona Server packages for MySQL from Percona repositories. For more information, see [{{post}}](https://www.percona.com/navigating-mysql-5-7-end-of-life).

For instructions for binary tarballs, see [Install {{post}} release from a binary tarball](binary-tarball.md#install-a-mysql-57-post-eol-support-release-from-a-binary-tarball).

## Procedure

1. Request access to the {{post}} repository from [Percona Support](https://www.percona.com/services/support/mysql-support) to receive the client ID and the access token needed to download the packages.

2. Configure the repository and install Percona Server for MySQL packages

    === "On Debian and Ubuntu"

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
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-57-eol/apt/ OPERATING_SYSTEM main
            ```

        4. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

        5. Install Percona Server for MySQL packages

            ```{.bash .data-prompt="$"}
            $ sudo apt install -y percona-server-server-5.7
            ```

            Install other required packages.

    === "On RHEL and derivatives"

        1. Create the `/etc/yum.repos.d/post-eol.repo` configuration file with the following contents with your [CLIENTID] and [TOKEN].

            ```ini title="/etc/yum.repos.d/post-eol.repo"
            baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-57-eol/yum/main/$releasever/RPMS/x86_64
            enabled=1
            gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
            ```

        2. Install Percona Server for MySQL packages

            ```{.bash .data-prompt="$"}
            $ sudo yum install -y percona-server-server-5.7
            ```
