> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Migrate to the audit log filter component

Percona Server for MySQL 9.7 replaces two legacy audit sources with `component_audit_log_filter`. The legacy sources are the `audit_log` plugin and the transitional `audit_log_filter` plugin.

This page covers migration from either source. The page maps plugin configuration to the component’s system variables and filter JSON, and walks through a safe cutover.

Before you start, read:

- [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md) — timing, general procedure, and which plugins transition before or after the server upgrade.
- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.md) — what the component is and why it replaces the plugin.
- [Install the audit log filter](https://docs.percona.com/percona-server/9.7/install-audit-log-filter.md) — install script, component URN, and the `mysql.audit_log_filter` / `mysql.audit_log_user` tables.

Note

The component and the plugin use different system variables and a different on-disk format. Do not enable both at the same time, and do not set `audit_log_*` plugin variables on a server running the component. See the [removal notice](https://docs.percona.com/percona-server/9.7/audit-log-plugin.md) on the plugin page.

## Which source are you migrating from?

Two legacy sources exist. The target is `component_audit_log_filter` in both cases. The starting point differs:

| Source                                                             | Recommended path                                                                                                                                                                                                            |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `audit_log` plugin (deprecated in 8.4, removed in 9.7)             | On 8.4, before upgrading: install the component, translate `audit_log_*` variables to filter JSON, validate, uninstall the plugin, and remove the plugin options from `my.cnf`. Then upgrade to 9.7.                        |
| `audit_log_filter` plugin (transitional, 8.0 and early 8.4 builds) | Upgrade to 9.7 first, then transition to the component per [Upgrade from plugins to components → Transition after upgrade](https://docs.percona.com/percona-server/9.7/upgrade-components.md#transition-after-the-upgrade). |

The following detailed mapping targets the `audit_log` plugin because the plugin’s configuration model — global `audit_log_*` variables and policy presets — differs most from the component. If you are migrating from the `audit_log_filter` plugin, the filter JSON you already wrote continues to work unchanged; the migration reduces to a shorter path:

1. Upgrade the server to 9.7.
1. Uninstall the plugin.
1. Run the component install script. See [Install the audit log filter](https://docs.percona.com/percona-server/9.7/install-audit-log-filter.md). The script creates `mysql.audit_log_filter` and `mysql.audit_log_user` and registers the component.
1. Re-apply each filter with [`audit_log_filter_set_filter()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) and re-assign accounts with [`audit_log_filter_set_user()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md). When you exported the plugin’s filter and user tables, those rows can be re-inserted directly.
1. Move non-filter settings (file path, format, rotation, syslog) from `audit_log_filter_*` plugin variables to the `audit_log_filter.*` component variables listed in the [variable mapping](#option-and-variable-mapping).

See also [Upgrade from plugins to components → Transition after upgrade](https://docs.percona.com/percona-server/9.7/upgrade-components.md#transition-after-the-upgrade).

## What changes, at a glance

- Configuration moves from global `audit_log_*` system variables into JSON filter definitions stored in `mysql.audit_log_filter`, plus per-account assignments in `mysql.audit_log_user`.
- Scope moves from a single global include/exclude list to per-account assignments. `admin@%` and `app@%` can use different filters on the same server.
- Rule changes require no restart or plugin reinstall. Update the JSON with `audit_log_filter_set_filter()`, and the next session applies the change.
- Log format names shift. The plugin’s `OLD`, `NEW`, `JSON`, and `CSV` map to the component’s `JSONL` (default), `JSON`, and `NEW`. The component does not emit `OLD` XML or `CSV`.
- The `audit_log_handler = SYSLOG` path becomes `audit_log_filter.handler = SYSLOG`. The syslog sub-variables use the same values under renamed component names.

## Migration steps

Migrate from the `audit_log` plugin before upgrading to 9.7

The `audit_log` plugin is removed in 9.7. The plugin library `audit_log.so` is not built or packaged. Complete the following migration steps on the 8.4 server before upgrading. Otherwise, the upgrade fails in one of the following ways:

- If `my.cnf` still contains `plugin-load-add=audit_log.so` or plugin options such as `audit_log_format`, the 9.7 server aborts at startup with `unknown variable 'audit_log_format=JSON'`. The server aborts after the data dictionary upgrade has completed, so the 8.4 server can no longer start on that data directory.
- If the plugin was installed with `INSTALL PLUGIN` and no plugin options are set, 9.7 starts, logs `Couldn't load plugin named 'audit_log'` at every startup, and runs without auditing.

If you already upgraded with the plugin registered, `UNINSTALL PLUGIN audit_log` fails on 9.7 with `ERROR 1305`. Remove the registration with `DELETE FROM mysql.plugin WHERE name='audit_log';` and then install the component.

1. **Inventory the current configuration.** On the plugin-enabled server, capture the legacy settings:

```sql
SHOW VARIABLES LIKE 'audit_log_%';
```

Save the output. Translate each non-default value into a component variable, a filter JSON rule, or an `audit_log_filter_set_user()` call.

1. **Stay on 8.4.** The `audit_log` plugin is not available in 9.7, so complete steps 3 through 7 on the 8.4 server. 8.4 includes `component_audit_log_filter`.
1. **Install the component** per [Install the audit log filter](https://docs.percona.com/percona-server/9.7/install-audit-log-filter.md). The install script creates `mysql.audit_log_filter` and `mysql.audit_log_user`, then runs `INSTALL COMPONENT`.
1. **Translate configuration** using the two mapping tables that follow. Apply non-filter settings (file path, format, rotation, syslog) as component variables. Apply scope settings (policy, include/exclude lists) as a filter definition plus user assignments.
1. **Run in parallel (optional, recommended).** Load both the plugin and the component. Verify that the events you care about appear in the component’s log. Compare record types, SQL text, and redactions.
1. **Cut over.** Uninstall the plugin (`UNINSTALL PLUGIN audit_log;`), remove `plugin-load-add=audit_log.so` and the plugin’s `audit_log_*` entries from `my.cnf`, and leave the component as the sole audit writer. Keep the component’s `audit_log_filter.*` variables. When you also had the transitional `audit_log_filter` plugin loaded, uninstall that plugin as well.
1. **Verify.** Log in as a subject account, execute a representative statement, and read the new log with [`audit_log_read()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_read) or by opening the file.
1. **Upgrade the server to 9.7** by following [Upgrade procedures](https://docs.percona.com/percona-server/9.7/upgrade-procedures.md).

## Option and variable mapping

The following table maps plugin system variables (left) to component system variables (right). Variables not listed have no direct equivalent because the filter JSON grammar subsumes them.

| Plugin variable                                               | Component equivalent                                                                                                                                                                                                                                                            | Notes                                                                                                                                                                                                                       |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `audit_log_file`                                              | [`audit_log_filter.file`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterfile)                                                                                                                                                       | Default file name and data-directory placement differ; see [Log file naming](https://docs.percona.com/percona-server/9.7/audit-log-filter-naming.md).                                                                       |
| `audit_log_format` (`OLD`/`NEW`/`JSON`/`CSV`)                 | [`audit_log_filter.format`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterformat) (`JSONL`/`JSON`/`NEW`)                                                                                                                            | Component default is `JSONL`. The component does not emit `OLD` XML or `CSV`; pick `NEW` to stay on XML or use `JSONL`/`JSON` (see [JSON and JSONL](https://docs.percona.com/percona-server/9.7/audit-log-filter-json.md)). |
| `audit_log_strategy`                                          | [`audit_log_filter.strategy`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterstrategy)                                                                                                                                               | Same `ASYNCHRONOUS` / `PERFORMANCE` / `SEMISYNCHRONOUS` / `SYNCHRONOUS` trade-offs.                                                                                                                                         |
| `audit_log_buffer_size`                                       | [`audit_log_filter.buffer_size`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterbuffer_size)                                                                                                                                         | Applies to `ASYNCHRONOUS` / `PERFORMANCE`.                                                                                                                                                                                  |
| `audit_log_rotate_on_size`                                    | [`audit_log_filter.rotate_on_size`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterrotate_on_size)                                                                                                                                   | Size-based rotation.                                                                                                                                                                                                        |
| `audit_log_rotations`                                         | [`audit_log_filter.prune_seconds`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterprune_seconds) + [`audit_log_filter.max_size`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filtermax_size) | The component prunes by age and total size instead of a fixed file count. Convert “keep N files” to an age or total-size budget.                                                                                            |
| `audit_log_flush`                                             | [`audit_log_rotate()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_rotate)                                                                                                                                                              | Manual rotation uses a UDF call instead of a variable toggle.                                                                                                                                                               |
| `audit_log_handler` (`FILE` / `SYSLOG`)                       | [`audit_log_filter.handler`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterhandler)                                                                                                                                                 | Same two values.                                                                                                                                                                                                            |
| `audit_log_syslog_ident`                                      | [`audit_log_filter.syslog_tag`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filtersyslog_tag)                                                                                                                                           | Renamed.                                                                                                                                                                                                                    |
| `audit_log_syslog_facility`                                   | [`audit_log_filter.syslog_facility`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filtersyslog_facility)                                                                                                                                 | —                                                                                                                                                                                                                           |
| `audit_log_syslog_priority`                                   | [`audit_log_filter.syslog_priority`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filtersyslog_priority)                                                                                                                                 | —                                                                                                                                                                                                                           |
| `audit_log_policy`                                            | *(filter JSON)*                                                                                                                                                                                                                                                                 | Translate to class selection — see Translating `audit_log_policy`.                                                                                                                                                          |
| `audit_log_include_accounts` / `audit_log_exclude_accounts`   | *(filter JSON + `audit_log_filter_set_user()`)*                                                                                                                                                                                                                                 | Per-account assignment replaces global lists — see [Translating include / exclude account lists](#translating-includeexclude-lists).                                                                                        |
| `audit_log_include_commands` / `audit_log_exclude_commands`   | *(filter JSON)*                                                                                                                                                                                                                                                                 | Use `log` conditions that test `general_sql_command.str`.                                                                                                                                                                   |
| `audit_log_include_databases` / `audit_log_exclude_databases` | *(filter JSON)*                                                                                                                                                                                                                                                                 | Use `log` conditions that test `table_database.str` in `table_access`.                                                                                                                                                      |

Component-only features with no plugin counterpart include:

- Block-on-match with `abort`
- Field redaction with `print` and `replace`
- Predefined variables and functions inside conditions
- Dynamic filter swapping with `activate` and `ref`

See [Write filter definitions](https://docs.percona.com/percona-server/9.7/write-filter-definitions.md) and the sub-pages.

## Translating `audit_log_policy` to filter JSON

`audit_log_policy` gated what the plugin recorded. The component expresses the same four choices as filter definitions:

| Plugin policy | Equivalent filter definition                                                                                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ALL`         | Log everything the component sees (respects [`audit_log_filter.event_mode`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filterevent_mode)): `{ "filter": { "log": true } }` |
| `LOGINS`      | `{ "filter": { "class": { "name": "connection" } } }`                                                                                                                                                               |
| `QUERIES`     | `{ "filter": { "class": [ { "name": "general" }, { "name": "table_access" } ] } }`                                                                                                                                  |
| `NONE`        | Either do not assign a filter to the account, or bind an empty filter: `{ "filter": {} }`                                                                                                                           |

Install any of these with [`audit_log_filter_set_filter()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) and assign them with [`audit_log_filter_set_user()`](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md). For example:

```sql
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
SELECT audit_log_filter_set_user('%',        'log_all');
```

## Translating include/exclude lists

The plugin filtered globally. The component filters per account through `audit_log_user` and per event through `log` conditions that compare event fields. Most migrations combine both.

### Accounts

Plugin:

```sql
SET GLOBAL audit_log_include_accounts = 'app@%,admin@localhost';
```

Component — assign a logging filter to the two accounts and leave the default `%` with no filter (or an empty filter):

```sql
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
SELECT audit_log_filter_set_user('app@%',          'log_all');
SELECT audit_log_filter_set_user('admin@localhost','log_all');
```

Plugin exclude list, inverted:

```sql
SET GLOBAL audit_log_exclude_accounts = 'monitor@%';
```

Component — keep the default `%` assigned to a logging filter and assign `monitor@%` to an empty filter (or leave it unassigned if `%` has no filter):

```sql
SELECT audit_log_filter_set_filter('no_log', '{ "filter": {} }');
SELECT audit_log_filter_set_user('monitor@%', 'no_log');
```

### Commands

Plugin:

```sql
SET GLOBAL audit_log_include_commands = 'select,insert,update,delete';
```

Component — narrow the `general` class with a `log` condition that tests `general_sql_command.str`:

```sql
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

```sql
SET GLOBAL audit_log_include_databases = 'app,reports';
```

Component — narrow `table_access` by `table_database.str`:

```sql
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

For a complete grammar reference (field names, logical operators, variables, functions), see [Write filter definitions](https://docs.percona.com/percona-server/9.7/write-filter-definitions.md) and [Definition fields reference](https://docs.percona.com/percona-server/9.7/audit-log-filter-definition-fields.md).

## Worked example

Starting plugin configuration in `my.cnf`:

```ini
[mysqld]
plugin-load-add          = audit_log.so
audit_log_format         = JSON
audit_log_policy         = ALL
audit_log_include_accounts = app@%,admin@localhost
audit_log_exclude_commands = set_option
audit_log_rotate_on_size = 104857600
audit_log_rotations      = 10
```

After running `audit_log_filter_linux_install.sql`, replace it with the following settings. Remove every plugin option, including `plugin-load-add = audit_log.so`, before you upgrade to 9.7:

```ini
[mysqld]
audit_log_filter.format         = JSON
audit_log_filter.rotate_on_size = 104857600
audit_log_filter.prune_seconds  = 2592000
```

Then define the filter and assign accounts:

```sql
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

Accounts that match neither `app@%` nor `admin@localhost`, and that have no explicit assignment to the default `%` filter, are not audited. The setup reproduces the plugin’s include-list behavior.

## Cutover and verification

1. Confirm the component is live:

   ```sql
   SELECT * FROM mysql.component WHERE component_urn = 'file://component_audit_log_filter';
   ```

1. Log in as a subject account, run a representative statement, and read the new log:

   ```sql
   SELECT audit_log_read('{}');
   ```

   See [Read log files](https://docs.percona.com/percona-server/9.7/reading-audit-log-filter-files.md).

1. Uninstall the legacy plugin and clear its settings from `my.cnf`:

   ```sql
   UNINSTALL PLUGIN audit_log;
   ```

1. Rotate once so new writes go to a fresh file under the component’s naming scheme:

   ```sql
   SELECT audit_log_rotate();
   ```

1. Archive any pre-existing plugin log files you want to keep. The component does not ingest those files. You can run [`filter_audit_log_filter_files`](https://docs.percona.com/percona-server/9.7/filter-audit-log-filter-files.md) to post-process component logs.

## Known caveats

- Log content changes slightly even when you keep the same format. Some statements that the 8.0 plugin did not record appear in current logs because the server sends additional events. The plugin page describes the `SELECT $$` example. Percona does not plan to backport format changes to match 8.0 output.
- The component stores state in `mysql.audit_log_filter` and `mysql.audit_log_user`. Back up those tables before making bulk changes, and include the tables in standard `mysql` database backups.
- Lifecycle events — `server_startup`, `server_shutdown`, and the `audit` class itself — are not valid filter targets. See [Definition fields reference](https://docs.percona.com/percona-server/9.7/audit-log-filter-definition-fields.md).
- `audit_log_filter.event_mode` defaults to `REDUCED`. When you relied on plugin logging for classes beyond `connection`, `general`, `table_access`, and `message`, set `event_mode = FULL` to match the broader class set.

## Additional reading

- [Upgrade from plugins to components](https://docs.percona.com/percona-server/9.7/upgrade-components.md)
- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.md)
- [Install the audit log filter](https://docs.percona.com/percona-server/9.7/install-audit-log-filter.md)
- [Write filter definitions](https://docs.percona.com/percona-server/9.7/write-filter-definitions.md)
- [Functions, options, and variables](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.md)
- [Audit log plugin](https://docs.percona.com/percona-server/9.7/audit-log-plugin.md) — legacy reference, with the removal notice
