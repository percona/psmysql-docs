# First five minutes after installation

This guide walks you through the most important security and stability steps to take right after installing Percona Server for MySQL. Completing these steps helps protect your server and makes troubleshooting easier.

Quickstart path: After [Install (Ubuntu)](quickstart-apt.md), [Install (Oracle Linux)](quickstart-yum.md), or [Docker](quickstart-docker.md). Next: [Work with a database](quickstart-database-script.md).

| Step | What you do |
|------|-------------|
| [Secure the installation](#secure-the-installation) | Run post-installation security steps so the server is not left in a default, weak state. |
| [Create a least-privilege admin user](#create-a-least-privilege-admin-user) | Use a dedicated admin account with only the privileges (permissions) that account needs instead of `root`. |
| [Configure an OOM-killer guardrail](#configure-an-oom-killer-guardrail) | Reduce the chance the Linux OOM killer will abruptly terminate the MySQL process. |
| [Enable diagnostic logging](#enable-diagnostic-logging) | Turn on error and slow-query logging so you can diagnose issues later. |
| [Verify the backup path](#verify-the-backup-path) | Ensure the directory where backups will go exists and is writable. |

When you are done, use [Sanity check: First five minutes](sanity-check.md) to verify that these steps were applied correctly.

## Secure the installation

Before doing anything else, complete the standard post-installation security steps. These ensure the server is not left with default passwords, anonymous users (accounts with no username that can connect without proper credentials), or remote root login.

1. Set or update the `root` password  
   The *root* account is the default MySQL administrative user. If you did not set its password during install (for example, on some RPM-based systems), set one now. See [Post-installation — Update the root password](post-installation.md#update-the-root-password).

2. Run `mysql_secure_installation` to:

    * Change the root password (if needed)
    * Disallow remote login for root
    * Remove anonymous users
    * Remove the test database
    * Reload privilege tables

3. Optional: populate time zone tables

If you installed from source or generic binaries, [populate the time zone tables](post-installation.md#populate-the-time-zone-tables) (the system data that makes time zone–aware date and time functions work correctly).

   For more information, see [Post-installation — Secure the server](post-installation.md#secure-the-server).

## Create a least-privilege admin user

Use a dedicated admin account for day-to-day administration instead of `root`. Give that account only the privileges the account needs (*least privilege*: the practice of granting only the minimum permissions necessary). Reserve `root` for emergencies and avoid using root for routine tasks.

1. Connect as `root` (or another user that can create users and grant privileges):

    ```shell
    mysql -u root -p
    ```

2. Create an admin user. Use a strong password and a specific *host* (the machine or network location the user can connect from; for example, `localhost` means the same machine only) instead of `%` (which means any host):

    ```sql
    CREATE USER 'admin'@'localhost' IDENTIFIED BY 'YourStrongPassword_12';
    ```

3. Grant only the privileges the admin needs. *Grant* means to assign a permission to a user. The following is a common set for an admin who manages users, replication, and backups but does not need full `SUPER` (a powerful built-in privilege) or global privileges on all databases (`*.*`):

    ```sql
    GRANT CREATE USER, RELOAD, PROCESS, REPLICATION CLIENT, REPLICATION SLAVE, BACKUP_ADMIN,
          SHOW DATABASES, SELECT ON *.* TO 'admin'@'localhost';
    FLUSH PRIVILEGES;
    ```

    `FLUSH PRIVILEGES` tells the server to reload the privilege tables so the new grants take effect immediately.

4. Test the new user:

    ```shell
    mysql -u admin -p -e "SHOW DATABASES;"
    ```

5. Use `admin` for daily tasks and keep `root` for rare, high-privilege operations.

!!! tip "Adjust privileges to your needs"
    Add or remove privileges based on what this admin will do. For example, add `SHOW VIEW`, `CREATE ROUTINE`, or `EVENT` if they manage views (saved queries presented as virtual tables), routines (stored procedures and functions), or scheduled events. Avoid granting `SUPER`, `ALL`, or `*.*` unless necessary. You can review effective privileges with [SHOW EFFECTIVE GRANTS](extended-show-grants.md).

## Configure an OOM-killer guardrail

On Linux, when the system runs low on memory, the kernel *OOM killer* (out-of-memory killer: a kernel process that terminates other processes to free memory) may terminate processes. MySQL can be one of them, which leads to abrupt shutdowns. You can make the MySQL service less likely to be chosen by adjusting its OOM score.

Using *systemd* (the Linux system and service manager that starts and manages the MySQL service), set `OOMScoreAdjust` so that the kernel prefers to kill other processes before MySQL. A typical value is `-500` (range is -1000 to 1000; lower means less likely to be killed).

1. Create or edit an override file for the MySQL service. On Red Hat–based systems the service is often `mysqld`; on Debian/Ubuntu the service may be named `mysql`. Adjust the service name if needed:

   ```shell
   sudo systemctl edit mysqld
   ```

   If your service is named `mysql`:

   ```shell
   sudo systemctl edit mysql
   ```

2. Add the following (use `mysqld` or `mysql` to match your service name):

   ```ini
   [Service]
   OOMScoreAdjust=-500
   ```

3. Save and close the editor. Reload systemd and restart the MySQL service:

   ```shell
   sudo systemctl daemon-reload
   sudo systemctl restart mysqld
   ```

4. Confirm the setting:

   ```shell
   systemctl show mysqld -p OOMScoreAdjust
   ```

   You should see `OOMScoreAdjust=-500` (or the value you set).

!!! note "Not a memory limit"
    The OOM score adjustment only influences *which* process the OOM killer chooses. It does not set a memory limit for MySQL. For strict limits, use cgroups or MySQL/InnoDB memory settings.

## Enable diagnostic logging

Enabling the *error log* (a file where the server records errors, warnings, and startup messages) and the *slow query log* (a file that records SQL statements that run longer than a threshold you set) gives you the information you need to diagnose problems and tune performance.

1. Locate your configuration file  
   The configuration file (often `my.cnf` or `mysqld.cnf`) controls server options. Common paths: `/etc/my.cnf`, `/etc/mysql/my.cnf`, or `/etc/mysql/mysql.conf.d/mysqld.cnf`. Edit the file under the `[mysqld]` section (the section that applies to the MySQL server process).

2. Ensure the error log is set  
   The server usually writes an error log by default. Confirm or set an explicit path so you know where to look:

   ```ini
   [mysqld]
   log_error=/var/log/mysql/error.log
   ```

   On some systems the directory is `/var/lib/mysql` (the default *data directory*, where the server stores database files) or similar. Create the log directory if needed and set ownership to the MySQL system user (the operating-system user that runs the MySQL process; often named `mysql`):

   ```shell
   sudo mkdir -p /var/log/mysql
   sudo chown mysql:mysql /var/log/mysql
   ```

3. Enable the slow query log  
   The slow query log helps you find queries that need optimization:

   ```ini
   slow_query_log = 1
   long_query_time = 2
   slow_query_log_file = /var/log/mysql/slow.log
   ```

   Adjust `long_query_time` (the time in seconds above which a query is considered “slow” and written to the log) to what you consider slow. Restart the server after changing the config.

4. Optional: restrict log locations  
   For tighter control over where logs are written, see [Restrict dynamic log file locations](restrict-dynamic-log-locations.md).

## Verify the backup path

Your backup strategy (for example, [Percona XtraBackup :octicons-link-external-16:](https://docs.percona.com/percona-xtrabackup/{{vers}}/index.html) for full physical backups, or `mysqldump` for logical backups that produce SQL) will write to a directory. Verify that path *before* you run a backup.

1. Choose a backup directory  
   For example, `/var/backups/mysql` or a dedicated volume. Do not use the *data directory* (where the server stores live database files) for backup output.

2. Create the directory and set permissions  
   The MySQL process (or the operating-system user that runs the backup tool) must be able to write there:

   ```shell
   sudo mkdir -p /var/backups/mysql
   sudo chown mysql:mysql /var/backups/mysql
   sudo chmod 750 /var/backups/mysql
   ```

3. Check that the backup directory is writable  
   As the MySQL user (or the backup user), test write access:

   ```shell
   sudo -u mysql touch /var/backups/mysql/.write_test && sudo -u mysql rm /var/backups/mysql/.write_test && echo "OK: backup path is writable"
   ```

4. Document the path  
   Use this path in your backup scripts, cron jobs, or documentation so that restores use the same location.

For backup strategy and tools, see [Backup and restore overview](backup-restore-overview.md). For [Percona XtraBackup :octicons-link-external-16:](https://docs.percona.com/percona-xtrabackup/{{vers}}/index.html), see the [Quickstart for {{vers}} :octicons-link-external-16:](https://docs.percona.com/percona-xtrabackup/{{vers}}/quickstart-overview.html).

## Next steps

* [Quickstart — Work with a database](quickstart-database-script.md) — Create tables and run queries (next step in the Quickstart path).
* Run [Sanity check: First five minutes](sanity-check.md) to confirm all steps were applied correctly.
* Use your new admin user for daily work and keep `root` for emergencies.
* Plan and test backups to the verified backup path.
* [Quickstart — Overview](quickstart-overview.md) — See the full Quickstart path.
