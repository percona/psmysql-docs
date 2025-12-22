# Uninstall the js_lang component

--8<--- "tech.preview.md:5:5"

The uninstall works only when no connections are using JavaScript stored programs. If there are connections, the procedure fails with an error.

To remove the component, run the following:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_js_lang';
```

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)