# Too Many Connections warning in the MySQL Error Log

When the [log_error_verbosity](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_log_error_verbosity) system variable is set to `2` or higher, the server generates a `Too many connections` warning in the error log.

## Benefits

This warning provides the following benefits:

| Benefit | Description |
| --- | --- |
| Monitoring server load | The "Too many connections" warning provides a clear indication that the database server is experiencing a high volume of incoming connections, which can be a sign of increased server load or potential performance issues. |
| Proactive troubleshooting | By monitoring the error log for this warning, developers and DBAs can quickly identify when the server is reaching its connection limit and take appropriate actions, such as scaling up resources or optimizing connection management. |
| Capacity planning | The frequency and patterns of "Too many connections" warnings can help database server teams plan for future infrastructure needs, ensuring that the server can handle the expected workload without performance degradation. |
| Identifying connection leaks | Persistent "Too many connections" warnings may indicate a problem with connection management, such as connections not being properly closed or released. This can help identify and address potential connection leaks. |
| Compliance and auditing | The error log, including the "Too many connections" warnings, can be valuable for compliance and auditing purposes, providing a record of server behavior and potential issues. |

## Version specific information

In version 8.0.12-1, the "Too many connections" warning feature was ported from Percona Server for MySQL 5.7.