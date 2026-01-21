# Troubleshoot js_lang procedures and functions

--8<--- "tech.preview.md:5:5"

The component includes a set of User-Defined Functions (UDFs) that retrieve and clear information about the last JS error that occurred in the current connection for the current user. This information updates each time a JS error occurs for the current connection and user. Successful execution of JS code does not change this state. 

The following UDFs are helpful for debugging JS code.

* `JS_GET_LAST_ERROR()`: Returns the error message for the last JS error that occurred in the current connection for the current user.

* `JS_GET_LAST_ERROR_INFO()`: Returns extended information about the last JS error that occurred in the current connection for the current user. In addition to the error message, it tries to provide the exact line and column where the problem occurred, as well as the stack trace if available.

* `JS_CLEAR_LAST_ERROR()`: Resets the information about the last JS error for the current connection and user, as if no error had occurred.

## Terminating JS routine execution

You can terminate the execution of a JS routine in the following ways:

1. You can kill a connection or statement that executes a JS routine using `KILL` or `KILL QUERY`, and the execution is aborted without much delay. For example, you can use `KILL QUERY` to abort a JS routine executing a long or infinite loop.

2. Exceeding the `MAX_EXECUTION_TIME` timeout (if present) for a statement that executes a JS routine aborts execution without much delay. For example, this option can be used to limit the execution time of a JS routine performing a long computation.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [js_lang component system variables](js-lang-variables.md)