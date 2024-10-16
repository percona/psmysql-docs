# Compare the data masking component to the data masking plugin

The Data Masking component feature is in [tech preview](glossary.md#tech-preview).

Percona Server for MySQL 8.0.34 introduces a data masking component that operates like a plugin but features a different architecture, enhancing the server’s functionality. Below are the main differences between the component and the plugin:

| Scenario               | Description                                                                                                    |
|------------------------|----------------------------------------------------------------------------------------------------------------|
| Character set support   | The component allows multi-byte character sets for general-purpose masking functions, while the plugin does not.|
| Masking capabilities    | The component can mask PAN, SSN, IBAN, UUID, Canada SIN, and UK NIN. In contrast, the plugin only handles PAN and SSN. |
| Data generation         | The component generates random email, US phone, PAN, SSN, IBAN, UUID, Canada SIN, and UK NIN data, while the plugin generates fewer types: email, US phone, PAN, and SSN. |
| Dictionary storage      | The component stores substitution dictionaries in the database, as opposed to the plugin, which keeps these dictionaries in a file. |
| Privilege management    | The component uses the `MASKING_DICTIONARIES_ADMIN` privilege for dictionary management, while the plugin requires the `FILE` privilege. |
| Function handling       | The component automatically registers or unregisters loadable functions during installation or uninstallation, while the plugin does not offer this automatic process. |

## Additional resources

[Install the data masking component](install-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)