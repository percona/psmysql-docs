# js_lang stored function or procedure

--8<--- "tech.preview.md:5:5"

Once the component's installed, you can write stored functions and procedures in JavaScript. The syntax looks like this:

```{.text .no-copy}
CREATE
    [DEFINER = user]
    FUNCTION [IF NOT EXISTS] sp_name ([func_parameter[,...]])
    RETURNS type
    LANGUAGE JS [other-func-characteristic ...] AS routine_body

CREATE
    [DEFINER = user]
    PROCEDURE [IF NOT EXISTS] sp_name ([proc_parameter[,...]])
    LANGUAGE JS [other-proc-characteristic ...] AS routine_body

routine_body:
		text_string_literal | dollar_quoted_string
```

Use the `LANGUAGE JS` clause when creating a routine.

End each statement with a semicolon. Without a statement terminator, the client sends the statements as one statement and the server returns `ERROR 1064`.

When binary logging is enabled, `CREATE FUNCTION` fails with `ERROR 1418` unless the function declares `DETERMINISTIC`, `NO SQL`, or `READS SQL DATA`. You can set `log_bin_trust_function_creators` instead.

```sql
CREATE FUNCTION f1(n INT) RETURNS INT LANGUAGE JS DETERMINISTIC AS $$
    return n*42;
$$;

CREATE PROCEDURE p1(a INT, b INT, OUT r INT) LANGUAGE JS AS $$
  r = a * b;
$$;

SELECT f1(2);
CALL p1(6, 7, @r);
SELECT @r;
```

??? example "Expected result"

    ```{.text .no-copy}
    +-------+
    | f1(2) |
    +-------+
    |    84 |
    +-------+
    ```

    ```{.text .no-copy}
    +------+
    | @r   |
    +------+
    |   42 |
    +------+
    ```

You can modify or delete stored programs in JS by using the standard `ALTER PROCEDURE/FUNCTION` and `DROP PROCEDURE/FUNCTION` statements. These statements do not require the `CREATE_JS_ROUTINE` privilege.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang privileges](js-lang-privileges.md)
- [js_lang component system variables](js-lang-variables.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)

