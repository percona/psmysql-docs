# Install the data masking component

The component has the following parts:

* A database server system table used to store the terms and dictionaries
* A `component_masking_functions` component that contains the loadable functions

The `MASKING_DICTIONARIES_ADMIN` privilege may be required by some functions.

## Install the component

The following steps install the component:

1. Create `masking_dictionaries`.

    ```{.bash data-prompt="mysql>"}
    mysql> CREATE TABLE IF NOT EXISTS
    mysql.masking_dictionaries(
        Dictionary VARCHAR(256) NOT NULL,
        Term VARCHAR(256) NOT NULL,
        UNIQUE INDEX dictionary_term_idx (Dictionary, Term)
    ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
    ```

2. Install the data masking components and the loadable functions.

    ```{.bash data-prompt="mysql>"}
    mysql> INSTALL COMPONENT 'file://component_masking_functions';
    ```

3. The `MASKING_DICTIONARIES_ADMIN` is required to use the the following functions:

    * `masking_dictionary_term_add`

    * `masking_dictionary_term_remove`

    * `masking_dictionary_remove`

        ```{.bash data-prompt="mysql>"}
        mysql> GRANT MASKING_DICTIONARIES_ADMIN ON *.* TO <user>;
        ```

## Useful links

[Uninstall the data masking component](uninstall-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)