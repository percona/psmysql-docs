> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# SQL conventions

Sure, here’s a description of common SQL style conventions with examples using common MySQL commands:

## Naming Conventions

Naming conventions refer to the rules and guidelines for naming database objects such as tables, columns, indexes, and stored procedures.

- **Use descriptive names**: Choose names that clearly describe the purpose or content of the database object.

```
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
);
```

- **Avoid abbreviations**: Prefer full and meaningful words over abbreviations to enhance readability and understanding.

```
ALTER TABLE customers
ADD COLUMN date_of_birth DATE;
```

## Indentation and Formatting

Indentation and formatting conventions improve the readability and maintainability of SQL code.

- **Indent SQL statements**: Indent SQL statements consistently to show the logical structure of queries and commands.

```
SELECT
    user_id,
    username,
    email
FROM
    users
WHERE
    user_id = 1;
```

- **Use consistent casing**: Use consistent casing for keywords, identifiers, and SQL functions to improve code consistency.

```
SELECT
    first_name,
    last_name,
    CONCAT_WS(' ', first_name, last_name) AS full_name
FROM
    customers;
```

## Comments

Comments are annotations added to SQL code to explain its purpose, logic, or any other relevant information.

- **Document intent**: Use comments to document the intent or purpose of SQL statements and code blocks.

```
-- Retrieve all active users
SELECT * FROM users WHERE status = 'active';
```

- **Avoid redundant comments**: Avoid adding comments that merely repeat the code without adding meaningful information.

```
-- This query retrieves all users
SELECT * FROM users;
```

These SQL style conventions help maintain consistency, readability, and clarity in SQL code, making it easier to understand, debug, and maintain.

## Advanced SQL features

- [Data Types Basic](https://docs.percona.com/percona-server/9.7/data-types-basic.html)
- [Functions](https://docs.percona.com/percona-server/9.7/functions.html)
- [SQL Errors](https://docs.percona.com/percona-server/9.7/sql-errors.html)
- [SQL Syntax](https://docs.percona.com/percona-server/9.7/sql-syntax.html)
- [Stored Procedures](https://docs.percona.com/percona-server/9.7/stored-procedures.html)
- [Stored Procedure Error Handling](https://docs.percona.com/percona-server/9.7/stored-procedure-error-handling.html)
- [Stored Procedure Variables](https://docs.percona.com/percona-server/9.7/stored-procedure-variables.html)
- [Triggers](https://docs.percona.com/percona-server/9.7/triggers.html)
- [Troubleshooting SQL](https://docs.percona.com/percona-server/9.7/troubleshooting-sql.html)
