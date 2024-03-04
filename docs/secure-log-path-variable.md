# The secure_log_path variable

## secure_log_path

This variable is implemented in Percona Server for MySQL 8.0.28-19 (2022-05-12).

| Variable Name | Description       |
|---------------|-------------------|
| Command-line  | --secure-log-path |
| Dynamic       | No                |
| Scope         | Global            |
| Data type     | String            |
| Default       | empty string      |

This variable restricts the location of the `slow_query_log`, `general_log`, and `buffered_error_log` files. Also, this variable is applied to the following options:

* `slow_query_log_file` - specifies the name of the slow query log file and the directory where to store this file.

* `general_log_file` - specifies the name of the general log file and the directory where to store this file.

* `buffered_error_log_filename` - specifies the name of the buffered error log file and the directory where to store this file. You can specify the size of the buffer for error logging in bytes with the `buffered-error-log-size` option.

The `secure_log_path` variable is read-only and is set up in a configuration file or the command line.

The value accepts a directory name as a string. The default value is an empty string. An empty string adds a warning to the error log and the log files are located in the default directory, /var/lib/mysql. If the value is a directory name, the log files are located in that directory. An attempt to move the log files from the specified directory results in an error.

## The example of the secure_log_path variable usage

Run the following commands as root:

1. Create the direcory to store the log files.

    ```{.bash data-prompt="[root@localhost ~]#"}
    [root@localhost ~]# mkdir /var/lib/mysqld-logs
    ```

2. Enable the following options and set them up with the created directory in /etc/my.cnf configuration file.

    ```text
    [mysqld]
    secure_log_path=/var/lib/mysqld-logs
    general-log=ON
    general-log-file=/var/lib/mysqld-logs/general_log
    slow-query-log=ON
    slow-query-log-file=/var/lib/mysqld-logs/slow_log
    buffered-error-log-size=1000
    buffered-error-log-filename=/var/lib/mysqld-logs/buffered_log 
    ```

3. Change the owner and group of the `/var/lib/mysqld-logs` directory and all its subdirectories and files to `mysql`.

    ```{.bash data-prompt="[root@localhost ~]#"}
    [root@localhost ~]# chown -R mysql:mysql /var/lib/mysqld-logs
    ```

4. Restart the MySQL server.

    ```{.bash data-prompt="[root@localhost ~]#"}
    [root@localhost ~]# systemctl restart mysql
    ```

5. Check that the slow query log and the general log are enabled for the MySQL server.

    ```{.bash data-prompt="[root@localhost ~]#"}
    [root@localhost ~]# mysql -e "select @@slow_query_log, @@general_log, @@secure_log_path"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +------------------+---------------+-----------------------+
        | @@slow_query_log | @@general_log | @@secure_log_path     |
        +------------------+---------------+-----------------------+
        |                1 |             1 | /var/lib/mysqld-logs/ |
        +------------------+---------------+-----------------------+
        ```

6. Check that the slow query log and the general log are stored in the `/var/lib/mysqld-logs` directory.

    ```{.bash data-prompt="[root@localhost ~]#"}
    [root@localhost ~]# cd /var/lib/mysqld-logs/
    [root@localhost mysqld-logs]# ls -lrth
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        -rw-r-----. 1 mysql mysqld-logs 240 Aug 18 11:56 localhost-slow.log
        -rw-r-----. 1 mysql mysqld-logs 565 Aug 18 11:56 localhost.log
        ```
