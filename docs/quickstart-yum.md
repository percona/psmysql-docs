# Install with YUM

Use the [Percona repositories] to install using YUM.

## Prerequisits

* Either use `sudo` or run as root

* Stable Internet access

## Installation steps

The examles of the "expected output" depend on the operating system. The following examples are based on Oracle Linux 9.3.
{.power-number}

1. Use the YUM package manager to install `percona-release`.

    ```{.bash data-prompt="$"}
    $ sudo yum install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Oracle Linux 9 BaseOS Latest (x86_64)                                                        7.0 MB/s |  20 MB     00:02
        Oracle Linux 9 Application Stream Packages (x86_64)                                          7.3 MB/s |  28 MB     00:03
        Oracle Linux 9 UEK Release 7 (x86_64)                                                        6.7 MB/s |  27 MB     00:04
        Last metadata expiration check: 0:00:04 ago on Fri 16 Feb 2024 12:34:26 PM UTC.
        percona-release-latest.noarch.rpm                                                             37 kB/s |  20 kB     00:00
        Dependencies resolved.
        ...
        * Enabling the Percona Original repository
        <*> All done!
        * Enabling the Percona Release repository
        <*> All done!
        The percona-release package now contains a percona-release script that can enable additional repositories for our newer products.

        For example, to enable the Percona Server 8.0 repository use:

            percona-release setup ps80

        Note: To avoid conflicts with older product versions, the percona-release setup command may disable our original repository for some products.

        For more information, please visit:
            https://www.percona.com/doc/percona-repo-config/percona-release.html


            Verifying        : percona-release-1.0-27.noarch                                                                       1/1

        Installed:
            percona-release-1.0-27.noarch

        Complete!
        ```

2. Use the `percona-release` tool to setup the repository for Percona Server for MySQL 8.0.

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup ps-80
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        * Disabling all Percona Repositories
        On Red Hat 8 systems it is needed to disable the following DNF module(s): mysql  to install Percona-Server
        Do you want to disable it? [y/N] y
        Disabling dnf module...
        Percona Release release/noarch YUM repository                                             2.7 kB/s | 1.8 kB     00:00
        Unable to resolve argument mysql
        Error: Problems in request:
        missing groups or modules: mysql
        DNF mysql module was disabled
        * Enabling the Percona Server 8.0 repository
        * Enabling the Percona Tools repository
        <*> All done!
        ```

3. Enable the `ps-80 release` repository.

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable ps-80 release
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        * Enabling the Percona Server 8.0 repository
        <*> All done!
        ```

4. Install the latest version of Percona Server for MySQL 8.0. This installation may take some time.

    ```{.bash data-prompt="$"}
    $ sudo yum install -y percona-server-server
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Percona Server 8.0 release/x86_64 YUM repository                                             1.0 MB/s | 2.3 MB     00:02
        Percona Tools release/x86_64 YUM repository                                                  761 kB/s | 1.1 MB     00:01
        Last metadata expiration check: 0:00:01 ago on Fri 16 Feb 2024 03:07:45 PM UTC.
        Dependencies resolved.
        …
        perl-vars-1.05-480.el9.noarch

        Complete!
        ```

5. Check the status of the mysql service and restart if needed.

    ```{.bash data-prompt="$"}
    $ sudo systemctl status mysql
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        ○ mysqld.service - MySQL Server
            Loaded: loaded (/usr/lib/systemd/system/mysqld.service; enabled; preset: disabled)
            Active: inactive (dead)
            Docs: man:mysqld(8)
                    http://dev.mysql.com/doc/refman/en/using-systemd.html
        ```

    ```{.bash data-prompt="$"}
    $ sudo systemctl restart mysql
    ```

    This command has no output.

6. Percona Server for MySQL generates a temporary password during installation. You must have the service running to access the log.

    ```{.bash data-prompt="$"}
    $ sudo grep 'temporary password' /var/log/mysqld.log
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        2024-02-12T16:05:03.969449Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: [random-generated-password]
        ```

7. Log in to the server. Use the password retrieved by the `grep` command. You can type the password or copy-and-paste. You do not see the characters in the password as you type.

    ```{.bash data-prompt="$"}
    $ mysql -uroot -p
    Enter password:
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Welcome to the MySQL monitor.  Commands end with ; or \g.
        Your MySQL connection id is 8
        Server version: 8.0.35-27 Percona Server (GPL), Release '27', Revision '2f8eeab2'$

        Copyright (c) 2009-2023 Percona LLC and/or its affiliates
        Copyright (c) 2000, 2023, Oracle and/or its affiliates.

        Oracle is a registered trademark of Oracle Corporation and/or its
        affiliates. Other names may be trademarks of their respective
        owners.

        Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

        mysql>
        ```

8. The temporary password must be replaced. Run the ALTER USER command tochange the password for the root user. Remember or save the new password.You will need it to log into the server in the next step.

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY '[your password]';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.01 sec)
        ```

9. Log out of the server. to verify that the password has changed.

    ```{.bash data-prompt="mysql>"}
    mysql> exit
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Bye
        ```

10. Log into the server with the new password to verify that the password has changed.


    ```{.bash data-prompt="$"}
    $ mysql -uroot -p
    Enter password:
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Welcome to the MySQL monitor.  Commands end with ; or \g.
        Your MySQL connection id is 8
        Server version: 8.0.35-27 Percona Server (GPL), Release '27', Revision '2f8eeab2'$

        Copyright (c) 2009-2023 Percona LLC and/or its affiliates
        Copyright (c) 2000, 2023, Oracle and/or its affiliates.

        Oracle is a registered trademark of Oracle Corporation and/or its
        affiliates. Other names may be trademarks of their respective
        owners.

        Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

        mysql>
        ```

## Create a database

??? Example "Benefits and what to watch out for when creating databases and tables"

    Creating a database and table has the following benefits:

    - Store and organize your data in a structured and consistent way.
    - Query and manipulate your data using SQL.
    - Enforce data integrity and security using constraints, triggers, views, roles, and permissions.
    - Optimize your data access and performance using indexes, partitions, caching, and other techniques.

    When you create a table, design your database schema carefully, changing it later may be difficult and costly. You should experiment with concurrency, transactions, locking, isolation, and other issues that may arise when multiple users access the same data. You must backup and restore your data regularly, as data loss or corruption may occur due to hardware failures, human errors, or malicious attacks.

To create a database, use the `CREATE DATABASE` statement. You can optionally specify the character set and collation for the database in the statement. After the database is created, select the database using the `USE` statement or the `-D` option in the MySQL client.

```{.bash data-prompt="mysql>"}
mysql> CREATE DATABASE mydb;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> use mydb;
```

??? example "Expected output"

    ```{.text .no-copy}
    Database changed
    ```

## Create a table

Create a table using the `CREATE TABLE` statement. You can specify the values for each column or use the DEFAULT keyword for columns with default values, data types, constraints, indexes, and other options.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE `employees` (
    `id` mediumint(8) unsigned NOT NULL auto_increment,
    `name` varchar(255) default NULL,
    `email` varchar(255) default NULL,
    `country` varchar(100) default NULL,
    PRIMARY KEY (`id`)
) AUTO_INCREMENT=1;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected, 1 warning (0.03 sec)
    ```

## Insert data into the table

Insert data into the table using the `INSERT INTO` SQL statement. This statement adds multiple records into a table in one statement.


```{.bash data-prompt="mysql>"}
mysql> INSERT INTO `employees` (`name`,`email`,`country`)
VALUES
    ("Erasmus Richardson","posuere.cubilia.curae@outlook.net","England"),
    ("Jenna French","rhoncus.donec@hotmail.couk","Canada"),
    ("Alfred Dejesus","interdum@aol.org","Austria"),
    ("Hamilton Puckett","dapibus.quam@outlook.com","Canada"),
    ("Michal Brzezinski","magna@icloud.pl","Poland"),
    ("Zofia Lis","zofial00@hotmail.pl","Poland"),
    ("Aisha Yakubu","ayakubu80@outlook.com","Nigeria"),
    ("Miguel Cardenas","euismod@yahoo.com","Peru"),
    ("Luke Jansen","nibh@hotmail.edu","Netherlands"),
    ("Roger Pettersen","nunc@protonmail.no","Norway");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 10 rows affected (0.02 sec)
    Records: 10  Duplicates: 0  Warnings: 0
    ```

## Run a SELECT query

SELECT queries retrieve data from one or more tables based on specified criteria. They are the most common type of query and can be used for various purposes, such as displaying, filtering, sorting, aggregating, or joining data. SELECT queries do not modify the data in the database but can affect the performance if the query involves large or complex datasets.



```{.bash data-prompt="mysql>"}
mysql>SELECT id, name, email, country FROM employees WHERE country = 'Poland';
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+-------------------+---------------------+---------+
    | id | name              | email               | country |
    +----+-------------------+---------------------+---------+
    |  5 | Michal Brzezinski | magna@icloud.pl     | Poland  |
    |  6 | Zofia Lis         | zofial00@hotmail.pl | Poland  |
    +----+-------------------+---------------------+---------+
    2 rows in set (0.00 sec)
    ```

## Run an Update query

UPDATE queries modify existing data in a table. They are used to change or correct the information stored in the database. UPDATE queries can update one or more columns and rows simultaneously, depending on the specified conditions. They may also fail if they violate any constraints or rules defined on the table.

    An example of an UPDATE query and then run a [SELECT](#select-query) with a WHERE clause to verify the update.

```{.bash data-prompt="mysql>"}
mysql> UPDATE employees SET name = 'Zofia Niemec' WHERE id = 6;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT name FROM employees WHERE id = 6;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------+
    | name         |
    +--------------+
    | Zofia Niemec |
    +--------------+
    1 row in set (0.00 sec)
    ```

## Run an INSERT query

INSERT queries add new data to a table. They are used to populate the database with new information. INSERT queries can insert one or more rows at a time, depending on the syntax. The query may fail if it violates any constraints or rules defined on the table, such as primary keys, foreign keys, unique indexes, or triggers.

Insert a row into a table and then run a [SELECT](#select-query) with a WHERE clause to verify the record was inserted.

```{.bash data-prompt="mysql>"}
mysql> INSERT INTO `employees` (`name`,`email`,`country`)
VALUES
("Kenzo Sasaki","KenSasaki@outlook.com","Japan");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT id, name, email, country FROM employees WHERE id = 11;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+--------------+-----------------------+---------+
    | id | name         | email                 | country |
    +----+--------------+-----------------------+---------+
    | 11 | Kenzo Sasaki | KenSasaki@outlook.com | Japan   |
    +----+--------------+-----------------------+---------+
    1 row in set (0.00 sec)
    ```

## Run a Delete query

DELETE queries remove existing data from a table. They are used to clean up the information no longer needed or relevant in the database. The DELETE queries can delete one or more rows at a time, depending on the specified conditions. They may also trigger cascading deletes on related tables if foreign key constraints are enforced.

Delete a row in the table and run a [SELECT](#select-query) with a WHERE clause to verify the deletion.

```{.bash data-prompt="mysql>"}
mysql> DELETE FROM employees WHERE id >= 11;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT id, name, email, country FROM employees WHERE id > 10;
```

??? example "Expected output"

    ```{.text .no-copy}
    Empty set (0.00 sec)
    ```






## Troubleshooting:

Installation:

* Verify repository is enabled: `sudo yum repolist`

* Check for package conflicts: `sudo yum deplist percona-server-server`

* Consult package logs: `sudo journalctl -u yum`

MySQL startup:

* Review system logs: `sudo journalctl -u mysqld`

* Check configuration files: /etc/my.cnf

## Security Steps:

* Keep software updated: `sudo yum update` regularly.

* Strong root password: Set a complex, unique password using [`mysql_secure_installation`](#secure-the-installation).

* Disable unused accounts and databases: Remove unnecessary elements.

* Monitor Server Activity: Employ tools, like [Percona Monitoring and Management], and logs to monitor server activity for suspicious behavior.

* Backup data regularly: Ensure robust backups for disaster recovery.

## Secure the installation

You can increase the security of MySQL by running`sudo mysql_secure installation`.

After installing MySQL, you should run the `mysql_secure_installation` script to improve the security of your database server. This script helps you perform several important tasks, such as:

- Set a password for the root user

- Select a level for the  password validation policy

- Remove anonymous users

- Disable root login remotely

- Remove the test database

- Reload the privilege table to ensure all changes take effect immediately

By running this script, you can prevent unauthorized access to your server and protect your data from potential threats.

```{.bash data-prompt="$"}
$ sudo mysql_secure_installation
```

??? example "Expected output"

    ```{.text .no-copy}
    Securing the MySQL server deployment.

    Enter password for user root:

    VALIDATE PASSWORD COMPONENT can be used to test passwords
    and improve security. It checks the strength of password
    and allows the users to set only those passwords which are
    secure enough. Would you like to setup VALIDATE PASSWORD component?

    Press y|Y for Yes, any other key for No:

    There are three levels of password validation policy:

    LOW    Length >= 8
    MEDIUM Length >= 8, numeric, mixed case, and special characters
    STRONG Length >= 8, numeric, mixed case, special characters and dictionary                  file

    Please enter 0 = LOW, 1 = MEDIUM and 2 = STRONG: 1
    Using existing password for root.

    Estimated strength of the password: 0
    Change the password for root ? ((Press y|Y for Yes, any other key for No) :

    New password:

    Re-enter new password:

    Estimated strength of the password: 100
    Do you wish to continue with the password provided?(Press y|Y for Yes, any other key for No) :
    By default, a MySQL installation has an anonymous user,
    allowing anyone to log into MySQL without having to have
    a user account created for them. This is intended only for
    testing, and to make the installation go a bit smoother.
    You should remove them before moving into a production
    environment.

    Remove anonymous users? (Press y|Y for Yes, any other key for No) :
    Success.


    Normally, root should only be allowed to connect from
    'localhost'. This ensures that someone cannot guess at
    the root password from the network.

    Disallow root login remotely? (Press y|Y for Yes, any other key for No) :
    Success.

    By default, MySQL comes with a database named 'test' that
    anyone can access. This is also intended only for testing,
    and should be removed before moving into a production
    environment.


    Remove test database and access to it? (Press y|Y for Yes, any other key for No) :
     - Dropping test database...
    Success.

     - Removing privileges on test database...
    Success.

    Reloading the privilege tables will ensure that all changes
    made so far will take effect immediately.

    Reload privilege tables now? (Press y|Y for Yes, any other key for No) :
    Success.

    All done!
    ```



## Next step

[Choose your next steps:material-arrow-right:](quickstart-next-steps.md){.md-button}



[Percona Monitoring and Management]: https://docs.percona.com/percona-monitoring-and-management
[Percona repositories]: percona-release.md
