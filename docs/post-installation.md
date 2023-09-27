# Post-installation

Depending on the type of installation, you may need to do the following tasks:

## Installed using binary files or compiling from source

| Task |
|---|
| [Initialize the data dictionary](#initialize-the-data-directory) |
| [Test the server](#test-the-server) |
| [Set service to start at boot time](#set-service-to-run-at-boot-time)|

### Initialize the data directory

If you install the server using either the source distribution or generic binary distribution files, the data directory is not initialized, and you must run the initialization process after installation.

Run mysqld with the [–initialize](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_initialize) option or the [initialize-insecure](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_initialize-insecure) option.

Executing `mysqld` with either option does the following:


* Verifies the existence of the data directory


* Initializes the system tablespace and related structures


* Creates system tables including grant tables, time zone tables, and server-side help tables


* Creates `root@localhost`

You should run the following steps with the `mysql` login.


1. Navigate to the MySQL directory. The example uses the default location.
	
	```{.bash data-prompt="$"}
	$ cd /usr/local/mysql
	```


1. Create a directory for the MySQL files. The [secure_file_priv](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_secure_file_priv) uses the directory path as a value.
	
	```{.bash data-prompt="$"}
	$ mkdir mydata
	```

	The `mysql` user account should have the `drwxr-x---` permissions.
	Four sections define the permissions; file or directory, User, Group, and Others.
	
	The first character designates if the permissions are for a file or directory. The first character is `d` for a directory.
	
	The rest of the sections are specified in three-character sets.
	
	| Permission | User | Group | Other |
	|------------|------|-------|-------|
	| Read       | Yes  | Yes   | No    |
	| Write      | Yes  | No    | No    |
	| Execute    | Yes  | Yes   | No    |
	

1. Run the command to initialize the data directory.

	```{.bash data-prompt="$"}
	$ bin/mysqld --initialize
	```

### Test the server

After you have initialized the data directory, and the server is started, you can run tests on the server.

This section assumes you have used the default installation settings. If you have modified the installation, navigate to the installation location. You can also add the location by [Setting the Environment Variables](https://dev.mysql.com/doc/refman/8.0/en/setting-environment-variables.html).

You can use the [mysqladmin](https://dev.mysql.com/doc/refman/8.0/en/mysqladmin.html) client to access the server.

If you have issues connecting to the server, use the `root` user and the root account password.

```{.bash data-prompt="$"}
$ sudo mysqladmin -u root -p version
```

??? example "Expected output"

    ```{.text .no-copy}
    Enter password:
    mysql Ver 8.0.19-10 for debian-linux-gnu on x86_64 (Percona Server (GPL), Release '10', Revision 'f446c04')
    ...
    Server version      8.0.19-10
    Protocol version    10
    Connection          Localhost via UNIX socket
    UNIX socket         /var/run/mysqld/mysqld.sock
    Uptime:             4 hours 58 min 10 section

    Threads:    2 Questions:    16 Slow queries: 0 Opens: 139 Flush tables: 3
    Open tables: 59  Queries per second avg: 0.0000
    ```

Use [mysqlshow](https://dev.mysql.com/doc/refman/8.0/en/mysqlshow.html) to display database and table information.

```{.bash data-prompt="$"}
$ sudo mysqlshow -u root -p
```

??? example "Expected output"

    ```{.text .no-copy}
    Enter password:

    +---------------------+
    |      Databases      |
    +=====================+
    | information_schema  |
    +---------------------+
    | mysql               |
    +---------------------+
    | performance_schema  |
    +---------------------+
    | sys                 |
    +---------------------+
    ```

### Set service to run at boot time

After a generic binary installation, manually configure systemd support.

The following commands start, check the status, and stop the server:

```{.bash data-prompt="$"}
$ sudo systemctl start mysqld
$ sudo systemctl status mysqld
$ sudo systemctl stop mysqld
```

Run the following command to start the service at boot time:

```{.bash data-prompt="$"}
$ sudo systemctl enable mysqld
```
Run the following command to prevent a service from starting at boot time:


```{.bash data-prompt="$"}
$ sudo systemctl disable mysqld
```

## All installations

| Task |
|---|
| [Update the root password](#update-root-password) |
| [Secure the server](#secure-the-server) |
| [Populate the time zone tables](#populate-the-time-zone-tables)


### Update the root password

During an installation on Debian/Ubuntu, you are prompted to enter a root password. On Red Hat Enterprise Linux and derivatives, you update the root password after installation.

Restart the server with the `--skip-grant-tables` option to allow access without a password. This option is insecure. This option also disables remote connections.

```{.bash data-prompt="$"}
$ sudo systemctl stop mysqld
$ sudo systemctl set-environment MYSQLD_OPTS="--skip-grant-tables"
$ sudo systemctl start mysqld 
$ mysql
```

Reload the grant tables to be able to run the `ALTER USER` statement. Enter a password that satisfies the current policy.

```{.sql data-prompt="mysql>"}
mysql> FLUSH PRIVILEGES;
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootPassword_12';
mysql> exit
```
If, when adding the password, MySQL returns `ERROR 1819 (HY000) Your password does not satisfy the current policy`, run the following command to see policy requirement.

```{.sql data-prompt="mysql>"}
mysql> SHOW VARIABLES LIKE 'validate_password%';
```
Redo your password to satisfy the requirements.

Stop the server, remove the `--skip-grant-tables` option, start the server, and log into the server with the updated password.

```{.bash data-prompt="$"}
$ sudo systemctl stop mysqld 
$ sudo systemctl unset-environment MYSQLD_OPTS 
$ sudo systemctl start mysqld 
$ mysql -u root -p
```

### Secure the server

The [mysql_secure_installation](https://dev.mysql.com/doc/refman/8.0/en/mysql-secure-installation.html)
script improves the security of the instance.

The script does the following:

* Changes the `root` password


* Disallows remote login for `root` accounts


* Removes anonymous users


* Removes the `test` database


* Reloads the privilege tables

The following statement runs the script:

```{.bash data-prompt="$"}
$ mysql_secure_installation
```



## Populate the time zone tables

The time zone system tables are the following:


* `time_zone`


* `time_zone_leap_second`


* `time_zone_name`


* `time_zone_transition`


* `time_zone_transition_type`

If you install the server using either the source distribution or the
generic binary distribution files, the installation creates the time zone
tables, but the tables are not populated.

The [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html) program
populates the tables from the `zoneinfo` directory data available in Linux.

A common method to populate the tables is to add the zoneinfo directory path
to `mysql_tzinfo_to_sql` and then send the output into
the [mysql system schema](https://dev.mysql.com/doc/refman/8.0/en/system-schema.html).

The example assumes you are running the command with the `root` account.
The account must have the privileges for modifying the `mysql`
system schema.

```{.bash data-prompt="$"}
$ mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p -D mysql
```
