# SQL syntax 

SQL (Structured Query Language) is a standardized language used to communicate with databases. Percona Server for MySQL follows SQL syntax, which consists of commands and statements for performing various operations on databases and their objects.

The SQL syntax includes commands for data manipulation (e.g., SELECT, INSERT, UPDATE, DELETE), data definition (e.g., CREATE, ALTER, DROP), data control (e.g., GRANT, REVOKE), and transaction control (e.g., COMMIT, ROLLBACK).


| Syntax type              | Description                                                                                                      |
|--------------------------|------------------------------------------------------------------------------------------------------------------|
| Data Manipulation        | MySQL supports powerful data manipulation features, allowing you to retrieve, insert, update, and delete data   |
| Data Definition          | With MySQL, you can define the structure of your database objects such as tables, indexes, views, and stored procedures |
| Data Control             | MySQL provides commands for controlling access to database objects and defining user privileges                  |
| Transaction Management   | MySQL supports transactions, which allow you to group multiple SQL statements into a single unit of work          |
| Stored Procedures        | MySQL allows you to define stored procedures and functions using SQL syntax                                      |
| Triggers                 | MySQL supports triggers, which are special types of stored procedures that automatically execute in response to specific events |
| Indexes                  | MySQL provides features for optimizing query performance, including the ability to create indexes on columns    |
| Views                    | MySQL allows you to create views, which are virtual tables generated from SQL queries                            |
| Data Types               | MySQL supports a wide range of data types for storing different types of data                                   |

These features make MySQL a powerful and versatile database management system, capable of handling a wide range of database tasks efficiently and effectively using SQL syntax.

While MySQL SQL syntax may deviate from the standard SQL syntax in some aspects, it generally aims to be compatible with standard SQL to ensure interoperability with other database systems and tools. However, developers should be aware of these differences and consult the MySQL documentation for guidance when writing SQL queries and statements.

MySQL SQL syntax largely adheres to the standard SQL syntax, but there are some differences and extensions that set it apart:

| Syntax              | Description                                                                                                                                                                           |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Data Types          | MySQL supports additional data types beyond the standard SQL specification, such as `ENUM`, `SET`, and `BOOLEAN`. These data types provide additional flexibility but may not be compatible with other database systems.                           |
| String Quoting      | MySQL allows both single quotes (`'`) and double quotes (`"`) for string literals, while standard SQL typically only uses single quotes. Additionally, MySQL supports backticks (`` ` ``) for quoting identifiers, which is not standard SQL syntax. |
| Case Sensitivity    | By default, MySQL treats table and column names as case-insensitive, while standard SQL treats them as case-sensitive. However, this behavior can be changed by adjusting the server configuration.                                              |
| LIMIT Clause        | MySQL uses the `LIMIT` clause to restrict the number of rows returned by a query, while standard SQL uses the `FETCH FIRST` or `OFFSET` clauses for similar functionality.                                                                          |
| AUTO_INCREMENT      | MySQL uses the `AUTO_INCREMENT` attribute to automatically generate unique values for a column, while standard SQL uses `IDENTITY` or sequences for this purpose.                                                                                  |
| SQL Functions       | MySQL provides additional built-in functions and extensions beyond the standard SQL functions. For example, MySQL has functions like `GROUP_CONCAT()` and `IFNULL()`, which may not be available in other database systems.                         |
| Storage Engines     | MySQL supports multiple storage engines, each with its own set of features and capabilities. This option allows users to choose the most suitable storage engine for their specific requirements, but it introduces differences in behavior and syntax. |

## Advanced SQL features

- [Data Types Basic](data-types-basic.md)
- [Functions](functions.md)
- [SQL Conventions](sql-conventions.md)
- [SQL Errors](sql-errors.md)
- [Stored Procedures](stored-procedures.md)
- [Stored Procedure Error Handling](stored-procedure-error-handling.md)
- [Stored Procedure Variables](stored-procedure-variables.md)
- [Triggers](triggers.md)
- [Troubleshooting SQL](troubleshooting-sql.md)