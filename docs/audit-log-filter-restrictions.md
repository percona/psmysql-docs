# Audit Log Filter restrictions

## General restrictions

* The component logs SQL statements only, not NoSQL APIs such as the Memcached interface.

* Event coverage follows [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode). In `REDUCED` mode, stored programs log the outer `CALL`, not each statement inside the body. The component never logs file contents referenced by statements such as `LOAD DATA`.

* Changing [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) at runtime is not atomic across an event stream. Events from a single statement may split across the switch. For a clean cutover, pause the workload before changing the value or restart the server with the new value in the option file. See [Switching `event_mode` at runtime](audit-log-filter-variables.md#switching-event_mode-at-runtime).

* On a cluster, install Audit Log Filter on every node that runs SQL.

* Aggregate audit data from every node yourself. The component does not centralize the data.

* Maintain a separate rule set per server. An uninitialized replica writes no audit rows for rules the replica lacks. Configure replication so that you do not blindly overwrite replica-local filter tables with source changes unless that outcome is intended.

    By default, replication can replicate `mysql.audit_log_filter` and `mysql.audit_log_user` from source to replica. Use replication filters or channels to exclude those tables when replicas should keep local rules.

    Replicated table rows alone do not refresh in-memory filter state. Restart the server, reload the component, or run `audit_log_filter_flush()` to apply table changes to the running component.

* Numeric fields in rules may use integer or string forms. `connection_type` accepts symbolic constants. See [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) and [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

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

    The event applies replicated filter changes shortly after replication commits them. For session details after flush, see [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush).

4. On the source, define a filter, assign it to users (UDFs or direct table edits), and call `audit_log_filter_flush()` on the source when needed.

5. After a minute, confirm the replica sees the filter; run queries as that user and verify the audit file.

When nothing appears, wait for the next event tick or run `SELECT audit_log_filter_flush();` on the replica immediately. Confirm that replication applied the rows and that the event is `ENABLED`. Persistent gaps usually indicate a replication issue. Investigate the replica's replication health.

When the component is missing on either host, install the component on source and replica independently.

### Limitation

Direct `INSERT`, `UPDATE`, or `DELETE` on the source without a source-side `audit_log_filter_flush()` still replicate to the replica. The scheduled event flushes on the replica. Replica filters update while the source in-memory state stays stale until someone flushes on the source.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter_flush()`

* [Install the audit log filter](install-audit-log-filter.md)

* [Upgrade Percona Server for MySQL](upgrade.md)

* [Binlogging and replication improvements](binlogging-replication-improvements.md)
