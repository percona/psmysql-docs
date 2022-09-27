# Data at Rest Encryption

*Percona Server for MySQL*  enables data at rest encryption of the InnoDB (file-per-table) tablespace by encrypting the physical database files. The data is automatically encrypted prior to writing to storage and automatically decrypted when read.
If unauthorized users access the data files, they cannot read the contents. Percona Server for MySQL 5.7 data at rest encryption is similar to the [MySQL 5.7 data-at-rest encryption](https://dev.mysql.com/doc/refman/5.7/en/innodb-data-encryption.html). Percona Server for MySQL 8.0 provides more encryption features and options which are not available in this version.

The following table lists the various features that are considered Generally Available (GA) or in **tech preview**. The **tech preview** features and variables are not recommended to be used in production. Features and variables marked as **deprecated** perform no action.

| Feature                                | Status                         | GA Version               | Tech Preview Version               | Deprecated Version |
|----------------------------------------|--------------------------------|--------------------------|------------------------------------|--------------------|
| Vault Keyring Plugin                   | Generally Available, supported | Percona Server 5.7.21-21 |
| Encrypting a File-Per-Table Tablespace | Generally Available, supported | Percona Server 5.7.21-21 |
| Encrypting a General Tablespace        | Generally Available, supported | Percona Server 5.7.21-21 |
| Temporary file encryption              | Generally Available, supported | Percona Server 5.7.22-22 |
| binlog_encrypt                         | Generally Available, supported | Percona Server 5.7.21-21 |
| InnoDB System Tablespace Encryption    | Deprecated                     | Percona Server 5.7.23-24 | Percona Server for MySQL 5.7.32-35 |
| Doublewrite buffer                     | Deprecated                     | Percona Server 5.7.23-24 | Percona Server for MySQL 5.7.32-35 |
| InnoDB Undo Tablespace Encryption      | Deprecated                     | Percona Server 5.7.23-24 | Percona Server for MySQL 5.7.32-35 |
| Redo Log Encryption                    | Deprecated                     | Percona Server 5.7.23-24 | Percona Server for MySQL 5.7.32-35 |
| Data Scrubbing                         | Deprecated                     | Percona Server 5.7.23-24 | Percona Server for MySQL 5.7.32-35 |

## Architecture

The data at rest encryption uses a two-tier architecture with the following components:

| Type                               | Description                                                                         |
|------------------------------------|-------------------------------------------------------------------------------------|
| Master key                         | The Master key is used to encrypt or decrypt the tablespace keys.                   |
| Tablespace key for each tablespace | The tablespace key encrypts the data pages and is written in the tablespace header. |

When the server must access the data, the master key decrypts the tablespace key, the tablespace is decrypted and available for read or write operations.

The two separate keys architecture allows the master key to be rotated in a
minimal operation. During the master key rotation, each tablespace key is
re-encrypted with the new master key. Only the first page of the tablespace file
(.ibd) is read and written during the rotation. An encrypted page is decrypted
at the I/O layer, added to the buffer pool, and used to read and write the data.
A buffer pool page is not encrypted. The I/O layer encrypts the page before the
page is flushed to disk.

An encryption key in the tablespace header is required to encrypt or decrypt the tablespace. The Master key is stored in the keyring plugin.

!!! note

    *Percona XtraBackup* version 2.4 supports the backup of encrypted general tablespaces.

# Vault Keyring Plugin

To enable encryption, use either of the following plugins:

* keyring_file stores the keyring data locally in a flat file

* keyring_vault provides an interface for the database with a HashiCorp Vault
server to store key and secure encryption keys.

Enable only one keyring plugin at a time. Enabling multiple keyring plugins is not supported and may result in data loss.

!!! note

    The keyring_file plugin should not be used for regulatory compliance.

To install the selected plugin, follow the [installing and uninstalling plugins](https://dev.mysql.com/doc/refman/8.0/en/plugin-loading.html) instructions.

## Loading the Keyring Plugin

Load the plugin at server startup with the [early-plugin-load Option](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_early-plugin-load)
to enable the keyring. To make encrypted table recovery more efficient,load the plugin with the configuration file.

Run the following command to load the keyring_file plugin:

```shell
$ mysqld --early-plugin-load="keyring_file=keyring_file.so"
```

!!! note

    To start a server with different early plugins to be loaded, the `--early-plugin-load` option can contain the plugin names in a double-quoted list with each plugin name separated by a semicolon. The use of double quotes ensures the semicolons do not create issues when the list is executed in a script.

To enable Master key vault encryption, the user must have
[SUPER](https://dev.mysql.com/doc/refman/5.7/en/privileges-provided.html#priv_super)
privileges.

The following statements loads the keyring_vault plugin and the keyring_vault_config. The second statement provides the location to the keyring_vault configuration file.

```text
[mysqld]
early-plugin-load="keyring_vault=keyring_vault.so"
loose-keyring_vault_config="/home/mysql/keyring_vault.conf"
```

Add the following statements to my.cnf:

```text
[mysqld]
early-plugin-load="keyring_vault=keyring_vault.so"
loose-keyring_value_config="/home/mysql/keyring_vault.conf"
```

Restart the server.

!!! note

    The keyring_vault extension, “.so”, and the file location for the vault configuration should be changed to match your operating system’s extension and operating system location.

## Describing the keyring_vault_config file

The keyring_vault_config file has the following information:

* `vault_url` - the Vault server address

* `secret_mount_point` - where the keyring_vault stores the keys

* `secret_mount_point_version` - the `KV Secrets Engine version (kv or kv-v2)` used. Implemented in *Percona Server for MySQL* 5.7.33-36.

* `token` - a token generated by the Vault server

* `vault_ca [optional]` - if the machine does not trust the Vault’s CA
certificate, this variable points to the CA certificate used to sign the
Vault’s certificates.

The following is a configuration file example:

```text
vault_url = https://vault.public.com:8202
secret_mount_point = secret
secret_mount_point_version = AUTO
token = 58a20c08-8001-fd5f-5192-7498a48eaf20
vault_ca = /data/keyring_vault_confs/vault_ca.crt
```

!!! warning

    Each `secret_mount_point` must be used by only one server. Multiple servers using the same secret_mount_point may cause unpredictable behavior.

Create a backup of the keyring configuration file or data file immediately
after creating the encrypted tablespace. If you are using Master key encryption, backup before master key rotation and after master key rotation.

The first time a key is retrieved from a keyring, the keyring_vault
communicates with the Vault server to retrieve the key type and data.

| Variables             |
|-----------------------|
| keyring_vault_config  |
| keyring_vault_timeout |

## Verifying the Keyring Plugin is Active

To verify the keyring plugin is active, run the [SHOW PLUGINS](https://dev.mysql.com/doc/refman/8.0/en/show-plugins.html) statement or
run a query on the INFORMATION_SCHEMA.PLUGINS table. You can also query the PLUGINS view.

```sql
SELECT plugin_name, plugin_status FROM INFORMATION_SCHEMA.PLUGINS WHERE plugin_name LIKE 'keyring%';
```

The output could be the following:

```text
+---------------+----------------+
| plugin_name   | plugin_status  |
+===============+================+
| keyring_file  | ACTIVE         |
+---------------+----------------+
```

## Encrypting a File-Per-Table Tablespace

The [CREATE TABLESPACE](https://dev.mysql.com/doc/refman/5.7/en/create-tablespace.html) statement is extended to allow the `ENCRYPTION=['Y/N']` option to encrypt a File-per-Table tablespace.

```sql
CREATE TABLE myexample (id INT mytext varchar(255)) ENCRYPTION='Y';
```

To enable encryption to an existing tablespace, add the `ENCRYPTION` option to the `ALTER TABLE` statement.

```sql
CREATE TABLE myexample ENCRYPTION='Y';
```

You must add the `ENCRYPTION` option to [ALTER TABLE](https://dev.mysql.com/doc/refman/5.7/en/alter-table.html) to change the table encryption state. Without the `ENCRYPTION` option, an encrypted table remains encrypted or an unencrypted table remains unencrypted.

To change the tablespace key, run the [optimize table](https://dev.mysql.com/doc/refman/5.7/en/optimize-table.html) command.

```sql
mysql> optimize table t1;
```

## Encrypting a General Tablespace

As of Percona Server 5.7.20-18, *Percona Server for MySQL* supports general tablespace encryption. You cannot partially encrypt the tables in a general tablespace. All of the tables must be encrypted or none of the tables are encrypted.

### Automatically Encrypting Tablespaces

Add the `innodb_encrypt_tables` variable to my.cnf to automatically encrypt general tablespaces. The possible values for the variable are:

| Value | Description                                                                                                                                         |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| OFF   | The default value which disables automatic encryption of new tables                                                                                 |
| ON    | Enables automatic encryption for new tables                                                                                                         |
| FORCE | New tables are automatically created with encryption.
Adding ENCRYPTION=NO to either a CREATE TABLE or ALTER TABLE statement results in a warning.
 |

The [CREATE TABLESPACE](https://dev.mysql.com/doc/refman/5.7/en/create-tablespace.html) statement is extended to allow the `ENCRYPTION=['
Y/N']` option.

```sql
CREATE TABLE t1 (id INT) ENCRYPTION='Y';
```

To encrypt an existing table, add the ENCRYPTION option in the `ALTER TABLE` statement.

```sql
ALTER TABLE t1 ENCRYPTION='Y';
```

You can also disable encryption for a table, set the
encryption to N.

```sql
ALTER TABLE t1 ENCRYPTION='N';
```

!!! note

    The `ALTER TABLE` statement modifies the current encryption mode only if the `ENCRYPTION` clause is explicitly added.

### System Variables

!!! note

    You cannot change the tablespace key for tables in a general tablespace.

## Encrypting Binary Logs

To start binlog encryption, start the server with `-encrypt-binlog=1`. This state requires `-master_verify_checksum` and `-binlog_checksum` to be `ON` and one of the keyring plugins loaded.

**NOTE**: These actions do not encrypt all binlogs in a replication schema. You must enable `encrypt-binlog` on each of the replica servers, even if they do not produce binlog files. Enabling encryption on replica servers enable relay log encryption.

You can rotate the encryption key used by *Percona Server for MySQL* by running the
following statement:

```sql
SELECT rotate_system_key("percona_binlog");
```

!!! note

    The `rotate_system_key("percona_binlog")` command is **Experimental** quality.

This command creates a new binlog encryption key in the keyring. The new key
encrypts the next binlog file.

## Temporary file encryption

*Percona Server for MySQL* supports the encryption of temporary file storage. Users enable the encryption with `encrypt-tmp_files`.

Enable the variable in the following command:

```text
[mysqld]
...
encrypt-tmp-files=ON
...
```

## Verifying the Encryption Setting

For single tablespaces, verify the ENCRYPTION option using
INFORMATION_SCHEMA.TABLES and the CREATE OPTIONS settings.

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM
       INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';
```

The output could be the following:

```text

+----------------------+-------------------+------------------------------+
| TABLE_SCHEMA         | TABLE_NAME        | CREATE_OPTIONS               |
+----------------------+-------------------+------------------------------+
|sample                | t1                | ENCRYPTION="Y"               |
+----------------------+-------------------+------------------------------+
```

A `flag` field in the `INFORMATION_SCHEMA.INNODB_TABLESPACES` has the bit
number 13 set if the tablespace is encrypted. This bit can be checked with the
`flag & 8192` expression with the following method:

```sql
SELECT space, name, flag, (flag & 8192) != 0 AS encrypted FROM
INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE name in ('foo', 'test/t2', 'bar',
'noencrypt');
```

The output could be the following:

```text

  +-------+-----------+-------+-----------+
  | space | name      | flag  | encrypted |
  +-------+-----------+-------+-----------+
  |    29 | foo       | 10240 |      8192 |
  |    30 | test/t2   |  8225 |      8192 |
  |    31 | bar       | 10240 |      8192 |
  |    32 | noencrypt |  2048 |         0 |
  +-------+-----------+-------+-----------+
  4 rows in set (0.01 sec)
```

To allow for master Key rotation, you can encrypt an already encrypted InnoDB
system tablespace with a new master key by running the following `ALTER
INSTANCE` statement:

```sql
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

## Rotating the Master Key

For security, you should rotate the Master key in a timely manner. Use the `ALTER INSTANCE` statement. To rotate the key, you must have `SUPER` privilege.

```sql
ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

The statement cannot be run at the same time you run `CREATE TABLE ... ENCRYPTION` or `ALTER TABLE ENCRYPTION` statements. The `ALTER INSTANCE` statement uses locks to prevent conflicts. If a DML statement is running, that statement must complete before the `ALTER INSTANCE` statement begins.

When the Master key is rotated, the tablespace keys in that instance are re-encrypted. The operation does not re-encrypt the tablespace data.

The re-encryption for the tablespace keys must succeed for the key rotation to be successful. If the rotation is interrupted, for example, if there is a server failure, the operation rolls forward when the server restarts.

## InnoDB System Tablespace Encryption

This feature was in **tech preview** from version 5.7.23-24 but is **deprecated** from version 5.7.32-35. This feature is not recommended to be used in production.

The InnoDB system tablespace is encrypted by using master key encryption. The
server must be started with the `--bootstrap` option.

If the variable innodb_sys_tablespace_encrypt is set to ON and the
server has been started in the bootstrap mode, you may create an encrypted table
as follows:

```sql
mysql> CREATE TABLE ... TABLESPACE=innodb_system ENCRYPTION='Y'
```

!!! note

    You cannot encrypt existing tables in the System tablespace.

It is not possible to convert the system tablespace from encrypted to
unencrypted or vice versa. A new instance should be created and user tables must
be transferred to the desired instance.

You can encrypt the already encrypted InnoDB system tablespace (key rotation)
with a new master key by running the following `ALTER INSTANCE` statement:

```sql
mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY
```

### `innodb_sys_tablespace_encrypt`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --innodb-sys-tablespace-encrypt |
| Scope        | Global                          |
| Dynamic      | No                              |
| Data type    | Boolean                         |
| Default      | OFF                             |

The variable has been implemented in Percona Server 5.7.23-24 and deprecated in Percona Server for MySQL 5.7.32-35. Enables the encryption of the InnoDB System tablespace. It is essential that the
server is started with the `--bootstrap` option.

## Doublewrite buffer

This feature was in **tech preview** from version Percona Server 5.7.23-24 but is **deprecated** from version Percona Server for MySQL 5.7.32-35. This feature is not recommended to be used in production.

The two types of doublewrite buffers used in *Percona Server for MySQL* are encrypted
differently.

When the InnoDB system tablespace is encrypted, the `doublewrite buffer` pages
are encrypted as well. The key which was used to encrypt the InnoDB system
tablespace is also used to encrypt the doublewrite buffer.

*Percona Server for MySQL* encrypts the `parallel doublewrite buffer` with the respective
tablespace keys. Only encrypted tablespace pages are written as encrypted in the
parallel doublewrite buffer. Unencrypted tablespace pages will be written as
unencrypted.

### `innodb_parallel_dblwr_encrypt`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --innodb-parallel-dblwr-encrypt |
| Scope        | Global                          |
| Dynamic      | Yes                             |
| Data type    | Boolean                         |
| Default      | OFF                             |

The variable has been implemented in Percona Server 5.7.23-24 and deprecated in Percona Server for MySQL 5.7.32-35. Enables the encryption of the parallel doublewrite buffer. For encryption, uses
the key of the tablespace where the parallel doublewrite buffer is used.

## InnoDB Undo Tablespace Encryption

This feature was in **tech preview** from version Percona Server 5.7.23-24 but is **deprecated** from version Percona Server for MySQL 5.7.32-35. This feature is not recommended to be used in production.

The encryption of InnoDB Undo tablespaces is only available when using
separate undo tablespaces. Otherwise, the InnoDB undo log is part of
the InnoDB system tablespace.

## System variables

### `innodb_undo_log_encrypt`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --innodb-undo-log-encrypt |
| Scope        | Global                    |
| Dynamic      | Yes                       |
| Data type    | Boolean                   |
| Default      | Off                       |

The variable has been implemented in Percona Server 5.7.23-24 and deprecated in Percona Server for MySQL 5.7.32-35. Enables the encryption of InnoDB Undo tablespaces. You can enable encryption and
disable encryption while the server is running.

!!! note

    If you enable undo log encryption, the server writes encryption information into the header. That information stays in the header during the life of the undo log. If you restart the server, the server will try to load the encryption key from the keyring during startup. If the keyring is not available, the server cannot start.

## Redo Log Encryption

This feature was in **tech preview** from version 5.7.23-24 but is **deprecated** from version 5.7.32-35. This feature is not recommended to be used in production.

InnoDB redo log encryption is enabled by setting the variable
innodb_redo_log_encrypt. This variable has three values:
`MASTER_KEY`, `KEYRING_KEY` and `OFF` (set by default).

`MASTER_KEY` uses the InnoDB master key to encrypt with unique keys for each
log file in the redo log header.

`KEYRING_KEY` uses the `percona_redo` versioned key from the keyring. When
innodb_redo_log_encrypt is set to `KEYRING_KEY`, each new redo log
file is encrypted with the latest `percona_redo` key from the keyring.

## System variables

Implemented in version Percona Server for MySQL 5.7.27-30, the key rotation is redesigned to allow `SELECT rotate_system_key("percona_redo)`. The currently used key version is available in the innodb_redo_key_version status. The feature is **Experimental**.

## Data Scrubbing

This feature was in **tech preview** from version Percona Server 5.7.23-24 but is **deprecated** from version Percona Server for MySQL 5.7.32-35. This feature is not recommended to be used in production.

While data encryption ensures that the existing data are not stored in plain
form, the data scrubbing literally removes the data once the user decides they
should be deleted. Compare this behavior with how the `DELETE` statement works
which only marks the affected data as *deleted* - the space claimed by this data
is overwritten with new data later.

Once enabled, data scrubbing works automatically on each tablespace
separately. To enable data scrubbing, you need to set the following variables:

* innodb-background-scrub-data-uncompressed

* innodb-background-scrub-data-compressed

Uncompressed tables can also be scrubbed immediately, independently of key
rotation or background threads. This can be enabled by setting the variable
innodb-immediate-scrub-data-uncompressed. This option is not supported for
compressed tables.

Note that data scrubbing is made effective by setting the
innodb_online_encryption_threads variable to a value greater than
**zero**.

## System Variables

### `innodb_background_scrub_data_compressed`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --innodb-background-scrub-data-compressed |
| Scope        | Global                                    |
| Dynamic      | Yes                                       |
| Data type    | Boolean                                   |
| Default      | OFF                                       |

The variable has been implemented in Percona Server 5.7.23-24 and deprecated in Percona Server for MySQL 5.7.32-35.

### `innodb_background_scrub_data_uncompressed`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --innodb-background-scrub-data-uncompressed |
| Scope        | Global                                      |
| Dynamic      | Yes                                         |
| Data type    | Boolean                                     |
| Default      | OFF                                         |

The variable has been implemented in Percona Server 5.7.23-24 and deprecated in Percona Server for MySQL 5.7.32-35.

## Variables

keyring_vault_config - Defines the location of the Loading the Keyring Plugin configuration file.

| Option        | Description            |
|---------------|------------------------|
| Command line  | --keyring-vault-config |
| Dynamic       | Yes                    |
| Scope         | Global                 |
| Variable Type | Text                   |
| Default       |

keyring_vault_timeout - Set the duration in seconds for the Vault server connection timeout. The default value is `15`. The allowed range is from `0` to `86400`. To wait an infinite amount of time set the variable to `0`.

| Option        | Description             |
|---------------|-------------------------|
| Command line  | --keyring-vault-timeout |
| Dynamic       | Yes                     |
| Scope         | Global                  |
| Variable Type | Numeric                 |
| Default       | 15                      |

### `innodb_encrypt_tables`

| Option       | Description             |
|--------------|-------------------------|
| Command-line | --innodb-encrypt-tables |
| Scope        | Global                  |
| Dynamic      | Yes                     |
| Data type    | Text                    |
| Default      | OFF                     |

The variable has been implemented in Percona Server 5.7.21-21.

!!! note

    This variable is **Experimental** quality.

### `innodb_redo_log_encrypt`

| Option       | Description               |
|--------------|---------------------------|
| Command-line | --innodb-redo-log-encrypt |
| Scope        | Global                    |
| Dynamic      | Yes                       |
| Data type    | Text                      |
| Default      | OFF                       |

The variable has been implemented in Percona Server 5.7.23-24. Enables the encryption of the redo log.


### `innodb_scrub_log`

| Option       | Description        |
|--------------|--------------------|
| Command-line | --innodb-scrub-log |
| Scope        | Global             |
| Dynamic      | Yes                |
| Data type    | Boolean            |
| Default      | OFF                |

The variable has been implemented in Percona Server 5.7.23-24. Specifies if data scrubbing should be automatically applied to the redo log.

### `innodb_scrub_log_speed`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --innodb-scrub-log-speed |
| Scope        | Global                   |
| Dynamic      | Yes                      |
| Data type    | Text                     |
| Default      |

The variable has been implemented in Percona Server 5.7.23-24. Specifies the velocity of data scrubbing (writing dummy redo log records) in bytes per second.
