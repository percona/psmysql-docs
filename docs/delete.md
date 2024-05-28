# DELETE statement

The DELETE statement removes one or more rows from a table based on specified conditions. It allows developers to selectively delete data from a table, providing a way to manage and maintain the database by removing unnecessary or outdated records.

## Advantages and Disadvantages of Using DELETE Statement

| Trade-offs        | Description                                                                                                                        |
|--------------|------------------------------------------------------------------------------------------------------------------------------------|
| Advantages   | Allows selective removal of specific rows from a table, helping to maintain data integrity and manage database resources efficiently. |
|              | Can be combined with WHERE clause to delete rows that meet certain conditions, providing flexibility in data manipulation.           |
|              | Provides a straightforward way to remove unwanted data without affecting the structure of the table or other related tables.       |
| Disadvantages| Deleting large amounts of data can impact performance and may require careful consideration to avoid unintended consequences.        |
|              | Deletes are permanent and irreversible, so it's crucial to double-check conditions and backup data before executing DELETE queries. |

## Syntax of DELETE Statement

The statement has the following options:

| Option | Description |
|---|---|
| `DELETE FROM table_name` | This clause specifies the table from which you want to delete rows. |
| `WHERE condition` (Optional) | This clause filters the rows to be deleted based on a specific condition. If omitted, all rows in the table will be deleted. |

The syntax of the DELETE statement is as follows:

```text
DELETE FROM table_name
[WHERE condition];
```

## Example of DELETE Statement

This example deletes all rows from the `orders` table where the `order_date` is before January 1, 2023.

```{.bash data-prompt="mysql>"}
DELETE FROM orders
WHERE order_date < '2023-01-01';
```

Fundamental SQL links:

* [Common SQL](docs/common-sql.md)
* [SQL Basics](docs/sql-basics.md)
* [SELECT](docs/select.md)
* [INSERT](docs/insert.md)
* [UPDATE](docs/update.md)
* [SQL Operators](docs/sql-operators.md)