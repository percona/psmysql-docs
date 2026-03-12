# Install the data masking component

## Prerequisites

* Percona Server for MySQL with the data masking component available for your version.
* The `component_masking_functions` library must be present in the server plugin directory. The `plugin_dir` system variable defines that directory; the server resolves `file://component_masking_functions` in `INSTALL COMPONENT` relative to `plugin_dir`. To verify the library is available, check that the file exists in the directory reported by:
  ```sql
  SHOW VARIABLES LIKE 'plugin_dir';
  ```
  If the library is missing, `INSTALL COMPONENT` fails at load time; check the server error log and your installation package or deployment to ensure the component library is installed in the plugin directory.

The component has the following parts:

* A system table, `mysql.masking_dictionaries`, used to store terms and dictionaries (you must create this table; see below).
* The loadable component `component_masking_functions`, which provides the masking functions.

The `MASKING_DICTIONARIES_ADMIN` privilege is required for dictionary management functions; the privilege is registered when the component is loaded.

## Install the component

Follow the steps in order. The table must exist and match the required schema before you run `INSTALL COMPONENT`; the component does not create the table. If the table is missing or the schema is wrong (for example, a typo in column names or types), the component can load in a broken state or fail.
{.power-number}

1. Create the `masking_dictionaries` table in the `mysql` schema.

    Ensure the statement completes and is committed before you run step 2. The schema below is required; do not alter column names or types unless a future Percona Server release documents a different schema. You are responsible for creating and maintaining this table; if the component’s expected schema changes in an upgrade, release or upgrade documentation will describe any required `ALTER TABLE` or migration that you must apply.

    ```sql
    CREATE TABLE IF NOT EXISTS
    mysql.masking_dictionaries(
        Dictionary VARCHAR(256) NOT NULL,
        Term VARCHAR(256) NOT NULL,
        UNIQUE INDEX dictionary_term_idx (Dictionary, Term)
    ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
    ```

2. Install the component and loadable functions.

    ```sql
    INSTALL COMPONENT 'file://component_masking_functions';
    ```

    If the command fails, check the server error log and confirm the library is present in `plugin_dir` (see [Prerequisites](#prerequisites)). The component is registered in `mysql.component` and is loaded again on server restart. On replicas or in high-availability setups, the instance may be in `read_only` or `super_read_only` mode; component loading in those states follows server behavior. If the component does not load on a replica (for example, because the library is missing or configuration differs), masking is not available on that instance until the cause is resolved.

    On Percona Server for MySQL 8.4.4-1 and later, dictionary-based functions (`gen_dictionary`, `gen_blocklist`) use the built-in `mysql.session` user for internal queries. Grant `mysql.session` the required privileges on the `masking_dictionaries` table as described in [Permissions](data-masking-function-list.md#permissions) in the data masking function list. Granting these privileges allows the server to read and modify the dictionary table for masking; the table may contain lookup data. Rely on your normal access controls and hardening for the `mysql` schema and dictionary contents.

3. Grant `MASKING_DICTIONARIES_ADMIN` to users who will manage dictionaries.

    The privilege is registered when the component loads. Run this step only after `INSTALL COMPONENT` has succeeded. If `GRANT` fails with an unknown-privilege or similar error, the component may not be loaded or your Percona Server version may not support this privilege; verify the component is loaded (for example, check `mysql.component`) and consult the documentation for your version.

    The following functions require `MASKING_DICTIONARIES_ADMIN`:

    * `masking_dictionary_term_add`
    * `masking_dictionary_term_remove`
    * `masking_dictionary_remove`

    ```sql
    GRANT MASKING_DICTIONARIES_ADMIN ON *.* TO <user>;
    ```

## Useful links

[Uninstall the data masking component](uninstall-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)

[Data masking quickstart](quickstart-data-masking.md) — create a test database and try masking functions.