# Uninstall Percona Server for MySQL 8.0 using the APT package manager

To uninstall Percona Server for MySQL, you must remove all the installed
packages. Removing packages with `apt remove` does not remove the
configuration and data files. Removing the packages with `apt purge` does remove the packages with configuration files and data files (all the databases). Depending on your needs, you can choose which command best suits you.

1. To uninstall Percona Server for MySQL, you must stop the Percona Server for MySQL service:

    ```{.bash data-prompt="$"} 
    $ sudo systemctl stop mysql
    ```

2. Remove the Percona Server for MySQL packages. You can use either command.

    a. The command, `apt remove` removes only the packages. This operation does not remove the data files (databases, tables, logs, configuration, and other files). 
        ```{.bash data-prompt="$"}
        $ sudo apt remove percona-server\
        ```

        If you do not need these remaining files, remove them manually.

    b. This command removes all the packages and any associated configuration files. This action ensures the complete removal of the packages from the system. 
    
        ```{.bash data-prompt="$"}
        $ sudo apt purge percona-server\`
        ```

3. To ensure associated packages are removed, run the following command:

    ```{.bash data-prompt="$"}
    $ sudo apt autoremove
    ```

4. You can manually remove the data directory by executing the following command. Back up any of the necessary data before deleting the files.

    ```{.bash data-prompt="$"}
    $ sudo rm -rf /var/lib/mysql/
    ```

