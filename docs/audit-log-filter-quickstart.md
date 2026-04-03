# Audit Log Filter quickstart

Use the following steps when the Audit Log Filter component and tables are already installed. For installation, see [install the audit log filter](install-audit-log-filter.md). You need `AUDIT_ADMIN`. Changing [`audit_log_filter.disable`](audit-log-filter-variables.md#audit_log_filterdisable) at runtime also requires `SYSTEM_VARIABLES_ADMIN`.

!!! tip "Quickstart"

    1. Optional: run `SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';` and note the counter.
    2. Run these five statements in order:

    ```sql
    SET GLOBAL audit_log_filter.disable = false;
    SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
    SELECT audit_log_filter_set_user('%', 'log_all');
    SELECT audit_log_filter_flush();
    SELECT 1;
    ```

    3. Run `SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';` again. The counter should increase. If it does not, verify the component loaded, tables exist, and [`audit_log_filter.disable`](audit-log-filter-variables.md#audit_log_filterdisable) is `false`.

    For JSON or JSONL [`audit_log_filter.format`](audit-log-filter-variables.md#audit_log_filterformat), read events with [`audit_log_read()`](audit-log-filter-variables.md#audit_log_read) ([Reading Audit Log Filter files](reading-audit-log-filter-files.md)). With the default `NEW` format in Percona Server 8.4, inspect the file named by [`audit_log_filter.file`](audit-log-filter-variables.md#audit_log_filterfile) on the server.

## Next steps

After the catch-all `log_all` rule works, replace it with a tighter JSON filter (by user, database, table, or event class). Call [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition), [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name), and [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush) so sessions pick up changes. Author rules in [Write audit_log_filter definitions](write-filter-definitions.md), compare assignment to JSON rules in [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md#assignment-vs-rules-inside-the-json), and validate names in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

If you switch to JSON or JSONL, read [Audit Log Filter file format overview](audit-log-filter-formats.md) and [Reading Audit Log Filter files](reading-audit-log-filter-files.md). For production, plan path, rotation, and retention with [`audit_log_filter.file`](audit-log-filter-variables.md#audit_log_filterfile), [`audit_log_rotate()`](audit-log-filter-variables.md#audit_log_rotate), and [Manage the Audit Log Filter files](manage-audit-log-filter.md).

Also see: [Audit Log Filter overview](audit-log-filter-overview.md) · [Install the audit log filter](install-audit-log-filter.md) · [Disable Audit Log Filter logging](disable-audit-log-filter.md) · [Audit log filter functions, options, and variables](audit-log-filter-variables.md) (full UDF and variable reference)
