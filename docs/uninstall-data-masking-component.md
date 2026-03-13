# Uninstall the data masking component

Uninstalling removes the masking functions and (if you choose) the dictionary table. The steps below prioritize a clean removal. Before you run them, address dependencies, privileges, and the risk of exposing previously masked data.

## Before you uninstall

* Views, stored procedures, and triggers: Any view, routine, or trigger that calls masking functions (for example, in a `SELECT` or default expression) depends on the component. After `UNINSTALL COMPONENT`, those objects become invalid. Queries that use them can fail with an error such as a missing function or component. Before uninstalling, identify and either drop or replace those objects, or ensure no application uses them. If you leave them in place and uninstall, applications that query the view may fail or, if they fall back to base tables, may see unmasked data. Plan to replace masking-based views with restricted views, dummy tables, or access denial so that uninstallation does not inadvertently expose raw data.

* Privileges: The install procedure grants `MASKING_DICTIONARIES_ADMIN` to users and may grant privileges to `mysql.session` on `mysql.masking_dictionaries`. Uninstalling does not revoke these. For a clean state, revoke them before or after uninstall. To revoke from `mysql.session`, the table must still exist, so do that before dropping the table. Example (adjust for your database if you changed `masking_database`):

  ```sql
  REVOKE MASKING_DICTIONARIES_ADMIN ON *.* FROM <user>;
  REVOKE SELECT, INSERT, UPDATE, DELETE ON mysql.masking_dictionaries FROM 'mysql.session'@'localhost';
  ```

* System variables: If you set masking-related variables (for example, `component_masking_functions.dictionaries_flush_interval_seconds` or the database used for the dictionaries table), remove or reset them in your configuration (for example, `my.cnf` or the command line). After the component is uninstalled, references to component variables in the config can produce "unknown variable" warnings or errors on server restart and can confuse configuration management tools.

* In-flight use: Ensure no views, routines, or applications are actively using masking functions when you uninstall. Uninstalling while queries or background processes depend on the component can cause those operations to fail.

## Uninstall steps

The following steps uninstall the component; the second step optionally drops the `masking_dictionaries` table.
{.power-number}

1. Uninstall the component and loadable functions.

    ```sql
    UNINSTALL COMPONENT 'file://component_masking_functions';
    ```

    After this step, any view, stored procedure, or trigger that references masking functions is invalid and will cause errors when used.

2. Optionally drop the `masking_dictionaries` table.

    Dropping this table permanently removes all dictionary data and cannot be undone. Skip this step if you plan to reinstall or upgrade and want to keep the table and data. If you might need the dictionary data later, back up the table or export the data before dropping.

    ```sql
    DROP TABLE mysql.masking_dictionaries;
    ```

    If you granted privileges to `mysql.session` on this table and did not revoke them in "Before you uninstall," the grant entries may remain in the system until you revoke them; revoking requires the table to exist, so revoke before dropping the table if you want a full cleanup.

## Useful links

[Install the data masking component](install-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)
