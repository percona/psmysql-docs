# Upgrade to Percona Server for MySQL Pro

--8<--- "pro-build-announcement.md"

This document provides instructions on upgrading from Percona Server for MySQL to Percona Server for MySQL Pro.

## Preconditions

To begin, please contact [Percona Support :octicons-link-external-16:](https://www.percona.com/services/support) to request access to the pro repository. They'll provide you with the client ID and access token needed for downloading packages.

For additional assistance during your upgrade process, our [Percona Support team :octicons-link-external-16:](https://www.percona.com/services/support) is available to help ensure a smooth transition.

[Check files in packages built for Percona Server for MySQL Pro](pro-files.md){.md-button}

## Procedure

1. Configure the repository

    === "On Debian and Ubuntu"

        1. Create the `/etc/apt/sources.list.d/psmysql-pro.list` configuration file with the following contents

            To get the `OPERATING_SYSTEM` value, run `lsb_release -sc`.

            ```ini title="/etc/apt/sources.list.d/psmysql-pro.list"
            deb http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-84-pro/apt/ OPERATING_SYSTEM main
            ```

        2. Update the local cache

            ```{.bash .data-prompt="$"}
            $ sudo apt update
            ```

    === "On RHEL and derivatives"

        Create the `/etc/yum.repos.d/psmysql-pro.repo` configuration file with the following contents

        ```ini title="/etc/yum.repos.d/psmysql-pro.repo"
        [ps-8.4-pro]
        name=PS_8.4_PRO
        baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-84-pro/yum/main/$releasever/RPMS/x86_64
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

        Install other required packages. [Check files in the DEB package built for Percona Server for MySQL 8.4](apt-files.md).

    === "On RHEL and derivatives"

        ```{.bash .data-prompt="$"}
        $ sudo yum install --allowerasing percona-server-server-pro
        ```
        
        Install other required packages. [Check files in the DEB package built for Percona Server for MySQL 8.4](apt-files.md).

4. Start the server
    
    ```{.bash .data-prompt="$"}
    $ sudo systemct start mysql
    ```

!!! note

    On Debian 12, you may receive the following warning after running `systemct` commands:
    
    ```text
    Warning: The unit file, source configuration file or drop-ins of mysql.service changed on disk. Run 'systemctl daemon-reload' to reload units.
    ```
    
    Run the following command to reload units:

    ```{.bash .data-prompt="$"}
    $ sudo systemctl daemon-reload
    ```

[Downgrade from Percona Server for MySQL Pro](downgrade-from-pro.md){.md-button}
