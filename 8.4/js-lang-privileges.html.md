> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# js_lang privileges

This feature is a [tech preview](https://docs.percona.com/percona-server/8.4/glossary.md#tech-preview). Before using this feature in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

Privileges control what users can do. You use them to give specific permissions to different users. This ability helps you keep your data secure by only allowing authorized users to access and change information in the database.

## Privileges

To create routines within a database, you must be granted the `CREATE_JS_ROUTINE` privilege and the standard `CREATE ROUTINE` privilege.

```sql
GRANT CREATE_JS_ROUTINE ON *.* TO user1@localhost;
```

If a user is granted the ability to create routines and holds the CREATE_JS_ROUTINE privilege, they are capable of creating stored functions and procedures using JS.

However, it is important to note that at this time, the creation of JS triggers or events is not supported.

## Further reading

- [js_lang stored procedure and function overview](https://docs.percona.com/percona-server/8.4/js-lang-overview.md)
- [Install js_lang component](https://docs.percona.com/percona-server/8.4/install-js-lang.md)
- [Uninstall the js_lang component](https://docs.percona.com/percona-server/8.4/uninstall-js-lang.md)
- [js_lang stored function or procedure](https://docs.percona.com/percona-server/8.4/js-lang-procedures.md)
- [js_lang component system variables](https://docs.percona.com/percona-server/8.4/js-lang-variables.md)
- [Troubleshoot js_lang procedures and functions](https://docs.percona.com/percona-server/8.4/js-lang-troubleshoot.md)
