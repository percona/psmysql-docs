> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Troubleshoot SQL code

Review [Get help from Percona](https://docs.percona.com/percona-server/9.7/get-help.md) for ways that we can work with you.

## Troubleshooting SQL Code

To troubleshoot SQL code, follow these steps:

| Action                        | Description                                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Review Error Messages         | Carefully read any error messages returned by the MySQL server. They often provide valuable clues about what went wrong. |
| Check Syntax                  | Verify that the SQL syntax is correct. A single typo or missing keyword can cause errors.                                |
| Verify Table and Column Names | Ensure that table and column names are spelled correctly and match the actual names in the database.                     |
| Test in Isolation             | Test each part of the SQL statement separately to identify which part is causing the issue.                              |
| Use Logging Tools             | Enable query logging or use debugging tools to track the execution of SQL queries and identify any issues.               |
| Review Documentation          | Consult the MySQL documentation to understand the correct usage of SQL statements and functions.                         |
| Seek Help                     | Don’t hesitate to ask for help from more experienced developers or consult online forums and communities for assistance. |

Troubleshooting SQL Code example:

Suppose you have the following SQL query that is not returning the expected results:

```text
SELECT * FORM users WHERE age = 30;
```

After reviewing the error message returned by MySQL, you notice a typo in the query. The keyword “FORM” should be “FROM”. After correcting the typo, the query becomes:

```text
SELECT * FROM users WHERE age = 30;
```

Now, the query should execute successfully and return the desired results.

## Advanced SQL features

- [Data Types Basic](https://docs.percona.com/percona-server/9.7/data-types-basic.md)
- [Functions](https://docs.percona.com/percona-server/9.7/functions.md)
- [SQL Conventions](https://docs.percona.com/percona-server/9.7/sql-conventions.md)
- [SQL Errors](https://docs.percona.com/percona-server/9.7/sql-errors.md)
- [SQL Syntax](https://docs.percona.com/percona-server/9.7/sql-syntax.md)
- [Stored Procedures](https://docs.percona.com/percona-server/9.7/stored-procedures.md)
- [Stored Procedure Error Handling](https://docs.percona.com/percona-server/9.7/stored-procedure-error-handling.md)
- [Stored Procedure Variables](https://docs.percona.com/percona-server/9.7/stored-procedure-variables.md)
- [Triggers](https://docs.percona.com/percona-server/9.7/triggers.md)
