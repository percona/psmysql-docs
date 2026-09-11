# The VECTOR Type

The `VECTOR` data type stores an ordered list of numeric values, called a vector, in a table column. For example, `[0.1, 0.3, 0.2]` represents a vector with three elements.

Vectors can represent numerical features, such as embeddings used for similarity search and machine learning. Each element in a `VECTOR` value uses a single-precision floating-point number.

## Syntax

```sql
VECTOR(N)
```

`N` specifies the dimension of the `VECTOR` column and defines the maximum number of elements that a stored vector can contain.

For example, the following statement creates an `embedding` column with a dimension of three:

```sql
CREATE TABLE documents (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    embedding VECTOR(3)
);
```

A `VECTOR(3)` column can store a vector with up to three elements. For example, it accepts vectors with two or three elements but rejects a vector with four elements.

Using the same number of elements as the declared dimension is strongly recommended.

## Store vector values

Use `TO_VECTOR()` to convert the string representation of a vector to a `VECTOR` value.

The following statement inserts a three-element vector into the `embedding` column:

```sql
INSERT INTO documents (id, title, embedding)
VALUES (
    1,
    'Example document',
    TO_VECTOR('[0.1, 0.3, 0.2]')
);
```

The number of elements in the vector must not exceed the dimension specified for the `VECTOR` column.

## Retrieve vector values

Use a `SELECT` statement to retrieve vector values:

```sql
SELECT id, embedding
FROM documents;
```

## Compare vectors

Vector applications often compare vectors to determine how similar they are. The result of a comparison is a numeric distance between the vectors.

Use `DISTANCE()` to calculate the distance between two vectors with a supported distance metric. The two vector values passed to `DISTANCE()` must contain the same number of elements. A mismatch causes an error.

For example:

```sql
SELECT DISTANCE(
    embedding,
    TO_VECTOR('[0.1, 0.3, 0.2]'),
    'COSINE'
) AS distance
FROM documents;
```

Different distance metrics compare vectors in different ways. For details about supported metrics, arguments, and return values, see [DISTANCE() Function](distance-function.md).

## See also

* [DISTANCE() Function](distance-function.md)
