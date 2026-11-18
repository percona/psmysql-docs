> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Uninstall Audit Log Filter

To remove the Audit Log Filter component from the server, run the following statement:

```
UNINSTALL COMPONENT 'file://component_audit_log_filter';
```

The statement performs the following actions:

- `UNINSTALL COMPONENT` drops a previously installed component from the server.
- `file://component_audit_log_filter` is the URN for the Audit Log Filter component. The component applies the configured rules and decides which audit events are recorded.

## Additional reading

- [Install the audit log filter](https://docs.percona.com/percona-server/9.7/install-audit-log-filter.html)
- [Audit Log Filter overview](https://docs.percona.com/percona-server/9.7/audit-log-filter-overview.html)
- [Upgrade components](https://docs.percona.com/percona-server/9.7/upgrade-components.html)
- [Disable Audit Log Filter logging](https://docs.percona.com/percona-server/9.7/disable-audit-log-filter.html)
- [Audit log filter functions, options, and variables](https://docs.percona.com/percona-server/9.7/audit-log-filter-variables.html)
