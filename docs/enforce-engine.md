# Enforcing storage engine

Percona Server for MySQL implements a variable to enforce the
use of a specific storage engine.

When this variable is specified and a user tries to create a table using an
explicit storage engine that is not the specified enforced engine, the user
will get either an error if the `NO_ENGINE_SUBSTITUTION` SQL mode is enabled
or a warning if `NO_ENGINE_SUBSTITUTION` is disabled and the table
will be created anyway using the enforced engine (this is consistent with the
default *MySQL* way of creating the default storage engine if other engines
are not available unless `NO_ENGINE_SUBSTITUTION` is set).

In case a user tries to enable [enforce_storage_engine](#enforce_storage_engine) with an engine that isn’t available, the system will not start.

!!! note

    If you’re using enforce_storage_engine, disable it before you start
    the upgraded server. In 8.4 there is no `mysql_upgrade` step: the server
    upgrades the data dictionary and system tables itself at startup, as
    controlled by the `--upgrade` server option (default `AUTO`). See
    [Upgrade procedures](upgrade-procedures.md). After the server has started
    and completed the upgrade, set `enforce_storage_engine` again in the
    option file.

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

This variable is not case sensitive.

## Example

Adding following option to [my.cnf](glossary.md#mycnf) will start the server with InnoDB as enforced storage engine.

```{.text .no-copy}
enforce_storage_engine=InnoDB
```
