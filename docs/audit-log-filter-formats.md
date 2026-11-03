# Audit Log Filter file format overview

On each auditable event, the component appends a record to the log. After startup, the first record describes the server and startup options; later records cover connections, disconnections, executed SQL, and more.

Which server actions become audit records depends on [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode), not on the file format. See that variable for `REDUCED` versus `FULL` and for releases before it existed.

If `LOAD_DATA` references files, the component does not log file contents.

Set format with [`audit_log_filter.format`](audit-log-filter-variables.md#audit_log_filterformat) at startup. Options:

| Format Type | Command | Description |
|---|---|---|
| [XML (new style)](audit-log-filter-new.md) | `audit_log_filter.format=NEW` | New XML layout (default in Percona Server 8.4) |
| [XML (old style)](audit-log-filter-old.md) | `audit_log_filter.format=OLD` | Legacy XML layout. Deprecated and may be removed in a later version. |
| [JSON](audit-log-filter-json.md) | `audit_log_filter.format=JSON` | One top-level JSON array of events |
| [JSONL](audit-log-filter-json.md) | `audit_log_filter.format=JSONL` | Added in 8.4.9-9. One compact JSON object per line inside a wrapping array. This layout is not standard JSON Lines. See [Standard JSONL and Percona JSONL](audit-log-filter-json.md#standard-jsonl-and-percona-jsonl). |

By default, new-style XML logs are neither compressed nor encrypted.

When you change `audit_log_filter.format`, rename `audit_log_filter.file` as well—for example use `audit.json` or `audit.jsonl` for JSON or JSONL. Reusing one base name obscures format changes across rotated files.

## Query text character set

Starting in Percona Server for MySQL 8.4.13-12, the component converts SQL statement text to UTF-8 before it writes the text. Log files written by earlier versions are not rewritten.

### Logged statement text

SQL statement text is converted from the client character set (`character_set_client`) to UTF-8 (`utf8mb4`) in all log formats: JSON, JSONL, NEW XML, OLD XML, and in syslog output (`audit_log_filter.handler = SYSLOG`). [`audit_log_read()`](audit-log-filter-variables.md#audit_log_read) returns the converted text.

Before 8.4.13-12, the bytes were written exactly as the client sent them. The JSON log of a non-`utf8mb4` client was not valid UTF-8, and `audit_log_read()` returned a `utf8mb4` result containing invalid bytes.

A `latin1` client that runs `SELECT 'café'` logs these bytes for `é`:

| | Bytes for `é` |
| --- | --- |
| Before 8.4.13-12 | `E9` (latin1, unchanged) |
| 8.4.13-12 and later, and MySQL Enterprise Audit 8.4.7 | `C3 A9` (UTF-8) |

### Filter comparisons

Filter conditions on the query text (`general_query.str`, `query.str`) compare the original client bytes. The query length fields (`general_query.length`, `query.length`) count those bytes, before conversion. This matches MySQL Enterprise Audit.

A UTF-8 filter value containing `café` matches the statement from a `utf8mb4` client. It does not match the same statement from a `latin1` client, although both statements are logged as UTF-8 `café`. The same applies to regex conditions on the query text (PS-11118, PS-11948).

### Characters that cannot be converted

Malformed bytes, characters without a Unicode mapping, and the bytes of an incomplete final sequence are written as `?`. Conversion resumes after each bad byte, so the rest of the statement is kept.

If the query text cannot be converted at all, for example because its character set is unknown or memory runs out, the event is not written and is counted in [`audit_log_filter_events_lost`](audit-log-filter-variables.md#audit-log-filter-status-variables). Raw query bytes are never written.

### Prepared statements

The server reports the character set in effect when an event is generated, not the character set the prepared statement was parsed with. If `character_set_client` changes after `PREPARE`, the text of `EXECUTE` and `COM_STMT_EXECUTE` events is converted from the wrong character set:

```sql
SET NAMES utf8mb4;
PREPARE s FROM 'SELECT "é"';
SET NAMES latin1;
EXECUTE s;   -- logged as SELECT "Ã©"
```

`PREPARE ... FROM '<literal>'` in a non-UTF-8 session is affected the same way, because the server stores the literal as `utf8mb3`.

### Differences from MySQL Enterprise Audit 8.4.7

For ordinary client character sets, the query text is converted to UTF-8 the same way as by MySQL Enterprise Audit.

Binary-labeled query text, for example a statement rewritten to hide a password, is validated as UTF-8. Valid sequences are kept. Malformed sequences are replaced with `?`. MySQL Enterprise Audit 8.4.7 re-encodes every byte, which double-encodes UTF-8 user names in such statements.

Only SQL statement text is converted. Connection attributes and other fields keep their previous behavior. Percona Server does not add MySQL Enterprise Audit's conversion of connection attributes.

### `audit_log_read()` and large records

A record larger than [`audit_log_filter.read_buffer_size`](audit-log-filter-variables.md#audit_log_filterread_buffer_size) is returned whole, in its own batch, instead of failing. Following batches use the configured size again.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter format - XML (new style)](audit-log-filter-new.md)
* [Audit Log Filter format - XML (old style)](audit-log-filter-old.md)
* [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.format`, `audit_log_filter.file`
* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
