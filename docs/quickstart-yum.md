# Install Percona Server for MySQL and create a database on Oracle Linux

Install Percona Server for MySQL with the Percona DNF repositories.

Quickstart path: Step 1 is Install. Step 2 is [Work with a database](quickstart-database-script.md).

For expected output, troubleshooting, and platform notes, see [Install using DNF](yum-repo.md). For unattended installs and temporary password automation, see [Non-interactive DNF installation for Percona Server for MySQL {{vers}}](yum-noninteractive-install.md). For Percona Toolkit UDFs and the testing repository, see [Optional steps after repository install for Percona Server for MySQL {{vers}}](optional-after-install.md).

--8<-- "percona-release.md"

## Prerequisites

* Either use `sudo` or run as root

* Stable Internet access

## Installation steps

{.power-number}

1. Install `percona-release`:

    ```shell
    sudo yum install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. Set up the repository for Percona Server for MySQL 8.4:

    [Optional] On Red Hat 8 systems (including Rocky Linux and AlmaLinux), disable the distribution's MySQL module first:

    ```shell
    sudo dnf module disable mysql -y
    ```

    Then run:

    ```shell
    sudo percona-release setup {{pkg}}
    ```

3. Enable the release repository:

    ```shell
    sudo percona-release enable {{pkg}} release
    ```

4. Install Percona Server for MySQL:

    ```shell
    sudo yum install -y percona-server-server
    ```

5. Start the MySQL service:

    ```shell
    sudo systemctl restart mysql
    ```

6. Retrieve the temporary password:

    ```shell
    sudo grep 'temporary password' /var/log/mysqld.log
    ```

7. Log in to the server using the temporary password:

    ```shell
    mysql -uroot -p
    Enter password:
    ```

8. Change the temporary password:

    ```sql
    ALTER USER 'root'@'localhost' IDENTIFIED BY '[your password]';
    exit
    ```

9. Log in again with the new password to verify:

    ```shell
    mysql -uroot -p
    Enter password:
    ```

## Secure the installation

[Optional] Run the `mysql_secure_installation` script to improve security. The script helps you:

* Set a password for the root user

* Select a password validation policy level

* Remove anonymous users

* Disable root login remotely

* Remove the test database

* Reload the privilege table

```shell
sudo mysql_secure_installation
```

--8<-- "quickstart-database-script.md"

## Troubleshooting

* **Connection issues**

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

* **Permission errors**

    If MySQL reports that a user lacks permission to perform an action, grant the needed privilege. For example, to allow a user to create databases from the MySQL shell:

    ```sql
    GRANT CREATE ON *.* TO 'username'@'localhost';
    FLUSH PRIVILEGES;
    ```

    Replace `username` with your MySQL user name.

* **Package installation issues**

    Check the system log for errors during installation:

    ```shell
    sudo journalctl -u mysqld -n 50
    ```

    For specific error messages, see the [Percona Server for MySQL documentation](index.md) or the [Percona community forum](https://forums.percona.com/).


## Security best practices

* Keep software updated: `sudo yum update` regularly.

* Strong root password: Set a complex, unique password using [`mysql_secure_installation`](#secure-the-installation).

* Disable unused accounts and databases: Remove unnecessary elements.

* Monitor Server Activity: Employ tools, like [Percona Monitoring and Management :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html), and logs to monitor server activity for suspicious behavior.

* Backup data regularly: Ensure robust backups for disaster recovery.


## Work with a database

[Work with a database:material-arrow-right:](quickstart-database-script.md){.md-button}

## Additional resources

* [Quickstart - Overview](quickstart-overview.md)

* [Run Percona Server for MySQL with Docker](quickstart-docker.md)

* [Install Percona Server for MySQL on Ubuntu](quickstart-apt.md)

* [Clean up your installation](quickstart-cleanup.md)

* [Next steps](quickstart-next-steps.md)


