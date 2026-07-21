# Reading Audit Log Filter files

Audit Log Filter exposes a SQL API to read audit files in JSON or JSONL only. Layout and the JSONL option are covered in [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md) and [Audit Log Filter file format overview](audit-log-filter-formats.md). Set `audit_log_filter.format` accordingly; [`audit_log_filter.file`](audit-log-filter-variables.md#audit_log_filterfile) defines the path, base name, and suffix used to locate files.

If a file no longer matches that pattern, readers ignore it.

## Reader functions

Two functions read JSON or JSONL audit files:

* [`audit_log_read`](audit-log-filter-variables.md#audit_log_read) — returns audit events from the log.

* [`audit_log_read_bookmark`](audit-log-filter-variables.md#audit_log_read_bookmark) — returns a bookmark for the last read position. Pass it into `audit_log_read()` to resume.

## Read commands

A session holds at most one active read context. Pick one of the following commands to open, advance, or close it. For the full argument reference, see [`audit_log_read()`](audit-log-filter-variables.md#audit_log_read).

### Resume from a bookmark

Start a read at the position returned by `audit_log_read_bookmark()`:

```sql
SELECT audit_log_read(audit_log_read_bookmark());
```

### Start at a timestamp

Start a read at an explicit timestamp. When the timestamp omits a time part, the component assumes `00:00:00`:

```sql
SELECT audit_log_read('{"start": {"timestamp": "2026-05-20 12:28:10"}}');
SELECT audit_log_read('{"start": {"timestamp": "2026-05-20"}}');
```

### Address one specific event

Pass a bookmark literal with `timestamp` and `id` and no `start` envelope:

```sql
SELECT audit_log_read('{"timestamp": "2026-05-20 12:28:10", "id": 1561422}');
```

### Limit the events per call

Cap how many events a single call returns by adding `max_array_length` to any positioning form:

```sql
SELECT audit_log_read('{"start": {"timestamp": "2026-05-20 12:28:10"}, "max_array_length": 3}');
```

### Continue from the current cursor

After a read sequence is open, continue advancing without supplying a new position:

```sql
SELECT audit_log_read();
```

### Close the active sequence

Release the reader cursor before opening a new sequence at a different position:

```sql
SELECT audit_log_read('null');
```

A read sequence also ends when the session ends. A single call cannot combine the `start` envelope with a top-level `timestamp` or `id`. To reposition while a sequence is active, close it first with `'null'`.

## Additional reading

* [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md)
* [Audit Log Filter file format overview](audit-log-filter-formats.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
* [Manage the Audit Log Filter files](manage-audit-log-filter.md)
* [Audit Log Filter overview](audit-log-filter-overview.md)
