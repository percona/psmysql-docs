# Create a database and table

??? Example "Benefits and what to watch out for when creating databases and tables"

    Creating a database and table has the following benefits:

    - Store and organize your data in a structured and consistent way.
    - Query and manipulate your data using SQL.
    - Enforce data integrity and security using constraints, triggers, views, roles, and permissions.
    - Optimize your data access and performance using indexes, partitions, caching, and other techniques.

    When you create a table, design your database schema carefully, changing it later may be difficult and costly. You should experiment with concurrency, transactions, locking, isolation, and other issues that may arise when multiple users access the same data. You must backup and restore your data regularly, as data loss or corruption may occur due to hardware failures, human errors, or malicious attacks.

The following steps create a database and create and populate a table.
{.power-number}

1. To create a database, use the `CREATE DATABASE` statement. You can optionally specify the character set and collation for the database in the statement. After the database is created, select the database using the `USE` statement or the `-D` option in the MySQL client.

     * Create and use a database example.

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

2. Create a table using the `CREATE TABLE` statement. You can specify the values for each column or use the DEFAULT keyword for columns with default values, data types, constraints, indexes, and other options.

     * Create a table example.

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

3. Insert data into the table using the `INSERT INTO` SQL statement. This statement adds multiple records into a table in one statement.

    * INSERT records into the table example.

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

## Next step

[Run SQL queries :material-arrow-right:](quickstart-queries.md){.md-button}
