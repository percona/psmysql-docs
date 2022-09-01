# Post-Installation steps for Percona Server for MySQL 5.7


After you have installed *Percona Server for MySQL* 5.7, you may need to do the following:

| Task                                                                                      | Description                                                                                                                                               |
|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Initialize the data directory](#initializing-the-data-directory)                         | The source distribution or generic binary distribution installation does not automatically initialize the data directory                                  |
| [Update the root password](#updating-the-root-password)                                   | The CentOS/RedHat installations set up a temporary root password.                                                                                         |
| [Securing the Installation](#securing-the-installation)                                   | The [mysql_secure_installation](https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html) script improves the security of the installation. |                                                                                                                          |
| [Checking the server status](#checking-the-server-status)                                 | Verify the server returns information                                                                                                                     |
| [Configuring the Server to Start at Startup](#configuring-the-server-to-start-at-startup) | Common method to start the server automatically                                                                                                           |
| [Testing the server](#testing-the-server)                                                 | Verify the server installation                                                                                                                            |
| [Populating the time zone tables](#populating-the-time-zone-tables)                       | The time zone tables are created but are not populated.                                                                                                   |
| [Exclude Buffer Pool Pages from core files](#excluding-buffer-pool-pages-from-core-files) | Reduce the size of the core files by excluding the buffer pool                                                                                            |

## Initializing the Data Directory

If you install the server using either the source distribution or generic binary distribution files, the data directory is not initialized, and you must run the initialization process after installation.

Run mysqld with the [–initialize](https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_initialize) option or the [initialize-insecure](https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_initialize-insecure) option.

Executing mysqld with either option does the following:


* Verifies the existence of the data directory


* Initializes the system tablespace and related structures


* Creates system tables including grant tables, time zone tables, and server-side help tables


* Creates `root@localhost`

You should run the following steps with the `mysql` login.


1. Navigate to the MySQL directory. The example uses the default location.

    ```shell
    $ cd /usr/local/mysql
    ```


1. Create a directory for the MySQL files. The [secure_file_priv](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_secure_file_priv) uses the directory path as a value.

    ```shell
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

    ```shell
    $ bin/mysqld --initialize
    ```
## Updating the `root` password

The RedHat and derivative distributions set up a temporary password 
when MySQL is installed.
To 
reset the password, you must start MySQL with the `--skip-grant-tables` 
option and update the `user` table.

The initial password is located using the following command:

```shell
$ grep 'temporary password' /var/log/mysqld.log
```
Follow this procedure to reset the root password:

1. Stop MySQL.

    ```shell
    $ sudo systemctl stop mysqld
    ```
    
2. Set `--skip-grant-tables` as an environment option. This method lets 
   you specify the option without modifying configuration files.

    ```shell
    $ sudo systemctl set-environment MYSQLD_OPTS="--skip-grant-tables 
    --skip-networking"
    ```
    
3. Restart MySQL to make the option change effective.

    ```shell
    $ sudo systemctl restart mysqld
    ```
    
4. Access MySQL as `root`.

    ```shell
    $ mysql -u root
    ```
    
5. Change the root password.

    ```sql
    mysql> FLUSH PRIVILEGES;
    mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY ('NewPassword');
    mysql> FLUSH PRIVILEGES;
    mysql> exit
    ```
    
6. Stop MySQL

    ```shell
    $ sudo systemctl stop mysqld
    ```
    
7. Reset the environment options.

    ```shell
    $ sudo systemctl unset-environment MYSQLD_OPTS
    ```

8. Start MySQL

    ```shell
    $ sudo systemctl start mysqld
    ```
    
9. Log in to MySQL using the root password.

    ```shell
    $ mysql -u root -p
    ```

!!! note

    if you have trouble logging in after following the steps, repeat the procedure but, instead of using the `ALTER USER` statement, modify the `user` table.

    ```sql
    mysql> UPDATE mysql.user SET authentication_string=PASSWORD
    ('NewPassword'), password_expired='N' 
    WHERE User='root' AND Host='localhost';
    mysql>FLUSH PRIVILEGES;
    ```

## Securing the Installation

The [mysql_secure_installation](https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html)
script improves the security of the installation.

Running the script does the following:


* Changes the `root` password


* Disallows remote login for `root` accounts


* Removes anonymous users


* Removes the `test` database


* Reloads the privilege tables

The following statement runs the script:

```shell
$ mysql_secure_installation
```

## Checking the server status

After a generic binary installation, the server starts. The following command checks the server status:

```shell
$ sudo service mysql status
```

Access the server with the following command:

```shell
$ mysql -u root -p
```

## Configuring the Server to Start at Startup

You can manage the server with systemd. If you have installed the server from a generic binary distribution on an operating system that uses systemd, you can manually configure systemd support.

The following commands start, check the status, and stop the server:

```shell
$ sudo systemctl start mysql
$ sudo systemctl status mysql
$ sudo systemctl stop mysql
```

Enabling the server to start at startup, run the following:

```shell
$ sudo systemctl enable mysql
```

## Testing the Server

After you have initialized the data directory, and the server is started, you can run tests on the server.

This section assumes you have used the default installation settings. If you have modified the installation, navigate to the installation location. You can also add the location by [Setting the Environment Variables](https://dev.mysql.com/doc/refman/5.7/en/setting-environment-variables.html).

You can use the [mysqladmin](https://dev.mysql.com/doc/refman/5.7/en/mysqladmin.html) client to access the server.

If you have issues connecting to the server, you should use the `root` user and the root account password.

```shell
$ sudo mysqladmin -u root -p version
```
The output should be similar to the following:
```text
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

Use [mysqlshow](https://dev.mysql.com/doc/refman/5.7/en/mysqlshow.html) to display database and table information.

```shell
$ sudo mysqlshow -u root -p
```
The output should be similar to the following:

```text
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

## Populating the time zone tables

The time zone system tables are the following:


* `time_zone`


* `time_zone_leap_second`


* `time_zone_name`


* `time_zone_transition`


* `time_zone_transition_type`

If you install the server using either the source distribution or generic binary distribution files, the installation creates the time zone tables, but the tables are not populated.

The [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/5.7/en/mysql-tzinfo-to-sql.html) program
populates the tables from the `zoneinfo` directory data available in Linux.

A common method to populate the tables is to add the zoneinfo directory path to `mysql_tzinfo_to_sql` and then send the output into `mysql`.

The example assumes you are running the command with the `root` account. You must use an account with the privileges able to modify MySQL system tables.

```shell
$ mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p rootpassword
```

## Excluding Buffer Pool Pages from Core files

Implemented in *Percona Server for MySQL* 5.7.33-36, you can use the [innodb_buffer_pool_in__core_file](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_buffer_pool_in_core_file) to reduce the size of the core file.

Buffer pools can produce large core files because the buffer pool is located in main memory. If the main memory is dumped to a core file, the buffer pool increases the size of the dump.

Having a large core file can have the following issues:


* Requires more time to write


* Consume disk space


* Reading the file

To exclude the buffer pool, run the following command at startup or use a `SET` statement:

```sql
mysqld> SET GLOBAL innodb_buffer_pool_in__core_file=OFF;
```
