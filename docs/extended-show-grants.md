# Review effective privileges with SHOW EFFECTIVE GRANTS

In MySQL, `SHOW GRANTS` has the following limitations:

* Shows only explicitly granted privileges

* Does not show inherited anonymous user privileges

* Does not show privileges inherited through roles unless the USING clause is specified

Other privileges might be available to the account but are not displayed. For example:

```sql
-- Create named and anonymous users
CREATE USER 'user1'@'localhost';
CREATE USER ''@'localhost';

-- Grant privilege to anonymous user
GRANT SELECT ON db.* TO ''@'localhost';
```

```sql
-- Check user1's grants
SHOW GRANTS FOR 'user1'@'localhost';
```
??? example "Expected output"

    ```text
    GRANT USAGE ON *.* TO 'user1'@'localhost'
    ```



Even though 'user1'@'localhost' can use `SELECT on db.*`, this privilege does not appear in `SHOW GRANTS`.

Percona Server for MySQL's `SHOW EFFECTIVE GRANTS` command provides a comprehensive view of a user's permissions. It reveals not only the privileges directly granted to the user but also those inherited from other accounts, such as anonymous users or roles. This includes system-level, database-level, and table-level privileges, giving you a complete picture of the user's access rights within the database.

The benefits are:

* Shows complete privilege picture

* Helps identify privilege sources

* Simplifies security audits

* Makes troubleshooting easier

* Reveals inherited privileges

## Example

If we create the following users:

```sql
CREATE USER grantee@localhost IDENTIFIED BY 'grantee1';
```

??? example "Expected output"

    ```text
    Query OK, 0 rows affected (0.50 sec)
    ```

```sql
CREATE USER grantee IDENTIFIED BY 'grantee2';
```

??? example "Expected output"

    ```text
    Query OK, 0 rows affected (0.09 sec)
    ```

```sql
CREATE DATABASE db2;
```

??? example "Expected output"

    ```text
    Query OK, 1 row affected (0.20 sec)
    ```

```sql
GRANT ALL PRIVILEGES ON db2.* TO grantee WITH GRANT OPTION;
```

??? example "Expected output"

    ```text
    Query OK, 0 rows affected (0.12 sec)
    ```

* `SHOW EFFECTIVE GRANTS` output before the change:

```sql
SHOW EFFECTIVE GRANTS;
```

??? example "Expected output"

    ```text
    +----------------------------------------------------------------------------------------------------------------+
    | Grants for grantee@localhost                                                                                   |
    +----------------------------------------------------------------------------------------------------------------+
    | GRANT USAGE ON *.* TO 'grantee'@'localhost' IDENTIFIED BY PASSWORD '*9823FF338D44DAF02422CF24DD1F879FB4F6B232' |
    +----------------------------------------------------------------------------------------------------------------+
    1 row in set (0.04 sec)
    ```

Although the grant for the `db2` database isn’t shown, `grantee` user has enough privileges to create the table in that database:

```shell
user@trusty:~mysql -ugrantee -pgrantee1 -h localhost
```

```sql
CREATE TABLE db2.t1(a int);
```

??? example "Expected output"

    ```text
    Query OK, 0 rows affected (1.21 sec)
    ```

* The output of `SHOW EFFECTIVE GRANTS` after the change shows all
the privileges for the `grantee` user:

```sql
SHOW EFFECTIVE GRANTS;
```

??? example "Expected output"

    ```text
    +-------------------------------------------------------------------+
    | Grants for grantee@localhost                                      |
    +-------------------------------------------------------------------+
    | GRANT USAGE ON *.* TO 'grantee'@'localhost' IDENTIFIED BY PASSWORD|
    | '*9823FF338D44DAF02422CF24DD1F879FB4F6B232'                       |
    | GRANT ALL PRIVILEGES ON `db2`.* TO 'grantee'@'%' WITH GRANT OPTION|
    +-------------------------------------------------------------------+
    2 rows in set (0.00 sec)
    ```
  
