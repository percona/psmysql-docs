# Get Started with component keyring

Enable the component keyring (`component_keyring_file`) in Percona Server {{vers}} for encryption at rest. In MySQL 8.4 and later, the supported path is the component keyring, not legacy keyring plugins.

!!! important

    Enable only one keyring at a time. Do not use legacy keyring plugins (such as `keyring_file` or `keyring_vault`) together with the component keyring.

    If you are upgrading from 8.0 or another release and already have data encrypted with a legacy keyring plugin, do not enable the component keyring without a migration plan. Data encrypted with the old plugin will not be readable by the new component; existing encrypted tables can become unreadable.

    See [Upgrade components](upgrade-components.md) and your upgrade documentation before switching. For migrating keys from a legacy keyring to the component keyring, check MySQL and Percona documentation for your version (for example, the mysql_migrate_keyring utility where applicable).

This guide is based on [Configuring the Component Keyring in Percona Server and PXC 8.4](https://percona.community/blog/2026/01/13/configuring-the-component-keyring-in-percona-server-and-pxc-8.4/) (Percona Community).

Scope: This quickstart assumes a typical package install and standard paths. Minimal images, custom builds, tarball installs, or locked-down environments may need different paths and steps. Confirm your binary location, plugin directory, and manifest path before following the steps below.

## Prerequisites

* Percona Server for MySQL {{vers}} installed
* `sudo` or root access to the server filesystem (to create the keyring directory, manifest, and component config)
* Service name may be `mysql` or `mysqld` depending on your system
* For the encryption examples (tables, system tablespace, redo/undo), the MySQL user you connect as must have the required privileges (for example, `CREATE TABLESPACE` for system tablespace). OS-level sudo does not grant MySQL privileges.

This guide assumes you have OS-level access to install and configure the keyring. In managed or hosted environments where you have only SQL privileges and no filesystem access, your provider must configure the keyring or offer an alternative. This quickstart does not cover managed or hosted environments with only SQL access.

## Step 1: Register the component (manifest)

The manifest file (`mysqld.my`) tells MySQL which component to load. The component's own configuration file (Step 3) configures how it behaves: where to store keys and whether the keyring is read-only.

MySQL loads components from a JSON manifest. A single typo, trailing comma, or missing quote can prevent the server from starting.

Before restarting, you can validate JSON syntax locally with `jq . /usr/sbin/mysqld.my` (if `jq` is installed). When the JSON is valid, `jq .` prints the file contents back; invalid JSON produces an error.

Note: jq only checks syntax. It does not verify that the component library exists in the plugin directory or that the server will load it. A successful jq run does not guarantee the server will start with the keyring. Do not paste configuration that contains paths or other sensitive details into third-party websites.
{.power-number}

1. Confirm where your server expects the manifest. The server reads the manifest from a location tied to the `mysqld` binary (often the same directory as the binary). Check the path of the running binary (for example, inspect your systemd unit file or run `readlink -f /proc/$(pgrep -f mysqld)/exe` on Linux).

    If you installed from a tarball or a non-standard repo, the path may not be `/usr/sbin`. Create the manifest in the location you confirmed. If the manifest is in the wrong place, the server ignores it and starts without the keyring; encryption (for example, `CREATE TABLE ... ENCRYPTION='Y'`) will then fail with no clear error.

    A common path is `/usr/sbin/mysqld.my`. Custom builds or container images may use `/usr/bin`, `/usr/local/sbin`, or another directory. Some packages or security modules (for example, AppArmor or SELinux) may block writing under `/usr/sbin`. Create the manifest file at the path you confirmed:

    ```bash
    sudo vi /usr/sbin/mysqld.my
    ```

2. Add the following JSON (check spelling and quotes):

    ```json
    {
      "components": "file://component_keyring_file"
    }
    ```

3. Set ownership and permissions:

    ```bash
    sudo chown root:root /usr/sbin/mysqld.my
    sudo chmod 644 /usr/sbin/mysqld.my
    ```

## Step 2: Create the keyring directory

The keyring directory holds encryption keys. Restrict access.

```bash
sudo mkdir -p /var/lib/mysql-keyring
sudo chown mysql:mysql /var/lib/mysql-keyring
sudo chmod 750 /var/lib/mysql-keyring
```

Rule of thumb: mysql owns the directory; only MySQL (and root for administration) should access it.

If you use a custom Linux user, a Docker volume, or a non-standard install, ensure the keyring directory is owned by the user that runs MySQL and that the MySQL process has read access to the manifest and component config files. "Permission denied" on startup usually means ownership or permissions on the manifest and component config paths.

In hardened environments (for example, security-hardened AMIs), extended attributes (ACLs) or immutable flags (for example, `chattr +i`) may also block access. If `chmod`/`chown` succeed but MySQL still cannot access the file or directory, check with `getfacl` or `lsattr` and adjust or remove restrictions as your security policy allows.

In orchestrated or container environments (for example, Kubernetes, OpenShift), file ownership and permissions are often managed by the platform (for example, Security Context Constraints or admission controllers). Manual `chown`/`chmod` may fail or be overwritten when the pod restarts. Check your platform documentation for how to set permissions or run as the correct user.

!!! warning "Back up the keyring file: data recovery depends on it"

    Do not delete the keyring file (for example, `/var/lib/mysql-keyring/component_keyring_file`) to "clean up" or for any other reason. If that file is lost or deleted, all data encrypted with it is **unrecoverable**. There is no way to decrypt tablespaces, redo logs, or undo logs without the keyring.

    **Life cycle:** Back up the keyring file and its directory as part of your normal backup strategy. Include the keyring in your restore procedures so that after a restore you can start MySQL with the same keys and access your encrypted data. If you move or clone the server, copy the keyring file to the new location before starting the server.

## Step 3: Configure the keyring component

Verify the component library exists before pointing the manifest at it. In a MySQL session (if the server is already running), run `SELECT @@plugin_dir;`. Then list that directory and confirm the `component_keyring_file` library (or the file name your distribution uses) is present. On Linux you can run `ls -la "$(mysql -N -e 'SELECT @@plugin_dir;')"` and look for a file related to `component_keyring_file`.

Minimal or slim container images may omit the library. Install the package that provides the keyring component or use a full image.

Create the component configuration file in the MySQL plugin directory. Use the path returned by `@@plugin_dir` (typical paths: `/usr/lib64/mysql/plugin` on RHEL-style, `/usr/lib/mysql/plugin` on Debian/Ubuntu).
{.power-number}

1. Go to the plugin directory (use the path from `@@plugin_dir` or adjust for your distribution):

    ```bash
    cd /usr/lib64/mysql/plugin
    ```

2. Create the config file:

    ```bash
    sudo vi component_keyring_file.cnf
    ```

3. Add (adjust `path` if you used a different keyring directory):

    ```json
    {
      "path": "/var/lib/mysql-keyring/component_keyring_file",
      "read_only": false
    }
    ```

    Use `"read_only": true` if you want to prevent runtime changes to the keyring. You can validate the component config file with `jq . component_keyring_file.cnf` before restarting.

4. Set ownership and permissions:

    ```bash
    sudo chown root:root component_keyring_file.cnf
    sudo chmod 640 component_keyring_file.cnf
    ```

## Step 4: Restart MySQL

Loading the component from the manifest requires a server restart. On a typical system:

```bash
sudo systemctl restart mysql
```

Or `sudo systemctl restart mysqld`, depending on your system.

In orchestrated or managed environments (for example, Kubernetes or some cloud DB services), restart may be controlled by a scheduler or not allowed mid-workflow. Plan the keyring setup during a maintenance window or coordinate with your provider. There is no supported way to load the keyring component at runtime without a restart when using the file-based manifest.

If the server does not start, check the error log. To see where it is written, run `SELECT @@log_error;` in a previous MySQL session, or look in common locations such as `/var/log/mysql/error.log` or the server datadir. JSON syntax errors in the manifest or component config (trailing commas, missing quotes, wrong brackets) are reported there. Fix the JSON and restart again.

## Step 5: Verify the keyring is loaded

In a MySQL session:

```sql
SELECT * FROM performance_schema.keyring_component_status;
```

You should see `component_keyring_file` with `Component_status` = Active and the correct `Data_file` path.

Example:

```text
+---------------------+-----------------------------------------------+
| STATUS_KEY          | STATUS_VALUE                                  |
+---------------------+-----------------------------------------------+
| Component_name      | component_keyring_file                        |
| Component_status    | Active                                        |
| Data_file           | /var/lib/mysql-keyring/component_keyring_file |
| Read_only           | No                                            |
+---------------------+-----------------------------------------------+
```

Seeing "Active" here means only that the keyring component is loaded and ready. Your data is not encrypted until you enable encryption for tables, tablespaces, or logs in the next section.

Treat Step 5 as "keyring ready". Actual protection comes from applying encryption in the Data at rest encryption section below.

## Data at rest encryption

With the keyring loaded, the server can encrypt data on disk (transparent data encryption, or TDE). Keys are stored in the keyring; you enable encryption per tablespace or for redo/undo logs.

**Performance:** Enabling system-wide encryption (redo logs, undo logs, and the system tablespace) consumes extra CPU cycles and I/O. Encryption has a measurable cost: throughput can drop and latency can increase. The impact depends on workload. Consider enabling encryption where it matters for compliance or risk, and measure performance under your load before and after.

### Tables and schemas

Create a new table with encryption:

```sql
CREATE TABLE myapp.sensitive_data (
  id INT PRIMARY KEY,
  payload VARCHAR(255)
) ENCRYPTION='Y';
```

Encrypt an existing table:

```sql
ALTER TABLE myapp.existing_table ENCRYPTION='Y';
```

Set default encryption for a schema so new tables are encrypted by default:

```sql
ALTER SCHEMA myapp DEFAULT ENCRYPTION='Y';
```

### System tablespace

Encrypt the system tablespace (data dictionary, `mysql` system tablespace):

```sql
ALTER TABLESPACE mysql ENCRYPTION='Y';
```

Requires the `CREATE TABLESPACE` privilege on the MySQL user you use (having OS sudo does not grant MySQL privileges).

Encrypting the system tablespace can be a long-running, high-I/O operation. On a large instance it may take minutes or hours and can increase load or cause blocking. Do not assume it is safe to run on a heavily loaded production system without a maintenance window. Plan for a maintenance window and expect significant I/O. See [Encrypt system tablespace](encrypt-system-tablespace.md).

### Redo and undo logs

Enable encryption for redo and undo log files so recovery and rollback data are encrypted on disk.

All `SET GLOBAL` settings are temporary and are lost at restart. For redo/undo log encryption, use the config file as the primary method. Do not enable it only with `SET GLOBAL` or your protection will vanish after the next reboot (for example, after a kernel update or crash).

Add these options to your MySQL config file (for example, `my.cnf`) so they persist:

```ini
innodb_redo_log_encrypt = ON
innodb_undo_log_encrypt = ON
```

Restart the server (or add the options and plan a restart). If these settings are only set with `SET GLOBAL` and not in the config file, the server will stop encrypting new redo/undo pages after a restart with no clear indication.

New log pages are encrypted when written; existing pages are unchanged until they are rewritten. See [Log encryption](encrypt-logs.md).

### Verify encryption

The following checks report metadata and schema settings only. They do not prove that data on disk is actually encrypted or that the keyring has served a key for that tablespace.

InnoDB encrypts data when the option is set. These queries only confirm that the option is set (the "label"), not that the "lock" is engaged on disk.

Tables: List tables that have the encryption option set. Such tables show `ENCRYPTION="Y"` in `CREATE_OPTIONS`:

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS
FROM INFORMATION_SCHEMA.TABLES
WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';
```

Tablespaces: Check whether a tablespace has the encryption flag set in `INNODB_TABLESPACES`. Bit 13 (value 8192) is set when the tablespace is marked encrypted:

```sql
SELECT name, (flag & 8192) != 0 AS encrypted
FROM INFORMATION_SCHEMA.INNODB_TABLESPACES;
```

Schemas: List schemas that have default encryption (new tables in schemas with default encryption are encrypted by default):

```sql
SELECT SCHEMA_NAME, DEFAULT_ENCRYPTION
FROM INFORMATION_SCHEMA.SCHEMATA
WHERE DEFAULT_ENCRYPTION = 'YES';
```

Redo and undo logs: Confirm whether redo and undo log encryption is enabled:

```sql
SHOW GLOBAL VARIABLES LIKE 'innodb_redo_log_encrypt';
SHOW GLOBAL VARIABLES LIKE 'innodb_undo_log_encrypt';
```

For more (binary logs, doublewrite, temporary files, and INNODB_TABLESPACES_ENCRYPTION), see [Verify encryption](verify-encryption.md).

## Clean up

If you ran the examples above and want to return the instance to its previous state, run the following. Skip any step that does not apply (for example, if you did not create `myapp` or encrypt the system tablespace).

Disable redo and undo log encryption. If you added them to `my.cnf`, remove or comment out those lines and restart; otherwise they will turn back on at next restart.

To turn off only for the current run:

```sql
SET GLOBAL innodb_redo_log_encrypt = OFF;
SET GLOBAL innodb_undo_log_encrypt = OFF;
```

Revert system tablespace encryption (only if you ran `ALTER TABLESPACE mysql ENCRYPTION='Y'`):

```sql
ALTER TABLESPACE mysql ENCRYPTION='N';
```

Remove the example schema default and tables. If you created the `myapp` schema or the example tables used in this guide:

```sql
ALTER SCHEMA myapp DEFAULT ENCRYPTION='N';
DROP TABLE IF EXISTS myapp.sensitive_data;
```

If you encrypted a different existing table, revert it with `ALTER TABLE schema_name.table_name ENCRYPTION='N';`.

The keyring remains loaded and the keyring files on disk are unchanged. To remove the keyring entirely, delete the component from `mysqld.my`, remove or rename `component_keyring_file.cnf`, and restart MySQL.

## Next steps

* Use [data at rest encryption](data-at-rest-encryption.md) (for example, encrypt tablespaces, redo/undo logs) with the keyring in place.
* [Verify encryption](verify-encryption.md) for your tablespaces and logs.
* For Percona XtraDB Cluster (PXC): keyring file is not replicated; copy the keyring file from the bootstrap node to other nodes before starting them.

## Operational notes

* Treat the keyring file as a secret: restrict access and include it in your secure backup strategy.
* Back up the keyring file and its directory. If the keyring is lost or damaged (for example, after a migration or permission change), you cannot decrypt data that was encrypted with the keyring. Recovery is not possible. Duplicate or back up the keyring before major changes to the server or filesystem.
* If the keyring is lost and you have encrypted data, recovery is not possible.
* To change the master key (for example, for rotation or compliance), use `ALTER INSTANCE ROTATE INNODB MASTER KEY`; see [Rotate the master encryption key](rotate-master-key.md). Do not delete or replace the keyring file manually to "reset" or rotate. You will lose access to all data encrypted with it.
* For MySQL 8.4 and later, components are the supported keyring model; avoid mixing with legacy keyring plugins.
