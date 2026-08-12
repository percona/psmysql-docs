# Upgrade from plugins to components

**Topic type**: Task

[Need help with plugin to component transitions? Percona Support can assist :octicons-link-external-16:](https://www.percona.com/services/expert-support/).

Percona Server for MySQL continues to shift several key features from plugins to components. The shift requires a manual transition during the upgrade. If a feature has both a plugin and a component, transition to the component before upgrading to {{vers}}.

For underlying MySQL guidance, see [Installing and Uninstalling Components :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/component-loading.html).

## Plugins moving to components in {{vers}}

The following table lists the affected plugins.

| Plugin | Status before {{vers}} | {{vers}} state | Notes |
|---|---|---|---|
| `keyring_vault` | Available only as a plugin | `component_keyring_vault` | The plugin is replaced by the `component_keyring_vault` component. Convert the configuration from the `keyring_vault_config` system variable format to JavaScript Object Notation (JSON) manually. |
| `audit_log` | Available only as a plugin | A deprecated plugin re-added in 8.4.7-7 | The recommended replacement is `component_audit_log_filter`. |
| `audit_log_filter` | Available only as a plugin | `component_audit_log_filter` | The plugin has a corresponding component. Transition to the component after upgrading to {{vers}}. |
| `data_masking` | Available as both a plugin and a component | `component_masking_functions` | Transition to `component_masking_functions` before upgrading to {{vers}}. |
| `binlog_utils_udf` and `percona-udf` user-defined functions | Installed via a plugin. The plugin install requires `CREATE FUNCTION ... SONAME ...` for each function. | `component_binlog_utils_udf` and `component_percona_udf` | User-defined functions are available as components in {{vers}}. After `INSTALL COMPONENT`, all functions register automatically. |

## How components differ from plugins

The component framework supersedes the legacy plugin model with several practical advantages. Review the following differences before planning a transition.

| Property | Plugins | Components |
|---|---|---|
| Loading statement | `INSTALL PLUGIN <NAME> SONAME '<FILE>.<SUFFIX>'` | `INSTALL COMPONENT 'file://<NAME>'`, or a manifest file for keyring components |
| Library path | Requires the platform-specific filename suffix | The component identifier omits the suffix and works across platforms |
| Registration | The `mysql.plugin` system table | The `mysql.component` system table |
| Configuration | System variables and `--early-plugin-load` | A component-specific configuration file, plus a JSON manifest for keyring components |
| Replication scope | The `INSTALL PLUGIN` statement is not replicated | Component installation is local to one server. Run the install on every server in the topology |
| Loadable functions | Each function requires `CREATE FUNCTION ... SONAME ...` | The component installs related loadable functions automatically |

## Transition a plugin to a component

The transition from a plugin to a component can be complicated. Always test the migration in a staging environment before applying changes to production. To minimize interruption, complete the following key preparation steps:

* Build a comprehensive testing strategy.

* Plan for downtime.

* Verify that existing functionality transfers correctly.

Before starting, review the differences between the plugin and the component. Configuration differs between the two models.

### Identify the loading mechanism

The component determines which of two loading mechanisms applies:

* Most components load at runtime with the `INSTALL COMPONENT` statement. The loader service registers the component in `mysql.component` and reloads the component on subsequent restarts.

* Keyring components require a JSON manifest file named `mysqld.my`. The manifest must be in place before server start. The keyring must initialize before the InnoDB storage engine.

For details on the keyring requirement, see [Keyring Component Installation :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/keyring-component-installation.html).

### Load a runtime-loaded component

The following steps cover components loaded with the `INSTALL COMPONENT` statement.

1. Create the component configuration file. Refer to the component documentation for required keys.

2. Load the component with `INSTALL COMPONENT 'file://<COMPONENT_NAME>'`.

3. Confirm that the component works in your staging environment. Run queries or operations that exercised the prior plugin.

4. After confirmation, remove the original plugin with `UNINSTALL PLUGIN <PLUGIN_NAME>`.

Plan the procedure to minimize downtime. Confirm that prior functionality transfers cleanly to the component.

### Configure the manifest file for keyring components

Keyring components do not load with `INSTALL COMPONENT`. The server reads a manifest file at startup and loads the named component before InnoDB initializes.

!!! important "Restart required"

    Manifest-loaded keyring components register only at server startup. Plan a restart window before deploying the manifest file.

Take the following actions:

* Create a global manifest file at `<INSTALL_DIR>/mysqld.my`. Optionally, redirect the global file to a local file in the data directory.

* Use JSON content that names the component to load. For example:

    ```json
    {
      "components": "file://component_keyring_vault"
    }
    ```

* Restrict file permissions. The `mysqld` user account must have read-only access to the manifest.

* Restart the server. Verify that the component initialized successfully.

For per-instance manifests, set `"read_local_manifest": true` in the global file. Place the `components` entry in the local file under the data directory.

### Verify the component is loaded

Use the following queries to confirm component state after server start:

* For keyring components, query the Performance Schema status table.

    ```sql
    SELECT * FROM performance_schema.keyring_component_status;
    ```

    A `Component_status` value of `Active` indicates a healthy initialization. A value of `Disabled` indicates a configuration problem. Check the server error log, fix the configuration, then run `ALTER INSTANCE RELOAD KEYRING`.

* For runtime-loaded components, query the `mysql.component` system table.

    ```sql
    SELECT component_id, component_group_id, component_urn FROM mysql.component;
    ```

* To confirm the legacy plugin is no longer loaded, run `SHOW PLUGINS` and verify the plugin row is absent.

### Choose the transition timing

The transition timing depends on the plugin. The following sub-sections describe the two paths.

#### Transition before the upgrade

Transition to the component before upgrading to {{vers}} when your release exposes both forms. The `data_masking` plugin and the `component_masking_functions` component fit this case.

#### Transition after the upgrade

Some features exist only as plugins in your existing release. Examples include `audit_log_filter` and `keyring_vault`. Upgrade to {{vers}} first, then transition to the component using the following sequence.

1. Test the plugin functionality to establish a baseline.

2. Stop the service and upgrade to {{vers}}.

3. Review and adjust configurations. For example, convert the `keyring_vault_config` system variable to JSON for the component.

4. Start the {{vers}} server.

5. Apply the loading mechanism for the component (`INSTALL COMPONENT` or a manifest file).

6. Verify the component with the queries in [Verify the component is loaded](#verify-the-component-is-loaded).

## Further reading

The following Percona Server for MySQL pages cover related topics:

* [Downgrade options](./downgrade.md)

* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)

* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)

* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)

* [Upgrade overview](./upgrade.md)

* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)

* [Upgrade strategies](./upgrade-strategies.md)

### Component-specific documentation

The following pages describe specific components:

* [Audit Log Filter component overview](./audit-log-filter-overview.md)

* [Install a component](./install-component.md)

* [Install Data Masking component](./install-data-masking-component.md)

* [Manage Audit Log Filter](./manage-audit-log-filter.md)

* [Uninstall a component](./uninstall-component.md)

* [Use Keyring Vault component](./use-keyring-vault-component.md)
