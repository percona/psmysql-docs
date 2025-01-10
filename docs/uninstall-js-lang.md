# Uninstall the js_lang component

The uninstall works only when no connections are using JavaScript stored programs. If there are connections, the procedure fails with an error.

To remove the component, run the following:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_js_lang';
```