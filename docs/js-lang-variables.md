# js_lang component system variables

--8<--- "tech.preview.md:5:5"

The following sections describe the system variables available in the js_lang component.

## js_lang system variables

The following js_lang system variables are available:

| Variable name | Description |
|---|---|
| [js_lang.max_mem_size](#js_langmax_mem_size) | Maximum memory size for JS routines |
| [js_lang.max_mem_size_hard_limit_factor](#js_langmax_mem_size_hard_limit_factor) | Maximum memory size hard limit factor |

The following variables are described in detail:

### `js_lang.max_mem_size`

| Options | Description |
| --- | --- |
| Command-line | --js-lang.max-mem-size=value |
| Dynamic | Yes |
| Scope | Global |
| Data type | Numeric |
| Default | 8388608 (8 MB) |
| Minimum value | 3145728 (3 MB) |
| Maximum value | 1073741824 (1 GB) |
| Block size | 1024 bytes |

This variable sets the soft memory allocation limit for JS routines. The component configures V8 with this limit. Since every JS execution (or session, depending on the isolation mode) creates a V8 environment, this limit prevents a single poorly written script or a loop from consuming all the server's physical memory.

Values are rounded down to the nearest multiple of 1024 bytes (block size). V8 requires a minimum heap size to start, which is typically around 10 MB.

V8 behavior with the soft limit:

The soft limit is a threshold that triggers V8's garbage collection (GC) process. When memory usage approaches the soft limit configured by this variable, V8 starts incremental marking in the background to identify objects that can be freed. This background GC runs without pausing JS execution. If the soft limit is reached or exceeded and GC cannot free enough memory, V8 Isolate Termination is triggered, stopping JS execution and returning a "Memory limit exceeded" error to the MySQL client.

Relationship to hard limit:

The hard limit is calculated as `js_lang.max_mem_size * js_lang.max_mem_size_hard_limit_factor` and is configured separately using the [`js_lang.max_mem_size_hard_limit_factor`](#js_langmax_mem_size_hard_limit_factor) variable. When the hard limit is reached, V8 performs a "last resort" garbage collection, stopping all execution to attempt to free every possible byte of memory. If this final GC cannot free enough memory, V8 triggers out-of-memory (OOM) handling, which terminates the mysqld process and causes a server exit. The hard limit is disabled by default (factor = 0) because it causes a server exit.

This variable is dynamic and can be changed at runtime using the `SET` statement. The updated value is applied to new V8 isolate contexts created after the change. Sessions that are already running may not be affected until the next time a context is initialized.

An example of setting the variable:

```sql
SET GLOBAL js_lang.max_mem_size = 16777216;
```

This sets the limit to 16 MB. To make the change persistent across server restarts, add this setting to your configuration file:

```ini
[mysqld]
js_lang.max_mem_size = 16777216
```

### `js_lang.max_mem_size_hard_limit_factor`

| Options | Description |
| --- | --- |
| Command-line | --js-lang.max-mem-size-hard-limit-factor=value |
| Dynamic | No |
| Scope | Global |
| Data type | Numeric |
| Default | 0 |
| Minimum value | 0 |
| Maximum value | 1024 |

This variable controls the hard limit for JS routine memory allocation. When set to a non-zero value, the component calculates the hard limit as `js_lang.max_mem_size * js_lang.max_mem_size_hard_limit_factor` in bytes.

When a JS session's memory usage reaches the hard limit threshold, V8 performs a "last resort" garbage collection, stopping all execution to attempt to free every possible byte of memory. If this final GC cannot free enough memory, V8 triggers out-of-memory (OOM) handling, which terminates the mysqld process and causes a server exit. This is different from the soft limit behavior, where V8 Isolate Termination stops only the JS execution and returns an error to the client.

When set to `0` (the default), the component does not set an explicit V8 memory limit. Instead, V8 uses the default limit, which is typically greater than 1 GB). The default V8 limt avoids a server exit from an abrupt out-of-memory (OOM) scenario.

!!! warning

    Allocating more than 1 GB of memory is not safe, as this allocation can exceed V8's default hard limit and cause the server to exit.

A non-zero value enforces the V8 hard limit. This setting ensures that the hard memory limit will never be exceeded, at the price of process abort. Note that large single allocations that exceed this limit will cause server exit.

You should be aware that:

* V8 may abort the process if a single allocation attempt exceeds the limit and garbage collection cannot free enough memory.

* Changing this variable requires a server restart

In earlier versions, the component set the V8 memory limit to `js_lang.max_mem_size * 4` bytes by default. This setting worked well for detecting memory limit violations with small allocations, but failed when a single huge allocation exceeded the limit. Attempting to allocate more than `js_lang.max_mem_size * 4` bytes in one operation could cause the server to crash because V8 aborts the process when an allocation exceeds its memory limit and garbage collection cannot help.

!!! note

    This variable relates to the internal heap limit for JS routines and works in conjunction with `js_lang.max_mem_size`. For more information about memory limits and troubleshooting, see [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md).

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)

