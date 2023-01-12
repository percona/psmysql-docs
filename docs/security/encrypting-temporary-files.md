# Encrypt temporary files

For InnoDB user-created temporary tables are created in a temporary tablespace
file and use the `innodb_temp_tablespace_encrypt` variable.

The `CREATE TEMPORARY TABLE` does not support the `ENCRYPTION` clause. The `TABLESPACE` clause cannot be set to `innodb_temporary`.

The global temporary tablespace datafile `ibtmp1` contains the temporary table
undo logs while intrinsic temporary tables and user-created temporary tables
are located in the encrypted session temporary tablespace.

To create new temporary tablespaces unencrypted, the following variables must
be set to `OFF` at runtime:

* `innodb_temp_tablespace_encrypt`

* `default_table_encryption`

Any existing encrypted user-created temporary files and intrinsic temporary
tables remain in an encrypted session.

Temporary tables are only destroyed when the session is disconnected.

The `default_table_encryption` setting in my.cnf determines if a temporary table is encrypted.

If the `innodb_temp_tablespace_encrypt` = “OFF” and the
`default_table_encryption` =”ON”, the user-created temporary tables are
encrypted. The temporary tablespace data file `ibtmp1`, which contains undo
logs, is not encrypted.

If the `innodb_temp_tablespace_encrypt` is “ON” for the system tablespace,
InnoDB generates an encryption key and encrypts the system's temporary
tablespace.  If you reset the encryption to “OFF”, all subsequent pages are
written to an unencrypted tablespace. Any generated keys are not erased to
allow encrypted tables and undo data to be decrypted.

For each temporary file, an encryption key has the following attributes:

* Generated locally

* Maintained in memory for the lifetime of the temporary file

* Discarded with the temporary file

## System variables

### `encrypt_tmp_files`

| Option       | Description         |
|--------------|---------------------|
| Command-line | --encrypt_tmp_files |
| Scope        | Global              |
| Dynamic      | No                  |
| Data type    | Boolean             |
| Default      | OFF                 |

This variable turns “ON” the encryption of temporary files created by the *Percona Server for MySQL*. The default value is `OFF`.

### `innodb_temp_tablespace_encrypt`

| Option       | Description                    |
|--------------|--------------------------------|
| Command-line | innodb-temp-tablespace-encrypt |
| Scope        | Global                         |
| Dynamic      | Yes                            |
| Data type    | Boolean                        |
| Default      | OFF                            |

When this variable is set to `ON`, the server encrypts the global temporary
tablespace and has the .ibtmp1 file extension and the session temporary tablespace and has the .ibt file extension. 

The variable does not enforce the encryption of currently open temporary files and does not rebuild the system's temporary tablespace to encrypt data that has already been written.
