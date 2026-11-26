> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Uninstall the js_lang component

This feature is a [tech preview](https://docs.percona.com/percona-server/8.4/glossary.md#tech-preview). Before using this feature in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

The uninstall works only when no connections are using JavaScript stored programs. If there are connections, the procedure fails with an error.

To remove the component, run the following:

```sql
UNINSTALL COMPONENT 'file://component_js_lang';
```

## Further reading

- [js_lang stored procedure and function overview](https://docs.percona.com/percona-server/8.4/js-lang-overview.md)
- [Install js_lang component](https://docs.percona.com/percona-server/8.4/install-js-lang.md)
- [js_lang stored function or procedure](https://docs.percona.com/percona-server/8.4/js-lang-procedures.md)
- [js_lang privileges](https://docs.percona.com/percona-server/8.4/js-lang-privileges.md)
- [js_lang component system variables](https://docs.percona.com/percona-server/8.4/js-lang-variables.md)
- [Troubleshoot js_lang procedures and functions](https://docs.percona.com/percona-server/8.4/js-lang-troubleshoot.md)
