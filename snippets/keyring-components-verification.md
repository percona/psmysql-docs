
## Verify the keyring component

After you start Percona Server for MySQL, confirm that the keyring component loaded and initialized. Query the `performance_schema.keyring_component_status` table:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

The query returns one row for each status key that the loaded component reports. The `Component_status` row indicates the result of initialization:

| `Component_status` value | Meaning | Recovery |
|---|---|---|
| `Active` | The component loaded and initialized successfully | None |
| `Disabled` | The component loaded but failed to initialize, typically due to a configuration error | Review the server error log, correct the configuration file, then run `ALTER INSTANCE RELOAD KEYRING` |

If a keyring component fails to load entirely, the server does not start. Check the server error log for diagnostic messages.

For the complete list of status keys that each component reports, see [keyring_component_status Table :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/performance-schema-keyring-component-status-table.html) in the MySQL Reference Manual.
