# Compare keyring components and keyring plugins

If you want to store encryption keys in Percona Server for MySQL securely, you have two options: keyring components and plugins. They are similar in functionality, but they have some differences that you should consider before choosing.

Keyring components are newer and more flexible than keyring plugins. You can load them using a manifest file, so you don't need the `--early-plugin-load` option. You can also configure the keyring components using their configuration files instead of system variables. Keyring components have fewer restrictions on the types and lengths of keys they can handle. For example, keyring components can support RSA keys, while keyring plugins cannot.

However, keyring components also have some disadvantages. They are incompatible with features that rely on keyring plugins, such as InnoDB encryption threads or binary log encryption. They also require more steps to install and uninstall than keyring plugins. You must create and edit each component's manifest file, configuration file, and component directory.

Keyring plugins are older than keyring components. You can load them using the `--early-plugin-load` option, which is more straightforward than a manifest file. You can also configure them using system variables, which are easier to manage than configuration files. Keyring plugins are compatible with certain features that use encryption keys.

However, keyring plugins also have some limitations. They have more restrictions on the types and lengths of keys they can support. For example, they cannot handle RSA keys, while keyring components can. They also require you to specify the plugin name and library file for each plugin you load.

To summarize, keyring components and plugins are ways to store encryption keys in Percona Server for MySQL, but they have different advantages and disadvantages. You should choose the one that suits your needs and preferences.
