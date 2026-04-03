# Redact audit log fields

Audit events that carry SQL statement text can leak sensitive values into the audit log. Examples include credentials, personal data, and secret literals. The Audit Log Filter can rewrite that text as a statement digest before the event is written. The log then records the statement shape without capturing the literal values.

This page covers the `print` / `replace` mechanism. For base filter authoring, see [Write audit_log_filter definitions](write-filter-definitions.md).

## What can be replaced

Four class and field pairs support replacement. They use two distinct field names (`general_query.str` and `query.str`), and only the `query_digest` function may supply the replacement value:

| Event class    | Replaceable field   | Notes |
|---|---|---|
| `general`      | `general_query.str` | |
| `table_access` | `query.str`         | |
| `query`        | `query.str`         | Requires [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) = `FULL` |
| `parse`        | `query.str`         | Requires [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) = `FULL` |

Replacement happens during filtering. The choice of literal text or digest applies regardless of which log format the writer produces later, including XML, JSON, and JSONL.

## Shape

A `print` item goes inside a class or event block:

```json
"print": {
  "field": {
    "name": "field_name",
    "print": condition,
    "replace": replacement_value
  }
}
```

* `name` — the replaceable field. Use a name from the preceding table.

* `print` — a condition. When the condition evaluates to `true`, the field is kept. When the condition evaluates to `false`, the field is replaced. Set `"print": false` to replace unconditionally.

* `replace` — the replacement value, specified as a `function` item. The component permits only `query_digest` with no arguments.

The conditional form lets you mix redacted and literal statements in the same filter.

## Examples

### Redact every `general` event

Replace statement text in every `general` event with its digest:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "print": {
        "field": {
          "name": "general_query.str",
          "print": false,
          "replace": {
            "function": { "name": "query_digest" }
          }
        }
      }
    }
  }
}
```

### Redact both statement-carrying classes

`general` and `table_access` both carry statement text. Combine them into one filter:

```json
{
  "filter": {
    "class": [
      {
        "name": "general",
        "print": {
          "field": {
            "name": "general_query.str",
            "print": false,
            "replace": { "function": { "name": "query_digest" } }
          }
        }
      },
      {
        "name": "table_access",
        "print": {
          "field": {
            "name": "query.str",
            "print": false,
            "replace": { "function": { "name": "query_digest" } }
          }
        }
      }
    ]
  }
}
```

The resulting audit stream contains only digests — no literal SQL text — which is a common baseline for PCI/PII environments.

### Redact only specific events

Scope replacement to a subset of events by nesting `print` inside an `event` block. This filter redacts `query.str` on `insert` and `update` `table_access` events but leaves `read` and `delete` alone:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update"],
        "print": {
          "field": {
            "name": "query.str",
            "print": false,
            "replace": { "function": { "name": "query_digest" } }
          }
        }
      }
    }
  }
}
```

### Redact account-management statements

`query_digest` with an argument is a Boolean comparator — useful in a `log` condition to decide *whether* to log an event based on its digest. Combined with field checks, you can log (and redact) only specific statement types. This filter fires on `general`/`status` events for account-management DDL and replaces the literal statement with its digest:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "print": {
          "field": {
            "name": "general_query.str",
            "print": false,
            "replace": {
              "function": { "name": "query_digest" }
            }
          }
        },
        "log": {
          "or": [
            { "field": { "name": "general_sql_command.str", "value": "alter_user" } },
            { "field": { "name": "general_sql_command.str", "value": "alter_user_default_role" } },
            { "field": { "name": "general_sql_command.str", "value": "create_role" } },
            { "field": { "name": "general_sql_command.str", "value": "create_user" } }
          ]
        }
      }
    }
  }
}
```

For the full set of `general_sql_command.str` values, see [Test event field values](write-filter-definitions.md#test-event-field-values).

## Conditional redaction

To keep literal text for *most* statements and redact only specific ones, or to do the reverse, use `query_digest` as a comparator inside `print`. With an argument, the function returns true when the current statement digest equals the argument.

Keep the literal text when the digest matches `SELECT ?`; replace otherwise:

```json
"print": {
  "field": {
    "name": "general_query.str",
    "print": {
      "function": {
        "name": "query_digest",
        "args": "SELECT ?"
      }
    },
    "replace": {
      "function": { "name": "query_digest" }
    }
  }
}
```

Invert with `not` — redact only the matching statements, keep literal text for everything else:

```json
"print": {
  "field": {
    "name": "general_query.str",
    "print": {
      "not": {
        "function": {
          "name": "query_digest",
          "args": "SELECT ?"
        }
      }
    },
    "replace": {
      "function": { "name": "query_digest" }
    }
  }
}
```

## Additional reading

* [Write audit_log_filter definitions](write-filter-definitions.md) — base grammar and `log` conditions.
* [Block statements with an audit log filter](block-statements-with-audit-filter.md) — use `abort` to prevent execution.
* [Audit Log Filter definition fields](audit-log-filter-definition-fields.md) — complete field reference per class.
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md).
