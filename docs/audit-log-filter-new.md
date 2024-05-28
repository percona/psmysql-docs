# Audit Log Filter format - XML (new style)

The filter writes the audit log filter file in XML. The XML file uses 
UTF-8.

The <AUDIT> is the root element and this element contains 
<AUDIT_RECORD> elements. Each <AUDIT_RECORD> element contains specific 
information about an event that is audited. 

For each new file, the Audit Log Filter component writes the XML 
declaration and the root element tag. The component writes the closing 
</AUDIT> root element when closing the file. If the file is open, this 
closing element is not available.

```xml

<?xml version="1.0" encoding="utf-8"?>
<AUDIT>
    <AUDIT_RECORD>
        <NAME>Audit</NAME>
        <RECORD_ID>0_2023-03-29T11:11:43</RECORD_ID>
        <TIMESTAMP>2023-03-29T11:11:43</TIMESTAMP>
        <SERVER_ID>1</SERVER_ID>
    </AUDIT_RECORD>
    <AUDIT_RECORD>
        <NAME>Command Start</NAME>
        <RECORD_ID>1_2023-03-29T11:11:45</RECORD_ID>
        <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
        <STATUS>0</STATUS>
        <CONNECTION_ID>1</CONNECTION_ID>
        <COMMAND_CLASS>query</COMMAND_CLASS>
    </AUDIT_RECORD>
    <AUDIT_RECORD>
        <NAME>Query</NAME>
        <RECORD_ID>2_2023-03-29T11:11:45</RECORD_ID>
        <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
        <COMMAND_CLASS>create_table</COMMAND_CLASS>
        <CONNECTION_ID>11</CONNECTION_ID>
        <HOST>localhost</HOST>
        <IP></IP>
        <USER>root[root] @ localhost []</USER>
        <OS_LOGIN></OS_LOGIN>
        <SQLTEXT>CREATE TABLE t1 (c1 INT)</SQLTEXT>
        <STATUS>0</STATUS>
    </AUDIT_RECORD>
    <AUDIT_RECORD>
        <NAME>Query Start</NAME>
        <RECORD_ID>3_2023-03-29T11:11:45</RECORD_ID>
        <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
        <STATUS>0</STATUS>
        <CONNECTION_ID>11</CONNECTION_ID>
        <COMMAND_CLASS>create_table</COMMAND_CLASS>
        <SQLTEXT>CREATE TABLE t1 (c1 INT)</SQLTEXT>
    </AUDIT_RECORD>
    <AUDIT_RECORD>
        <NAME>Query</NAME>
        <RECORD_ID>4_2023-03-29T11:11:45</RECORD_ID>
        <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
        <COMMAND_CLASS>create_table</COMMAND_CLASS>
        <CONNECTION_ID>11</CONNECTION_ID>
        <HOST>localhost</HOST>
        <IP></IP>
        <USER>root[root] @ localhost []</USER>
        <OS_LOGIN></OS_LOGIN>
        <SQLTEXT>CREATE TABLE t1 (c1 INT)</SQLTEXT>
        <STATUS>0</STATUS>
    </AUDIT_RECORD>
    <AUDIT_RECORD>
        <NAME>Command End</NAME>
        <RECORD_ID>5_2023-03-29T11:11:45</RECORD_ID>
        <TIMESTAMP>2023-03-29T11:11:45</TIMESTAMP>
        <STATUS>0</STATUS>
        <CONNECTION_ID>1</CONNECTION_ID>
        <COMMAND_CLASS>query</COMMAND_CLASS>
    </AUDIT_RECORD>
</AUDIT>
```

The order of the attributes within an <AUDIT_RECORD> can vary. Certain attributes are in every element. Other attributes are optional and depend on the type of audit record.

The attributes in every element are the following:

| Attribute Name | Description                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `<NAME>`       | The action that generated the audit record.                                                                                                            |
| `<RECORD_ID>`  | The `<RECORD_ID>` consists of a sequence number and a timestamp value. The sequence number is initialized when the component opens the audit log filter file. |
| `<TIMESTAMP>`  | Displays the date and time when the audit event happened.                                                                                              |

The optional attributes are the following:

| Attribute Name          | Description            |
| ----------------------- | ---------------------- |
| `<COMMAND_CLASS>`       | Contains the type of performed action.                                                         |
| `<CONNECTION_ID>`       | Contains the client connection identifier.                                                     |
| `<CONNECTION_ATTRIBUTES>`| Contains the client connection attributes. Each attribute has a `<NAME>` and `<VALUE>` pair.  |
| `<CONNECTION_TYPE>`     | Contains the type of connection security.                                                      |
| `<DB>`                  | Contains the database name.                                                                    |
| `<HOST>`                | Contains the client's hostname.                                                                |
| `<IP>`                  | Contains the client's IP address.                                                              |
| `<MYSQL_VERSION>`       | Contains the MySQL server version.                                                             |
| `<OS_LOGIN>`            | Contains the user name used during an external authentication, for example, if the user is authenticated through an LDAP component. If the authentication component does not set a value or the user is authenticated using MySQL authentication, this value is empty.               |
| `<OS_VERSION>`          | Contains the server's operating system.                                                        |
| `<PRIV_USER>`           | Contains the user name used by the server when checking privileges. This name may be different than `<USER>`.     |
| `<PROXY_USER>`          | Contains the proxy user. If a proxy is not used, the value is empty.                           |
| `<SERVER_ID>`           | Contains the server ID.                                                                        |
| `<SQLTEXT>`             | Contains the text of the SQL statement.                                                        |
| `<STARTUP_OPTIONS>`     | Contains the startup options. These options may be provided by the command line or files.      |
| `<STATUS>`              | Contains the status of a command. A 0 (zero) is a success. A nonzero value is an error.        |
| `<STATUS_CODE>`         | Contains the status of a command, which either succeeds (0) or an error occurred (1).          |
| `<TABLE>`               | Contains the table name.                                                                       |
| `<USER>`                | Contains the user name from the client. This name may be different than `<PRIV_USER>`.         |
| `<VERSION>`             | Contains the audit log filter format.                                                          |