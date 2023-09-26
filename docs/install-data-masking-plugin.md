# Install and remove the data masking plugin

This feature was implemented in *Percona Server for MySQL* version Percona Server for MySQL 8.0.17-8.

The Percona Data Masking plugin is a free and Open Source implementation of the
*MySQL*’s data masking plugin. Data Masking provides a set of functions to hide
sensitive data with modified content.

## Install the plugin

The following command installs the plugin and the functions:

```{.bash data-prompt="$"}
INSTALL PLUGIN data_masking SONAME 'data_masking.so';
```

## Uninstall the plugin

Use the [UNINSTALL PLUGIN](https://dev.mysql.com/doc/refman/8.0/en/uninstall-plugin.html) statement and the [DROP FUNCTION](https://dev.mysql.com/doc/refman/8.0/en/drop-function.html) statement to disable and uninstall the plugin and then remove the functions. 

```{.bash data-prompt="mysql>"}
UNINSTALL PLUGIN data_masking;
```
