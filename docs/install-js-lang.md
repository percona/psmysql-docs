# Install js_lang component

--8<--- "tech.preview.md:5:5"

The `plugin_dir` system variable specifies where the component library is located. If you need to, you should set the `plugin_dir` variable when you start the server.

Install the `percona-server-js` package before you install the `js_lang` component. This package provides support for server-side JavaScript stored programs in Percona Server.

Run the command for your operating system:

=== "Ubuntu"

    ```shell
    sudo apt install percona-server-js
    ```

    The `apt` package installs the library in `/usr/lib/mysql/plugin/`. This path is the value of `plugin_dir`.

=== "RHEL"

    ```shell
    sudo dnf install percona-server-js
    ```

For more information about the `percona-server-js` package, see [DEB repository package list](apt-files.md) and [Yum repository package list](yum-files.md).

To install the `js_lang` component, you need to run the following command:

```sql
INSTALL COMPONENT 'file://component_js_lang';
```

When you install the `component_js_lang`, it gives you a new global privilege called `CREATE_JS_ROUTINE`. This privilege enables you to create JS routines within the database.

Grant `CREATE_JS_ROUTINE` to the account that will create routines, even `root`.

```sql
GRANT CREATE_JS_ROUTINE ON *.* TO root@localhost;
```

Creating a routine without this privilege fails with `ERROR 1227`. The error names `CREATE_JS_ROUTINE`.

For more information about this privilege, see [js_lang privileges](js-lang-privileges.md).

!!! note
    Running `INSTALL COMPONENT` a second time returns `ERROR 3529: Cannot load component from specified URN`.

If you [uninstall the js_lang component](uninstall-js-lang.md), restart the server before you install it again. Reinstalling without a restart fails with `ERROR 6000: Re-installing the component without server restart is not supported`.

After the restart, run `INSTALL COMPONENT` again.

For more details, check out [INSTALL COMPONENT](install-component.md).

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [js_lang component system variables](js-lang-variables.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)