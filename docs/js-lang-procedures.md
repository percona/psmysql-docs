# js_lang stored function or procedure

--8<--- "tech.preview.md:5:5"

Once the component's installed, you can write stored functions and procedures in JavaScript. The syntax looks like this:

```text
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

```sql
CREATE FUNCTION f1(n INT) RETURNS INT LANGUAGE JS AS $$
	return n*42;
$$

CREATE PROCEDURE p1(a INT, b INT, OUT r INT) LANGUAGE JS AS $$
  r = a * b;
$$
```

You can modify or delete stored programs in JS by using the standard `ALTER PROCEDURE/FUNCTION` and `DROP PROCEDURE/FUNCTION` statements. These statements do not require the `CREATE_JS_ROUTINE` privilege.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang privileges](js-lang-privileges.md)
- [js_lang component system variables](js-lang-variables.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)

