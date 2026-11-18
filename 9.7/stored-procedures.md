> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Stored Procedures

A stored procedure is a set of pre-defined SQL statements stored in the database and executed as a single unit. It allows users to execute complex operations without rewriting the same code multiple times.

| Benefit              | Description                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Code Reusability     | Stored procedures can be reused multiple times in different parts of an application, reducing code duplication.                |
| Improved Performance | By executing multiple SQL statements in a single call, stored procedures can reduce network traffic and improve performance.   |
| Enhanced Security    | Users can execute stored procedures without needing direct access to underlying tables, improving security and data integrity. |
| Centralized Logic    | Business logic is encapsulated within stored procedures, making it easier to manage and maintain.                              |

| Disadvantage            | Description                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Difficulty in Debugging | Stored procedures can be challenging to debug, as they are executed on the database server rather than within the application code.   |
| Vendor Lock-in          | Stored procedures are specific to a particular database system, making it difficult to migrate to another database platform.          |
| Limited Portability     | Stored procedures written in one database system may not be compatible with other systems, limiting portability and interoperability. |

## Stored Procedure examples

### Create a Stored Procedure

```
DELIMITER //
CREATE PROCEDURE GetCustomerDetails (IN customerId INT)
    BEGIN
        SELECT * FROM customers WHERE id = customerId;
    END //
DELIMITER ;
```

### Call a Stored Procedure

```
CALL GetCustomerDetails(123);
```

### Modify a Stored Procedure

```
DELIMITER //
ALTER PROCEDURE GetCustomerDetails (IN customerId INT)
    BEGIN
        SELECT name, city FROM customers WHERE id = customerId;
    END //
DELIMITER ;
```

### Drop a Stored Procedure

```
DROP PROCEDURE IF EXISTS GetCustomerDetails;
```

## Advanced SQL features

- [Data Types Basic](https://docs.percona.com/percona-server/9.7/data-types-basic.html)
- [Functions](https://docs.percona.com/percona-server/9.7/functions.html)
- [SQL Conventions](https://docs.percona.com/percona-server/9.7/sql-conventions.html)
- [SQL Errors](https://docs.percona.com/percona-server/9.7/sql-errors.html)
- [SQL Syntax](https://docs.percona.com/percona-server/9.7/sql-syntax.html)
- [Stored Procedure Error Handling](https://docs.percona.com/percona-server/9.7/stored-procedure-error-handling.html)
- [Stored Procedure Variables](https://docs.percona.com/percona-server/9.7/stored-procedure-variables.html)
- [Triggers](https://docs.percona.com/percona-server/9.7/triggers.html)
- [Troubleshooting SQL](https://docs.percona.com/percona-server/9.7/troubleshooting-sql.html)
