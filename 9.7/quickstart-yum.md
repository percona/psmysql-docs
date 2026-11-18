> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install Percona Server for MySQL and create a database on Oracle Linux

Use the Percona repositories to install using YUM.

Quickstart path: Step 1 — Install. Next: [Work with a database](https://docs.percona.com/percona-server/9.7/quickstart-database-script.html) (step 2).

The `percona-release` tool is a command-line utility that simplifies the management and installation of Percona software packages, providing access to the latest versions and ensuring consistency across environments. For more information, refer to the [Percona Software Repositories Documentation](https://docs.percona.com/percona-software-repositories/index.html).

## Prerequisites

- Either use `sudo` or run as root
- Stable Internet access

## Installation steps

{.power-number}

1. Install `percona-release`:

   ```
   sudo yum install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm
   ```

1. Set up the repository for Percona Server for MySQL 9.7:

   On RHEL 8 and derivatives (Oracle Linux 8, Rocky Linux 8, AlmaLinux 8), you must disable the distribution’s MySQL module first. Otherwise, the module hides the Percona packages and the installation fails with `All matches were filtered out by modular filtering`. On RHEL 9 this step is not needed. On RHEL 10 skip this step: RHEL 10 has no MySQL module, and the command fails.

   ```
   sudo dnf module disable mysql -y
   ```

   Then enable only the Percona Server for MySQL 9.7 release repository. This command disables any other Percona repositories:

   ```
   sudo percona-release enable-only ps-97-lts release
   ```

1. Check that the repository is enabled. The output must list the `ps-97-lts-release-<arch>` repository:

   ```
   sudo dnf repolist | grep ps-97-lts
   ```

1. Install Percona Server for MySQL:

   ```
   sudo yum install -y percona-server-server
   ```

1. Start the MySQL service:

   ```
   sudo systemctl restart mysql
   ```

1. Retrieve the temporary password:

   ```
   sudo grep 'temporary password' /var/log/mysqld.log
   ```

1. Log in to the server using the temporary password:

   ```
   mysql -uroot -p
   Enter password:
   ```

1. Change the temporary password:

   ```
   ALTER USER 'root'@'localhost' IDENTIFIED BY '[your password]';
   exit
   ```

1. Log in again with the new password to verify:

   ```
   mysql -uroot -p
   Enter password:
   ```

## Secure the installation

[Optional] Run the `mysql_secure_installation` script to improve security. The script helps you:

- Set a password for the root user
- Select a password validation policy level
- Remove anonymous users
- Disable root login remotely
- Remove the test database
- Reload the privilege table

```
sudo mysql_secure_installation
```

## Troubleshooting

- **Connection issues**

  - Check that the MySQL service is running:

    ```
    sudo systemctl status mysql
    ```

  - If the service is not active, start it:

    ```
    sudo systemctl start mysql
    ```

  - Try connecting with the password you set during installation:

    ```
    mysql -uroot -p
    Enter password:
    ```

- **Permission errors**

  If MySQL reports that a user lacks permission to perform an action, grant the needed privilege. For example, to allow a user to create databases from the MySQL shell:

  ```
  GRANT CREATE ON *.* TO 'username'@'localhost';
  FLUSH PRIVILEGES;
  ```

  Replace `username` with your MySQL user name.

- **Package installation issues**

  Check the system log for errors during installation:

  ```
  sudo journalctl -u mysqld -n 50
  ```

  For specific error messages, see the [Percona Server for MySQL documentation](https://docs.percona.com/percona-server/9.7/index.html) or the [Percona community forum](https://forums.percona.com/).

## Security best practices

- Keep software updated: `sudo yum update` regularly.
- Strong root password: Set a complex, unique password using [`mysql_secure_installation`](#secure-the-installation).
- Disable unused accounts and databases: Remove unnecessary elements.
- Monitor Server Activity: Employ tools, like [Percona Monitoring and Management](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html) , and logs to monitor server activity for suspicious behavior.
- Backup data regularly: Ensure robust backups for disaster recovery.

## Work with a database

[Work with a database](https://docs.percona.com/percona-server/9.7/quickstart-database-script.html)

## Additional resources

- [Quickstart - Overview](https://docs.percona.com/percona-server/9.7/quickstart-overview.html)
- [Run Percona Server for MySQL with Docker](https://docs.percona.com/percona-server/9.7/quickstart-docker.html)
- [Install Percona Server for MySQL on Ubuntu](https://docs.percona.com/percona-server/9.7/quickstart-apt.html)
- [Clean up your installation](https://docs.percona.com/percona-server/9.7/quickstart-cleanup.html)
- [Next steps](https://docs.percona.com/percona-server/9.7/quickstart-next-steps.html)
