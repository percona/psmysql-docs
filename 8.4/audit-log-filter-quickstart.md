> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Audit Log Filter quickstart

Use the following steps when the Audit Log Filter component and tables are already installed. For installation, see [install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html). You need `AUDIT_ADMIN`. Changing [`audit_log_filter.disable`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterdisable) at runtime also requires `SYSTEM_VARIABLES_ADMIN`.

Quickstart

1. Optional: run `SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';` and note the counter.
1. Run these five statements in order:

```
SET GLOBAL audit_log_filter.disable = false;
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
SELECT audit_log_filter_set_user('%', 'log_all');
SELECT audit_log_filter_flush();
SELECT 1;
```

1. Run `SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';` again. The counter should increase. If it does not, verify the component loaded, tables exist, and [`audit_log_filter.disable`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterdisable) is `false`.

For JSON or JSONL [`audit_log_filter.format`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterformat), read events with [`audit_log_read()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_read) ([Reading Audit Log Filter files](https://docs.percona.com/percona-server/8.4/reading-audit-log-filter-files.html)). With the default `NEW` format in Percona Server 8.4, inspect the file named by [`audit_log_filter.file`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterfile) on the server.

## Next steps

After the catch-all `log_all` rule works, replace it with a tighter JSON filter (by user, database, table, or event class). Call [`audit_log_filter_set_filter()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filter_set_filterfilter_name-definition), [`audit_log_filter_set_user()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filter_set_useruser_name-filter_name), and [`audit_log_filter_flush()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filter_flush) so sessions pick up changes. Author rules in [Write audit_log_filter definitions](https://docs.percona.com/percona-server/8.4/write-filter-definitions.html), compare assignment to JSON rules in [Filter the Audit Log Filter logs](https://docs.percona.com/percona-server/8.4/filter-audit-log-filter-files.html#assignment-vs-rules-inside-the-json), and validate names in [Audit Log Filter definition fields](https://docs.percona.com/percona-server/8.4/audit-log-filter-definition-fields.html).

If you switch to JSON or JSONL, read [Audit Log Filter file format overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-formats.html) and [Reading Audit Log Filter files](https://docs.percona.com/percona-server/8.4/reading-audit-log-filter-files.html). For production, plan path, rotation, and retention with [`audit_log_filter.file`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterfile), [`audit_log_rotate()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_rotate), and [Manage the Audit Log Filter files](https://docs.percona.com/percona-server/8.4/manage-audit-log-filter.html).

Also see: [Audit Log Filter overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.html) · [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html) · [Disable Audit Log Filter logging](https://docs.percona.com/percona-server/8.4/disable-audit-log-filter.html) · [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html) (full UDF and variable reference)
