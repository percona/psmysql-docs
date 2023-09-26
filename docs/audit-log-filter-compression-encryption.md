# Audit Log Filter compression and encryption

The feature is in [tech preview](glossary.md#tech-preview).

## Compression

You can enable compression for any [format](audit-log-filter-formats.md) by setting the `audit_log_filter_compression` system variable when the server starts.

The `audit_log_filter_compression` variable can be either of the following:

* NONE (no compression) - the default value
* GZIP - uses the GNU Zip compression

If compression and encryption are enabled, the plugin applies compression before encryption. If you must manually recover a file with both settings, first decrypt the file and then uncompress the file.

## Encryption

You can encrypt any audit log filter file in any [format](audit-log-filter-formats.md). The audit log filter plugin generates the initial password, but you can use user-defined passwords after that. The plugin stores the passwords in the keyring, so that feature must be enabled.

Set the `audit_log_filter_encryption` system variable with the server starts. The allowed values are the following:

* NONE - no encryption, the default value
* AES - AES-256-CBC (Cipher Block Chaining) encryption

The AES uses the 256-bit key size.

The following audit log filter functions are used with encryption:

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
				<th>Function name</th>
				<th>Description</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>audit_log_encryption_password_set()</td>
				<td>Stores the password in the keyring. If encryption is enabled, the function also rotates the log file by renaming the current log file and creating a log file encrypted with the password.</td>
			</tr>
			<tr>
				<td>audit_log_encryption_password_get()</td>
				<td>Invoking this function without an argument returns the current encryption password. An argument that specifies the keyring ID of an archived password or current password returns that password by ID.</td>
			</tr>
		</tbody>
	</table>
</body>
</html>

The `audit_log_filter_password_history_keep_days` variable is used with encryption. If the variable is not zero (0) , invoking `audit_log_encryption_password_set()` causes the expiration of archived audit log passwords.

When the plugin starts with encryption enabled, the plugin checks if the keyring has an audit log filter encryption password. If no password is found, the plugin generates a random password and stores this password in the keyring. Use `audit_log_encryption_password_get()` to review this password.

If compression and encryption are enabled, the plugin applies compression before encryption. If you must manually recover a file with both settings, first decrypt the file and then uncompress the file.

## Manually uncompressing and decrypting audit log filter files

To decrypt an encrypted log file, use the openssl command. For example:

```bash
openssl enc -d -aes-256-cbc -pass pass:password
    -iter iterations -md sha256
    -in audit.timestamp.log.pwd_id.enc
    -out audit.timestamp.log
```

To execute that command, you must obtain a password and iterations. To do this, use `audit_log_encryption_password_get()`. 

This function gets the encryption password, and the iterations count and returns this data as a JSON-encoded string. For example, if the audit log file name is `audit.20190415T151322.log.20190414T223342-2.enc`, the password ID is `20190414T223342-2` and the keyring ID is `audit-log-20190414T223342-2`. 

Get the keyring password:

```mysql
mysql> SELECT audit_log_encryption_password_get('audit-log-20190414T223342-2');
```

The return value of this function may look like the following:

??? example "Expected output"
    ```text
    {"password":"6i1Nx35CKMIaQaFzBrDzLpCq6gC","iterations":568977}
    ```