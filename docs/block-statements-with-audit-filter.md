# Block statements with an audit log filter

The Audit Log Filter does more than observe events. An `abort` item inside an `event` block **prevents matching statements from executing**. Blocked statements are still logged, and the client sees:

```none
ERROR 1045 (28000): Statement was aborted by an audit log filter
```

Use blocking to enforce policy at the SQL layer. For example, stop writes against a sensitive table from any application path, independently of `GRANT`.

For background on filter authoring, see [Write audit_log_filter definitions](write-filter-definitions.md). This page assumes you have a working filter JSON and want to add blocking.

!!! warning

    You can lock yourself out. If an `abort` rule matches a statement your own account runs, the statement fails. The `AUDIT_ABORT_EXEMPT` privilege (granted automatically to `SYSTEM_USER` accounts) bypasses `abort` conditions and lets you recover from a misconfiguration. Keep at least one such account available.

## Syntax

`abort` lives inside an `event` block and can be:

* A Boolean. `true` aborts every event the `event` block matches. `false` is a no-op.

* A condition built from `field`, `and`, `or`, `not`, `variable`, or `function` items, using the same grammar as a `log` condition. The event is aborted when the condition evaluates to true.

```json
"event": {
  "name": [ "qualifying subclass names" ],
  "abort": condition
}
```

For the field grammar used in conditions, see [Test event field values](write-filter-definitions.md#test-event-field-values) and [Combine conditions with logical operators](write-filter-definitions.md#combine-conditions-with-logical-operators) on the authoring page.

## Not every event is abortable

Only events marked **Yes** in the [Abortability](audit-log-filter-definition-fields.md#abortability) table can be blocked. For example, `table_access` and `message` subclasses can be aborted, but `connection` and `general` subclasses cannot. When a filter tries to abort a non-abortable event, the server writes a warning to the error log and lets the statement through.

## Example 1: Block all DML on any table

The following filter blocks `insert`, `update`, and `delete` statements against every table:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete"],
        "abort": true
      }
    }
  }
}
```

Use this kind of rule on a standby or read-only replica to enforce immutability at the SQL surface. Then assign the filter with [`audit_log_filter_set_user()`](audit-log-filter-variables.md).

## Example 2: Block DML on a specific table

Restrict the block to a single table by comparing `table_database.str` and `table_name.str`:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete"],
        "abort": {
          "and": [
            { "field": { "name": "table_database.str", "value": "finances" } },
            { "field": { "name": "table_name.str", "value": "bank_account" } }
          ]
        }
      }
    }
  }
}
```

Every attempt to write to `finances.bank_account` fails with the audit abort error, regardless of which application issued the write. The component logs each attempt.

## Example 3: Block a list of tables

Use `or` to enumerate several target tables inside the same `and`:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete"],
        "abort": {
          "and": [
            { "field": { "name": "table_database.str", "value": "finances" } },
            {
              "or": [
                { "field": { "name": "table_name.str", "value": "bank_account" } },
                { "field": { "name": "table_name.str", "value": "ledger" } },
                { "field": { "name": "table_name.str", "value": "transactions" } }
              ]
            }
          ]
        }
      }
    }
  }
}
```

## Combine blocking with logging

Blocking and logging are independent. The same event can carry both a `log` and an `abort` item. For example, log every blocked attempt and also log failed `SELECT`s on the same object. Keep the two concerns as separate event blocks when the conditions differ:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "read",
          "log": {
            "field": { "name": "table_name.str", "value": "bank_account" }
          }
        },
        {
          "name": ["insert", "update", "delete"],
          "abort": {
            "field": { "name": "table_name.str", "value": "bank_account" }
          }
        }
      ]
    }
  }
}
```

## Recovery

When an `abort` rule prevents administrators from running essential statements:

1. Connect with an account that holds `AUDIT_ABORT_EXEMPT`, typically a `SYSTEM_USER` account.

2. Replace the filter with a safer definition using [`audit_log_filter_set_filter()`](audit-log-filter-variables.md).

3. Reassign accounts with [`audit_log_filter_set_user()`](audit-log-filter-variables.md) when needed.

Test `abort` rules on a clone before applying them to production.

## See also

* [Write audit_log_filter definitions](write-filter-definitions.md) — base grammar and `log` conditions.

* [Redact audit log fields](redact-audit-log-fields.md) — hide statement text with `print` and `replace`.

* [Audit Log Filter definition fields](audit-log-filter-definition-fields.md#abortability) — which events can be aborted.

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md).
