# Uninstall the component

The following steps uninstall the component:

1. Uninstall the component with [`UNINSTALL_COMPONENT`](uninstall-component.md) and the loadable functions.

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_masking_functions';
```

2. Drop `masking_dictionaries`.

```{.bash data-prompt="mysql>"}
mysql> DROP TABLE mysql.masking_dictionaries;
```

## Useful links

[Install the data masking component](install-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)