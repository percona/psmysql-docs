> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Variables in stored procedures, functions, and triggers

To add a variable in MySQL, you use the `DECLARE` keyword within the context of a stored program, such as a stored procedure, function, or trigger. The `DECLARE` keyword is used to define a new variable along with its data type and optionally, its initial value.

| Value         | Description                                                                                                                                              |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| variable_name | This is the name of the variable you want to declare. Variable names must follow the rules for identifiers in MySQL.                                     |
| data_type     | This specifies the data type of the variable, such as `INT`, `VARCHAR`, `DECIMAL`, `DATE`, etc.                                                          |
| default_value | This is an optional parameter that specifies the default value for the variable. If not provided, the variable will be initialized to `NULL` by default. |

```
DECLARE variable_name data_type [DEFAULT default_value];
```

- When you declare a variable using the `DECLARE` keyword, you are essentially telling MySQL to reserve space in memory to store a value of the specified data type.
- Variables in MySQL are scoped to the block in which they are declared. This means they can only be used within the block of code (for example, stored procedure, function) in which they are declared.
- Variables can be used to store and manipulate values within the context of the stored program. They are commonly used for temporary storage of intermediate results, loop counters, or parameters passed to the program.

```
DECLARE total_sales DECIMAL(10, 2) DEFAULT 0.0;
```

This statement has the following settings:

| Description                                                                                                                            | Value            |
| -------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `total_sales` is the name of the variable.                                                                                             | `total_sales`    |
| `DECIMAL(10, 2)` specifies that `total_sales` will hold decimal numbers with a precision of 10 digits and a scale of 2 decimal places. | `DECIMAL(10, 2)` |
| `DEFAULT 0.0` sets the initial value of `total_sales` to 0.0. If not provided, the default value would be `NULL`.                      | `DEFAULT 0.0`    |

## Advanced SQL features

- [Data Types Basic](https://docs.percona.com/percona-server/9.7/data-types-basic.html)
- [Functions](https://docs.percona.com/percona-server/9.7/functions.html)
- [SQL Conventions](https://docs.percona.com/percona-server/9.7/sql-conventions.html)
- [SQL Errors](https://docs.percona.com/percona-server/9.7/sql-errors.html)
- [SQL Syntax](https://docs.percona.com/percona-server/9.7/sql-syntax.html)
- [Stored Procedures](https://docs.percona.com/percona-server/9.7/stored-procedures.html)
- [Stored Procedure Error Handling](https://docs.percona.com/percona-server/9.7/stored-procedure-error-handling.html)
- [Triggers](https://docs.percona.com/percona-server/9.7/triggers.html)
- [Troubleshooting SQL](https://docs.percona.com/percona-server/9.7/troubleshooting-sql.html)
