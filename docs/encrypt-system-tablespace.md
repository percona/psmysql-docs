# Encrypt system tablespace

By default, the system tablespace, which contains the system database and the data dictionary tables, is unencrypted. To change the encryption requires the `CREATE TABLESPACE` privilege on all tables in the instance.

In an `ALTER TABLESPCE` statement, add the `ENCRYPTION` option with the tablespace name to enable encryption.

```{.bash data-prompt="mysql>"}
mysql> ALTER TABLESPACE mysql ENCRYPTION='Y';
```
Disable encryption by setting the `ENCRYPTION` option to 'N".

```{.bash data-prompt="mysql>"}
mysql> ALTER TABLESPACE mysql ENCRYPTION='N';
```
