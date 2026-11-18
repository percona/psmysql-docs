> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Post-installation

Depending on the type of installation, you may need to do the following tasks:

## Installed using binary files or compiling from source

| Task                                                                  |
| --------------------------------------------------------------------- |
| [Initialize the data dictionary](#initialize-the-data-directory)      |
| [Test the server](#test-the-server)                                   |
| [Set service to start at boot time](#set-service-to-run-at-boot-time) |

### Initialize the data directory

The [binary tarball install](https://docs.percona.com/percona-server/8.4/binary-tarball-install.html) creates `/var/lib/mysql`, initializes it, and reads the temporary `root` password from the error log:

```
sudo grep 'temporary password' /var/lib/mysql/error.log
```

Expected output

```
2026-10-28T12:38:09.636475Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: <temporary password>
```

Copy the password.

### Test the server

After you have initialized the data directory and started the server, you can run tests on the server.

Use the [mysqladmin](https://dev.mysql.com/doc/refman/8.4/en/mysqladmin.html) client from the tarball. Enter the temporary `root` password when prompted.

```
/usr/local/mysql/bin/mysqladmin -u root -p -S /var/run/mysqld/mysqld.sock version
```

Expected output

```
Enter password:
mysql Ver 8.4.11-12 for debian-linux-gnu on x86_64 (Percona Server (GPL), Release '10', Revision 'f446c04')
...
Server version      8.4.11-12
Protocol version    10
Connection          Localhost via UNIX socket
UNIX socket         /var/run/mysqld/mysqld.sock
Uptime:             4 hours 58 min 10 section

Threads:    2 Questions:    16 Slow queries: 0 Opens: 139 Flush tables: 3
Open tables: 59  Queries per second avg: 0.0000
```

Use [mysqlshow](https://dev.mysql.com/doc/refman/8.4/en/mysqlshow.html) to display database and table information.

```
/usr/local/mysql/bin/mysqlshow -u root -p -S /var/run/mysqld/mysqld.sock
```

Expected output

```
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

The [binary tarball install](https://docs.percona.com/percona-server/8.4/binary-tarball-install.html#install-on-ubuntu-2604) creates `/etc/systemd/system/mysqld.service` and starts the server.

The following commands start, check the status, and stop the server:

```
sudo systemctl start mysqld
sudo systemctl status mysqld
sudo systemctl stop mysqld
```

Run the following command to start the service at boot time:

```
sudo systemctl enable mysqld
```

Run the following command to prevent a service from starting at boot time:

```
sudo systemctl disable mysqld
```

## All installations

| Task                                                            |
| --------------------------------------------------------------- |
| [Update the root password](#update-the-root-password)           |
| [Secure the server](#secure-the-server)                         |
| [Populate the time zone tables](#populate-the-time-zone-tables) |

### Update the root password

During an installation on Debian/Ubuntu, you are prompted to enter a root password. On Red Hat Enterprise Linux and derivatives, you update the root password after installation.

Restart the server with the `--skip-grant-tables` option to allow access without a password. This option is insecure. This option also disables remote connections.

```
sudo systemctl stop mysql
sudo systemctl set-environment MYSQLD_OPTS="--skip-grant-tables"
sudo systemctl start mysql
mysql
```

Reload the grant tables to be able to run the `ALTER USER` statement. Enter a password that satisfies the current policy.

```
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'rootPassword_12';
exit
```

If the command fails, with `ERROR 1524 (HY000): Plugin [plugin name] is not loaded.`, then check if the plugin is available.

```
SELECT PLUGIN_NAME, PLUGIN_STATUS
       FROM INFORMATION_SCHEMA.PLUGINS
       WHERE PLUGIN_NAME LIKE 'validate%';
```

If the result is empty or shows `DISABLED`, the plugin is not available. Switch the MySQL user to use the default authentication plugin, `caching_sha2_password` or `mysql_native_password` for your installation.

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'rootPassword_12';
```

If, when adding the password, MySQL returns `ERROR 1819 (HY000) Your password does not satisfy the current policy`, run the following command to see policy requirement.

```
SHOW VARIABLES LIKE 'validate_password%';
```

Redo your password to satisfy the requirements.

Stop the server, remove the `--skip-grant-tables` option, start the server, and log into the server with the updated password.

```
sudo systemctl stop mysql
sudo systemctl unset-environment MYSQLD_OPTS 
sudo systemctl start mysql
mysql -u root -p
```

### Secure the server

The [mysql_secure_installation](https://dev.mysql.com/doc/refman/8.4/en/mysql-secure-installation.html) script improves the security of the instance.

The script does the following:

- Changes the `root` password
- Disallows remote login for `root` accounts
- Removes anonymous users
- Removes the `test` database
- Reloads the privilege tables

The following statement runs the script:

```
mysql_secure_installation
```

## Populate the time zone tables

The time zone system tables are the following:

- `time_zone`
- `time_zone_leap_second`
- `time_zone_name`
- `time_zone_transition`
- `time_zone_transition_type`

If you install the server using either the source distribution or the generic binary distribution files, the installation creates the time zone tables, but the tables are not populated.

The [mysql_tzinfo_to_sql](https://dev.mysql.com/doc/refman/8.4/en/mysql-tzinfo-to-sql.html) program populates the tables from the `zoneinfo` directory data available in Linux.

A common method to populate the tables is to add the zoneinfo directory path to `mysql_tzinfo_to_sql` and then send the output into the [mysql system schema](https://dev.mysql.com/doc/refman/8.4/en/system-schema.html) .

The example assumes you are running the command with the `root` account. The account must have the privileges for modifying the `mysql` system schema.

```
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p -D mysql
```
