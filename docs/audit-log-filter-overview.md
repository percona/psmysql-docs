# Audit Log Filter overview

The Audit Log Filter plugin provides security monitoring and access control for your MySQL server. The plugin allows you to monitor database activity, log specific events, and block connections or queries based on configurable rules.

## What the plugin does

The plugin monitors server activity and creates detailed log files containing information about:

* Database connections and disconnections

* SQL statements executed by users

* Database objects accessed

* User account activity

## How it works

The plugin uses the `mysql` system database to store filter configurations and user account assignments. You can change the database location by setting the [`audit_log_filter_database`](audit-log-filter-variables.md#audit_log_filter_database) variable at server startup.

## Required privileges

The `AUDIT_ADMIN` privilege is required to manage the Audit Log Filter plugin configuration. Define privileges at runtime at server startup. Audit Log Filter privileges may be unavailable if the plugin is not enabled.

### `AUDIT_ADMIN`

This privilege is required to manage audit log filters and their configuration. Users with this privilege can create, modify, and remove filters, assign filters to user accounts, and perform other administrative operations.

Required for audit log filter functions such as:

* Creating and removing filters

* Assigning filters to user accounts

* Flushing filter configurations

* Managing audit log file rotation

### `AUDIT_ABORT_EXEMPT`

This privilege allows queries from a user account to bypass blocking actions in audit log filters. When a filter is configured to block or deny queries, users with this privilege can still execute their queries successfully.

The privilege provides emergency access when audit filters are misconfigured and would otherwise block legitimate operations. Queries executed by users with this privilege are still logged for audit compliance.

User accounts with the `SYSTEM_USER` privilege automatically have the `AUDIT_ABORT_EXEMPT` privilege.

## Performance considerations

The Audit Log Filter plugin consumes system resources while running. Consider the following factors when enabling the plugin:

* CPU overhead: Filtering and logging operations require additional CPU cycles for each audited event

* Memory usage: The plugin uses memory for buffering log entries and maintaining filter configurations

* Disk I/O: Log file writes create additional disk activity, especially on high-traffic systems

* Storage requirements: Audit log files can grow large and consume significant disk space over time

* Network impact: If logging to remote systems, network bandwidth usage increases

* Complex filtering: Queries that monitor multiple events and users consume more resources than simple filters

Monitor system performance after enabling the plugin and adjust filter configurations or log rotation settings as needed to maintain acceptable performance levels.

## Complex filtering considerations

The Audit Log Filter plugin supports sophisticated filtering rules that can monitor multiple criteria simultaneously. However, complex filters require more processing power:

* Multiple event types: Filters that check for several event classes (connection, query, table access) use more CPU cycles

* Multiple user accounts: Monitoring many users simultaneously increases memory usage and processing time

* Nested conditions: JSON filters with multiple nested conditions require more evaluation time

* Real-time evaluation: Each query must be evaluated against all active filters, so more filters mean more overhead

Start with simple filters and gradually add complexity while monitoring performance impact.

## Comparison with audit log plugin

The Audit Log Filter plugin is the successor to the [audit log plugin](audit-log-plugin.md) and provides significant improvements:

* Enhanced filtering: More granular control over what gets logged and when

* Blocking capabilities: Can block queries and connections, not just log them

* JSON configuration: More flexible filter definitions using JSON format

* Multiple output formats: Supports XML and JSON log formats

* Advanced features: Compression, encryption, and remote logging capabilities

## Audit Log Filter tables

The Audit Log Filter plugin uses `mysql` system database tables in the `InnoDB` storage engine. These tables store user account data and filter data. When you start the server, change the plugin's database with the `audit_log_filter_database` variable.

The `audit_log_filter` table stores the definitions of the filters and has the following column definitions:

| Column name | Data type | Description |
|-------------|-----------|-------------|
| NAME | VARCHAR(64) | Name of the filter |
| FILTER | JSON | Definition of the filter linked to the name as a JSON value |

The `audit_log_user` table stores account data and has the following column definitions:

| Column name | Data type | Description |
|-------------|-----------|-------------|
| USER | VARCHAR(32) | The account name of the user |
| HOST | VARCHAR(255) | The account name of the host |
| FILTERNAME | VARCHAR(64) | The account filter name |

## Next steps

To get started with the Audit Log Filter plugin:

1. [Install the Audit Log Filter](install-audit-log-filter.md) - Installation instructions

2. [Filter Audit Log Files](filter-audit-log-filter-files.md) - Creating and managing filters

3. [Audit Log Filter Variables](audit-log-filter-variables.md) - Configuration options

4. [Manage Audit Log Files](manage-audit-log-filter.md) - Log file management
