# Thread states for DROP TABLE operations

Percona Server for MySQL 9.7.2-2 adds two performance schema stages for `DROP TABLE` operations. The stages mark the start and the end of a table drop. Use the stages to check whether a session actively runs a table drop. The stages help diagnose long-running or blocked `DROP TABLE` statements.

## Stages

The following table lists the two stages:

| Stage | Description |
|---|---|
| `stage/sql/dropping table` | The thread starts the drop operation. Percona Server for MySQL sets this stage at the start of `drop_base_table()` for base tables and at the start of `drop_temporary_table()` for temporary tables. |
| `stage/sql/after drop` | The thread completes the drop routine and returns. |

A `DROP TABLE` statement completes fast. The two stages stay visible for a short time only. Query the stage history in Performance Schema to capture the stages. Do not rely only on `SHOW PROCESSLIST`.

## Stage history example

Truncate the stage history, run a `DROP TABLE` statement, and query the recorded stage events:

```sql
TRUNCATE TABLE performance_schema.events_stages_history_long;

DROP TABLE test.t1;

SELECT EVENT_NAME
FROM performance_schema.events_stages_history_long
ORDER BY EVENT_ID;
```

??? example "Expected output"
 
    ```{.text .no-copy}
    EVENT_NAME
    stage/sql/starting
    stage/sql/checking permissions
    stage/sql/dropping table
    stage/sql/after drop
    stage/sql/waiting for handler commit
    stage/sql/query end
    stage/sql/closing tables
    stage/sql/freeing items
    stage/sql/cleaning up
    ```

The `INFORMATION_SCHEMA.PROFILING` table shows the same stages without the `stage/sql/` prefix: `dropping table` and `after drop`. Percona deprecated `INFORMATION_SCHEMA.PROFILING`. Use Performance Schema instead.

## Notes

The following notes apply to the two stages:

- The stages apply to base tables and temporary tables

- The stage names use lowercase, plain English text, consistent with existing stage names such as `creating table` and `After create`

- If `performance_schema.threads` or `SHOW PROCESSLIST` does not show the stages, the drop operation likely completed before the sample. Query `events_stages_history_long` for a reliable trace
