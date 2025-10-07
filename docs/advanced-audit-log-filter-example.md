# Advanced audit log filter configuration

## Overview

Audit log filtering controls which database events the audit log plugin records. This configuration example shows how to set up comprehensive logging for general users while completely disabling logging for monitoring users.

## Prerequisites

Before configuring audit log filters, ensure that:

* The audit log filter plugin is installed and enabled

* You have administrative privileges to configure audit log settings

* The audit log filter plugin has the necessary permissions to write log files

You can tune the audit log filter plugin using the following variables:


| Variable | Default | Typical value for heavy logging | Description |
|----------|---------|--------------------------------|-------------|
| [audit-log-filter](audit-log-filter-variables.md#audit-log-filter) | OFF | ON | Master switch for the filter subsystem. |
| [audit_log_filter_max_size](audit-log-filter-variables.md#audit_log_filter_max_size) | 0 (unlimited) | 1073741824 (1 GB) | Max size of the filter definition file; rotation occurs when exceeded. |
| [audit_log_filter_prune_seconds](audit-log-filter-variables.md#audit_log_filter_prune_seconds) | 0 (no pruning) | 86400 (24 h) | Age after which old filter entries are pruned. |
| [audit_log_filter_strategy](audit-log-filter-variables.md#audit_log_filter_strategy) | default | default | Determines how overlapping filters are resolved (keep‑first vs. most‑specific). |
| [audit_log_filter_rotate_on_size](audit-log-filter-variables.md#audit_log_filter_rotate_on_size) | 0 | 1 | Rotate the audit log file when it reaches `audit_log_buffer_size`. |
| [audit_log_filter_file](audit-log-filter-variables.md#audit_log_filter_file) | `<datadir>/audit.log` | *unchanged* | Path of the audit log file (requires server restart to change). |

Most of these variables in the table are dynamic system variables – you can view or change them at runtime with `SHOW GLOBAL VARIABLES / SET GLOBAL`.

Only `audit_log_file` (the path) is static; changing this variable requires a restart.

## Rule precedence

* User-Specific Filter Wins: A specific user filter set with `audit_log_filter_set_user` always takes precedence over the wildcard (`%`) filter.

* Most Specific Pattern Wins: If a user matches multiple connection patterns (e.g., `user@host`), the most specific pattern is applied. For example, `monitor@%` is applied instead of the less specific `%`.

* Last Call Wins: When a user has multiple filters attached using `audit_log_filter_set_user`, the filter from the last execution of that command is the one that is applied.

### Global system control

* The `audit-log-filter` global can enable or disable the auditing subsystem but does not affect the internal precedence logic of individual user filters.

## Use case requirements

The following requirements define the audit logging behavior:

For user % (wildcard/general users):

* Log SELECT operations

* Log INSERT operations

* Log UPDATE operations

* Log DELETE operations

* Log TRUNCATE operations

* Log CREATE operations

* Log DROP operations

* Log ALTER operations

* Log connection events (successful and failed)

* Log disconnection events

For user monitor:

* Log no events (completely disable logging)

## Filter configuration details

The configuration uses two distinct filter types:

* Comprehensive logging filter: Captures connection events and specific SQL operations for general users
* No logging filter: Completely disables audit logging for monitoring users

The filter applies to users matching the specified patterns:

* `%` matches all users (wildcard pattern)

* `monitor@%` matches users with the monitor username from any host

## Implementation

Create and apply the audit log filters using the following configuration:

```sql
-- Define a custom filter for comprehensive logging
SET @log_custom_filter = '{
  "filter": {
    "class": [
      {
        "name": "connection",
        "event": [
          { "name": "connect" },
          { "name": "disconnect" },
          { "name": "error" }               /* captures failed login attempts */
        ]
      },
      {
        "name": "general",
        "event": [
          {
            "name": "status",
            "log": {
              "or": [
                { "field": { "name": "general_sql_command.str", "value": "select" } },
                { "field": { "name": "general_sql_command.str", "value": "insert" } },
                { "field": { "name": "general_sql_command.str", "value": "update" } },
                { "field": { "name": "general_sql_command.str", "value": "delete" } },
                { "field": { "name": "general_sql_command.str", "value": "truncate" } },
                { "field": { "name": "general_sql_command.str", "value": "create" } },   /* DDL fix */
                { "field": { "name": "general_sql_command.str", "value": "alter" } },    /* DDL fix */
                { "field": { "name": "general_sql_command.str", "value": "drop" } }     /* DDL fix */
              ]
            }
          }
        ]
      }
    ]
  }
}';
```

```sql
-- Verify JSON syntax before loading (optional but recommended)
SELECT JSON_VALID(@log_custom_filter) AS is_valid;
```

`JSON_VALID()` returns `1` if the string is valid JSON, `0` otherwise.

```sql
-- Define a filter that disables logging
SET @log_none_filter = '{
  "filter": { "log": false }
}';
```

```sql
-- Define a filter that logs only specific SQL commands
SET @log_custom_filter = '{
  "filter": {
    "log": true,
    "rules": [
      {
        "type": "sql",
        "conditions": [
          { "field": { "name": "general_sql_command.str", "value": "select" } },
          { "field": { "name": "general_sql_command.str", "value": "insert" } },
          { "field": { "name": "general_sql_command.str", "value": "update" } },
          { "field": { "name": "general_sql_command.str", "value": "delete" } },
          { "field": { "name": "general_sql_command.str", "value": "create" } },
          { "field": { "name": "general_sql_command.str", "value": "alter" } },
          { "field": { "name": "general_sql_command.str", "value": "drop" } }
        ]
      }
    ]
  }
}';
```

```sql
-- Apply filters to specific users
SELECT audit_log_filter_set_filter('log_custom', @log_custom_filter);
SELECT audit_log_filter_set_filter('log_none', @log_none_filter);

-- Set user-specific audit logging rules
SELECT audit_log_filter_set_user('%', 'log_custom');
SELECT audit_log_filter_set_user('monitor@%', 'log_none');
```



## Testing and validation

Verify that the audit log filters work correctly by performing these tests:

```sql
-- Check that filters are applied correctly
SELECT audit_log_filter_set_user('testuser@localhost', 'log_custom');
SELECT audit_log_filter_set_user('monitor@localhost', 'log_none');

-- Verify filter assignments
SELECT * FROM mysql.audit_log_filter;
SELECT * FROM mysql.audit_log_user;
```

Test the configuration by:
* Connecting as a general user and performing various SQL operations

* Connecting as a monitor user and performing operations

* Checking the audit log file for expected entries

## Troubleshooting

Common issues and solutions:


| Issue                        | Description                                                                                  |
|-------------------------------|----------------------------------------------------------------------------------------------|
| Filter not applied            | Verify that the audit log plugin is enabled and the filter names are correct                |
| Unexpected logging            | Check user pattern matching and filter precedence rules                                     |
| Performance impact            | Monitor system performance when comprehensive logging is enabled                            |


## Configuration Breakdown

| Filter Type | Description | Key Characteristics |
|------------|-------------|---------------------|
| <b>Wildcard User Filter (`%`)</b> | Captures operations for general users | • Ensures <b>comprehensive auditing</b><br>• Applies to all users matching the wildcard<br>• Logs multiple SQL operation types |
| <b>Monitor User Filter</b> | Logging control for specific users | • <b>Completely disables logging</b><br>• Provides granular user-level exclusion<br>• Prevents any audit trail for specified users |
| <b>Flexible Matching</b> | User pattern-based filtering | • Uses `%` wildcard for broad rule application<br>• Enables dynamic user group configurations<br>• Simplifies management of similar user accounts |

## Security considerations

When configuring audit log filters:

* Review filter rules regularly to ensure they meet security requirements

* Consider the impact of comprehensive logging on system performance

* Ensure that monitoring users cannot bypass audit logging through filter manipulation

* Document all filter changes for compliance and auditing purposes

## Performance impact

Comprehensive audit logging affects system performance:

* Each logged event requires disk I/O operations

* Large numbers of concurrent users increase logging overhead

* Consider log rotation and cleanup strategies for long-term operation

## Best practices

* Always align audit filters with specific security and compliance requirements

* Regularly review and update audit logging configurations

* Use the principle of least privilege when defining logging scopes

* Test filter configurations in a development environment before applying to production

* Monitor audit log file sizes and implement appropriate rotation policies
