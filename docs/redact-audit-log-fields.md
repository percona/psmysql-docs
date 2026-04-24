# Redact audit log fields

Audit events that carry SQL statement text can leak sensitive values into the audit log. Examples include credentials, personal data, and secret literals. The Audit Log Filter can rewrite that text as a **statement digest** before the event is written. The log records *what kind of statement ran* without capturing the literal values.

This page covers the `print` and `replace` mechanism. For base filter authoring, see [Write audit_log_filter definitions](write-filter-definitions.md).

## What can be replaced

Only the statement-text fields are replaceable, and only with the `query_digest` function:

| Event class    | Replaceable field   | Event mode required |
|---|---|---|
| `general`      | `general_query.str` | `REDUCED` or `FULL` |
| `table_access` | `query.str`         | `REDUCED` or `FULL` |
| `query`        | `query.str`         | `FULL`              |
| `parse`        | `query.str`         | `FULL`              |

The `general` and `table_access` classes are processed in both event modes. The `query` and `parse` classes are processed only when [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) is `FULL`. A filter that targets `query` or `parse` under `REDUCED` is rejected at parse time.

Replacement happens during filtering, so the choice between literal text and digest applies regardless of which log format (XML or JSON) writes the event.

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

* `name` — the replaceable field from the preceding table.

* `print` — a condition. When the condition evaluates to **true**, the field is kept. When the condition evaluates to **false**, the field is replaced. Use `"print": false` to replace unconditionally.

* `replace` — the replacement value, specified as a `function` item. Only `query_digest` (with no arguments) is permitted.

The conditional form lets you mix redacted and literal statements in the same filter.

## Example 1: Redact every `general` event

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

## Example 2: Redact both statement-carrying classes

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

The resulting audit stream contains only digests, with no literal SQL text. The output is a common baseline for PCI and PII environments.

## Example 3: Redact only specific events

Scope replacement to a subset of events by nesting `print` inside an `event` block. The following filter redacts `query.str` on `insert` and `update` `table_access` events but leaves `read` and `delete` alone:

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

## Example 4: Redact account-management statements

`query_digest` with an argument is a Boolean comparator. The comparator is useful in a `log` condition to decide *whether* to log an event based on the digest. Combined with field checks, you can log and redact only specific statement types. The following filter matches `general`/`status` events for account-management DDL and replaces the literal statement with the digest:

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

To keep literal text for *most* statements and redact only specific ones (or the reverse), use `query_digest` as a comparator inside `print`. With an argument, the function returns true when the active statement digest equals the argument.

Keep the literal text when the digest matches `SELECT ?`, and replace otherwise:

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

Invert with `not` to redact only the matching statements and keep literal text for the rest:

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

### `args` shorthand and typed-array form

`query_digest` accepts the single string argument in two equivalent forms:

* Shorthand (preferred): `"args": "SELECT ?"`. Use this form for a single literal string.

* Typed array: `"args": [{"string": {"string": "SELECT ?"}}]`. Use this form when a rule generator emits the verbose typed-array layout for every function call.

The component parses both forms identically. The shorthand is shorter and easier to read.

## See also

* [Write audit_log_filter definitions](write-filter-definitions.md) — base grammar and `log` conditions.

* [Block statements with an audit log filter](block-statements-with-audit-filter.md) — use `abort` to prevent execution.

* [Audit Log Filter definition fields](audit-log-filter-definition-fields.md) — complete field reference per class.

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md).
