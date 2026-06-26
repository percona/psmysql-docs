# Install Percona Server for MySQL and create a database on Ubuntu

Install Percona Server for MySQL with the Percona APT repositories.

Quickstart path: Step 1 is Install. Step 2 is [Work with a database](quickstart-database-script.md).

For command explanations, HTTPS (`--scheme`) details, and authentication during install, see [Use an APT repository to install Percona Server for MySQL](apt-repo.md). For debconf preseed and unattended installs, see [Non-interactive APT installation for Percona Server for MySQL {{vers}}](apt-noninteractive-install.md).

--8<-- "percona-release.md"

## Prerequisites

- Run commands as the root user or with `sudo`.

- Confirm stable internet access.

## Installation steps

To install the server, complete the following steps:
{.power-number}

1. Update the package index:

    ```shell
    sudo apt update
    ```

2. Install curl:

    ```shell
    sudo apt install -y curl
    ```

3. Download and install the `percona-release` repository package:

    ```shell
    curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
    ```

4. Configure the Percona Server for MySQL {{vers}} repository. This step prepares the repository configuration and is intentionally separate from step 5:

    ```shell
    sudo percona-release setup {{pkg}} --scheme https
    ```

5. Enable the Percona Server for MySQL release repository:

    ```shell
    sudo percona-release enable {{pkg}} release --scheme https
    sudo apt update
    ```

6. Install Percona Server for MySQL:

    ```shell
    sudo apt install -y percona-server-server
    ```

    During installation, the package manager prompts you to complete the following actions:

    - Enter a root password. Use `<strong-password>` as a placeholder for a value you choose.

    - Confirm the password.

    - --8<--- "authentication-9x-overview.md:1:1" See [Authentication methods](authentication-methods.md).

7. [Optional] Secure the installation:

    Run the `mysql_secure_installation` script to improve security. The script helps you:

    * Set a password for the root user

    * Select a password validation policy level

    * Remove anonymous users

    * Disable root login remotely

    * Remove the test database

    * Reload the privilege table

    ```shell
    sudo mysql_secure_installation
    ```

8. Check the service status and restart if needed:

    ```shell
    sudo systemctl status mysql
    sudo systemctl restart mysql
    ```

9. Log in to the server using the password you set during installation:

    ```shell
    mysql -uroot -p
    Enter password:
    ```

## Work with a database

The following steps create a database and run basic queries. You can also open the [Work with a database](quickstart-database-script.md) script on its own page.

--8<-- "quickstart-database-script.md"

[Work with a database:material-arrow-right:](quickstart-database-script.md){.md-button}

## Troubleshooting

* Connection issues

    * Check that the MySQL service is running:

        ```shell
        sudo systemctl status mysql
        ```

    * If the service is not active, start it:

        ```shell
        sudo systemctl start mysql
        ```

    * Try connecting with the password you set during installation:

        ```shell
        mysql -uroot -p
        Enter password:
        ```

* Permission errors

    If MySQL reports that a user lacks permission to perform an action, grant the needed privilege. For example, to allow a user to create databases from the MySQL shell:

    ```sql
    GRANT CREATE ON *.* TO 'username'@'localhost';
    FLUSH PRIVILEGES;
    ```

    Replace `username` with your MySQL user name.

* Package installation issues

    Check the system log for errors during installation:

    ```shell
    sudo journalctl -u mysql -n 50
    ```

    For specific error messages, see the [Percona Server for MySQL documentation](index.md) or the [Percona community forum](https://forums.percona.com/).

## Security best practices

- Strong passwords: Use complex and unique passwords for all accounts, including the root account.

- Minimize permissions: Grant each user only the privileges required for their tasks.

- Disable unnecessary accounts: Remove test accounts and unused accounts.

- Regular backups: Run consistent backup routines to protect data.

- Keep software updated: Apply security patches to Percona Server and related packages.

- Monitor server activity: Use tools such as [Percona Monitoring and Management :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html) and server logs to detect suspicious behavior.

## Additional resources

- [Quickstart overview](quickstart-overview.md)

- [Run Percona Server for MySQL with Docker](quickstart-docker.md)

- [Install Percona Server for MySQL on Oracle Linux](quickstart-yum.md)

- [Clean up your installation](quickstart-cleanup.md)

- [Next steps](quickstart-next-steps.md)

