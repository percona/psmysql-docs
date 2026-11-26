> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install Percona Server for MySQL and create a database on Ubuntu

Use the Percona repositories to install Percona Server for MySQL with APT.

Quickstart path: Step 1, Install. Next: [Work with a database](https://docs.percona.com/percona-server/9.7/quickstart-database-script.md) is step two.

For step-by-step command explanations, HTTPS (`--scheme`) details, non-interactive installs, and debconf guidance, see [Use an APT repository to install Percona Server for MySQL](https://docs.percona.com/percona-server/9.7/apt-repo.md).

The `percona-release` tool is a command-line utility that simplifies the management and installation of Percona software packages, providing access to the latest versions and ensuring consistency across environments. For more information, refer to the [Percona Software Repositories Documentation](https://docs.percona.com/percona-software-repositories/index.html).

## Prerequisites

- Run commands as the root user or with `sudo`.
- Confirm stable internet access.

## Installation steps

To install the server, complete the following steps:

1. Update the package index:

   ```shell
   sudo apt update
   ```

1. Install curl:

   ```shell
   sudo apt install -y curl
   ```

1. Download and install the `percona-release` repository package:

   ```shell
   curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
   sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
   ```

1. Enable only the Percona Server for MySQL 9.7 release repository. This command disables any other Percona repositories:

   ```shell
   sudo percona-release enable-only ps-97-lts release --scheme https
   ```

1. Update the package index:

   ```shell
   sudo apt update
   ```

1. Install Percona Server for MySQL:

   ```shell
   sudo apt install -y percona-server-server
   ```

   During installation, the package manager prompts you to complete the following actions:

   - Enter a root password. Use `<strong-password>` as a placeholder for a value you choose.
   - Confirm the password.

   The package manager may ask additional debconf questions depending on the package and distribution. On 9.7, password-based authentication defaults to `caching_sha2_password`. The `mysql_native_password` plugin is not available on MySQL 9.x. See [Authentication methods](https://docs.percona.com/percona-server/9.7/authentication-methods.md).

1. [Optional] Secure the installation:

   Run the `mysql_secure_installation` script to improve security. The script helps you:

   - Set a password for the root user
   - Select a password validation policy level
   - Remove anonymous users
   - Disable root login remotely
   - Remove the test database
   - Reload the privilege table

   ```shell
   sudo mysql_secure_installation
   ```

1. Check the service status and restart if needed:

   ```shell
   sudo systemctl status mysql
   sudo systemctl restart mysql
   ```

1. Log in to the server using the password you set during installation:

   ```shell
   mysql -uroot -p
   Enter password:
   ```

## Work with a database

The following steps create a database and run basic queries. You can also open the [Work with a database](https://docs.percona.com/percona-server/9.7/quickstart-database-script.md) script on its own page.

[Work with a database](https://docs.percona.com/percona-server/9.7/quickstart-database-script.md)

## Troubleshooting

- Connection issues

  - Check that the MySQL service is running:

    ```shell
    sudo systemctl status mysql
    ```

  - If the service is not active, start it:

    ```shell
    sudo systemctl start mysql
    ```

  - Try connecting with the password you set during installation:

    ```shell
    mysql -uroot -p
    Enter password:
    ```

- Permission errors

  If MySQL reports that a user lacks permission to perform an action, grant the needed privilege. For example, to allow a user to create databases from the MySQL shell:

  ```sql
  GRANT CREATE ON *.* TO 'username'@'localhost';
  FLUSH PRIVILEGES;
  ```

  Replace `username` with your MySQL user name.

- Package installation issues

  Check the system log for errors during installation:

  ```shell
  sudo journalctl -u mysql -n 50
  ```

  For specific error messages, see the [Percona Server for MySQL documentation](https://docs.percona.com/percona-server/9.7/index.md) or the [Percona community forum](https://forums.percona.com/).

## Security best practices

- Strong passwords: Use complex and unique passwords for all accounts, including the root account.
- Minimize permissions: Grant each user only the privileges required for their tasks.
- Disable unnecessary accounts: Remove test accounts and unused accounts.
- Regular backups: Run consistent backup routines to protect data.
- Keep software updated: Apply security patches to Percona Server and related packages.
- Monitor server activity: Use tools such as [Percona Monitoring and Management](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html) and server logs to detect suspicious behavior.

## Additional resources

- [Quickstart overview](https://docs.percona.com/percona-server/9.7/quickstart-overview.md)
- [Run Percona Server for MySQL with Docker](https://docs.percona.com/percona-server/9.7/quickstart-docker.md)
- [Install Percona Server for MySQL on Oracle Linux](https://docs.percona.com/percona-server/9.7/quickstart-yum.md)
- [Clean up your installation](https://docs.percona.com/percona-server/9.7/quickstart-cleanup.md)
- [Next steps](https://docs.percona.com/percona-server/9.7/quickstart-next-steps.md)
