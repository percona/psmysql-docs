# Audit log plugin

!!! note "Deprecation notice"

    The audit log plugin is deprecated in Percona Server for MySQL 8.4 and will be removed in a future release. This deprecation is due to the availability of the [audit log filter component](audit-log-filter-overview.md), which is the recommended replacement. Users should migrate to this component, which provides equivalent functionality with enhanced flexibility, performance, and filtering capabilities, ensuring continued support for auditing and compliance requirements.

    This deprecation affects all installations that rely on the audit log plugin for event logging, compliance auditing, or activity tracking. The plugin will continue to function, but no further development or maintenance is planned.

    The audit log plugin and the audit log filter component use different configuration variables and options.
    
    * Do not attempt to use audit log filter variables, options, or configuration syntax with the deprecated audit log plugin. Doing so can lead to startup failures, unexpected behavior, or data loss.

    * Do not install both audit log plugin and audit log filter component simultaneously.

    The audit‑log entries may look different from the 8.0 entries. The audit log plugin itself has not changed, but other server components have, and those changes affect the log output. For example, 8.4 logs a `SELECT $$` statement each time a client connects because the client now supports “dollar‑quoted” strings. This feature did not exist in 8.0.

    Percona does not plan to modify 8.4 audit logs to match the format or content of 8.0 logs.

Percona Audit Log Plugin provides monitoring and logging of connection and query activity that were performed on specific server. Information about the activity is stored in a log file. 

## Install the plugin

The audit Log plugin is installed, but, by default, is not enabled when you install Percona Server for MySQL. To check if the plugin is enabled run the following command. This command searches for plugins with names containing the word "audit" in the `information_schema.PLUGINS` table. 

```sql
SELECT * FROM information_schema.PLUGINS WHERE PLUGIN_NAME LIKE '%audit%';
```

The empty result suggests that no such plugins are installed or loaded.

??? example "Expected output"

    ```sql
    Empty set (0.00 sec)
    ```

This command checks for system variables whose names start with "audit." 

```sql
SHOW variables LIKE 'audit%';
```

The empty result means that no such system variables exist or are currently defined.

??? example "Expected output"

    ```sql
    Empty set (0.01 sec)
    ```

This command lists system variables with names starting with "plugin." As seen in the example output, it displays the `plugin_dir` variable, which specifies the directory path where MySQL plugins are stored.

```sql
SHOW variables LIKE 'plugin%';
```

??? example "Expected output"

    ```sql
    +---------------+------------------------+
    | Variable_name | Value                  |
    +---------------+------------------------+
    | plugin_dir    | /usr/lib/mysql/plugin/ |
    +---------------+------------------------+
    1 row in set (0.00 sec)
    ```

!!! note

    The location of the MySQL plugin directory depends on the operating system and may be different on your system.

The following command enables the plugin:

```sql
INSTALL PLUGIN audit_log SONAME 'audit_log.so';
```

Run the following command to verify if the plugin was installed correctly:

```sql
SELECT * FROM information_schema.PLUGINS WHERE PLUGIN_NAME LIKE '%audit%'\G
```

??? example "Expected output"

    ```sql
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

You can review the audit log variables with the following command:

```sql
SHOW variables LIKE 'audit%';
```

??? example "Expected output"

    ```sql
    +-----------------------------+---------------+
    | Variable_name               | Value         |
    +-----------------------------+---------------+
    | audit_log_buffer_size       | 1048576       |
    | audit_log_exclude_accounts  |               |
    | audit_log_exclude_commands  |               |
    | audit_log_exclude_databases |               |
    | audit_log_file              | audit.log     |
    | audit_log_flush             | OFF           |
    | audit_log_format            | OLD           |
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

The plugin supports the following log formats: `OLD`, `NEW`, `JSON`, and `CSV`. The `OLD` format and the `NEW` format are based on XML. The `OLD` format defines each log record with XML attributes. The `NEW` format defines each log record with XML tags. The information logged is the same for all four formats. The audit_log_format variable controls the log format choice.

### Format examples

The following formats are available:

=== "Old log format"

    ```sql
    <AUDIT_RECORD
    NAME="Query"
    RECORD="3_2021-06-30T11:56:53"
    TIMESTAMP="2021-06-30T11:57:14 UTC"
    COMMAND_CLASS="select"
    CONNECTION_ID="3"
    STATUS="0"
    SQLTEXT="select * from information_schema.PLUGINS where PLUGIN_NAME like '%audit%'"
    USER="root[root] @ localhost []"
    HOST="localhost"
    OS_USER=""
    IP=""
    DB=""
    />
    ```

=== "New log format"

    ```sql
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

The audit Log plugin generates a log of following events.


=== "Audit" 

    Audit event indicates that audit logging started or finished. `NAME` field will be `Audit` when logging started and `NoAudit` when logging finished. Audit record also includes server version and command-line arguments.

        ??? example "Audit event"

            ```sql
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

    Connect record event will have `NAME` field `Connect` when user logged in or login failed, or `Quit` when connection is closed.

    The additional fields for this event are the following:

        * `CONNECTION_ID`

        * `STATUS`

        * `USER`

        * `PRIV_USER`

        * `OS_LOGIN`

        * `PROXY_USER`

        * `HOST`

        * `IP`

    The value for `STATUS` is `0` for successful logins and non-zero for failed logins.

    ??? example "Disconnect event"

        ```sql
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

    Additional fields for this event are: `COMMAND_CLASS` (values come from the `com_status_vars` array in the `sql/mysqld.cc\`` file in a MySQL source distribution.

    Examples are `select`, `alter_table`, `create_table`, etc.), `CONNECTION_ID`, `STATUS` (indicates an error when the vaule is non-zero), `SQLTEXT` (text of SQL-statement), `USER`, `HOST`, `OS_USER`, `IP`.

    The possible values for the `NAME` name field for this event are `Query`, `Prepare`, `Execute`, `Change user`, etc.

    ??? example "Query event"

        ```sql
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

To stream the audit log to syslog you’ll need to set audit_log_handler variable to `SYSLOG`. To control the syslog file handler, the following variables can be used: audit_log_syslog_ident, audit_log_syslog_facility, and audit_log_syslog_priority These variables have the same meaning as appropriate parameters described in the [syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

!!! note

    The actions for the variables: audit_log_strategy, audit_log_buffer_size, audit_log_rotate_on_size, audit_log_rotations are captured only with `FILE` handler.

## Filter methods

You can filter the results by the following methods.

=== "Filter by user"

    The filtering by user feature adds two new global variables:
    audit_log_include_accounts and
    audit_log_exclude_accounts to specify which user accounts should be
    included or excluded from audit logging.

    Only one of these variables can contain a list of users to be either included or excluded, while the other must be `NULL`. If one of the variables is set to be not `NULL` (contains a list of users), the attempt to set another one fails. An empty string means an empty list.

    Changes of audit_log_include_accounts and audit_log_exclude_accounts do not apply to existing server connections.

=== "Filter by SQL command type"

    The filtering by SQL command type adds two new global variables:
    [audit_log_include_commands](#audit_log_include_commands) and
    [audit_log_exclude_commands](#audit_log_exclude_commands) to specify which command types should be included or excluded from audit logging.

    Only one of these variables can contain a list of command types to be
    either included or excluded, while the other needs to be `NULL`. If one of
    the variables is set to be not `NULL` (contains a list of command types),
    the attempt to set another one will fail. An empty string is defined as an empty list.

    If both the audit_log_exclude_commands variable and the
    audit_log_include_commands variable are `NULL`, all commands are logged.

=== "Filtering by database"

    The filtering by an SQL database is implemented by two global variables:
    audit_log_include_databases and
    audit_log_exclude_databases to specify which databases should be included or excluded from audit logging.

    Only one of these variables can contain a list of databases to be either
    included or excluded, while the other needs to be `NULL`. If one of the
    variables is set to be not `NULL` (contains a list of databases), the
    attempt to set another one will fail. Empty string means an empty list.

    If query is accessing any of databases listed in
    audit_log_include_databases, the query will be logged.
    If query is accessing only databases listed in
    audit_log_exclude_databases, the query will not be logged.
    `CREATE TABLE` statements are logged unconditionally.

    Changes of audit_log_include_databases and
    audit_log_exclude_databases do not apply to existing server
    connections.

## Filter examples

The following are examples of the different filters.

=== "Filter by user"

    The following example adds users who will be monitored:

    ```sql
    SET GLOBAL audit_log_include_accounts = 'user1@localhost,root@localhost';
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    If you try to add users to both the include list and the exclude list, the server returns the following error:

    ```sql
    SET GLOBAL audit_log_exclude_accounts = 'user1@localhost,root@localhost';
    ```

    ??? example "Expected output"

        ```sql
        ERROR 1231 (42000): Variable 'audit_log_exclude_accounts' can't be set to the value of 'user1@localhost,root@localhost'
        ```

    To switch from filtering by included user list to the excluded user list or back,
    first set the currently active filtering variable to `NULL`:

    ```sql
    SET GLOBAL audit_log_include_accounts = NULL;
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = 'user1@localhost,root@localhost';
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = "'user'@'host'";
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = '''user''@''host''';
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_accounts = '\'user\'@\'host\'';
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    To see which user accounts have been added to the exclude list, run the following command:

    ```sql
    SELECT @@audit_log_exclude_accounts;
    ```

    ??? example "Expected output"

        ```sql
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

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    When `user1` connects from `localhost`, the user is listed:

    ```sql
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

    To exclude `user1` from logging in Percona Server for MySQL 8.4, set:

    ```sql
    SET GLOBAL audit_log_exclude_accounts = 'user1@%';
    ```

    The value can be `NULL` or comma separated list of accounts in form
    `user@host` or `'user'@'host'` (if user or host contains comma).



=== "Filter by SQL command type"

    The available command types can be listed by running:

    ```sql
    SELECT name FROM performance_schema.setup_instruments WHERE name LIKE "statement/sql/%" ORDER BY name;
    ```

    ??? example "Expected output"

        ```sql
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

        ```sql
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

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_commands= 'set_option,create_db';
    ```

    ??? example "Expected output"

        ```sql
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

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_include_databases= 'db1','db3';
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    If you you try to add databases to both include and exclude lists server will
    show you the following error:

    ```sql
    SET GLOBAL audit_log_exclude_databases = 'test,mysql,db1';
    ```

    ??? example "Error message"

        ```sql
        ERROR 1231 (42000): Variable 'audit_log_exclude_databases can't be set to the value of 'test,mysql,db1'
        ```

    To switch from filtering by included database list to the excluded one or back,
    first set the currently active filtering variable to `NULL`:

    ```sql
    SET GLOBAL audit_log_include_databases = NULL;
    ```

    ??? example "Expected output"

        ```sql
        Query OK, 0 rows affected (0.00 sec)
        ```

    ```sql
    SET GLOBAL audit_log_exclude_databases = 'test,mysql,db1';
    ```

    ??? example "Expected output"

        ```sql
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

This variable is used to specify the audit log strategy, possible values are:

* `ASYNCHRONOUS` - (default) log using memory buffer, do not drop messages if buffer is full

* `PERFORMANCE` - log using memory buffer, drop messages if buffer is full

* `SEMISYNCHRONOUS` - log directly to file, do not flush and sync every event

* `SYNCHRONOUS` - log directly to file, flush and sync every event

This variable has effect only when audit_log_handler is set to `FILE`.

### `audit_log_file`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | audit.log          |

This variable is used to specify the filename that’s going to store the audit log. It can contain the path relative to the datadir or absolute path.

### `audit_log_flush`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |
| Default value   | OFF                |

When this variable is set to `ON` log file will be closed and reopened.

### `audit_log_buffer_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | Numeric            |
| Default value   | 1 Mb               |

This variable can be used to specify the size of memory buffer used for logging, used when audit_log_strategy variable is set to `ASYNCHRONOUS` or `PERFORMANCE` values. This variable has effect only when audit_log_handler is set to `FILE`.

### `audit_log_exclude_accounts`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

This variable is used to specify the list of users for which
Filtering by user is applied. The value can be `NULL` or comma
separated list of accounts in form `user@host` or `'user'@'host'` (if user
or host contains comma). If this variable is set, then
audit_log_include_accounts must be unset, and vice versa.

### `audit_log_exclude_commands`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

This variable is used to specify the list of commands for which
Filtering by SQL command type is applied. The value can be `NULL` or
comma separated list of commands. If this variable is set, then
audit_log_include_commands must be unset, and vice versa.

### `audit_log_exclude_databases`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

Use this variable to specify the databases to be filtered. The value can be NULL or a comma-separated list of databases if you set this variable, unset `audit_log_include_databases`, and vice versa.


### `audit_log_format`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | OLD                |
| Allowed values | `OLD`, `NEW`, `CSV`, `JSON`|

This variable is used to specify the audit log format. The audit log plugin
supports four log formats: `OLD`, `NEW`, `JSON`, and `CSV`. `OLD` and
`NEW` formats are based on XML, where the former outputs log record properties
as XML attributes and the latter as XML tags. Information logged is the same in
all four formats.

### `audit_log_include_accounts`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

This variable is used to specify the list of users for which
Filtering by user is applied. The value can be `NULL` or comma
separated list of accounts in form `user@host` or `'user'@'host'` (if user
or host contains comma). If this variable is set, then
audit_log_exclude_accounts must be unset, and vice versa.

### `audit_log_include_commands`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

This variable is used to specify the list of commands for which
Filtering by SQL command type is applied. The value can be `NULL` or
comma separated list of commands. If this variable is set, then
audit_log_exclude_commands must be unset, and vice versa.

### `audit_log_include_databases`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |

This variable defines the list of databases to be filtered. You can set the value to NULL or a comma-separated list of databases. If you set this variable, you must unset `audit_log_exclude_databases`; the opposite is true.

### `audit_log_policy`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | String             |
| Default        | ALL                |
| Allowed values | `ALL`, `LOGINS`, `QUERIES`, `NONE` |

This variable is used to specify which events should be logged. Possible values
are:

* `ALL` - all events will be logged

* `LOGINS` - only logins will be logged

* `QUERIES` - only queries will be logged

* `NONE` - no events will be logged

### `audit_log_rotate_on_size`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | Numeric            |
| Default value  | 0                  |

This variable is measured in bytes and specifies the maximum size of the audit log file. Upon reaching
this size, the audit log will be rotated. The rotated log files are present in
the same directory as the current log file. The sequence number is appended to
the log file name upon rotation. 

If the value is set to 0 (the default), the audit log files won’t rotate.

Set the `audit_log_handler` to FILE to enable this variable.

### `audit_log_rotations`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | Numeric            |
| Default value   | 0                  |

This variable is used to specify how many log files should be kept when
audit_log_rotate_on_size variable is set to non-zero value. This
variable has effect only when audit_log_handler is set to `FILE`.

### `audit_log_handler`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | FILE               |
| Allowed values | `FILE`, `SYSLOG`   |

This variable is used to configure where the audit log will be written. If it is
set to `FILE`, the log will be written into a file specified by
audit_log_file variable. If it is set to `SYSLOG`, the audit log
will be written to syslog.

### `audit_log_syslog_ident`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | percona-audit      |

This variable is used to specify the `ident` value for syslog. This variable
has the same meaning as the appropriate parameter described in the [syslog(3)
manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

### `audit_log_syslog_facility`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | LOG_USER           |

This variable is used to specify the `facility` value for syslog. This
variable has the same meaning as the appropriate parameter described in the
[syslog(3) manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

### `audit_log_syslog_priority`

| Option         | Description        |
| -------------- | ------------------ |
| Command Line:  | Yes                |
| Scope:         | Global             |
| Dynamic:       | No                 |
| Data type      | String             |
| Default value   | LOG_INFO           |
| Allowed values | `LOG_EMERG`, `LOG_ALERT`, `LOG_CRIT`, `LOG_ERR`, `LOG_WARNING`, `LOG_NOTICE`, `LOG_INFO`, `LOG_DEBUG` |

This variable is used to specify the severity level for syslog. The
`audit_log_syslog_priority` variable does not include the facility; it only
selects the severity level (`LOG_EMERG` … `LOG_DEBUG`).

The full syslog priority that `syslog()` receives is built internally by OR-ing
the configured facility (`audit_log_syslog_facility`) with this level.

The default `LOG_INFO` means "ordinary informational messages"; you can raise or
lower the level as needed, while the facility stays at its default unless you
change it explicitly.

For more details about syslog priority levels, see the [syslog(3)
manual](https://man7.org/linux/man-pages/man3/syslog.3.html).

## Status Variables

### `Audit_log_buffer_size_overflow`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type      | Numeric            | 

The number of times an audit log entry was either
dropped or written directly to the file due to its size being bigger
than audit_log_buffer_size variable.
