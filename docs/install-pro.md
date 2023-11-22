# Install Pro packages of Percona Server for MySQL

This document provides guidelines how to install Pro packages of Percona Server for MySQL from Percona repositories. [Learn more about Percona Server for MySQL Pro :material-arrow-top-right:](../psmysql-pro.md).

## Procedure

1. Request the access to the pro repository from Percona Support. You will receive the client ID and the access token which you use when downloading the packages.

2. Configure the repository

    === "On Debian and Ubuntu"

        1. Download the Percona `gpg` key:

            ```{.bash .data-prompt="$"}
            $ wget https://github.com/percona/percona-repositories/raw/main/deb/percona-keyring.gpg 
            ```

        2. Add the Percona `gpg` key to `trusted.gpg.d` directory:

            ```{.bash .data-prompt="$"}
            $ sudo cp percona-keyring.gpg /etc/apt/trusted.gpg.d/
            ```

        3. Create the `/etc/apt/sources.list.d/psmysql-pro.list` configuration file with the following contents

            To get the `OPERATING_SYSTEM` value, run `lsb_release -sc`.
            
            ```ini title="/etc/apt/sources.list.d/psmysql-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/apt/ OPERATING_SYSTEM main
            ```

        4. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === "On RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmysql-pro.repo` configuration file with the following contents

        ```ini title="/etc/yum.repos.d/psmysql-pro.repo"
        [ps-8.0-pro]
        name=PS_8.0_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/yum/main/$releasever/RPMS/x86_64
        enabled=1
        gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
        ```

3. Install Percona Server for MySQL packages

    === "On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-server-pro
        ```

    === "On RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install -y percona-server-server-pro
        ```

4. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemct start mysql
    ```

