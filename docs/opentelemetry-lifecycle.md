# Install and manage the OpenTelemetry component

!!! note
    The OpenTelemetry component (`component_telemetry`) is a community MySQL 9.7 feature. Percona Server for MySQL includes this component. The component works the same as in upstream MySQL.

The OpenTelemetry component is a dynamically loadable module. Percona Server for MySQL does not load this component by default. To stream metrics, traces, and logs to your configured endpoints, install the component first.

## Install the component

To install the component, connect to the server with a user account that has the `INSERT` privilege on the `mysql.component` system table. Run the following statement:

```sql
INSTALL COMPONENT 'file://component_telemetry';
```

This statement registers the component in the `mysql.component` system table. Percona Server loads the component automatically on every server restart. You do not need to add loading directives to your `my.cnf` file.

## Verify the installation

To confirm that the component is loaded, query the `mysql.component` system table:

```sql
SELECT component_urn
FROM mysql.component
WHERE component_urn = 'file://component_telemetry';
```

A returned row with `file://component_telemetry` confirms the installation. You can then configure your metrics, traces, and logging endpoints.

## Uninstall the component

You can remove the component without restarting the database server.

!!! warning
    Uninstalling the component stops all active telemetry streams immediately. This action creates gaps in your monitoring dashboards. Before you remove the component, confirm that your observability platforms, such as Percona Monitoring and Management or an external OpenTelemetry collector, do not depend on this data.

To uninstall the component, run the following statement:

```sql
UNINSTALL COMPONENT 'file://component_telemetry';
```

This statement unloads the component from memory and also removes the component entry from the `mysql.component` table. After uninstallation, the component does not load during future server restarts.