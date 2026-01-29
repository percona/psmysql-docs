# Clean up your installation

Clean up is optional. If you want to remove Percona Server for MySQL and clean up your system, follow the steps below for your installation method.

!!! warning

    These steps will remove Percona Server for MySQL and may delete all data files (databases, tables, logs, etc.). Take a backup before proceeding if you need to preserve any data.

=== "Docker"

    If you installed Percona Server for MySQL using Docker, follow these steps:

    1. Exit the MySQL command client shell if you're still connected:

        ```sql
        exit
        ```

        You can also use `\q` or `quit` commands. The execution of the statement also closes the connection.

    2. Stop and remove the Docker container:

        ```shell
        docker container rm psmysql -f
        ```

        ??? example "Expected output"

            ```text
            psmysql
            ```

    3. Remove the Docker image:

        ```shell
        docker image rmi percona/percona-server:{{tag}}
        ```

        If you are running the ARM64 version of Percona Server, use:

        ```shell
        docker image rmi percona/percona-server:{{arm_tag}}
        ```

        ??? example "Expected output"

            ```text
            Untagged: percona/percona-server:{{tag}}
            Untagged: percona/percona-server@sha256:4944f9b365e0dc88f41b3b704ff2a02d1459fd07763d7d1a444b263db8498e1f
            Deleted: sha256:b2588da614b1f382468fc9f44600863e324067a9cae57c204a30a2105d61d9d9
            ...
            ```

    4. Remove the Docker volume (if you created one):

        ```shell
        docker volume rm myvol
        ```

        ??? example "Expected output"

            ```text
            myvol
            ```

=== "Ubuntu (APT)"

    If you installed Percona Server for MySQL using APT on Ubuntu or Debian, follow these steps:

    1. Stop the Percona Server for MySQL service:

        ```shell
        sudo systemctl stop mysql
        ```

    2. Choose one of the following options:

        **Option A: Remove packages but keep data files**

        This command removes the packages but leaves data files (databases, tables, logs, configuration, etc.) behind:

        ```shell
        sudo apt remove percona-server*
        ```

        **Option B: Remove packages and delete all data files**

        !!! warning

            This command removes all packages and permanently deletes all data files (databases, tables, logs, etc.). Ensure you have a backup if you need this data.

        ```shell
        sudo apt purge percona-server*
        ```

    3. [Optional] If you used Option A and want to remove data files manually:

        !!! warning

            This step permanently deletes all data files. Ensure you have a backup if you need this data.

        ```shell
        sudo rm -rf /var/lib/mysql
        sudo rm -f /etc/mysql/my.cnf
        ```

=== "Oracle Linux (YUM or DNF)"

    If you installed Percona Server for MySQL using YUM or DNF on Oracle Linux or RHEL, follow these steps:

    1. Stop the Percona Server for MySQL service:

        ```shell
        sudo systemctl stop mysql
        ```

    2. Remove the packages:

        ```shell
        sudo yum remove percona-server*
        ```

        Or if you're using DNF:

        ```shell
        sudo dnf remove percona-server*
        ```

        These commands remove the packages but leave data files behind. If you want to remove data files as well, continue to step 3.

    3. [Optional] Remove data and configuration files:

        !!! warning

            This step permanently deletes all data files (databases, tables, logs, etc.). Ensure you have a backup if you need this data.

        ```shell
        sudo rm -rf /var/lib/mysql
        sudo rm -f /etc/my.cnf
        ```

## Next steps

[Next steps](quickstart-next-steps.md)

## Additional resources

* [Quickstart - Overview](quickstart-overview.md)

* [Run Percona Server for MySQL with Docker](quickstart-docker.md)

* [Install Percona Server for MySQL on Ubuntu](quickstart-apt.md)

* [Install Percona Server for MySQL on Oracle Linux](quickstart-yum.md)

* [Work with a database](quickstart-database-script.md)
