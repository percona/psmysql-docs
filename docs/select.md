# SELECT statement

The syntax of a SELECT statement in MySQL is straightforward. You start with the keyword SELECT, followed by the columns from which you want to retrieve data. You can specify the table from which to retrieve data using the FROM keyword. Optionally, you can include conditions to filter the results using the WHERE clause.

The following table is a breakdown of the syntax:

| Syntax        | Description                                                                                                                                                     |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **SELECT**    | This keyword indicates that you want to retrieve data from the database.                                                                                        |
| **Columns**   | Specify the columns you want to retrieve data from. You can use the asterisk (*) to select all columns or specify individual column names separated by commas. |
| **FROM**      | Use the FROM keyword to specify the table from which you want to retrieve data.                                                                                  |
| **WHERE (optional)** | If you want to filter the results based on specific conditions, you can use the WHERE clause. This clause allows you to specify conditions using comparison operators like =, >, <, etc., and logical operators like AND, OR, NOT. |


```text
SELECT column1, column2
FROM table_name
WHERE condition;
```

- `SELECT column1, column2` specifies that you want to retrieve data from column1 and column2.
- `FROM table_name` specifies the table from which you want to retrieve data.
- `WHERE condition` is an optional clause that filters the results based on the specified condition.

Fundamental SQL links:

* [Common SQL](docs/common-sql.md)
* [SQL Basics](docs/sql-basics.md)
* [INSERT](docs/insert.md)
* [DELETE](docs/delete.md)
* [UPDATE](docs/update.md)
* [SQL Operators](docs/sql-operators.md)