# Install Percona Server for MySQL Pro on Amazon Linux 2023

--8<--- "pro-build-announcement.md"

This document provides guidelines how to install Pro packages of Percona Server for MySQL from Percona repositories. [Check files in packages built for Percona Server for MySQL Pro :material-arrow-right:](pro-files.md){.md-button}

## Procedure

!!! note 

    Percona Server for MySQL 8.0.41-32 Pro build is available for the following platforms:

    * Amazon Linux 2023 (AL2023) - We support both AMD64 and ARM64 versions of Amazon Linux 2023.

1. Request the access to the pro repository from Percona Support. You will receive the client ID and the access token which you use when downloading the packages.


2. Create the `/etc/yum.repos.d/psmysql-pro.repo` configuration file with the following contents with your [CLIENTID] and [TOKEN].

    ```ini title="/etc/yum.repos.d/psmysql-pro.repo"
    [ps-8.0-pro]
    name=PS_8.0_PRO
    baseurl=http://repo.percona.com/private/[CLIENTID]-[TOKEN]/ps-80-pro/yum/release/$releasever/RPMS/x86_64
    enabled=1
    gpgkey = https://repo.percona.com/yum/PERCONA-PACKAGING-KEY
    ```

3. Install Percona Server for MySQL packages
        
    ```{.bash .data-prompt="$"}
    $ sudo yum install -y percona-server-server-pro
    ```

    Install other required packages. [Check files in packages built for Percona Server for MySQL Pro](pro-files.md).

4. Start the server

    ```{.bash .data-prompt="$"}
    $ sudo systemctl start mysql
    ```

## Next step

[Enable the FIPS mode :material-arrow-right:](fips.md){.md-button}