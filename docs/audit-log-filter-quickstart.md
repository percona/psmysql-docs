# Audit Log Filter quickstart

Use the following steps after you install the Audit Log Filter component and tables. See [install the audit log filter](install-audit-log-filter.md) when the component is not yet installed.

You need `AUDIT_ADMIN`. Changing [`audit_log_filter.disable`](audit-log-filter-variables.md#audit_log_filterdisable) at runtime also requires `SYSTEM_VARIABLES_ADMIN`.

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

    3. Run `SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';` again. The counter should increase. When the counter does not increase, verify that the component loaded, the tables exist, and [`audit_log_filter.disable`](audit-log-filter-variables.md#audit_log_filterdisable) is `false`.

    With the default `JSONL` [`audit_log_filter.format`](audit-log-filter-variables.md#audit_log_filterformat), read events with [`audit_log_read()`](audit-log-filter-variables.md#audit_log_read). See [Reading Audit Log Filter files](reading-audit-log-filter-files.md). You can also inspect the file named by [`audit_log_filter.file`](audit-log-filter-variables.md#audit_log_filterfile) on the server. The `JSON` format uses the same reader. The `NEW` (XML) format is read directly from the log file.

## Next steps

After the catch-all `log_all` rule works, replace the rule with a tighter JSON filter. Scope the filter by user, database, table, or event class.

Call the filter UDFs to apply changes:

* [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition)

* [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name)

* [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush)

Author rules in [Write audit_log_filter definitions](write-filter-definitions.md). Compare assignment to JSON rules in [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md#assignment-vs-rules-inside-the-json). Validate names in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

When you switch to JSON or JSONL, read [Audit Log Filter file format overview](audit-log-filter-formats.md) and [Reading Audit Log Filter files](reading-audit-log-filter-files.md).

For production, plan path, rotation, and retention with:

* [`audit_log_filter.file`](audit-log-filter-variables.md#audit_log_filterfile)

* [`audit_log_rotate()`](audit-log-filter-variables.md#audit_log_rotate)

* [Manage the Audit Log Filter files](manage-audit-log-filter.md)

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Install the audit log filter](install-audit-log-filter.md)

* [Disable Audit Log Filter logging](disable-audit-log-filter.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
