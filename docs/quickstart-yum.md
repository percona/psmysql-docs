# Install Percona Server for MySQL and create a database on Oracle Linux

Use the Percona repositories to install using YUM.

--8<-- "percona-release.md"

## Prerequisites

* Either use `sudo` or run as root

* Stable Internet access

## Installation steps

{.power-number}

1. Install `percona-release`:

    ```{.bash data-prompt="$"}
    $ sudo yum install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm
    ```

2. Set up the repository for Percona Server for MySQL 8.4:

    ```{.bash data-prompt="$"}
    $ sudo percona-release setup {{pkg}}
    ```

    On Red Hat 8 systems, you may be prompted to disable the DNF mysql module. Answer `y` to continue.

3. Enable the release repository:

    ```{.bash data-prompt="$"}
    $ sudo percona-release enable {{pkg}} release
    ```

4. Install Percona Server for MySQL:

    ```{.bash data-prompt="$"}
    $ sudo yum install -y percona-server-server
    ```

5. Start the MySQL service:

    ```{.bash data-prompt="$"}
    $ sudo systemctl restart mysql
    ```

6. Retrieve the temporary password:

    ```{.bash data-prompt="$"}
    $ sudo grep 'temporary password' /var/log/mysqld.log
    ```

7. Log in to the server using the temporary password:

    ```{.bash data-prompt="$"}
    $ mysql -uroot -p
    Enter password:
    ```

8. Change the temporary password:

    ```{.bash data-prompt="mysql>"}
    mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY '[your password]';
    mysql> exit
    ```

9. Log in again with the new password to verify:

    ```{.bash data-prompt="$"}
    $ mysql -uroot -p
    Enter password:
    ```

--8<-- "quickstart-database-script.md"

## Troubleshooting:

Installation:

* Verify repository is enabled: `sudo yum repolist`

* Check for package conflicts: `sudo yum deplist percona-server-server`

* Consult package logs: `sudo journalctl -u yum`

MySQL startup:

* Review system logs: `sudo journalctl -u mysqld`

* Check configuration files: /etc/my.cnf

## Security Steps:

* Keep software updated: `sudo yum update` regularly.

* Strong root password: Set a complex, unique password using [`mysql_secure_installation`](#secure-the-installation).

* Disable unused accounts and databases: Remove unnecessary elements.

* Monitor Server Activity: Employ tools, like [Percona Monitoring and Management :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/quickstart/quickstart.html), and logs to monitor server activity for suspicious behavior.

* Backup data regularly: Ensure robust backups for disaster recovery.

## Secure the installation

[Optional] Run the `mysql_secure_installation` script to improve security. The script helps you:
- Set a password for the root user
- Select a password validation policy level
- Remove anonymous users
- Disable root login remotely
- Remove the test database
- Reload the privilege table

```{.bash data-prompt="$"}
$ sudo mysql_secure_installation
```

## Clean up

If you want to remove Percona Server for MySQL and clean up your system, see [Clean up your installation](quickstart-cleanup.md).

## Other installation methods

- [Quickstart - Overview](quickstart-overview.md)
- [Run Percona Server for MySQL with Docker](quickstart-docker.md)
- [Install Percona Server for MySQL on Ubuntu](quickstart-apt.md)
- [Clean up your installation](quickstart-cleanup.md)
- [Next steps](quickstart-next-steps.md)

## Next step

[Choose your next steps:material-arrow-right:](quickstart-next-steps.md){.md-button}
