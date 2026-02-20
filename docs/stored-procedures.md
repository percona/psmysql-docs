# Stored Procedures

A stored procedure is a set of pre-defined SQL statements stored in the database and executed as a single unit. It allows users to execute complex operations without rewriting the same code multiple times.

| Benefit               | Description                                                                                                                      |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Code Reusability      | Stored procedures can be reused multiple times in different parts of an application, reducing code duplication.                   |
| Improved Performance | By executing multiple SQL statements in a single call, stored procedures can reduce network traffic and improve performance.     |
| Enhanced Security     | Users can execute stored procedures without needing direct access to underlying tables, improving security and data integrity. |
| Centralized Logic     | Business logic is encapsulated within stored procedures, making it easier to manage and maintain.                                |

| Disadvantage           | Description                                                                                                                                                                       |
|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Difficulty in Debugging | Stored procedures can be challenging to debug, as they are executed on the database server rather than within the application code.                                               |
| Vendor Lock-in         | Stored procedures are specific to a particular database system, making it difficult to migrate to another database platform.                                                    |
| Limited Portability    | Stored procedures written in one database system may not be compatible with other systems, limiting portability and interoperability.                                          |

## Stored Procedure examples

### Create a Stored Procedure

```sql
DELIMITER //
CREATE PROCEDURE GetCustomerDetails (IN customerId INT)
    BEGIN
        SELECT * FROM customers WHERE id = customerId;
    END //
DELIMITER ;
```

### Call a Stored Procedure

```sql
CALL GetCustomerDetails(123);
```

### Modify a Stored Procedure

```sql
DELIMITER //
ALTER PROCEDURE GetCustomerDetails (IN customerId INT)
    BEGIN
        SELECT name, city FROM customers WHERE id = customerId;
    END //
DELIMITER ;
```

### Drop a Stored Procedure

```sql
DROP PROCEDURE IF EXISTS GetCustomerDetails;
```

## Advanced SQL features

* [Data Types Basic](data-types-basic.md)
* [Functions](functions.md)
* [SQL Conventions](sql-conventions.md)
* [SQL Errors](sql-errors.md)
* [SQL Syntax](sql-syntax.md)
* [Stored Procedure Error Handling](stored-procedure-error-handling.md)
* [Stored Procedure Variables](stored-procedure-variables.md)
* [Triggers](triggers.md)
* [Troubleshooting SQL](troubleshooting-sql.md)
