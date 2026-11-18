> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Disable Audit Log Filter logging

The `audit_log_filter.disable` system variable turns audit logging on or off for all connections.

| Value                              | Effect                 |
| ---------------------------------- | ---------------------- |
| `audit_log_filter.disable = true`  | Stops audit logging.   |
| `audit_log_filter.disable = false` | Enables audit logging. |

Set the variable in an option file, on the command line, or at runtime:

```
SET GLOBAL audit_log_filter.disable = true;
```

## Privileges required

Runtime changes require both of the following privileges:

- `AUDIT_ADMIN`
- `SYSTEM_VARIABLES_ADMIN`

## Additional reading

- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html) — `audit_log_filter.disable`
- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.html)
- [Uninstall Audit Log Filter](https://docs.percona.com/percona-server/9.7/uninstall-audit-log-filter.html)
- [Install the audit log filter](https://docs.percona.com/percona-server/9.7/install-audit-log-filter.html)
