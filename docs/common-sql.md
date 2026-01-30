# Common SQL commands

SQL commands used by MySQL can be categorized into different types based on their purposes: Data Definition Language (DDL), Data Manipulation Language (DML), Data Control Language (DCL), and Transaction Control Language (TCL).

## Data Manipulation Language (DML)

DML commands manage data within database tables.

Common DML commands include:

* [**SELECT**]: This command retrieves data from one or more tables in the database.

    ```sql
    SELECT * FROM customers;
    ```

* [**INSERT**]: This command adds new records to a table.

    ```sql
    INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com');
    ```

* [**UPDATE**]: This command modifies existing records in a table.

    ```sql
    UPDATE customers SET email = 'newemail@example.com' WHERE id = 1;
    ```

* [**DELETE**]: This command removes records from a table.
 
    ```sql
    DELETE FROM customers WHERE id = 1;
    ```

## Data Definition Language (DDL)

DDL commands define, modify, and remove database objects such as tables, indexes, and views.

Common DDL commands include:

* **CREATE**: This command creates new database objects like tables, indexes, and views.

    ```sql
    CREATE TABLE employees (id INT, name VARCHAR(50));
    ```

* **ALTER**: This command modifies the structure of existing database objects.

    ```sql
    ALTER TABLE employees ADD COLUMN email VARCHAR(100);
    ```

* **DROP**: This command removes database objects from the database.

    ```sql
    DROP TABLE employees;
    ```

## Data Control Language (DCL)

DCL commands control access to database objects and define privileges.

Common DCL commands include:

* **GRANT**: This command grants specific privileges to database users.

    ```sql
    GRANT SELECT, INSERT ON employees TO 'user1'@'localhost';
    ```

* **REVOKE**: This command revokes privileges from database users.

    ```sql
    REVOKE INSERT ON employees FROM 'user2'@'localhost';
    ```

## Transaction Control Language (TCL)

TCL commands manage transactions within a database.

Common TCL commands include:

* **COMMIT**: This command saves changes made during the current transaction to the database.

    ```sql
    COMMIT;
    ```

* **ROLLBACK**: This command undoes changes made during the current transaction and restores the database to its previous state.

    ```sql
    ROLLBACK;
    ```
    
Fundamental SQL links:

* [SQL Basics](sql-basics.md)
* [SELECT](select.md)
* [INSERT](insert.md)
* [DELETE](delete.md)
* [UPDATE](update.md)
* [SQL Operators](sql-operators.md)