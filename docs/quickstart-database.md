# Create a database and tables

??? Information "Benefits and what to watch out for when creating databases and tables"

    Creating a database and table has the following benefits:

    - Store and organize your data in a structured and consistent way.
    - Query and manipulate your data using SQL.
    - Enforce data integrity and security using constraints, triggers, views, roles, and permissions.
    - Optimize your data access and performance using indexes, partitions, caching, and other techniques.

    When you create a table, design your database schema carefully; changing it later may be difficult and costly. Experiment with concurrency, transactions, locking, isolation, and other issues that may arise when multiple users access the same data. You must backup and restore your data regularly, as data loss or corruption may occur due to hardware failures, human errors, or malicious attacks.

The following steps create a database and create and populate a table.
{.power-number}

1. To create a database, use the `CREATE DATABASE` statement. Optionally specify the character set and collation for the database in the statement. After the database is created, select the database using the `USE` statement or the `-D` option in the MySQL client.

     * Create and use a database example.

        ```{.bash data-prompt="mysql>"}
        mysql> CREATE DATABASE mydb;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Query OK, 1 row affected (0.01 sec)
            ```


2. Create a table using the `CREATE TABLE` statement. You can specify the values for each column or use the DEFAULT keyword for columns with default values, data types, constraints, indexes, and other options.

    ```{.bash data-prompt="mysql>"}
    mysql> USE mydb;
    --
    -- table structure for table `members`
    --
    DROP TABLE IF EXISTS `members`;

    CREATE TABLE `members` (
        `id` int NOT NULL auto_increment,
        `firstname` varchar(255) DEFAULT NULL,
        `lastname` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`)
    ) AUTO_INCREMENT=1;

    --
    -- table structure for table `country`
    --

    DROP TABLE IF EXISTS `country`;

    CREATE TABLE `country` (
        id int NOT NULL,
        country varchar(255) DEFAULT NULL,
        PRIMARY KEY (id)
    );

    --
    -- table structure for table `members_country`
    --

    DROP TABLE IF EXISTS `members_country`;

    CREATE TABLE `members_country` (
        members_id int NOT NULL,
        country_id int NOT NULL,
        PRIMARY KEY (members_id, country_id)
    );

    --
    -- list the tables in the database
    --
    SHOW TABLES;

    --
    -- Get the structure of the tables
    --

    DESCRIBE members;
    DESCRIBE country;
    DESCRIBE members_country;

    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        mysql> USE mydb;
        Database changed
        mysql>         --
            ->         -- table structure for table `members`
            ->         --
            ->         DROP TABLE IF EXISTS `members`;
        Query OK, 0 rows affected (0.02 sec)

        mysql>
        mysql>         CREATE TABLE `members` (
            ->           `id` int NOT NULL auto_increment,
            ->           `firstname` varchar(255) DEFAULT NULL,
            ->           `lastname` varchar(255) DEFAULT NULL,
            ->           PRIMARY KEY (`id`)
            ->         ) AUTO_INCREMENT=1;
        Query OK, 0 rows affected (0.01 sec)

        mysql>
        mysql>         --
            ->         -- table structure for table `country`
            ->         --
            ->
            ->         DROP TABLE IF EXISTS `country`;
        Query OK, 0 rows affected (0.00 sec)

        mysql>
        mysql>         CREATE TABLE `country` (
            ->             id int NOT NULL,
            ->             country varchar(255) DEFAULT NULL,
            ->             PRIMARY KEY (id)
            ->         );
        Query OK, 0 rows affected (0.01 sec)

        mysql>
        mysql>         --
            ->         -- table structure for table `members_country`
            ->         --
            ->
            ->         DROP TABLE IF EXISTS `members_country`;
        Query OK, 0 rows affected (0.00 sec)

        mysql>
        mysql>         CREATE TABLE `members_country` (
            ->             members_id int NOT NULL,
            ->             country_id int NOT NULL,
            ->             PRIMARY KEY (members_id, country_id)
            ->         );
        Query OK, 0 rows affected (0.01 sec)

        mysql>
        mysql>         --
            ->         -- list the tables in the database
            ->         --
            ->         SHOW TABLES;
        +-----------------+
        | Tables_in_mydb  |
        +-----------------+
        | country         |
        | members         |
        | members_country |
        +-----------------+
        3 rows in set (0.00 sec)

        mysql>
        mysql>         --
            ->         -- Get the structure of the tables
            ->         --
            ->
            ->         DESCRIBE members;
        +-----------+--------------+------+-----+---------+----------------+
        | Field     | Type         | Null | Key | Default | Extra          |
        +-----------+--------------+------+-----+---------+----------------+
        | id        | int          | NO   | PRI | NULL    | auto_increment |
        | firstname | varchar(255) | YES  |     | NULL    |                |
        | lastname  | varchar(255) | YES  |     | NULL    |                |
        +-----------+--------------+------+-----+---------+----------------+
        3 rows in set (0.00 sec)

        mysql>         DESCRIBE country;
        +---------+--------------+------+-----+---------+-------+
        | Field   | Type         | Null | Key | Default | Extra |
        +---------+--------------+------+-----+---------+-------+
        | id      | int          | NO   | PRI | NULL    |       |
        | country | varchar(255) | YES  |     | NULL    |       |
        +---------+--------------+------+-----+---------+-------+
        2 rows in set (0.00 sec)

        mysql>         DESCRIBE members_country;
        +------------+------+------+-----+---------+-------+
        | Field      | Type | Null | Key | Default | Extra |
        +------------+------+------+-----+---------+-------+
        | members_id | int  | NO   | PRI | NULL    |       |
        | country_id | int  | NO   | PRI | NULL    |       |
        +------------+------+------+-----+---------+-------+
        2 rows in set (0.01 sec)
        ```

3. Insert data into the table using the `INSERT INTO` SQL statement. This statement adds multiple records into a table in one statement.

    * INSERT records into the table example.

        ```{.bash data-prompt="mysql>"}
        mysql> BEGIN;
        
                    LOCK TABLES country WRITE;
                    INSERT INTO country VALUES (7001, 'Nigeria'),(7002, 'Poland'),( 7003,'Canada');
                    UNLOCK TABLES;
                    
                    LOCK TABLES members WRITE;
                    INSERT INTO members (firstname, lastname)
                    VALUES ('Jenna', 'French'),
                    ('Hamilton', 'Puckett'),
                    ('Michal', 'Brzezinski'),
                    ('Zofia', 'Lis'),
                    ('Grant', 'Zika');
                    UNLOCK TABLES;

                    LOCK TABLES members_country WRITE;
                    INSERT INTO members_country (members_id, country_id)
                    VALUES (1, 7003), (2, 7003), (3, 7002), (4, 7002), (5, 7001);
                    UNLOCK TABLES;

        COMMIT;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            LOCK TABLES country WRITE;
            Query OK, 0 rows affected (0.00 sec)

            mysql>         INSERT INTO country VALUES (7001, 'Nigeria'),(7002, 'Poland'),( 7003,'Canada');
            Query OK, 3 rows affected (0.01 sec)
            Records: 3  Duplicates: 0  Warnings: 0

            mysql>         UNLOCK TABLES;
            Query OK, 0 rows affected (0.00 sec)

            mysql>
                ->         LOCK TABLES members WRITE;
            Query OK, 0 rows affected (0.00 sec)

            mysql>         INSERT INTO members (firstname, lastname)
                ->         VALUES ('Jenna', 'French'),
                ->           ('Hamilton', 'Puckett'),
                ->           ('Michal', 'Brzezinski'),
                ->           ('Zofia', 'Lis'),
                ->           ('Grant', 'Zika');
                        Query OK, 5 rows affected (0.01 sec)
                        Records: 5  Duplicates: 0  Warnings: 0

                        mysql>         UNLOCK TABLES;
                        Query OK, 0 rows affected (0.00 sec)

            mysql>
            mysql>         LOCK TABLES members_country WRITE;
            Query OK, 0 rows affected (0.00 sec)

            mysql>         INSERT INTO members_country (members_id, country_id)
                ->         VALUES (1, 7003), (2, 7003), (3, 7002), (4, 7002), (5, 7001);
            Query OK, 5 rows affected (0.00 sec)
            Records: 5  Duplicates: 0  Warnings: 0

            mysql>         UNLOCK TABLES;
            Query OK, 0 rows affected (0.00 sec)
            ```

## Next step

[Run SQL queries :material-arrow-right:](quickstart-queries.md){.md-button}
