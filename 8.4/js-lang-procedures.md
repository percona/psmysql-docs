> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# js_lang stored function or procedure

This feature is a [tech preview](https://docs.percona.com/percona-server/8.4/glossary.html#tech-preview). Before using this feature in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

Once the component’s installed, you can write stored functions and procedures in JavaScript. The syntax looks like this:

```
CREATE
    [DEFINER = user]
    FUNCTION [IF NOT EXISTS] sp_name ([func_parameter[,...]])
    RETURNS type
    LANGUAGE JS [other-func-characteristic ...] AS js_routine_body

CREATE
    [DEFINER = user]
    PROCEDURE [IF NOT EXISTS] sp_name ([proc_parameter[,...]])
    LANGUAGE JS [other-proc-characteristic ...] AS js_routine_body

routine_body:
        text_string_literal | dollar_quoted_string
```

Use the `LANGUAGE JS` clause when creating a routine.

```
CREATE FUNCTION f1(n INT) RETURNS INT LANGUAGE JS AS $$
    return n*42;
$$

CREATE PROCEDURE p1(a INT, b INT, OUT r INT) LANGUAGE JS AS $$
  r = a * b;
$$
```

You can modify or delete stored programs in JS by using the standard `ALTER PROCEDURE/FUNCTION` and `DROP PROCEDURE/FUNCTION` statements. These statements do not require the `CREATE_JS_ROUTINE` privilege.

## Further reading

- [js_lang stored procedure and function overview](https://docs.percona.com/percona-server/8.4/js-lang-overview.html)
- [Install js_lang component](https://docs.percona.com/percona-server/8.4/install-js-lang.html)
- [Uninstall the js_lang component](https://docs.percona.com/percona-server/8.4/uninstall-js-lang.html)
- [js_lang privileges](https://docs.percona.com/percona-server/8.4/js-lang-privileges.html)
- [js_lang component system variables](https://docs.percona.com/percona-server/8.4/js-lang-variables.html)
- [Troubleshoot js_lang procedures and functions](https://docs.percona.com/percona-server/8.4/js-lang-troubleshoot.html)
