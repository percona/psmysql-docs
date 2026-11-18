> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Migrate to the audit log filter component

Percona Server for MySQL 8.4 replaces two legacy audit sources — the `audit_log` plugin and the transitional `audit_log_filter` plugin — with `component_audit_log_filter`. This page covers migration from either source: it maps plugin configuration to the component’s system variables and filter JSON, and walks through a safe cutover.

Before you start, read:

- [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html) — timing, general procedure, and which plugins transition before vs. after the server upgrade.
- [Audit Log Filter overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.html) — what the component is and why it replaces the plugin.
- [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html) — install script, component URN, and the `mysql.audit_log_filter` / `mysql.audit_log_user` tables.

Note

The component and the plugin use different system variables and a different on-disk format. Do not enable both at the same time, and do not set `audit_log_*` plugin variables on a server running the component. See the [deprecation notice](https://docs.percona.com/percona-server/8.4/audit-log-plugin.html) on the plugin page.

## Which source are you migrating from?

Two legacy sources exist. The target is the same (`component_audit_log_filter`), but the starting point differs:

| Source                                                                               | Recommended path                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `audit_log` plugin (pre-8.4 installs, still available in 8.4 as a deprecated plugin) | Upgrade to 8.4, install the component, translate `audit_log_*` variables to filter JSON, validate in parallel, then uninstall the plugin.                                                                          |
| `audit_log_filter` plugin (transitional, 8.0 and early 8.4 builds)                   | Upgrade to 8.4 first, then transition to the component per [Upgrade from plugins to components → Transition after upgrade](https://docs.percona.com/percona-server/8.4/upgrade-components.html#transition-timing). |

The detailed mapping in the following sections targets the `audit_log` plugin, because its configuration model differs most from the component. The plugin model uses global `audit_log_*` variables and policy presets. If you are migrating from the `audit_log_filter` plugin, the filter JSON you already wrote continues to work unchanged. Your migration reduces to a shorter path:

1. Upgrade the server to 8.4.
1. Uninstall the plugin.
1. Run the component install script (see [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html)) — this creates `mysql.audit_log_filter` and `mysql.audit_log_user` and registers the component.
1. Re-apply each filter with [`audit_log_filter_set_filter()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filter_set_filterfilter_name-definition) and re-assign accounts with `audit_log_filter_set_user()`. If you exported the plugin’s filter/user tables, those rows can be re-inserted directly.
1. Move non-filter settings (file path, format, rotation, syslog) from `audit_log_filter_*` plugin variables to the `audit_log_filter.*` component variables listed in the [variable mapping](#option-and-variable-mapping).

See also [Upgrade from plugins to components → Transition after upgrade](https://docs.percona.com/percona-server/8.4/upgrade-components.html#transition-timing).

## What changes, at a glance

- Configuration moves from global `audit_log_*` system variables into JSON filter definitions stored in `mysql.audit_log_filter`, plus per-account assignments in `mysql.audit_log_user`.
- Scope moves from a single global include/exclude list to per-account assignments — `admin@%` and `app@%` can use different filters on the same server.
- Rule changes no longer require a restart or plugin reinstall: update the JSON with `audit_log_filter_set_filter()` and the next session picks it up.
- Log format names shift: the plugin’s `OLD` / `NEW` / `JSON` / `CSV` become the component’s `OLD` / `NEW` / `JSON` / `JSONL`. The component does not produce `CSV` output.
- The `audit_log_handler = SYSLOG` path becomes `audit_log_filter.handler = SYSLOG` with the same syslog sub-variables renamed.

## Migration steps

1. Inventory the current configuration. On the 8.0 server, or on a plugin-enabled 8.4 server, capture the legacy settings:

```
SHOW VARIABLES LIKE 'audit_log_%';
```

Save the output. You will translate each non-default value into either a component variable, a filter JSON rule, or an `audit_log_filter_set_user()` call.

1. Upgrade the server to 8.4 by following [Upgrade procedures](https://docs.percona.com/percona-server/8.4/upgrade-procedures.html). The `audit_log` plugin remains loadable in 8.4, so the old log keeps flowing during the transition.
1. Install the component per [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html). The install script creates `mysql.audit_log_filter` and `mysql.audit_log_user`, then runs `INSTALL COMPONENT`.
1. Translate configuration using the two mapping tables in the following sections. Apply non-filter settings (file path, format, rotation, syslog) as component variables. Apply scope settings (policy, include/exclude lists) as a filter definition plus user assignments.
1. Run in parallel. This step is optional but recommended. With both the plugin and the component loaded, verify that the events you care about appear in the component’s log. Compare record types, SQL text, and redactions.
1. Cut over. Uninstall the plugin with `UNINSTALL PLUGIN audit_log;`, remove `audit_log_*` entries from `my.cnf`, and leave the component as the sole audit writer. If you also had the transitional `audit_log_filter` plugin loaded, uninstall it as well.
1. Verify. Log in as a subject account, execute a representative statement, and read the new log with [`audit_log_read()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_read) or by opening the file.

## Option and variable mapping

The following maps plugin system variables (left) to component system variables (right). Anything not listed has no direct equivalent because it is subsumed by the filter JSON grammar.

| Plugin variable                                               | Component equivalent                                                                                                                                                                                                                                                                 | Notes                                                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `audit_log_file`                                              | [`audit_log_filter.file`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterfile)                                                                                                                                                          | Default file name and data-directory placement differ; see [Log file naming](https://docs.percona.com/percona-server/8.4/audit-log-filter-naming.html).                                                                                                                                      |
| `audit_log_format` (`OLD`/`NEW`/`JSON`/`CSV`)                 | [`audit_log_filter.format`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterformat) (`OLD`/`NEW`/`JSON`/`JSONL`)                                                                                                                         | `CSV` is not supported by the component. For line-delimited ingest, use `JSONL` (see [JSON and JSONL](https://docs.percona.com/percona-server/8.4/audit-log-filter-json.html)).                                                                                                              |
| `audit_log_strategy`                                          | [`audit_log_filter.strategy`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterstrategy)                                                                                                                                                  | Same `ASYNCHRONOUS` / `PERFORMANCE` / `SEMISYNCHRONOUS` / `SYNCHRONOUS` trade-offs.                                                                                                                                                                                                          |
| `audit_log_buffer_size`                                       | [`audit_log_filter.buffer_size`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterbuffer_size)                                                                                                                                            | Applies to `ASYNCHRONOUS` / `PERFORMANCE`.                                                                                                                                                                                                                                                   |
| `audit_log_rotate_on_size`                                    | [`audit_log_filter.rotate_on_size`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterrotate_on_size)                                                                                                                                      | Size-based rotation.                                                                                                                                                                                                                                                                         |
| `audit_log_rotations`                                         | [`audit_log_filter.prune_seconds`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterprune_seconds) or [`audit_log_filter.max_size`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filtermax_size) | The component does not keep a fixed file count. Choose age-based pruning (`prune_seconds`) or total-size pruning (`max_size`); the two options are mutually exclusive. Convert “keep N files” to an approximate age or total-size budget (for example, `rotate_on_size` × N for `max_size`). |
| `audit_log_flush`                                             | [`audit_log_rotate()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_rotate)                                                                                                                                                                 | Manual rotation uses a UDF call rather than a variable toggle.                                                                                                                                                                                                                               |
| `audit_log_handler` (`FILE` / `SYSLOG`)                       | [`audit_log_filter.handler`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterhandler)                                                                                                                                                    | Same two values.                                                                                                                                                                                                                                                                             |
| `audit_log_syslog_ident`                                      | [`audit_log_filter.syslog_tag`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filtersyslog_tag)                                                                                                                                              | Renamed.                                                                                                                                                                                                                                                                                     |
| `audit_log_syslog_facility`                                   | [`audit_log_filter.syslog_facility`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filtersyslog_facility)                                                                                                                                    | —                                                                                                                                                                                                                                                                                            |
| `audit_log_syslog_priority`                                   | [`audit_log_filter.syslog_priority`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filtersyslog_priority)                                                                                                                                    | —                                                                                                                                                                                                                                                                                            |
| `audit_log_policy`                                            | *(filter JSON)*                                                                                                                                                                                                                                                                      | Translate to class selection — see [Translating audit_log_policy to filter JSON](#translating-audit_log_policy-to-filter-json).                                                                                                                                                              |
| `audit_log_include_accounts` / `audit_log_exclude_accounts`   | *(filter JSON + `audit_log_filter_set_user()`)*                                                                                                                                                                                                                                      | Per-account assignment replaces global lists — see [Translating include/exclude lists](#translating-includeexclude-lists).                                                                                                                                                                   |
| `audit_log_include_commands` / `audit_log_exclude_commands`   | *(filter JSON)*                                                                                                                                                                                                                                                                      | Use `log` conditions that test `general_sql_command.str`.                                                                                                                                                                                                                                    |
| `audit_log_include_databases` / `audit_log_exclude_databases` | *(filter JSON)*                                                                                                                                                                                                                                                                      | Use `log` conditions that test `table_database.str` in `table_access`.                                                                                                                                                                                                                       |

Component-only features that have no plugin counterpart include block-on-match (`abort`), field redaction (`print` / `replace`), predefined variables and functions inside conditions, and dynamic filter swapping (`activate` / `ref`). See [Write filter definitions](https://docs.percona.com/percona-server/8.4/write-filter-definitions.html) and its sub-pages.

## Translating `audit_log_policy` to filter JSON

`audit_log_policy` gated what the plugin recorded. The component expresses the same four choices as filter definitions:

| Plugin policy | Equivalent filter definition                                                                                                                                                                                          |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ALL`         | Log everything the component sees (respects [`audit_log_filter.event_mode`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterevent_mode)): `{ "filter": { "log": true } }` |
| `LOGINS`      | `{ "filter": { "class": { "name": "connection" } } }`                                                                                                                                                                 |
| `QUERIES`     | `{ "filter": { "class": [ { "name": "general" }, { "name": "table_access" } ] } }`                                                                                                                                    |
| `NONE`        | Either do not assign a filter to the account, or bind an empty filter: `{ "filter": {} }`                                                                                                                             |

Install any of these with [`audit_log_filter_set_filter()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filter_set_filterfilter_name-definition) and assign them with [`audit_log_filter_set_user()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html). For example:

```
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
SELECT audit_log_filter_set_user('%',        'log_all');
```

## Translating include/exclude lists

The plugin filtered globally. The component filters per account (via `audit_log_user`) and per event (via `log` conditions that compare event fields). Most migrations combine both.

### Accounts

Plugin:

```
SET GLOBAL audit_log_include_accounts = 'app@%,admin@localhost';
```

Component — assign a logging filter to the two accounts and leave the default `%` with no filter (or an empty filter):

```
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
SELECT audit_log_filter_set_user('app@%',          'log_all');
SELECT audit_log_filter_set_user('admin@localhost','log_all');
```

Plugin exclude list, inverted:

```
SET GLOBAL audit_log_exclude_accounts = 'monitor@%';
```

Component — keep the default `%` assigned to a logging filter and assign `monitor@%` to an empty filter (or leave it unassigned if `%` has no filter):

```
SELECT audit_log_filter_set_filter('no_log', '{ "filter": {} }');
SELECT audit_log_filter_set_user('monitor@%', 'no_log');
```

### Commands

Plugin:

```
SET GLOBAL audit_log_include_commands = 'select,insert,update,delete';
```

Component — narrow the `general` class with a `log` condition that tests `general_sql_command.str`:

```
SELECT audit_log_filter_set_filter('log_dml', '{
  "filter": {
    "class": {
      "name": "general",
      "log": {
        "field": {
          "name": "general_sql_command.str",
          "value": ["select", "insert", "update", "delete"]
        }
      }
    }
  }
}');
```

For exclusion, wrap the condition in `not`.

### Databases

Plugin:

```
SET GLOBAL audit_log_include_databases = 'app,reports';
```

Component — narrow `table_access` by `table_database.str`:

```
SELECT audit_log_filter_set_filter('log_app_reports', '{
  "filter": {
    "class": {
      "name": "table_access",
      "log": {
        "field": {
          "name": "table_database.str",
          "value": ["app", "reports"]
        }
      }
    }
  }
}');
```

For a complete grammar reference (field names, logical operators, variables, functions), see [Write filter definitions](https://docs.percona.com/percona-server/8.4/write-filter-definitions.html) and [Definition fields reference](https://docs.percona.com/percona-server/8.4/audit-log-filter-definition-fields.html).

## Worked example

Starting plugin configuration in `my.cnf`:

```
[mysqld]
plugin-load-add          = audit_log.so
audit_log_format         = JSON
audit_log_policy         = ALL
audit_log_include_accounts = app@%,admin@localhost
audit_log_exclude_commands = set_option
audit_log_rotate_on_size = 104857600
audit_log_rotations      = 10
```

After upgrading to 8.4 and running `audit_log_filter_linux_install.sql`, replace it with:

```
[mysqld]
audit_log_filter.format         = JSON
audit_log_filter.rotate_on_size = 104857600
audit_log_filter.max_size       = 1048576000
```

The plugin’s `audit_log_rotations = 10` with `audit_log_rotate_on_size = 104857600` (100 MiB) maps to a 1 GiB total-size cap (`10 × 104857600`). Age-based retention with [`audit_log_filter.prune_seconds`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterprune_seconds) is an alternative; do not set both `max_size` and `prune_seconds` — the component accepts only one at a time.

Then define the filter and assign accounts:

```
SELECT audit_log_filter_set_filter('log_all_except_set_option', '{
  "filter": {
    "class": [
      { "name": "connection" },
      { "name": "table_access" },
      {
        "name": "general",
        "log": {
          "not": {
            "field": { "name": "general_sql_command.str", "value": "set_option" }
          }
        }
      }
    ]
  }
}');

SELECT audit_log_filter_set_user('app@%',           'log_all_except_set_option');
SELECT audit_log_filter_set_user('admin@localhost', 'log_all_except_set_option');
```

Accounts that do not match `app@%` or `admin@localhost` — and that have no explicit assignment to the default `%` filter — are not audited, which reproduces the plugin’s include-list behavior.

## Cutover and verification

1. Confirm the component is live:

   ```
   SELECT * FROM mysql.component WHERE component_urn = 'file://component_audit_log_filter';
   ```

1. Log in as a subject account, run a representative statement, and read the new log:

   ```
   SELECT audit_log_read('{}');
   ```

   See [Read log files](https://docs.percona.com/percona-server/8.4/reading-audit-log-filter-files.html).

1. Uninstall the legacy plugin and clear its settings from `my.cnf`:

   ```
   UNINSTALL PLUGIN audit_log;
   ```

1. Rotate once so new writes go to a fresh file under the component’s naming scheme:

   ```
   SELECT audit_log_rotate();
   ```

1. For any pre-existing plugin log files you want to keep, archive them. The component does not ingest them, but you can run [`filter_audit_log_filter_files`](https://docs.percona.com/percona-server/8.4/filter-audit-log-filter-files.html) to post-process component logs.

## Known caveats

- Log content changes slightly even when you keep the same format. Some statements that the 8.0 plugin did not record appear in 8.4 logs because the server sends additional events. The plugin page calls out the `SELECT $$` example. Percona does not plan to backport format changes to match 8.0 output.
- The component stores state in `mysql.audit_log_filter` and `mysql.audit_log_user`. Back up those tables before making bulk changes, and include them in your normal `mysql` database backups.
- Lifecycle events (`server_startup`, `server_shutdown`, and the `audit` class itself) are not valid filter targets — see [Definition fields reference](https://docs.percona.com/percona-server/8.4/audit-log-filter-definition-fields.html#audit-log-filter-definition-fields).
- `audit_log_filter.event_mode` defaults to `REDUCED`. If you relied on plugin logging for classes beyond `connection`, `general`, `table_access`, and `message`, set `event_mode = FULL` in `my.cnf` before you start the server. Changing the value on a running server creates a window where in-flight events are evaluated inconsistently against the new mode, and audit output during that window cannot be reconciled after the fact. If a restart is not possible, follow the `SET GLOBAL` with [`audit_log_filter_flush()`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filter_flush) inside a maintenance window. For the full caveat, see [`audit_log_filter.event_mode`](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html#audit_log_filterevent_mode).

## Additional reading

- [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html)
- [Audit Log Filter overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.html)
- [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.html)
- [Write filter definitions](https://docs.percona.com/percona-server/8.4/write-filter-definitions.html)
- [Functions, options, and variables](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.html)
- [Audit log plugin](https://docs.percona.com/percona-server/8.4/audit-log-plugin.html) — legacy reference, with the deprecation notice
