> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Uninstall Percona Server for MySQL

To completely uninstall Percona Server for MySQL, remove all the installed packages and data files.

1. Stop the Percona Server for MySQL service:

   ```shell
   sudo service mysql stop
   ```

1. Remove the packages:

   ```shell
   sudo yum remove percona-server*
   ```

1. Remove the data and configuration files:

   Warning

   This step removes all the packages and deletes all the data files (databases, tables, logs, etc.). Take a backup before this operation in case you need the data.

   ```shell
   rm -rf /var/lib/mysql
   rm -f /etc/my.cnf
   ```
