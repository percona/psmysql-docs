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

Different distance metrics compare vectors in different ways. The [DISTANCE() quickstart](quickstart-distance.md) runs every supported metric against the same stored vector and the same query vector. For arguments, return values, and metric definitions, see [DISTANCE() Function](distance-function.md).

## Limitations

* `TO_VECTOR()` rejects very small values close to zero, such as `1e-40`, and returns the `ER_TO_VECTOR_CONVERSION` error. To store such a value, insert the vector as a binary string instead of a string representation.

* With `INSERT IGNORE` or a non-strict SQL mode, a vector with more elements than the column dimension does not cause an error. The server stores an empty value instead. Use strict SQL mode and plain `INSERT` statements for `VECTOR` columns.

* In a `MEMORY` table, place `VECTOR` columns after all columns that belong to a key. If a `VECTOR` column comes before the last key column, `CREATE TABLE` fails with the `ER_TABLE_CANT_HANDLE_BLOB` error.

## See also

* [Get started with DISTANCE()](quickstart-distance.md)
* [DISTANCE() Function](distance-function.md)
* [Vector indexes](vector-index.md)
