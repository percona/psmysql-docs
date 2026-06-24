
A keyring component loads at server startup from a manifest file. The component reads a JSON configuration file during initialization. Do not load a keyring component with `INSTALL COMPONENT`. InnoDB needs the keyring before the `mysql.component` table is available.

Create a global manifest file named `mysqld.my` in the directory that contains the `mysqld` binary. For multiple instances on one host, create a local manifest file with the same name in each data directory.

To install a keyring component, complete these steps:

1. Write a manifest in valid JSON format

2. Write a configuration file

If the manifest file does not exist, the server does not load the keyring component. During startup, the server reads the global manifest from the installation directory. The global manifest can list the component directly or point to a local manifest in the data directory.
