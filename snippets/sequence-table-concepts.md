The function is an inline table-valued function. This function creates a temporary table with multiple rows. You can use this function within a single SELECT statement. Oracle MySQL Server only has the [`JSON_TABLE` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/json-table-functions.html) table function. The Percona Server for MySQL has the `JSON_TABLE` table function and Percona sequence table functions. A single SELECT statement generates a multi-row result set. In contrast, a scalar function (like [EXP(x) :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/mathematical-functions.html#function_exp) or [LOWER(str) :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/string-functions.html#function_lower) always returns a single value of a specific data type.

As with any [derived tables :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/derived-tables.html), a table function requires an [alias :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/identifiers.html) in the `SELECT` statement.

The result set is a single column with the predefined column name `value` of type `BIGINT UNSIGNED`. You can reference the `value` column in `SELECT` statements. The following statements are valid. Using `n` as the number of generated values, the following is the basic syntax:

The first number in the series, the initial term, is defined as `0`, and the series ends with a value less than `n`.

Consecutive terms increase or decrease by a common difference. The default common difference value is `1`. However, it is possible to filter the results using the WHERE clause to simulate common differences greater than 1.

Sequences are helpful for various purposes, such as populating tables and generating test data.
