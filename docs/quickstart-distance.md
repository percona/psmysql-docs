# Get started with DISTANCE()

This quickstart compares one stored vector with one query vector using every distance metric that `DISTANCE()` supports. The metric examples share one table and the same two unit-length vectors, `[0.3333333333, 0.6666666667, 0.6666666667]` and `[0.2857142857, 0.4285714286, 0.8571428571]`, so the metric is what changes the result.

The supported metrics are:

* [`EUCLIDEAN`](#euclidean-distance)
* [`EUCLIDEAN_SQUARED`](#euclidean-squared-distance)
* [`COSINE`](#cosine-distance)
* [`DOT`](#dot-distance)
* [`MANHATTAN`](#manhattan-distance)

You need access to a Percona Server for MySQL {{vers}} server and an account that can create a database and tables. For arguments and return values, see [DISTANCE() Function](distance-function.md).


## Create the sample database and table

The following statements create and select a dedicated `distance_quickstart` database so that the examples do not modify a table in your current database. If that database already exists, either [remove it](#clean-up) or use another database name.

`TO_VECTOR()` converts the string representation of a vector to a `VECTOR` value. The statements also create a `documents` table and store `[0.3333333333, 0.6666666667, 0.6666666667]` in the `embedding` column:

```sql

DROP DATABASE IF EXISTS testdb;

CREATE DATABASE testdb CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE testdb;

DROP TABLE IF EXISTS documents;

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

`EUCLIDEAN_SQUARED` returns the square of the Euclidean distance. This metric is a Percona Server extension.

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

The calculation is `(1/21)^2 + (5/21)^2 + (4/21)^2 = 42/441 = 2/21 ≈ 0.0952381`.

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

For unit-length vectors, Euclidean distance is a monotonic function of cosine similarity, so `EUCLIDEAN` and `COSINE` typically rank matches the same way, which is why embeddings are often normalized before a metric is chosen.

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

In a similarity search, a table contains multiple embeddings. Add three more documents to the sample table:

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
