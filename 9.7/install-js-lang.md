> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install js_lang component

This feature is a [tech preview](https://docs.percona.com/percona-server/9.7/glossary.md#tech-preview). Before using this feature in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

The `plugin_dir` system variable specifies where the component library is located. If you need to, you should set the `plugin_dir` variable when you start the server.

To install the `js_lang` component, you need to run the following command:

```sql
INSTALL COMPONENT 'file://component_js_lang';
```

If you decide to uninstall the component, you may have to restart the server before you can reinstall it.

When you install the `component_js_lang`, it gives you a new global privilege called `CREATE_JS_ROUTINE`. This privilege allows you to create JS routines within the database.

For more details, check out [INSTALL COMPONENT](https://docs.percona.com/percona-server/9.7/install-component.md).

## Further reading

- [js_lang stored procedure and function overview](https://docs.percona.com/percona-server/9.7/js-lang-overview.md)
- [Uninstall the js_lang component](https://docs.percona.com/percona-server/9.7/uninstall-js-lang.md)
- [js_lang stored function or procedure](https://docs.percona.com/percona-server/9.7/js-lang-procedures.md)
- [js_lang privileges](https://docs.percona.com/percona-server/9.7/js-lang-privileges.md)
- [js_lang component system variables](https://docs.percona.com/percona-server/9.7/js-lang-variables.md)
- [Troubleshoot js_lang procedures and functions](https://docs.percona.com/percona-server/9.7/js-lang-troubleshoot.md)
