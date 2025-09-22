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

Enabling the plugin produces a log file that contains a record of server activity. The log file has information on connections and databases accessed by that connection. 

The plugin uses the `mysql` system database to store filter and user account data. Set the [`audit_log_filter_database`](audit-log-filter-variables.md#audit_log_filter_database) variable at server startup to select a different database. When you change the database, you must create the required tables in the new database and migrate any existing filter data.

The `AUDIT_ADMIN` privilege is required to enable users to manage the Audit Log Filter plugin.

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

Define the privilege at runtime at the startup of the server. The associated Audit Log Filter privilege can be unavailable if the plugin is not enabled.

### `AUDIT_ADMIN`

This privilege is defined by the server and enables the user to configure the plugin.

### `AUDIT_ABORT_EXEMPT`

This privilege allows queries from a user account to always be executed. An `abort` item does not block them. This ability lets the user account regain access to a system if an audit is misconfigured. The query is logged due to the privilege. User accounts with the `SYSTEM_USER` privilege have the `AUDIT_ABORT_EXEMPT` privilege.

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