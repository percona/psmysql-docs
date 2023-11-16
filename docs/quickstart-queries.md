# Run SQL queries

The following steps run a SELECT query, an UPDATE query, an INSERT INTO query, and a DELETE query on a table in the database. These are a series of structured query language (SQL) statements that manipulate the data in a database.
{.power-number}

1. SELECT queries retrieve data from one or more tables based on specified criteria. They are the most common type of query and can be used for various purposes, such as displaying, filtering, sorting, aggregating, or joining data. SELECT queries do not modify the data in the database but can affect the performance if the query involves large or complex datasets.

    * An example of a SELECT query.
  
        ```{.bash data-prompt="mysql>"}
        mysql>SELECT id, name, email, country FROM employees WHERE country = 'Poland';
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +----+-------------------+---------------------+---------+
            | id | name              | email               | country |
            +----+-------------------+---------------------+---------+
            |  5 | Michal Brzezinski | magnus@iclound.pl   | Poland  |
            |  6 | Zofia Lis         | zofial00@hotmail.pl | Poland  |
            +----+-------------------+---------------------+---------+
            2 rows in set (0.01 sec)
            ```

2. UPDATE queries modify existing data in a table. They are used to change or correct the information stored in the database. UPDATE queries can update one or more columns and rows simultaneously, depending on the specified conditions. They may also fail if they violate any constraints or rules defined on the table.

    * An example of an UPDATE query and then run a [SELECT](#select-query) with a WHERE clause to verify the update.

        ```{.bash data-prompt="mysql>"}
        mysql> UPDATE employees SET name = 'Zofia Niemec' WHERE id = 6;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Query OK, 1 row affected (0.01 sec)
            Rows matched: 1  Changed: 1  Warnings: 0
            ```

        ```{.bash data-prompt="mysql>"}
        mysql> SELECT id, name, email, country FROM employees WHERE country = 'Poland';
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +----+-------------------+---------------------+---------+
            | id | name              | email               | country |
            +----+-------------------+---------------------+---------+
            |  5 | Michal Brzezinski | magnus@iclound.pl   | Poland  |
            |  6 | Zofia Niemec      | zofial00@hotmail.pl | Poland  |
            +----+-------------------+---------------------+---------+
            2 rows in set (0.00 sec)
            ```

3. INSERT queries add new data to a table. They are used to populate the database with new information. INSERT queries can insert one or more rows at a time, depending on the syntax. The query may fail if it violates any constraints or rules defined on the table, such as primary keys, foreign keys, unique indexes, or triggers.

    * Insert a row into a table and then run a [SELECT](#select-query) with a WHERE clause to verify the record was inserted.

        ```{.bash data-prompt="mysql>"}
        INSERT INTO `employees` (`name`,`email`,`country`)
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

4. DELETE queries remove existing data from a table. They are used to clean up the information no longer needed or relevant in the database. The DELETE queries can delete one or more rows at a time, depending on the specified conditions. They may also trigger cascading deletes on related tables if foreign key constraints are enforced.

    * Delete a row in the table and run a [SELECT](#select-query) with a WHERE clause to verify the deletion.

        ```{.bash data-prompt="mysql>"}
        mysql> DELETE FROM employees WHERE id >= 11;
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
            Empty set (0.00 sec)
            ```

## Next step

[Clean up :material-arrow-right:](quickstart-exit.md){.md-button}