# Audit log filter functions, options and variables

All audit log functions return a string value that shows the operation result. The
string "OK" indicates successful completion. "ERROR: message" indicates failure
with an accompanying error message.

Audit‑log functions always accept and return strings in `utf8mb4`.

!!! warning "Plugin compatibility"

    **Important**: The audit log filter functions, options, and variables are designed specifically for the `audit log filter` plugin.
    They cannot be used with the `audit log` plugin. These functions are
    designed to operate on specific data types and structures that are unique to
    the `audit log filter` plugin. Attempting to use these functions with the `audit log` plugin can result in errors because the functions would
    operate on the wrong data format.

The following sections describe the audit log filter plugin functionality organized by purpose:

## Plugin management

Controls how the audit log filter plugin is loaded and configured.

| Name | Type | Description |
| --- | --- | --- |
| [`audit-log-filter`](#audit-log-filter) | Option | Plugin loading behavior |
| [`audit_log_filter_database`](#audit_log_filter_database) | Variable | Database for configuration tables |
| [`audit_log_filter_disable`](#audit_log_filter_disable) | Variable | Disable plugin logging |

## Filter management

Create, configure, and manage audit filters and user assignments.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_filter_set_filter()`](#audit_log_filter_set_filterfilter_name-definition) | Function | Create or update filters |
| [`audit_log_filter_remove_filter()`](#audit_log_filter_remove_filterfilter_name) | Function | Remove filters |
| [`audit_log_filter_set_user()`](#audit_log_filter_set_useruser_name-filter_name) | Function | Assign filters to users |
| [`audit_log_filter_remove_user()`](#audit_log_filter_remove_useruser_name) | Function | Remove user filter assignments |
| [`audit_log_filter_flush()`](#audit_log_filter_flush) | Function | Apply filter changes |
| [`audit_log_filter_filter_id`](#audit_log_filter_filter_id) | Variable | Current session filter ID |

## Log reading and navigation

Read audit logs and navigate through log entries.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_read()`](#audit_log_read) | Function | Read audit log entries |
| [`audit_log_read_bookmark()`](#audit_log_read_bookmark) | Function | Get current log position |
| [`audit_log_filter_read_buffer_size`](#audit_log_filter_read_buffer_size) | Variable | Read buffer size |

## Log file management

Configure log file location, rotation, and maintenance.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_rotate()`](#audit_log_rotate) | Function | Manually rotate log files |
| [`audit_log_filter_file`](#audit_log_filter_file) | Variable | Log file name and location |
| [`audit_log_filter_max_size`](#audit_log_filter_max_size) | Variable | Maximum total log size |
| [`audit_log_filter_rotate_on_size`](#audit_log_filter_rotate_on_size) | Variable | Auto-rotation size threshold |
| [`audit_log_filter_prune_seconds`](#audit_log_filter_prune_seconds) | Variable | Log file retention time |

## Output format and destination

Configure how audit logs are formatted and where they are sent.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_filter_format`](#audit_log_filter_format) | Variable | Log format (JSON, XML) |
| [`audit_log_filter_format_unix_timestamp`](#audit_log_filter_format_unix_timestamp) | Variable | Include UNIX timestamps |
| [`audit_log_filter_handler`](#audit_log_filter_handler) | Variable | Output destination (FILE/SYSLOG) |
| [`audit_log_filter_syslog_tag`](#audit_log_filter_syslog_tag) | Variable | Syslog tag |
| [`audit_log_filter_syslog_priority`](#audit_log_filter_syslog_priority) | Variable | Syslog priority |

## Performance and buffering

Optimize audit logging performance and memory usage.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_filter_buffer_size`](#audit_log_filter_buffer_size) | Variable | Write buffer size |
| [`audit_log_filter_strategy`](#audit_log_filter_strategy) | Variable | Logging strategy |

## Encryption and security

Configure encryption for audit log files and manage encryption keys.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_encryption_password_get()`](#audit_log_encryption_password_getkeyring_id) | Function | Get encryption password |
| [`audit_log_encryption_password_set()`](#audit_log_encryption_password_setnew_password) | Function | Set encryption password |
| [`audit_log_filter_encryption`](#audit_log_filter_encryption) | Variable | Encryption type |
| [`audit_log_filter_key_derivation_iterations_count_mean`](#audit_log_filter_key_derivation_iterations_count_mean) | Variable | Key derivation iterations |
| [`audit_log_filter_password_history_keep_days`](#audit_log_filter_password_history_keep_days) | Variable | Password retention period |

## Compression

Configure compression for audit log files.

| Name | Type | Description |
| --- | --- | --- |
| [`audit_log_filter_compression`](#audit_log_filter_compression) | Variable | Compression type |


## Plugin management

### `audit-log-filter`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --audit-log-filter[=value]|
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | Enumeration                     |
| Default      | ON                              |

This option determines how, at startup, the server loads the `audit_log_filter`
plugin. The plugin must be registered.

The valid values are the following:

* `ON` - Load the plugin if it is available

* `OFF` - Do not load the plugin

* `FORCE` - Load the plugin even if it has been disabled

* `FORCE_PLUS_PERMANENT` - Load the plugin and prevent it from being unloaded

### `audit_log_filter_database`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-database |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | mysql  |

This variable defines the database name where the audit log filter plugin stores its
configuration tables. This is a read-only variable that you must set at system startup.
The database name cannot exceed 64 characters or be `NULL`.

An invalid database name prevents the audit log filter plugin from functioning.

### `audit_log_filter_disable`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-disable |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Boolean  |
| Default | OFF |

This variable disables the plugin logging for all connections and any sessions.

This variable requires the user account to have `SYSTEM_VARIABLES_ADMIN` and
`AUDIT_ADMIN` privileges.



## Filter management

### audit_log_filter_set_filter(filter_name, definition)

This function, when provided with a filter name and definition, adds the filter.

The new filter has a different filter ID. Generates an error if the filter name
exists.

#### Parameters

* `filter_name` - a selected filter name as a string.

* `definition` - the filter definition as a `JSON` value. The `JSON` structure defines
  the filtering rules, including which events to log, block, or exclude. Example:
  `{"filter": {"log": true, "block": false}}`


#### Returns

This function returns either an `OK` for success or an error message for failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SET @filter = '{ "filter": { "log": true }}'
```

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_set_filter('filter-name', @filter);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------------+
    | audit_log_filter_set_filter('filter-name', @filter)  |
    +-------------------------------------------------------------+
    | OK                                                          |
    +-------------------------------------------------------------+
    ```

### audit_log_filter_remove_filter(filter_name)

This function removes the selected filter from the current set of filters.

When you remove a filter, any user accounts that were assigned to that filter are
affected as follows:

* The filter assignments for those user accounts are removed from the `audit_log_filter_user` table

* For user accounts currently in active sessions, the filter is immediately
  detached and they will use the default filter behavior

* For user accounts not in active sessions, those user accounts will use the default filter behavior when they establish new connections in the future

#### Parameters

`filter_name` - a selected filter name as a string.


#### Returns

This function returns either an `OK` for success or an error message for failure.

If the filter name does not exist, no error is generated.


#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_remove_filter('filter-name');
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------------+
    | audit_log_filter_remove_filter('filter-name')  |
    +------------------------------------------------+
    | OK                                             |
    +------------------------------------------------+
    ```

### audit_log_filter_set_user(user_name, filter_name)

This function assigns the filter to the selected user account.

!!! note

    Starting from Percona Server for MySQL 8.0.42, `audit_log_filter_set_user()` accepts account names with wildcard characters (`'%'` and `'_'`) in the host part. For example, you can use `'usr1@%'`, `'usr2%192.168.0.%'`, or `'usr3@%.mycorp.com'.

A user account can only have one filter. If the user account already has a filter, this function replaces the current filter. The behavior depends on the user's session status:

* Active sessions: The filter change does not take effect immediately. The current session continues using the old filter.

* Future connections: When the user account establishes a new connection, the new filter will be applied.

The user name, `%`, is the default account. The filter assigned to `%` is used
by any user account without a defined filter.

#### Parameters

* `user_name` - a selected user name in either the `user_name`@`host_name` format or `%`.

* `filter_name` - a selected filter name as a string.

#### Returns

This function returns either an `OK` for success or an error message for failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_set_user('user-name@localhost', 'filter-name');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------------------+
    | audit_log_filter_set_user('user-name@localhost', 'filter-name')  |
    +-------------------------------------------------------------------+
    | OK                                                                |
    +-------------------------------------------------------------------+
    ```

### audit_log_filter_remove_user(user_name)

This function removes the assignment of a filter from the selected user account.

If the user account is in a current session, they are not affected. New sessions
for this user account use the default account filter or are not logged.

If the user-name is `%`, the default account filter is removed.

#### Parameters

`user_name` - a selected user name in either the `user_name`@`host_name` format or `%`.


#### Returns

This function returns either an `OK` for success or an error message for failure.

If the user_name has no filter assigned, no error is generated.


#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_remove_user('user-name@localhost');
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------------------+
    | audit_log_filter_remove_user('user-name@localhost')  |
    +------------------------------------------------------+
    | OK                                                   |
    +------------------------------------------------------+
    ```

### audit_log_filter_flush()

This function updates the audit log filter tables and makes any changes
operational.

Modifying the audit log filter tables directly with `INSERT`, `UPDATE`, or
`DELETE` does not implement the modifications immediately. The tables must be
flushed to have those changes take effect.

This function forces reloading all filters and should only be used if someone
has modified the tables directly.

!!! important

    Avoid using this function. This function performs an operation that is similar
    to uninstalling and reinstalling the plugin. Filters are detached from all
    current sessions. To restart logging, the current sessions must either
    disconnect and reconnect or do a change-user operation.

#### Parameters

None.

#### Returns

This function returns either an `OK` for success or an error message for failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_filter_flush();
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------------+
    | audit_log_filter_flush() |
    +--------------------------+
    | OK                       |
    +--------------------------+
    ```

### `audit_log_filter_filter_id`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-file-id |
| Dynamic | No  |
| Scope | Session  |
| Data type | Integer  |
| Default | 0  |
| Minimum value | 0 |
| Maximum value | 4292967295 |

This variable defines the internal ID of the audit log filter in the current
session.

The default value is 0 (zero) - the session has no assigned filter.

## Log reading and navigation

### audit_log_read()

If the audit log filter format is JSON, this function reads the audit log and
returns an array of the audit events as a JSON string. Generates an error if the
format is not JSON.

#### Parameters

None. If the start position is not provided, the read continues from the current
position.

Optional: You can specify a starting position for the read with `start` or a
`timestamp` and an `id`. Both items are considered a bookmark and can be used to
identify an event. You must include both (`timestamp` and `id`) or an error is
generated. If the `timestamp` does not include a `time` section, the function
assumes the time is `00:00`.

You can also provide a `max_array_length` to limit the number of log events.

Call [`audit_log_read_bookmark()`](#audit_log_read_bookmark) to return the most
recently written event.

#### Returns

This function returns a string of a `JSON` array of the audit events, or a `JSON`
NULL value. Returns `NULL` and generates an error if the call fails.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read();
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------------------------------------------+
    | audit_log_read()                                                             |
    +------------------------------------------------------------------------------+
    | [{"timestamp" : "2023-06-02 09:43:25", "id": 10, "class":"connection",      |
    |  "connection_id": 1, "user": "root@localhost", "host": "localhost",         |
    |  "command_class": "select", "sqltext": "SELECT * FROM users"}]             |
    +------------------------------------------------------------------------------+
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read(audit_log_read_bookmark());
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------------------------------------------+
    | audit_log_read(audit_log_read_bookmark())                                   |
    +------------------------------------------------------------------------------+
    | [{"timestamp" : "2023-06-02 09:43:25", "id": 10, "class":"connection",      |
    |  "connection_id": 1, "user": "root@localhost", "host": "localhost",         |
    |  "command_class": "select", "sqltext": "SELECT * FROM users"}]             |
    +------------------------------------------------------------------------------+
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read('{"timestamp": "2023-06-02 09:43:25", "id": 10}');
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------------------------------------------+
    | audit_log_read('{"timestamp": "2023-06-02 09:43:25", "id": 10}')           |
    +------------------------------------------------------------------------------+
    | [{"timestamp" : "2023-06-02 09:43:25", "id": 10, "class":"connection",      |
    |  "connection_id": 1, "user": "root@localhost", "host": "localhost",         |
    |  "command_class": "select", "sqltext": "SELECT * FROM users"}]             |
    +------------------------------------------------------------------------------+
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read('{"timestamp": "2023-06-02 09:43:25", "id": 10}', 100);
```

### audit_log_read_bookmark()

This function provides a bookmark for the most recently written audit log event
as a JSON string. Generates an error if the format is not JSON.

If this function is used with [`audit_log_read()`](#audit_log_read), the
`audit_log_read()` function starts reading at that position.

#### Parameters

None.

#### Returns

This function returns a `JSON` string containing a bookmark for success or
`NULL` and an error for failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read_bookmark();
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------------------------------------+
    | audit_log_read_bookmark()                          |
    +----------------------------------------------------+
    | {"timestamp" : "2023-06-02 09:43:25", "id": 10 }   |
    +----------------------------------------------------+
    ```

### `audit_log_filter_read_buffer_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-read-buffer-size |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Unit | Bytes |
| Default | 32768  |
| Minimum value | 0 |
| Maximum value | 18446744073709551615 |

This option is only supported for JSON-format files.

The size of the buffer for reading from the audit log filter file. The `audit_log_read()` function reads only from this buffer size.

## Log file management

### audit_log_rotate()

This function rotates the current audit log file. The current file is renamed
with a timestamp suffix. A new empty log file is created with the original name.

#### Parameters

None.

#### Returns

This function returns the renamed file name.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_rotate();
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------------------+
    | audit_log_rotate()               |
    +----------------------------------+
    | audit_filter.log.20250901120000  |
    +----------------------------------+
    ```

### `audit_log_filter_file`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-file |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | audit_filter.log  |

This variable defines the name of the audit log filter file. The plugin writes events to this file.

The file name can be specified in either of the following ways:

* Relative path: The plugin creates the file in the MySQL data directory

* Full path: The plugin uses the exact path you specify

If you use a full path, ensure the directory is accessible only to users who need
to view the log and the MySQL server.

For more information, see [Naming conventions](audit-log-filter-naming.md)

### `audit_log_filter_max_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-max-size |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 1GB |
| Minimum value | 0 |
| Maximum value | 18446744073709551615 |
| Unit | bytes |
| Block size | 4096 |

Defines pruning based on the combined size of the files:

The default value is 1GB.

A value of 0 (zero) disables pruning based on size.

A value greater than 0 (zero) enables pruning based on size and defines the combined size limit. When the files exceed this limit, they can be pruned.

The value is based on 4096 (block size). A value is truncated to the nearest multiple of the block size. If the value is less than 4096, the value is treated as 0 (zero).

If the values for `audit_log_filter_rotate_on_size` and `audit_log_filter_max_size` are greater than 0, we recommend that `audit_log_filter_max_size` value should be at least seven times the `audit_log_filter_rotate_on_size` value.

Pruning requires the following options:

* `audit_log_filter_max_size`
* `audit_log_filter_rotate_on_size`
* `audit_log_filter_prune_seconds`

### `audit_log_filter_rotate_on_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-rotate-on-size |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer |
| Default | 1GB  |
| Minimum value | 0 |
| Maximum value | 18446744073709551615 |
| Unit | bytes |
| Block size | 4096 |

Performs an automatic log file rotation based on the size. The default value is 1GB. If the value is greater than 0, when the log file size exceeds the value, the plugin renames the current file and opens a new log file using the original name.

If you set the value to less than 4096, the plugin does not automatically rotate the log files. You can rotate the log files manually using [`audit_log_rotate()`](#audit_log_rotate). If the value is not a multiple of 4096, the plugin truncates the value to the nearest multiple.

### `audit_log_filter_prune_seconds`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-prune-seconds |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 0  |
| Minimum value | 0 |
| Maximum value | 18446744073709551615 |
| Unit | seconds |

Defines when the audit log filter file is pruned. This pruning is based on the age of the file. The value is measured in seconds.

A value of 0 (zero) is the default and disables pruning. The maximum value is 18446744073709551615.

A value greater than 0 enables pruning. An audit log filter file can be pruned after this value.

To enable log pruning, you must set one of the following:

* Enable log rotation by setting `audit_log_filter_rotate_on_size`
* Add a value greater than 0 (zero) for either `audit_log_filter_max_size` or `audit_log_filter_prune_seconds`

## Output Format and Destination

### `audit_log_filter_format`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-format |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | NEW  |
| Available values | OLD, NEW, JSON |

This variable defines the audit log filter file format.

The available values are the
following:

* [OLD (old-style XML)](audit-log-filter-old.md)

* [NEW (new-style XML)](audit-log-filter-new.md)

* [JSON](audit-log-filter-json.md).

### `audit_log_filter_format_unix_timestamp`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-format-unix-timestamp |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Boolean  |
| Default | OFF  |

This option is only supported for JSON-format files. This option does nothing when used with other format types.

Enabling this option adds a `time` field to JSON-format files. The integer
represents the UNIX timestamp value and indicates the date and time when the
audit event was generated. Changing the value causes a file rotation because all
records must either have or do not have the `time` field. This option requires
the `AUDIT_ADMIN` and `SYSTEM_VARIABLES_ADMIN` privileges.

### `audit_log_filter_handler`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-handler |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | FILE  |

Defines where the plugin writes the audit log filter file. The following values are
available:

* `FILE` - plugin writes the log to a location specified in [`audit_log_filter_file`](#audit_log_filter_file)

* `SYSLOG` - plugin writes to the syslog

When using `SYSLOG`, the plugin uses the syslog facility and priority settings
defined by `audit_log_filter_syslog_facility` and `audit_log_filter_syslog_priority`
variables. The syslog tag is controlled by `audit_log_filter_syslog_tag`.

### `audit_log_filter_syslog_tag`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --audit-log-filter-syslog-tag= |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | String                         |
| Default      | audit-filter                         |

Specifies the syslog tag value used when writing audit log entries to syslog.
This tag appears in syslog entries to identify the source of the audit log
messages. The default value is "audit-filter".

### `audit_log_filter_syslog_priority`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-syslog-priority |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | LOG_INFO |

Defines the `priority` value for the syslog. The option has the same meaning as the appropriate parameter described in the [syslog(3) manual :octicons-link-external-16:](https://man7.org/linux/man-pages/man3/syslog.3.html).

## Performance and buffering

### `audit_log_filter_buffer_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-buffer-size |
| Dynamic | No  |
| Scope | Global  |
| Data type | Integer  |
| Default | 1048576  |
| Minimum value | 4096 |
| Maximum value | 18446744073709547520 |
| Units | bytes |
| Block size | 4096 |

This variable defines the buffer size in multiples of 4096 when logging is asynchronous. Audit events are temporarily stored in this buffer before being
written to the log file, which improves performance by reducing disk I/O operations.

The plugin initializes a single buffer and removes the buffer when the plugin terminates.

### `audit_log_filter_strategy`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-strategy |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | ASYNCHRONOUS  |

Defines the Audit Log filter plugin's logging method. The valid values are the following:

| Values | Description |
| --- | --- |
| ASYNCHRONOUS | Waits until there is buffer space available (default, best performance) |
| PERFORMANCE | Drops audit events if buffer is full (fastest, may lose events) |
| SEMISYNCHRONOUS | Allows OS caching, calls sync() periodically (balanced) |
| SYNCHRONOUS | Calls sync() after each event (safest, slowest performance) |

## Encryption and security

### audit_log_encryption_password_get(keyring_id)

This function returns the encryption password. Any keyring plugin or keyring
component can be used. The plugin or component must be enabled. If the plugin
or component is not enabled, an error occurs.

#### Parameters

`keyring_id` - optional parameter. If omitted, the function returns the current
encryption password. If provided, specify the keyring ID to retrieve a specific
encryption password (current or archived). The keyring ID is a string identifier
used by the keyring system to distinguish between different stored passwords.

#### Returns

This function returns a JSON object with the following structure:
- `password`: The encryption password as a string
- `iterations`: The number of iterations used for password derivation (integer)

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_encryption_password_get();
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------------------------+
    | audit_log_encryption_password_get()         |
    +---------------------------------------------+
    | {"password":"passw0rd","iterations":5689}   |
    +---------------------------------------------+
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_encryption_password_get('current_key');
```

#### Security considerations

This function returns sensitive encryption passwords. Ensure proper access controls
are in place. The returned password should be handled securely and not logged or
stored in plain text. Only users with appropriate privileges should execute this
function.

### audit_log_encryption_password_set(new_password)

This function sets the encryption password and stores the new password in the
keyring.

#### Parameters

`new_password` - the new password as a string. The maximum length is 766 bytes.

#### Returns

This function returns a string. An `OK` indicates a success. `ERROR` indicates
a failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_encryption_password_set('passw0rd');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------------------------+
    | audit_log_encryption_password_set('passw0rd')       |
    +-----------------------------------------------------+
    | OK                                                  |
    +-----------------------------------------------------+
    ```

#### Security considerations

This function stores sensitive encryption passwords in the keyring. Ensure the
password meets security requirements (sufficient length, complexity). The password
is used to encrypt audit log files and should be kept secure. Only users with
appropriate privileges should execute this function.

### `audit_log_filter_encryption`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-encryption |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | NONE  |
| Valid values | NONE or AES |

This variable defines the encryption type for the audit log filter file. The
values can be either of the following:

* `NONE` - the default value, no encryption
* `AES` - uses AES-256 encryption for audit log files

When encryption is enabled, the plugin uses AES-256 encryption to secure audit log
files. The encryption keys are managed through the MySQL keyring system. Ensure
that a keyring plugin is installed and configured before enabling encryption.

### `audit_log_filter_key_derivation_iterations_count_mean`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-key-derivation-iterations-count-mean |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 60000  |
| Minimum value | 1000 |
| Maximum value | 1000000 |

Defines the average number of iterations used when deriving encryption keys from
passwords. The actual iteration count is randomly generated and varies by no more
than 10% from this mean value.

Higher values provide better security but require more CPU time for key derivation.
The default value of 60000 provides a good balance between security and performance.
For high-security environments, consider increasing this value to 100000 or higher.

### `audit_log_filter_password_history_keep_days`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-password-history-keep-days |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 0  |
| Minimum value | 0 |
| Maximum value | 18446744073709551615 |
| Unit | days |

Defines when passwords may be removed and measured in days.

Encrypted log files have passwords stored in the keyring. The plugin also stores a password history. A password does not expire, despite being past the value, in case the password is used for rotated audit logs. The operation of creating a password also archives the previous password.

The default value is 0 (zero). This value disables the expiration of passwords. Passwords are retained forever.

If the plugin starts and encryption is enabled, the plugin checks for an audit log filter encryption password. If a password is not found, the plugin generates a random password.

Call [audit_log_encryption_password_set(new_password)](#audit_log_encryption_password_setnew_password) to set a specific password.

## Compression

### `audit_log_filter_compression`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter-compression |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | NONE  |
| Valid values | NONE or GZIP |

This variable defines the compression type for the audit log filter file. The
values can be either `NONE`, the default value and file has no compression, or
`GZIP`.

## Audit log filter status variables

The audit log filter plugin exposes status variables. These variables provide information on the operations.

| Name | Description |
| -- | --- |
| `audit_log_filter_current_size` | The current size of the audit log filter file. If the log is rotated, the size is reset to 0. |
| `audit_log_filter_direct_writes` | Identifies when the `log_strategy_type` = ASYNCHRONOUS and messages bypass the write buffer and are written directly to the log file  |
| `audit_log_filter_max_drop_size` | In the performance logging mode, the size of the largest dropped event. |
| `audit_log_filter_events` | The number of audit log filter events |
| `audit_log_filter_events_filtered` | The number of filtered audit log filter plugin events |
| `audit_log_filter_events_lost` | If the event is larger than the available audit log filter buffer space, the event is lost |
| `audit_log_filter_events_written` | The number of audit log filter events written |
| `audit_log_filter_total_size` | The total size of the events written to all audit log filter files. The number increases even when a log is rotated |
| `audit_log_filter_write_waits` | In the asynchronous logging mode, the number of times an event waited for space in the audit log filter buffer |
