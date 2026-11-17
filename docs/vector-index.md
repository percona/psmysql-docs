# Vector indexes

--8<--- "tech.preview.md:5:5"

A vector index speeds up similarity search on a `VECTOR` column. Without an index, a query such as `ORDER BY DISTANCE(...) LIMIT 10` computes the distance to every row in the table and then sorts the results, so the query gets slower as the table grows. With a vector index, the server compares the query vector with only a small part of the table, so the query stays fast on large tables.

Percona Server for MySQL implements vector indexes in InnoDB with the Hierarchical Navigable Small World (HNSW) algorithm. You store embeddings next to your business data and query both with standard SQL. Vector indexes follow the same transaction rules as any other InnoDB index. You do not need a separate vector database or a pipeline to keep two systems in sync.

## Version changes

Percona Server for MySQL 9.7.4-4 introduces vector indexes as a tech preview feature.

## How a vector index works

An HNSW index organizes vectors into a layered graph in which each vector links to its closest neighbors. A search starts at the top layer and moves through the graph toward the vectors closest to the query vector. The search visits only a small part of the table, so response time stays low as the table grows.

HNSW performs an *approximate nearest neighbor* (ANN) search. The index returns vectors that are very close to the query vector, but the results can occasionally differ from an exact search that compares every row. *Recall* measures the share of true nearest neighbors that the index finds. You control the balance between recall and speed with the [index options](#index-options) and the [`innodb_hnsw_ef_search`](#innodb_hnsw_ef_search) variable.

The server keeps the graph in memory and stores a copy in InnoDB. After a restart, the server loads the graph gradually. Each query loads only the parts of the graph that the search needs. The [`innodb_hnsw_max_memory`](#innodb_hnsw_max_memory) variable limits the total memory that all graphs use.

!!! note

    Each vector index must fit in memory. The current implementation does not support indexes larger than the memory limit you configure.

## Requirements

A table that has a vector index must meet the following requirements:

* The table uses the InnoDB storage engine.

* The table has a single-column primary key of type `BIGINT UNSIGNED`.

* The indexed column has the `VECTOR(N)` data type and the `NOT NULL` attribute.

* The table has only one vector index.

* The table is a regular table. Partitioned tables and temporary tables do not support vector indexes.

* No foreign key with `ON DELETE CASCADE` or `ON UPDATE CASCADE` references the table.

The server rejects a `CREATE TABLE` or `ALTER TABLE` statement that does not meet these requirements and returns an `ER_NOT_SUPPORTED_YET` error that names the reason.

## Create a vector index

You can add a vector index when you create a table, add the index to an existing table with `CREATE VECTOR INDEX`, or add the index with `ALTER TABLE`. Each form requires the `TYPE hnsw` clause.

### Syntax

```sql
-- In CREATE TABLE
VECTOR {KEY | INDEX} index_name (column_name) TYPE hnsw [(option = value [, option = value] ...)]

-- As a separate statement
CREATE VECTOR INDEX index_name ON table_name (column_name) TYPE hnsw [(option = value [, ...])]

-- In ALTER TABLE
ALTER TABLE table_name ADD VECTOR {KEY | INDEX} index_name (column_name) TYPE hnsw [(option = value [, ...])]
```

`USING hnsw` works as a synonym for `TYPE hnsw`. `SHOW CREATE TABLE` displays the `USING` form.

### Create a table with a vector index

The examples on this page use the following table. The `embedding` column holds three-dimensional vectors to keep the examples short. Embedding models typically produce vectors with hundreds or thousands of dimensions.

```sql
CREATE TABLE documents (
    id        BIGINT UNSIGNED PRIMARY KEY,
    title     VARCHAR(100) NOT NULL,
    category  VARCHAR(20)  NOT NULL,
    embedding VECTOR(3)    NOT NULL,
    VECTOR KEY idx_embedding (embedding) TYPE hnsw (M = 16)
);
```

Insert sample rows:

```sql
INSERT INTO documents (id, title, category, embedding) VALUES
    (1, 'Install guide',     'docs', TO_VECTOR('[0.1, 0.2, 0.3]')),
    (2, 'Upgrade guide',     'docs', TO_VECTOR('[0.2, 0.1, 0.4]')),
    (3, 'Release notes',     'news', TO_VECTOR('[0.9, 0.8, 0.1]')),
    (4, 'Backup tutorial',   'docs', TO_VECTOR('[0.4, 0.5, 0.6]')),
    (5, 'Product launch',    'news', TO_VECTOR('[0.15, 0.25, 0.3]')),
    (6, 'Security advisory', 'news', TO_VECTOR('[0.1, 0.3, 0.3]'));
```

`SHOW CREATE TABLE` displays every index option, including the options you did not set:

```sql
SHOW CREATE TABLE documents\G
```

??? example "Expected output"

    ```{.text .no-copy}
    *************************** 1. row ***************************
           Table: documents
    Create Table: CREATE TABLE `documents` (
      `id` bigint unsigned NOT NULL,
      `title` varchar(100) NOT NULL,
      `category` varchar(20) NOT NULL,
      `embedding` vector(3) NOT NULL,
      PRIMARY KEY (`id`),
      VECTOR KEY `idx_embedding` (`embedding`) USING `hnsw` (`M`=16, `ef_construction`=200, `metric`=`euclidean`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    ```

The server saves the full set of options with the index. A dump of the table recreates the index with the same options, even on a server version with different defaults.

### Add a vector index to an existing table

Use `CREATE VECTOR INDEX` or `ALTER TABLE`:

```sql
CREATE VECTOR INDEX idx_embedding ON documents (embedding) TYPE hnsw (M = 16, metric = cosine);
```

```sql
ALTER TABLE documents ADD VECTOR INDEX idx_embedding (embedding) TYPE hnsw (M = 16, metric = cosine);
```

The first vector index on a table rebuilds the table and then builds the graph from the existing rows. The build reads the table with several threads. The [`innodb_parallel_read_threads` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/9.7/en/innodb-parameters.html#sysvar_innodb_parallel_read_threads) variable sets the number of threads. Plan the operation for a maintenance window on a large table. For the supported algorithms and lock levels, see [Change or drop a vector index](#change-or-drop-a-vector-index).

### Load large data sets

For a large data set, load the rows first and add the vector index afterward. Avoid inserting a large number of rows into a table that already has a vector index.

```sql
CREATE TABLE documents (
    id        BIGINT UNSIGNED PRIMARY KEY,
    title     VARCHAR(100) NOT NULL,
    category  VARCHAR(20)  NOT NULL,
    embedding VECTOR(3)    NOT NULL
);

-- Load the data, for example with LOAD DATA or multi-row INSERT statements

ALTER TABLE documents ADD VECTOR INDEX idx_embedding (embedding) TYPE hnsw (M = 16);
```

An index build over existing rows is much faster than adding the same rows one at a time:

* The build compares vectors in several threads at once, so the build uses all available CPU cores. The [`innodb_parallel_read_threads` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/9.7/en/innodb-parameters.html#sysvar_innodb_parallel_read_threads) variable controls the number of threads.

* The build writes the finished index to disk in one pass. Each row-by-row insert also updates many existing entries in the index, which causes many small writes.

After the build, the server does not keep the graph in memory, and `Innodb_hnsw_memory_used` shows `0`. The first queries load the graph gradually, so these queries run slower than later ones. Before you measure performance or open the table to production traffic, run a representative set of queries to warm up the index.

!!! note

    If your vectors are very regular, for example counters or sequences, a parallel build can leave some rows unreachable. See [Indexes on very regular data](#indexes-on-very-regular-data).

## Index options

Set index options in the parentheses after `TYPE hnsw`. Option names are case-insensitive. Write option values as numbers or unquoted identifiers: `metric = cosine` is valid, `metric = 'cosine'` causes a syntax error. Each option can appear only once.

| Option | Default | Range | Description |
| --- | --- | --- | --- |
| `M` | `25` | `2` to `200` | The maximum number of neighbors that each vector links to in the graph. A larger value improves recall and helps with high-dimensional data, but uses more memory and makes inserts slower. |
| `ef_construction` | `200` | `1` to `4096` | The number of candidate neighbors that the server examines when the server adds a vector to the graph. A larger value builds a higher-quality graph and improves recall, but makes inserts and index builds slower. |
| `metric` | `euclidean` | `euclidean`, `cosine` | The distance metric that the graph uses. Choose the metric that matches your embedding model. |

!!! important

    The graph quality depends on `M` and `ef_construction` at the time the server inserts each vector. If you build the graph with low values, a higher [`innodb_hnsw_ef_search`](#innodb_hnsw_ef_search) value later does not make up for the lower quality. To change `M`, `ef_construction`, or `metric`, drop and re-create the index.

### Choose a metric

The `metric` option decides which `DISTANCE()` metric the index can serve:

| Index `metric` | Queries that use the index |
| --- | --- |
| `euclidean` | `DISTANCE(..., 'EUCLIDEAN')` and `DISTANCE(..., 'EUCLIDEAN_SQUARED')` |
| `cosine` | `DISTANCE(..., 'COSINE')` |

A query with any other metric, such as `DOT` or `MANHATTAN`, runs as a full table scan with a sort.

A `cosine` index does not accept a zero vector, such as `[0, 0, 0]`, because cosine distance has no defined value for a vector without magnitude. An `INSERT` or `UPDATE` with a zero vector, or an index build over a table that contains one, fails with the `ER_VECTOR_INDEX_WRONG_VALUE` error.

## Search with a vector index

The optimizer uses a vector index for a query that has all of the following properties:

* The query reads from one table. A query with a join does not use the vector index.

* The query has one `ORDER BY` expression: a `DISTANCE()` or `VECTOR_DISTANCE()` call on the indexed column and a constant query vector. The arguments can appear in either order.

* The `ORDER BY` uses ascending order.

* The query has a `LIMIT` clause.

* The `DISTANCE()` metric matches the index `metric`. See [Choose a metric](#choose-a-metric).

The following query returns the three documents closest to the query vector:

```sql
SELECT id,
       title,
       CAST(DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN') AS DECIMAL(8, 6)) AS distance
FROM documents
ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN')
LIMIT 3;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+-------------------+----------+
    | id | title             | distance |
    +----+-------------------+----------+
    |  1 | Install guide     | 0.050000 |
    |  5 | Product launch    | 0.086603 |
    |  6 | Security advisory | 0.111803 |
    +----+-------------------+----------+
    ```

You can also sort by a column alias for the distance expression:

```sql
SELECT id, DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN') AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

### Combine vector search with filters

Add a `WHERE` clause to filter the results by business data. The server applies the filter after the vector search:

1. The server reads rows from the vector index, starting with the closest.

2. The server skips the rows that do not match the filter.

3. The search continues until the query has as many rows as `LIMIT` requests, or until no rows remain.

If enough rows match the filter, the query returns the full `LIMIT` number of rows.

```sql
SELECT id, title
FROM documents
WHERE category = 'docs'
ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN')
LIMIT 3;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+-----------------+
    | id | title           |
    +----+-----------------+
    |  1 | Install guide   |
    |  2 | Upgrade guide   |
    |  4 | Backup tutorial |
    +----+-----------------+
    ```

If few rows match the filter, the server reads many rows before the query has enough results, and the query slows down. If a filter matches only a small share of the table, create a regular index on the filtered column and skip the vector index. The server then reads the matching rows through the regular index and sorts them by exact distance:

```sql
CREATE INDEX idx_category ON documents (category);

SELECT id, title
FROM documents IGNORE INDEX FOR ORDER BY (idx_embedding)
WHERE category = 'docs'
ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN')
LIMIT 3;
```

`HAVING` clauses and views that contain the distance expression also work with the vector index.

### Check whether a query uses the vector index

Run `EXPLAIN`. In the traditional output, the `type` column shows `vector_ann`, the `key` column shows the vector index, and the `Extra` column does not contain `Using filesort`. The index already returns rows in order of distance, so the query needs no sort.

`EXPLAIN FORMAT=TREE` shows a `Vector index search` step:

```sql
EXPLAIN FORMAT=TREE
SELECT id, title
FROM documents
WHERE category = 'docs'
ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN')
LIMIT 3;
```

??? example "Expected output"

    The following output omits cost estimates:

    ```{.text .no-copy}
    -> Limit: 3 row(s)
        -> Filter: (documents.category = 'docs')
            -> Vector index search on documents using idx_embedding (embedding = to_vector('[0.1, 0.2, 0.35]'))
    ```

If the plan shows `Table scan` and `Sort` instead, the query does not use the vector index. The next section lists the common reasons.

### Queries that do not use the vector index

The optimizer uses the vector index only for `ORDER BY DISTANCE(...) LIMIT n` queries. The following queries read the whole table, sort the rows, and return exact results:

| Query | Reason |
| --- | --- |
| `ORDER BY DISTANCE(...)` without `LIMIT` | The query asks for every row in exact order. |
| `ORDER BY DISTANCE(...) DESC LIMIT n` | An HNSW index finds the nearest vectors, not the farthest. |
| `WHERE DISTANCE(...) < 0.5` | A range condition must return every qualifying row. An approximate search can miss some of them. |
| A `DISTANCE()` metric that differs from the index `metric` | The graph orders vectors by a different distance. |
| A query vector that is not constant, for example another column | The search needs a fixed starting point. |
| A `NULL` query vector | `NULL` defines no order. |
| A query with `GROUP BY`, `DISTINCT`, a window function, or `MATCH()` | The query needs every row, or the full-text search must read the table. |
| A query with a join | The vector index serves single-table queries only. |

To compare the approximate result with the exact result, force a full scan with `IGNORE INDEX` or `IGNORE INDEX FOR ORDER BY`:

```sql
SELECT id, title
FROM documents IGNORE INDEX (idx_embedding)
ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN')
LIMIT 3;
```

!!! note

    The vector index has no cost model. The optimizer chooses the index whenever the query matches the rules above, even on a small table or with a `LIMIT` value close to the number of rows. The server does not warn when an approximate result differs from the exact result.

## Tune search recall

The [`innodb_hnsw_ef_search`](#innodb_hnsw_ef_search) variable sets the minimum number of candidates that a search keeps while the search moves through the graph. The server uses the larger of `innodb_hnsw_ef_search` and the `LIMIT` value.

A larger value improves recall and makes queries slower. A smaller value makes queries faster and can reduce recall. The variable has session scope, so you can choose a different value for each workload:

```sql
-- Interactive search: favor speed
SET SESSION innodb_hnsw_ef_search = 40;

-- Batch job or evaluation: favor recall
SET SESSION innodb_hnsw_ef_search = 400;
```

To measure recall for your data, run a sample of queries twice: once with the index and once with `IGNORE INDEX`. Then compare the returned rows.

## Manage memory

The [`innodb_hnsw_max_memory`](#innodb_hnsw_max_memory) variable sets the upper limit, in bytes, for the memory that all vector index graphs on the server use together. The default value is 1 GiB.

When the graphs reach the limit, a statement that needs more memory fails with the following error, and the graph stays unchanged:

```{.text .no-copy}
ERROR HY000: Memory capacity of 1073741824 bytes for 'innodb_hnsw_max_memory' exceeded. The vector index graph was left unchanged. Raise innodb_hnsw_max_memory and retry.
```

The variable is dynamic. Raise the limit and run the statement again. You do not need to restart the server:

```sql
SET GLOBAL innodb_hnsw_max_memory = 4 * 1024 * 1024 * 1024;
```

To monitor memory usage, check the [`Innodb_hnsw_memory_used`](#innodb_hnsw_memory_used) status variable:

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_hnsw_memory_used';
```

The value has the following behavior:

* The value starts at `0` after a server restart, because the server loads graphs only when queries need them.

* The value grows as queries load graphs and as you insert or update rows.

* The value does not drop after `DELETE` or after a rolled-back `INSERT`, because the graph keeps those vectors. See [Modify indexed data](#modify-indexed-data).

* The value drops when you drop or rebuild an index, for example with `OPTIMIZE TABLE`, or when the server closes a table that no query uses.

* An index build that runs inside `ALTER TABLE` counts toward the limit until the build finishes.

* A table rebuild, such as `OPTIMIZE TABLE` or `ALTER TABLE ... FORCE`, can need up to twice the memory of the index. If the graph is already in memory, the server holds the old graph and the new graph at the same time. Right after a restart, the rebuild needs memory for one graph only.

* `FLUSH STATUS` does not reset the value.

`OPTIMIZE TABLE` reports a memory error as a row in its result set, with `Msg_type` set to `error`, and does not return an SQL error. Applications that check only for SQL errors do not detect the failure. Check the `Msg_type` column, or rebuild the table with `ALTER TABLE ... FORCE`, which returns an SQL error.

To estimate the memory an index needs, multiply the number of vectors by the vector size (4 bytes per dimension) and add space for the neighbor links, which grows with `M`. Allow extra memory for growth: see [Modify indexed data](#modify-indexed-data).

## Modify indexed data

You use regular `INSERT`, `UPDATE`, `DELETE`, and `REPLACE` statements on a table with a vector index. The server updates the index as part of each statement.

* `INSERT` adds a vector to the graph.

* `UPDATE` of the vector column or the primary key adds a new vector to the graph. The old vector stays in the graph.

* `DELETE` leaves the vector in the graph.

* A rolled-back `INSERT` or `UPDATE` leaves the new vector in the graph.

The server keeps old vectors because transactions that started earlier can still need them. Queries never return a deleted or outdated vector. Old vectors still take memory and disk space, so the index grows with the number of changes, not with the number of rows.

Old vectors also make the search less accurate: on a table with many updates or deletes, the index finds fewer of the true nearest neighbors over time. On a table with frequent updates or deletes, rebuild the index periodically to reclaim the space and restore accuracy:

```sql
OPTIMIZE TABLE documents;
```

`ALTER TABLE ... FORCE` also rebuilds the index.

### Vector dimensions

Every vector in an indexed column must have exactly the number of dimensions that the column defines. On a table with a vector index, `INSERT`, `UPDATE`, `REPLACE`, `INSERT IGNORE`, and `INSERT ... ON DUPLICATE KEY UPDATE` reject a vector with a different number of dimensions:

```{.text .no-copy}
ERROR HY000: Column 'embedding' has a vector without the 3 dimensions its vector index needs.
```

A `VECTOR(N)` column without a vector index accepts a vector with fewer than `N` dimensions. A vector with more than `N` dimensions fails with the `ER_DATA_TOO_LONG` error in both cases.

Avoid `INSERT IGNORE` and non-strict SQL modes for `VECTOR` columns. In these modes, a vector with more than `N` dimensions does not fail. The server stores an empty value instead. `INSERT ... SELECT` from a table with such a row fails, and a dump of the table fails to load.

If the table already contains shorter vectors, `ALTER TABLE ... ADD VECTOR INDEX` and `CREATE VECTOR INDEX` fail with the same error, and the server does not change the table. Before you add the index, find the affected rows. Each dimension takes 4 bytes, so a `VECTOR(3)` value takes 12 bytes:

```sql
SELECT id, LENGTH(embedding) / 4 AS dimensions
FROM documents
WHERE LENGTH(embedding) <> 3 * 4;
```

Correct or delete the returned rows, and then add the index.

`LOAD DATA` with `ALGORITHM = BULK` does not support tables with a vector index. Use regular `LOAD DATA` or `INSERT` statements instead.

## Indexes on very regular data

On very regular data, a vector index can silently miss some rows. Very regular data means vectors that lie close to a straight line, such as counters, sequences, calibration data, or grid-like data. The issue does not affect embeddings from real models, such as text or image embeddings.

The issue appears when several threads add vectors to the same graph at once:

* `ALTER TABLE ... ADD VECTOR INDEX` or `CREATE VECTOR INDEX` on a table that already has rows

* `OPTIMIZE TABLE` and other statements that rebuild the index

* `INSERT` statements from several sessions at the same time

In these cases, the index can lose track of a few percent of the rows. A search never returns such a row, even a search for the row's own vector. The server reports no error or warning, and `CHECK TABLE` reports no problem.

If your table stores very regular data, build and rebuild the index with one read thread:

```sql
SET SESSION innodb_parallel_read_threads = 1;
ALTER TABLE documents ADD VECTOR INDEX idx_embedding (embedding) TYPE hnsw;
```

Use the same setting before `OPTIMIZE TABLE` or `ALTER TABLE ... FORCE`. A single-threaded build takes longer on a large table. Concurrent inserts from several sessions can still cause the issue on such data, so load very regular data from one session where possible.

To check whether the index can find a row, search for the row's own vector with `LIMIT 1`. First, read the stored vector:

```sql
SELECT VECTOR_TO_STRING(embedding) FROM documents WHERE id = 1;
```

Then search with that value as a constant. The query must return the same row:

```sql
SELECT id FROM documents
ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.3]'), 'EUCLIDEAN')
LIMIT 1;
```

Run `EXPLAIN` on the search to confirm that the query uses the vector index. A query that does not use the index returns exact results and does not show the issue.

## Transactions and isolation

Vector search follows the same transaction rules as any other InnoDB query. A query returns only the rows that are visible to the current transaction:

* The query does not return rows from transactions that have not committed.

* If another transaction deletes a row and commits after your transaction starts, your transaction still sees the row, as in any other `REPEATABLE READ` query.

* A query returns an updated row once, at the distance of the row version the transaction sees.

* A rolled-back insert never appears in the results.

Each returned row matches what your transaction can see. However, the search is approximate, so two runs of the same query can return different rows:

* With `REPEATABLE READ`, other sessions can change the graph between two runs of the same search in one transaction. The second run can then return different rows.

* With `SERIALIZABLE`, the vector index does not lock the set of nearest neighbors. A concurrent transaction can insert a closer vector that a repeated query then returns.

The server does not return a warning in these cases. If your application needs a stable result set within a transaction, store the IDs that the first query returns and work with those IDs.

### Locking reads

A vector search can read more rows than the search returns. After an `UPDATE` of a vector, the graph keeps the old vector until you rebuild the index. When a search reaches an old vector, the server reads the row, finds that the row has changed, and skips the row.

In a locking read, such as `SELECT ... FOR UPDATE` or `SELECT ... FOR SHARE`, InnoDB locks each row that the search reads, as for any other locking read. The isolation level decides what happens to the lock on a skipped row:

* With `READ COMMITTED`, InnoDB releases the lock on a skipped row immediately.

* With `REPEATABLE READ`, InnoDB keeps the lock on a skipped row until the transaction ends.

Under `REPEATABLE READ`, a locking vector search can therefore hold locks on rows that the search did not return. These locks can cause the following effects:

* Other sessions wait to write to those rows, or receive a deadlock error.

* A `SELECT ... FOR UPDATE SKIP LOCKED` query in another session skips those rows and returns a more distant row instead.

* On a replica, the replication applier waits for those rows until the transaction ends.

To avoid these effects, use one of the following approaches:

* Run locking vector reads with `READ COMMITTED`:

    ```sql
    SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
    START TRANSACTION;
    SELECT id FROM documents
    ORDER BY DISTANCE(embedding, TO_VECTOR('[0.1, 0.2, 0.35]'), 'EUCLIDEAN')
    LIMIT 1
    FOR UPDATE SKIP LOCKED;
    -- process the row
    COMMIT;
    ```

* Rebuild the index regularly with `OPTIMIZE TABLE` on tables with frequent vector updates, so that the graph contains fewer old vectors.

## Change or drop a vector index

### Algorithms and locking

| Operation | Supported options |
| --- | --- |
| Add the first vector index to a table | `ALGORITHM=INPLACE` or `ALGORITHM=COPY`. Requires `LOCK=SHARED` or stricter. The server rebuilds the table. |
| Replace a vector index, for example `DROP INDEX` and `ADD VECTOR INDEX` with new options in one statement | `ALGORITHM=INPLACE` or `ALGORITHM=COPY`. Requires `LOCK=SHARED` or stricter. The server does not rebuild the table. |
| Drop the only vector index | Supports `LOCK=NONE`. The server rebuilds the table. |
| Any other `ALTER TABLE` on a table with a vector index | Requires `LOCK=SHARED` or stricter. `ALGORITHM=INSTANT` is not available. |

During an operation with `LOCK=SHARED`, other sessions can read the table but cannot write to the table.

On a table that also has a `FULLTEXT` index, InnoDB cannot rebuild the table in place. Adding the first vector index or dropping the last one then requires `ALGORITHM=COPY`, and `OPTIMIZE TABLE` runs as a copy as well.

`ALGORITHM=INPLACE` builds a vector index faster and produces a smaller index than `ALGORITHM=COPY`. Use `ALGORITHM=COPY` only when the server requires that algorithm.

### Change index options

To change `M`, `ef_construction`, or `metric`, replace the index in one statement:

```sql
ALTER TABLE documents
    DROP INDEX idx_embedding,
    ADD VECTOR INDEX idx_embedding (embedding) TYPE hnsw (M = 32, ef_construction = 400),
    ALGORITHM=INPLACE, LOCK=SHARED;
```

### Drop a vector index

```sql
DROP INDEX idx_embedding ON documents;
```

`DROP TABLE` and `TRUNCATE TABLE` also remove the index data. After `TRUNCATE TABLE`, the index is empty and ready for new rows.

## Storage

Each vector index uses one hidden InnoDB table that stores the graph. The name of the table follows the pattern `percona_vec_hnsw_<table_id>_<index_id>`. The table does not appear in `SHOW TABLES` or `INFORMATION_SCHEMA.TABLES`, but appears in `INFORMATION_SCHEMA.INNODB_TABLES`. InnoDB writes the table to the redo and undo logs like any other table, so crash recovery restores the index without extra steps.

A table with a vector index also has a hidden column. The column does not appear in `SELECT *` or `SHOW COLUMNS` output, and applications do not need to change.

The server reserves names that match the hidden table pattern. `CREATE TABLE` and `RENAME TABLE` fail with the `ER_WRONG_TABLE_NAME` error for such names.

## Replication and backup

The binary log contains only the changes to the base table. Each replica builds its own graph from the changes that the replica applies. Because each graph has a slightly different structure, the same approximate query can return different rows on the source and on a replica. Exact queries return the same results on every server.

Use row-based replication (`binlog_format=ROW`, the default) for tables with a vector index. A statement that changes data based on a vector search, such as `DELETE ... ORDER BY DISTANCE(...) LIMIT n`, can choose different rows on the replica if the server logs the statement instead of the changed rows.

`ALTER TABLE ... ADD VECTOR INDEX` takes about the same time on a replica as on the source, given similar hardware and settings. The statement blocks writes to the table on the source, so the replica does not need to apply concurrent changes while the replica builds the index.

To back up a server that has vector indexes, use Percona XtraBackup 9.7.2-3 or later. For details, see [the Percona XtraBackup documentation]().

`ALTER TABLE ... DISCARD TABLESPACE` and `ALTER TABLE ... IMPORT TABLESPACE` do not support tables with a vector index. `FLUSH TABLES ... FOR EXPORT` returns a warning for such tables, and you cannot import the exported files. To move a table with a vector index, use a logical dump or a physical backup of the whole server.

## Downgrade

Percona Server for MySQL versions without vector index support cannot read a vector index. If you start an earlier 9.7 release on a data directory that contains a vector index, the server crashes when a statement uses the table. The same crash happens on a clone recipient that runs an earlier release. A logical dump that contains vector index definitions fails to load on an earlier release with a syntax error.

To downgrade in place to a release without vector index support:

1. On the current server, drop every vector index:

    ```sql
    ALTER TABLE documents DROP INDEX idx_embedding;
    ```

    To list every vector index on the server, run:

    ```sql
    SELECT DISTINCT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE INDEX_TYPE = 'VECTOR';
    ```

2. Shut down the server with a slow shutdown, so that InnoDB writes all changes to the data files:

    ```sql
    SET GLOBAL innodb_fast_shutdown = 0;
    SHUTDOWN;
    ```

3. Start the earlier release on the same data directory.

Before you take a logical dump for an earlier release, drop the vector indexes the same way, or remove the `VECTOR KEY` clauses from the dump file.

If you already started an earlier release on a data directory with a vector index and that server no longer starts, start the newer release on the same data directory again. The newer release rolls back the incomplete statement. Then follow the steps above: drop every vector index, shut down with `innodb_fast_shutdown = 0`, and start the earlier release.

## Limitations

* Each table supports one vector index.

* The table must have a single-column `BIGINT UNSIGNED` primary key.

* The index supports only the `euclidean` and `cosine` metrics. The `DOT`, `EUCLIDEAN_SQUARED`, and `MANHATTAN` index metrics are not available. A `euclidean` index serves `EUCLIDEAN_SQUARED` queries.

* The server does not support vector indexes on:

    * Virtual generated columns
    * Partitioned tables
    * Temporary tables
    * Nullable columns

* The server does not support invisible vector indexes or the `KEY_BLOCK_SIZE` option on a vector index.

* Tables with a vector index cannot have `ON DELETE CASCADE` or `ON UPDATE CASCADE` foreign keys.

* `ALTER TABLE` with `ALGORITHM=INSTANT` or `LOCK=NONE` is not available while the table has a vector index.

* `DISCARD TABLESPACE` and `IMPORT TABLESPACE` are not available while the table has a vector index.

* An in-place downgrade to a release without vector index support requires that you drop all vector indexes first. See [Downgrade](#downgrade).

* `LOAD DATA` with `ALGORITHM = BULK` is not available for tables with a vector index.

* Each vector index must fit within [`innodb_hnsw_max_memory`](#innodb_hnsw_max_memory). The index does not support larger-than-memory graphs.

* Deleted and outdated vectors stay in the index until you rebuild the index. On a table with many updates or deletes, recall drops over time. A rebuild restores recall.

* In rare cases, the vector index cannot reach a row and never returns the row. A filtered search can then return no rows, even if a matching row exists. To get exact results for such a query, use `IGNORE INDEX`. A rebuild of the index can restore the row.

* Under `REPEATABLE READ`, a locking vector search keeps locks on rows that the search reads but does not return. See [Locking reads](#locking-reads).

* A `VECTOR(N)` column without a vector index accepts vectors with fewer than `N` dimensions. Such rows prevent you from adding a vector index until you correct them. See [Vector dimensions](#vector-dimensions).

* Only single-table queries use the vector index.

* On very regular data, such as vectors that lie close to a straight line, a parallel index build or concurrent inserts can leave some rows unreachable. See [Indexes on very regular data](#indexes-on-very-regular-data).

* The hypergraph optimizer does not use vector indexes. When you enable the hypergraph optimizer, vector queries run as a full table scan with a sort and return exact results.

* The same approximate query can return different results on a source and a replica.

## System variables

### `innodb_hnsw_ef_search`

| Option | Description |
| --- | --- |
| Command-line: | `--innodb-hnsw-ef-search` |
| Dynamic: | Yes |
| Scope: | Global, Session |
| Data type: | Integer |
| Default value: | `40` |
| Range: | `1` to `100000` |

Sets the minimum number of candidates that a vector index search keeps. The server uses the larger of this value and the query `LIMIT`. Larger values improve recall and increase query time. See [Tune search recall](#tune-search-recall).

### `innodb_hnsw_max_memory`

| Option | Description |
| --- | --- |
| Command-line: | `--innodb-hnsw-max-memory` |
| Dynamic: | Yes |
| Scope: | Global |
| Data type: | Integer |
| Default value: | `1073741824` (1 GiB) |
| Range: | `0` to `18446744073709551615` |
| Unit: | Bytes |

Sets the upper limit for the memory that all vector index graphs on the server use together. A statement that needs more memory after the server reaches the limit fails with an error. The value `0` removes the limit. See [Manage memory](#manage-memory).

## Status variables

### `Innodb_hnsw_memory_used`

| Option | Description |
| --- | --- |
| Scope: | Global |
| Data type: | Integer |
| Unit: | Bytes |

Shows the memory, in bytes, that all vector index graphs on the server currently use. The server compares this value with [`innodb_hnsw_max_memory`](#innodb_hnsw_max_memory). The value starts at `0` after a restart, and `FLUSH STATUS` does not reset the value. The value does not include the per-node lookup structures or temporary memory that searches use.

## Error messages

| Error | Cause |
| --- | --- |
| `ER_NO_INDEX_TYPE` | The vector index definition has no `TYPE` clause. |
| `ER_INDEX_TYPE_NOT_SUPPORTED` | The `TYPE` clause names an index type other than `hnsw`. |
| `ER_INDEX_MUST_HAVE_COMPATIBLE_COLUMN` | The indexed column does not have the `VECTOR` data type. |
| `ER_ILLEGAL_INDEX_CONSTRUCTION_PARAMETER` | The definition contains an unknown index option. |
| `ER_ILLEGAL_INDEX_CONSTRUCTION_PARAMETER_VALUE` | An index option has a value outside the allowed range. |
| `ER_DUPLICATE_INDEX_CONSTRUCTION_PARAMETER` | The definition sets the same option more than once. |
| `ER_NOT_SUPPORTED_YET` | The table or statement does not meet the [requirements](#requirements), or the definition uses an unsupported metric. |
| `ER_VECTOR_INDEX_WRONG_DIMENSIONS` | A vector does not have the number of dimensions that the column defines, either in a new row or in an existing row when you add the index. |
| `ER_VECTOR_INDEX_WRONG_VALUE` | A `cosine` index received a zero vector. |
| `ER_CAPACITY_EXCEEDED` | The vector index graphs reached the `innodb_hnsw_max_memory` limit. |
| `ER_ALTER_OPERATION_NOT_SUPPORTED_REASON_VECTOR_NOLOCK` | The `ALTER TABLE` statement requests `LOCK=NONE` on a table with a vector index. |
| `ER_ALTER_OPERATION_NOT_SUPPORTED_REASON_VECTOR_INSTANT` | The `ALTER TABLE` statement requests `ALGORITHM=INSTANT` on a table with a vector index. |

## See also

* [The VECTOR Type](vector.md)
* [DISTANCE() Function](distance-function.md)
* [Get started with DISTANCE()](quickstart-distance.md)
