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

The calculation is `sqrt((0.3333333333 - 0.2857142857)^2 + (0.6666666667 - 0.4285714286)^2 + (0.6666666667 - 0.8571428571)^2) = sqrt(0.0476190476^2 + 0.2380952381^2 + (-0.1904761904)^2) = sqrt(0.0952380952) ≈ 0.3086067`.

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

The calculation is `(0.3333333333 - 0.2857142857)^2 + (0.6666666667 - 0.4285714286)^2 + (0.6666666667 - 0.8571428571)^2 = 0.0022675737 + 0.0566893424 + 0.0362811791 = 0.0952380952 ≈ 0.0952381`. The result ranges from `0` (same direction) through `1` (orthogonal) to `2` (opposite directions).


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

Because both vectors are already unit length, cosine similarity here is the raw inner product: `0.3333333333 × 0.2857142857 + 0.6666666667 × 0.4285714286 + 0.6666666667 × 0.8571428571 = 0.0952380952 + 0.2857142857 + 0.5714285714 = 0.9523809524 ≈ 0.952381`. Cosine distance is `1 - 0.9523809524 = 0.0476190476 ≈ 0.047619`.

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

The inner product is `0.3333333333 × 0.2857142857 + 0.6666666667 × 0.4285714286 + 0.6666666667 × 0.8571428571 = 0.0952380952 + 0.2857142857 + 0.5714285714 = 0.9523809524 ≈ 0.952381`, and DISTANCE() returns its negative: `-0.952381`.

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

The calculation is `|0.3333333333 - 0.2857142857| + |0.6666666667 - 0.4285714286| + |0.6666666667 - 0.8571428571| = 0.0476190476 + 0.2380952381 + 0.1904761904 = 0.4761904761 ≈ 0.476190`.

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

Lower distance values represent closer matches. The exact query vector ranks first because its cosine distance is `0`. The `Opposite document` row (id 3) does not appear because it is the farthest from the query vector. Its cosine distance is about `1.975`, the largest of the four rows, so `LIMIT 3` excludes it. Remove `LIMIT 3` to list all four rows.

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

With `COSINE`, `Nearby document` ranks ahead of `Example document`. With `EUCLIDEAN`, the order is reversed. `Nearby document` points in almost exactly the same direction as the query vector but is much shorter, so cosine distance treats it as very close while Euclidean distance does not. 

The `Opposite document` row ranks last under both metrics, with a Euclidean distance of about `1.556`, so `LIMIT 3` excludes it here as well. The stored vectors here are not unit length, so the two metrics are not equivalent. Choose the metric that matches how your embedding model was trained, and normalize your vectors if you want direction alone to decide the ranking.

### List all rows under both metrics

To see every row under both metrics in one result, select both distances and remove `LIMIT`:

```sql
SELECT id,
       content,
       DISTANCE(embedding, TO_VECTOR('[0.5, 0.625, 0.75]'), 'COSINE') AS cosine_distance,
       DISTANCE(embedding, TO_VECTOR('[0.5, 0.625, 0.75]'), 'EUCLIDEAN') AS euclidean_distance
FROM documents
ORDER BY id;
```

??? example "Expected output"

    ```text
    +----+--------------------+-----------------------+---------------------+
    | id | content            | cosine_distance       | euclidean_distance  |
    +----+--------------------+-----------------------+---------------------+
    |  1 | Example document   |  0.012341670683137851 | 0.19094064094969537 |
    |  2 | Nearby document    | 0.0053884541273605535 |  0.4330127018922193 |
    |  3 | Opposite document  |    1.9746318461970762 |  1.5562374497485916 |
    |  4 | Exact query vector |                     0 |                   0 |
    +----+--------------------+-----------------------+---------------------+
    4 rows in set (0.005 sec)
    ```

The `Opposite document` row has the largest distance under both metrics, `1.9746318461970762` for `COSINE` and `1.5562374497485916` for `EUCLIDEAN`. It ranks last in both searches, so `LIMIT 3` excludes it.

## Compare raw and normalized vectors

`COSINE` ignores the length of the vectors, but `EUCLIDEAN` does not. When two texts cover the same topic but differ greatly in length, the raw Euclidean distance can be large even though the cosine distance is close to `0`. Normalizing both vectors to length `1` removes the difference.

The following example stores term-count vectors for a long article and a short summary of the same article. The eight dimensions count the words photosynthesis, light, chlorophyll, plant, energy, carbon, oxygen, and glucose. The article vector is about 21 times longer than the summary vector, but the word proportions are almost the same. The `normalized` rows hold the same two vectors divided by their own lengths, `sqrt(54994) ≈ 234.508` and `sqrt(123) ≈ 11.0905`.

These vectors are simplified term counts that illustrate the length effect. Embeddings from a model typically have hundreds or thousands of dimensions, with smaller elements that can be positive or negative, so the distances between texts on the same topic are usually larger than the values in this example.

The statements use the `testdb` database from the first section:

```sql
CREATE TABLE doc_vectors (
    doc VARCHAR(10),
    kind VARCHAR(12),
    embedding VECTOR(8),
    PRIMARY KEY (doc, kind)
);

INSERT INTO doc_vectors (doc, kind, embedding)
VALUES
    ('article', 'raw', TO_VECTOR('[120, 85, 40, 150, 70, 45, 38, 30]')),
    ('summary', 'raw', TO_VECTOR('[6, 4, 2, 7, 3, 2, 2, 1]')),
    ('article', 'normalized', TO_VECTOR('[0.5117096314, 0.3624609889, 0.1705698771, 0.6396370393, 0.2984972850, 0.1918911118, 0.1620413833, 0.1279274079]')),
    ('summary', 'normalized', TO_VECTOR('[0.5410017808, 0.3606678539, 0.1803339269, 0.6311687443, 0.2705008904, 0.1803339269, 0.1803339269, 0.0901669635]'));
```

Compare the article with the summary using both metrics:

```sql
SELECT a.kind AS vector_type,
       DISTANCE(a.embedding, s.embedding, 'COSINE') AS cosine_distance,
       DISTANCE(a.embedding, s.embedding, 'EUCLIDEAN') AS euclidean_distance
FROM doc_vectors AS a
JOIN doc_vectors AS s
  ON s.kind = a.kind
 AND a.doc = 'article'
 AND s.doc = 'summary'
ORDER BY a.kind DESC;
```

??? example "Expected output"

    ```text
    +-------------+-----------------------+---------------------+
    | vector_type | cosine_distance       | euclidean_distance  |
    +-------------+-----------------------+---------------------+
    | raw         | 0.0018530644915591976 |   223.4390297150433 |
    | normalized  |  0.001853019054323557 | 0.06087799819964219 |
    +-------------+-----------------------+---------------------+
    2 rows in set (0.010 sec)
    ```

For the `raw` rows, the dot product of `[120, 85, 40, 150, 70, 45, 38, 30]` and `[6, 4, 2, 7, 3, 2, 2, 1]` is `2596`, and the vector lengths are `sqrt(54994) ≈ 234.508` and `sqrt(123) ≈ 11.0905`. The cosine distance is `1 - 2596 / (sqrt(54994) × sqrt(123)) ≈ 0.0018530645`, which matches `0.0018530644915591976`. The element differences are `114, 81, 38, 143, 67, 43, 36, 29`, so the Euclidean distance is `sqrt(49925) ≈ 223.4390297`, which matches `223.4390297150433`.

For the `normalized` rows, both vectors have length `1`, so the cosine distance is `1 - dot product`. The dot product of the two normalized vectors is approximately `0.998147`, so the cosine distance is approximately `0.001853`, which matches `0.001853019054323557` to six decimal places. The element differences are `-0.0293, 0.0018, -0.0098, 0.0085, 0.0280, 0.0116, -0.0183, 0.0378`, so the Euclidean distance is `sqrt(0.0037061290) ≈ 0.0608780`, which matches `0.06087799819964219`.

The `normalized` cosine distance differs from the `raw` value in the sixth significant digit (`0.001853019…` compared with `0.001853064…`). The vector elements are stored as 4-byte floats, and the calculation subtracts a value close to `1` from `1`, so small rounding differences become visible. For more information, see the [precision note](#create-the-sample-database-and-table).

The cosine distance is nearly the same for both rows because cosine distance divides out the vector length. The raw Euclidean distance reflects the length difference rather than the topic. Use `COSINE`, or normalize your vectors before you use `EUCLIDEAN`, when vector length does not carry meaning for your data.

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