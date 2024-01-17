# Upgrade keyring_vault or keyring_plugin


## Upgrade from Vault Secrets Engine Version 1 to Version 2

You can upgrade from the Vault Secrets Engine Version 1 to Version 2.
Use either of the following methods:

=== "secret_mount_point_version = AUTO"

    Set the `secret_mount_point_version` to `AUTO` or the variable is not set in the `keyring_vault` plugin configuration files in all Percona Servers. The `AUTO` value ensures that the autodetection mechanism is invoked during the plugin's initialization.

=== "secret_mount_point_version = 2"

    Set the `secret_mount_point_version` to `2` to ensure that plugins do not initialize unless the `kv` to `kv-v2` upgrade completes.

The `keyring_vault` plugin that works with `kv-v2` secret engines does not use the built-in key versioning capabilities. The keyring key versions are encoded into key names.


## Upgrade from 8.0.22-13 or earlier to 8.0.23-14 or later

The `keyring_vault` plugin configuration files created before
Percona Server for MySQL 8.0.23-14 work only with `KV Secrets Engine -
Version 1 (kv)` and do not have the `secret_mount_point_version`
parameter. After the upgrade to 8.0.23-14 or later, the `secret_mount_point_version` is implicitly considered `AUTO`, the information is probed, and the secrets engine version is determined to `1`.

## Upgrade from 5.7 to 8.0 based on the KV Secrets Engine version

=== "Upgrade from 5.7.32 or older"

    When you upgrade from Percona Server for MySQL 5.7.32 or older, you can only use
    `KV Secrets Engine 1 (kv)`. You can upgrade to any version of
    Percona Server for MySQL 8.0. The old `keyring_vault`` plugin and new
    `keyring_vault` plugin work correctly with the existing Vault Server
    data under the existing `keyring_vault` plugin configuration file.

=== "Upgrade 5.7.33 or newer"

    You have the following options when upgrading from Percona Server for MySQL 5.7.33 or newer.
    If you use `KV Secrets Engine 1 (kv)`, you can upgrade to any version of Percona Server for MySQL 8.0.
    If you use `KV Secrets` Engine 2 (kv-v2)` you can upgrade to Percona Server for MySQL 8.0.23 or newer. This version is the first with a `keyring_vault` plugin that supports `kv-v2`.