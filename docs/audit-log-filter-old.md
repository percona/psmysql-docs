# Audit Log Filter format - XML (old style)

The old style XML format uses `<AUDIT>` tag as the root element and adds the `</AUDIT>` tag when the file closes. Each audited event is contained in an <AUDIT_RECORD> element. 

The order of the attributes within an <AUDIT_RECORD> can vary. Certain attributes are in every element. Other attributes are optional and depend on the type of audit record.

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

The required attributes are the following:

<!DOCTYPE html>
<html>
<head>
	<title>HTML Table Generator</title> 
	<style>
		#demTable {
			width:100%;
			height:100%;
			border:1px solid #b3adad;
			border-collapse:collapse;
			padding:5px;
		}
		#demTable th {
			border:1px solid #b3adad;
			padding:5px;
			background: #f0f0f0;
			color: #313030;
		}
		#demTable td {
			border:1px solid #b3adad;
			text-align:left;
			padding:5px;
			background: #ffffff;
			color: #313030;
		}
	</style>
</head>
<body>
	<table id="demTable">
		<thead>
			<tr>
				<th><div style="class: fitwidth, color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Attribute Name</div></th>
				<th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Description</div></th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>&nbsp;NAME</td>
				<td>&nbsp;The action that generated the audit record.</td>
			</tr>
			<tr>
				<td>&nbsp;RECORD_ID</td>
				<td>&nbsp;The RECORD_ID consists of a sequence number and a timestamp value. The sequence number is initialized when the component opens the audit log filter file.</td>
			</tr>
			<tr>
				<td>&nbsp;TIMESTAMP</td>
				<td>&nbsp;Displays the date and time when the audit event happened.</td>
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
		#demTable {
			width:100%;
			height:100%;
			border:1px solid #b3adad;
			border-collapse:collapse;
			padding:5px;
		}
		#demTable th {
			border:1px solid #b3adad;
			padding:5px;
			background: #f0f0f0;
			color: #313030;
		}
		#demTable td {
			border:1px solid #b3adad;
			text-align:left;
			padding:5px;
			background: #ffffff;
			color: #313030;
		}
	</style>
</head>
<body>
	<table id="demTable">
		<thead>
			<tr>
				<th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Attribute Name</div></th>
				<th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Description</div></th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td><span style="font-family: -apple-system, &quot;system-ui&quot;, &quot;Segoe WPC&quot;, &quot;Segoe UI&quot;, system-ui, Ubuntu, &quot;Droid Sans&quot;, sans-serif; font-size: 14px; font-style: normal; font-weight: 400;">COMMAND_CLASS</span><br></td>
				<td>Type of action performed</td>
			</tr>
			<tr>
				<td>CONNECTION_ID</td>
				<td>Client connection identifier</td>
			</tr>
			<tr>
				<td>CONNECTION_TYPE</td>
				<td>Connection security type</td>
			</tr>
			<tr>
				<td>DB</td>
				<td>Database name</td>
			</tr>
			<tr>
				<td>HOST</td>
				<td>Client's hostname</td>
			</tr>
			<tr>
				<td>IP</td>
				<td>Client's IP address</td>
			</tr>
			<tr>
				<td>MYSQL_VERSION</td>
				<td>Server version</td>
			</tr>
			<tr>
				<td>OS_LOGIN</td>
				<td>The user name used during an external authentication, for example, if the user is authenticated through an LDAP component. If the authentication component does not set a value or the user is authenticated using MySQL authentication, this value is empty.</td>
			</tr>
			<tr>
				<td>OS_VERSION</td>
				<td>Server's operating system</td>
			</tr>
			<tr>
				<td>PRIV_USER</td>
				<td>The user name used by the server when checking privileges. This name may be different than USER.</td>
			</tr>
			<tr>
				<td>PROXY_USER</td>
				<td>The proxy user. If a proxy is not used, the value is empty.</td>
			</tr>
			<tr>
				<td>SERVER_ID</td>
				<td>Server Identifier</td>
			</tr>
			<tr>
				<td>SQLTEXT</td>
				<td>SQL statement text</td>
			</tr>
			<tr>
				<td>STARTUP_OPTIONS</td>
				<td>Server startup options, either command line or config files</td>
			</tr>
			<tr>
				<td>STATUS</td>
				<td>Command's status - a 0 (zero) is a success, a non-zero is an error</td>
			</tr>
			<tr>
				<td>STATUS_CODE</td>
				<td><span style="font-style: normal; font-weight: 400;">A 0 (zero) is a success, a non-zero is an error</span><br></td>
			</tr>
			<tr>
				<td>TABLE</td>
				<td>Table name</td>
			</tr>
			<tr>
				<td>USER</td>
				<td>&nbsp;Client's user name - this name may be different than PRIV_USER.</td>
			</tr>
			<tr>
				<td>VERSION</td>
				<td>Format of audit log filter</td>
			</tr>
		</tbody>
	</table>
</body>
</html>