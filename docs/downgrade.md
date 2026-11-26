# Downgrade Percona Server for MySQL

--8<--- "get-help-snip.md"

[Need help planning a downgrade? Percona Support can assist :octicons-link-external-16:](https://www.percona.com/services/expert-support/).

## Before you downgrade

Review the following prerequisites before starting a downgrade:

* Understand the Percona Server for MySQL release model. Percona ships Long-Term Support (LTS) releases and bug-fix releases within each LTS series.

* Treat hot fixes as separate releases when you plan a downgrade.

* For a replication topology, perform a rolling downgrade. Apply a single-server method to each server in turn.

* Take a verified backup before any downgrade attempt.

* Do not attempt to downgrade below 8.4. Earlier paths are not supported.

* If the server has vector indexes, drop every vector index before you downgrade to a release earlier than 9.7.4-4. See [Downgrade a server with vector indexes](#downgrade-a-server-with-vector-indexes).

For the underlying MySQL guidance, see [Downgrading MySQL :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/downgrading.html).

## Identify a supported downgrade path

The following table summarizes supported downgrade paths from {{vers}} LTS.

| Downgrade path | Example | Supported methods | Notes |
|---|---|---|---|
| Within the same LTS series | {{vers}}.y LTS to {{vers}}.x LTS | In-place, logical dump and load, MySQL Clone, or replication | Same-LTS downgrades have the most flexibility. |
| To the previous LTS series | {{vers}}.x LTS to 8.4.y | Logical dump and load, or replication | Use this path as a rollback only. The data must contain no features from the upgraded version. |

!!! important "Rollback constraint"

    Cross-series paths fit a rollback scenario only. If you have run any feature unique to {{vers}} against the data, do not use a cross-series downgrade. Restore from a pre-upgrade backup instead.

## Choose a downgrade method

The following methods support the paths in [Identify a supported downgrade path](#identify-a-supported-downgrade-path):

* In-place: stop the server, replace binaries, and restart with the existing data directory. Available within the same LTS series only.

* Logical dump and load: export the data with `mysqldump` and load the dump into the older version.

* MySQL Clone: clone data between servers within the same LTS series.

* Replication: configure replication from {{vers}} to the older version, validate the replica, and cut traffic over.

For cutover and validation guidance during a downgrade, see [Upgrade strategies](./upgrade-strategies.md).

## Downgrade a server with vector indexes

Percona Server for MySQL 9.7.4-4 introduces [vector indexes](vector-index.md). Releases earlier than 9.7.4-4 cannot read a vector index. Starting an earlier release on a data directory that contains a vector index causes an unexpected server exit when a statement accesses the table. If the server exits during an `INSERT`, the earlier release cannot restart on that data directory.

The other downgrade methods fail as well:

* A MySQL Clone recipient that runs an earlier release exits unexpectedly on start.

* A logical dump that contains vector index definitions fails to load on an earlier release with a syntax error.

Before you downgrade to a release earlier than 9.7.4-4, drop every vector index:

1. List the vector indexes on the server:

    ```sql
    SELECT DISTINCT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME
    FROM INFORMATION_SCHEMA.STATISTICS
    WHERE INDEX_TYPE = 'VECTOR';
    ```

2. Drop each vector index that the query returns:

    ```sql
    ALTER TABLE <schema>.<table> DROP INDEX <index_name>;
    ```

3. Run the query from step 1 again. The query must return no rows.

4. Shut down the server with a slow shutdown, so that InnoDB writes all changes to the data files:

    ```sql
    SET GLOBAL innodb_fast_shutdown = 0;
    SHUTDOWN;
    ```

5. Downgrade with the method that you chose.

Dropping a vector index keeps your data. The `VECTOR` columns and their values stay in the table. To use vector search again, upgrade the server and create the indexes again.

### Recover from a failed downgrade

If you started a release earlier than 9.7.4-4 on a data directory that contains a vector index, and that server no longer starts, follow these steps:

1. Start the release that you downgraded from (9.7.4-4 or later) on the same data directory. This release rolls back the incomplete statement.

2. Drop every vector index, as described in the previous steps.

3. Shut down the server with `innodb_fast_shutdown = 0`.

4. Start the release that you want to downgrade to.

## Assess downgrade risks

!!! warning "Data loss risk"

    A failed downgrade can corrupt or destroy data. Create and verify a backup before any downgrade attempt. Restore the backup if the downgrade encounters issues.

The following table lists the risks of downgrading.

| Risk | Description |
|---|---|
| Data loss | Data loss is possible if the downgrade encounters issues. Create a backup of your data before attempting a downgrade. |
| Incompatibility | Features used in the upgraded version can cause incompatibility. |
| Performance | Downgrading can reduce performance. |
| Security | Older versions lack security updates available in upgraded versions, which can increase exposure. |

## Further reading

The following Percona Server for MySQL pages cover related topics:

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade from plugins to components](./upgrade-components.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)
