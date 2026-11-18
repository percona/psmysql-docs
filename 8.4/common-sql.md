> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Common SQL commands

SQL commands used by MySQL can be categorized into different types based on their purposes: Data Definition Language (DDL), Data Manipulation Language (DML), Data Control Language (DCL), and Transaction Control Language (TCL).

## Data Manipulation Language (DML)

DML commands manage data within database tables.

Common DML commands include:

- \[**SELECT**\]: This command retrieves data from a table or from several tables when you use a join. In this example, it selects all columns with a wildcard (`*`) from the `customers` table.

Be careful when using wildcards. They return every column, which can slow down queries, use more memory and network resources, and put extra load on both the server and the client.

````
```sql
SELECT * FROM customers;
````

```

- [**INSERT**]: This command adds new records to a table.

```

INSERT INTO customers (name, city) VALUES ('John Doe', 'Berlin');

```
- [**UPDATE**]: This command modifies existing records in a table.

```

UPDATE customers SET city = 'Madrid' WHERE id = 1;

```
- [**DELETE**]: This command removes records from a table.

```

DELETE FROM customers WHERE id = 1;

```

## Data Definition Language (DDL)

DDL commands define, modify, and remove database objects such as tables, indexes, and views.

Common DDL commands include:

- **CREATE**: This command creates new database objects like tables, indexes, and views.

```

CREATE TABLE employees (id INT, name VARCHAR(50));

```
- **ALTER**: This command modifies the structure of existing database objects.

```

ALTER TABLE employees ADD COLUMN city VARCHAR(50);

```
- **DROP**: This command removes database objects from the database.

```

DROP TABLE employees;

```

## Data Control Language (DCL)

DCL commands control access to database objects and define privileges.

Common DCL commands include:

- **GRANT**: This command grants specific privileges to database users.

```

GRANT SELECT, INSERT ON employees TO 'user1'@'localhost';

```
- **REVOKE**: This command revokes privileges from database users.

```

REVOKE INSERT ON employees FROM 'user2'@'localhost';

```

## Transaction Control Language (TCL)

TCL commands manage transactions within a database.

Common TCL commands include:

- **COMMIT**: This command saves changes made during the current transaction to the database.

```

COMMIT;

```
- **ROLLBACK**: This command undoes changes made during the current transaction and restores the database to its previous state.

```

ROLLBACK;

````

Fundamental SQL links:

- [SQL Basics](https://docs.percona.com/percona-server/8.4/sql-basics.html)
- [SELECT](https://docs.percona.com/percona-server/8.4/select.html)
- [INSERT](https://docs.percona.com/percona-server/8.4/insert.html)
- [DELETE](https://docs.percona.com/percona-server/8.4/delete.html)
- [UPDATE](https://docs.percona.com/percona-server/8.4/update.html)
- [SQL Operators](https://docs.percona.com/percona-server/8.4/sql-operators.html)```
````
