# Enforce storage engine

Percona Server for MySQL lets you enforce a specific storage engine for table creation. You do this with the [`enforce_storage_engine`](#enforce_storage_engine) variable.

## Benefits

The option allows you to enforce a specific storage engine for all table creations. This ability can be useful for:


When `enforce_storage_engine` is set, Percona Server behaves as follows:

| Benefit               | Description                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------------|
| Ensuring consistency   | Prevents creating tables with different storage engines, ensuring consistent behavior and performance. |
| Simplifying administration | Centralizing the storage engine selection streamlines database administration procedures.     |
| Optimizing performance | Improves performance when an application is designed for a specific storage engine.             |
| Compliance             | Enforces a specific storage engine to meet regulatory or compliance requirements.               |

## Version information

* [Percona Server for MySQL 8.0.13-4](release-notes/Percona-Server-8.0.13-4.md): The feature was ported from Percona Server for MySQL 5.7.

## System variables

### `enforce_storage_engine`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Config file    | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value  | NULL               |

This variable is not case-sensitive.

When `enforce_storage_engine` is set, the server enforces specfic rules for table creation.

If [`NO_ENGINE_SUBSTITUTION` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_no_engine_substitution) SQL mode is enabled.

The server enforces strict storage engine rules during table creation. If you specify a storage engine that differs from the enforced engine, the server will do the following:

* Generates an error

* Does not create a table

If [`NO_ENGINE_SUBSTITUTION` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_no_engine_substitution) SQL mode is disabled.

When you specify a storage engine that differs from the enforced engine, the server does the following:

* Creates the table using the enforced storage engine

* Issues a warning about engine substitution

You can check the current SQL mode settings:

```{.bash data-prompt="mysql>"}
mysql> SELECT @sql_mode;
```

The server requires a valid storage engine setting for `enforce_storage_engine`. If the storage engine is not available, the server does not start.

You can check the available storage engines with the following command:

```{.bash data-prompt="mysql>"}
mysql> SHOW ENGINES;
```

??? example "Expected output"

    ```{.text .no-copy}
    Engine      | Support | Comment
    ------------|---------|------------------
    InnoDB      | DEFAULT | Supports transactions, foreign keys
    MyISAM      | YES     | MySQL storage engine
    MEMORY      | YES     | Hash based, stored in memory
    CSV         | YES     | CSV storage engine
    ARCHIVE     | YES     | Archive storage engine
    ```

The `Support` column indicates the following:

* `DEFAULT`: The default engine

* `YES`: Engine is supported

* `NO`: Engine is not supported

* `DISABLED`: Engine is disabled


!!! important

    If you use `enforce_storage_engine`, you must either disable
    it before doing `mysql_upgrade` or run `mysql_upgrade` with the server
    started with the `--skip-grants-tables` option.


## Example

To enforce the InnoDB storage engine, add this option to your [my.cnf](glossary.md#mycnf) file:

```ini

[mysqld]
enforce_storage_engine=InnoDB

```

Changes to the `my.cnf` do not affect a running server. You must restart the server for the change to take effect:

```{.bash data-prompt="$"}
$ sudo systemctl restart mysqld
```


