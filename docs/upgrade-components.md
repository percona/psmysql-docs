# Upgrading from plugins to components 

[Need help navigating plugin to component transitions? Percona Support can assist].(https://www.percona.com/services/support)

The following plugins have changed:

| Plugin | 8.0 information | {{vers}} changes | Notes |
|---|---|---|---|
| `keyring_vault` | Only available as a plugin | `component_keyring_vault` | A manual upgrade path is required. For example, the plugin configuration file, specified by the `keyring_vault_config` system variable, must be transformed to a JSON format for the `component_keyring_vault.cnf`. |
| `audit_log` | Only available as a plugin | removed | Recommended that you use the `component_audit_log_filter`. |
| `audit_log_filter` | Only available as a plugin | `component_audit_log_filter` | Transition the plugin to the component after the upgrade to {{vers}}. |
| `data_masking` | Available as a plugin and component | `component_masking_functions` | Transition the plugin to the component in 8.0 before the upgrade to {{vers}} |
| `binlog_utils_udf` user defined functions | Only available as plugin. Users must install the plugin and then run `CREATE FUNCTION ... SONAME...` | `component_binlog_utils_udf` | Run `INSTALL COMPONENT` and all functions are registered automatically. |
| `percona-udf` user defined functions | Must create individual functions with `CREATE FUNCTION ... SONAME ...`. | `component_percona_udf` | Run `INSTALL COMPONENT` and all functions are registered automatically. Can still use `CREATE FUNCTION ... SONAME ...` if needed. |

We recommend if you use a plugin and the feature also available a component, switch to the component in 8.0 series before upgrading to {{vers}}.

## Transition a plugin to a component

The operation to transition from a plugin to a component can be complicated. Always test the migration in a staging environment before applying the changes to the production servers. To ensure there is minimal interruption, the key preparation steps are the following:

* Plan for downtime 

* Create a comprehensive testing strategy

* Verify that the existing functionality transfers correctly

Before you start, review the differences between the plugin and the component. A plugin configuration has plugin-specific system variables and uses the `--early-plugin-load` option. A component has a configuration file and loads using a manifest.

1. Setup the component's configuration file.

2. Load the component using the manifest.

3. Confirm that the component works. Run queries or other operations and test the component thoroughtly in your test environment.

4. After confirmation, remove the original plugin.

Some plugins may require more configuration and setup during the transition to a component. For those plugins, you may have the following scenario:

1. Test the plugin in 8.0.

2. Stop the service

3. Upgrade to {{vers}}

4. Review and adjust the configurations, as needed

5. Start the new {{vers}}

6. Confirm the component in {{vers}}