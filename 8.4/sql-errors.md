> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Common SQL errors

Error handling in SQL commands involves managing and responding to errors that may occur during database operations. It ensures that the database remains consistent and provides feedback to users when errors occur.

## SELECT statement

When executing a SELECT statement, errors may occur due to invalid syntax, missing tables, or insufficient permissions.

```
SELECT * FROM non_existent_table;
ERROR 1146 (42S02): Table 'database_name.non_existent_table' doesn't exist
```

## INSERT Statement

Errors can occur during INSERT operations if data violates constraints or exceeds column limits.

```
INSERT INTO table_name (id, name) VALUES (1, 'John');
ERROR 1136 (21S01): Column count doesn't match value count at row 1
```

## UPDATE Statement

UPDATE statements may encounter errors when attempting to modify non-existent rows or violating constraints.

```
UPDATE table_name SET non_existent_column = 'value';
ERROR 1054 (42S22): Unknown column 'non_existent_column' in 'field list'
```

## DELETE Statement

Errors in DELETE statements can occur if the WHERE clause condition is invalid or violates constraints.

```
DELETE FROM table_name WHERE id = 'non_numeric_value';
ERROR 1054 (42S22): Unknown column 'non_numeric_value' in 'where clause'
```

## DDL Statements (CREATE, ALTER, DROP)

DDL statements may fail due to syntax errors, existing object conflicts, or insufficient privileges.

```
CREATE TABLE existing_table (id INT PRIMARY KEY);
ERROR 1050 (42S01): Table 'existing_table' already exists
```

## Advanced SQL features

- [Data Types Basic](https://docs.percona.com/percona-server/8.4/data-types-basic.html)
- [Functions](https://docs.percona.com/percona-server/8.4/functions.html)
- [SQL Conventions](https://docs.percona.com/percona-server/8.4/sql-conventions.html)
- [SQL Syntax](https://docs.percona.com/percona-server/8.4/sql-syntax.html)
- [Stored Procedures](https://docs.percona.com/percona-server/8.4/stored-procedures.html)
- [Stored Procedure Error Handling](https://docs.percona.com/percona-server/8.4/stored-procedure-error-handling.html)
- [Stored Procedure Variables](https://docs.percona.com/percona-server/8.4/stored-procedure-variables.html)
- [Triggers](https://docs.percona.com/percona-server/8.4/triggers.html)
- [Troubleshooting SQL](https://docs.percona.com/percona-server/8.4/troubleshooting-sql.html)
