# Install Percona Server for MySQL and create a database on Ubuntu

Use the Percona repositories to install using APT.

--8<-- "percona-release.md"

## Prerequisites

* Either use `sudo` or run as root

* Stable Internet access

## Installation steps

{.power-number}

1. Update the package index:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

2. Install curl:

    ```{.bash data-prompt="$"}
    $ sudo apt install -y curl
    ```

3. Download and install the `percona-release` repository package:

    ```{.bash data-prompt="$"}
    $ curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
    $ sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
    ```

4. Set up the Percona Server for MySQL 8.4 repository:

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup {{pkg}}
    ```

5. Enable the Percona Server for MySQL release repository:

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable {{pkg}} release
    $ sudo apt update
    ```

6. Install Percona Server for MySQL:

    ```{.bash data-prompt="$"}
    $ sudo apt install -y percona-server-server
    ```

    During installation, you will be prompted to:
    - Enter a root password (use `secret` for these examples, or choose your own)
    - Confirm the password
    - Choose authentication method (Strong password encryption recommended)

7. [Optional] Secure the installation:

    Run the `mysql_secure_installation` script to improve security. The script helps you:
    - Set a password for the root user
    - Select a password validation policy level
    - Remove anonymous users
    - Disable root login remotely
    - Remove the test database
    - Reload the privilege table

    ```{.bash data-prompt="$"}
    $ sudo mysql_secure_installation
    ```

8. Check the service status and restart if needed:

    ```{.bash data-prompt="$"}
    $ sudo systemctl status mysql
    $ sudo systemctl restart mysql
    ```

9. Log in to the server using the password you set during installation:

    ```{.bash data-prompt="$"}
    $ mysql -uroot -p
    Enter password:
    ```

## Next steps

The steps below walk you through creating a database and running basic queries. You can also open the [Create a database](quickstart-database-script.md) script in its own page.

--8<-- "quickstart-database-script.md"

## Troubleshooting

* Connection Issues: Double-check credentials, ensure service is running, and verify firewall configurations if applicable.

* Permission Errors: Grant necessary permissions to users using GRANT statements within the MySQL shell.

* Package Installation Issues: Refer to Percona documentation and online forums for specific error messages and solutions.

##Security best practices

* Strong Passwords: Utilize complex and unique passwords for all users, especially the root account.

* Minimize Permissions: Grant users only the privileges necessary for their tasks.

* Disable Unnecessary Accounts: Remove test accounts and unused accounts.

* Regular Backups: Implement consistent backup routines to safeguard your data.

* Keep Software Updated: Maintain Percona Server and related packages updated with security patches.

* Monitor Server Activity: Employ tools, like [Percona Monitoring and Management :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html), and logs to monitor server activity for suspicious behavior.

## Additional resources

- [Quickstart - Overview](quickstart-overview.md)
- [Create a database](quickstart-database-script.md)
- [Run Percona Server for MySQL with Docker](quickstart-docker.md)
- [Install Percona Server for MySQL on Oracle Linux](quickstart-yum.md)
- [Clean up your installation](quickstart-cleanup.md)
- [Next steps](quickstart-next-steps.md)

