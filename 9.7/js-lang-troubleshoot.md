> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Troubleshoot js_lang procedures and functions

This feature is a [tech preview](https://docs.percona.com/percona-server/9.7/glossary.html#tech-preview). Before using this feature in production, we recommend that you test restoring production from physical backups in your environment, and also use the alternative backup method for redundancy.

The component includes a set of User-Defined Functions (UDFs) that retrieve and clear information about the last JS error that occurred in the current connection for the current user. This information updates each time a JS error occurs for the current connection and user. Successful execution of JS code does not change this state.

The following UDFs are helpful for debugging JS code.

- `JS_GET_LAST_ERROR()`: Returns the error message for the last JS error that occurred in the current connection for the current user.
- `JS_GET_LAST_ERROR_INFO()`: Returns extended information about the last JS error that occurred in the current connection for the current user. In addition to the error message, it tries to provide the exact line and column where the problem occurred, as well as the stack trace if available.
- `JS_CLEAR_LAST_ERROR()`: Resets the information about the last JS error for the current connection and user, as if no error had occurred.

## Terminating JS routine execution

You can terminate the execution of a JS routine in the following ways:

1. You can kill a connection or statement that executes a JS routine using `KILL` or `KILL QUERY`, and the execution is aborted without much delay. For example, you can use `KILL QUERY` to abort a JS routine executing a long or infinite loop.
1. Exceeding the `MAX_EXECUTION_TIME` timeout (if present) for a statement that executes a JS routine aborts execution without much delay. For example, this option can be used to limit the execution time of a JS routine performing a long computation.

## Further reading

- [js_lang stored procedure and function overview](https://docs.percona.com/percona-server/9.7/js-lang-overview.html)
- [Install js_lang component](https://docs.percona.com/percona-server/9.7/install-js-lang.html)
- [Uninstall the js_lang component](https://docs.percona.com/percona-server/9.7/uninstall-js-lang.html)
- [js_lang stored function or procedure](https://docs.percona.com/percona-server/9.7/js-lang-procedures.html)
- [js_lang privileges](https://docs.percona.com/percona-server/9.7/js-lang-privileges.html)
- [js_lang component system variables](https://docs.percona.com/percona-server/9.7/js-lang-variables.html)
