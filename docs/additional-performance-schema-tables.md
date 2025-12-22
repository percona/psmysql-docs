# Additional PERFORMANCE_SCHEMA tables

This document lists the additional `PERFORMANCE_SCHEMA` tables provided by Percona Server for MySQL that are not documented elsewhere.

### `performance_schema.account_failed_login_lock_status`

The `performance_schema.account_failed_login_lock_status` table is available in Percona Server for MySQL 8.4.7-7 and later. The table exposes information about temporary account locking from the MySQL internal Access Control List (ACL) cache. 

This table is read-only. Users need `SELECT` privilege on the `performance_schema` database or on this specific table to access its contents.

!!! note

    If an account is locked using the `CREATE USER` or `ALTER USER` statements with the `ACCOUNT LOCK` clause, the `ACCOUNT LOCK` status is not captured in the `account_failed_login_lock_status` table. The server records the `ACCOUNT LOCK` state in the `mysql.user` table.

| Column Name              | Data Type           | Description                                                                                                                                    |
|--------------------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `USER`                   | `CHAR(..)`          | The MySQL user name                                                                                                                           |
| `HOST`                   | `CHAR(..)`          | The MySQL host name                                                                                                                           |
| `IS_TRACKING_ACTIVE`     | `enum('YES','NO')`  | Indicates whether failed login tracking is enabled for the account                                                                            |
| `MAX_ATTEMPTS`           | `INTEGER`           | Maximum number of failed login attempts allowed before account is locked (corresponds to FAILED_LOGIN_ATTEMPTS clause value in CREATE USER statement) |
| `PASSWORD_LOCK_DAYS`     | `INTEGER`           | Number of days for which account will be temporarily locked after exceeding the MAX_ATTEMPTS limit. Set to -1 if account is locked forever (corresponds to PASSWORD_LOCK_TIME clause value in CREATE USER) |
| `IS_LOCKED`              | `BOOLEAN`           | Indicates if account is temporarily locked by failed login lock tracking. NULL if tracking is not enabled for account                        |
| `REMAINING_ATTEMPTS`     | `INTEGER`           | Number of failed login attempts remaining before account will be locked. NULL if tracking is not enabled for account                         |
| `REMAINING_DAYS_LOCKED`  | `INTEGER`           | Number of days for which account is locked due to failed login lock tracking. -1 means that account is locked "forever" (until server restart/FLUSH PRIVILEGES or specific account unlock). NULL if tracking is not enabled for account |