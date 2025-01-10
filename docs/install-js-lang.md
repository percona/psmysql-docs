# Install js_lang component

The `plugin_dir` system variable specifies where the component library is located. If you need to, you should set the `plugin_dir` variable when you start the server.

To install the `js_lang` component, you need to run the following command:

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://component_js_lang';
```

If you decide to uninstall the component, you may have to restart the server before you can reinstall it.

When you install the `component_js_lang`, it gives you a new global privilege called `CREATE_JS_ROUTINE`. This privilege allows you to create JS routines within the database.

For more details, check out [INSTALL COMPONENT](install-component.md).