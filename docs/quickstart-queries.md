# Run SQL queries

The following steps run a SELECT query, an UPDATE query, an INSERT INTO query, and a DELETE query on a table in the database. These are a series of structured query language (SQL) statements that manipulate the data in a database.
{.power-number}

1. SELECT queries retrieve data from one or more tables based on specified criteria. They are the most common query type and can be used for various purposes, such as displaying, filtering, sorting, aggregating, or joining data. SELECT queries do not modify the data in the database but can affect the performance if the query involves large or complex datasets.

    * An example of a SELECT query.
  
        ```{.bash data-prompt="mysql>"}
        mysql> SELECT id, firstname, lastname from members;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +----+-----------+------------+
            | id | firstname | lastname   |
            +----+-----------+------------+
            |  1 | Jenna     | French     |
            |  2 | Hamilton  | Puckett    |
            |  3 | Michal    | Brzezinski |
            |  4 | Zofia     | Lis        |
            |  5 | Grant     | Zika       |
            +----+-----------+------------+
            5 rows in set (0.01 sec)
            ```

        ```{.bash data-prompt="mysql>"}
        mysql> SELECT id, country from country;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +------+---------+
            | id   | country |
            +------+---------+
            | 7001 | Nigeria |
            | 7002 | Poland  |
            | 7003 | Canada  |
            +------+---------+
            3 rows in set (0.00 sec)
            ```

        ```{.bash data-prompt="mysql>"}
        mysql> SELECT members_id, country_id from members_country;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +------------+------------+
            | members_id | country_id |
            +------------+------------+
            |          1 |       7003 |
            |          2 |       7003 |
            |          3 |       7002 |
            |          4 |       7002 |
            |          5 |       7001 |
            +------------+------------+
            5 rows in set (0.00 sec)
            ```

        ```{.bash data-prompt="mysql>"}
        mysql> SELECT m.firstname, m.lastname, c.country FROM members m INNER JOIN members_country mc ON m.id = mc.members_id INNER JOIN country c ON c.id = mc.country_id;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +-----------+------------+---------+
            | firstname | lastname   | country |
            +-----------+------------+---------+
            | Jenna     | French     | Canada  |
            | Hamilton  | Puckett    | Canada  |
            | Michal    | Brzezinski | Poland  |
            | Zofia     | Lis        | Poland  |
            | Grant     | Zika       | Nigeria |
            +-----------+------------+---------+
            5 rows in set (0.00 sec)
            ```

2. UPDATE queries modify existing data in a table. They are used to change or correct the information stored in the database. UPDATE queries can update one or more columns and rows simultaneously, depending on the specified conditions. They may also fail if they violate any constraints or rules defined on the table.

    * An example of an UPDATE query and then run a [SELECT](#select-query) with a WHERE clause to verify the update.

        ```{.bash data-prompt="mysql>"}
        mysql> UPDATE members SET lastname = 'Niemec' WHERE id = 4;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Query OK, 1 row affected (0.01 sec)
            Rows matched: 1  Changed: 1  Warnings: 0
            ```

        ```{.bash data-prompt="mysql>"}
        mysql> SELECT firstname, lastname FROM members WHERE id = 4;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            +-----------+----------+
            | firstname | lastname |
            +-----------+----------+
            | Zofia     | Niemec   |
            +-----------+----------+
            1 row in set (0.00 sec)
            ```

3. INSERT queries add new data to a table. They are used to populate the database with new information. INSERT queries can insert one or more rows at a time, depending on the syntax. The query may fail if it violates any constraints or rules defined on the table, such as primary keys, foreign keys, unique indexes, or triggers.

    * Insert a row into a table. A [SELECT](#select-query) query with a WHERE clause verifies that the record was inserted.

        ```{.bash data-prompt="mysql>"}
        mysql> BEGIN;
                    INSERT INTO members (firstname, lastname) VALUES ('Kenzo','Sasaki');
                    SELECT firstname, lastname FROM members WHERE id = (SELECT MAX(id) FROM members);
                    INSERT INTO country (id, country) VALUES (7004, 'Japan');
                    SELECT country FROM country WHERE id = (SELECT MAX(id) FROM country);
                    INSERT INTO members_country (members_id, country_id) VALUES (6, 7004);
                    SELECT m.firstname, m.lastname, c.country FROM members m INNER JOIN members_country mc ON m.id = mc.members_id INNER JOIN country c ON c.id = mc.country_id WHERE m.id = (SELECT MAX(id) FROM members);
                COMMIT;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            BEGIN;
            Query OK, 0 rows affected (0.00 sec)

            mysql>                     INSERT INTO members (firstname, lastname) VALUES ('Kenzo','Sasaki');
            Query OK, 1 row affected (0.01 sec)

            mysql>                     SELECT firstname, lastname FROM members WHERE id = 6;
            +-----------+----------+
            | firstname | lastname |
            +-----------+----------+
            | Kenzo     | Sasaki   |
            +-----------+----------+
            1 row in set (0.00 sec)

            mysql>                     INSERT INTO country (id, country) VALUES (7004, 'Japan');
            Query OK, 1 row affected (0.00 sec)

            mysql>                     SELECT country FROM country WHERE id = 7004;
            +---------+
            | country |
            +---------+
            | Japan   |
            +---------+
            1 row in set (0.00 sec)

            mysql>                     INSERT INTO members_country (members_id, country_id) VALUES (6, 7004);
            Query OK, 1 row affected (0.00 sec)

            mysql>                     SELECT m.firstname, m.lastname, c.country FROM members m INNER JOIN members_country mc ON m.id = mc.members_id INNER JOIN country c ON c.id = mc.country_id WHERE m.id = 6;
            +-----------+----------+---------+
            | firstname | lastname | country |
            +-----------+----------+---------+
            | Kenzo     | Sasaki   | Japan   |
            +-----------+----------+---------+
            1 row in set (0.00 sec)

            mysql>                 COMMIT;
            Query OK, 0 rows affected (0.00 sec)
            
            ```

4. DELETE queries remove existing data from a table. They are used to clean up the information that is no longer needed or relevant in the database. The DELETE queries can delete one or more rows simultaneously, depending on the specified conditions. They may also trigger cascading deletes on related tables if foreign key constraints are enforced.

    * Delete a row in the table and run a [SELECT](#select-query) with a WHERE clause to verify the deletion.

        ```{.bash data-prompt="mysql>"}
        mysql> BEGIN;
                    DELETE FROM members order by id desc limit 1;
                    DELETE FROM country order by id desc limit 1;
                    DELETE FROM members_country order by members_id desc limit 1;
               COMMIT;
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Query OK, 1 row affected (0.01 sec)
            Query OK, 1 row affected (0.01 sec)
            Query OK, 1 row affected (0.01 sec)
            ```

        ```{.bash data-prompt="mysql>"}
        mysql> SELECT m.firstname, m.lastname, c.country FROM members m INNER JOIN members_country mc ON m.id = mc.members_id INNER JOIN country c ON c.id = mc.country_id WHERE country = 'Japan';
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Empty set (0.00 sec)
            ```

## Next step

[Clean up :material-arrow-right:](quickstart-exit.md){.md-button}
