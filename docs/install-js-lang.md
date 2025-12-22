# Install js_lang component

--8<--- "tech.preview.md:5:5"

The `plugin_dir` system variable specifies where the component library is located. If you need to, you should set the `plugin_dir` variable when you start the server.

To install the `js_lang` component, you need to run the following command:

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://component_js_lang';
```

If you decide to uninstall the component, you may have to restart the server before you can reinstall it.

When you install the `component_js_lang`, it gives you a new global privilege called `CREATE_JS_ROUTINE`. This privilege allows you to create JS routines within the database.

For more details, check out [INSTALL COMPONENT](install-component.md).

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)