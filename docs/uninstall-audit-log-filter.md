# Uninstall Audit Log Filter

To remove the Audit Log Filter component from the server, run:

```sql
UNINSTALL COMPONENT 'file://component_audit_log_filter';
```

What this does:

* `UNINSTALL COMPONENT` — Drops a previously installed component from the server.
* `file://component_audit_log_filter` — URN for the Audit Log Filter component, which applies your rules and decides which audit events are recorded.

## Additional reading

* [Install the audit log filter](install-audit-log-filter.md)
* [Audit Log Filter overview](audit-log-filter-overview.md)
* [Upgrade components](upgrade-components.md)
* [Disable Audit Log Filter logging](disable-audit-log-filter.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
