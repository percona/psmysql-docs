# Uninstall Percona Server for MySQL

To completely uninstall Percona Server for MySQL, remove all the installed packages and data files.

1. Stop the Percona Server for MySQL service:

	```{.bash data-prompt="$"}
	$ sudo systemctl stop mysql
	```

2. As a superuser, either `root` or using `sudo`, use `yum` and the `remove` option. You can use the `remove` option to remove a specific package or a group of packages. In the example, the command removes all packages starting with `percona-server`. 

	```{.bash data-prompt="$"}
	$ sudo yum remove percona-server*
	```

3. The first command removes the `/var/lib/mysql` directory and everything within it. The second command removes the `/etc/my.cnf` file, the main configuration file for Percona Server for MySQL.

	!!! warning
	
	    This step removes all the packages and deletes all the data files (databases, tables, logs, and other files). Take a backup before doing this in case you need the data.
	
	```{.bash data-prompt="$"}
	$ rm -rf /var/lib/mysql
	$ rm -f /etc/my.cnf
	```