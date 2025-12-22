# js_lang privileges

--8<--- "tech.preview.md:5:5"

Privileges control what users can do. You use them to give specific permissions to different users. This ability helps you keep your data secure by only allowing authorized users to access and change information in the database. 

## Privileges

To create routines within a database, you must be granted the `CREATE_JS_ROUTINE` privilege and the standard `CREATE ROUTINE` privilege.

```{.bash data-prompt="mysql>"}
mysql> GRANT CREATE_JS_ROUTINE ON *.* TO user1@localhost;
```

If a user is granted the ability to create routines and holds the CREATE_JS_ROUTINE privilege, they are capable of creating stored functions and procedures using JS.

However, it is important to note that at this time, the creation of JS triggers or events is not supported.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)