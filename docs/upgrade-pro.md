# Upgrade to Percona Server for MySQL Pro

Percona Server for MySQL Pro includes the [capabilities](psmysql-pro.md#capabilities) that are typically requested by large enterprises. Percona Server for MySQL Pro contains packages created and tested by Percona. These packages are supported only for Percona Customers with a subscription.

[Become a Percona Customer](https://www.percona.com/about/contact){.md-button}

Review [Get more help](get-help.md) for ways that we can work with you.

This document provides instructions on upgrading from Percona Server for MySQL to Percona Server for MySQL Pro.

## Preconditions

Request the access to the pro repository from Percona Support. You will receive the client ID and the access token which you use when downloading the packages.

[Check files in packages built for Percona Server for MySQL Pro :material-arrow-right:](pro-files.md){.md-button}

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

3. Install Percona Server for MySQL Pro packages

    === "On Debian and Ubuntu"

        ```{.bash .data-prompt="$"}
        $ sudo apt install -y percona-server-server-pro
        ```

        Install other required packages. [Check files in the DEB package built for Percona Server for MySQL 8.0](apt-files.md).

    === "On RHEL and derivatives"

        The `--allow erasing` option allows Yum to remove existing packages that conflict with the new installation. This is often necessary when         upgrading or reinstalling software.
   
        ```{.bash .data-prompt="$"}
        $ sudo yum install --allowerasing percona-server-server-pro
        ```
        
        Install other required packages. [Check files in the RPM package built for Percona Server for MySQL 8.0](yum-files.md).

5. Start the server
    
    ```{.bash .data-prompt="$"}
    $ sudo systemctl start mysql
    ```

!!! note

    On Debian 12, you may receive the following warning after running `systemctl` commands:
    
    ```text
    Warning: The unit file, source configuration file, or drop-ins of mysql.service changed on disk. Run 'systemctl daemon-reload' to reload units.
    ```
    
    Run the suggested command:

    ```{.bash .data-prompt="$"}
    $ sudo systemctl daemon-reload
    ```

[Downgrade from Percona Server for MySQL Pro :material-arrow-right:](downgrade-from-pro.md){.md-button}
