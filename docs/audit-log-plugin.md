# Audit log plugin

!!! note "Deprecation notice"

    The audit log plugin is deprecated as of Percona Server for MySQL 8.4 and will be removed in a future release. The [audit log filter component](audit-log-filter-overview.md) is the recommended replacement. Migrate to the component for equivalent functionality with improved flexibility, performance, and filtering capabilities.

    For a step-by-step mapping of `audit_log_*` system variables, `audit_log_policy`, and include/exclude lists to filter JSON and component variables, see [Migrate to the audit log filter component](migrate-to-audit-log-filter-component.md).

    The deprecation affects all installations that rely on the audit log plugin for event logging, compliance auditing, or activity tracking. The plugin continues to function, but Percona plans no further development or maintenance.

    The audit log plugin and the audit log filter component use different configuration variables and options.

    * Do not use audit log filter variables, options, or configuration syntax with the deprecated audit log plugin. Mixing the two can cause startup failures, unexpected behavior, or data loss.

    * Do not install the audit log plugin and the audit log filter component at the same time.

    Audit log entries may look different from earlier 8.0 entries. The audit log plugin itself has not changed, but other server components have, and those changes affect the log output. For example, current releases log a `SELECT $$` statement each time a client connects, because the client now supports "dollar-quoted" strings. This feature did not exist in 8.0.

    Percona does not plan to modify current audit logs to match the format or content of 8.0 logs.

The Percona Audit Log Plugin monitors and logs connection and query activity on a specific server. The plugin stores the activity information in a log file.

## Install the plugin

The Audit Log plugin ships with Percona Server for MySQL but is not enabled by default. To check whether the plugin is enabled, run the following statement. The query searches for plugins with names that contain the word "audit" in the `information_schema.PLUGINS` table.

```sql
SELECT * FROM information_schema.PLUGINS WHERE PLUGIN_NAME LIKE '%audit%';
```

An empty result indicates that no such plugins are installed or loaded.

??? example "Expected output"

    ```{.text .no-copy}
    Empty set (0.00 sec)
    ```

The following statement checks for system variables whose names start with `audit`:

```sql
SHOW variables LIKE 'audit%';
```

An empty result means that no matching system variables exist or are currently defined.

??? example "Expected output"

    ```{.text .no-copy}
    Empty set (0.01 sec)
    ```

The following statement lists system variables whose names start with `plugin`. The example output shows the `plugin_dir` variable, which specifies the directory path where MySQL plugins are stored.

```sql
SHOW variables LIKE 'plugin%';
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------+------------------------+
    | Variable_name | Value                  |
    +---------------+------------------------+
    | plugin_dir    | /usr/lib/mysql/plugin/ |
    +---------------+------------------------+
    1 row in set (0.00 sec)
    ```

!!! note

    The location of the MySQL plugin directory depends on the operating system and may differ on your system.

The following statement enables the plugin:

```sql
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
```

Run the following statement to verify that the plugin installed correctly:

```sql
SELECT * FROM information_schema.PLUGINS WHERE PLUGIN_NAME LIKE '%audit%'\G
```

??? example "Expected output"

    ```{.text .no-copy}
    *************************** 1. row ***************************
            PLUGIN_NAME: audit_log
            PLUGIN_VERSION: 0.2
            PLUGIN_STATUS: ACTIVE
            PLUGIN_TYPE: AUDIT
    PLUGIN_TYPE_VERSION: 4.1
            PLUGIN_LIBRARY: audit_log.so
    PLUGIN_LIBRARY_VERSION: 1.7
            PLUGIN_AUTHOR: Percona LLC and/or its affiliates.
        PLUGIN_DESCRIPTION: Audit log
            PLUGIN_LICENSE: GPL
            LOAD_OPTION: ON
    1 row in set (0.00 sec)
    ```

Review the audit log variables with the following statement:

```sql
SHOW variables LIKE 'audit%';
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------+---------------+
    | Variable_name               | Value         |
    +-----------------------------+---------------+
    | audit_log_buffer_size       | 1048576       |
    | audit_log_exclude_accounts  |               |
    | audit_log_exclude_commands  |               |
    | audit_log_exclude_databases |               |
    | audit_log_file              | audit.log     |
    | audit_log_flush             | OFF           |
    | audit_log_format            | NEW           |
    | audit_log_handler           | FILE          |
    | audit_log_include_accounts  |               |
    | audit_log_include_commands  |               |
    | audit_log_include_databases |               |
    | audit_log_policy            | ALL           |
    | audit_log_rotate_on_size    | 0             |
    | audit_log_rotations         | 0             |
    | audit_log_strategy          | ASYNCHRONOUS  |
    | audit_log_syslog_facility   | LOG_USER      |
    | audit_log_syslog_ident      | percona-audit |
    | audit_log_syslog_priority   | LOG_INFO      |
    +-----------------------------+---------------+
    18 rows in set (0.00 sec)
    ```

## Log format

The plugin supports the following log formats: `NEW`, `JSON`, and `CSV`. The `NEW` format is based on XML and defines each log record with XML tags. The information logged is the same for all three formats. The `audit_log_format` variable controls the format choice.

### Format examples

The following formats are available:

=== "New log format"

    ```{.text .no-copy}
    <AUDIT_RECORD>
    <NAME>Query</NAME>
    <RECORD>16684_2021-06-30T16:07:41</RECORD>
    <TIMESTAMP>2021-06-30T16:08:06 UTC</TIMESTAMP>
    <COMMAND_CLASS>select</COMMAND_CLASS>
    <CONNECTION_ID>2</CONNECTION_ID>
    <STATUS>0</STATUS>
    <SQLTEXT>select id, holder from one</SQLTEXT>
    <USER>root[root] @ localhost []</USER>
    <HOST>localhost</HOST>
    <OS_USER></OS_USER>
    <IP></IP>
    <DB></DB>
    ```

=== "JSON format"

    ```json
    {"audit_record":{"name":"Query","record":"13149_2021-06-30T15:03:11","timestamp":"2021-06-30T15:07:58 UTC","command_class":"show_databases","connection_id":"2","status":0,"sqltext":"show databases","user":"root[root] @ localhost []","host":"localhost","os_user":"","ip":"","db":""}}
    ```

=== "CSV format"

    ```csv
    "Query","22567_2021-06-30T16:10:09","2021-06-30T16:19:00 UTC","select","2",0,"select count(*) from one","root[root] @ localhost []","localhost","","",""
    ```


## Audit log events

The Audit Log plugin generates log records for the following events.


=== "Audit"

    An `Audit` event indicates that audit logging started or finished. The `NAME` field contains `Audit` when logging started and `NoAudit` when logging finished. The audit record also includes the server version and command-line arguments.

        ??? example "Audit event"

            ```{.text .no-copy}
            <AUDIT_RECORD
            NAME="Audit"
            RECORD="1_2021-06-30T11:56:53"
            TIMESTAMP="2021-06-30T11:56:53 UTC"
            MYSQL_VERSION="5.7.34-37"
            STARTUP_OPTIONS="--daemonize --pid-file=/var/run/mysqld/mysqld.pid"
            OS_VERSION="x86_64-debian-linux-gnu"
            />
            ```

=== "Connect or Disconnect"

    The connect record event uses the `NAME` field `Connect` when a user logs in or a login fails, and `Quit` when the connection closes.

    The additional fields for this event are as follows:

        * `CONNECTION_ID`

        * `STATUS`

        * `USER`

        * `PRIV_USER`

        * `OS_LOGIN`

        * `PROXY_USER`

        * `HOST`

        * `IP`

    `STATUS` is `0` for successful logins and non-zero for failed logins.

    ??? example "Disconnect event"

        ```{.text .no-copy}
        <AUDIT_RECORD
        NAME="Quit"
        RECORD="5_2021-06-29T19:33:03"
        TIMESTAMP="2021-06-29T19:34:38Z"
        CONNECTION_ID="14"
        STATUS="0"
        USER="root"
        PRIV_USER="root"
        OS_LOGIN=""
        PROXY_USER=""
        HOST="localhost"
        IP=""
        DB=""
        />
        ```

=== "Query"

    The additional fields for this event are `COMMAND_CLASS`, `CONNECTION_ID`, `STATUS`, `SQLTEXT`, `USER`, `HOST`, `OS_USER`, and `IP`.

    * `COMMAND_CLASS` — Values come from the `com_status_vars` array in the `sql/mysqld.cc` file of the MySQL source distribution. Example values include `select`, `alter_table`, and `create_table`.

    * `STATUS` — Non-zero value indicates an error.

    * `SQLTEXT` — Text of the SQL statement.

    Possible values for the `NAME` field include `Query`, `Prepare`, `Execute`, and `Change user`.

    ??? example "Query event"

        ```{.text .no-copy}
        <AUDIT_RECORD
        NAME="Query"
        RECORD="4_2021-06-29T19:33:03"
        TIMESTAMP="2021-06-29T19:33:34Z"
        COMMAND_CLASS="show_variables"
        CONNECTION_ID="14"
        STATUS="0"
        SQLTEXT="show variables like 'audit%'"
        USER="root[root] @ localhost []"
        HOST="localhost"
        OS_USER=""
        IP=""
        DB=""
        />
        ```

## Stream the audit log to syslog

To stream the audit log to syslog, set the `audit_log_handler` variable to `SYSLOG`. Use `audit_log_syslog_ident`, `audit_log_syslog_facility`, and `audit_log_syslog_priority` to control the syslog handler. These variables share the meanings of the corresponding parameters documented in the [syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

!!! note

    The `FILE` handler is the only handler that captures the effects of `audit_log_strategy`, `audit_log_buffer_size`, `audit_log_rotate_on_size`, and `audit_log_rotations`.

## Filter methods

Filter the results with any of the following methods.

=== "Filter by user"

    Filtering by user uses two global variables, `audit_log_include_accounts` and `audit_log_exclude_accounts`, which specify the user accounts to include in or exclude from audit logging.

    Only one variable at a time may hold a list; the other must be `NULL`. An attempt to set the second variable fails while the first variable is non-`NULL`. An empty string represents an empty list.

    Changes to `audit_log_include_accounts` and `audit_log_exclude_accounts` do not apply to existing server connections.

=== "Filter by SQL command type"

    Filtering by SQL command type uses two global variables, [audit_log_include_commands](#audit_log_include_commands) and [audit_log_exclude_commands](#audit_log_exclude_commands), which specify the command types to include in or exclude from audit logging.

    Only one variable at a time may hold a list; the other must be `NULL`. An attempt to set the second variable fails while the first variable is non-`NULL`. An empty string represents an empty list.

    When both `audit_log_exclude_commands` and `audit_log_include_commands` are `NULL`, the component logs all commands.

=== "Filtering by database"

    Filtering by SQL database uses two global variables, `audit_log_include_databases` and `audit_log_exclude_databases`, which specify the databases to include in or exclude from audit logging.

    Only one variable at a time may hold a list; the other must be `NULL`. An attempt to set the second variable fails while the first variable is non-`NULL`. An empty string represents an empty list.

    A query that accesses any database listed in `audit_log_include_databases` is logged. A query that accesses only databases listed in `audit_log_exclude_databases` is not logged. `CREATE TABLE` statements are logged unconditionally.

    Changes to `audit_log_include_databases` and `audit_log_exclude_databases` do not apply to existing server connections.

## Filter examples

The following are examples of the different filters.

=== "Filter by user"

    The following example adds users who will be monitored:

    ```sql
    SET GLOBAL audit_log_include_accounts = 'user1@localhost,root@localhost';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    If you try to add users to both the include list and the exclude list, the server returns the following error:

    ```sql
    SET GLOBAL audit_log_exclude_accounts = 'user1@localhost,root@localhost';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        ERROR 1231 (42000): Variable 'audit_log_exclude_accounts' can't be set to the value of 'user1@localhost,root@localhost'
        ```

    To switch from filtering by included user list to the excluded user list or back,
    first set the currently active filtering variable to `NULL`:

    ```sql
    SET GLOBAL audit_log_include_accounts = NULL;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = 'user1@localhost,root@localhost';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = "'user'@'host'";
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = '''user''@''host''';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = '\'user\'@\'host\'';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    To see which user accounts have been added to the exclude list, run the following command:

    ```sql
    SELECT @@audit_log_exclude_accounts;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +------------------------------+
        | @@audit_log_exclude_accounts |
        +------------------------------+
        | 'user'@'host'                |
        +------------------------------+
        1 row in set (0.00 sec)
        ```

    Account names from mysql.user table are logged in the
    audit log. For example when you create a user:

    ```sql
    CREATE USER 'user1'@'%' IDENTIFIED BY '111';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    When `user1` connects from `localhost`, the user is listed:

    ```{.text .no-copy}
    <AUDIT_RECORD
    NAME="Connect"
    RECORD="2_2021-06-30T11:56:53"
    TIMESTAMP="2021-06-30T11:56:53 UTC"
    CONNECTION_ID="6"
    STATUS="0"
    USER="user1" ;; this is a 'user' part of account
    PRIV_USER="user1"
    OS_LOGIN=""
    PROXY_USER=""
    HOST="localhost" ;; this is a 'host' part of account
    IP=""
    DB=""
    />
    ```

    To exclude `user1` from logging, set:

    ```sql
    SET GLOBAL audit_log_exclude_accounts = 'user1@%';
    ```

    The value may be `NULL` or a comma-separated list of accounts in the form `user@host` or `'user'@'host'` (use the quoted form when the user or host contains a comma).



=== "Filter by SQL command type"

    The available command types can be listed by running:

    ```sql
    SELECT name FROM performance_schema.setup_instruments WHERE name LIKE "statement/sql/%" ORDER BY name;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +------------------------------------------+
        | name                                     |
        +------------------------------------------+
        | statement/sql/alter_db                   |
        | statement/sql/alter_db_upgrade           |
        | statement/sql/alter_event                |
        | statement/sql/alter_function             |
        | statement/sql/alter_procedure            |
        | statement/sql/alter_server               |
        | statement/sql/alter_table                |
        | statement/sql/alter_tablespace           |
        | statement/sql/alter_user                 |
        | statement/sql/analyze                    |
        | statement/sql/assign_to_keycache         |
        | statement/sql/begin                      |
        | statement/sql/binlog                     |
        | statement/sql/call_procedure             |
        | statement/sql/change_db                  |
        | statement/sql/change_master              |
        ...
        | statement/sql/xa_rollback                |
        | statement/sql/xa_start                   |
        +------------------------------------------+
        145 rows in set (0.00 sec)
        ```

    You can add commands to the `include` filter by running:

    ```sql
    SET GLOBAL audit_log_include_commands= 'set_option,create_db';
    ```

    Create a database with the following command:

    ```sql
    CREATE DATABASE sample;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        <AUDIT_RECORD>
        <NAME>Query</NAME>
        <RECORD>24320_2021-06-30T17:44:46</RECORD>
        <TIMESTAMP>2021-06-30T17:45:16 UTC</TIMESTAMP>
        <COMMAND_CLASS>create_db</COMMAND_CLASS>
        <CONNECTION_ID>2</CONNECTION_ID>
        <STATUS>0</STATUS>
        <SQLTEXT>CREATE DATABASE sample</SQLTEXT>
        <USER>root[root] @ localhost []</USER>
        <HOST>localhost</HOST>
        <OS_USER></OS_USER>
        <IP></IP>
        <DB></DB>
        </AUDIT_RECORD>
        ```

    To switch the command type filtering type from included type list to the excluded list
    or back, first reset the currently-active list to `NULL`:

    ```sql
    SET GLOBAL audit_log_include_commands = NULL;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_commands= 'set_option,create_db';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    A stored procedure has the `call_procedure` command type. All
    the statements executed within the procedure have the same type
    `call_procedure` as well.

=== "Filter by database"

    To add databases to be monitored, run:

    ```sql
    SET GLOBAL audit_log_include_databases = 'test,mysql,db1';
    ```

    ??? note "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_include_databases= 'db1','db3';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    When you try to add databases to both the include and exclude lists, the server returns the following error:

    ```sql
    SET GLOBAL audit_log_exclude_databases = 'test,mysql,db1';
    ```

    ??? example "Error message"

        ```{.text .no-copy}
        ERROR 1231 (42000): Variable 'audit_log_exclude_databases can't be set to the value of 'test,mysql,db1'
        ```

    To switch from filtering by included database list to the excluded one or back,
    first set the currently active filtering variable to `NULL`:

    ```sql
    SET GLOBAL audit_log_include_databases = NULL;
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_databases = 'test,mysql,db1';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

## System variables

### `audit_log_strategy`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | ASYNCHRONOUS       |
| Allowed values | `ASYNCHRONOUS`, `PERFORMANCE`, `SEMISYNCHRONOUS`, `SYNCHRONOUS`|

Specifies the audit log strategy. The allowed values are as follows:

* `ASYNCHRONOUS` — (default) log through a memory buffer and do not drop messages when the buffer is full.

* `PERFORMANCE` — log through a memory buffer and drop messages when the buffer is full.

* `SEMISYNCHRONOUS` — log directly to the file without flushing and syncing every event.

* `SYNCHRONOUS` — log directly to the file and flush and sync every event.

The variable has effect only when `audit_log_handler` is set to `FILE`.

### `audit_log_file`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | audit.log          |

Specifies the filename that stores the audit log. The value may be a path relative to the data directory or an absolute path.

### `audit_log_flush`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |
| Default value   | OFF                |

When the variable is set to `ON`, the server closes and reopens the log file.

### `audit_log_buffer_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | Numeric            |
| Default value   | 1 Mb               |

Specifies the size of the memory buffer used for logging when `audit_log_strategy` is `ASYNCHRONOUS` or `PERFORMANCE`. The variable has effect only when `audit_log_handler` is set to `FILE`.

### `audit_log_exclude_accounts`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Specifies the list of users to which filtering by user applies. The value may be `NULL` or a comma-separated list of accounts in the form `user@host` or `'user'@'host'` (use the quoted form when the user or host contains a comma). When `audit_log_exclude_accounts` is set, leave `audit_log_include_accounts` unset, and vice versa.

### `audit_log_exclude_commands`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Specifies the list of commands to which filtering by SQL command type applies. The value may be `NULL` or a comma-separated list of commands. When `audit_log_exclude_commands` is set, leave `audit_log_include_commands` unset, and vice versa.

### `audit_log_exclude_databases`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Specifies the databases to filter. The value may be `NULL` or a comma-separated list of databases. When `audit_log_exclude_databases` is set, leave `audit_log_include_databases` unset, and vice versa.


### `audit_log_format`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | NEW                |
| Allowed values | `NEW`, `CSV`, `JSON`|

Specifies the audit log format. The audit log plugin supports three log formats: `NEW`, `JSON`, and `CSV`. The `NEW` format is based on XML and outputs log record properties as XML tags. The information logged is the same in all three formats.

### `audit_log_include_accounts`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Specifies the list of users to which filtering by user applies. The value may be `NULL` or a comma-separated list of accounts in the form `user@host` or `'user'@'host'` (use the quoted form when the user or host contains a comma). When `audit_log_include_accounts` is set, leave `audit_log_exclude_accounts` unset, and vice versa.

### `audit_log_include_commands`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Specifies the list of commands to which filtering by SQL command type applies. The value may be `NULL` or a comma-separated list of commands. When `audit_log_include_commands` is set, leave `audit_log_exclude_commands` unset, and vice versa.

### `audit_log_include_databases`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Specifies the list of databases to filter. The value may be `NULL` or a comma-separated list of databases. When `audit_log_include_databases` is set, leave `audit_log_exclude_databases` unset, and vice versa.

### `audit_log_policy`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |
| Default        | ALL                |
| Allowed values | `ALL`, `LOGINS`, `QUERIES`, `NONE` |

Specifies which events to log. The allowed values are as follows:

* `ALL` — log all events.

* `LOGINS` — log only logins.

* `QUERIES` — log only queries.

* `NONE` — log no events.

### `audit_log_rotate_on_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | Numeric            |
| Default value  | 0                  |

Specifies the maximum audit log file size in bytes. When the audit log reaches this size, the server rotates the log. Rotated log files remain in the same directory as the current log file. The server appends a sequence number to the log file name on rotation.

When the value is `0` (the default), the audit log files do not rotate.

Set `audit_log_handler` to `FILE` to enable this variable.

### `audit_log_rotations`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | Numeric            |
| Default value   | 0                  |

Specifies how many log files to keep when `audit_log_rotate_on_size` is set to a non-zero value. The variable has effect only when `audit_log_handler` is set to `FILE`.

### `audit_log_handler`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | FILE               |
| Allowed values | `FILE`, `SYSLOG`   |

Specifies where to write the audit log. `FILE` writes to the file specified by `audit_log_file`. `SYSLOG` writes to syslog.

### `audit_log_syslog_ident`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | percona-audit      |

Specifies the `ident` value for syslog. The variable has the same meaning as the corresponding parameter in the [syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

### `audit_log_syslog_facility`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | LOG_USER           |

Specifies the `facility` value for syslog. The variable has the same meaning as the corresponding parameter in the [syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

### `audit_log_syslog_priority`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | LOG_INFO           |
| Allowed values | `LOG_EMERG`, `LOG_ALERT`, `LOG_CRIT`, `LOG_ERR`, `LOG_WARNING`, `LOG_NOTICE`, `LOG_INFO`, `LOG_DEBUG` |

Specifies the severity level for syslog. The `audit_log_syslog_priority` variable does not include the facility. The variable selects only the severity level (`LOG_EMERG` through `LOG_DEBUG`).

The server builds the full syslog priority passed to `syslog()` by OR-ing the configured facility (`audit_log_syslog_facility`) with this level.

The default `LOG_INFO` represents ordinary informational messages. Raise or lower the level as needed. The facility stays at the default unless you change it explicitly.

For more details about syslog priority levels, see the [syslog(3)
manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

## Status Variables

### `Audit_log_buffer_size_overflow`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type      | Numeric            | 

The number of times an audit log entry was dropped or written directly to the file because the entry size exceeded `audit_log_buffer_size`.

## Additional reading

* [Audit Log Filter overview](audit-log-filter-overview.md) — recommended replacement component

* [Migrate to the audit log filter component](migrate-to-audit-log-filter-component.md) — variable mapping and cutover procedure

* [Install the audit log filter](install-audit-log-filter.md)

* [Upgrade components](upgrade-components.md)

* [Upgrade Percona Server for MySQL](upgrade.md)

* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
