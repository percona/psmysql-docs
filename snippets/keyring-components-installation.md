
Install a keyring component through a manifest file. During startup, the server reads the manifest. Each component reads a corresponding configuration file during initialization.

Do not load keyring components with either of the following methods:

| Method | Why it fails |
|---|---|
| `--early-plugin-load` option | Loads plugins only, not components |
| `INSTALL COMPONENT` statement | Registers components in the `mysql.component` table, which the server loads after `InnoDB` initialization |

Components that `InnoDB` requires at startup must load earlier.

Create a global manifest file named `mysqld.my` in the installation directory. Optionally, create a local manifest file with the same name in a data directory.

To install a keyring component, complete the following steps:

1. Write a manifest in valid JSON format

2. Write a configuration file

A manifest file declares which component to load. The server skips any component whose manifest file does not exist. During startup, the server reads the global manifest file from the installation directory. The global manifest file either contains the required information or references a local manifest file in the data directory.

Use a local manifest file in each data directory when you run multiple server instances with different keyring components. Each instance then loads the correct keyring component.

!!! warning

    Enable only one keyring plugin or keyring component per server instance. Percona Server does not support multiple or mixed keyring implementations. Unsupported configurations can cause data loss.
