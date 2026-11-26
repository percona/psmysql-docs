> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Uninstall Audit Log Filter

To remove the Audit Log Filter component from the server, run:

```sql
UNINSTALL COMPONENT 'file://component_audit_log_filter';
```

What this does:

- `UNINSTALL COMPONENT` — Drops a previously installed component from the server.
- `file://component_audit_log_filter` — URN for the Audit Log Filter component, which applies your rules and decides which audit events are recorded.

## Additional reading

- [Install the audit log filter](https://docs.percona.com/percona-server/8.4/install-audit-log-filter.md)
- [Audit Log Filter overview](https://docs.percona.com/percona-server/8.4/audit-log-filter-overview.md)
- [Upgrade components](https://docs.percona.com/percona-server/8.4/upgrade-components.md)
- [Disable Audit Log Filter logging](https://docs.percona.com/percona-server/8.4/disable-audit-log-filter.md)
- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/8.4/audit-log-filter-variables.md)
