# Audit Log Filter format - XML (new style)

Starting with Percona Server for MySQL 8.4.8-8 on the {{vers}} line, the following describes new-style XML (`audit_log_filter.format=NEW`) from the Audit Log Filter component: element names, typical fields, and formatter behavior were aligned to the server for that release. This documentation build targets {{release}} (bump on each publish). If you run an older {{vers}} build than 8.4.8-8, verify against your own audit log in case output differs. Implementation reference: `components/audit_log_filter/log_record_formatter/new.cc` and `base.cc`.

The Audit Log Filter component can write the audit log file as new-style XML
(`audit_log_filter.format=NEW`). The file uses UTF-8.

The root element is `<AUDIT>`. It contains `<AUDIT_RECORD>` elements. Each
`<AUDIT_RECORD>` describes one audited event.

For each new file, the component writes the XML declaration and the opening
`<AUDIT>` tag. When the file is closed, the component writes the closing
`</AUDIT>` tag. If the file is still open, that closing tag is not present yet.

Element order inside `<AUDIT_RECORD>` is not guaranteed (the writer may
emit fields in a fixed order in practice, but consumers should not depend on it).

Timestamps use the server local time zone, in `YYYY-MM-DDTHH:MM:SS`
form. They do not append a ` UTC` suffix to the timestamp string.

!!! note "NEW XML behavior (from 8.4.8-8, docs {{release}})"

    Audit logging on/off is recorded with `<NAME>` values `Startup` and
    `Shutdown`. The NEW formatter does not emit `STATUS_CODE`, and
    does not write `VERSION`, `STARTUP_OPTIONS`, `MYSQL_VERSION`, or
    `OS_VERSION` on the startup or shutdown audit record. Disconnect events
    use the name `Disconnect`.

## Example (illustrative)

The snippet below shows the shape of several record types. Exact sets of
elements depend on the event, filters, and server configuration.

```xml
<?xml version="1.0" encoding="utf-8"?>
<AUDIT>
 <AUDIT_RECORD>
  <NAME>Startup</NAME>
  <RECORD_ID>1_2023-03-29T11:11:43</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:43</TIMESTAMP>
  <COMMAND_CLASS>Audit</COMMAND_CLASS>
  <SERVER_ID>1</SERVER_ID>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Connect</NAME>
  <RECORD_ID>2_2023-03-29T11:11:44</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:44</TIMESTAMP>
  <COMMAND_CLASS>Connection</COMMAND_CLASS>
  <CONNECTION_ID>11</CONNECTION_ID>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <USER>root</USER>
  <OS_LOGIN/>
  <PRIV_USER>root</PRIV_USER>
  <PROXY_USER/>
  <DB>test</DB>
  <STATUS>0</STATUS>
  <CONNECTION_TYPE>TCP/IP</CONNECTION_TYPE>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Command Start</NAME>
  <RECORD_ID>3_2023-03-29T11:11:45</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>1</CONNECTION_ID>
  <COMMAND_CLASS>query</COMMAND_CLASS>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Query Start</NAME>
  <RECORD_ID>4_2023-03-29T11:11:45</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>11</CONNECTION_ID>
  <COMMAND_CLASS>create_table</COMMAND_CLASS>
  <SQLTEXT>CREATE TABLE t1 (c1 INT)</SQLTEXT>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Query Status End</NAME>
  <RECORD_ID>5_2023-03-29T11:11:45</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>11</CONNECTION_ID>
  <COMMAND_CLASS>create_table</COMMAND_CLASS>
  <SQLTEXT>CREATE TABLE t1 (c1 INT)</SQLTEXT>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Command End</NAME>
  <RECORD_ID>6_2023-03-29T11:11:45</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
  <STATUS>0</STATUS>
  <CONNECTION_ID>1</CONNECTION_ID>
  <COMMAND_CLASS>query</COMMAND_CLASS>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Disconnect</NAME>
  <RECORD_ID>7_2023-03-29T11:11:50</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:11:50</TIMESTAMP>
  <COMMAND_CLASS>Connection</COMMAND_CLASS>
  <CONNECTION_ID>11</CONNECTION_ID>
  <HOST>localhost</HOST>
  <IP>127.0.0.1</IP>
  <USER>root</USER>
  <OS_LOGIN/>
  <PRIV_USER>root</PRIV_USER>
  <PROXY_USER/>
  <DB>test</DB>
  <STATUS>0</STATUS>
  <CONNECTION_TYPE>TCP/IP</CONNECTION_TYPE>
 </AUDIT_RECORD>
 <AUDIT_RECORD>
  <NAME>Shutdown</NAME>
  <RECORD_ID>8_2023-03-29T11:12:00</RECORD_ID>
  <TIMESTAMP>2023-03-29T11:12:00</TIMESTAMP>
  <COMMAND_CLASS>Audit</COMMAND_CLASS>
  <SERVER_ID>1</SERVER_ID>
 </AUDIT_RECORD>
</AUDIT>
```

Query-class events (`Query Start`, `Query Status End`, nested variants, and
so on) include `STATUS`, `CONNECTION_ID`, `COMMAND_CLASS` (SQL
command name from the event), and often `SQLTEXT` (or digest text from
extended info). They do not include `HOST`, `IP`, `USER`, or
`OS_LOGIN` in NEW XML from 8.4.8-8 onward—those appear on connection
records (and on general records, which use subclasses such as `Log`,
`Error`, `Result`, `Status`, not the string `Query`).

Connection records use `COMMAND_CLASS` with the value `Connection`
(the event class label).

If the client supplies connection attributes and the event carries them,
`CONNECTION_ATTRIBUTES` holds one `ATTRIBUTE` per attribute, each with a
`NAME` and `VALUE` child element.

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
| `<NAME>` | Event subclass string (for example `Startup`, `Connect`, `Query Start`, `TableRead`). |
| `<RECORD_ID>` | Sequence number and timestamp (see [`audit_log_filter` file handling](reading-audit-log-filter-files.md)); format `SEQ_TIMESTAMP` where the timestamp part matches the formatter’s timestamp string. |
| `<TIMESTAMP>` | Local date and time for the event. |

## Optional elements (by record category)

Many elements appear only for specific event classes. The following table lists
elements used by the NEW XML formatter from Percona Server for MySQL 8.4.8-8 onward for at least one
event type. It is not a promise that every field appears in every record.

| Element | Description |
| --- | --- |
| `<COMMAND_CLASS>` | Meaning depends on the record: connection events use `Connection`; table-access events use `Table Access`; command events use the `COM_*` command text (`query`, and so on); query events use the SQL command name (for example `select`, `create_table`); general events use `General`. |
| `<CONNECTION_ID>` | Client connection ID. |
| `<CONNECTION_ATTRIBUTES>` | Nested `ATTRIBUTE` elements, each with `NAME` and `VALUE`. Omitted if there are no attributes. |
| `<CONNECTION_TYPE>` | Connection security / transport (for example `TCP/IP`, `SSL`, `Socket`). |
| `<STATUS>` | Status code for the event (for `Query` / `Command` / connection records, `0` success and non-zero for failure where applicable). |
| `<SQLTEXT>` | Statement or digest text when the event carries SQL text. |
| `<HOST>`, `<IP>`, `<USER>` | Client context on connection and general records (and on authentication records where applicable). Not emitted on `Query Start` / `Query Status End` style records in NEW XML. |
| `<OS_LOGIN>` | External user from authentication (`external_user`); on connection records from 8.4.8-8 onward (documented behavior). |
| `<PRIV_USER>`, `<PROXY_USER>`, `<DB>` | Included on connection records (including disconnect) from 8.4.8-8 onward (documented behavior). |
| `<SERVER_ID>` | On `Startup`, `Shutdown`, and similar audit records. |
| `<DB>`, `<TABLE>` | Database and table name on table-access records (`TableRead`, `TableInsert`, …). |
| `<VARIABLE_NAME>`, `<VARIABLE_VALUE>` | Global variable audit events. |
| `<STORED_PROGRAM>` | Stored program events (`DB` also appears). |
| `<FLAGS>`, `<REWRITTEN_QUERY>` | Parse events (`SQLTEXT` may appear). |
| `<COMPONENT>`, `<PRODUCER>`, `<MESSAGE>`, `<MAP>` | Message events. `<MAP>` contains `<ELEMENT>` children, each with a `<KEY>` and `<VALUE>`. Message events also include `<USER>`, `<OS_LOGIN>`, `<HOST>`, `<IP>`, `<STATUS>`, and `<STATUS_CODE>` fields. |

Characters such as `<`, `>`, `&`, and `"` in element text are XML-escaped by
the component. Very long values may be truncated according to server-side
limits.
