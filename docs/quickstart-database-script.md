# Work with a database

??? Example "Benefits and what to watch out for when creating databases and tables"

    Creating a database and table provides the following benefits:

    * Store and organize your data in a structured and consistent way.

    * Query and manipulate your data using SQL statements like SELECT, INSERT, UPDATE, and DELETE.

    * Use primary keys to uniquely identify records.

    This quickstart demonstrates basic database operations. As you advance, you can add constraints, triggers, views, indexes, and other features to enforce data integrity, improve security, and optimize performance.

    When you create a table, design your database schema carefully, as changing the schema later may be difficult and costly. You should also backup and restore your data regularly, as data loss or corruption may occur due to hardware failures, human errors, or malicious attacks.

You are welcome to name any items to match your organization's standards or use your table structure and data. If you do, the results are different from the expected results.

To create a database, use the `CREATE DATABASE` statement. After the database is created, select the database using the `USE` statement.

```sql
CREATE DATABASE mydb;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```sql
USE mydb;
```

??? example "Expected output"

    ```{.text .no-copy}
    Database changed
    ```

## Create tables

Create tables using the `CREATE TABLE` statement. You can specify data types, constraints, indexes, and other options for each column.

First, create the `departments` table:

```sql
CREATE TABLE `departments` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(100),
    PRIMARY KEY (`id`)
);
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

Next, create the `employees` table with a foreign key to the departments table:

```sql
CREATE TABLE `employees` (
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(255),
    `department_id` INT,
    `country` VARCHAR(100),
    PRIMARY KEY (`id`),
    FOREIGN KEY (`department_id`) REFERENCES `departments`(`id`)
);
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected, 1 warning (0.03 sec)
    ```

## Insert data into the tables

Insert data into the `departments` table first:

```sql
INSERT INTO `departments` (`name`)
VALUES
    ("Engineering"),
    ("Sales"),
    ("Marketing");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 3 rows affected (0.01 sec)
    Records: 3  Duplicates: 0  Warnings: 0
    ```

Insert data into the `employees` table using the `INSERT INTO` SQL statement. This statement adds multiple records into a table in one statement.

Insert data into the table using the `INSERT INTO` SQL statement. This statement adds multiple records into a table in one statement.


```sql
INSERT INTO `employees` (`name`,`department_id`,`country`)
VALUES
    ("Erasmus Richardson",1,"England"),
    ("Jenna French",2,"Canada"),
    ("Alfred Dejesus",1,"Austria"),
    ("Hamilton Puckett",3,"Canada"),
    ("Michal Brzezinski",1,"Poland"),
    ("Zofia Lis",2,"Poland"),
    ("Aisha Yakubu",3,"Nigeria"),
    ("Miguel Cardenas",1,"Peru"),
    ("Luke Jansen",2,"Netherlands"),
    ("Roger Pettersen",1,"Norway");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 10 rows affected (0.02 sec)
    Records: 10  Duplicates: 0  Warnings: 0
    ```

## View all data

To view all records in a table, use `SELECT *` to retrieve all columns:

```sql
SELECT * FROM employees;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+---------------------+--------------+------------+
    | id | name                | department_id| country    |
    +----+---------------------+--------------+------------+
    |  1 | Erasmus Richardson |            1 | England    |
    |  2 | Jenna French        |            2 | Canada     |
    |  3 | Alfred Dejesus      |            1 | Austria    |
    |  4 | Hamilton Puckett    |            3 | Canada     |
    |  5 | Michal Brzezinski   |            1 | Poland     |
    |  6 | Zofia Lis           |            2 | Poland     |
    |  7 | Aisha Yakubu        |            3 | Nigeria    |
    |  8 | Miguel Cardenas     |            1 | Peru       |
    |  9 | Luke Jansen         |            2 | Netherlands|
    | 10 | Roger Pettersen     |            1 | Norway     |
    +----+---------------------+--------------+------------+
    10 rows in set (0.00 sec)
    ```

## Join tables

JOIN queries combine data from multiple tables based on a related column. Use JOINs to retrieve data from related tables in a single query.

Join the `employees` and `departments` tables to display employee names with their department names:

```sql
SELECT e.id, e.name, d.name AS department, e.country 
FROM employees e 
JOIN departments d ON e.department_id = d.id;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+---------------------+------------+------------+
    | id | name                | department | country    |
    +----+---------------------+------------+------------+
    |  1 | Erasmus Richardson | Engineering| England    |
    |  2 | Jenna French        | Sales      | Canada     |
    |  3 | Alfred Dejesus      | Engineering| Austria    |
    |  4 | Hamilton Puckett    | Marketing  | Canada     |
    |  5 | Michal Brzezinski   | Engineering| Poland     |
    |  6 | Zofia Lis           | Sales      | Poland     |
    |  7 | Aisha Yakubu        | Marketing  | Nigeria    |
    |  8 | Miguel Cardenas     | Engineering| Peru       |
    |  9 | Luke Jansen         | Sales      | Netherlands|
    | 10 | Roger Pettersen     | Engineering| Norway     |
    +----+---------------------+------------+------------+
    10 rows in set (0.00 sec)
    ```

## Run a SELECT query

SELECT queries retrieve data from one or more tables based on specified criteria. They are the most common type of query and can be used for various purposes, such as displaying, filtering, sorting, aggregating, or joining data. SELECT queries do not modify the data in the database but can affect the performance if the query involves large or complex datasets.



```sql
SELECT e.id, e.name, d.name AS department, e.country 
FROM employees e 
JOIN departments d ON e.department_id = d.id 
WHERE e.country = 'Poland';
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+-------------------+------------+---------+
    | id | name              | department | country |
    +----+-------------------+------------+---------+
    |  5 | Michal Brzezinski | Engineering| Poland  |
    |  6 | Zofia Lis         | Sales      | Poland  |
    +----+-------------------+------------+---------+
    2 rows in set (0.00 sec)
    ```

## Run an Update query

UPDATE queries modify existing data in a table. They are used to change or correct the information stored in the database. UPDATE queries can update one or more columns and rows simultaneously, depending on the specified conditions. They may also fail if they violate any constraints or rules defined on the table.

Run an UPDATE query to change a record, and then run a [SELECT](#run-a-select-query) with a WHERE clause to verify the update.

```sql
UPDATE employees SET name = 'Zofia Niemec' WHERE id = 6;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

```sql
SELECT name FROM employees WHERE id = 6;
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

INSERT queries add new data to a table. They are used to populate the database with new information. INSERT queries can insert one or more rows at a time, depending on the syntax. INSERT queries may fail if they violate any constraints or rules defined on the table, such as primary keys, foreign keys, unique indexes, or triggers.

Insert a row into a table and then run a [SELECT](#run-a-select-query) with a WHERE clause to verify the record was inserted.

```sql
INSERT INTO `employees` (`name`,`department_id`,`country`)
VALUES
("Kenzo Sasaki",1,"Japan");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```sql
SELECT e.id, e.name, d.name AS department, e.country 
FROM employees e 
JOIN departments d ON e.department_id = d.id 
WHERE e.id = 11;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+--------------+------------+---------+
    | id | name         | department | country |
    +----+--------------+------------+---------+
    | 11 | Kenzo Sasaki | Engineering| Japan   |
    +----+--------------+------------+---------+
    1 row in set (0.00 sec)
    ```

## Run a Delete query

DELETE queries remove existing data from a table. They are used to clean up the information no longer needed or relevant in the database. The DELETE queries can delete one or more rows at a time, depending on the specified conditions. They may also trigger cascading deletes on related tables if foreign key constraints are enforced.

Delete a row in the table and run a [SELECT](#run-a-select-query) with a WHERE clause to verify the deletion.

```sql
DELETE FROM employees WHERE id >= 11;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```sql
SELECT e.id, e.name, d.name AS department, e.country 
FROM employees e 
JOIN departments d ON e.department_id = d.id 
WHERE e.id > 10;
```

??? example "Expected output"

    ```{.text .no-copy}
    Empty set (0.00 sec)
    ```

## Count records

Use the `COUNT()` function to count the number of records that match a condition:

```sql
SELECT COUNT(*) FROM employees;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------+
    | COUNT(*) |
    +----------+
    |       10 |
    +----------+
    1 row in set (0.00 sec)
    ```

```sql
SELECT d.name AS department, COUNT(*) AS employee_count
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name;
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------+---------------+
    | department | employee_count|
    +------------+---------------+
    | Engineering|             5 |
    | Sales      |             3 |
    | Marketing  |             2 |
    +------------+---------------+
    3 rows in set (0.00 sec)
    ```

## Next step

* [Clean up your installation](quickstart-cleanup.md) (optional)

* [Next steps](quickstart-next-steps.md)

## Additional resources

* [Quickstart - Overview](quickstart-overview.md)

* [Run Percona Server for MySQL with Docker](quickstart-docker.md)

* [Install Percona Server for MySQL on Ubuntu](quickstart-apt.md)

* [Install Percona Server for MySQL on Oracle Linux](quickstart-yum.md)

* [Clean up your installation](quickstart-cleanup.md)

* [Next steps](quickstart-next-steps.md)

