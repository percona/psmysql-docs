# The ps-admin script

The `ps-admin` script is an administrative helper in Percona Server for MySQL {{vers}}.

The script enables or disables optional plugins and the MyRocks storage engine on a running server.

The script connects with administrator credentials and runs the required `INSTALL PLUGIN` or `UNINSTALL PLUGIN` statements.

## Requirements

Meet the following requirements before you run `ps-admin`:

* Install and start Percona Server for MySQL {{vers}}.

* Keep the `mysql` client in the same directory as `ps-admin`.

* Grant the MySQL user privilege to install or uninstall plugins.

* Confirm that the plugin shared library exists in the server plugin directory.

Run `ps-admin` as the operating system `root` user or with `sudo`.

Install the `percona-server-rocksdb` package before you enable MyRocks.

## Command syntax

The following syntax is the general form of the command:

```shell
$ sudo ps-admin <ACTION> -u <MYSQL_ADMIN_USER> -p[<MYSQL_ADMIN_PASSWORD>] \
    [-S <SOCKET>] [-h <HOST> -P <PORT>]
```

Replace `<ACTION>` with one enable option or one disable option.

Specify at least one `--enable-*` option or one `--disable-*` option.

Use only `--enable-rocksdb` or only `--disable-rocksdb` for MyRocks. Apply the same rule to each plugin.

Print the option list with the following command:

```shell
$ ps-admin --help
```

## Connection options

The following table lists options that control the MySQL connection:

| Option | Short option | Description |
| --- | --- | --- |
| `--user=<USER_NAME>` | `-u` | MySQL administrator user name. The default value is `root`. |
| `--password[=<PASSWORD>]` | `-p` | MySQL administrator password. An empty `-p` value prompts for the password. |
| `--socket=<PATH>` | `-S` | Unix socket file for the connection |
| `--host=<HOST_NAME>` | `-h` | Host name for a TCP connection |
| `--port=<PORT_NUM>` | `-P` | Port number for a TCP connection |
| `--config-file=<FILE>` | `-c` | File that provides credentials and options |

## Plugin and engine options

The following table lists options that enable or disable plugins and MyRocks:

| Option | Short option | Action |
| --- | --- | --- |
| `--enable-rocksdb` | `-k` | Enable the MyRocks (`ROCKSDB`) storage engine |
| `--disable-rocksdb` | `-o` | Disable the MyRocks storage engine |
| `--enable-pam` | `-i` | Enable the Pluggable Authentication Modules (PAM) plugin (`auth_pam`) |
| `--disable-pam` | `-n` | Disable the PAM plugin |
| `--enable-pam-compat` | `-j` | Enable the Oracle-compatible PAM plugin (`auth_pam_compat`) |
| `--disable-pam-compat` | `-K` | Disable the Oracle-compatible PAM plugin |
| `--enable-audit` | `-a` | Enable the Audit Log plugin (`audit_log`) |
| `--disable-audit` | `-w` | Disable the Audit Log plugin |
| `--enable-mysqlx` | `-x` | Enable the MySQL X plugin (`mysqlx`) |
| `--disable-mysqlx` | `-g` | Disable the MySQL X plugin |

## Enable MyRocks

Install the MyRocks package first. For package steps, see [Percona MyRocks installation guide](install-myrocks.md).

Enable MyRocks with the following command:

```shell
$ sudo ps-admin --enable-rocksdb -u root -p
```

The script searches for `ha_rocksdb.so` in the following locations:

* `../lib/plugin` relative to the `ps-admin` directory

* `/usr/lib64/mysql/plugin`

* `/usr/lib/mysql/plugin`

The script then installs the MyRocks plugins on the running server.

Verify the engine with the following statement:

```sql
SHOW ENGINES;
```

The `ROCKSDB` row must show `YES` in the `Support` column.

InnoDB remains the default storage engine after the enable command. To create tables on MyRocks, set `default-storage-engine=rocksdb` in the `[mysqld]` section of `my.cnf`, or add `ENGINE=RocksDB` to each `CREATE TABLE` statement.

For more detail, see [Percona MyRocks installation guide](install-myrocks.md).

## Enable the PAM authentication plugin

Enable the full PAM plugin with the following command:

```shell
$ sudo ps-admin --enable-pam -u root -p
```

The script runs the following statement:

```sql
INSTALL PLUGIN auth_pam SONAME 'auth_pam.so';
```

Enable the Oracle-compatible PAM plugin with the following command:

```shell
$ sudo ps-admin --enable-pam-compat -u root -p
```

The script runs the following statement:

```sql
INSTALL PLUGIN auth_pam_compat SONAME 'auth_pam_compat.so';
```

Configure the PAM stack after the plugin is active. For PAM files, user accounts, and client requirements, see [PAM authentication plugin](pam-plugin.md).

## Enable the Audit Log plugin

!!! note "Deprecation notice"

    The Audit Log plugin is deprecated in Percona Server for MySQL {{vers}}. Use the [Audit Log Filter component](audit-log-filter-overview.md) as the replacement. Do not install the Audit Log plugin and the Audit Log Filter component on the same server.

Enable the Audit Log plugin with the following command:

```shell
$ sudo ps-admin --enable-audit -u root -p
```

The script runs the following statement:

```sql
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
```

For plugin variables and log format, see [Audit log plugin](audit-log-plugin.md).

## Enable the MySQL X plugin

The MySQL X plugin provides X Protocol support.

Enable the MySQL X plugin with the following command:

```shell
$ sudo ps-admin --enable-mysqlx -u root -p
```

The script runs the following statement:

```sql
INSTALL PLUGIN mysqlx SONAME 'mysqlx.so';
```

For X Protocol and plugin options, see the [X Plugin :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/x-plugin.html) documentation.

## Disable a plugin or engine

Disable MyRocks with the following command:

```shell
$ sudo ps-admin --disable-rocksdb -u root -p
```

Convert MyRocks tables to another engine before you disable MyRocks if you still need the data.

Disable other plugins with the matching `--disable-*` option.

The following examples disable each supported plugin:

```shell
$ sudo ps-admin --disable-pam -u root -p
```

```shell
$ sudo ps-admin --disable-pam-compat -u root -p
```

```shell
$ sudo ps-admin --disable-audit -u root -p
```

```shell
$ sudo ps-admin --disable-mysqlx -u root -p
```

## Verify plugin status

The script checks `INFORMATION_SCHEMA.PLUGINS` before each change.

Confirm the result with the following statement:

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS, PLUGIN_TYPE
FROM INFORMATION_SCHEMA.PLUGINS
WHERE PLUGIN_NAME IN (
  'ROCKSDB',
  'auth_pam',
  'auth_pam_compat',
  'audit_log',
  'mysqlx'
);
```

The `PLUGIN_STATUS` value is `ACTIVE` after a successful enable operation.

An empty result after a disable operation means the plugin is not loaded.

## Connection examples

Prompt for the password on a local socket:

```shell
$ sudo ps-admin --enable-pam -u root -p -S /var/run/mysqld/mysqld.sock
```

Connect over TCP:

```shell
$ sudo ps-admin --enable-rocksdb -u root -pPassw0rd -h 127.0.0.1 -P 3306
```

## Troubleshoot

Use the following actions after a script error:

* Check the user name, password, host, port, or socket after a plugin list failure.

* Install the MyRocks package after a missing `ha_rocksdb.so` library message.

* Uninstall leftover MyRocks plugins by hand after a partial install, then run `--enable-rocksdb` again.

* Verify the plugin library path and MySQL plugin privileges after an install failure.

Review the server error log after an install or uninstall failure.

## Other reading

The following topics describe the features that `ps-admin` enables or disables:

* [Percona MyRocks installation guide](install-myrocks.md)

* [Show storage engines](show-engines.md)

* [PAM authentication plugin](pam-plugin.md)

* [Authentication methods](authentication-methods.md)

* [Audit log plugin](audit-log-plugin.md)

* [Audit Log Filter overview](audit-log-filter-overview.md)

* [Migrate to the audit log filter component](migrate-to-audit-log-filter-component.md)

* [Post-installation](post-installation.md)

!!! note

    The MySQL X plugin (`--enable-mysqlx` and `--disable-mysqlx`) is omitted from this list. Percona Server for MySQL has no dedicated MySQL X plugin.
