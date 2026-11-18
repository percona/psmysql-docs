> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Reading Audit Log Filter files

Audit Log Filter exposes a SQL API to read audit files in JSON or JSONL only. Layout and the JSONL option appear in [Audit Log Filter format - JSON and JSONL](https://docs.percona.com/percona-server/9.7/audit-log-filter-json.html) and [Audit Log Filter file format overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-formats.html).

Set `audit_log_filter.format` to match. [`audit_log_filter.file`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html#audit_log_filterfile) defines the path, base name, and suffix that readers use to locate files.

When a file no longer matches the pattern, readers ignore the file.

## Functions used for reading the files

The following functions read JSON or JSONL audit files:

- [`audit_log_read`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html#audit_log_read) — returns audit events from the log.
- [`audit_log_read_bookmark`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html#audit_log_read_bookmark) — returns a bookmark for the last read position. Pass the bookmark into `audit_log_read()` to resume.

Start a read with a bookmark or an explicit start position:

```
SELECT audit_log_read(audit_log_read_bookmark());
```

Continue from the current cursor:

```
SELECT audit_log_read();
```

The read sequence ends when the session ends or when you call `audit_log_read('null')`.

## Common starting points

The `audit_log_read()` argument is a JSON object. Pick one of the following starting forms.

Start at a specific timestamp:

```
SELECT audit_log_read('{"start": {"timestamp": "2026-05-20 12:28:10"}}');
```

Start at a date (the time defaults to `00:00:00`):

```
SELECT audit_log_read('{"start": {"timestamp": "2026-05-20"}}');
```

Cap how many events the call returns with `max_array_length`:

```
SELECT audit_log_read('{"start": {"timestamp": "2026-05-20 12:28:10"}, "max_array_length": 3}');
```

Resume from an explicit bookmark. Pass both `timestamp` and `id` at the top level, with no `start` wrapper:

```
SELECT audit_log_read('{"timestamp": "2026-05-20 12:28:10", "id": 1561422}');
```

The `start` form and the bookmark form (`timestamp` + `id`) are mutually exclusive. See [`audit_log_read()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html#audit_log_read) for the full parameter reference, including constraints on re-seeding a read sequence in flight.

## Additional reading

- [Audit Log Filter format - JSON and JSONL](https://docs.percona.com/percona-server/9.7/audit-log-filter-json.html)
- [Audit Log Filter file format overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-formats.html)
- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html)
- [Manage the Audit Log Filter files](https://docs.percona.com/percona-server/9.7/manage-audit-log-filter.html)
- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.html)
