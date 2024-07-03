# Functions

A function in MySQL is a reusable block of code that performs a specific task and returns a value. It allows users to encapsulate logic, modularize code, and perform complex calculations or data manipulations.

## Advantages of Using Functions:

| Benefits        | Description                                                                                                                                                                      |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Reusability     | Functions can be reused multiple times in different parts of a SQL statement or query, reducing code duplication and promoting code modularity and maintainability.          |
| Encapsulation   | Functions encapsulate logic and calculations, making it easier to understand and manage complex operations within the database.                                                |
| Performance     | Functions can improve query performance by reducing the amount of data transferred between the database server and the client application.                                       |
| Customization   | Functions allow users to create custom data transformations and calculations tailored to specific business requirements, enhancing the flexibility of the database.      |

## Disadvantages of Using Functions:

| Disadvantages   | Description                                                                                                                                                                      |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Performance     | Functions may introduce performance overhead, particularly if they involve complex computations or require access to large datasets.                                           |
| Maintenance     | Functions require maintenance to keep them synchronized with changes to the underlying data model or business logic. Changes may impact the behavior of dependent queries. |
| Portability     | Functions written in MySQL may not be compatible with other database systems, limiting the portability of applications and databases.                                           |
| Security        | Improperly designed or implemented functions may pose security risks, such as SQL injection vulnerabilities or unauthorized access to sensitive data.                        |

## Create function

```{.bash data-prompt="mysql>"}
mysql> CREATE FUNCTION calculate_discount (total_amount DECIMAL(10, 2)) RETURNS DECIMAL(10, 2)
    -> BEGIN
    ->     DECLARE discount DECIMAL(10, 2);
    ->     IF total_amount > 100 THEN
    ->         SET discount = total_amount * 0.1;
    ->     ELSE
    ->         SET discount = 0;
    ->     END IF;
    ->     RETURN discount;
    -> END;
```

## Call function

```{.bash data-prompt="mysql>"}
mysql> SELECT calculate_discount(120);
```

## Drop function

```{.bash data-prompt="mysql>"}
mysql> DROP FUNCTION IF EXISTS calculate_discount;
```

## Advanced SQL features

- [Data Types Basic](data-types-basic.md)
- [SQL Conventions](sql-conventions.md)
- [SQL Errors](sql-errors.md)
- [SQL Syntax](sql-syntax.md)
- [Stored Procedures](stored-procedures.md)
- [Stored Procedure Error Handling](stored-procedure-error-handling.md)
- [Stored Procedure Variables](stored-procedure-variables.md)
- [Triggers](triggers.md)
- [Troubleshooting SQL](troubleshooting-sql.md)