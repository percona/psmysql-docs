# Audit log filter functions, options, and variables

The following sections describe the [functions](#audit-log-filter-functions), [options, and variables](#audit-log-filter-options-and-variables) available in the audit log filter component.

## Audit log filter functions

The following audit log filter functions are available.

| Function name |
| --- | 
| [audit_log_encryption_password_get(keyring_id)](#audit_log_encryption_password_getkeyring_id) |
| [audit_log_encryption_password_set(new_password)](#audit_log_encryption_password_setnew_password) |
| [audit_log_filter_flush()](#audit_log_filter_flush) |
| [audit_log_read()](#audit_log_read) |
| [audit_log_read_bookmark()](#audit_log_read_bookmark) |
| [audit_log_session_filter_id()](#audit_log_session_filter_id)|
| [audit_log_filter_remove_filter(filter_name)](#audit_log_filter_remove_filterfilter_name) |
| [audit_log_filter_remove_user(user_name)](#audit_log_filter_remove_useruser_name) |
| [audit_log_rotate()](#audit_log_rotate) |
| [audit_log_filter_set_filter(filter_name, definition)](#audit_log_filter_set_filterfilter_name-definition) |
| [audit_log_filter_set_user(user_name, filter_name)](#audit_log_filter_set_useruser_name-filter_name)|

### audit_log_encryption_password_get(keyring_id)

This function returns the encryption password. Any keyring component or keyring component can be used, but the component or component must be enabled. If the component or component is not enabled, an error occurs.

#### Parameters

`keyring_id` - If the function does not contain a keyring_id, the function returns the current encryption password. You can also request a specific encryption password with the keyring ID of either the current password or an archived password.

#### Returns

This function returns a JSON object containing the password, iterations count used by the password.

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

### audit_log_encryption_password_set(new_password)

This function sets the encryption password and stores the new password in the keyring. 

#### Parameters

`password` - the password as a string. The maximum length is 766 bytes.

#### Returns

This function returns a string. An `OK` indicates a success. `ERROR` indicates a failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_encryption_password_set(passw0rd);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------------------------+
    | audit_log_encryption_password_set(passw0rd)         |
    +-----------------------------------------------------+
    | OK                                                  |
    +-----------------------------------------------------+
    ```

### audit_log_filter_flush()

This function updates the audit log filter tables and makes any changes operational. 

Modifying the audit log filter tables directly with `INSERT`, `UPDATE`, or `DELETE` does not implement the modifications immediately. The tables must be flushed to have those changes take effect. 

This function forces reloading all filters and should only be used if someone has modified the tables directly. 

!!! important

    Avoid using this function. This function performs an operation that is similar to uninstalling and reinstalling the component. Filters are detached from all current sessions. To restart logging, the current sessions must either disconnect and reconnect or do a change-user operation. 

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

### audit_log_read()

If the audit log filter format is JSON, this function reads the audit log and returns an array of the audit events as a JSON string. Generates an error if the format is not JSON.

#### Parameters

None. If the start position is not provided, the read continues from the current position. 

Optional: You can specify a starting position for the read with `start` or a `timestamp` and an `id`, both items are considered a bookmark and can be used to identify an event. You must include both (`timestamp` and `id`) or an error is generated. If the `timestamp` does not include a `time` section, the function assumes  the time is `00:00`.

You can also provide a `max_array_length` to limit the number of log events.

Call[`audit_log_read_bookmark()`](#audit_log_read_bookmark) to return the most recently written event.

#### Returns

This function returns a string of a JSON array of the audit events or a JSON NULL value. Returns `NULL` and generates an error if the call fails.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read(audit_log_read_bookmark());
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------------------------------------------+
    | audit_log_read(audit_log_read_bookmark())                                   |
    +------------------------------------------------------------------------------+
    | [{"timestamp" : "2023-06-02 09:43:25", "id": 10,"class":"connection",]       |
    +------------------------------------------------------------------------------+
    ```

### audit_log_read_bookmark()

This function provides a bookmark for the most recently written audit log event as a JSON string. Generates an error if the format is not JSON.

If this function is used with [`audit_log_read()](#audit_log_read), the `audit_log_read()` function starts reading at that position.

#### Parameters

None.

#### Returns

This function returns a `JSON` string containing a bookmark for success or  `NULL` and an error for failure.

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

### `audit_log_session_filter_id()`

This function returns the internal ID of the audit log filter in the current session.

Returns 0 (zero) if the session has no assigned filter.

### audit_log_filter_remove_filter(filter_name)

This function removes the selected filter from the current set of filters.

If user accounts are assigned the selected filter, the user accounts are no longer filtered. The user accounts are removed from `audit_log_user`. If the user accounts are in a current session, they are detached from the selected filter and no longer logged.

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

### audit_log_filter_remove_user(user_name)

This function removes the assignment of a filter from the selected user account.

If the user account is in a current session, they are not affected. New sessions for this user account use the default account filter or are not logged.

If the user name is `%`, the default account filter is removed.

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

### audit_log_rotate()

#### Parameters

None.

#### Returns

This function returns the renamed file name.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_rotate();
```

### audit_log_filter_set_filter(filter_name, definition)

This function, when provided with a filter name and definition, adds the filter. 

The new filter has a different filter ID. Generates an error if the filter name exists.

#### Parameters

* `filter_name` - a selected filter name as a string.

* `definition` - Defines the definition as a JSON value.


#### Returns

This function returns either an `OK` for success or an error message for failure.

#### Example

```{.bash data-prompt="mysql>"}
mysql> SET @filter = '{ "filter_name": { "log": true }}'
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

### audit_log_filter_set_user(user_name, filter_name)

This function assigns the filter to the selected user account.

Starting from Percona Server for MySQL 8.4.4, the audit_log_filter_set_user() UDF accepts account names with wildcard characters (`'%'` and `'_'`) in the host part. For example, you can use `‘usr1@%'`, `‘usr2%192.168.0.%’`, or `'usr3@%.mycorp.com'`.

A user account can only have one filter. If the user account already has a filter, this function replaces the current filter. If the user account is in a current session, nothing happens. When the user account connects again the new filter is used.

The user name, `%`, is the default account. The filter assigned to `%` is used by any user account without a defined filter.

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

## Audit log filter options and variables

| Name |
| --- |
| [`audit_log_filter.buffer_size`](#audit_log_filterbuffer_size) |
| [`audit_log_filter.compression`](#audit_log_filtercompression) |
| [`audit_log_filter.database`](#audit_log_filterdatabase) |
| [`audit_log_filter.disable`](#audit_log_filterdisable) |
| [`audit_log_filter.encryption`](#audit_log_filterencryption) |
| [`audit_log_filter.file`](#audit_log_filterfile) |
| [`audit_log_filter.format`](#audit_log_filterformat) |
| [`audit_log_filter.format_unix_timestamp`](#audit_log_filterformat_unix_timestamp) |
| [`audit_log_filter.handler`](#audit_log_filterhandler) |
| [`audit_log_filter.key_derivation_iterations_count_mean`](#audit_log_filterkey_derivation_iterations_count_mean) |
| [`audit_log_filter.max_size`](#audit_log_filtermax_size) |
| [`audit_log_filter.password_history_keep_days`](#audit_log_filterpassword_history_keep_days) |
| [`audit_log_filter.prune_seconds`](#audit_log_filterprune_seconds) |
| [`audit_log_filter.read_buffer_size`](#audit_log_filterread_buffer_size) |
| [`audit_log_filter.rotate_on_size`](#audit_log_filterrotate_on_size) |
| [`audit_log_filter.strategy`](#audit_log_filterstrategy) |
| [`audit_log_filter.syslog_tag`](#audit_log_filtersyslog_tag) |
| [`audit_log_filter.syslog_priority`](#audit_log_filtersyslog_priority) |

### `audit_log_filter.buffer_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.buffer-size |
| Dynamic | No  |
| Scope | Global  |
| Data type | Integer  |
| Default | 1048576  |
| Minimum value | 4096 |
| Maximum value | 18446744073709547520 |
| Units | byes |
| Block size | 4096 |

This read-only variable defines the buffer size in multiples of `4096` when logging is asynchronous. Events are temporarily stored in this buffer before being written to the log file. This variable requires a server restart to change.

The component initializes a single buffer and removes the buffer when the component terminates.

### `audit_log_filter.compression`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.compression |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | NONE  |
| Valid values | NONE or GZIP |

This read-only variable defines the compression type for the audit log filter file. This variable requires a server restart to change. The values can be either `NONE`, the default value and file has no compression, or `GZIP`.


### `audit_log_filter.database` 

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.database |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | mysql  |

This read-only variable defines the audit_log_filter database, which stores the necessary tables. 

The database name cannot exceed 64 characters or be `NULL`. An invalid database name prevents the use of the audit log filter component.

This variable requires a server restart to change.

### `audit_log_filter.disable`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.disable |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Boolean  |
| Default | OFF |

This variable disables the component logging for all connections and any sessions. 

This variable requires the user account to have `SYSTEM_VARIABLES_ADMIN` and `AUDIT_ADMIN` privileges.

### `audit_log_filter.encryption`

| Option name | Description |
| --- | --- | 
| Command-line | --audit-log-filter.encryption |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | NONE  |
| Valid values | NONE or AES |

This read-only variable defines the encryption type for the audit log filter file. This variable requires a server restart to change. The values can be either of the following:

* `NONE` - the default value, no encryption

* `AES` 

### `audit_log_filter.file`

| Option name | Description |
| --- | --- | 
| Command-line | --audit-log-filter.file |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | audit_filter.log  |

This read-only variable defines the filename of the audit log filter file. The component writes events to this file. This variable requires a server restart to change.

The filename can be either of the following:

* a relative path name - the component looks for this file in the data directory

* a full path name - the component uses the given value
  
If you use a full path name, ensure the directory is accessible only to users who need to view the log and the server.

For more information, see [Naming conventions](audit-log-filter-naming.md)

### `audit_log_filter.format`

| Option name | Description |
| --- | --- | 
| Command-line | --audit-log-filter.format |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | NEW  |
| Available values | OLD, NEW, JSON |

This read-only variable defines the audit log filter file format. This variable requires a server restart to change.

The available values are the following: 

* [OLD (old-style XML)](audit-log-filter-old.md)

* [NEW (new-style XML)](audit-log-filter-new.md)

* [JSON](audit-log-filter-json.md).

### `audit_log_filter.format_unix_timestamp`

| Option name | Description |
| --- | --- | 
| Command-line | --audit-log-filter.format-unix-timestamp |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Boolean  |
| Default | OFF  |

This option is only supported for JSON-format files.

Enabling this option adds a `time` field to JSON-format files. The integer represents the UNIX timestamp value and indicates the date and time when the audit event was generated. Changing the value causes a file rotation because all records must either have or do not have the `time` field. This option requires the `AUDIT_ADMIN` and `SYSTEM_VARIABLES_ADMIN` privileges.

This option does nothing when used with other format types.

### `audit_log_filter.handler`

| Option name | Description |
| --- | --- | 
| Command-line | --audit-log-filter.handler |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | FILE  |

This read-only variable defines where the component writes the audit log filter file. This variable requires a server restart to change. The following values are available:

* `FILE` - component writes the log to a location specified in [`audit_log_filter.file`](#audit_log_filterfile)

* `SYSLOG` - component writes to the syslog

### `audit_log_filter.key_derivation_iterations_count_mean`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.key-derivation-iterations-count-mean |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 60000  |
| Minimum value | 1000 |
| Maximum value | 1000000 |

Defines the mean value of iterations used by the password-based derivation routine while calculating the encryption key and iv values. A random number represents the actual iteration count and deviates no more than 10% from this value.

### `audit_log_filter.max_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.max-size |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 1GB |
| Minimum value | 0 |
| Maximum value | 18446744073709551615 |
| Unit | bytes |
| Block size | 4096 |

This variable defines the maximum combined size of all audit log files before pruning occurs.

**Default value:** 1GB

**Behavior:**
* A value of 0 (zero) disables size-based pruning
* A value greater than 0 enables pruning when the combined size of all audit log files exceeds this limit
* Values are rounded down to the nearest multiple of 4096 bytes (block size)
* Values less than 4096 are treated as 0 (disabled)

**Recommendation:** When both `audit_log_filter.rotate_on_size` and `audit_log_filter.max_size` are greater than 0, set `audit_log_filter.max_size` to at least seven times the `audit_log_filter.rotate_on_size` value.

**Pruning requirements:** To enable pruning, you must configure at least one of the following:
* [`audit_log_filter.rotate_on_size`](#audit_log_filterrotate_on_size) - enables rotation
* [`audit_log_filter.max_size`](#audit_log_filtermax_size) - enables size-based pruning  
* [`audit_log_filter.prune_seconds`](#audit_log_filterprune_seconds) - enables time-based pruning


### `audit_log_filter.password_history_keep_days`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.password-history-keep-days |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 0  |

Defines when passwords may be removed and measured in days.

Encrypted log files have passwords stored in the keyring. The component also stores a password history. A password does not expire, despite being past the value, in case the password is used for rotated audit logs. The operation of creating a password also archives the previous password.

The default value is 0 (zero). This value disables the expiration of passwords. Passwords are retained forever. 

If the component starts and encryption is enabled, the component checks for an audit log filter encryption password. If a password is not found, the component generates a random password.

Call [audit_log_encryption_password_set(new_password)](#audit_log_encryption_password_setnew_password) to set a specific password.


### `audit_log_filter.prune_seconds`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.prune-seconds |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Default | 0  |
| Minimum value | 0 |
| Maximum value | 1844674073709551615 |
| Unit | seconds |

Defines when the audit log filter file is pruned. This pruning is based on the age of the file. The value is measured in seconds. 

A value of 0 (zero) is the default and disables pruning. The maximum value is 18446744073709551615.

A value greater than 0 enables pruning. An audit log filter file can be pruned after this value.

To enable log pruning, you must set one of the following:

* Enable log rotation by setting [`audit_log_filter.rotate_on_size`](#audit_log_filterrotate_on_size)
* Add a value greater than 0 (zero) for either [`audit_log_filter.max_size`](#audit_log_filtermax_size) or [`audit_log_filter.prune_seconds`](#audit_log_filterprune_seconds) 


### `audit_log_filter.read_buffer_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.read-buffer-size |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer  |
| Unit | Bytes |
| Default | 32768  |

This option is only supported for JSON-format files.

The size of the buffer for reading from the audit log filter file. The `audit_log_filter_read()` reads only from this buffer size.

### `audit_log_filter.rotate_on_size`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.rotate-on-size |
| Dynamic | Yes  |
| Scope | Global  |
| Data type | Integer |
| Default | 1073741824  |

Performs an automatic log file rotation based on the size. The default value is 1073741824. If the value is greater than 0, when the log file size exceeds the value, the component renames the current file and opens a new log file using the original name.

If you set the value to less than 4096, the component does not automatically rotate the log files. You can rotate the log files manually using [`audit_log_rotate()`](#audit_log_rotate). If the value is not a multiple of 4096, the component truncates the value to the nearest multiple.

### `audit_log_filter.strategy`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.strategy |
| Dynamic | No  |
| Scope | Global  |
| Data type | Enumeration  |
| Default | ASYNCHRONOUS  |

This read-only variable defines the Audit Log filter component's logging method. This variable requires a server restart to change. The valid values are the following:

| Values | Description |
| --- | --- |
| ASYNCHRONOUS | Waits until there is outer buffer space |
| PERFORMANCE | If the outer buffer does not have enough space, drops requests |
| SEMISYNCHRONOUS | Operating system permits caching |
| SYNCHRONOUS | Each request calls `sync()` |

### `audit_log_filter.syslog_tag`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --audit-log-filter.syslog-tag=  |
| Dynamic      | No                              |
| Scope        | Global                          |
| Data type    | String                          |
| Default      | audit-filter                    |

This read-only variable specifies the syslog tag value. This variable requires a server restart to change.

### `audit_log_filter.syslog_facility`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.syslog-facility |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | LOG_USER |

This read-only variable specifies the syslog `facility` value. This variable requires a server restart to change. The option has the same meaning as the appropriate parameter described in the [syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).


### `audit_log_filter.syslog_priority`

| Option name | Description |
| --- | --- |
| Command-line | --audit-log-filter.syslog-priority |
| Dynamic | No  |
| Scope | Global  |
| Data type | String  |
| Default | LOG_INFO |

This read-only variable defines the `priority` value for the syslog. This variable requires a server restart to change. The option has the same meaning as the appropriate parameter described in the [syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

## Audit log filter status variables

The audit log filter component exposes status variables. These variables provide information on the operations.

<table border="0" cellpadding="6" cellspacing="0">
  <thead>
    <tr>
      <th style="width: 40ch; white-space: nowrap;">Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>audit_log_filter_current_size</code></td>
      <td>The current size of the audit log filter file. If the log is rotated, the size is reset to 0.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_direct_writes</code></td>
      <td>Identifies when the <code>log_strategy_type</code> = ASYNCHRONOUS and messages bypass the write buffer and are written directly to the log file.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_max_drop_size</code></td>
      <td>In the performance logging mode, the size of the largest dropped event.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_events</code></td>
      <td>The number of audit log filter events.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_events_filtered</code></td>
      <td>The number of filtered audit log filter component events.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_events_lost</code></td>
      <td>If the event is larger than the available audit log filter buffer space, the event is lost.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_events_written</code></td>
      <td>The number of audit log filter events written.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_total_size</code></td>
      <td>The total size of the events written to all audit log filter files. The number increases even when a log is rotated.</td>
    </tr>
    <tr>
      <td><code>audit_log_filter_write_waits</code></td>
      <td>In the asynchronous logging mode, the number of times an event waited for space in the audit log filter buffer.</td>
    </tr>
  </tbody>
</table>
