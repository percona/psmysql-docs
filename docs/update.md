# UPDATE statement

## Purpose of the UPDATE Statement

The UPDATE statement modifies existing records in a table. It allows developers to change the values of one or more columns in a specific row or set of rows based on certain conditions.

Advantages and Disadvantages of Using the UPDATE Statement:

| Trade-offs       | Description                                                                                                                                     |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| Advantages  | - Allows for updating existing data without the need to delete and re-insert records.                                                           |
|             | - Provides flexibility in modifying specific columns or rows based on specified conditions.                                                     |
|             | - Can be used in conjunction with WHERE clause to update only selected rows, reducing unnecessary updates and improving performance.              |
|             | - Supports bulk updates, allowing multiple rows to be modified in a single statement.                                                            |
| Disadvantages | - Incorrectly formulated UPDATE statements can lead to unintended data changes or data loss.                                                   |
|              | - Lack of proper WHERE clause can result in updating all rows in a table, potentially causing data corruption or performance issues.            |
|              | - May cause locking and contention issues in high-concurrency environments, impacting the performance of other queries accessing the same table. |

Syntax of an UPDATE Statement:

| Option | Description |
|---|---|
| `UPDATE table_name` | This clause specifies the name of the table you want to modify. |
| `SET column_name1 = value1, column_name2 = value2, ...` | This clause defines which columns you want to update and their corresponding new values. You can update multiple columns by separating them with commas. |
| `WHERE condition` (optional) | This clause specifies a condition that filters which rows in the table will be affected by the update. If omitted, all rows in the table will be updated. |

```text
UPDATE table_name
SET column1 = value1, column2 = value2, ...
[WHERE condition];
```

In this example, the statement does the following:

- Modifies the `salary` column for employees in the 'Sales' department.

- Increases the salary of each employee by 10% (`salary * 1.1`).

```{.bash data-prompt="mysql>"}
UPDATE employees
SET salary = salary * 1.1
WHERE department = 'Sales';
```

Fundamental SQL links:

* [Common SQL](common-sql.md)
* [SQL Basics](sql-basics.md)
* [SELECT](select.md)
* [INSERT](insert.md)
* [DELETE](delete.md)
* [SQL Operators](sql-operators.md)