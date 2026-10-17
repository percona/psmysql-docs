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

The global dynamic `js_lang.max_console_log_size` variable limits the console log size in bytes for each user and connection. It does not limit the number of messages. When the log reaches the limit, the oldest messages are discarded. The newest messages are kept.

At the minimum value of 10240, 30,000 six-character messages left 1,280 messages, from `m28721` to `m30000`. Each kept message used 8 bytes.

## Accessing console logs

The following UDFs are available for accessing and managing console logs:

* `JS_GET_CONSOLE_LOG()`: Returns a simple and plain representation of the console log for the current user and connection pair. We only show the text of the log messages in this representation (for example, no timestamps or level of log messages is shown). Each log message gets its own line and is indented two spaces for each group level.

    A failed `console.assert` prints `Assertion failed: ...`. A counter prints `default: 1`. A timer prints `t: 0.001 ms`. `%o` prints `[object Array]`. `%O` prints `#<Object>`.

* `JS_GET_CONSOLE_LOG_JSON()`: Returns a JSON representation of the console log for the current user and connection pair. Each log entry is represented by an object in a JSON array returned. Each object includes `timestamp`, `level`, and `message`. A `level` value can be `"Info"`. A group header includes `isGroupLabel` set to `true`. A message inside a group includes the group hierarchy as an array. This representation can be used for advanced processing of console log output such as filtering by severity or providing an interactive version of the log output.

* `JS_CLEAR_CONSOLE_LOG()`: Empties the console log for the current user and connection pair. It also returns the number of log entries it has removed. Note that unlike the similar `console.clear()` call, this UDF does not reset the current group stack for the console instance.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)
