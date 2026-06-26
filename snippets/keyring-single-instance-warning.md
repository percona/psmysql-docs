!!! warning

    Enable only one keyring component at a time for each server instance. Enabling multiple keyring components is not supported and may result in data loss.

!!! warning

    Enable only one keyring plugin or one keyring component at a time for each server instance. Enabling multiple keyring plugins or keyring components or mixing keyring plugins or keyring components is not supported and may result in data loss.

!!! important

    Enable only one keyring at a time. Do not use legacy keyring plugins (such as `keyring_file` or `keyring_vault`) together with the component keyring.

    If you are upgrading from 8.0 or another release and already have data encrypted with a legacy keyring plugin, do not enable the component keyring without a migration plan. Data encrypted with the old plugin will not be readable by the new component; existing encrypted tables can become unreadable.

    See [Upgrade components](upgrade-components.md) and your upgrade documentation before switching. For migrating keys from a legacy keyring to the component keyring, check MySQL and Percona documentation for your version (for example, the mysql_migrate_keyring utility where applicable).
