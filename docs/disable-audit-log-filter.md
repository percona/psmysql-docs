# Disable Audit Log Filter logging

The `audit_log_filter.disable` system variable turns audit logging on or off for all connections.

| Value | Effect |
|---|---|
| `audit_log_filter.disable = true` | Stops audit logging. |
| `audit_log_filter.disable = false` | Enables audit logging. |

Set the variable in an option file, on the command line, or at runtime:

```sql
SET GLOBAL audit_log_filter.disable = true;
```

## Privileges required

Runtime changes require both of the following privileges:

* `AUDIT_ADMIN`

* `SYSTEM_VARIABLES_ADMIN`

## Additional reading

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md) — `audit_log_filter.disable`

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Uninstall Audit Log Filter](uninstall-audit-log-filter.md)

* [Install the audit log filter](install-audit-log-filter.md)
