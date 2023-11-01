# Audit Log Filter file naming conventions

The feature is in [tech preview](glossary.md#tech-preview).

## Name qualities

The audit log filter file name has the following qualities:

* Optional directory name
* Base name
* Optional suffix

Using either [compression](audit-log-filter-compression-encryption.md) or [encryption](audit-log-filter-compression-encryption.md) adds the following suffixes:

* Compression adds the `.gz` suffix
* Encryption adds the `pwd_id.enc` suffix

The `pwd_id` represents the password used for encrypting the log files. The audit log filter plugin stores passwords in the keyring.

You can combine compression and encryption, which adds both suffixes to the `audit_filter.log` name.

The following table displays the possible ways a file can be named:

<!DOCTYPE html>
<html>
<head>
	<title>HTML Table Generator</title> 
	<style>
		table {
			border:1px solid #b3adad;
			border-collapse:collapse;
			padding:5px;
		}
		table th {
			border:1px solid #b3adad;
			padding:5px;
			background: #f0f0f0;
			color: #313030;
		}
		table td {
			border:1px solid #b3adad;
			text-align:center;
			padding:5px;
			background: #ffffff;
			color: #313030;
		}
	</style>
</head>
<body>
	<table>
		<thead>
			<tr>
				<th>Default name</th>
				<th>Enabled feature</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>audit.log&nbsp;</td>
				<td>No compression or encryption&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;audit.log.gz</td>
				<td>Compression&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;audit.log.pwd_id.enc</td>
				<td>&nbsp;Encryption</td>
			</tr>
			<tr>
				<td>audit.log.gz.pwd_id.enc&nbsp;</td>
				<td>Compression, encryption&nbsp;</td>
			</tr>
		</tbody>
	</table>
</body>
</html>

### Encryption ID format

The format for `pwd_id` is the following:

* A UTC value in `YYYYMMDDThhmmss` format that represents when the password was created
* A sequence number that starts at `1` and increases if passwords have the same timestamp value

The following are examples of pwd_id values:

```text
20230417T082215-1
20230301T061400-1
20230301T061400-2
```

The following example is a list of the audit log filter files with the `pwd_id`:

```text
audit_filter.log.20230417T082215-1.enc
audit_filter.log.20230301T061400-1.enc
audit_filter.log.20230301T061400-2.enc
```

The current password has the largest sequence number.

## Renaming operations

During initialization, the plugin checks if a file with that name exists. 
If it does, the plugin renames the file. The plugin writes to an empty file.

During termination, the plugin renames the file.


