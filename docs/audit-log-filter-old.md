# Audit Log Filter format - XML (old style)

!!! note "Deprecation notice"

    The OLD XML format (`audit_log_filter.format=OLD`) is deprecated and may be removed in a later version. Use [XML (new style)](audit-log-filter-new.md), [JSON, or JSONL](audit-log-filter-json.md) instead.

OLD XML wraps records in `<AUDIT>` … `</AUDIT>`. Each event is one `<AUDIT_RECORD>` (attribute-style XML).

Attribute order varies. Every record includes the attributes listed under [Required attributes](#required-attributes). Other attributes are optional by event type.

```xml
<?xml version="1.0" encoding="utf-8"?>
<AUDIT>
  <AUDIT_RECORD
    NAME="Audit"
    RECORD_ID="0_2023-03-29T11:15:52"
    TIMESTAMP="2023-03-29T11:15:52"
    SERVER_ID="1"/>
  <AUDIT_RECORD
    NAME="Command Start"
    RECORD_ID="1_2023-03-29T11:15:53"
    TIMESTAMP="2023-03-29T11:15:53"
    STATUS="0"
    CONNECTION_ID="1"
    COMMAND_CLASS="query"/>
  <AUDIT_RECORD
    NAME="Query"
    RECORD_ID="2_2023-03-29T11:15:53"
    TIMESTAMP="2023-03-29T11:15:53"
    COMMAND_CLASS="create_table"
    CONNECTION_ID="11"
    HOST="localhost"
    IP=""
    USER="root[root] @ localhost []"
    OS_LOGIN=""
    SQLTEXT="CREATE TABLE t1 (c1 INT)"
    STATUS="0"/>
  <AUDIT_RECORD
    NAME="Query Start"
    RECORD_ID="3_2023-03-29T11:15:53"
    TIMESTAMP="2023-03-29T11:15:53"
    STATUS="0"
    CONNECTION_ID="11"
    COMMAND_CLASS="create_table"
    SQLTEXT="CREATE TABLE t1 (c1 INT)"/>
  <AUDIT_RECORD
    NAME="Query Status End"
    RECORD_ID="4_2023-03-29T11:15:53"
    TIMESTAMP="2023-03-29T11:15:53"
    STATUS="0"
    CONNECTION_ID="11"
    COMMAND_CLASS="create_table"
    SQLTEXT="CREATE TABLE t1 (c1 INT)"/>
  <AUDIT_RECORD
    NAME="Query"
    RECORD_ID="5_2023-03-29T11:15:53"
    TIMESTAMP="2023-03-29T11:15:53"
    COMMAND_CLASS="create_table"
    CONNECTION_ID="11"
    HOST="localhost"
    IP=""
    USER="root[root] @ localhost []"
    OS_LOGIN=""
    SQLTEXT="CREATE TABLE t1 (c1 INT)"
    STATUS="0"/>
  <AUDIT_RECORD
    NAME="Command End"
    RECORD_ID="6_2023-03-29T11:15:53"
    TIMESTAMP="2023-03-29T11:15:53"
    STATUS="0"
    CONNECTION_ID="1"
    COMMAND_CLASS="query"/>
</AUDIT>
```

### Required attributes

| Attribute | Description |
| --- | --- |
| `NAME` | Action that produced the record |
| `RECORD_ID` | Sequence number and timestamp; sequence resets when the component opens the log file |
| `TIMESTAMP` | Event date and time |

### Optional attributes

| Attribute | Description |
| --- | --- |
| `COMMAND_CLASS` | Action or command class |
| `CONNECTION_ID` | Client connection ID |
| `CONNECTION_TYPE` | Connection security / transport |
| `DB` | Database name |
| `HOST` | Client host name |
| `IP` | Client IP address |
| `OS_LOGIN` | External auth user (for example LDAP); empty for built-in auth |
| `PRIV_USER` | Privilege check user (may differ from `USER`) |
| `PROXY_USER` | Proxy user if used; otherwise empty |
| `SERVER_ID` | Server ID |
| `SQLTEXT` | SQL text |
| `STATUS` | `0` success, non-zero error |
| `TABLE` | Table name |
| `USER` | Client user (may differ from `PRIV_USER`) |

## Additional reading

* [Audit Log Filter file format overview](audit-log-filter-formats.md)
* [Audit Log Filter format - XML (new style)](audit-log-filter-new.md)
* [Audit Log Filter format - JSON and JSONL](audit-log-filter-json.md)
* [Audit log filter functions, options, and variables](audit-log-filter-variables.md)
* [Audit Log Filter overview](audit-log-filter-overview.md)