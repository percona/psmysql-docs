# JS stored function or procedure

Once the component's installed, you can write stored functions and procedures in JavaScript. The syntax looks like this:

```{.text .no-copy}
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

```{.bash data-prompt="mysql>"}
mysql> CREATE FUNCTION f1(n INT) RETURNS INT LANGUAGE JS AS $$
	return n*42;
$$

mysql> CREATE PROCEDURE p1(a INT, b INT, OUT r INT) LANGUAGE JS AS $$
  r = a * b;
$$
```

You can modify or delete stored programs in JS by using the standard `ALTER PROCEDURE/FUNCTION` and `DROP PROCEDURE/FUNCTION` statements. These statements do not require the `CREATE_JS_ROUTINE` privilege.

