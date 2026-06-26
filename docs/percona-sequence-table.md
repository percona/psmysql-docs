# PERCONA_SEQUENCE_TABLE(n) function

Using the `PERCONA_SEQUENCE_TABLE()` function provides the following:

--8<--- "sequence-table-benefits.md"

## Version update

<!-- Update this doc to be valid for 9.7-->

Percona Server for MySQL 8.4 deprecated [`SEQUENCE_TABLE()`](sequence-table.md), and Percona may remove this function in a future release. We recommend that you use `PERCONA_SEQUENCE_TABLE()` instead.

To maintain compatibility with existing third-party software, `SEQUENCE_TABLE` is no longer a reserved term and can be used as a regular identifier.

## Table functions

--8<--- "sequence-table-concepts.md:1:1"

## Syntax

--8<--- "sequence-table-concepts.md:3:3"

--8<--- "sequence-table-concepts.md:5:5"

### PERCONA_SEQUENCE_TABLE(n) [AS] alias

```text
SELECT … FROM PERCONA_SEQUENCE_TABLE(n) [AS] alias

PERCONA_SEQUENCE_TABLE(n) [AS] alias
```

```text
SELECT * FROM PERCONA_SEQUENCE_TABLE(n) AS tt;
SELECT <expr(value)> FROM PERCONA_SEQUENCE_TABLE(n) AS tt;
```

--8<--- "sequence-table-concepts.md:7:7"

### Basic sequence generation

In this example, the following statement generates a sequence:

```sql
SELECT * FROM PERCONA_SEQUENCE_TABLE(3) AS tt;
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

```sql
SELECT value AS result \
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

--8<--- "sequence-table-concepts.md:9:9"

The following example prints only even numbers from the 0..7 range:

```sql
SELECT value AS result \
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

```sql
SELECT FLOOR(RAND() * 100) AS result \
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

```sql
SELECT MD5(value) AS result \
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

```sql
CREATE TABLE t1 AS SELECT * FROM PERCONA_SEQUENCE_TABLE(4) AS tt;

SELECT * FROM t1;
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

--8<--- "sequence-table-concepts.md:11:11"

[SEQUENCE_TABLE()]: sequence-table.md