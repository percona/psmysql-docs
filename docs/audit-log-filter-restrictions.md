# Audit Log Filter restrictions

## General restrictions

### Event coverage

* The component logs SQL statements only—not NoSQL APIs such as the Memcached interface.

* Event coverage follows [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode). In `REDUCED` mode, stored programs log the outer `CALL`, not each statement inside the body. The component never logs file contents referenced by statements such as `LOAD DATA`.

* Set `audit_log_filter.event_mode` in `my.cnf` and restart the server. Changing the value on a running server creates a window where in-flight events are evaluated inconsistently, in either direction between `REDUCED` and `FULL`. Audit output during the switch cannot be reconciled after the fact. If a restart is not possible, follow the `SET GLOBAL` change with [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush) inside a maintenance window to narrow the window. For details, see [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode).

### Cluster and replication

* On a cluster, install Audit Log Filter on every node that runs SQL.

* Aggregate audit data from every node yourself—the component does not centralize it.

* Maintain a separate rule set per server. An uninitialized replica writes no audit rows for rules it lacks. Configure replication so you do not blindly overwrite replica-local filter tables with source changes unless that is intended.

    By default, replication can replicate `mysql.audit_log_filter` and `mysql.audit_log_user` from source to replica. Use replication filters or channels to exclude those tables when replicas should keep local rules.

    Replicated table rows alone do not refresh in-memory filter state. Restart, reload the component, or run `audit_log_filter_flush()` to apply table changes to the running component.

### Filter validation

* Starting in Percona Server for MySQL 8.4.9-9, numeric fields in rules may use integer or string forms, and `connection_type` accepts symbolic constants—see [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) and [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

* Before 8.4.9-9, the parser silently ignored unknown JSON keys. Misspelling a structural key (for example `classes` instead of `class`, `events` instead of `event`, `names` instead of `name`, `logs` instead of `log`) caused the subtree to be skipped, and the filter fell back to default behavior (log everything) with no error. Upgrade to 8.4.9-9 or later to catch these mistakes at parse time.

## Synchronizing audit log filters between a source and a replica

Replicate the filter tables and run `audit_log_filter_flush()` on the replica so replicated rows take effect in the component. Post-flush session behavior is documented under [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush).

### Procedure: scheduled event to flush filters on the replica

1. Install Percona Server for MySQL on the source with Audit Log Filter.

2. Clone a replica from a source backup.

3. On the replica, create a one-minute event:

       ```sql
       USE mysql;
       CREATE EVENT auditflush
           ON SCHEDULE EVERY 1 MINUTE
           COMMENT 'Flush audit log filters every minute'
           DO
             SELECT audit_log_filter_flush();
       ```

    The event applies replicated filter changes shortly after replication commits them. For session details after flush (8.4.9-9+), see [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush).

4. On the source, define a filter, assign it to users (UDFs or direct table edits), and call `audit_log_filter_flush()` on the source when needed.

5. After a minute, confirm the replica sees the filter; run queries as that user and verify the audit file.

If nothing appears, wait for the next event tick or run `SELECT audit_log_filter_flush();` on the replica immediately; confirm replication applied the rows and the event is `ENABLED`. Persistent gaps usually mean a replication issue—investigate the replica’s replication health.

If the component is missing on either host, install it on source and replica independently.

### Limitation

Direct `INSERT`/`UPDATE`/`DELETE` on the source without `audit_log_filter_flush()` there still replicate to the replica; the scheduled event flushes on the replica, so replica filters update while the source in-memory state stays stale until someone flushes there.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter_flush()`
* [Install the audit log filter](install-audit-log-filter.md)
* [Upgrade Percona Server for MySQL](upgrade.md)
* [Binlogging and replication improvements](binlogging-replication-improvements.md)
