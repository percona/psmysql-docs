# Filter the Audit Log Filter logs

Rule-based filtering includes or excludes events using these attributes:

* User account
* Audit event class
* Audit event subclass
* Audit event fields (for example, `COMMAND_CLASS` or `STATUS`)

Which classes and subclasses you can target depends on [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode). Validated names appear in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

Define multiple filters and assign any filter to multiple accounts, or register a default filter for accounts without a specific row. You define filters through SQL function calls.

After you define a filter, the server persists it in `mysql` system tables.

## Audit Log Filter functions

The six management UDFs in the following table — `audit_log_filter_flush()`, `audit_log_filter_set_filter()`, `audit_log_filter_remove_filter()`, `audit_log_filter_set_user()`, `audit_log_filter_remove_user()`, and [`audit_log_rotate()`](audit-log-filter-variables.md#audit_log_rotate) — require the `AUDIT_ADMIN` privilege.

The reader UDFs ([`audit_log_read()`](audit-log-filter-variables.md#audit_log_read), [`audit_log_read_bookmark()`](audit-log-filter-variables.md#audit_log_read_bookmark)), the session-id helper ([`audit_log_session_filter_id()`](audit-log-filter-variables.md#audit_log_session_filter_id)), and the keyring helpers ([`audit_log_encryption_password_get()`](audit-log-filter-variables.md#audit_log_encryption_password_getkeyring_id), [`audit_log_encryption_password_set()`](audit-log-filter-variables.md#audit_log_encryption_password_setnew_password)) do not require `AUDIT_ADMIN`. The keyring helpers require an initialized keyring component or plugin.

These functions drive rule-based filtering:

| Function | Description | Example |
|---|---|---|
| audit_log_filter_flush() | Flush filter tables and reload definitions into the component | `SELECT audit_log_filter_flush();` |
| audit_log_filter_set_filter() | Create or replace a named filter | `SELECT audit_log_filter_set_filter('log_connections', '{ "filter": {} }');` |
| audit_log_filter_remove_filter() | Drop a named filter | `SELECT audit_log_filter_remove_filter('filter-name');` |
| audit_log_filter_set_user() | Bind a filter to a user account | `SELECT audit_log_filter_set_user('user-name@localhost', 'filter-name');` |
| audit_log_filter_remove_user() | Clear filter bindings for a user account | `SELECT audit_log_filter_remove_user('user-name@localhost');` |

Through SQL, you define, inspect, and change audit log filters; definitions live in the `mysql` system database.

[`audit_log_session_filter_id()`](audit-log-filter-variables.md#audit_log_session_filter_id) returns the active audit log filter ID for the current session.

Filter definitions are JSON values.

Reloading rules from tables, persistence after `audit_log_filter_set_filter()`, and post-flush session behavior are covered under [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush) and [Persistence and refreshing](audit-log-filter-variables.md#persistence-and-refreshing) in [Audit log filter functions, options, and variables](audit-log-filter-variables.md).

## Filter modification lifecycle

The following diagram shows how filter changes persist, reload into the component, and reach sessions, including when [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush) runs.

![Audit Log Filter modification lifecycle](_static/audit-log-filter-modification-lifecycle.png)

## Constraints

Enable the `component_audit_log_filter` component and ensure audit tables exist before calling audit log filter functions. The account must hold the required privileges.

## Filter definition validation

*Introduced in Percona Server for MySQL 8.4.9-9.*

The server validates filter definitions at parse time and rejects invalid input with a clear error:

* Unknown field names (e.g., `"WRONG.str"`)

* Invalid class or event subclass names

* Empty arrays (e.g., `"class": []`)

* Unknown JSON keys (e.g., `"classes"` instead of `"class"`, `"events"` instead of `"event"`, `"names"` instead of `"name"`, `"logs"` instead of `"log"`)

* `print` rules that reference invalid fields for any class in a multi-class array

* Mismatched field types (e.g., negative values for unsigned fields, integers where only strings are allowed)

An empty filter object `{}` is equivalent to `{"filter": {"log": true}}` and logs every event. To log nothing, use `{"filter": {"log": false}}`.

#### Behavior before 8.4.9-9

Before 8.4.9-9, the parser silently ignored unknown keys. Misspelling a structural key caused the parser to skip that entire subtree and fall back to the default. For example, the filter `{"filter": {"classes": [...]}}` (note `classes` instead of `class`) was parsed as `{"filter": {}}`, which logs every event. No error was returned, and the filter appeared to succeed. The same applied to `events` instead of `event`, `names` instead of `name`, and `logs` instead of `log`. Upgrade to 8.4.9-9 or later to catch these mistakes at parse time.

Parse-phase subclass names must use `preparse` and `postparse`.

[`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) controls which classes new definitions may use; filters saved under `FULL` can still load under `REDUCED` with some classes skipped (see that variable).

## Using the audit log filter functions

### Assignment vs rules inside the JSON

Two mechanisms apply, in order:

1. Assignment (`mysql.audit_log_user`) — Each session uses one named filter from the `USER` and `HOST` columns (the same `user_name`@`host_name` form you pass to [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name)). The server loads that filter’s JSON from `mysql.audit_log_filter`. Assignments do not merge: a session never evaluates two separate filter definitions at once.

2. Rules inside the assigned JSON — `log` conditions on a class or event block narrow which events match within the already-selected filter. Conditions compare event fields (such as `user.str`, `host.str`, `table_database.str`, `table_name.str`, `status`) with `field` items, and combine them with `and` / `or` / `not`. They are not a second user- or host-level assignment row. For example, bind one filter to `'app'@'%'` and still include a `log` condition under a `connection` rule so only connection events from chosen client hosts are logged.

See [Test event field values](write-filter-definitions.md#test-event-field-values) and [Combine conditions with logical operators](write-filter-definitions.md#combine-conditions-with-logical-operators) for the grammar used in rule-level conditions.

### Which `audit_log_user` row applies

On connect, the component selects a row in `mysql.audit_log_user` whose `USER` and `HOST` match the session account. Literal `user`@`host` pairs match when they equal the session identity. Starting in Percona Server for MySQL 8.4.4, wildcard characters (`%` and `_`) are allowed in the host portion of the assignment string (see [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name)); pattern matching matches the behavior when you create the row through that function.

Keep assignments non-overlapping when you use wildcards. If several rows could match one connection, precedence is not specified here—prefer explicit literal `user`@`host` rows (or one clear pattern plus a `'%'` default) and confirm behavior on a test server.

With no matching row, the component uses the default assignment: the account registered with `audit_log_filter_set_user()` using `%` as the user name (see [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name)).

If neither a matching row nor a default exists, the component skips event processing for that connection.

A specific account row overrides the default: if both `admin`@`localhost` and `%` have filters, `admin` from `localhost` uses the `admin`@`localhost` filter, not the default.

You can bind filters to named accounts or remove those bindings.

To clear a binding, unassign the filter or assign a different one. How sessions refresh when assignments change is described under [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name) and [`audit_log_filter_remove_filter()`](audit-log-filter-variables.md#audit_log_filter_remove_filterfilter_name).

## set_filter options and available filters

JSON layout (`filter`, `class`, nested rules, examples) is in [Write audit_log_filter definitions](write-filter-definitions.md). The authoritative list of class names, event subclass names, and per-class field names that `audit_log_filter_set_filter()` accepts appears in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md). This section lists the keys that may appear at each level of a filter definition.

### Filter-level keys

| Key | Role |
|---|---|
| `log`   | Boolean global default. `true` enables logging everywhere not turned off by a more specific rule; `false` requires per-class/per-event `log` overrides to write anything. |
| `class` | One class block or an array of class blocks. Each block sets `"name"` to an event class (`general`, `connection`, `table_access`, `message`; plus `global_variable`, `command`, `query`, `stored_program`, `authentication`, `parse` when `event_mode=FULL`). |
| `id`    | Optional filter identifier. Referenced by `activate` / `ref` when one filter swaps itself for another mid-session (see [Replace a filter dynamically](write-filter-definitions.md#replace-a-filter-dynamically)). |

### Class-block keys

| Key | Role |
|---|---|
| `name`  | The class name. Use one of the values listed in the preceding section. |
| `log`   | Optional. Boolean, or a condition that narrows matches by event-field values. |
| `event` | Optional. One event block or an array. Each block names one subclass and can carry its own `log`, `abort`, `print`, or nested `filter`. Subclasses depend on the class. For `table_access`: `read`, `insert`, `update`, `delete`. For `connection`: `connect`, `disconnect`, `change_user`, plus `pre_authenticate` in `FULL`. See the [event and subclass table](write-filter-definitions.md#list-of-event-and-subclass-options) and [definition fields](audit-log-filter-definition-fields.md). |
| `print` | Optional. Field-replacement rule. The component limits replacement to four class/field pairs (`general`/`general_query.str`, `table_access`/`query.str`, `query`/`query.str`, `parse`/`query.str`) with the `query_digest` function. See [Redact audit log fields](redact-audit-log-fields.md). |

### Event-block keys

| Key | Role |
|---|---|
| `name`   | Subclass name. May be a string (one subclass) or an array (several). |
| `log`    | Optional. Boolean, or a condition over event fields. |
| `abort`  | Optional. Boolean or condition that blocks execution of matching statements — see [Block statements with an audit log filter](block-statements-with-audit-filter.md). |
| `print`  | Optional. Field-replacement rule scoped to this event — see [Redact audit log fields](redact-audit-log-fields.md). |
| `filter` | Optional. Nested subfilter used with `activate` / `ref` for dynamic filter swapping — see [Replace a filter dynamically](write-filter-definitions.md#replace-a-filter-dynamically). |

### Conditions

`log` and `abort` accept a Boolean (`true` / `false`) or a condition built from these items:

| Item | Role |
|---|---|
| `field`    | `{ "name": "<event-field>", "value": <value> }`. Compares an event field such as `user.str`, `host.str`, `table_database.str`, `table_name.str`, `status`, `general_command.str`, or `general_sql_command.str`. Per-class fields are listed in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md). |
| `variable` | `{ "name": "<server-variable>", "value": <value> }`. Compares a predefined variable such as `audit_log_connection_policy_value`. |
| `function` | `{ "name": "<function>", "args": [...] }`. Calls a built-in. The Percona implementation supports two functions: `string_find` and `query_digest` — see [Reference predefined functions](write-filter-definitions.md#reference-predefined-functions). |
| `and`      | Array of sub-conditions; all must be true. |
| `or`       | Array of sub-conditions; at least one must be true. |
| `not`      | A single sub-condition; true when the inner evaluates to false. |

Field-value typing (JSON numbers for integer fields such as `status`, strings for `*.str` fields, and `"::tcp/ip"`-style symbolic constants for `connection_type`) is covered under [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) and in the [`connection`](audit-log-filter-definition-fields.md#connection) section of [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

### Examples

Start from a single-class filter that logs every `connection` event the component sees:

```sql
SELECT audit_log_filter_set_filter('log_connection', '{
  "filter": {
    "class": { "name": "connection" }
  }
}');
```

Narrow to a single subclass by nesting `event` inside the class block (not as a sibling of `class`):

```sql
SELECT audit_log_filter_set_filter('log_connect_only', '{
  "filter": {
    "class": {
      "name": "connection",
      "event": { "name": "connect" }
    }
  }
}');
```

Narrow further by adding a `log` condition that tests event fields — here, log `connect` events from only two accounts, originating from one host:

```sql
SELECT audit_log_filter_set_filter('log_admin_connect', '{
  "filter": {
    "class": {
      "name": "connection",
      "event": {
        "name": "connect",
        "log": {
          "and": [
            { "field": { "name": "user.str", "value": ["admin", "developer"] } },
            { "field": { "name": "host.str", "value": "10.0.0.5" } }
          ]
        }
      }
    }
  }
}');
```

For full authoring detail, see:

* [Write audit_log_filter definitions](write-filter-definitions.md) — inclusive and exclusive patterns, conditions, and the complete grammar
* [Audit Log Filter definition fields](audit-log-filter-definition-fields.md) — canonical class, event, and field names validation accepts
* [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) — `REDUCED` versus `FULL` class sets

## Additional reading

* [Write audit_log_filter definitions](write-filter-definitions.md)
* [Audit Log Filter definition fields](audit-log-filter-definition-fields.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter quickstart](audit-log-filter-quickstart.md)
* [Audit Log Filter restrictions](audit-log-filter-restrictions.md)
