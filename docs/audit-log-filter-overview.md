# Audit Log Filter overview

The Audit Log Filter plugin provides comprehensive database auditing capabilities for Percona Server. The plugin allows you to monitor, log, and block connections or queries actively executed on the selected server.

## What is audit log filter?

The Audit Log Filter plugin enables you to:

| Issue                | Description                                                                                   |
|:----------------------|:----------------------------------------------------------------------------------------------|
| Monitor database activity | Track all database connections, queries, and administrative actions                         |
| Comply with regulations   | Meet compliance requirements for database auditing                                          |
| Enhance security          | Detect suspicious activities and unauthorized access attempts                              |
| Control access            | Block specific queries or connections based on configurable rules                          |
| Generate reports          | Create detailed audit trails for security analysis                                        |

## What the plugin does

The plugin uses the `mysql` system database to store filter and user account data. Set the [`audit_log_filter_database`](audit-log-filter-variables.md#audit_log_filter_database) variable at server startup to select a different database. When you change the database, you must create the required tables in the new database and migrate any existing filter data.

* Database connections and disconnections

## System requirements

* Percona Server version: 8.0.34-26 or later

* Storage engine: InnoDB (for audit tables)

* Privileges: SYSTEM_VARIABLES_ADMIN to configure the plugin

* Disk space: Sufficient space for audit log files

* Memory: Additional memory overhead for audit processing

## Basic configuration

The Audit Log Filter plugin uses several key configuration variables:

* Dynamic variables: Can be changed at runtime using `SET GLOBAL` without restarting the server

* Read-only variables: Can only be changed at server startup in the configuration file

* [`audit_log_filter_enable`](audit-log-filter-variables.md#audit_log_filter_enable): Enable or disable the audit filter engine (dynamic)

* [`audit_log_filter_database`](audit-log-filter-variables.md#audit_log_filter_database): Database for storing filter definitions (read-only)

* [`audit_log_filter_mode`](audit-log-filter-variables.md#audit_log_filter_mode): Set to ALLOW (whitelist) or DENY (blacklist) (dynamic)

* [`audit_log_filter_rotate_on_size`](audit-log-filter-variables.md#audit_log_filter_rotate_on_size): Log file rotation size limit (dynamic)

## Privileges

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

The Audit Log Filter plugin uses `mysql` system database tables in the `InnoDB` storage engine. These tables store user account data and filter data.

The `audit_log_filter` table stores the definitions of the filters and has the following column definitions:

| Column name | Description |
|:-----------:|:-----------:|
| NAME | Name of the filter |
| FILTER | Definition of the filter linked to the name as a JSON value |

The `audit_log_user` table stores account data and has the following column definitions:

| Column name | Description |
|:-----------:|:-----------:|
| USER | The account name of the user |
| HOST | The account name of the host |
| FILTERNAME | The account filter name |

## Log formats and output

The Audit Log Filter plugin supports multiple log formats:

* JSON format: Machine-readable format for automated processing

* XML (new): Human-readable format with structured data

* XML (old): Legacy XML format for backward compatibility

The plugin logs various types of events:

* Connection events: User logins, logouts, and connection failures

* Query events: SQL statements executed by users

* Administrative events: Server configuration changes

* Error events: Failed operations and security violations

## Security considerations

When implementing the Audit Log Filter plugin, consider these security aspects:

| Issue               | Description                                                                                   |
|:--------------------|:----------------------------------------------------------------------------------------------|
| Performance impact   | Audit logging adds overhead to database operations                                            |
| Storage requirements | Audit logs can grow large; plan for log rotation and archival                                 |
| Sensitive data       | Configure filters to avoid logging sensitive information                                     |
| Access control       | Restrict access to audit log files and configuration                                          |
| Backup strategy      | Include audit logs in your backup and recovery procedures                                    |
## References

[Install the Audit Log Filter](install-audit-log-filter.md)

[Audit Log Filter Variables & Functions](audit-log-filter-variables.md)
