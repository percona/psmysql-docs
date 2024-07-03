# Common SQL commands

SQL commands used by MySQL can be categorized into different types based on their purposes: Data Definition Language (DDL), Data Manipulation Language (DML), Data Control Language (DCL), and Transaction Control Language (TCL).

## Data Manipulation Language (DML)

DML commands manage data within database tables.

Common DML commands include:

* [**SELECT**]: This command retrieves data from one or more tables in the database.

    ```text
    mysql> SELECT * FROM customers;
    ```

* [**INSERT**]: This command adds new records to a table.

    ```text
    mysql> INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com');
    ```

* [**UPDATE**]: This command modifies existing records in a table.

    ```text
    mysql> UPDATE customers SET email = 'newemail@example.com' WHERE id = 1;
    ```

* [**DELETE**]: This command removes records from a table.
 
    ```text
    mysql> DELETE FROM customers WHERE id = 1;
    ```

## Data Definition Language (DDL)

DDL commands define, modify, and remove database objects such as tables, indexes, and views.

Common DDL commands include:

* **CREATE**: This command creates new database objects like tables, indexes, and views.

    ```text
    mysql> CREATE TABLE employees (id INT, name VARCHAR(50));
    ```

* **ALTER**: This command modifies the structure of existing database objects.

    ```text
    mysql> ALTER TABLE employees ADD COLUMN email VARCHAR(100);
    ```

* **DROP**: This command removes database objects from the database.

    ```text
    mysql> DROP TABLE employees;
    ```

## Data Control Language (DCL)

DCL commands control access to database objects and define privileges.

Common DCL commands include:

* **GRANT**: This command grants specific privileges to database users.

    ```text
    mysql> GRANT SELECT, INSERT ON employees TO 'user1'@'localhost';
    ```

* **REVOKE**: This command revokes privileges from database users.

    ```text
    mysql> REVOKE INSERT ON employees FROM 'user2'@'localhost';
    ```

## Transaction Control Language (TCL)

TCL commands manage transactions within a database.

Common TCL commands include:

* **COMMIT**: This command saves changes made during the current transaction to the database.

    ```text
    mysql> COMMIT;
    ```

* **ROLLBACK**: This command undoes changes made during the current transaction and restores the database to its previous state.

    ```text
    mysql> ROLLBACK;
    ```

    [**SELECT**]: select.md
    [**INSERT**]: insert.md
    [**UPDATE**]: update.md
    [**DELETE**]: delete.md

Fundamental SQL links:

* [SQL Basics](sql-basics.md)
* [SELECT](select.md)
* [INSERT](insert.md)
* [DELETE](delete.md)
* [UPDATE](update.md)
* [SQL Operators](sql-operators.md)