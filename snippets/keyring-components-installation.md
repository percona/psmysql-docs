
The component must be installed with a manifest. A keyring component is not loaded with the `--early-plugin-load` option on the server. The server uses a manifest and the component consults its configuration file during initialization. You should only load a keyring component with a manifest file. Do not use the `INSTALL_COMPONENT` statement, which loads the keyring components too late in the startup sequence of the server. For example, `InnoDB` requires the component, but because the components are registered in the `mysql.component` table, this table is loaded after `InnoDB` initialization.

You should create a global manifest file named `mysqld.my` in the installation directory and, optionally, create a local manifest file, also named `mysqld.my` in a data directory.

To install a keyring component, do the following:

1. Write a manifest in a valid JSON format

2. Write a configuration file

A manifest file indicates which component to load. If the manifest file does not exist, the server does not load the component associated with that file. During startup, the server reads the global manifest file from the installation directory. The global manifest file can contain the required information or point to a local manifest file located in the data directory. If you have multiple server instances that use different keyring components use a local manifest file in each data directory to load the correct keyring component for that instance.

!!! warning

    Enable only one keyring plugin or one keyring component at a time for each server instance. Enabling multiple keyring plugins or keyring components or mixing keyring plugins or keyring components is not supported and may result in data loss.