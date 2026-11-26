> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Disable Audit Log Filter logging

The `audit_log_filter.disable` system variable turns audit logging on or off for all connections:

| Value                              | Effect                 |
| ---------------------------------- | ---------------------- |
| `audit_log_filter.disable = true`  | Stops audit logging.   |
| `audit_log_filter.disable = false` | Enables audit logging. |

Set it in an option file, on the command line, or at runtime:

```sql
SET GLOBAL audit_log_filter.disable = true;
```

## Privileges required

Runtime changes require both:

- `AUDIT_ADMIN`
- `SYSTEM_VARIABLES_ADMIN`

## Additional reading

- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.md) — `audit_log_filter.disable`
- [Audit Log Filter overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.md)
- [Uninstall Audit Log Filter](https://docs.percona.com/percona-server/8.4/uninstall-audit-log-filter.md)
- [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.md)
