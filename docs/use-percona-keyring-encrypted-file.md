# Use the Percona encrypted keyring file component

The `component_percona_keyring_encrypted_file` component stores encryption keys in a password-protected file on the server filesystem. The component is part of Percona Server for MySQL. After you load the keyring, you use the component for [data at rest encryption](data-at-rest-encryption.md) the same way as other keyring components.

The [Use the keyring file component](use-keyring-file.md) page documents `component_keyring_file`. That component stores keyring data as plaintext JSON on disk. The `component_percona_keyring_encrypted_file` component encrypts the keyring file with a password that you provide.

Percona Server includes a separate component with its own on-disk format. A keyring file from MySQL Enterprise `component_keyring_encrypted_file` does not work with `component_percona_keyring_encrypted_file`.

!!! important

    Load only one keyring at a time. Do not load `component_percona_keyring_encrypted_file` with `component_keyring_file`, legacy keyring plugins, or another keyring component.

    Plan a migration before you switch keyrings if encrypted data already exists on the server. See [Upgrade components](upgrade-components.md) and [Migrate keyring data](#migrate-keyring-data).

See [Get Started with component keyring](quickstart-component-keyring.md) for a walkthrough of the unencrypted file keyring.

## Version changes

Percona Server for MySQL {{vers}} includes `component_percona_keyring_encrypted_file` from release 8.4.11-11

## Choose a file-based keyring component

| Component | Keyring file on disk | Password required | Percona Server |
|-----------|----------------------|-------------------|----------------|
| `component_keyring_file` | Plaintext JSON | No | Yes |
| `component_percona_keyring_encrypted_file` | Encrypted (PBKDF2 + AES) | Yes | Yes |

For key storage outside a local file, see these pages:

* [Use the keyring vault component](use-keyring-vault-component.md)

* [Use AWS KMS](using-amz-kms.md)

* [Use KMIP](using-kmip.md)

## Component installation

--8<--- "keyring-components-installation.md"

## Manifest file

The manifest tells the server to load `component_percona_keyring_encrypted_file` at startup. Create a file named `mysqld.my` in JSON format.

The server reads a global manifest from the directory that contains the `mysqld` binary. The path depends on your install method. Package installs on Linux often use `/usr/sbin/mysqld.my`. Tarball installs, containers, and custom builds may use another directory. Confirm the `mysqld` binary location before you create the manifest. You can place a local manifest in the data directory if multiple instances on one host need different keyring components.

=== "Global manifest only"

    ```json
    {
      "read_local_manifest": false,
      "components": "file://component_percona_keyring_encrypted_file"
    }
    ```

=== "Global and local manifests"

    Global manifest in the directory that contains the `mysqld` binary:

    ```json
    {
      "read_local_manifest": true
    }
    ```

    Local manifest in the data directory:

    ```json
    {
      "components": "file://component_percona_keyring_encrypted_file"
    }
    ```

Restart the server after you create or change a manifest.

## Configuration file

The component reads settings from a JSON configuration file named `component_percona_keyring_encrypted_file.cnf`. The global configuration file is in the plugin directory by default. Confirm the path with the following statement:

```sql
SELECT @@plugin_dir;
```

Typical paths:

* `/usr/lib64/mysql/plugin` on RHEL-style systems

* `/usr/lib/mysql/plugin` on Debian and Ubuntu

You can place a local configuration file in the data directory when you set `read_local_config` in the global file.

The `component_percona_keyring_encrypted_file.cnf` file supports the following options. Option order in the JSON file does not matter. Place `read_local_config` only in the global configuration file in the plugin directory. Place `path`, `read_only`, and `password` or `password_file` in the global file or in the local file in the data directory, depending on `read_local_config`.

* `password`: Password for encryption and decryption of the keyring file. Specify `password` or `password_file`, not both. The password must not be empty.

* `password_file`: Path to a file that contains the password. Specify `password_file` or `password`, not both. Use this option to keep secrets out of the component configuration file. See [File permissions](#file-permissions).

* `path`: Full path to the keyring data file. The component creates this file on first use if the file does not exist. The directory must exist. Use a dedicated directory with restricted permissions. Do not use the data directory. See [File permissions](#file-permissions).

* `read_local_config` [optional]: Use this option only in the global configuration file. The option controls whether the component reads configuration from a local file in the data directory. Allowed values are `true` or `false`. If you omit this option, the component uses only the global configuration file.

    If the global file includes `read_local_config` and other items, the component checks `read_local_config` first:

    * `false`: The component uses the other items in the global file. The component ignores the local configuration file.

    * `true`: The component ignores the other items in the global file. The component reads the local configuration file.

* `read_only`: When `true`, the keyring rejects runtime changes. The keyring does not accept new keys or key removal. When `false`, the keyring accepts key changes. This option is mandatory.

=== "Inline password"

    ```json
    {
      "path": "/var/lib/mysql-keyring/component_percona_keyring_encrypted_file",
      "read_only": false,
      "password": "your-strong-password"
    }
    ```

=== "Password file"

    ```json
    {
      "path": "/var/lib/mysql-keyring/component_percona_keyring_encrypted_file",
      "read_only": false,
      "password_file": "/var/lib/mysql-keyring/keyring.password"
    }
    ```

!!! warning "Protect the keyring file and password"

    You need the encrypted keyring file at `path` and the correct password to access keys. See [File permissions](#file-permissions). Include the keyring file, password, and password file in backup and restore procedures.

    Encrypted tablespaces, redo logs, and undo logs become unrecoverable if the keyring file is lost, corrupted, or opened with the wrong password. Do not delete or edit the keyring file manually to rotate keys. Use [Rotate the master encryption key](rotate-master-key.md) to rotate keys.

## File permissions

The MySQL server user needs read access to the manifest, configuration file, and password file. The user needs read and write access to the keyring directory. Set ownership and permissions before you restart the server.

=== "Manifest"

    ```bash
    sudo chown root:root /usr/sbin/mysqld.my
    sudo chmod 644 /usr/sbin/mysqld.my
    ```

    Adjust the path if your manifest is not in `/usr/sbin`.

=== "Configuration file"

    ```bash
    cd /usr/lib64/mysql/plugin
    sudo chown root:root component_percona_keyring_encrypted_file.cnf
    sudo chmod 640 component_percona_keyring_encrypted_file.cnf
    ```

    Adjust the path for your `@@plugin_dir` value. If you use inline `password`, use mode `640` or tighter on the configuration file.

=== "Keyring directory"

    The component creates the keyring data file at `path` on first use. Place `path` in a directory owned by the MySQL user with mode `750`:

    ```bash
    sudo chown mysql:mysql /var/lib/mysql-keyring
    sudo chmod 750 /var/lib/mysql-keyring
    ```

=== "Password file"

    When you set `password_file`, the MySQL server user must be able to read the file:

    ```bash
    sudo chown mysql:mysql /var/lib/mysql-keyring/keyring.password
    sudo chmod 600 /var/lib/mysql-keyring/keyring.password
    ```

## On-disk format

The keyring payload is JSON. The file on disk is encrypted. Each write uses the following steps:

* PBKDF2-HMAC-SHA256 derives a 256-bit AES key from the password

* The component generates a random salt and initialization vector (IV)

* AES encrypts the JSON payload

The file starts with a version 1 header:

```text
[version:1 byte][salt:32 bytes][iterations:4 bytes, big-endian][iv:16 bytes][ciphertext]
```

The default PBKDF2 iteration count is 600000. During writes, the component can create a `.backup` file next to the keyring data file for rollback.

## Verify the component is loaded

Restart the server. Run the following statement to confirm that the keyring is active:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

If the component loaded successfully, the result includes the following values:

| STATUS_KEY | Expected value |
|------------|----------------|
| Component_name | `component_percona_keyring_encrypted_file` |
| Component_status | `Active` |
| Data_file | The `path` value from the configuration file |
| Read_only | `Yes` or `No`, matching the `read_only` setting |
| Password | `<SET>` with inline `password`; `<NONE>` otherwise |
| Password_file | File path with `password_file`; `<NONE>` otherwise |

Example output:

```text
+---------------------+---------------------------------------------------------------+
| STATUS_KEY          | STATUS_VALUE                                                  |
+---------------------+---------------------------------------------------------------+
| Component_name      | component_percona_keyring_encrypted_file                      |
| Author              | Percona                                                       |
| Component_status    | Active                                                        |
| Data_file           | /var/lib/mysql-keyring/component_percona_keyring_encrypted_file |
| Read_only           | No                                                            |
| Password            | <SET>                                                         |
| Password_file       | <NONE>                                                        |
+---------------------+---------------------------------------------------------------+
```

The `Active` status means the keyring is ready. The `Active` status does not mean data is encrypted. Enable encryption separately for tables, tablespaces, and logs. See [Data at Rest Encryption](data-at-rest-encryption.md).

If startup fails, check the error log with `SELECT @@log_error;`. Common causes:

* Missing or empty password

* Both `password` and `password_file` are set

* The MySQL server user cannot read the password file

* JSON syntax errors in the manifest or configuration file

* Wrong password for an existing keyring file

## Reload the keyring configuration

You can reload the keyring after you change the component configuration file. You do not need a full server restart. Run the following statement:

```sql
ALTER INSTANCE RELOAD KEYRING;
```

Reload succeeds when the updated configuration is valid and the password decrypts the existing keyring file. Reload fails when the password is wrong. After a failed reload, the component can report `Disabled` in `keyring_component_status`.

## Change the keyring password

The password in the `component_percona_keyring_encrypted_file` configuration encrypts the keyring data file. Changing `password` or the contents of `password_file` does not re-encrypt an existing keyring file with the new password.

To change the password, migrate the keys temporarily from `component_percona_keyring_encrypted_file` to the unencrypted `component_keyring_file`, configure `component_percona_keyring_encrypted_file` with the new password, and migrate the keys back to a new encrypted keyring file.

!!! warning

    Stop the MySQL server before you start the migration and keep the server stopped until the migration is complete.

    `component_keyring_file` stores the intermediate keyring data in an unencrypted file. Protect the file from unauthorized access and remove it after you successfully migrate the keys back to `component_percona_keyring_encrypted_file`.

1. Before you stop the server, check the directory where the keyring component libraries are installed:

    ```sql
    SELECT @@plugin_dir;
    ```

    Use this directory as the value of `--component-dir` in the migration commands.

2. Stop the MySQL server:

    ```bash
    sudo systemctl stop mysql
    ```

3. Configure `component_keyring_file` as the temporary destination for the first migration.

    The `mysql_migrate_keyring` utility must be able to load the configuration for both the source and destination keyring components.

    If the component uses a local configuration file, set `"read_local_config": true` in its global configuration file and place the local configuration file in the directory that you specify with `--source-keyring-configuration-dir` or `--destination-keyring-configuration-dir`.

    Configure `component_keyring_file` to use a temporary keyring data file that does not already exist. For example:

    ```json
    {
      "path": "/var/lib/mysql-keyring/keyring_file_plain",
      "read_only": false
    }
    ```

4. Migrate the keys from `component_percona_keyring_encrypted_file` to `component_keyring_file`:

    ```bash
    mysql_migrate_keyring \
      --component-dir=<component_directory> \
      --source-keyring=component_percona_keyring_encrypted_file \
      --source-keyring-configuration-dir=<encrypted_keyring_configuration_directory> \
      --destination-keyring=component_keyring_file \
      --destination-keyring-configuration-dir=<keyring_file_configuration_directory>
    ```

    Replace:

    * `<component_directory>` with the directory that contains the keyring component libraries.
    * `<encrypted_keyring_configuration_directory>` with the directory that contains the local configuration for `component_percona_keyring_encrypted_file`.
    * `<keyring_file_configuration_directory>` with the directory that contains the local configuration for `component_keyring_file`.

    Verify that the migration completes successfully before you continue.

5. Update the `component_percona_keyring_encrypted_file` configuration with the new password.

    If you configure the password directly, replace the existing `password` value:

    ```json
    {
      "path": "/var/lib/mysql-keyring/component_percona_keyring_encrypted_file",
      "read_only": false,
      "password": "new-strong-password"
    }
    ```

    If you use `password_file`, replace the password stored in the file specified by `password_file`.

    Keep the existing `path` value unless you also intend to change the location of the encrypted keyring data file.

6. Move the existing encrypted keyring data file to a secure backup location.

    The `path` configured for `component_percona_keyring_encrypted_file` must not contain the old encrypted keyring file when you migrate the keys back. The second migration creates a new encrypted keyring file at this location.

    For example:

    ```bash
    sudo mv \
      /var/lib/mysql-keyring/component_percona_keyring_encrypted_file \
      /secure/backup/location/component_percona_keyring_encrypted_file.old
    ```

    !!! important

        Verify that the migration to `component_keyring_file` completed successfully before you move the existing encrypted keyring file.

        Keep the original encrypted keyring file and the old password until you verify that the migration with the new password succeeded and that the server can access the encrypted data.

7. Migrate the keys from the temporary `component_keyring_file` back to `component_percona_keyring_encrypted_file`:

    ```bash
    mysql_migrate_keyring \
      --verbose \
      --component-dir=<component_directory> \
      --source-keyring=component_keyring_file \
      --source-keyring-configuration-dir=<keyring_file_configuration_directory> \
      --destination-keyring=component_percona_keyring_encrypted_file \
      --destination-keyring-configuration-dir=<encrypted_keyring_configuration_directory>
    ```

    The migration reads the keys from the temporary unencrypted keyring and creates a new encrypted keyring data file at the `path` configured for `component_percona_keyring_encrypted_file`. The component uses the new `password` or `password_file` value to encrypt the file.

8. Remove the temporary unencrypted keyring data file after the migration completes successfully:

    ```bash
    sudo rm /var/lib/mysql-keyring/keyring_file_plain
    ```

9. Start the MySQL server:

    ```bash
    sudo systemctl start mysql
    ```

10. Verify that `component_percona_keyring_encrypted_file` is active:

    ```sql
    SELECT STATUS_KEY, STATUS_VALUE
    FROM performance_schema.keyring_component_status
    WHERE STATUS_KEY IN ('Component_name', 'Component_status');
    ```

    Verify that `Component_name` is `component_percona_keyring_encrypted_file` and `Component_status` is `Active`.

    Verify that encrypted tables and other encrypted data that use keys from the keyring remain accessible.

After you verify the new encrypted keyring and encrypted data, securely remove the backup of the old encrypted keyring file when you no longer need it.

## Use the keyring with encryption

You can enable transparent data encryption (TDE) when `component_percona_keyring_encrypted_file` is active. TDE applies to the following objects:

* Individual tables and schema defaults: [Encrypt file-per-table tablespace](encrypt-file-per-table-tablespace.md) and [Encrypt schema or general tablespace](encrypt-tablespaces.md)

* System tablespace: [Encrypt system tablespace](encrypt-system-tablespace.md)

* Redo and undo logs: [Log encryption](encrypt-logs.md)

* Binary and relay logs: [Encrypt binary log files and relay log files](encrypt-binary-relay-log-files.md)

See [Verify encryption](verify-encryption.md) to confirm encryption settings.

## Migrate keyring data

The `mysql_migrate_keyring` utility copies keys between `component_percona_keyring_encrypted_file` and `component_keyring_file`. Both components need valid configuration files in the configuration directory that you pass to the utility. See [Use the keyring file component](use-keyring-file.md) for `component_keyring_file` details.

Follow these steps:

1. Stop the server.

2. Create configuration files for the source and destination keyring components.

3. Run `mysql_migrate_keyring`.

4. Update the manifest to load the destination component.

5. Start the server.

6. Verify keys and encrypted data.

The following example migrates from the encrypted Percona keyring to the unencrypted file keyring:

```bash
mysql_migrate_keyring \
  --component-dir=/usr/lib64/mysql/plugin \
  --source-keyring=component_percona_keyring_encrypted_file \
  --source-keyring-configuration-dir=/var/lib/mysql \
  --destination-keyring=component_keyring_file \
  --destination-keyring-configuration-dir=/var/lib/mysql
```

To migrate in the other direction, swap the `--source-keyring` and `--destination-keyring` values. The destination encrypted keyring configuration must include `path`, `read_only`, and `password` or `password_file`. Keep the server stopped during migration. Update `mysqld.my` to reference the destination component before you restart.

## Operational notes

These notes apply after you load the component and use it for data at rest encryption. They cover backups, instance moves, clusters, key rotation, and compliance.

* Backups: Include the encrypted keyring file, password, and encrypted data in the same backup plan. Restore fails for encrypted tablespaces or logs without the keyring file and password.

* Cloning and migration: Copy the keyring file when you move an instance to new hardware. Use the same password in the component configuration on the new host before you start the server.

* Percona XtraDB Cluster (PXC): The keyring file is not replicated. Copy the keyring file from the bootstrap node to other nodes. Each node must use the same password in the component configuration.

* Master key rotation: Run `ALTER INSTANCE ROTATE INNODB MASTER KEY` to rotate the InnoDB master key. See [Rotate the master encryption key](rotate-master-key.md).

* Compliance: A password-protected local keyring file protects keys at rest on the host. A local keyring file is not a substitute for a dedicated key management system or a hardware security module (HSM) when regulations require one.

## Uninstall the component

Follow these steps to stop use of the encrypted file keyring:

1. Remove or rename the manifest entry for `file://component_percona_keyring_encrypted_file` in `mysqld.my`.

2. Remove or rename `component_percona_keyring_encrypted_file.cnf`.

3. Restart the server.

Do not delete the keyring data file if encrypted data exists on the instance. You need the keyring data file and the correct password to decrypt encrypted tablespaces and logs.

!!! admonition "See also"

    [Keyring components overview](keyring-components-plugins-overview.md)

    [Use the keyring file component](use-keyring-file.md)

    [Get Started with component keyring](quickstart-component-keyring.md)

    [Data at Rest Encryption](data-at-rest-encryption.md)

    [Upgrade components](upgrade-components.md)

    [Rotate the master encryption key](rotate-master-key.md)
