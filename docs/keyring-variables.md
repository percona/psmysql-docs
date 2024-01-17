# Keyring system variables

### `keyring_vault_config`

| Option       | Description            |
|--------------|------------------------|
| Command-line | --keyring-vault-config |
| Scope        | Global                 |
| Dynamic      | Yes                    |
| Data type    | Text                   |
| Default      |

This variable defines the location of the keyring_vault_plugin
configuration file.

### `keyring_vault_timeout`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --keyring-vault-timeout |
| Scope        | Global                  |
| Dynamic      | Yes                     |
| Data type    | Numeric                 |
| Default      | 15                      |

Set the duration in seconds for the Vault server connection timeout. The
default value is `15`. The allowed range is from `0` to `86400`. The
timeout can also be disabled to wait an infinite amount of time by setting
this variable to `0`.