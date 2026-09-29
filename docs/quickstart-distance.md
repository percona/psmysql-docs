# Get started with DISTANCE()

This quickstart compares one stored vector with one query vector using every distance metric that `DISTANCE()` supports. The metric examples share one table and the same two unit-length vectors, `[0.3333333333, 0.6666666667, 0.6666666667]` and `[0.2857142857, 0.4285714286, 0.8571428571]`, so the metric is what changes the result. Later sections use the same table to rank several vectors and to show how the function handles invalid input.

The supported metrics are:

* [`EUCLIDEAN`](#euclidean-distance)
* [`EUCLIDEAN_SQUARED`](#euclidean-squared-distance)
* [`COSINE`](#cosine-distance)
* [`DOT`](#dot-distance)
* [`MANHATTAN`](#manhattan-distance)

You need access to a Percona Server for MySQL {{vers}} server and an account that can create a database and tables. 

For arguments and return values, see [DISTANCE() Function](distance-function.md).

## Create the sample database and table

The following statements create and select a dedicated `testdb` database so that the examples do not modify a table in your current database. If that database already exists, either [remove it](#clean-up) or use another database name. The first statement drops `testdb` if the database already exists, including everything in that database.

`TO_VECTOR()` converts the string representation of a vector to a `VECTOR` value. The statements also create a `documents` table and store `[0.3333333333, 0.6666666667, 0.6666666667]` in the `embedding` column:

```sql

DROP DATABASE IF EXISTS testdb;

CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE testdb;

CREATE TABLE documents (
    id INT PRIMARY KEY,
    content VARCHAR(100),
    embedding VECTOR(3)
);

INSERT INTO documents (id, content, embedding)
VALUES (
    1,
    'Example document',
    TO_VECTOR('[0.3333333333, 0.6666666667, 0.6666666667]')
);
```

Each example below compares that stored embedding with `[0.2857142857, 0.4285714286, 0.8571428571]`.

!!! note "Precision of the results"

    A `VECTOR` stores each element as a single-precision (4-byte) float, and `DISTANCE()` returns a `DOUBLE`. Results can therefore differ from exact arithmetic in the seventh or eighth significant digit. The calculation shown under each output gives the exact value, and the digits you see after the seventh decimal place may differ from the output shown here.

## Euclidean distance

`EUCLIDEAN` measures the straight-line distance between the vectors.

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.2857142857, 0.4285714286, 0.8571428571]'),
    'EUCLIDEAN'
) AS distance
FROM documents;
```

??? example "Expected output"

    ```text
    +--------------------+
    | distance           |
    +--------------------+
    | 0.3086067045227826 |
    +--------------------+
    1 row in set (0.003 sec)
    ```

The calculation is `sqrt((1/3 - 2/7)^2 + (2/3 - 3/7)^2 + (2/3 - 6/7)^2) = sqrt((1/21)^2 + (5/21)^2 + (-4/21)^2) = sqrt(42/441) = sqrt(2/21) ≈ 0.3086067`.

## Euclidean squared distance

`EUCLIDEAN_SQUARED` returns the square of the Euclidean distance. Use this metric when you only need to rank vectors, because the metric skips the square root.

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.2857142857, 0.4285714286, 0.8571428571]'),
    'EUCLIDEAN_SQUARED'
) AS distance
FROM documents;
```

??? example "Expected output"

    ```text
    +---------------------+
    | distance            |
    +---------------------+
    | 0.09523809807641204 |
    +---------------------+
    1 row in set (0.003 sec)
    ```

The calculation is `(1/21)^2 + (5/21)^2 + (-4/21)^2 = 42/441 = 2/21 ≈ 0.0952381`. The result ranges from `0` (same direction) through `1` (orthogonal) to `2` (opposite directions).


## Cosine distance

`COSINE` returns `1 - cosine similarity`.

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.2857142857, 0.4285714286, 0.8571428571]'),
    'COSINE'
) AS distance
FROM documents;
```

??? example "Expected output"

    ```text
    +---------------------+
    | distance            |
    +---------------------+
    | 0.04761904701083697 |
    +---------------------+
    1 row in set (0.001 sec)
    ```

Because both vectors are already unit length, cosine similarity here is the raw inner product: `(1/3)(2/7) + (2/3)(3/7) + (2/3)(6/7) = 2/21 + 6/21 + 12/21 = 20/21 ≈ 0.952381`. Cosine distance is `1 - 20/21 = 1/21 ≈ 0.047619`.

For unit-length vectors, Euclidean distance is a monotonic function of cosine similarity, so both metrics produce the same ranking. For vectors of different lengths, they can differ.

## DOT distance

For `DOT`, `DISTANCE()` returns the negative inner product, so a smaller value means the vectors are more closely aligned.

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.2857142857, 0.4285714286, 0.8571428571]'),
    'DOT'
) AS distance
FROM documents;
```

??? example "Expected output"

    ```text
    +---------------------+
    | distance            |
    +---------------------+
    | -0.9523809935365408 |
    +---------------------+
    1 row in set (0.001 sec)
    ```

The inner product is `20/21 ≈ 0.952381`, and DISTANCE() returns its negative: `-0.952381`.

## Manhattan distance

`MANHATTAN` adds the absolute difference between corresponding elements. This metric is a Percona Server extension.

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.2857142857, 0.4285714286, 0.8571428571]'),
    'MANHATTAN'
) AS distance
FROM documents;
```

??? example "Expected output"

    ```text
    +--------------------+
    | distance           |
    +--------------------+
    | 0.4761904776096344 |
    +--------------------+
    1 row in set (0.001 sec)
    ```

The calculation is `|1/21| + |5/21| + |4/21| = 10/21 ≈ 0.476190`.

## Find the closest vectors

A similarity search compares a query vector against many stored embeddings. Add three more documents to the sample table:

```sql
INSERT INTO documents (id, content, embedding)
VALUES
    (2, 'Nearby document', TO_VECTOR('[0.25, 0.375, 0.5]')),
    (3, 'Opposite document', TO_VECTOR('[-0.125, -0.25, -0.375]')),
    (4, 'Exact query vector', TO_VECTOR('[0.5, 0.625, 0.75]'));
```

Use `DISTANCE()` in the `ORDER BY` clause and sort in ascending order. `LIMIT 3` returns the three closest vectors:

```sql
SELECT id,
       content,
       CAST(
           DISTANCE(
               embedding,
               TO_VECTOR('[0.5, 0.625, 0.75]'),
               'COSINE'
           ) AS DECIMAL(8, 6)
       ) AS distance
FROM documents
ORDER BY distance ASC
LIMIT 3;
```

??? example "Expected output"

    ```text
    +----+--------------------+----------+
    | id | content            | distance |
    +----+--------------------+----------+
    |  4 | Exact query vector | 0.000000 |
    |  2 | Nearby document    | 0.005388 |
    |  1 | Example document   | 0.012342 |
    +----+--------------------+----------+
    3 rows in set (0.003 sec)
    ```

Lower distance values represent closer matches. The exact query vector ranks first because its cosine distance is `0`.

### Compare rankings across metrics

The metric can change which document ranks second. Run the same search with `EUCLIDEAN`:

```sql
SELECT id,
       content,
       CAST(
           DISTANCE(
               embedding,
               TO_VECTOR('[0.5, 0.625, 0.75]'),
               'EUCLIDEAN'
           ) AS DECIMAL(8, 6)
       ) AS distance
FROM documents
ORDER BY DISTANCE(
             embedding,
             TO_VECTOR('[0.5, 0.625, 0.75]'),
             'EUCLIDEAN'
         ) ASC
LIMIT 3;
```

??? example "Expected output"

    ```text
    +----+--------------------+----------+
    | id | content            | distance |
    +----+--------------------+----------+
    |  4 | Exact query vector | 0.000000 |
    |  1 | Example document   | 0.190941 |
    |  2 | Nearby document    | 0.433013 |
    +----+--------------------+----------+
    3 rows in set (0.003 sec)
    ```

With `COSINE`, document 2 ranks ahead of document 1. With `EUCLIDEAN`, the order is reversed. Document 2 points in almost exactly the same direction as the query vector but is much shorter, so cosine distance treats it as very close while Euclidean distance does not. The stored vectors here are not unit length, so the two metrics are not equivalent. Choose the metric that matches how your embedding model was trained, and normalize your vectors if you want direction alone to decide the ranking.


## Handle invalid input

Keep the following behaviors in mind when you build queries:

* Vectors with different dimensions cause an error.
* If either vector is `NULL`, `DISTANCE()` returns `NULL`.
* For `COSINE`, a zero vector such as `[0, 0, 0]` returns `NULL` because cosine distance is undefined for a zero vector.
* An unsupported or misspelled metric name causes an error.
* Metric names are case-insensitive, so `cosine` and `COSINE` are equivalent.

For complete argument and return-value details, see [DISTANCE() Function](distance-function.md).

## Clean up

When you finish the quickstart, optionally remove the sample database and all of its contents:

```sql
DROP DATABASE IF EXISTS testdb;
```

## See also

* [DISTANCE() Function](distance-function.md)
* [The VECTOR Type](vector.md)
