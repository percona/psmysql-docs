# Troubleshoot js_lang procedures and functions

--8<--- "tech.preview.md:5:5"

The component includes a set of User-Defined Functions (UDFs) that retrieve and clear information about the last JS error that occurred in the current connection for the current user. This information updates each time a JS error occurs for the current connection and user. Successful execution of JS code does not change this state. 

The following UDFs are helpful for debugging JS code.

* `JS_GET_LAST_ERROR()`: Returns the error message for the last JS error that occurred in the current connection for the current user.

* `JS_GET_LAST_ERROR_INFO()`: Provides detailed information about the last JS error that occurred in the current connection for the current user including the error message, the exact line and column where the problem occurred, and the stack trace if available.

* `JS_CLEAR_LAST_ERROR()`: Resets the information about the last JS error for the current connection and user, as if no error had occurred.

To terminate a connection or statement executing a JS routine, you can take immediate action to abort the execution, ensuring that any unintended operations can be swiftly stopped.

This functionality is crucial for managing and controlling the execution of routines, ensuring that any unintended or potentially harmful operations can be swiftly terminated to maintain the stability and performance of the database environment.

If the `MAX_EXECUTION_TIME` timeout is exceeded for a statement running a JS routine, the execution aborts execution without much delay. You can use this option to limit the execution time of a JS routine that's performing a long computation.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [js_lang component system variables](js-lang-variables.md)