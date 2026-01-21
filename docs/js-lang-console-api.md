# js_lang Console API

--8<--- "tech.preview.md:5:5"

The js_lang component provides support for the JS Console API as described at [console.spec.whatwg.org :octicons-link-external-16:](https://console.spec.whatwg.org/). The Console API provides rudimentary support for debugging including logging, timers, and counters. Users can use methods of the JS console object to write messages to the console log, and then later inspect this log using UDFs.

!!! note
    This document does not go into details describing the behavior of each console call. Refer to the [Console API specification :octicons-link-external-16:](https://console.spec.whatwg.org/) for detailed information. You can also use [developer.mozilla.org/en-US/docs/Web/API/console :octicons-link-external-16:](https://developer.mozilla.org/en-US/docs/Web/API/console) as a more convenient reference.

## Supported logging calls

Our implementation supports the following logging calls described in the Console API specification:

* `assert()`
* `clear()`
* `debug()`
* `error()`
* `info()`
* `log()`
* `warn()`

## Supported counting, grouping, and timing calls

We also support calls implementing functionality for:

* **Counting**: `count()`, `countReset()`
* **Grouping**: `group()`, `groupCollapsed()`, `groupEnd()`
* **Timing**: `time()`, `timeLog()`, `timeEnd()`

## Unsupported calls

We do not support `trace()`, `table()`, `dir()`, and `dirxml()` calls from the specification. They can be called but do nothing.

## Log severity levels

Our implementation supports Error, Warning, Info, and Debug log severity levels. The `console.log()` and `console.timeLog()` calls use Info log severity.

## Substitution and format specifiers

For those logging calls which support substitution/format specifiers per specification, we support the following substitution/format specifiers: `%s`, `%i`, `%d`, `%f`, `%o`, `%O`, `%c`, `%%`.

## String conversion

Unless the specification says otherwise (for example, when substitution/format specifiers are used), when we convert a JS value to a string in order to add it to a console log message, we try to use a representation that is useful for debugging purposes. However, for Object values, the current result of such conversion is rather brief and far from optimal (see Node.js or browsers for example).

## Console log instances

Each user in each connection gets access to its own separate instance of the console log.

## Console log size limits

The number of console log messages that are kept for each user-connection pair is limited by the global dynamic `js_lang.max_console_log_size` variable. Once the console instance for the pair reaches this limit, we start to discard the oldest messages from the console log when new messages are added.

## Accessing console logs

The following UDFs are available for accessing and managing console logs:

* `JS_GET_CONSOLE_LOG()`: Returns a simple and plain representation of the console log for the current user and connection pair. We only show the text of the log messages in this representation (for example, no timestamps or level of log messages is shown). Each log message gets its own line and is indented according to its grouping.

* `JS_GET_CONSOLE_LOG_JSON()`: Returns a JSON representation of the console log for the current user and connection pair. Each log entry is represented by an object in a JSON array returned. This object contains all the available information about the log entry, such as the log entry timestamp, its log level, whether it belongs to a group (in which case we provide the hierarchy of the groups it belongs to in the form of an array), and whether it is a group header. This representation can be used for advanced processing of console log output such as filtering by severity or providing an interactive version of the log output.

* `JS_CLEAR_CONSOLE_LOG()`: Empties the console log for the current user and connection pair. It also returns the number of log entries it has removed. Note that unlike the similar `console.clear()` call, this UDF does not reset the current group stack for the console instance.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)
