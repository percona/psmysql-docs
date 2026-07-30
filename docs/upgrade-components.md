# Upgrade from plugins to components 

[Need help navigating plugin to component transitions? Percona Support can assist :octicons-link-external-16:](https://www.percona.com/services/support).

Percona Server for MySQL {{vers}} introduces a shift from plugins to components for several key features, a change that requires a manual transition during the upgrade process. It is generally recommended to transition to the component version of a feature in the 8.0 series before performing the upgrade to {{vers}} if both a plugin and a component are available for that feature.

<!-- Update this doc to be valid for 9.7-->

The following plugins have changed:

| Plugin | 8.0 information | {{vers}} changes | Notes |
|---|---|---|---|
| `keyring_vault` | Only available as a plugin | `component_keyring_vault` | This plugin has been replaced by the `component_keyring_vault` component. The upgrade requires a manual conversion of the plugin's configuration file from the `keyring_vault_config` system variable format to a JSON format. |
| `audit_log` | Only available as a plugin | a deprecated plugin added in 8.4.7-7 | The recommended replacement is `component_audit_log_filter`. |
| `audit_log_filter` | Only available as a plugin | `component_audit_log_filter` | This plugin has a corresponding component. The transition to the component should be performed after the upgrade to {{vers}}. |
| `data_masking` | Available as a plugin and component | `component_masking_functions` | For this feature, it is specifically advised to transition to the `component_masking_functions` in the 8.0 series before upgrading to {{vers}}. |
| `binlog_utils_udf` and `percona-udf` user defined functions | Previously installed via a plugin. Users must install the plugin and then run `CREATE FUNCTION ... SONAME ...` for each function. | `component_binlog_utils_udf` and `component_percona_udf` | These user-defined functions, previously installed via plugins, are now available as components. After running `INSTALL COMPONENT`, all functions are automatically registered, which simplifies the process. |


## Transition a plugin to a component

The operation to transition from a plugin to a component can be complicated. Always test the migration in a staging environment before applying the changes to the production servers. To ensure there is minimal interruption, the key preparation steps are the following:

* Plan for downtime 

* Create a comprehensive testing strategy

* Verify that the existing functionality transfers correctly

Before you start, review the differences between the plugin and the component. The configuration of these features changes: plugins use system variables and the `--early-plugin-load` option, while components rely on a separate configuration file and are loaded using a manifest.

### General procedure

The general procedure for transitioning from a plugin to a component involves:

1. Setup the component's configuration file.

2. Load the component using the manifest (`INSTALL COMPONENT` or manifest file, as applicable).

3. Confirm that the component works. Thoroughly test the component's functionality in your staging environment. Run queries or other operations to verify all existing functionality is correctly transferred.

4. After confirmation, remove the original plugin.

This process should be carefully planned to minimize downtime and ensure that all existing functionality is correctly transferred.

### Transition timing

The timing of the transition depends on the specific plugin:

* **Transition before upgrade**: For plugins that have both plugin and component versions available in 8.0 (for example, `data_masking`), transition to the component in 8.0 before upgrading to {{vers}}.

* **Transition after upgrade**: For plugins that only exist as plugins in 8.0 but have component equivalents in {{vers}} (for example, `audit_log_filter`, `keyring_vault`), you must upgrade to {{vers}} first, then transition to the component. The general procedure for these cases is:

  1. Test the plugin functionality in 8.0 to establish a baseline.

  2. Stop the service and upgrade to {{vers}}.

  3. Review and adjust configurations as needed (for example, convert `keyring_vault_config` system variable to JSON format for the component).

  4. Start the new {{vers}} server.

  5. Transition to the component following the general procedure above.

  6. Verify the component works correctly in {{vers}}.

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade checklist for {{vers}}](./upgrade-checklist-8.4.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Downgrade options](./downgrade.md)
* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)
* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md)
* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)

### Component-specific documentation

* [Install a component](./install-component.md)
* [Uninstall a component](./uninstall-component.md)
* [Use Keyring Vault component](./use-keyring-vault-component.md)
* [Install Data Masking component](./install-data-masking-component.md)
* [Audit Log Filter component overview](./audit-log-filter-overview.md)
* [Migrate to the audit log filter component](./migrate-to-audit-log-filter-component.md)
* [Manage Audit Log Filter](./manage-audit-log-filter.md)