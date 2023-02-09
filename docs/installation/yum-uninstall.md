# Uninstall Percona Server for MySQL

To completely uninstall Percona Server for MySQL, remove all the installed packages and data files.

1. Stop the Percona Server for MySQL service:

	```{.bash data-prompt="$"}
	$ sudo service mysql stop
	```

2. Remove the packages:

	```{.bash data-prompt="$"}
	$ sudo yum remove percona-server*
	```

3. Remove the data and configuration files:

	!!! warning
	
	    This step removes all the packages and deletes all the data files (databases, tables, logs, etc.). Take a backup before doing this in case you need the data.
	
	```{.bash data-prompt="$"}
	$ rm -rf /var/lib/mysql
	$ rm -f /etc/my.cnf
	```