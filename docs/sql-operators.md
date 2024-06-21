# SQL operators

## Purpose of SQL Operators

SQL operators are symbols or keywords used to perform operations on data in SQL queries. They allow developers to manipulate and compare data, perform calculations, and filter results based on specified conditions.

Advantages and Disadvantages of Using SQL Operators:

| Trade-Offs      | Description                                                                                                                                                                                                                     |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Advantages      | - Enables developers to perform various operations on data, such as arithmetic calculations, comparisons, logical operations, and string concatenation.                                                                   |
|                 | - Provides flexibility in crafting complex queries to extract, transform, and manipulate data according to specific requirements.                                                                                              |
|                 | - Enhances query efficiency by allowing filtering and sorting of data directly within SQL queries, reducing the need for post-processing in application code.                                                                 |
| Disadvantages   | - May introduce complexity to queries, especially when multiple operators are combined or when dealing with complex logical conditions.                                                                                       |
|                 | - Requires careful consideration of operator precedence and evaluation order to ensure the desired results are obtained.                                                                                                        |
|                 | - Can sometimes result in less readable or maintainable queries, particularly for developers unfamiliar with the SQL syntax or operators being used.                                                                            |

Syntax of Using SQL Operators:

| Option           | Description                                                                                                                                                                                                                    |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Arithmetic       | Arithmetic operators such as `+`, `-`, `*`, `/`, and `%` are used to perform mathematical calculations on numeric data.                                                                                                       |
| Comparison       | Comparison operators like `=`, `<>`, `<`, `>`, `<=`, and `>=` are used to compare values and determine their relationship.                                                                                                   |
| Logical          | Logical operators such as `AND`, `OR`, and `NOT` are used to perform logical operations on boolean values or expressions.                                                                                                     |
| Concatenation    | The `CONCAT()` function or `||` operator is used to concatenate strings together.                                                                                                                                              |
| Bitwise          | Bitwise operators like `&`, `|`, `^`, `~`, `<<`, and `>>` are used to perform bitwise operations on binary data.                                                                                                               |
| Assignment       | The `=` and `:=` operators are used to assign values to variables or columns.                                                                                                                                                  |
| In               | The `IN` operator is used to check whether a value matches any value in a list or subquery.                                                                                                                                    |
| Like             | The `LIKE` operator is used to compare a value to a pattern using wildcard characters `%` and `_`.                                                                                                                             |

Example of Using SQL Operators:

- **Arithmetic Operator Example**:

```text
mysql> SELECT 10 * 5; -- Multiplication
```

- **Comparison Operator Example**:

```text
mysql> SELECT * FROM products WHERE price > 100; -- Select products with price greater than 100
```

- **Logical Operator Example**:

```text
mysql> SELECT * FROM customers WHERE age >= 18 AND age <= 30; -- Select customers aged between 18 and 30
```

- **Concatenation Operator Example**:

```text
mysql> SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees; -- Concatenate first name and last name
```

- **Bitwise Operator Example**:

```text
mysql> SELECT id, name FROM permissions WHERE permission_flags & 4 = 4; -- Select permissions with specific flag
```

- **Assignment Operator Example**:

```text
mysql> SET @total_sales := 500; -- Assigning a value to a variable
```

- **In Operator Example**:

```text
mysql> SELECT * FROM products WHERE category_id IN (1, 2, 3); -- Select products in specified categories
```

- **Like Operator Example**:

```text
mysql> SELECT * FROM customers WHERE email LIKE '%@example.com'; -- Select customers with email domain example.com
```

These examples illustrate how SQL operators are used in Percona Server for MySQL queries to perform various data operations.

Fundamental SQL links:

- [Common SQL](common-sql.md)
- [SQL Basics](sql-basics.md)
- [SELECT](select.md)
- [INSERT](insert.md)
- [DELETE](delete.md)
- [UPDATE](update.md)