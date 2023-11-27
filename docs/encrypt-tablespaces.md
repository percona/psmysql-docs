# Encrypt schema or general tablespace

Percona Server for MySQL uses the same encryption architecture as MySQL, a two-tier system consisting of a master key and tablespace keys. The master key can be changed, or rotated in the keyring, as needed. Each tablespace key, when
decrypted, remains the same.

The feature requires the keyring plugin.

## Set the default for schemas and general tablespace encryption

The tables in a general tablespace are either all encrypted or all unencrypted.
A tablespace cannot contain a mixture of encrypted tables and unencrypted
tables.

The encryption of a schema or a general tablespace is determined by the
`default_table_encryption` variable unless you specify the
ENCRYPTION clause in the CREATE SCHEMA or CREATE TABLESPACE statement.

You can set the `default_table_encryption` variable in an individual
connection.

```{.bash data-prompt="mysql>"}
mysql> SET default_table_encryption=ON;
```

## `default_table_encryption`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | default-table-encryption |
| Scope        | Session                  |
| Dynamic      | Yes                      |
| Data type    | Text                     |
| Default      | OFF                      |


Defines the default encryption setting for schemas and general tablespaces. The
variable allows you to create or alter schemas or tablespaces without specifying
the ENCRYPTION clause. The default encryption setting applies only to schemas
and general tablespaces and is not applied to the MySQL system tablespace.

The variable has the following possible options:

| Value | Description |
|---|---|
|  `ON` | New tables are encrypted. Add `ENCRYPTION="N"` to the `CREATE TABLE` or `ALTER TABLE` statement to create unencrypted tables. |
| `OFF` | By default, new tables are unencrypted. Add `ENCRYPTION="Y"` to the `CREATE TABLE` or `ALTER TABLE` statement to create encrypted tables.

!!! note

    The `ALTER TABLE` statement changes the current encryption mode only if you use the `ENCRYPTION` clause.
    
## `innodb_encrypt_online_alter_logs`

| Option       | Description                        |
|--------------|------------------------------------|
| Command-line | --innodb-encrypt-online-alter-logs |
| Scope        | Global                             |
| Dynamic      | Yes                                |
| Data type    | Boolean                            |
| Default      | OFF                                |

This variable simultaneously turns on the encryption of files used by InnoDB for
full-text search using parallel sorting, building indexes using merge sort, and
online DDL logs created by InnoDB for online DDL. Encryption is available for
file merges used in queries and backend processes.

## Use ENCRYPTION

If you do not set the default encryption setting, you can create general
tablespaces with the `ENCRYPTION` setting.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLESPACE tablespace_name ENCRYPTION='Y';
```

All tables contained in the tablespace are either encrypted or not encrypted.
You cannot encrypt only some of the tables in a general tablespace. This
feature extends the  [CREATE TABLESPACE](https://dev.mysql.com/doc/refman/8.0/en/create-tablespace.html) statement to
accept the `ENCRYPTION='Y/N'` option.

The option is a tablespace attribute and is not allowed with the `CREATE TABLE` or `SHOW CREATE TABLE` statement except with file-per-table tablespaces.

In an encrypted general tablespace, an attempt to create an unencrypted table
generates the following error:

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE t3 (a INT, b TEXT) TABLESPACE foo ENCRYPTION='N';
```

??? example "Expected output"

    ```{.text .no-copy}
    ERROR 1478 (HY0000): InnoDB: Tablespace 'foo' can contain only ENCRYPTED tables.
    ```

The server diagnoses an attempt to create or move tables, including partitioned ones, to a
general tablespace with an incompatible encryption setting and aborts the process.

If you must move tables between incompatible tablespaces, create tables with the same structure in another tablespace and run `INSERT INTO SELECT` from each of the source tables into the destination tables.

## Export an encrypted general tablespace

You can only export encrypted file-per-table tablespaces
