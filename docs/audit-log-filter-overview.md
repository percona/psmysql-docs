# Audit Log Filter overview

The Audit Log Filter component allows you to monitor, log, and block a connection or query actively executed on the selected server. 

Enabling the component produces a log file that contains a record of server activity. The log file has information on connections and databases accessed by that connection. 

Set [`audit_log_filter.format`](audit-log-filter-variables.md#audit_log_filterformat) at startup to choose an output format. [NEW](audit-log-filter-new.md) (default) writes new-style XML with one `<AUDIT_RECORD>` element per event. [OLD](audit-log-filter-old.md) writes the original XML layout. [JSON](audit-log-filter-json.md) writes a JSON array of pretty-printed event objects. [JSONL](audit-log-filter-json.md) (introduced in Percona Server for MySQL 8.4.9-9) writes each event as a single compact JSON object on its own line inside a wrapping JSON array, making it easy to process with line-oriented tools and log aggregation systems. See [format overview](audit-log-filter-formats.md) for a side-by-side comparison.

The [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) variable, introduced in Percona Server for MySQL 8.4.9-9, controls which event classes are processed. The default mode is `REDUCED`, which limits logging to `general/status`, `connection/connect`, `connection/disconnect`, `connection/change_user`, `table_access/*`, and `message/*`. Set `event_mode=FULL` to process all event classes. Before Percona Server for MySQL 8.4.9-9 all events were always written (equivalent to `FULL`).

The component uses the `mysql` system database to store filter and user account data. Set the [`audit_log_filter.database`](audit-log-filter-variables.md#audit_log_filterdatabase) variable at server startup to select a different database.

The `AUDIT_ADMIN` privilege is required to enable users to manage the Audit Log Filter component.

## Privileges

Define the privilege at runtime at the startup of the server. The associated Audit Log Filter privilege can be unavailable if the component is not enabled.

### `AUDIT_ADMIN`

This privilege is defined by the server and enables the user to configure the component.

### `AUDIT_ABORT_EXEMPT`

This privilege allows queries from a user account to always be executed. An `abort` item does not block them. This ability lets the user account regain access to a system if an audit is misconfigured. The query is logged due to the privilege. User accounts with the `SYSTEM_USER` privilege have the `AUDIT_ABORT_EXEMPT` privilege.

## Audit Log Filter tables

The Audit Log Filter component uses `mysql` system database tables in the `InnoDB` storage engine. These tables store user account data and filter data. When you start the server, change the component's database with the `audit_log_filter.database` variable.

The `audit_log_filter` table stores the definitions of the filters and has the following column definitions:

| Column name | Description                                                   |
|-------------|---------------------------------------------------------------|
| NAME        | Name of the filter                                            |
| FILTER      | Definition of the filter linked to the name as a JSON value  |

The `audit_log_user` table stores account data and has the following column definitions:

| Column name  | Description                         |
|--------------|-------------------------------------|
| USER         | The account name of the user        |
| HOST         | The account name of the host        |
| FILTERNAME   | The account filter name             |
