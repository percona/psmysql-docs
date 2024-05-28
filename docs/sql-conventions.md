# SQL conventions

Sure, here's a description of common SQL style conventions with examples using common MySQL commands:

## Naming Conventions

Naming conventions refer to the rules and guidelines for naming database objects such as tables, columns, indexes, and stored procedures.

- **Use descriptive names**: Choose names that clearly describe the purpose or content of the database object.

  ```{.bash data-prompt="mysql>"}
  mysql> CREATE TABLE users (
  mysql>     user_id INT AUTO_INCREMENT PRIMARY KEY,
  mysql>     username VARCHAR(50),
  mysql>     email VARCHAR(100)
  mysql> );
  ```

- **Avoid abbreviations**: Prefer full and meaningful words over abbreviations to enhance readability and understanding.

  ```{.bash data-prompt="mysql>"}
  mysql> ALTER TABLE customers
  mysql> ADD COLUMN date_of_birth DATE;
  ```

## Indentation and Formatting

Indentation and formatting conventions improve the readability and maintainability of SQL code.

- **Indent SQL statements**: Indent SQL statements consistently to show the logical structure of queries and commands.

  ```{.bash data-prompt="mysql>"}
  mysql> SELECT
  mysql>     user_id,
  mysql>     username,
  mysql>     email
  mysql> FROM
  mysql>     users
  mysql> WHERE
  mysql>     user_id = 1;
  ```

- **Use consistent casing**: Use consistent casing for keywords, identifiers, and SQL functions to improve code consistency.

  ```{.bash data-prompt="mysql>"}
  mysql> SELECT
  mysql>     first_name,
  mysql>     last_name,
  mysql>     CONCAT_WS(' ', first_name, last_name) AS full_name
  mysql> FROM
  mysql>     customers;
  ```

## Comments

Comments are annotations added to SQL code to explain its purpose, logic, or any other relevant information.

- **Document intent**: Use comments to document the intent or purpose of SQL statements and code blocks.

  ```{.bash data-prompt="mysql>"}
  mysql> -- Retrieve all active users
  mysql> SELECT * FROM users WHERE status = 'active';
  ```

- **Avoid redundant comments**: Avoid adding comments that merely repeat the code without adding meaningful information.

  ```{.bash data-prompt="mysql>"}
  mysql> -- This query retrieves all users
  mysql> SELECT * FROM users;
  ```

These SQL style conventions help maintain consistency, readability, and clarity in SQL code, making it easier to understand, debug, and maintain.

## Advanced SQL features

* [Data Types Basic](data-types-basic.md)
* [Functions](functions.md)
* [SQL Errors](sql-errors.md)
* [SQL Syntax](sql-syntax.md)
* [Stored Procedures](stored-procedures.md)
* [Stored Procedure Error Handling](stored-procedure-error-handling.md)
* [Stored Procedure Variables](stored-procedure-variables.md)
* [Triggers](triggers.md)
* [Troubleshooting SQL](troubleshooting-sql.md)