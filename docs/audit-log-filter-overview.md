# Audit Log Filter overview

The Audit Log Filter component allows you to monitor and log database activity on the selected server. The component can also block queries or connections that match specific security rules, providing an additional layer of protection.

Enabling the component produces a log file that contains a record of server activity. The log file has information on connections and databases accessed by that connection.

The component uses the `mysql` system database to store filter and user account data. Set the [`audit_log_filter.database`](audit-log-filter-variables.md#audit_log_filterdatabase) variable at server startup to select a different database.

For installation instructions, see [Install the audit log filter](install-audit-log-filter.md). For detailed information on writing filter definitions, see [Write audit_log_filter definitions](write-filter-definitions.md).

## What is a filter?

A filter is a set of rules that determines which database events are logged or blocked by the Audit Log Filter component. Filters are defined using JSON and specify criteria such as:

* Which users to monitor

* Which databases or tables to track

* What types of operations to log (connections, queries, table access, etc.)

* Whether to log or block matching events

### How filters work

When a database event occurs (such as a user connecting, executing a query, or accessing a table), the Audit Log Filter component checks if any active filters match that event. If a filter matches:

* Logging: The event is written to the audit log file

* Blocking: If the filter includes an `abort` item, the operation can be prevented from executing

Filters are stored in the `mysql.audit_log_filter` table and can be assigned to specific user accounts or set as a default filter for all users.

### Filter components

A filter definition includes:

* Event classes: Categories of events (connection, table_access, general, etc.)

* Event subclasses: Specific types within a class (connect, disconnect, read, write, etc.)

* Filter criteria: Conditions such as user, database, table, status, etc.

* Action: Whether to log the event, block it, or both

For more details on writing filter definitions, see [Write audit_log_filter definitions](write-filter-definitions.md).

## Filter assignment and precedence

The Audit Log Filter component uses a specific precedence order when determining which filter to apply to a user connection.

### Filter assignment logic

When a new connection is established, the component searches for a filter assignment in the following order:

1. User-specific filter: If the user account has a filter directly assigned via `audit_log_filter_set_user()`, that filter is used.

2. Default filter: If no user-specific filter exists, but a default filter is assigned to the `%` account, that filter is used.

3. No filtering: If neither a user-specific nor default filter exists, no events are processed.

### Default account filter

The default account is represented by `%` as the account name. Assigning a filter to `%` makes it the default filter for all users who don't have a specific filter assigned.

Example:

```sql
-- Assign a default filter that logs all connection events
SELECT audit_log_filter_set_user('%', 'log_all_connections');
```

### Filter precedence scenarios

| Scenario | User Filter | Default Filter | Result |
|----------|------------|---------------|--------|
| User has specific filter | Assigned | Assigned | User's specific filter is used |
| User has no filter, default exists | None | Assigned | Default filter is used |
| Neither exists | None | None | No filtering (events not processed) |
| User filter removed | Removed | Assigned | Default filter is used for new connections |

### Current sessions vs new connections

Important behavior:

* Filter changes take effect for new connections immediately

* Current sessions continue using the filter that was active when they connected

* To apply a new filter to current sessions, users must:

  * Execute `CHANGE_USER` command, or

  * Disconnect and reconnect

Example:

1. User `admin@localhost` connects → Uses filter `filter_A`

2. Administrator changes user's filter to `filter_B`

3. User's current session → Still uses `filter_A`

4. User disconnects and reconnects → Now uses `filter_B`

### Removing filters

When you remove a filter using `audit_log_filter_remove_filter()`:

* The filter is unassigned from all users (including the default `%` account)

* Current sessions are detached from the filter

* New connections for affected users fall back to:

  * Default filter (if one exists), or

  * No filtering (if no default exists)

### Best practices

1. Always set a default filter for the `%` account to ensure all connections are logged
2. Test filter changes before deploying to production
3. Document filter assignments to track which users have specific filters
4. Use wildcards in `audit_log_filter_set_user()` (available starting from version 8.4.4, see [release notes](release-notes/8.4.4-4.md)) for flexible user matching

## Blocking queries and connections

The Audit Log Filter component can not only log events but also block queries or connections that match specific filter rules. This blocking capability provides an additional layer of security by preventing unauthorized or dangerous operations.

When a filter includes an `abort` item set to `true`, matching queries or connections are blocked before execution. The blocked operation is still logged to the audit log, but the query does not execute. Users with the `AUDIT_ABORT_EXEMPT` privilege (or `SYSTEM_USER` privilege) are exempt from blocking, ensuring administrators can always regain access if filters are misconfigured.

For detailed information on blocking syntax, examples, and best practices, see [Write audit_log_filter definitions](write-filter-definitions.md#blocking-queries-and-connections).

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

You can modify these tables directly using SQL, but you must call `audit_log_filter_flush()` after making changes for them to take effect. For more information on managing filters, see [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md).

## Privileges

The `AUDIT_ADMIN` privilege is required to enable users to manage the Audit Log Filter component. Define the privilege at runtime at the startup of the server. The associated Audit Log Filter privilege can be unavailable if the component is not enabled.

### `AUDIT_ADMIN`

The `AUDIT_ADMIN` privilege is defined by the server and enables the user to configure the component. Users with this privilege can:

* Create, modify, and remove filters

* Assign filters to user accounts

* Manage audit log configuration

* Rotate and manage log files

### `AUDIT_ABORT_EXEMPT`

The `AUDIT_ABORT_EXEMPT` privilege allows queries from a user account to always be executed. An `abort` item does not block them. This exemption ability lets the user account regain access to a system if an audit is misconfigured. The query is logged due to the privilege. User accounts with the `SYSTEM_USER` privilege have the `AUDIT_ABORT_EXEMPT` privilege.

## Privilege interactions

The following table shows how privileges interact with audit log filter functionality:

| Privilege | Can Configure Filters | Can Block Queries | Exempt from Blocks | Notes |
|-----------|---------------------|-------------------|-------------------|-------|
| `AUDIT_ADMIN` | Yes | Yes | No | Required for filter management functions |
| `AUDIT_ABORT_EXEMPT` | No | No | Yes | Queries always execute even if blocked by filter |
| `SYSTEM_USER` | No | No | Yes | Automatically has `AUDIT_ABORT_EXEMPT` privilege |
| `SUPER` | Yes (legacy) | Yes | No | Deprecated in MySQL 8.0+, use `AUDIT_ADMIN` instead |

!!! note "Privilege precedence"

    Users with `AUDIT_ABORT_EXEMPT` (or `SYSTEM_USER`) can always execute queries, even when filters are configured to block them. This privilege precedence ensures administrators can regain access if filters are misconfigured.

## Next steps

Now that you understand the basics of the Audit Log Filter component:

* [Install the audit log filter](install-audit-log-filter.md) - Set up the component

* [Write audit_log_filter definitions](write-filter-definitions.md) - Learn how to create filters

* [Filter the Audit Log Filter logs](filter-audit-log-filter-files.md) - Manage filters and assignments

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) - Reference for all functions and variables

--8<--- "get-help-snip.md"
