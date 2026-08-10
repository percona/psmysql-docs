# The VECTOR Type

The `VECTOR` data type stores an ordered list of numeric values, called a vector, in a table column. For example, `[0.1, 0.2, 0.3]` represents a vector with three values.

Vectors can represent numerical features, such as embeddings used for similarity search and machine learning. Each element in a `VECTOR` value uses a single-precision floating-point number.

## Syntax

```sql
VECTOR(N)
```

`N` specifies the number of elements, or dimensions, in the vector. All values stored in the column must have the same number of dimensions.

For example, the following statement creates an `embedding` column that stores three-dimensional vectors:

```sql
CREATE TABLE documents (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    embedding VECTOR(3)
);
```

A `VECTOR(3)` value contains exactly three elements, such as `[0.1, 0.2, 0.3]`. A vector with two or four elements does not match the column dimension.

## Store vector values

Use `TO_VECTOR()` to convert the string representation of a vector to a `VECTOR` value.

The following statement inserts a three-dimensional vector into the `embedding` column:

```sql
INSERT INTO documents (id, title, embedding)
VALUES (
    1,
    'Example document',
    TO_VECTOR('[0.1, 0.2, 0.3]')
);
```

The number of elements passed to `TO_VECTOR()` must match the dimension of the `VECTOR` column.

## Retrieve vector values

Use a `SELECT` statement to retrieve vector values:

```sql
SELECT id, embedding
FROM documents;
```

## Compare vectors

Vector applications often compare vectors to determine how similar they are. The result of a comparison is a numeric distance between the vectors.

Use `DISTANCE()` to calculate this distance with a supported distance metric. For example:

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.1, 0.2, 0.3]'),
    'COSINE'
) AS distance
FROM documents;
```

Different distance metrics compare vectors in different ways. For details about the supported metrics, arguments, and return values, see [DISTANCE() Function](distance-function.md).

## See also

- [DISTANCE() Function](distance-function.md)
