# Downgrade from Percona Server for MySQL Pro

If you want to downgrade from Percona Server for MySQL Pro to the same version of Percona Server for MySQL, do the following:

=== "On Debian and Ubuntu"

    1. Set up the Percona Server for MySQL 8.4 repository
    
        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ps84
        ```

    2. Stop the `mysql` server.
       
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mysql
        ```

    3. Install the server package

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-server-server
        ```

        Install other required packages. [Check files in the DEB package built for Percona Server for MySQL 8.4](apt-files.md).

    4. Start the `mysql` server

        ```{.bash data-prompt="$"}
        $ sudo systemctl start mysql
        ```

    !!! note

        On Debian 12, if you want to remove the Percona Server for MySQL after the downgrade, you must stop the 
        server manually. This behavior will be fixed in future releases.
       
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mysql
        ```

=== "On RHEL and derivatives"

    1. Set up the Percona Server for MySQL 8.4 repository
    
        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ps84
        ```
 
    2. Stop the `mysql` server.
       
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mysql
        ```

    3. Install the server package

        ```{.bash data-prompt="$"}
        $ sudo yum --allowerasing install percona-server-server
        ```
    
        Install other required packages. [Check files in the RPM package built for Percona Server for MySQL 8.4](yum-files.md).

    4. Start the `mysql` server

        ```{.bash data-prompt="$"}
        $ sudo systemctl start mysql
        ```
