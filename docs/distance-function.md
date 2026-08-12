# DISTANCE() Function

The `DISTANCE()` function computes the distance between two `VECTOR` values to enable similarity searches and other vector-based operations.

A vector is an ordered list of numeric values, such as `[1, 2, 3]`. The distance between two vectors is a numeric value that indicates how similar the vectors are.

A distance metric defines how the function calculates this value. Different metrics compare properties such as vector values, direction, or magnitude. In general, a smaller distance indicates greater similarity.

`VECTOR_DISTANCE()` is a synonym for `DISTANCE()` and provides compatibility with MySQL 9.x syntax. Both functions accept the same arguments and return the same result.

## Syntax

```sql
DISTANCE(vector_a, vector_b, metric)
VECTOR_DISTANCE(vector_a, vector_b, metric)
```

Both functions require exactly three arguments.

## Arguments

`DISTANCE()` accepts the following arguments:

* `vector_a` and `vector_b` specify the vectors to compare. Both arguments must be values of `VECTOR` data type or binary strings that represent float vectors. Other data types cause an error. The vectors must have the same dimension. A dimension mismatch causes an error.

* `metric` specifies the distance metric. Use a constant string or hex literal that resolves to a supported metric. Metric names are case-insensitive. You cannot use a column reference or a computed expression, such as `CONCAT()`, for this argument.

For a binary-string vector, the byte length must be a multiple of 4 because each vector element is a 4-byte single-precision floating-point value. An invalid byte length causes an error.

The `metric` argument cannot be `NULL`. An unsupported metric name causes an error.

## Supported distance metrics

The following distance metrics are supported:

| Metric              | Description                                                                                                                                                                                                                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `EUCLIDEAN`         | Measures the straight-line distance between two vectors (L2 distance). The result is non-negative. A value of `0` means the vectors are identical. Lower values indicate greater similarity.                                                                                                                        |
| `EUCLIDEAN_SQUARED` | Calculates the square of the Euclidean distance without the square root calculation. Use this metric when you need to rank vectors by distance but do not need the actual Euclidean distance. The result is non-negative. A value of `0` means the vectors are identical. Lower values indicate greater similarity. |
| `COSINE`            | Measures the difference in direction between two vectors rather than their magnitude. For real-valued vectors, the result ranges from `0` to `2`. A value of `0` indicates the same direction, while `2` indicates opposite directions.                                                                             |
| `DOT`               | Calculates the negative inner product (dot product). The dot product multiplies corresponding elements from the two vectors and adds the results. Lower returned values indicate greater similarity.                                                                                                                |
| `MANHATTAN`         | Adds the absolute differences between corresponding vector elements (L1 distance). The result is non-negative. A value of `0` means the vectors are identical. Lower values indicate greater similarity.                                                                                                            |

## Return value

`DISTANCE()` returns a `DOUBLE` value that represents the result of the selected distance metric. `DOUBLE` is a floating-point numeric data type that can represent fractional values, for example, `5.196152`.

If either input vector is `NULL`, `DISTANCE()` returns `NULL`.

With the `COSINE` metric, `DISTANCE()` returns `NULL` if either vector has a zero L2 norm (magnitude), such as `[0, 0, 0]`. Cosine distance is undefined for a zero vector.

The result is nullable regardless of whether the input columns allow `NULL`. When you use `DISTANCE()` with `CREATE TABLE ... SELECT`, MySQL creates the result column with the `DOUBLE` data type.

## Examples

### Calculate the distance between two vectors

`TO_VECTOR()` converts the string representation of a vector to a `VECTOR` value.

The following example calculates the Euclidean distance between two vectors:

```sql
SELECT DISTANCE(
    TO_VECTOR('[1, 2, 3]'),
    TO_VECTOR('[4, 5, 6]'),
    'EUCLIDEAN'
) AS distance;
```

The result is a `DOUBLE` value:

??? example "Expected output"

    ```text
    +-------------------+
    | distance          |
    +-------------------+
    | 5.196152422706632 |
    +-------------------+
    ```

### Use another distance metric

Specify a different metric in the third argument to change how `DISTANCE()` compares the vectors.

The following example calculates the cosine distance:

```sql
SELECT DISTANCE(
    TO_VECTOR('[1, 2, 3]'),
    TO_VECTOR('[4, 5, 6]'),
    'COSINE'
) AS distance;
```

### Find similar vectors

Assume that the `documents` table contains an `embedding` column defined as `VECTOR(3)`.

Use `DISTANCE()` in an `ORDER BY` clause to rank stored vectors by their distance from a query vector. Sorting by distance in ascending order places the closest vectors first.

The following query uses cosine distance to return the five closest vectors:

```sql
SELECT id,
       DISTANCE(
           embedding,
           TO_VECTOR('[0.1, 0.2, 0.3]'),
           'COSINE'
       ) AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

`VECTOR_DISTANCE()` produces the same result:

```sql
SELECT id,
       VECTOR_DISTANCE(
           embedding,
           TO_VECTOR('[0.1, 0.2, 0.3]'),
           'COSINE'
       ) AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

## See also

* [The VECTOR Type](vector.md)
