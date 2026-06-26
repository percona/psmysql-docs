!!! warning "Back up the keyring file: data recovery depends on it"

    Do not delete the keyring file (for example, `/var/lib/mysql-keyring/component_keyring_file`) to "clean up" or for any other reason. If that file is lost or deleted, all data encrypted with it is **unrecoverable**. There is no way to decrypt tablespaces, redo logs, or undo logs without the keyring.

    **Life cycle:** Back up the keyring file and its directory as part of your normal backup strategy. Include the keyring in your restore procedures so that after a restore you can start MySQL with the same keys and access your encrypted data. If you move or clone the server, copy the keyring file to the new location before starting the server.

* Treat the keyring file as a secret: restrict access and include it in your secure backup strategy.

* Back up the keyring file and its directory. If the keyring is lost or damaged (for example, after a migration or permission change), you cannot decrypt data that was encrypted with the keyring. Recovery is not possible.

* If the keyring is lost and you have encrypted data, recovery is not possible.
