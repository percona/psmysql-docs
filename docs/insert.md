# INSERT statement

In MySQL, the INSERT statement adds new rows of data to a table. It follows a simple syntax pattern that beginners can easily understand.

| Trade-Offs      | Description                                                                                                                                                                                                                         |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Advantages      | - Allows for efficient addition of new data into the database.                                                                                                                                                                     |
|                 | - Provides flexibility to insert data into specific columns or all columns of a table.                                                                                                                                               |
|                 | - Supports inserting multiple rows with a single INSERT statement.                                                                                                                                                                 |
|                 | - Can be used in conjunction with SELECT statements to insert data from one table into another.                                                                                                                                      |
| Disadvantages   | - May result in performance overhead, especially when inserting large volumes of data or when indexes need to be updated.                                                                                                           |
|                 | - Requires proper error handling to deal with constraints, such as primary key or unique constraints, to prevent duplicate entries.                                                                                                 |
|                 | - Limited functionality for bulk inserts compared to specialized tools or techniques like bulk loading utilities.                                                                                                                   |

Syntax of the INSERT Statement:

| Option                | Description                                                                                                                                                                                                                                        |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| INSERT INTO          | This keyword indicates that you are performing an insertion operation into a table.                                                                                                                                                                |
| table_name           | This is the name of the table where you want to insert the data.                                                                                                                                                                                  |
| column1, column2, ...| These are optional and specify the columns into which you want to insert data. If omitted, values must be provided for all columns in the table, in the same order as they are defined in the table.                                        |
| VALUES               | This keyword introduces the list of values to be inserted into the specified columns. Alternatively, you can use the SELECT statement to retrieve data from another table and insert it into the specified columns.                     |
| value1, value2, ... | These are the values to be inserted into the corresponding columns. The number and order of values must match the number and order of columns specified in the INSERT INTO clause.                                                               |

The number of values in the `VALUES` clause must always match the number of columns specified or the total number of columns in the table.

To insert data into a table, you use the INSERT INTO statement followed by the table name and a list of column names (if specified) or the `VALUES` keyword, followed by the values you want to insert into the table.

```sql
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);
```

In this example, we are doing the following:

- Inserting a new row into the "employees" table.

- The values 1, 'John Doe', and 50000 are being inserted into the "id", "name", and "salary" columns, respectively.

```{.bash data-prompt="mysql>"}
mysql> INSERT INTO employees (id, name, salary)
        VALUES (1, 'John Doe', 50000);
```

Fundamental SQL links:

* [Common SQL](common-sql.md)
* [SQL Basics](sql-basics.md)
* [SELECT](select.md)
* [DELETE](delete.md)
* [UPDATE](update.md)
* [SQL Operators](sql-operators.md)