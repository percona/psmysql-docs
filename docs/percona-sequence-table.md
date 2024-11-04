# PERCONA_SEQUENCE_TABLE(n) function

Using the `PERCONA_SEQUENCE_TABLE()` function provides the following:

| Benefit                   | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| Generates Sequences       | Acts as an inline table-valued function that generates a sequence of numbers.                     |
| Table-Valued Function     | Unlike traditional scalar functions, `PERCONA_SEQUENCE_TABLE()` returns a virtual table with a single column named `value` containing the generated sequence. |
| Simpler Syntax            | Simplifies queries that need to generate predictable sequences of numbers.                        |
| Flexibility               | Allows dynamic definition of sequences within queries, offering more control compared to pre-defined tables for sequences. |
| Predefined Sequence       | Does not manage sequences like Oracle or PostgreSQL; instead, it allows definition and generation of sequences within a `SELECT` statement. |
| Customization             | Enables customization of starting value, increment/decrement amount, and number of values to generate. |

## Version update

Percona Server for MySQL 8.4 deprecated [`SEQUENCE_TABLE()`](sequence-table.md), and Percona may remove this function in a future release. We recommend that you use `PERCONA_SEQUENCE_TABLE()` instead.

To maintain compatibility with existing third-party software, `SEQUENCE_TABLE` is no longer a reserved term and can be used as a regular identifier.

## Table functions

The function is an inline table-valued function. This function creates a temporary table with multiple rows. You can use this function within a single SELECT statement. Oracle MySQL Server only has the `JSON_TABLE` table function. The Percona Server for MySQL has the `JSON_TABLE` and `PERCONA_SEQUENCE_TABLE()` table functions. A single SELECT statement generates a multi-row result set. In contrast, a scalar function (like [EXP(x)](https://dev.mysql.com/doc/refman/8.4/en/mathematical-functions.html#function_exp) or [LOWER(str)](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html#function_lower) always returns a single value of a specific data type.

## Syntax

As with any [derived tables](https://dev.mysql.com/doc/refman/8.4/en/derived-tables.html), a table function requires an [alias](https://dev.mysql.com/doc/refman/8.4/en/identifiers.html) in the `SELECT` statement.

The result set is a single column with the predefined column name `value` of type `BIGINT UNSIGNED`. You can reference the `value` column in `SELECT` statements. The following statements are valid. Using `n` as the number of generated values, the following is the basic syntax:

### PERCONA_SEQUENCE_TABLE(n) [AS] alias

```{.text .no-copy}
SELECT … FROM PERCONA_SEQUENCE_TABLE(n) [AS] alias

PERCONA_SEQUENCE_TABLE(n) [AS] alias
```

```{.text .no-copy}
SELECT * FROM PERCONA_SEQUENCE_TABLE(n) AS tt;
SELECT <expr(value)> FROM PERCONA_SEQUENCE_TABLE(n) AS tt;
```

The first number in the series, the initial term, is defined as `0`, and the series ends with a value less than `n`.

### Basic sequence generation

In this example, the following statement generates a sequence:

```{.bash data-prompt="mysql>"}
mysql> SELECT * FROM PERCONA_SEQUENCE_TABLE(3) AS tt;
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------+
    | value |
    +-------+
    |     0 |
    |     1 |
    |     2 |
    +-------+
    ```

### Start with a specific value

You can define the initial value using the `WHERE` clause. The following example starts the sequence with `4`.

```{.bash data-prompt="mysql>"}
mysql> SELECT value AS result \
       FROM \
            (SELECT seq AS value
             FROM PERCONA_SEQUENCE_TABLE(8)) AS tt \
       WHERE value >= 4;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------+
    | result |
    +--------+
    |      4 |
    |      5 |
    |      6 |
    |      7 |
    +--------+
    ```

### Filter even numbers

Consecutive terms increase or decrease by a common difference. The default common difference value is `1`. However, it is possible to filter the results using the WHERE clause to simulate common differences greater than 1.

The following example prints only even numbers from the 0..7 range:

```{.bash data-prompt="mysql>"}
mysql> SELECT value AS result \
       FROM PERCONA_SEQUENCE_TABLE(8) AS tt \
       WHERE value % 2 = 0;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------+
    | result |
    +--------+
    |      0 |
    |      2 |
    |      4 |
    |      6 |
    +--------+
    ```

### Generate random numbers

The following is an example of using the function to populate a table with a set of random numbers:

```{.bash data-prompt="mysql>"}
mysql> SELECT FLOOR(RAND() * 100) AS result \
       FROM PERCONA_SEQUENCE_TABLE(4) AS tt;
```

The output could be the following:

??? example "Expected output"

    ```{.text .no-copy}
    +--------+
    | result |
    +--------+
    |     24 |
    |     56 |
    |     70 |
    |     25 |
    +--------+
    ```

### Generate random strings

You can populate a table with a set of pseudo-random strings with the following statement:

```{.bash data-prompt="mysql>"}
mysql> SELECT MD5(value) AS result \
       FROM PERCONA_SEQUENCE_TABLE(4) AS tt;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------------------+
    | result                           |
    +----------------------------------+
    | f17d9c990f40f8ac215f2ecdfd7d0451 |
    | 2e5751b7cfd7f053cd29e946fb2649a4 |
    | b026324c6904b2a9cb4b88d6d61c81d1 |
    | 26ab0db90d72e28ad0ba1e22ee510510 |
    +----------------------------------+
    ```

### Add a sequence to a table

You can add the sequence as a column to a new table or an existing table, as shown in this example:

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE t1 AS SELECT * FROM PERCONA_SEQUENCE_TABLE(4) AS tt;

mysql> SELECT * FROM t1;
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------+
    | value |
    +-------+
    |     0 |
    |     1 |
    |     2 |
    |     3 |
    +-------+
    ```

Sequences are helpful for various purposes, such as populating tables and generating test data.

[`JSON_TABLE()`]: https://dev.mysql.com/doc/refman/8.4/en/json-table-functions.html

[SEQUENCE_TABLE()]: sequence-table.md