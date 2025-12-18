---
title: Restrict dynamic log file locations
description: The `secure_log_path` system variable plays a crucial role in enhancing
  the security and organization of log files within a MySQL database environment by
  restricting where dynamic log files can be sto.
slug: restrict-dynamic-log-locations
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Restrict dynamic log file locations

The `secure_log_path` system variable plays a crucial role in enhancing the security and organization of log files within a MySQL database environment by restricting where dynamic log files can be stored.

In a MySQL environment, restricting dynamic log locations offers several benefits:

| Benefit              | Details                                                                                                      |
|----------------------|--------------------------------------------------------------------------------------------------------------|
| Enhanced security    | It prevents unauthorized modification of log files, protecting sensitive information and audit trails.       |
| Improved compliance  | It helps meet regulatory requirements for data security and auditability.                                    |
| Simplified administration | It centralizes log files, making them easier to manage and monitor.                                      |
| Increased reliability | It reduces the risk of accidental log file deletion or corruption. |

The disadvantages could be:

* Reduced flexibility: Cannot change the log file locations easily

* Increased complexity: Adds an extra layer of configuration and management

* Performance impact: Writing to log files on slower storage media may increase overhead and potentially affect the overall performance of the MySQL server.

The benefits of restricting dynamic log locations in MySQL outweigh the disadvantages, especially in security-conscious environments.

## secure_log_path

| Variable Name | Description       |
|---------------|-------------------|
| Command-line  | --secure-log-path |
| Dynamic       | No                |
| Scope         | Global            |
| Data type     | String            |
| Default       | empty string      |

The `secure_log_path` variable controls where specific log files are stored. This variable expects a directory name as a string value. By default, the value is an empty string, allowing older applications to continue functioning without requiring a secure log path.

This variable affects the following options:

| Option                        | Description                                           |
|-------------------------------|-------------------------------------------------------|
| `slow_query_log=ON`            | Enables the storage of the slow query log file.         |
| `slow_query_log_file`          | Sets the name and location of the slow query log file. |
|                                |                                                        |
| `general_log=ON`               | Enables the storage of the general log file.            |
| `general_log_file`             | Sets the name and location of the general log file.   |
|                                |                                                        |
| `buffered_error_log_filename`  | Sets the name and location of the buffered error log file. |
| `buffered-error-log-size`      | Specifies the size of the buffer for error logging in bytes.   |

The `secure_log_path` variable is read-only and must be set up in a configuration file or the command line.

| Value         | Description                                                                                                                                                                                                                       |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Empty string  | The variable only adds a warning to the error log and does nothing. The log files are located in the default directory, `/var/lib/mysql`.     |
| Directory name| If the value contains a directory name, then the slow query log and the general log must be located in that directory. An attempt to move either of these files outside of the specified directory results in an error.           |

By establishing a controlled logging environment through the `secure_log_path` variable, MySQL administrators can significantly enhance both the security and manageability of their logs, reducing risks associated with unauthorized access and data integrity.

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