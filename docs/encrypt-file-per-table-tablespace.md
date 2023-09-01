# Encrypt File-Per-Table Tablespace

The file_per_table tablespace inherits the default schema encryption setting. Use the `ENCRYPTION` clause in the  in `CREATE TABLE` statement to explicitly set the encryption.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE ... ENCRYPTION='Y';
```
To change the encryption setting for an existing file_per_table tablespace, add the `ENCRYPTION` clause. The `ALTER TABLE` statement without the `ENCRYPTION` clause does not change the encryption state.

```{.bash data-prompt="mysql>"}
mysql> ALTER TABLE ... ENCRYPTION='Y';
```

If the `table_encryption_privilege_check` is enabled, the `TABLE_ENCRYPTION_ADMIN` privilige is required to change the file_per_table encryption setting from the default schema encryption. 
