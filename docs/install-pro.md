# Install Percona Server for MySQL Pro

--8<--- "pro-build-announcement.md"

Review [Get more help](get-help.md) for ways that we can work with you.

This document provides guidelines how to install Pro packages of Percona Server for MySQL from Percona repositories. [Check files in packages built for Percona Server for MySQL Pro :material-arrow-right:](pro-files.md){.md-button}

[Install Percona Server for MySQL Pro on Amazon Linux 2023 :material-arrow-right:](install-pro-amzn.md){.md-button}

## Procedure

1. Request access to the pro repository from Percona Support. You will receive the client ID and the access token, which you use when downloading the packages.

2. Configure the repository and install Percona Server for MySQL packages

    === "On Debian or Ubuntu"

        1. Download the Percona `gpg` key:

            ```{.bash .data-prompt="$"}
            $ wget https://github.com/percona/percona-repositories/raw/main/deb/percona-keyring.gpg 
            ```

        2. Add the Percona `gpg` key to `trusted.gpg.d` directory:

            ```{.bash .data-prompt="$"}
            $ sudo cp percona-keyring.gpg /etc/apt/trusted.gpg.d/
            ```

        3. Create the `/etc/apt/sources.list.d/psmysql-pro.list` configuration file with the following contents, and your [CLIENTID] and [TOKEN].

            To find the `OPERATING_SYSTEM` value, run `lsb_release -sc`.
            
            ```ini title="/etc/apt/sources.list.d/psmysql-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/apt/ OPERATING_SYSTEM main
            ```

        4. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```
        
        5. Install Percona Server for MySQL packages
        
            ```{.bash .data-prompt="$"}
            $ sudo apt install -y percona-server-server-pro
            ```

            If needed, install other required packages. [Review the DEB packages built for Percona Server for MySQL 8.0](apt-files.md).

    === "On RHEL, Amazon Linux 2023, or derivatives"

        1. Create the `/etc/yum.repos.d/psmysql-pro.repo` configuration file with the following contents, and your [CLIENTID] and [TOKEN].

            ```ini title="/etc/yum.repos.d/psmysql-pro.repo"
            [ps-8.0-pro]
            name=PS_8.0_PRO
            baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/yum/release/$releasever/RPMS/x86_64
            enabled=1
            gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
            ```

        2. Install Percona Server for MySQL packages
        
            ```{.bash .data-prompt="$"}
            $ sudo dnf install percona-server-server-pro
            ```

            Install other required packages. [Check files in the RPM package built for Percona Server for MySQL 8.0](yum-files.md).

3. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemctl start mysqld
    ```

## Next step

[Enable FIPS mode :material-arrow-right:](fips.md){.md-button}
