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


  <!DOCTYPE html>
  <html>
<head>
	<title>HTML Table Generator</title> 
	<style>
		table {
			width:150%;
			height:100%;
			border:1px solid #b3adad;
			border-collapse:collapse;
			padding:1px;
		}
		table th {
			border:1px solid #b3adad;
			padding:1px;
			background: #f0f0f0;
			color: #313030;
		}
		table td {
			border:1px solid #b3adad;
			text-align:left;
			padding:1px;
			background: #ffffff;
			color: #313030;
		}
	</style>
</head>
<body>
	<table>
		<thead>
			<tr>
				<th>Attribute Name</th>
				<th>Description</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>&nbsp;&lt;NAME&gt;</td>
				<td>The action that generated the audit record.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;RECORD_ID&gt;</td>
				<td>The &lt;RECORD_ID&gt; consists of a sequence number and a timestamp value. The sequence number is initialized when the component opens the audit log filter file.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;TIMESTAMP&gt;</td>
				<td>Displays the date and time when the audit event happened.</td>
			</tr>
		</tbody>
	</table>
</body>
</html>
The optional attributes are the following:

  <!DOCTYPE html>
  <html>
<head>
	<title>HTML Table Generator</title> 
	<style>
		table {
			width:150%;
			height:100%;
			border:1px solid #b3adad;
			border-collapse:collapse;
			padding:1px;
		}
		table th {
			border:1px solid #b3adad;
			padding:1px;
			background: #f0f0f0;
			color: #313030;
		}
		table td {
			border:1px solid #b3adad;
			text-align:left;
			padding:1px;
			background: #ffffff;
			color: #313030;
		}
	</style>
</head>
<body>
	<table>
		<thead>
			<tr>
				<th>Attribute Name</th>
				<th>Description</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>&nbsp;&lt;COMMAND_CLASS&gt;</td>
				<td>Contains the type of performed action.&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;CONNECTION_ID&gt;</td>
				<td>Contains the client connection identifier.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;CONNECTION_ATTRIBUTES&gt;</td>
				<td>Contains the client connection attributes. Each attribute has a &lt;NAME&gt; and &lt;VALUE&gt; pair.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;CONNECTION_TYPE&gt;</td>
				<td>Contains the type of connection security.&nbsp;<br></td>
			</tr>
			<tr>
				<td>&nbsp;&lt;DB&gt;</td>
				<td>Contains the database name.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;HOST&gt;</td>
				<td>Contains the client's hostname.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;IP&gt;</td>
				<td>Contains the client's IP address.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;MYSQL_VERSION&gt;</td>
				<td>Contains the MySQL server version.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;OS_LOGIN&gt;</td>
				<td>Contains the user name used during an external authentication, for example, if the user is authenticated through an LDAP component. If the authentication component does not set a value or the user is authenticated using MySQL authentication, this value is empty.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;OS_VERSION&gt;</td>
				<td>Contains the server's operating system.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;PRIV_USER&gt;</td>
				<td>Contains the user name used by the server when checking privileges. This name may be different than &lt;USER&gt;.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;PROXY_USER&gt;</td>
				<td>Contains the proxy user. If a proxy is not used, the value is empty.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;SERVER_ID&gt;</td>
				<td>Contains the server ID.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;SQLTEXT&gt;</td>
				<td>Contains the text of the SQL statement.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;STARTUP_OPTIONS&gt;</td>
				<td>Contains the startup options. These options may be provided by the command line or files.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;STATUS&gt;</td>
				<td>Contains the status of a command. A 0 (zero) is a success. A nonzero value is an error.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;STATUS_CODE&gt;</td>
				<td>Contains the status of a command, which either succeeds (0) or an error occurred (1).</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;TABLE&gt;</td>
				<td>Contains the table name.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;USER&gt;</td>
				<td>Contains the user name from the client. This name may be different than &lt;PRIV_USER&gt;.</td>
			</tr>
			<tr>
				<td>&nbsp;&lt;VERSION&gt;</td>
				<td>Contains the audit log filter format.</td>
			</tr>
		</tbody>
	</table>
</body>
</html>