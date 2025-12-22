# Additional PERFORMANCE_SCHEMA tables

This page lists the `performance_schema` tables added to standard *MySQL* by *Percona Server for MySQL* that don't exist elsewhere in the documentation.

## Account failed login lock status

### `performance_schema.account_failed_login_lock_status`

The `performance_schema.account_failed_login_lock_status` table is implemented in Percona Server for MySQL 8.0.44-35. This table exposes information about temporary account locking from the MySQL internal Access Control List (ACL) cache. 

This table is read-only. Users require global, per-database, or per-table `SELECT` privilege on this table to access its contents.

!!! note

    If an account is locked using the `CREATE USER` or `ALTER USER` statements with the `ACCOUNT LOCK` clause, this status is not captured in this table. The server records the `ACCOUNT LOCK` state in the `mysql.user` table.

| Column Name              | Data Type           | Description                                                                                                                                    |
|--------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `USER`                   | `CHAR(..)`          | Identifies the user account described by the table row                                                                                        |
| `HOST`                   | `CHAR(..)`          | Identifies the user account described by the table row                                                                                        |
| `IS_TRACKING_ACTIVE`     | `enum('YES','NO')`  | Indicates whether failed login tracking is enabled for the account                                                                            |
| `MAX_ATTEMPTS`           | `INTEGER`           | Maximum number of failed login attempts allowed before account is locked (corresponds to FAILED_LOGIN_ATTEMPTS clause value in CREATE USER or ALTER USER statement) |
| `PASSWORD_LOCK_DAYS`     | `INTEGER`           | Number of days for which account will be temporarily locked after exceeding the MAX_ATTEMPTS limit. Set to -1 if account is locked forever (corresponds to PASSWORD_LOCK_TIME clause value in CREATE USER or ALTER USER statement) |
| `IS_LOCKED`              | `BOOLEAN`           | Indicates if account is temporarily locked by failed login lock tracking. NULL if tracking is not enabled for account                        |
| `REMAINING_ATTEMPTS`     | `INTEGER`           | Number of failed login attempts remaining before account will be locked. NULL if tracking is not enabled for account                         |
| `REMAINING_DAYS_LOCKED`  | `INTEGER`           | Number of days for which account is locked due to failed login lock tracking. -1 means that account is locked "forever" (until server restart/FLUSH PRIVILEGES or specific account unlock). NULL if tracking is not enabled for account |
