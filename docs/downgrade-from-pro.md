# Downgrade from Percona Server for MySQL Pro

If you want to downgrade from Percona Server for MySQL Pro to the same version of Percona Server for MySQL, do the following:

!!! note

    For Ubuntu 22.04 the downgrade from percona-mysql-router-pro to percona-mysql-router will be implemented in future releases.

=== "On Debian and Ubuntu"

    1. Set up the Percona Server for MySQL 8.0 repository
    
        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ps80
        ```

    2. Stop the `mysql` server
       
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mysql
        ```

    3. Install the server package

        ```{.bash data-prompt="$"}
        $ sudo apt install percona-server-server
        ```

       Install other required packages. [Check files in the DEB package built for Percona Server for MySQL 8.0](apt-files.md).

    4. Stop the `mysql` server again.
       
        ```{.bash data-prompt="$"}
        $ sudo systemctl stop mysql
        ```

    5. Create an alternative symbolic link for the MySQL configuration file, `my.cnf`, that points to `/etc/mysql/mysql.cnf`

        ```{.bash data-prompt="$"}
        $ sudo update-alternatives --force --install /etc/mysql/my.cnf my.cnf "/etc/mysql/mysql.cnf" 300
        ```

    6. Start the `mysql` server

        ```{.bash data-prompt="$"}
        $ sudo systemctl start mysql
        ```

=== "On RHEL and derivatives"

    1. Set up the Percona Server for MySQL 8.0 repository
    
        ```{.bash data-prompt="$"}
        $ sudo percona-release setup ps80
        ```

    2. Back up the `my.cnf` configuration file 

        ```{.bash data-prompt="$"}
        $ sudo cp /etc/my.cnf /etc/my.cnf_back
        ```

    3. Remove the server Pro package

        ```{.bash data-prompt="$"}
        $ sudo yum remove percona-server-server-pro
        ```

    4. Install the server package

        ```{.bash data-prompt="$"}
        $ sudo yum install percona-server-server
        ```
    
        Install other required packages. [Check files in the RPM package built for Percona Server for MySQL 8.0](yum-files.md).

    5. Overwrite the contents of `/etc/my.cnf` configuration file with the contents from `my.cnf_back` configuration file.

        ```{.bash data-prompt="$"}
        $ sudo cp /etc/my.cnf_back /etc/my.cnf
        ```

    6. Start the `mysql` server

        ```{.bash data-prompt="$"}
        $ sudo systemctl start mysql
        ```

