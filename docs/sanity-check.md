# Sanity check: First five minutes

This guide helps you verify that the [First five minutes](first-five-minutes.md) security and stability steps have been applied correctly. Run these checks after completing the First five minutes, or on an existing server to see if those steps are in place.

You need:

* Access to the MySQL server as a user with enough *privileges* (permissions to run statements and see system data) to run the SQL checks—for example, `root` (the default MySQL administrative user) or the admin user you created.
* Ability to run shell commands (and `systemctl`, the systemd command to inspect and manage services) on the host (the machine where MySQL runs).

## Summary: what we check

| Check | Purpose |
|-------|---------|
| [1. Root and security script](#1-root-and-security-script) | Root has a password and basic hardening (no anonymous user, no test DB, root not remote) is done. |
| [2. Least-privilege admin user](#2-least-privilege-admin-user) | A dedicated admin user exists and does not have full SUPER/ALL. |
| [3. OOM-killer guardrail](#3-oom-killer-guardrail) | systemd OOM score is set so MySQL is less likely to be killed by the kernel when the system is low on memory. |
| [4. Diagnostic logging](#4-diagnostic-logging) | Error log and slow query log are enabled and paths are set. |
| [5. Backup path](#5-backup-path) | Backup directory exists and is writable by the MySQL (or backup) user. |

## 1. Root and security script

Goal: Confirm the MySQL `root` account is not empty and that `mysql_secure_installation`–style hardening is in place.

1.1 Root has a password  
Try connecting without a password; the connection should fail:

```shell
mysql -u root -h localhost 2>&1 | head -1
```

You want to see an access denied or password-related error, not a successful connection.

1.2 No anonymous user  
*Anonymous users* (accounts with an empty username that can connect without proper credentials) should not exist:

```shell
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user = '';"
```

Expected: *empty result set* (no rows returned by the query).

1.3 No remote root  
The `root` user should not be allowed to connect from remote hosts—only from the same machine (`root@localhost` or similar):

```shell
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user = 'root' AND host != 'localhost';"
```

Expected: empty result set. If you use a specific hostname for root (e.g. `root@127.0.0.1`), that is fine; the important thing is no `root@'%'` (which would allow root from any host).

1.4 Test database removed  
The default `test` database (a sample database that is often removed for security) should not exist:

```shell
mysql -u root -p -e "SHOW DATABASES LIKE 'test';"
```

Expected: empty result set.

## 2. Least-privilege admin user

Goal: Confirm you have a dedicated admin user and that the account does not have full `SUPER` (a powerful built-in privilege) or global privileges on all databases (`*.*`) unless you intentionally grant them.

2.1 List admin-like users  
Adjust the user name if you used something other than `admin`:

```shell
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user IN ('admin','dba','mysqladmin') OR user NOT IN ('root','mysql.session','mysql.sys','mysql.infoschema');"
```

Use this to identify the account you use for day-to-day admin.

2.2 Check that admin does not have SUPER  
Replace `'admin'@'localhost'` with your admin user and *host* (the connection source; `localhost` means the same machine):

```shell
mysql -u root -p -e "SHOW GRANTS FOR 'admin'@'localhost';"
```

Expected: no line containing `SUPER` or `ALL PRIVILEGES ON *.*` unless you deliberately grant them. A limited set of *grants* (assigned privileges) such as `CREATE USER`, `RELOAD`, `PROCESS`, `REPLICATION CLIENT`, `BACKUP_ADMIN`, etc., is what we expect from the First five minutes.

2.3 (Optional) Effective privileges  
To see the full *effective* privilege set (the combined permissions a user actually has, including from roles), use [SHOW EFFECTIVE GRANTS](extended-show-grants.md) if your server supports that statement:

```shell
mysql -u root -p -e "SHOW EFFECTIVE GRANTS FOR 'admin'@'localhost';"
```

## 3. OOM-killer guardrail

Goal: Confirm that the MySQL systemd service has a lower *OOM score* (a value the kernel uses when choosing which process to terminate when the system is out of memory; lower means less likely to be killed) so the kernel is less likely to kill MySQL.

3.1 Service name  
On Red Hat–based systems the service is often `mysqld`; on Debian/Ubuntu the service may be named `mysql`. Check which is in use:

```shell
systemctl status mysqld 2>/dev/null || systemctl status mysql 2>/dev/null
```

3.2 OOMScoreAdjust  
Use the same service name as above:

```shell
systemctl show mysqld -p OOMScoreAdjust
# or
systemctl show mysql -p OOMScoreAdjust
```

Expected: `OOMScoreAdjust=-500` (or another negative value). If you see an empty value or `OOMScoreAdjust=0`, the First five minutes OOM guardrail is not applied.

## 4. Diagnostic logging

Goal: Confirm the error log and slow query log are enabled and that paths are set so you can find them.

4.1 Error log  
Check that the *error log* (the file where the server records errors, warnings, and startup messages) is set and that the server is writing to that file:

```shell
mysql -u root -p -e "SELECT @@log_error;"
```

Expected: a non-empty path (e.g. `/var/log/mysql/error.log` or a path under the *datadir*—the directory where the server stores database files). Then check that the file exists and is recent:

```shell
ls -la $(mysql -u root -p -N -e "SELECT @@log_error;" 2>/dev/null)
```

4.2 Slow query log  
Check that the *slow query log* (the file that records SQL statements that run longer than the `long_query_time` threshold) is on and where that log is written:

```shell
mysql -u root -p -e "SELECT @@slow_query_log, @@slow_query_log_file, @@long_query_time;"
```

Expected: `slow_query_log = 1`, and `slow_query_log_file` set to a path you can monitor. Optionally confirm the file exists and is writable after the server has been running with slow log enabled.

## 5. Backup path

Goal: Confirm the directory you use for backups exists and is writable by the MySQL *system user* (the operating-system user that runs the MySQL process or backup tool; often named `mysql`).

5.1 Choose your backup path  
Use the same path you configured in [First five minutes — Verify the backup path](first-five-minutes.md#verify-the-backup-path) (e.g. `/var/backups/mysql`). Set that path in a variable for the next commands:

```shell
BACKUP_DIR=/var/backups/mysql
```

5.2 Directory exists  
```shell
test -d "$BACKUP_DIR" && echo "OK: backup directory exists" || echo "FAIL: backup directory missing"
```

5.3 Writable by MySQL user  
Replace `mysql` with the user that runs your backup tool if different:

```shell
sudo -u mysql touch "$BACKUP_DIR/.write_test" 2>/dev/null && sudo -u mysql rm -f "$BACKUP_DIR/.write_test" && echo "OK: backup path is writable" || echo "FAIL: backup path not writable by mysql"
```

## Optional: run checks in one go

You can run a subset of these checks from the shell in one pass. The following assumes:

* Service name is `mysqld` (change to `mysql` if needed).
* Admin user is `'admin'@'localhost'` (change SQL if needed).
* Backup path is `/var/backups/mysql` (change if needed).
* You will enter the root password when prompted.

```shell
echo "=== 1. No anonymous user ==="
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user = '';"

echo "=== 2. No remote root ==="
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user = 'root' AND host != 'localhost';"

echo "=== 3. No test database ==="
mysql -u root -p -e "SHOW DATABASES LIKE 'test';"

echo "=== 4. Admin grants (no SUPER/ALL on *.*) ==="
mysql -u root -p -e "SHOW GRANTS FOR 'admin'@'localhost';"

echo "=== 5. OOMScoreAdjust ==="
systemctl show mysqld -p OOMScoreAdjust

echo "=== 6. Error log and slow query log ==="
mysql -u root -p -e "SELECT @@log_error, @@slow_query_log, @@slow_query_log_file;"

echo "=== 7. Backup path writable ==="
BACKUP_DIR=/var/backups/mysql
test -d "$BACKUP_DIR" && sudo -u mysql touch "$BACKUP_DIR/.write_test" 2>/dev/null && sudo -u mysql rm -f "$BACKUP_DIR/.write_test" && echo "OK: writable" || echo "FAIL or missing"
```

Interpret the output using the expected results described in each section above.

## Next steps

* If any check fails, re-read the corresponding section in [First five minutes](first-five-minutes.md) and apply or fix the step.
* Re-run this sanity check after changes to confirm everything passes.
* For backup strategy and restore testing, see [Backup and restore overview](backup-restore-overview.md).
