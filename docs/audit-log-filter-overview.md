# Audit Log Filter overview

The Audit Log Filter component allows you to monitor, log, and block a connection or query actively executed on the selected server. 

Enabling the component produces a log file that contains a record of server activity. The log file has information on connections and databases accessed by that connection. 

The component uses the `mysql` system database to store filter and user account data. Set the [`audit_log_filter.database`](audit-log-filter-variables.md#audit_log_filterdatabase) variable at server startup to select a different database.

The `AUDIT_ADMIN` privilege is required to enable users to manage the Audit Log Filter component.

## Privileges

Define the privilege at runtime at the startup of the server.

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
