# Write audit_log_filter definitions

Audit log filters are JSON documents you pass to `audit_log_filter_set_filter()`.

Every filter nests rules under a root `filter` object. For authoritative class, event, and field names that validation accepts, see [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }

  /* Ensure the first column's width matches its content */
  th:first-child, td:first-child {
    white-space: nowrap;
    width: 1%; /* Allows the column to shrink or expand to fit its content */
  }
</style>

| Benefit | Description |
|---|---|
| Smaller logs | Target only the events you need—less disk, simpler retention. |
| Lighter I/O | Fewer bytes per rotation window; less audit overhead on busy hosts. |
| Sharper security signal | Emphasize sensitive tables, account changes, and chosen DML/DDL instead of noise. |
| Faster investigations | Analysts skim fewer lines when irrelevant classes stay out of the file. |
| Compliance fit | Capture the evidence frameworks ask for without logging everything. |
| Lower resource burn | Trim CPU, memory, and disk spent on unwanted audit volume. |

## Basic structure

A filter is a JSON document whose root is a single `filter` object. `filter` contains an optional global `log` flag, an optional `id` (used for dynamic filter swapping), and one or more `class` rules. Each class rule can carry its own `log` condition and an optional `event` list; each event block can carry `log`, `abort`, `print`, or a nested `filter`. Conditions inside `log` / `abort` / `print` are built from `field`, `variable`, `function`, and the `and` / `or` / `not` logical operators.

The tree below summarizes where each key legally nests:

```text
filter                                   # root object
├── log                                  # optional boolean; global default
├── id                                   # optional; referenced by activate / ref
└── class                                # one object or an array of class rules
    ├── name: <class>                    # "connection" | "general" | "table_access" | "message"
    ├── log                              # optional; boolean OR a condition
    ├── print                            # optional; field-replacement rule (redaction)
    └── event                            # one object or an array of event rules
        ├── name: <subclass>             # e.g. "connect", "status", "update", "insert", …
        ├── log                          # optional; boolean OR a condition
        ├── abort                        # optional; boolean OR a condition (blocks execution)
        ├── print                        # optional; field-replacement rule (redaction)
        └── filter                       # optional; subfilter for dynamic swapping

condition := {
  field    : { name, value | regex }     # literal value, or ICU regex on a string field
  variable : { name, value }             # compare a predefined server variable
  function : { name, args? }             # call a predefined function
  and | or : [ condition, … ]            # combine sub-conditions
  not      : condition                   # invert a sub-condition
}
```

Keep this shape in mind as you read the rest of the page: every subsequent example hangs something off one of these nodes.

A minimal skeleton:

```json
{
  "filter": {
    "class": [
      {
        "name": "class_type",
        "event": [
          { "name": "event_subclass" }
        ]
      }
    ]
  }
}
```

Replace `class_type` with a real class name (`connection`, `general`, `table_access`, `message`) and `event_subclass` with one of its subclasses. Add a `log` condition under the class or the event to narrow which matching events are actually written.

### Practical example

The following filter logs only `connection` events whose `user.str` is `admin` or `developer` **and** whose `host.str` is `192.168.0.1`:

```json
{
  "filter": {
    "class": [
      {
        "name": "connection",
        "log": {
          "and": [
            { "field": { "name": "user.str", "value": ["admin", "developer"] } },
            { "field": { "name": "host.str", "value": "192.168.0.1" } }
          ]
        }
      }
    ]
  }
}
```

Unpacking the shape:

* `"class"` holds an array of class rules.
* `"name": "connection"` selects the `connection` class.
* `"log"` under the class block is a condition; the class logs only the events that satisfy it.
* The condition is an `and` over two `field` comparisons. `user.str` and `host.str` are fields carried by every `connection` event (see [Audit Log Filter definition fields](audit-log-filter-definition-fields.md)). `user.str`'s `value` is an array, so the comparison is true when the field matches any value in the array.

Rule-level conditions like this one narrow *which events are logged* — they do not determine *which filter a session uses*. Session-to-filter binding is separate, done with [`audit_log_filter_set_user()`](audit-log-filter-variables.md) and stored in `mysql.audit_log_user`. A session only reaches this JSON after the server has chosen this filter for it.

### Log all events

Toggle global logging with the top-level `log` flag:

```json
{
  "filter": { "log": true }
}
```

`"log": true` logs everything; `"log": false` logs nothing.

An empty filter object also logs everything:

```json
{
  "filter": { }
}
```

That is equivalent to `"log": true`.

Behavior summary:

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }

  /* Ensure the first column's width matches its content */
  th:first-child, td:first-child {
    white-space: nowrap;
    width: 1%; /* Allows the column to shrink or expand to fit its content */
  }
</style>

| Option | Details |
|--------|---------|
| Explicit `log` | Honors `true` / `false` at that level. |
| No `log`, no class/event rules | Defaults to on (log all). |
| Class or event rules present | Each block can carry its own `log` override. |

### Log specific event classes

To limit logging to one class, set `class.name`, for example `connection`:

```json
{
  "filter": {
    "class": { "name": "connection" }
  }
}
```

`{ "name": "connection" }` under `filter.class` audits connection events (connect, disconnect, change user—subject to `event_mode` and optional `event` narrowing).

The next example turns default logging off, then turns connection logging back on inside the class block:

```json
{
  "filter": {
    "log": false,
    "class": { 
      "log": true, 
      "name": "connection" 
    }
  }
}
```

### Log multiple classes or events

Log several classes either as separate objects in an array or as one array of names—equivalent when you do not need per-class options yet.

#### Per-class object list

Use a list of class objects when you will add per-class keys (`user`, `event`, …) later.

```json
{
  "filter": {
    "class": [
      { "name": "connection" },
      { "name": "general" },
      { "name": "table_access" }
    ]
  }
}
```

#### Compact name array

Combine class names in one array when rules stay uniform across the listed classes:

```json
{
  "filter": {
    "class": [
      { "name": [ "connection", "general", "table_access" ] }
    ]
  }
}
```
Prefer this compact form only when no per-class overrides are needed.


#### List of event and subclass options

Typical class and subclass pairs for authoring (subject to [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode)); validate exact spellings in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

<div class="nowrap-first" markdown="1">

| Class name        | Event subclass | Details                                                                 |
|---|---|---|
| `connection`      | `connect`        | New sessions (success or failure)              |
| `connection`      | `change_user`    | `CHANGE USER`                                  |
| `connection`      | `disconnect`     | Session end                                    |
| `general`         | `status`         | Query / command completion (success vs failure) |
| `general`         | `log`            | Statement log events (`FULL` mode)              |
| `general`         | `error`          | Statement error events (`FULL` mode)            |
| `general`         | `result`         | Statement result events (`FULL` mode)           |
| `table_access`    | `read`           | Reads (`SELECT`, `INSERT … SELECT`, …)          |
| `table_access`    | `delete`         | Deletes / truncate-style operations            |
| `table_access`    | `insert`         | Inserts / `REPLACE`                            |
| `table_access`    | `update`         | Updates                                        |
| `message`         | `internal`       | Internal audit API messages                    |
| `message`         | `user`           | User-emitted messages (`audit_api_message_emit_udf()`) |
| `connection`      | `pre_authenticate` | Pre-authentication handshake (`FULL` mode)            |
| `command`         | `start`, `end`   | Client command wrapper (`FULL` mode)            |
| `parse`           | `preparse`, `postparse` | Before and after SQL parsing (`FULL` mode) |
| `query`           | `start`, `status_end` | SQL execution bracket (`FULL` mode)          |
| `query`           | `nested_start`, `nested_status_end` | Nested SQL inside stored programs (`FULL` mode) |
| `stored_program`  | `execute`        | Stored-program invocation (`FULL` mode)         |
| `global_variable` | `get`, `set`     | Global variable read/write (`FULL` mode)        |
| `authentication`  | `flush`, `authid_create`, `credential_change`, `authid_rename`, `authid_drop` | Account and privilege changes (`FULL` mode) |

</div>

Mix and match subclasses under `event` to mirror your threat model.

## Event classes, log output, and SQL commands

Filter JSON uses lowercase class and event names (`query` / `start`). Log output uses different spellings depending on format:

* NEW and OLD XML — `<NAME>` carries a display string (for example `Query Start`, `TableRead`, `Log`).
* JSON and JSONL — `class` and `event` keys use the same lowercase names as filter definitions (for example `"class": "query"`, `"event": "start"`).

The SQL statement type appears separately as `COMMAND_CLASS` in XML or as `sql_command` inside event-specific objects in JSON. Filter on statement type with `general_sql_command.str` (REDUCED `general`/`status` records and FULL-mode `general` events) or `sql_command_id` (`query` class in FULL mode). The authoritative list of valid `sql_command` strings is the `com_status_vars` array in `sql/mysqld.cc` in the Percona Server source tree.

[`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) controls how many classes are emitted:

* `REDUCED` (default from 8.4.9-9) — `connection`, `general`/`status`, `table_access`, and `message` only. DDL, DCL, TCL, and most administrative statements appear as a single `general`/`status` record (XML `<NAME>Query</NAME>`) or as `table_access` when the server reports table touches.
* `FULL` — adds `command`, `parse`, `query`, `stored_program`, `global_variable`, and `authentication`. A single client statement can produce a sequence of ten or more records.

Lifecycle records (`audit` / `server_startup` / `server_shutdown`) may appear in the log at startup or shutdown but are not valid filter-definition targets. See [Audit Log Filter definition fields](audit-log-filter-definition-fields.md).

### SQL command values by category

The following tables list common `COMMAND_CLASS` / `sql_command` values grouped by SQL category. The list is representative, not exhaustive. For the complete set, see `com_status_vars` in `sql/mysqld.cc`.

#### DDL (Data Definition Language)

| `sql_command` | Example statement |
| --- | --- |
| `create_db` | `CREATE DATABASE test1` |
| `drop_db` | `DROP DATABASE test1` |
| `alter_db` | `ALTER DATABASE …` |
| `create_table` | `CREATE TABLE t1 (…)` |
| `alter_table` | `ALTER TABLE t1 …` |
| `drop_table` | `DROP TABLE t1` |
| `truncate` | `TRUNCATE TABLE t1` |
| `rename_table` | `RENAME TABLE …` |
| `create_index` | `CREATE INDEX …` |
| `drop_index` | `DROP INDEX …` |
| `create_view` | `CREATE VIEW …` |
| `drop_view` | `DROP VIEW …` |
| `create_trigger` | `CREATE TRIGGER …` |
| `drop_trigger` | `DROP TRIGGER …` |
| `create_procedure` | `CREATE PROCEDURE …` |
| `drop_procedure` | `DROP PROCEDURE …` |
| `create_function` | `CREATE FUNCTION …` |
| `drop_function` | `DROP FUNCTION …` |
| `create_event` | `CREATE EVENT …` |
| `drop_event` | `DROP EVENT …` |
| `alter_tablespace` | `CREATE TABLESPACE …`, `DROP TABLESPACE …`, `ALTER TABLESPACE …` |
| `create_compression_dictionary` | `CREATE COMPRESSION_DICTIONARY …` |
| `drop_compression_dictionary` | `DROP COMPRESSION_DICTIONARY …` |

#### DML (Data Manipulation Language)

| `sql_command` | Example statement |
| --- | --- |
| `select` | `SELECT …`, `SELECT DATABASE()` |
| `insert` | `INSERT INTO …` |
| `insert_select` | `INSERT INTO … SELECT …` |
| `update` | `UPDATE …` |
| `delete` | `DELETE FROM …` |
| `replace` | `REPLACE INTO …` |
| `load` | `LOAD DATA …` |
| `call_procedure` | `CALL proc()` |
| `do` | `DO …` |
| `ha_open`, `ha_read`, `ha_close` | `HANDLER …` |

#### DCL (Data Control Language)

| `sql_command` | Example statement |
| --- | --- |
| `grant` | `GRANT …` |
| `grant_roles` | `GRANT role …` |
| `revoke` | `REVOKE …` |
| `revoke_all` | `REVOKE ALL …` |
| `revoke_roles` | `REVOKE role …` |
| `create_user` | `CREATE USER …` |
| `drop_user` | `DROP USER …` |
| `alter_user` | `ALTER USER …` |
| `rename_user` | `RENAME USER …` |
| `create_role` | `CREATE ROLE …` |
| `drop_role` | `DROP ROLE …` |
| `set_password` | `SET PASSWORD …` |
| `set_role` | `SET ROLE …` |

#### TCL (Transaction Control Language)

| `sql_command` | Example statement |
| --- | --- |
| `begin` | `START TRANSACTION`, `BEGIN` |
| `commit` | `COMMIT` |
| `rollback` | `ROLLBACK` |
| `savepoint` | `SAVEPOINT …` |
| `release_savepoint` | `RELEASE SAVEPOINT …` |
| `rollback_to_savepoint` | `ROLLBACK TO SAVEPOINT …` |
| `xa_start` | `XA START …` |
| `xa_end` | `XA END …` |
| `xa_prepare` | `XA PREPARE …` |
| `xa_commit` | `XA COMMIT …` |
| `xa_rollback` | `XA ROLLBACK …` |

#### Administration, replication, and session

| `sql_command` | Example statement |
| --- | --- |
| `change_db` | `USE db_name` (also logged as client command `Init DB` in FULL mode) |
| `set_option` | `SET GLOBAL …`, `SET SESSION …` |
| `show_databases` | `SHOW DATABASES` |
| `show_tables` | `SHOW TABLES` |
| `show_fields` | `DESCRIBE tbl`, `DESC tbl`, `SHOW COLUMNS …`, `SHOW FIELDS …` |
| `show_variables` | `SHOW VARIABLES` |
| `show_status` | `SHOW STATUS` |
| `show_grants` | `SHOW GRANTS` |
| `flush` | `FLUSH …` |
| `reset` | `RESET …` |
| `kill` | `KILL …` |
| `shutdown` | `SHUTDOWN` |
| `restart` | `RESTART` |
| `prepare_sql` | `PREPARE …` |
| `execute_sql` | `EXECUTE …` |
| `dealloc_sql` | `DEALLOCATE PREPARE …` |
| `lock_tables` | `LOCK TABLES …` |
| `unlock_tables` | `UNLOCK TABLES` |
| `install_plugin` | `INSTALL PLUGIN …` |
| `uninstall_plugin` | `UNINSTALL PLUGIN …` |
| `install_component` | `INSTALL COMPONENT …` |
| `uninstall_component` | `UNINSTALL COMPONENT …` |
| `replica_start` | `START REPLICA` |
| `replica_stop` | `STOP REPLICA` |
| `binlog` | `BINLOG …` |
| `purge` | `PURGE BINARY LOGS …` |
| `optimize` | `OPTIMIZE TABLE …` |
| `analyze` | `ANALYZE TABLE …` |
| `check` | `CHECK TABLE …` |
| `repair` | `REPAIR TABLE …` |

Client-level COM names (not `sql_command`) appear on `command` class records in FULL mode. Common values include `Query`, `Init DB` (for `USE`), `Ping`, and `Quit`.

### Typical event sequences

The tables below show which classes and events fire for common operations. Sequences assume `audit_log_filter.event_mode=FULL` and a filter that logs everything (`{"filter": {"log": true}}`). With `REDUCED` mode, only the rows marked REDUCED apply; other rows are skipped at runtime.

Column key:

* **Filter class / event** — names to use in filter JSON.
* **Log `<NAME>`** — value in NEW XML `<NAME>` (JSON `event` uses the filter event name).
* **`sql_command`** — value in `COMMAND_CLASS` or `general_sql_command.str` when present.

#### `CREATE DATABASE test1`

| Order | Filter class / event | Log `<NAME>` (NEW XML) | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `command` / `start` | `Command Start` | `Query` |
| 2 | `parse` / `preparse` | `Preparse` | `Parse` |
| 3 | `parse` / `postparse` | `Postparse` | `Parse` |
| 4 | `general` / `log` | `Log` | `General` |
| 5 | `query` / `start` | `Query Start` | `create_db` |
| 6 | `query` / `status_end` | `Query Status End` | `create_db` |
| 7 | `general` / `result` | `Result` | `General` |
| 8 | `general` / `status` | `Status` or `Query` | `create_db` (REDUCED: this is the only query-phase record) |
| 9 | `command` / `end` | `Command End` | `Query` |

#### `USE test1` followed by `SELECT DATABASE()`

`USE` and `SELECT` are separate client commands. Each command produces its own `command` / `start` … `command` / `end` wrapper.

**`USE test1`**

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `command` / `start` | `Command Start` | `Init DB` |
| 2 | `general` / `log` | `Log` | `General` |
| 3 | `general` / `result` | `Result` | `General` |
| 4 | `general` / `status` | `Status` or `Query` | `change_db` (REDUCED) |
| 5 | `command` / `end` | `Command End` | `Init DB` |

**`SELECT DATABASE()`**

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `command` / `start` | `Command Start` | `Query` |
| 2 | `parse` / `preparse` | `Preparse` | `Parse` |
| 3 | `parse` / `postparse` | `Postparse` | `Parse` |
| 4 | `general` / `log` | `Log` | `General` |
| 5 | `query` / `start` | `Query Start` | `select` |
| 6 | `query` / `status_end` | `Query Status End` | `select` |
| 7 | `general` / `result` | `Result` | `General` |
| 8 | `general` / `status` | `Status` or `Query` | `select` (REDUCED) |
| 9 | `command` / `end` | `Command End` | `Query` |

#### `CREATE TABLE sbtest1 (…)`

Same pattern as `CREATE DATABASE`, with `create_table` as the `sql_command` on `query` / `start` and `query` / `status_end`. `table_access` records are not emitted for DDL that does not read or write table data through the table-access API.

#### `DROP TABLE sbtest1`

Same FULL-mode sequence as `CREATE TABLE`, with `drop_table` as the `sql_command`.

#### `ALTER TABLE …`

Same FULL-mode sequence as `CREATE DATABASE`, with `alter_table` as the `sql_command` on `query` / `start` and `query` / `status_end`.

#### `CREATE INDEX` / `DROP INDEX`

Same FULL-mode sequence as `CREATE TABLE`. Index DDL uses `create_index` or `drop_index` as the `sql_command`:

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `create_index` or `drop_index` |
| 2 | `query` / `status_end` | `Query Status End` | same as row 1 |

#### `DESCRIBE tbl` / `DESC tbl`

`DESCRIBE` and `DESC` are logged as `show_fields`, not a separate `describe` command name:

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `show_fields` |
| 2 | `query` / `status_end` | `Query Status End` | `show_fields` |

#### `CREATE TABLESPACE` / `DROP TABLESPACE`

Both statements use `alter_tablespace` as the `sql_command` on the `query` records. The `command`, `parse`, and `general` wrapper matches other COM `Query` statements.

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `alter_tablespace` |
| 2 | `query` / `status_end` | `Query Status End` | `alter_tablespace` |

#### `CREATE COMPRESSION_DICTIONARY` / `DROP COMPRESSION_DICTIONARY`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `create_compression_dictionary` or `drop_compression_dictionary` |
| 2 | `query` / `status_end` | `Query Status End` | same as row 1 |

#### `DROP DATABASE test2`

Same FULL-mode sequence as `CREATE DATABASE`, with `drop_db` as the `sql_command`. After the database is dropped, the server may run an implicit `SELECT DATABASE()`; that statement produces a second `command` wrapper with `select` as the `sql_command`.

#### `SAVEPOINT save1`

TCL statements routed through COM `Query` produce the same `command`, `parse`, and `general` wrapper as `CREATE DATABASE`. The `query` phase carries the TCL-specific `sql_command`:

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `savepoint` |
| 2 | `query` / `status_end` | `Query Status End` | `savepoint` |

In REDUCED mode, only `general` / `status` with `general_sql_command.str` = `savepoint` is emitted.

`RELEASE SAVEPOINT` and `ROLLBACK TO SAVEPOINT` use `release_savepoint` and `rollback_to_savepoint` respectively on the `query` records.

#### `ROLLBACK`

Same wrapper as other COM `Query` statements. The `query` phase uses `rollback` as the `sql_command`:

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `rollback` |
| 2 | `query` / `status_end` | `Query Status End` | `rollback` |

In REDUCED mode, only `general` / `status` with `general_sql_command.str` = `rollback` is emitted.

#### `START TRANSACTION`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `begin` |
| 2 | `query` / `status_end` | `Query Status End` | `begin` |

#### `COMMIT`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `commit` |
| 2 | `query` / `status_end` | `Query Status End` | `commit` |

#### `SET @@SESSION.…`

Session and global variable assignments use `set_option` on the `query` records. In FULL mode, `global_variable` / `set` records may also appear for some `SET` forms.

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `set_option` |
| 2 | `query` / `status_end` | `Query Status End` | `set_option` |

#### `OPTIMIZE TABLE`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `optimize` |
| 2 | `query` / `status_end` | `Query Status End` | `optimize` |

`ANALYZE TABLE`, `CHECK TABLE`, and `REPAIR TABLE` use `analyze`, `check`, and `repair` respectively.

#### `CREATE USER`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `create_user` |
| 2 | `query` / `status_end` | `Query Status End` | `create_user` |

In FULL mode, `authentication` / `authid_create` may also appear.

#### `GRANT`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `grant` |
| 2 | `query` / `status_end` | `Query Status End` | `grant` |

The `SQLTEXT` on `Query Status End` may show normalized identifier quoting (for example backticks around schema and table names) that differs from the `Query Start` record.

#### `DROP USER`

`DROP USER` emits an `authentication` record between the `query` bracket records:

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `drop_user` |
| 2 | `authentication` / `authid_drop` | `Auth Authid Drop` | `Authentication` |
| 3 | `query` / `status_end` | `Query Status End` | `drop_user` |

#### `INSERT INTO …`

DML that touches a table adds a `table_access` record between the `query` bracket records. This sequence appears in both FULL and REDUCED modes for the `table_access` row.

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `insert` |
| 2 | `table_access` / `insert` | `TableInsert` | `insert` (REDUCED) |
| 3 | `query` / `status_end` | `Query Status End` | `insert` |

`UPDATE` and `DELETE` follow the same pattern with `TableUpdate` / `update` and `TableDelete` / `delete`. `SELECT` that reads tables emits `TableRead` / `read` instead.

Unless noted otherwise, the `command`, `parse`, and `general` wrapper for the examples in this section matches `CREATE DATABASE`.

#### Server startup

At component initialization the log receives lifecycle records that cannot be targeted in filter JSON:

| Log `<NAME>` (NEW XML) | JSON `class` / `event` | Notes |
| --- | --- | --- |
| `Audit` | `audit` / `startup` | Component startup; includes `SERVER_ID`, `STARTUP_OPTIONS`, `OS_VERSION`, `MYSQL_VERSION` in XML |
| `Auth Flush` | `authentication` / `flush` | Privilege cache flush during startup (`FULL` mode) |

MySQL `server_startup` tracking events are not written to the audit log by this component.

#### `SHUTDOWN`

| Order | Filter class / event | Log `<NAME>` | `sql_command` or COM |
| --- | --- | --- | --- |
| 1 | `query` / `start` | `Query Start` | `shutdown` |
| 2 | `general` / `log` | `Log` | `General` |
| 3 | `query` / `status_end` | `Query Status End` | `shutdown` |

Component shutdown writes an `audit` / `shutdown` record (XML `<NAME>NoAudit</NAME>`). MySQL `server_shutdown` tracking events are not written.

### Filtering by statement type

To log only DDL against a schema, combine class rules with `general_sql_command.str` conditions:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "or": [
            { "field": { "name": "general_sql_command.str", "value": "create_db" } },
            { "field": { "name": "general_sql_command.str", "value": "drop_db" } },
            { "field": { "name": "general_sql_command.str", "value": "create_table" } },
            { "field": { "name": "general_sql_command.str", "value": "drop_table" } },
            { "field": { "name": "general_sql_command.str", "value": "alter_table" } }
          ]
        }
      }
    }
  }
}
```

In FULL mode, add parallel rules under the `query` class using `sql_command_id` if you need the bracketing `query` / `start` and `query` / `status_end` records instead of (or in addition to) the `general` / `status` summary.

For format-specific field layouts, see [Audit Log Filter format - XML (new style)](audit-log-filter-new.md) and [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md).

## Filter patterns

Inclusive patterns list what to log; exclusive patterns drop noisy work from an otherwise-on stream. Pick one approach per filter — combining them in a single rule set is harder to reason about than two separate filters bound to different account patterns.

### Inclusive filters

Inclusive rules list what to log—pair classes with `user`, `database`, `table`, `event`, `status`, and similar fields until the stream matches your policy.

#### When to use inclusive filters

Spell out:

* Which classes matter

* Which accounts or objects to watch

* Which subclasses or outcomes qualify

Typical uses: compliance evidence, privileged-user monitoring, schema-change tracking, incident response.

Tighter filters mean less noise and less I/O—always stage-test rules before production.

#### Inclusive filter example

Administrators often watch destructive `table_access` work—this skeleton logs `update` and `delete` only:

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "event": [
          {
            "name": ["update", "delete"],
            "log": {
              "and": [
                { "field": { "name": "table_database.str", "value": "app_db" } },
                { "field": { "name": "table_name.str", "value": "sensitive_tbl" } }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

The rule matches `update` and `delete` `table_access` events, and the nested `log` condition narrows logging to events whose `table_database.str` equals `app_db` **and** `table_name.str` equals `sensitive_tbl`. `read` and `insert` subclasses are not named, so they skip the rule entirely.

* `"class"` — begins the class rule block.
* `"name": "table_access"` — limits to table-access events (subclasses: `read`, `insert`, `update`, `delete`).
* `"event"` — selects the `update` and `delete` subclasses; other subclasses skip this rule.
* `"log"` — a per-event condition. `true` logs every match; a `field` / `and` / `or` / `not` structure logs only matches that satisfy the condition.
* `"field"` — compares an event field against a value. `table_database.str` and `table_name.str` are fields carried by every `table_access` event (see [Audit Log Filter definition fields](audit-log-filter-definition-fields.md) for the full list).

To widen or narrow the rule, change the field values, add `or` branches for multiple tables, or drop either `field` check to scope by database only or by table name only.

#### Log only UPDATE and DELETE on a specific table

To log `update` and `delete` against a single table — or a short list of tables inside one database — combine `table_database.str` with an `or` over `table_name.str` values:

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "event": [
          {
            "name": ["update", "delete"],
            "log": {
              "and": [
                { "field": { "name": "table_database.str", "value": "app_db" } },
                {
                  "or": [
                    { "field": { "name": "table_name.str", "value": "sensitive_tbl" } },
                    { "field": { "name": "table_name.str", "value": "audit_events" } }
                  ]
                }
              ]
            }
          }
        ]
      }
    ]
  }
}
```

To scope to one database only, omit the inner `or` and keep the `table_database.str` check. Note that `table_access` events do not carry a user field, so filtering by account must be done at assignment time with [`audit_log_filter_set_user()`](audit-log-filter-variables.md).

### Exclusive filters

Exclusive (or negated) rules drop noisy work. There are two idioms:

* Set `"log": true` at the filter level, then set `"log": false` on a specific class or event to suppress just that slice.
* Use a `"not"` logical operator inside a `log` condition to drop matches that satisfy an expression.

#### Suppress one class while logging everything else

```json
{
  "filter": {
    "log": true,
    "class": { "name": "general", "log": false }
  }
}
```

This logs every event *except* `general` class events. `log: true` at the top enables logging globally, then the class-level `log: false` carves out one class.

#### Invert a field match with `not`

Wrap a condition in `not` inside a `log` item to drop the events that match it. Because inversion tests a field on the current event, use a field the class actually carries (for example, `table_database.str` on `table_access`; `user.str` on `connection`; `general_user.str` on `general`). The example below suppresses `table_access` events against the internal `mysql` schema:

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "log": {
          "not": {
            "field": { "name": "table_database.str", "value": "mysql" }
          }
        }
      }
    ]
  }
}
```

This logs `table_access` events except those touching the `mysql` system schema. For a user-based suppression, apply the `not` against a field that exists on the class you're filtering — `user.str` on `connection`, `general_user.str` on `general` — or scope the filter to specific accounts at assignment time with [`audit_log_filter_set_user()`](audit-log-filter-variables.md).

#### Exclusive filter example

This filter logs everything except `general` events, and within `connection` events drops `connect`/`disconnect` subclasses (keeping only `change_user`):

```json
{
  "filter": {
    "log": true,
    "class": [
      {
        "name": "connection",
        "event": [
          { "name": "connect", "log": false },
          { "name": "disconnect", "log": false }
        ]
      },
      { "name": "general", "log": false }
    ]
  }
}
```

* The top-level `"log": true` turns everything on by default.
* The `connection` block's `event` list silences the two noisy subclasses but leaves `change_user` on.
* The second class entry turns off the entire `general` class.

Field-type rules (JSON numbers versus strings, `connection_type` symbolic constants such as `"::tcp/ip"`, and which types are accepted for each field) are described under [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition) and in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md#connection).

## Advanced filter constructs

The sections so far cover logging on or off at class/event granularity. The filter language also supports per-event **conditions**, execution **blocking**, references to server **variables** and **functions**, field-value **replacement** (redaction), and **dynamic** filter swapping.

Validate exact field names and types against [Audit Log Filter definition fields](audit-log-filter-definition-fields.md) before deploying any of these to production.

### Test event field values

Inside an `event` block, a `log` item can carry a `field` comparison. The rule logs the event only when the field equals the given value.

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "field": { "name": "general_command.str", "value": "Query" }
        }
      }
    }
  }
}
```

The above logs `general`/`status` events only when `general_command.str` equals `Query` (dropping `Execute`, `Quit`, and `Change user`). String fields take string values; integer fields (such as `status` on `connection`, or `general_error_code` on `general`) take JSON numbers.

Fields available on each class are listed in [Audit Log Filter definition fields](audit-log-filter-definition-fields.md). Examples:

* `connection`: `status`, `user.str`, `host.str`, `ip.str`, `database.str`, `connection_type`

* `general`: `general_error_code`, `general_user.str`, `general_command.str`, `general_query.str`, `general_sql_command.str`, `general_host.str`, `general_ip.str`

* `table_access`: `query.str`, `table_database.str`, `table_name.str`

A string field also accepts a regular expression. See [Regular expression field conditions](#regular-expression-field-conditions).

### Regular expression field conditions

Starting with Percona Server for MySQL 8.4.13-13, a field condition can match a string field to a regular expression. Use `regex` in place of `value`.

Install the Audit Log Filter component first. See [Install the audit log filter](install-audit-log-filter.md). The account that calls `audit_log_filter_set_filter()` and `audit_log_filter_flush()` needs the `AUDIT_ADMIN` privilege.

The server accepts a `regex` condition in each item that accepts a field condition:

* The `log` key

* The `abort` key

* The `print` condition of a field replacement. See [Redact audit log fields](redact-audit-log-fields.md).

* The `activate` condition of a replacement filter. See [Replace a filter dynamically](#replace-a-filter-dynamically).

* The `and`, `or`, and `not` keys

The following definition logs `insert`, `update`, and `delete` events. The class name is `table_access`. The `table_database.str` value equals `tpcc`. The `table_name.str` value matches `new_orders`, `orders`, or `history`. One or more digits follow `new_orders`, `orders`, or `history`. The filter name `log_tpcc_tables` is an example name.

```sql
SELECT audit_log_filter_set_filter('log_tpcc_tables', '{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete"],
        "log": {
          "and": [
            {"field": {"name": "table_database.str", "value": "tpcc"}},
            {"field": {"name": "table_name.str", "regex": "^(new_orders|orders|history)[0-9]+$"}}
          ]
        }
      }
    }
  }
}');
SELECT audit_log_filter_flush();
```

Percona Server for MySQL 8.4.9-9 and subsequent releases detach each open session when `audit_log_filter_flush()` runs. The session loads the filter after reconnect or `CHANGE_USER`. A connection that opens after the flush loads the filter at once. See [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush).

#### Field object members

A field object with `regex` contains exactly one `name` member and exactly one `regex` member. The server rejects a `value` member, a duplicated member, or any other member in that field object. The field object accepts no `re` or `regexp` alias. `value` remains a literal comparison.

#### Accepted fields

The server accepts `regex` only on string fields. The server rejects integer fields, such as `connection_type` and any `*.length` field. The server rejects `general_connection_id` and `general_thread_id` on class `general`. The server rejects `connection_id` on classes `connection` and `table_access`. On each other class, `connection_id` is a string field that accepts `regex`. [Audit Log Filter definition fields](audit-log-filter-definition-fields.md) lists each field type.

#### Pattern

`regex` is a non-empty JSON string. The string uses ICU regular expression syntax. The SQL `REGEXP` functions use ICU regular expression syntax. The pattern is not POSIX ERE. The pattern is not PCRE. The server rejects an empty pattern. You use `^$` or `\A\z` to match an empty value.

#### Match rules

The server searches for the pattern anywhere in the value. You use `^...$` to anchor the match to the whole value. In ICU, `$` also matches before a final line terminator. You use `\A...\z` to anchor the match absolutely. The match is case-sensitive. Collations do not affect the match. `lower_case_table_names` does not affect the match. The pattern accepts inline flags such as `(?i)`.

#### Backslash escapes

You escape each backslash in JSON (`"\\d+"`). You escape each backslash again in an ordinary SQL string literal (`'{"regex": "\\\\d+"}'`). You build the definition with `JSON_OBJECT()`. You write `[0-9]` in place of `\d`. `JSON_OBJECT()` and `[0-9]` avoid most backslash escapes.

In `JSON_OBJECT()`, the SQL string `'\\d+'` is the pattern `\d+`. The same pattern inside a SQL string that holds JSON text is `'{"regex": "\\\\d+"}'`.

```sql
SELECT audit_log_filter_set_filter(
  'log_digit_tables',
  JSON_OBJECT(
    'filter', JSON_OBJECT(
      'class', JSON_OBJECT(
        'name', 'table_access',
        'event', JSON_OBJECT(
          'name', JSON_ARRAY('read', 'insert', 'update', 'delete'),
          'log', JSON_OBJECT(
            'field', JSON_OBJECT(
              'name', 'table_name.str',
              'regex', '[0-9]+'
            )
          )
        )
      )
    )
  )
);
```

The `log` condition is inside the `event` object. A class-level `log` key accepts only `true` or `false`. A condition in a class-level `log` key returns the error `'log' must be of bool type`.

`[0-9]+` has no anchor. The pattern matches a `table_name.str` value that contains a digit at any position. `log_digit_tables` is an example filter name. You run `audit_log_filter_flush()` after this call. You reconnect each open session after the flush.

#### Absent values

The condition finds no match when the field is absent from the event. The event carries `general_query.str` as an empty string when the query text is not available. The event carries `table_access` `query.str` as an empty string when the query text is not available.

#### UTF-8 and NUL bytes

The server matches the value as UTF-8. The server decodes each malformed sequence as U+FFFD. The server does not convert query text from the client character set before the match. A `value` comparison also skips conversion from the client character set ([PS-10355](https://perconadev.atlassian.net/browse/PS-10355)). A UTF-8 literal such as `café` does not match the latin1 bytes of the same statement. The server logs the statement as UTF-8. A NUL byte ends each connection field, each table field, and each other field. Each query text field keeps the full field length.

#### Validation errors

`audit_log_filter_set_filter()` validates the definition. The server runs the same checks when the server loads filters from `mysql.audit_log_filter`. An invalid pattern returns the following error:

```text
ERROR: Incorrect rule definition: invalid regular expression for field 'table_name.str': U_REGEX_MISMATCHED_PAREN at line 1, offset 8
```

The server also rejects a pattern in the following cases:

| Pattern | Error text |
| --- | --- |
| The pattern is longer than 16384 UTF-8 bytes | `regular expression exceeds 16384 UTF-8 bytes` |
| The pattern is not valid UTF-8 | `pattern is not valid UTF-8` |

`audit_log_filter_flush()` runs the same checks on the stored definitions. A failed check returns a different error text. For example:

```text
ERROR: Filter 'rx_reload' has wrong format: invalid regular expression for field 'table_name.str': U_REGEX_MISMATCHED_PAREN at line 1, offset 8
```

After a failed flush, the server keeps the previously loaded rules active for every session.

The server escapes keys, names, and patterns in each error message. The server truncates each key, name, and pattern to 96 bytes. The 96 bytes include the `...` suffix that the server adds on truncation.

The following table lists the escaped forms. `XX` is the hexadecimal value of the character or byte.

| Character or byte | Escaped form |
| --- | --- |
| Backslash (`\`) | `\\` |
| Single quote (`'`) | `\u0027` |
| Control character | `\u00XX` |
| Invalid UTF-8 byte | `\xXX` |

#### Limits and failed matches

The ICU time limit is 32. The backtracking stack limit is 8000000 bytes. 32 is the default for `regexp_time_limit`. 8000000 bytes is the default for `regexp_stack_limit`. The server does not use the session value of `regexp_time_limit`. The server does not use the session value of `regexp_stack_limit`.

The server treats a match past either limit as no match. The server treats every other match failure as no match.

| Context | Effect of a failed match |
| --- | --- |
| `log` | The condition does not select the event. A failed match inside `not` selects the event. |
| `abort` | The server does not abort the statement. |
| `print` condition | The server replaces the field. A false `print` condition replaces the field. See [Redact audit log fields](redact-audit-log-fields.md). |
| `activate` | The server does not activate the replacement filter. |

A failed `log` match can omit the event from the log. A failed match on a positive `abort` condition can allow the statement to execute.

The server increments the `Audit_log_filter_regex_match_errors` status variable for every failed match. See [Audit log filter status variables](audit-log-filter-variables.md#audit-log-filter-status-variables).

```sql
SHOW GLOBAL STATUS LIKE 'Audit_log_filter_regex_match_errors';
```

The server writes an error log warning for the first failure of each condition. The server reports each additional failure of the same condition at most once per 60 seconds. The following warning is the error log text:

```text
Audit log filter 'f': regex '(a+)+$' on field 'general_query.str' failed (timeout: U_REGEX_TIME_OUT); condition treated as not matching. Further failures of this condition are reported at most once per 60 seconds.
```

The server matches a killed statement in the normal way. The server matches a killed connection in the normal way. The server matches a statement that `MAX_EXECUTION_TIME` stops in the normal way. `KILL` does not interrupt a regex match after the match starts. The server applies `KILL` after the match completes. The server applies `KILL` after the match reaches a limit.

#### Performance

The server compiles each condition when the server loads the filter. Each evaluation creates a separate matcher. A `regex` comparison is more expensive than a `value` comparison. The cost of an unanchored search grows with the value length. You place cheap equality conditions before a `regex` condition in an `and` list. The server stops evaluation at the first false operand. A smaller definition does not mean lower CPU usage.

#### Upgrade and downgrade

Versions before Percona Server for MySQL 8.4.13-13 ignore a `regex` member when the field object also contains `value`. Starting with Percona Server for MySQL 8.4.13-13, the server rejects a field object that contains both `regex` and `value`.

After an upgrade, the server restarts and loads the stored definitions. One rejected definition blocks the load of the whole filter set. The block applies even when no account uses the rejected definition. The server audits no events until you fix each rejected definition and `audit_log_filter_flush()` succeeds. The error log shows an error such as the following:

```text
[ERROR] [MY-011071] [Server] Component audit_log_filter reported: 'Failed to load filtering rules: Filter 'stale' has wrong format: event field definition 'field' must have either 'value' or 'regex', not both'
```

On a running server, a failed `audit_log_filter_flush()` keeps the previously loaded rules active. See [Validation errors](#validation-errors).

##### Before an upgrade

Complete the following steps on the version without `regex` support:
{.power-number}

1. List the stored definitions that contain `regex`:

    ```sql
    SELECT name FROM mysql.audit_log_filter
    WHERE JSON_CONTAINS_PATH(filter, 'one', '$**.regex');
    ```

2. In each listed definition, find each field object that contains both `regex` and `value`. Remove the `regex` member from that field object. Keep the `value` member. The version without `regex` support rejects a field object without `value`.

    `audit_log_filter_set_filter()` cannot overwrite an existing filter. The function returns `ERROR: Rule with this name already exists`. Complete the following steps for each listed definition:

    1. List the accounts that use the filter:

        ```sql
        SELECT * FROM mysql.audit_log_user WHERE filtername = '<name>';
        ```

    2. Remove the filter. `audit_log_filter_remove_filter()` also deletes the rows for the filter in `mysql.audit_log_user`.

        ```sql
        SELECT audit_log_filter_remove_filter('<name>');
        ```

    3. Store the definition without the `regex` member:

        ```sql
        SELECT audit_log_filter_set_filter('<name>', '<definition>');
        ```

    4. Assign the filter to each account from the list:

        ```sql
        SELECT audit_log_filter_set_user('<user>@<host>', '<name>');
        ```

    As an alternative, update the `filter` column of `mysql.audit_log_filter` directly.

3. Run `audit_log_filter_flush()`.

After the upgrade, you can rewrite a definition to use `regex` without `value`.

Upgrade each server that loads the same filter tables before you define a `regex` condition. A replica is an example of a server that loads the same filter tables. [Audit Log Filter restrictions](audit-log-filter-restrictions.md) describes replication of `mysql.audit_log_filter`.

##### Before a downgrade

Complete the following steps on the version that supports `regex`, before the downgrade:
{.power-number}

1. Remove or rewrite every `regex` condition in the filter and in each replacement filter.

2. Run `audit_log_filter_flush()`.

3. Reconnect each session.

### Combine conditions with logical operators

`and`, `or`, and `not` let you build compound conditions. They take an array (for `and` / `or`) or a single sub-condition (for `not`) and can be nested arbitrarily.

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "or": [
            {
              "and": [
                { "field": { "name": "general_command.str",    "value": "Query" } },
                { "field": { "name": "general_command.length", "value": 5 } }
              ]
            },
            {
              "and": [
                { "field": { "name": "general_command.str",    "value": "Execute" } },
                { "field": { "name": "general_command.length", "value": 7 } }
              ]
            }
          ]
        }
      }
    }
  }
}
```

This logs `general`/`status` events whose `general_command` is either `Query` (length 5) or `Execute` (length 7). Use `not` to invert any sub-expression — for example, `{ "not": { "field": { "name": "user.str", "value": "healthcheck" } } }` matches everything except the `healthcheck` account (on a class that actually carries `user.str`).

### Block execution with `abort`

An `event` block can carry an `abort` item that prevents matching statements from executing. The same block cannot carry both `log` and `abort`; use separate event blocks when you need both behaviors on the same class. Because blocking is a policy-enforcement capability — not observability — it is covered on its own page: [Block statements with an audit log filter](block-statements-with-audit-filter.md).

### Reference predefined variables

A `log` or `abort` condition can test a predefined variable with a `variable` item. The condition is true when the variable equals the given value.

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "variable": {
            "name": "audit_log_connection_policy_value",
            "value": "::none"
          }
        }
      }
    }
  }
}
```

Predefined variables mirror the legacy-mode `audit_log_*_policy` system variables so operators can re-tune an active filter by changing a server variable rather than rewriting the JSON:

* `audit_log_connection_policy_value` — `0`/`"::none"`, `1`/`"::errors"`, `2`/`"::all"`.
* `audit_log_policy_value` — `0`/`"::none"`, `1`/`"::logins"`, `2`/`"::all"`, `3`/`"::queries"`.
* `audit_log_statement_policy_value` — `0`/`"::none"`, `1`/`"::errors"`, `2`/`"::all"`.

Symbolic constants (`"::none"`, `"::all"`, …) are case-sensitive strings and are interchangeable with the numeric form.

### Reference predefined functions

Use a `function` item to call a built-in inside a `log`, `abort`, `print`, or `replace` condition. The `name` field holds the function name without parentheses. The `args` field is an array of arguments. Omit `args` when the function takes none.

The Percona Server audit log filter component implements two predefined functions: `string_find` and `query_digest`. Other names from the upstream MySQL Enterprise Audit reference, such as `find_in_include_list`, `find_in_exclude_list`, and `debug_sleep`, are not recognized in this component. Calls to those names fail validation.

The following filter logs `general`/`status` events only when the executed statement contains the substring `password`:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "function": {
            "name": "string_find",
            "args": [
              { "string": { "field": "general_query.str" } },
              { "string": { "string": "password" } }
            ]
          }
        }
      }
    }
  }
}
```

Each element of the `args` array is a typed wrapper object with exactly one member. The member name is the argument type — `string` is the only argument type currently used. The member value is an object with exactly one member whose name identifies the value source. Two sources are accepted:

* `field` — read the named event field at evaluation time, for example `{ "string": { "field": "general_query.str" } }`.

* `string` — supply a literal string, for example `{ "string": { "string": "password" } }`.

Bare-string array elements (for example `"password"`) and bare-field elements (`{ "field": "general_query.str" }` without the outer `string` wrapper) are rejected by filter validation.

Available functions:

* `string_find(text, substr)` returns `true` when `substr` appears inside `text`. The comparison is case-sensitive. Both arguments are strings. Wrap each argument in the typed-wrapper format shown in the preceding example. This function helps match keywords inside `general_query.str` or `query.str` without forcing a digest comparison.

* `query_digest([str])` has two shapes that depend on the argument:

    * No argument: the function returns the normalized statement digest of the current event's SQL text. Use this shape inside a `replace` clause to substitute literal SQL with the digest. For details, see [Redact audit log fields](redact-audit-log-fields.md).

    * One string argument: the function returns `true` when the supplied digest equals the current event's digest. Use this shape inside a `log`, `abort`, or `print` condition. Wrap the call in `not` to invert the match. Use this form to act on specific statement patterns. For example, block any statement whose digest matches `SELECT ?`.

    Starting in Percona Server for MySQL 8.4.9-9, `query_digest` accepts a string shorthand for its single argument: `"args": "SELECT ?"`. The shorthand is equivalent to the verbose form `"args": [{ "string": { "string": "SELECT ?" } }]`. Earlier releases require the verbose form. The shorthand is specific to `query_digest` — `string_find` requires the verbose form for both arguments.

A condition that calls a function evaluates to `true` when the function returns a truthy value. Truthy values include non-empty strings and Boolean `true`. Combine function calls with `and`, `or`, and `not` to build richer rules. For example, log only when `string_find` matches and the user is not on an allow list.

### Replace event field values (redaction)

A `print` / `replace` item inside a class or event block rewrites statement text on one of four class/field pairs (`general`/`general_query.str`, `table_access`/`query.str`, `query`/`query.str`, `parse`/`query.str`; the last two require `FULL` mode) as a `query_digest` before the event is logged, which keeps literal values out of the audit stream. This is a compliance/PII capability covered on its own page: [Redact audit log fields](redact-audit-log-fields.md).

### Replace a filter dynamically

A filter can swap itself for a different rule set mid-session. Nest a `filter` block inside an event and give the outer filter an `id`; use `activate` to trigger the swap and `ref` to point back at the original.

```json
{
  "filter": {
    "id": "main",
    "class": {
      "name": "table_access",
      "event": {
        "name": ["update", "delete"],
        "log": false,
        "filter": {
          "class": {
            "name": "general",
            "event": { "name": "status",
                       "filter": { "ref": "main" } }
          },
          "activate": {
            "or": [
              { "field": { "name": "table_name.str", "value": "temp_1" } },
              { "field": { "name": "table_name.str", "value": "temp_2" } }
            ]
          }
        }
      }
    }
  }
}
```

How it behaves:

* `main` waits for `table_access` `update` or `delete` events. `log: false` means those events are not logged directly.
* When one of those events touches `temp_1` or `temp_2`, the inner filter activates.
* The inner filter waits for the next `general`/`status` event (typically end of statement), logs it, then the nested `ref: main` restores the outer filter.

Net effect: you log one `general`/`status` entry per statement that touched `temp_1` or `temp_2`, instead of many `table_access` rows. A single `UPDATE temp_1, temp_3 SET ...` emits one log entry rather than one per row touched.

`activate` is only valid inside a subfilter — using it on the top-level `filter` raises an error. `id` values are scoped to the filter definition only; they are unrelated to the `audit_log_filter_id` system variable.

## Best practices

1. Start wide, then narrow — begin with a noisy catch-all in staging, then peel away classes you do not need.
2. Test combinations — overlapping rules and assignments surprise people; validate on a clone.
3. Plan retention — pair filters with rotation, pruning, and disk budgets ([Manage the Audit Log Filter files](manage-audit-log-filter.md)).
4. Watch overhead — granular auditing costs CPU and I/O; ramp detail gradually and watch latency plus `audit_log_filter_*` status counters.


## Worked example: financial tracking filter

This page authors the JSON. To deploy a finished filter, store it with [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition), bind it to accounts with [`audit_log_filter_set_user()`](audit-log-filter-variables.md#audit_log_filter_set_useruser_name-filter_name), and reload sessions with [`audit_log_filter_flush()`](audit-log-filter-variables.md#audit_log_filter_flush). The [Audit Log Filter quickstart](audit-log-filter-quickstart.md) and [Install the audit log filter](install-audit-log-filter.md) cover the deploy sequence.

The following worked example threads JSON authoring, deployment, and verification end-to-end.

This filter logs DML on two tables in `financial_db` and all connection events. Account scoping is applied at assignment time, since `table_access` events do not carry a user field.

```sql
-- Create the filter
SELECT audit_log_filter_set_filter('financial_tracking', '{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "event": [
          {
            "name": ["insert", "update", "delete"],
            "log": {
              "and": [
                { "field": { "name": "table_database.str", "value": "financial_db" } },
                {
                  "or": [
                    { "field": { "name": "table_name.str", "value": "accounts" } },
                    { "field": { "name": "table_name.str", "value": "transactions" } }
                  ]
                }
              ]
            }
          }
        ]
      },
      {
        "name": "connection",
        "event": [
          { "name": "connect" },
          { "name": "disconnect" }
        ]
      }
    ]
  }
}');
```

Field-value typing (JSON numbers for integer fields such as `status`, strings for `*.str` fields, and `"::tcp/ip"`-style symbolic constants for `connection_type`) is covered under [`audit_log_filter_set_filter()`](audit-log-filter-variables.md#audit_log_filter_set_filterfilter_name-definition).

Assign the filter to just the accounts that should be audited instead of to `%`:

```sql
-- Assign to specific accounts; other users keep their existing filter (or none).
SELECT audit_log_filter_set_user('admin@%',        'financial_tracking');
SELECT audit_log_filter_set_user('finance_team@%', 'financial_tracking');
```

The filter records:

* `insert` / `update` / `delete` on `financial_db.accounts` and `financial_db.transactions` for the two assigned accounts.

* `connect` / `disconnect` events for the same accounts.

* Nothing for other users (they are not bound to this filter) and nothing outside the declared schema/tables unless you extend the JSON.

Inspect metadata directly:

```sql
-- Check created filters
SELECT * FROM mysql.audit_log_filter;

-- Check user assignments
SELECT * FROM mysql.audit_log_user;
```

Tail the audit file (default under the data directory) to confirm events stream as expected.

## Additional reading

* [Block statements with an audit log filter](block-statements-with-audit-filter.md)
* [Redact audit log fields](redact-audit-log-fields.md)
* [Audit Log Filter definition fields](audit-log-filter-definition-fields.md)
* [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Audit Log Filter quickstart](audit-log-filter-quickstart.md)
* [Audit Log Filter restrictions](audit-log-filter-restrictions.md)
