# Extended `SHOW GRANTS`

In Oracle MySQL `SHOW GRANTS` displays only the privileges granted explicitly to the named account. Other privileges might be available to the account, but they are not displayed. For example, if an anonymous account exists, the named account might be able to use its privileges, but `SHOW GRANTS` will not display them. In *Percona Server for MySQL* `SHOW GRANTS` command was extended to display all the effectively available privileges to the account.

## Example

If we create the following users:

```sql
mysql> CREATE USER grantee@localhost IDENTIFIED BY 'grantee1';
```

The output should be similar to the following:

```text
Query OK, 0 rows affected (0.50 sec)
```

```sql
mysql> CREATE USER grantee IDENTIFIED BY 'grantee2';
```

The output should be similar to the following:

```text
Query OK, 0 rows affected (0.09 sec)
```

```sql
mysql> CREATE DATABASE db2;
```

The output should be similar to the following:

```text
Query OK, 1 row affected (0.20 sec)
```

```sql
mysql> GRANT ALL PRIVILEGES ON db2.* TO grantee WITH GRANT OPTION;
```

The output should be similar to the following:

```text
Query OK, 0 rows affected (0.12 sec)
```


* `SHOW GRANTS` output before the change:

```sql
mysql> SHOW GRANTS;
```

The output should be similar to the following:

```text
+----------------------------------------------------------------------------------------------------------------+
| Grants for grantee@localhost                                                                                   |
+----------------------------------------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'grantee'@'localhost' IDENTIFIED BY PASSWORD '*9823FF338D44DAF02422CF24DD1F879FB4F6B232' |
+----------------------------------------------------------------------------------------------------------------+
1 row in set (0.04 sec)
```

Although the grant for the `db2` database isn’t shown, `grantee` user has enough privileges to create the table in that database:

```sql
user@trusty:~$ mysql -ugrantee -pgrantee1 -h localhost
```

```sql
mysql> CREATE TABLE db2.t1(a int);
```

The output should be similar to the following:

```text
Query OK, 0 rows affected (1.21 sec)
```


* `SHOW GRANTS` output after the change shows all the privileges for the `grantee` user:

```sql
mysql> SHOW GRANTS;
```

The output should be similar to the following:

```text
+----------------------------------------------------------------------------------------------------------------+
| Grants for grantee@localhost                                                                                   |
+----------------------------------------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'grantee'@'localhost' IDENTIFIED BY PASSWORD '*9823FF338D44DAF02422CF24DD1F879FB4F6B232' |
| GRANT ALL PRIVILEGES ON `db2`.* TO 'grantee'@'%' WITH GRANT OPTION                                             |
+----------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

### Version-Specific Information

> 
> * Percona Server for MySQL 5.7.10-1:
> Feature ported from *Percona Server for MySQL* 5.6

### Other reading


* [#53645](http://bugs.mysql.com/bug.php?id=53645) - `SHOW GRANTS` not displaying all the applicable grants
