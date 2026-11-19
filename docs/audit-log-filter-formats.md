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

Starting in Percona Server for MySQL 8.4.13-12, the component converts SQL statement text to UTF-8.

The component does not rewrite log files from earlier versions.

### Statement text in the log

The component converts SQL statement text from the client character set (`character_set_client`) to UTF-8 (`utf8mb4`).

The component converts statement text in the following log formats:

* JSON

* JSONL

* NEW XML

* OLD XML

* Syslog output (`audit_log_filter.handler = SYSLOG`)

[`audit_log_read()`](audit-log-filter-variables.md#audit_log_read) returns the UTF-8 statement text.

Before 8.4.13-12, the component writes each byte as the client sends that byte.

Before 8.4.13-12, the JSON log from a non-`utf8mb4` client is not valid UTF-8.

Before 8.4.13-12, `audit_log_read()` returns a `utf8mb4` result with invalid bytes.

A `latin1` client logs the following bytes for `é` in `SELECT 'café'`:

| | Bytes for `é` |
| --- | --- |
| Before 8.4.13-12 | `E9` (latin1, unchanged) |
| 8.4.13-12 and later, and MySQL Enterprise Audit 8.4.7 | `C3 A9` (UTF-8) |

### Filter comparisons

Filter conditions on the query text (`general_query.str`, `query.str`) compare the original client bytes.

The query length fields (`general_query.length`, `query.length`) count the original client bytes before conversion.

The comparison and the byte count match MySQL Enterprise Audit.

A UTF-8 filter value with `café` matches the statement from a `utf8mb4` client.

The same filter value does not match the same statement from a `latin1` client.

The component logs both statements as UTF-8 `café`.

Regex conditions on the query text use the original client bytes (PS-11118, PS-11948).

### Characters that cannot be converted

The component writes malformed bytes as `?`.

The component writes characters without a Unicode mapping as `?`.

The component writes the bytes of an incomplete final sequence as `?`.

Conversion resumes after each bad byte.

The component keeps the rest of the statement.

The component does not write the event when the component cannot convert the query text.

Examples of that failure include an unknown character set and insufficient memory.

The component counts the event in [`audit_log_filter_events_lost`](audit-log-filter-variables.md#audit-log-filter-status-variables).

The component never writes the raw query bytes.

### Prepared statements

The server reports the character set active when the server generates the event.

The server does not report the character set used to parse the prepared statement.

If `character_set_client` changes after `PREPARE`, the component converts `EXECUTE` and `COM_STMT_EXECUTE` text from the wrong character set:

```sql
SET NAMES utf8mb4;
PREPARE s FROM 'SELECT "é"';
SET NAMES latin1;
EXECUTE s;   -- logged as SELECT "Ã©"
```

In a non-UTF-8 session, the server stores a `PREPARE ... FROM '<literal>'` literal as `utf8mb3`.

The component converts that literal from the wrong character set.

### Differences from MySQL Enterprise Audit 8.4.7

The component converts query text from an ordinary client character set to UTF-8.

MySQL Enterprise Audit applies that UTF-8 conversion.

The component validates binary-labeled query text as UTF-8.

One example is a statement the server rewrites to hide a password.

The component keeps valid sequences.

The component replaces malformed sequences with `?`.

MySQL Enterprise Audit 8.4.7 re-encodes every byte.

The byte re-encode double-encodes UTF-8 user names in binary-labeled statements.

The component converts only SQL statement text.

Connection attributes and other fields keep their previous behavior. Percona Server does not add MySQL Enterprise Audit's conversion of connection attributes.

### `audit_log_read()` and large records

`audit_log_read()` returns a whole record larger than [`audit_log_filter.read_buffer_size`](audit-log-filter-variables.md#audit_log_filterread_buffer_size).

`audit_log_read()` returns that record in a batch of one record.

`audit_log_read()` does not fail on that record.

Batches after that record use `audit_log_filter.read_buffer_size`.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter format - XML (new style)](audit-log-filter-new.md)
* [Audit Log Filter format - XML (old style)](audit-log-filter-old.md)
* [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.format`, `audit_log_filter.file`
* [Reading Audit Log Filter files](reading-audit-log-filter-files.md)
* [Audit Log Filter compression and encryption](audit-log-filter-compression-encryption.md)
