# Upgrade to Percona Server for MySQL Pro

Are you a Percona Customer already and are you ready to enjoy all the [benefits of Percona Server for MySQL Pro](../psmysql-pro.md)? 

This document provides instructions on how you can upgrade from Percona Server for MySQL Basic to Percona Server for MySQL Pro.

## Preconditions 

Request the access to the pro repository from Percona Support. You will receive the client ID and the access token which you use when downloading the packages.

## Procedure

1. Configure the repository

    === "On Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmysql-pro.list` configuration file with the following contents

            To get the `OPERATING_SYSTEM` value, run `lsb_release -sc`.

            ```ini title="/etc/apt/sources.list.d/psmysql-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/apt/ OPERATING_SYSTEM main
            ```

        2. Update the local cache

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

2. Stop the `mysql` server

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop mysql
    ```

3. Install Percona Server for MySQL PRO packages

    === "On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-server-pro
        ```
    === "On RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install --allowerasing percona-server-server-pro
        ```

4. Start the server
    ```{.bash .data-prompt="$"}
    $ sudo systemct start mysql
    ```