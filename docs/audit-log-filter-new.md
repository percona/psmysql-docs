# Audit Log Filter format - XML (new style)

Percona Server for MySQL 8.4.9-9 introduces the following changes to the NEW XML formatter:

* Record IDs (`<RECORD_ID>`) are 1-based instead of 0-based
* Empty field values use self-closing XML tags (`<OS_LOGIN/>`) instead of empty tag pairs (`<OS_LOGIN></OS_LOGIN>`)
* Indentation uses 1 space per nesting level instead of 2 spaces
* The startup record (`<NAME>Audit</NAME>`) now includes `<VERSION>`, `<STARTUP_OPTIONS>`, `<OS_VERSION>`, and `<MYSQL_VERSION>`
* Message events use `<MAP>` (containing `<ELEMENT>` children each with a `<KEY>` and `<VALUE>`) instead of `<MESSAGE_ATTRIBUTES>`; message events also include `<USER>`, `<OS_LOGIN>`, `<HOST>`, `<IP>`, `<STATUS>`, and `<STATUS_CODE>`
* The `<COMMAND_CLASS>` values now use the same command-name mapping as upstream MySQL Enterprise Audit (for example `create_table`, `set_option`)
* The new [`audit_log_filter.event_mode`](audit-log-filter-variables.md#audit_log_filterevent_mode) variable controls which events appear:

    * `REDUCED` (default) — emits only the most relevant record per action
    * `FULL` — adds lifecycle events: `Command Start`/`Command End`, `Query Start`/`Query Status End`, `Preparse`/`Postparse`, `Pre Authenticate`, stored-program `Execute`, `Variable Get`/`Variable Set`, and authentication subclass events (`Auth Credential Change`, `Auth Authid Rename`, `Auth Authid Drop`, `Auth Flush`)

    Before Percona Server for MySQL 8.4.9-9 all events were always written (equivalent to `FULL`).

If you run an older {{vers}} build than 8.4.9-9, verify against your own audit log in case output differs. Implementation reference: `components/audit_log_filter/log_record_formatter/new.cc` and `base.cc`.

The Audit Log Filter component can write the audit log file as new-style XML
(`audit_log_filter.format=NEW`). The file uses UTF-8.

The root element is `<AUDIT>`. It contains `<AUDIT_RECORD>` elements. Each
`<AUDIT_RECORD>` describes one audited event.

Element order inside `<AUDIT_RECORD>` is not guaranteed (the writer may
emit fields in a fixed order in practice, but consumers should not depend on it).

Timestamps use the server local time zone, in `YYYY-MM-DDTHH:MM:SS`
form. They do not append a ` UTC` suffix to the timestamp string.

## Example — REDUCED mode (default)

With `audit_log_filter.event_mode=REDUCED` (the default), the component
emits only the most relevant record per action. The snippet below shows
several record types. Exact sets of elements depend on filters and server
configuration.

```xml
<?xml version="1.0" encoding="utf-8"?>
<AUDIT>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>1_2026-03-27T20:00:59</RECORD_ID>
  <NAME>Audit</NAME>
  <SERVER_ID>1</SERVER_ID>
  <VERSION>1</VERSION>
  <STARTUP_OPTIONS>/usr/sbin/mysqld --defaults-file=/etc/my.cnf --basedir=/usr --port=3306 --socket=/var/run/mysqld/mysqld.sock --datadir=/var/lib/mysql</STARTUP_OPTIONS>
  <OS_VERSION>x86_64-Linux</OS_VERSION>
  <MYSQL_VERSION>8.4.9-9</MYSQL_VERSION>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>2_2026-03-27T20:00:59</RECORD_ID>
  <NAME>Connect</NAME>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER>root</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>connect</COMMAND_CLASS>
  <CONNECTION_TYPE>TCP/IP</CONNECTION_TYPE>
  <PRIV_USER>root</PRIV_USER>
  <PROXY_USER/>
  <DB/>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>28_2026-03-27T20:00:59</RECORD_ID>
  <NAME>TableRead</NAME>
  <CONNECTION_ID>20</CONNECTION_ID>
  <USER>root[root] @ localhost [127.0.0.1]</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>select</COMMAND_CLASS>
  <SQLTEXT>SELECT * FROM t_access</SQLTEXT>
  <DB>test</DB>
  <TABLE>t_access</TABLE>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>29_2026-03-27T20:00:59</RECORD_ID>
  <NAME>Query</NAME>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER>root[root] @ localhost [127.0.0.1]</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>select</COMMAND_CLASS>
  <SQLTEXT>SELECT * FROM t_access</SQLTEXT>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>45_2026-03-27T20:00:59</RECORD_ID>
  <NAME>Message</NAME>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER>root[root] @ localhost [127.0.0.1]</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>internal</COMMAND_CLASS>
  <COMPONENT>test_audit_api_message</COMPONENT>
  <PRODUCER>test_audit_api_message</PRODUCER>
  <MESSAGE>test_audit_api_message_internal</MESSAGE>
  <MAP>
   <ELEMENT>
    <KEY>my_numeric_key</KEY>
    <VALUE>-9223372036854775808</VALUE>
   </ELEMENT>
  </MAP>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>88_2026-03-27T20:00:59</RECORD_ID>
  <NAME>Connect</NAME>
  <CONNECTION_ID>22</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER>root</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>connect</COMMAND_CLASS>
  <CONNECTION_TYPE>SSL</CONNECTION_TYPE>
  <CONNECTION_ATTRIBUTES>
   <ATTRIBUTE>
    <NAME>_pid</NAME>
    <VALUE>764350</VALUE>
   </ATTRIBUTE>
   <ATTRIBUTE>
    <NAME>_platform</NAME>
    <VALUE>x86_64</VALUE>
   </ATTRIBUTE>
   <ATTRIBUTE>
    <NAME>_os</NAME>
    <VALUE>Linux</VALUE>
   </ATTRIBUTE>
   <ATTRIBUTE>
    <NAME>_client_name</NAME>
    <VALUE>libmysql</VALUE>
   </ATTRIBUTE>
   <ATTRIBUTE>
    <NAME>_client_version</NAME>
    <VALUE>8.4.9-9</VALUE>
   </ATTRIBUTE>
   <ATTRIBUTE>
    <NAME>program_name</NAME>
    <VALUE>mysqladmin</VALUE>
   </ATTRIBUTE>
  </CONNECTION_ATTRIBUTES>
  <PRIV_USER>root</PRIV_USER>
  <PROXY_USER/>
  <DB/>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:00:59</TIMESTAMP>
  <RECORD_ID>90_2026-03-27T20:00:59</RECORD_ID>
  <NAME>Quit</NAME>
  <CONNECTION_ID>22</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER>root</USER>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>connect</COMMAND_CLASS>
  <CONNECTION_TYPE>SSL</CONNECTION_TYPE>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <TIMESTAMP>2026-03-27T20:01:00</TIMESTAMP>
  <RECORD_ID>91_2026-03-27T20:01:00</RECORD_ID>
  <NAME>NoAudit</NAME>
  <SERVER_ID>1</SERVER_ID>
 </AUDIT_RECORD>
</AUDIT>
```

## Example — FULL mode (additional events)

With `audit_log_filter.event_mode=FULL`, the component emits lifecycle
events that bracket each action. Below are the additional event types
produced in FULL mode. They appear alongside the records shown in the
REDUCED example above.

```xml
 <!-- Pre-authentication (before credentials are verified) -->
 <AUDIT_RECORD>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <RECORD_ID>2_2026-04-03T13:19:21</RECORD_ID>
  <NAME>Pre Authenticate</NAME>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <STATUS_CODE>0</STATUS_CODE>
  <USER/>
  <OS_LOGIN/>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <COMMAND_CLASS>connect</COMMAND_CLASS>
  <CONNECTION_TYPE>TCP/IP</CONNECTION_TYPE>
 </AUDIT_RECORD>

 <!-- Command lifecycle: wraps every client command -->
 <AUDIT_RECORD>
  <NAME>Command Start</NAME>
  <RECORD_ID>5_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <COMMAND_CLASS>Query</COMMAND_CLASS>
 </AUDIT_RECORD>

 <!-- Parse events: before and after SQL parsing -->
 <AUDIT_RECORD>
  <NAME>Preparse</NAME>
  <RECORD_ID>6_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Parse</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <FLAGS>0</FLAGS>
  <SQLTEXT>INSERT INTO t_access VALUES (1, 'inserted')</SQLTEXT>
  <REWRITTEN_QUERY></REWRITTEN_QUERY>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Postparse</NAME>
  <RECORD_ID>7_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Parse</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <FLAGS>0</FLAGS>
  <SQLTEXT>INSERT INTO t_access VALUES (1, 'inserted')</SQLTEXT>
  <REWRITTEN_QUERY></REWRITTEN_QUERY>
 </AUDIT_RECORD>

 <!-- Query lifecycle: brackets a single SQL statement execution -->
 <AUDIT_RECORD>
  <NAME>Query Start</NAME>
  <RECORD_ID>124_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <COMMAND_CLASS>insert</COMMAND_CLASS>
  <SQLTEXT>INSERT INTO t_access VALUES (1, 'inserted')</SQLTEXT>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Query Status End</NAME>
  <RECORD_ID>126_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <COMMAND_CLASS>insert</COMMAND_CLASS>
  <SQLTEXT>INSERT INTO t_access VALUES (1, 'inserted')</SQLTEXT>
 </AUDIT_RECORD>

 <AUDIT_RECORD>
  <NAME>Command End</NAME>
  <RECORD_ID>129_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <COMMAND_CLASS>Query</COMMAND_CLASS>
 </AUDIT_RECORD>

 <!-- Stored-program execution -->
 <AUDIT_RECORD>
  <NAME>Execute</NAME>
  <RECORD_ID>91_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Stored Program</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <DB>test</DB>
  <STORED_PROGRAM>trigger_nested_query</STORED_PROGRAM>
 </AUDIT_RECORD>

 <!-- Nested query inside a stored procedure -->
 <AUDIT_RECORD>
  <NAME>Query Nested Start</NAME>
  <RECORD_ID>92_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <COMMAND_CLASS>do</COMMAND_CLASS>
  <SQLTEXT>DO (SELECT 'nested query from stored procedure')</SQLTEXT>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Query Nested Status End</NAME>
  <RECORD_ID>93_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <COMMAND_CLASS>do</COMMAND_CLASS>
  <SQLTEXT>DO (SELECT 'nested query from stored procedure')</SQLTEXT>
 </AUDIT_RECORD>

 <!-- Global variable access -->
 <AUDIT_RECORD>
  <NAME>Variable Get</NAME>
  <RECORD_ID>284_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>select</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <VARIABLE_NAME>sort_buffer_size</VARIABLE_NAME>
  <VARIABLE_VALUE>262144</VARIABLE_VALUE>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Variable Set</NAME>
  <RECORD_ID>306_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>set_option</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <VARIABLE_NAME>sort_buffer_size</VARIABLE_NAME>
  <VARIABLE_VALUE>1048576</VARIABLE_VALUE>
 </AUDIT_RECORD>

 <!-- Authentication subclass events -->
 <AUDIT_RECORD>
  <NAME>Auth Credential Change</NAME>
  <RECORD_ID>337_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Authentication</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <USER>audit_tmp_user</USER>
  <HOST>localhost</HOST>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Auth Authid Rename</NAME>
  <RECORD_ID>368_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Authentication</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <USER>audit_tmp_user</USER>
  <HOST>localhost</HOST>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Auth Authid Drop</NAME>
  <RECORD_ID>399_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Authentication</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <USER>audit_renamed</USER>
  <HOST>localhost</HOST>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Auth Flush</NAME>
  <RECORD_ID>430_2026-04-03T13:19:21</RECORD_ID>
  <TIMESTAMP>2026-04-03T13:19:21</TIMESTAMP>
  <COMMAND_CLASS>Authentication</COMMAND_CLASS>
  <CONNECTION_ID>20</CONNECTION_ID>
  <STATUS>0</STATUS>
  <USER></USER>
  <HOST></HOST>
 </AUDIT_RECORD>
```

## Record descriptions

Query events use `<NAME>Query</NAME>` and include `<STATUS>`,
`<STATUS_CODE>`, `<CONNECTION_ID>`, `<COMMAND_CLASS>` (SQL command name
from the event), and often `<SQLTEXT>`. They also include `<HOST>`,
`<IP>`, `<USER>`, and `<OS_LOGIN>`.

Table-access events (`TableRead`, `TableInsert`, `TableUpdate`,
`TableDelete`) include `<DB>`, `<TABLE>`, `<COMMAND_CLASS>`, `<SQLTEXT>`,
`<HOST>`, `<IP>`, `<USER>`, and `<OS_LOGIN>`. They do not include
`<STATUS>` or `<STATUS_CODE>`.

Connection events (`Connect`, `Quit`) use `<COMMAND_CLASS>` with the value
`connect` and include `<CONNECTION_TYPE>`. `Connect` records additionally
carry `<PRIV_USER>`, `<PROXY_USER>`, and `<DB>`.

If the client supplies connection attributes and the event carries them,
`CONNECTION_ATTRIBUTES` holds one `ATTRIBUTE` per attribute, each with a
`NAME` and `VALUE` child element.

`Command Start` / `Command End` (FULL mode only) bracket every client
command (`Query`, `Ping`, `Quit`). Their `<COMMAND_CLASS>` holds the
`COM_*` command text (for example `Query`, `Ping`, `Quit`). They include
`<STATUS>` and `<CONNECTION_ID>` but not `<HOST>`, `<IP>`, `<USER>`, or
`<OS_LOGIN>`.

`Query Start` / `Query Status End` and their nested variants
`Query Nested Start` / `Query Nested Status End` (FULL mode only) bracket
a single SQL statement execution. They carry `<STATUS>`,
`<CONNECTION_ID>`, `<COMMAND_CLASS>`, and `<SQLTEXT>` but not `<HOST>`,
`<IP>`, `<USER>`, or `<OS_LOGIN>`.

`Preparse` / `Postparse` (FULL mode only) fire before and after SQL
parsing. They carry `<COMMAND_CLASS>` set to `Parse`, `<FLAGS>`,
`<SQLTEXT>`, and `<REWRITTEN_QUERY>`.

`Execute` (FULL mode only) fires when a stored program is invoked. It
carries `<COMMAND_CLASS>` set to `Stored Program`, `<DB>`, and
`<STORED_PROGRAM>`.

`Variable Get` / `Variable Set` (FULL mode only) fire on global variable
reads and writes. They carry `<COMMAND_CLASS>`, `<VARIABLE_NAME>`, and
`<VARIABLE_VALUE>`.

Authentication subclass events (FULL mode only) include
`Pre Authenticate`, `Auth Credential Change`, `Auth Authid Rename`,
`Auth Authid Drop`, and `Auth Flush`. They use `<COMMAND_CLASS>` set to
`Authentication` (or `connect` for `Pre Authenticate`) and include
`<STATUS>`, `<USER>`, and `<HOST>`.

Empty field values use self-closing XML tags (`<TAG/>`) instead of empty
tag pairs (`<TAG></TAG>`). Fields affected include `USER`, `OS_LOGIN`,
`HOST`, `IP`, `COMMAND_CLASS`, `PRIV_USER`, `PROXY_USER`, and `DB`.

Record IDs (`<RECORD_ID>`) are 1-based. The indentation uses 1 space per
nesting level: `<AUDIT_RECORD>` is indented by 1 space, child elements
by 2, nested children by 3, and deepest elements by 4.

## Mandatory elements

These appear on every `<AUDIT_RECORD>` in this format:

| Element | Description |
| --- | --- |
| `<NAME>` | Event subclass string. REDUCED mode: `Audit`, `Connect`, `Query`, `Ping`, `TableRead`, `TableInsert`, `TableUpdate`, `TableDelete`, `Message`, `Quit`, `NoAudit`. FULL mode adds: `Pre Authenticate`, `Command Start`, `Command End`, `Preparse`, `Postparse`, `Query Start`, `Query Status End`, `Query Nested Start`, `Query Nested Status End`, `Execute`, `Variable Get`, `Variable Set`, `Auth Credential Change`, `Auth Authid Rename`, `Auth Authid Drop`, `Auth Flush`. |
| `<RECORD_ID>` | Sequence number and timestamp (see [`audit_log_filter` file handling](reading-audit-log-filter-files.md)); format `SEQ_TIMESTAMP` where the timestamp part matches the formatter’s timestamp string. |
| `<TIMESTAMP>` | Local date and time for the event. |

## Optional elements (by record category)

Many elements appear only for specific event classes. The following table lists
elements used by the NEW XML formatter from Percona Server for MySQL 8.4.9-9 onward for at least one
event type. It is not a promise that every field appears in every record.

| Element | Description |
| --- | --- |
| `<COMMAND_CLASS>` | Meaning depends on the record: connection events (`Connect`, `Quit`) use `connect`; table-access and query events use the SQL command name (for example `select`, `insert`, `create_table`, `set_option`); message events use the message type (`internal`, `user`); command lifecycle events use the COM name (`Query`, `Ping`, `Quit`); parse events use `Parse`; stored-program events use `Stored Program`; authentication events use `Authentication`. Empty (`<COMMAND_CLASS/>`) on `Ping` records. |
| `<CONNECTION_ID>` | Client connection ID. |
| `<CONNECTION_ATTRIBUTES>` | Nested `ATTRIBUTE` elements, each with `NAME` and `VALUE`. Omitted if there are no attributes. |
| `<CONNECTION_TYPE>` | Connection security / transport (for example `TCP/IP`, `SSL`, `Socket`). |
| `<STATUS>` | Status code (`0` for success, non-zero for failure). Present on `Query`, `Connect`, `Quit`, `Ping`, `Message`, and authentication records. Also on `Command Start`/`End`, `Query Start`/`Status End` in FULL mode. Not present on table-access records. |
| `<STATUS_CODE>` | High-level status (`0` for success, `1` for failure). Present alongside `<STATUS>` on `Query`, `Connect`, `Quit`, `Ping`, and `Message` records. |
| `<SQLTEXT>` | Statement or digest text when the event carries SQL text. |
| `<HOST>`, `<IP>`, `<USER>` | Client context. Present on `Query`, `Connect`, `Quit`, `Ping`, table-access, `Message`, `Pre Authenticate`, and authentication records. Not emitted on `Command Start`/`End`, `Query Start`/`Status End`, `Preparse`/`Postparse`, `Execute`, or `Variable` records. |
| `<OS_LOGIN>` | External user from authentication (`external_user`). Present on `Query`, `Connect`, `Quit`, `Ping`, table-access, `Message`, and `Pre Authenticate` records. |
| `<PRIV_USER>`, `<PROXY_USER>`, `<DB>` | Included on `Connect` records. |
| `<SERVER_ID>` | On `Audit` and `NoAudit` records. |
| `<VERSION>` | Audit log format version. On `Audit` (startup) records. |
| `<STARTUP_OPTIONS>` | Server command-line arguments as a single string. On `Audit` (startup) records. |
| `<OS_VERSION>` | Operating system and architecture. On `Audit` (startup) records. |
| `<MYSQL_VERSION>` | Server version string. On `Audit` (startup) records. |
| `<DB>`, `<TABLE>` | Database and table name on table-access records (`TableRead`, `TableInsert`, `TableUpdate`, `TableDelete`). `<DB>` also appears on `Execute` (stored program) records. |
| `<VARIABLE_NAME>`, `<VARIABLE_VALUE>` | Global variable audit events (`Variable Get`, `Variable Set`). FULL mode only. |
| `<STORED_PROGRAM>` | Stored program name on `Execute` events (`<DB>` also appears). FULL mode only. |
| `<FLAGS>`, `<REWRITTEN_QUERY>` | Parse events (`Preparse`, `Postparse`). `<SQLTEXT>` also appears. FULL mode only. |
| `<COMPONENT>`, `<PRODUCER>`, `<MESSAGE>`, `<MAP>` | Message events. `<MAP>` contains `<ELEMENT>` children, each with a `<KEY>` and `<VALUE>`. Message events also include `<USER>`, `<OS_LOGIN>`, `<HOST>`, `<IP>`, `<STATUS>`, and `<STATUS_CODE>` fields. |

Characters such as `<`, `>`, `&`, and `"` in element text are XML-escaped by
the component. Very long values may be truncated according to server-side
limits.
