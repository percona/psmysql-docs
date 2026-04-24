# Audit Log Filter overview

The Audit Log Filter component records, audits, and can block matching connections or statements on the configured server.

With the component enabled, the server writes an audit log file. The file captures connection events, executed statements, and the schemas that sessions touched.

## Architecture

The following diagram shows how the Audit Log Filter component sits between the server core, the filter rules, and the audit output.

![Audit Log Filter component architecture](_static/audit-log-filter-arch.png)

### Why the filter component

The component replaces the [legacy audit log plugin](audit-log-plugin.md). The design meets three goals that the plugin could not:

* Change rules without restarting the server.

    Filter definitions and account assignments live in `mysql` system tables. Updates through [`audit_log_filter_set_filter()`](audit-log-filter-variables.md) and [`audit_log_filter_set_user()`](audit-log-filter-variables.md) take effect on new sessions and reloads. The server stays online. The legacy plugin required `audit_log_*` system-variable changes. Those changes often required a restart or plugin reinstall to adjust scope.

* Scope audits per account, not globally.

    Each row in `mysql.audit_log_user` binds a user or user pattern to a named filter. The rows let you audit `admin@%` and `app@%` differently on the same instance. The legacy plugin offered only global include and exclude lists (`audit_log_include_accounts` and `audit_log_exclude_accounts`) on top of a single policy preset.

* Express rules as data, not as knob settings.

    Filter definitions are JSON documents. A rule can match an event, a class, a subclass, or a specific field value. You combine matches with `and`, `or`, and `not`. Rules can call predefined variables and functions, block execution with `abort`, and redact statement text in place with `print` and `replace`. The legacy plugin had policy presets (`LOGINS`, `QUERIES`, `ALL`) with coarser control and no blocking or redaction.

The design delivers a secondary benefit. Events that a filter drops never reach the formatter or the writer. The server therefore avoids the cost of auditing every event and discarding most of the data at the sink. Combined with per-account scoping, operators can raise audit detail on sensitive accounts without paying for verbose logging elsewhere.

See [Write audit_log_filter definitions](write-filter-definitions.md) for the JSON grammar, [Block statements with an audit log filter](block-statements-with-audit-filter.md) for `abort`, and [Redact audit log fields](redact-audit-log-fields.md) for `print` and `replace`.

## Audit data flow

The following diagram traces audit events from the server through filtering and formatting into the log (file, syslog, or another handler).

![Audit Log Filter data flow](_static/audit-data-flow.png)

Set [`audit_log_filter.format`](audit-log-filter-variables.md#audit_log_filterformat) at startup. [Audit Log Filter file format overview](audit-log-filter-formats.md) compares JSONL (default), JSON, and NEW.

[`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) selects the event classes the component audits. The default is `REDUCED`. `FULL` enables every class the component supports, including classes beyond the four core classes. The variable reference lists the full class sets, validation rules, and behavior on older releases.

The component stores filter definitions and account assignments in the `mysql` system database. Set [`audit_log_filter.database`](audit-log-filter-variables.md#audit_log_filterdatabase) at startup to use a different database.

You need `AUDIT_ADMIN` to administer the Audit Log Filter component.

## Privileges

The server defines the Audit Log Filter privileges at startup.

### `AUDIT_ADMIN`

Grantees of `AUDIT_ADMIN` can configure the component.

### `AUDIT_ABORT_EXEMPT`

A filter may include an `abort` rule that blocks matching statements. To bypass those aborts, an account needs both `SYSTEM_USER` and the global `AUDIT_ABORT_EXEMPT` privilege granted on `*.*`.

Only that pair lets matching statements run when a filter would otherwise abort the statement. The component still writes those statements to the audit log.

## Audit log filter tables

The Audit Log Filter component uses `mysql` system tables on `InnoDB`. The tables hold account assignments and filter JSON. Point the component at another database through `audit_log_filter.database` when the server starts.

The `audit_log_filter` table stores named filter definitions:

| Column name | Description                                |
|-------------|--------------------------------------------|
| NAME        | Filter name                                |
| FILTER      | JSON filter definition linked to the name  |

The `audit_log_user` table maps accounts to filters:

| Column name  | Description                    |
|--------------|--------------------------------|
| USER         | MySQL account user part        |
| HOST         | MySQL account host part        |
| FILTERNAME   | Name of the assigned filter    |

### Filter storage hierarchy

The following diagram shows how rows in `audit_log_filter` map to `audit_log_user`, including the default `%` account.

![Audit Log Filter storage hierarchy](_static/audit-filter-hierarchy.png)

On connect, the component loads one filter definition from the matching `USER`/`HOST` row in `mysql.audit_log_user`. If no row matches, the component falls back to the default account (`%`). A concrete account such as `admin`@`localhost` overrides a `%` assignment.

Rules inside the filter's JSON apply after load. For example, `log` conditions that test `user.str` or `host.str` with `field` items narrow which events get written. The rules do not act as a second assigned filter. See [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md#using-the-audit-log-filter-functions) for assignment order and wildcards. See [Write audit_log_filter definitions](write-filter-definitions.md#test-event-field-values) for the JSON grammar that `log` conditions use.

## Additional reading

* [Install the audit log filter](install-audit-log-filter.md)

* [Audit Log Filter quickstart](audit-log-filter-quickstart.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)

* [Write audit_log_filter definitions](write-filter-definitions.md)

* [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md)

* [Audit Log Filter file format overview](audit-log-filter-formats.md)

* [Migrate to the audit log filter component](migrate-to-audit-log-filter-component.md) — variable mapping, policy translation, worked example, and cutover for either audit plugin

* [Upgrade components](upgrade-components.md) — general plugin-to-component transition procedure

* [Audit log plugin](audit-log-plugin.md) — deprecated plugin reference
