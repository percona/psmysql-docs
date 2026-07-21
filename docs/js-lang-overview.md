# js_lang stored procedure and function overview

--8<--- "tech.preview.md:5:5"

You can use stored procedures and functions written in JS with a MySQL-compatible database. This feature helps you manage complex data processing tasks. This method improves performance. This method lets developers run complex operations faster. If you know JS, you can use your existing skills. Using stored procedures and functions reduces the work done by client applications. Using stored procedures and functions also improves overall system performance. Using stored procedures and functions helps developers process data faster. Using stored procedures and functions also makes maintenance and scaling easier. This approach is a good solution for developers who know JS.

| Benefit                            | Description                                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------------|
| Familiarity                        | Developers who already know JS can use their existing skills.                                 |
| Efficiency                         | JS can run complex data processing tasks more efficiently.                                    |
| Performance                        | Stored procedures and functions in JS improve database performance. They reduce the work done by client applications.|
| Reusability                        | You can write code once in stored procedures and functions. Then you can use that code in multiple applications.|
| Scalability                        | Using stored procedures and functions makes database operations easier to maintain and scale.  |
| Simplified Development Process     | This feature makes development easier for developers who know JS.                              |
| Integration with Client Applications| Stored procedures and functions work well with client applications. You need less additional processing.|
| Optimization                       | This feature improves overall system performance through efficient data processing.            |


## Limitations

The JS procedure parameters cannot be JS reserved words and must be [legal JS identifiers :octicons-link-external-16:](https://www.capscode.in/blog/valid-identifier-in-js).

Our implementation offers the same level of JS support as the V8 engine inside the context of a database engine. You can check out the details at [v8.dev/docs :octicons-link-external-16:](https://v8.dev/docs) and [tc39.es/ecma262 :octicons-link-external-16:](https://v8.dev/docs). Developers have access to standard operators, data types, objects (such as Math), and functions defined in the ECMAScript standard. However, objects and modules specific to Node.NS or DOM, which are only available in browsers, are not accessible. 

In a typical database environment, direct access to external files (like reading or writing files on the server's file system) is restricted. Our implementation adheres to a trusted external routine language policy, ensuring routines cannot perform operations beyond what is normally possible for database users. Consequently, file or network I/O operations are not supported within our routines.

Our system supports asynchronous JS code, but it does not work well for database routines. Since everything runs on the same thread and there is nothing to wait for asynchronously, using asynchronous code is unnecessary and not recommended.

We always run JS code in strict mode, and developers cannot disable or change this setting.

## Type conversions

SQL and JS use different data types, so the js_lang component converts values when passing SQL parameters to JS and back. SQL `NULL` values are converted to JS `null` values, and JS `null` and `undefined` values are always mapped to SQL `NULL`. When converting to JS strings, data is automatically converted from the SQL parameter's character set to `utf8mb4`.

For detailed information about type conversions, including complete conversion tables and rules, see [js_lang type conversions](js-lang-type-conversions.md).

## System variables

The js_lang component provides the following system variables for configuring JS routine execution:

| Variable name | Description | Default |
|---|---|---|
| [`js_lang.max_mem_size`](js-lang-variables.md#js_langmax_mem_size) | Maximum memory size (soft limit) for JS routines | 8 MB |
| [`js_lang.max_mem_size_hard_limit_factor`](js-lang-variables.md#js_langmax_mem_size_hard_limit_factor) | Hard limit factor for memory allocation | 0 (disabled) |

The `js_lang.max_mem_size` variable sets a soft limit on memory usage per JS environment. The `js_lang.max_mem_size_hard_limit_factor` variable (settable only at start-up) allows you to override V8's internal hard memory limit, though this is not recommended for most users.

These variables help prevent runaway scripts from consuming excessive memory or CPU time. For detailed information about each variable, including configuration options, examples, and memory limit behavior, see [js_lang component system variables](js-lang-variables.md).

## Status variables

The js_lang component provides global status variables for monitoring JS routine execution:

* **Memory usage**: `js_lang_total_heap_size`, `js_lang_peak_total_heap_size`, `js_lang_used_heap_size`, `js_lang_peak_used_heap_size`, `js_lang_external_memory_size`, `js_lang_peak_external_memory_size`
* **Contexts**: `js_lang_contexts`, `js_lang_peak_contexts`
* **Call count**: `js_lang_stored_program_call_count`

!!! note
    Status variable values are approximate as they are refreshed at Isolate creation/destruction and GC time, not on each operation.

## User-defined functions

The js_lang component includes a set of User-Defined Functions (UDFs) that retrieve and clear information about the last JS error that occurred in the current connection for the current user. This information updates each time a JS error occurs for the current connection and user. Successful execution of JS code does not change this state.

The following UDFs are helpful for debugging JS code:

* `JS_GET_LAST_ERROR()`: Returns the error message for the last JS error that occurred in the current connection for the current user.

* `JS_GET_LAST_ERROR_INFO()`: Returns extended information about the last JS error that occurred in the current connection for the current user. In addition to the error message, it tries to provide the exact line and column where the problem occurred, as well as the stack trace if available.

* `JS_CLEAR_LAST_ERROR()`: Resets the information about the last JS error for the current connection and user, as if no error had occurred.

* `JS_GET_MEMORY_USAGE_JSON()`: Returns information about memory usage by the JS environment (isolate) for the current user and connection pair, as well as total memory usage by all JS environments in the server, in the form of a JSON object. The returned object includes `local` (per-environment) and `global` (aggregated) memory statistics with heap sizes, external memory, and context counts. If there is no JS environment for the current user-connection pair, the `local` member is `null`.

For more information about using these functions for troubleshooting, see [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md).

## Console API

The js_lang component provides support for the JS Console API as described at [console.spec.whatwg.org :octicons-link-external-16:](https://console.spec.whatwg.org/). The Console API provides debugging support including logging, timers, and counters. Users can use methods of the JS console object to write messages to the console log, and then inspect this log using UDFs.

Our implementation supports logging calls (`assert()`, `clear()`, `debug()`, `error()`, `info()`, `log()`, `warn()`), counting (`count()`, `countReset()`), grouping (`group()`, `groupCollapsed()`, `groupEnd()`), and timing (`time()`, `timeLog()`, `timeEnd()`). Each user-connection pair has its own separate console log instance, with size limits controlled by the `js_lang.max_console_log_size` variable.

For detailed information about the Console API, including supported calls, format specifiers, log severity levels, and UDFs for accessing console logs, see [js_lang Console API](js-lang-console-api.md).

## Further reading

- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [js_lang component system variables](js-lang-variables.md)
- [js_lang type conversions](js-lang-type-conversions.md)
- [js_lang Console API](js-lang-console-api.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)
