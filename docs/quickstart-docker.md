# Quickstart - Run Percona Server for MySQL container images with Docker

**Quickstart path:** Step 1 — Install. Next: [Work with a database](quickstart-database-script.md) (step 2).

## Prerequisites

* Docker Engine and Docker Compose installed and running

* Stable internet connection

* Basic understanding of the command-line interface (CLI)

Always adapt the commands and configurations to your specific environment and security requirements.

## Start a Docker container

Choose one of the following methods:

=== "Docker Compose"

    1. Create a directory and add a `docker-compose.yml` file:

        ```yaml
        services:
          mysql:
            image: percona/percona-server:{{tag}}
            container_name: psmysql
            ports:
              - "3306:3306"
            environment:
              MYSQL_ROOT_PASSWORD: secret
            volumes:
              - myvol:/var/lib/mysql
            restart: unless-stopped
        volumes:
          myvol:
        ```

        To run the Docker ARM64 version of Percona Server for MySQL, use the `{{arm_tag}}` tag instead of `{{tag}}` in the `image` line. If needed, you can replace the `secret` password with a [stronger password](#security-best-practices).

    2. Start the container:

        ```shell
        docker compose up -d
        ```

        ??? example "Expected output"

            ```text
            [+] Running 2/2
             ✔ Network quickstart_default  Created
             ✔ Container psmysql           Started
            ```

=== "docker run"

    If you prefer to run the container manually, use the following. The command has the following options:

    | Option | Description |
    |--------|--------------|
    | `-d` | Runs the container in detached mode. |
    | `-p 3306:3306` | Maps the container's MySQL port (3306) to the same port on your host. |
    | `--name psmysql` | Container name (required for the connect step below). |
    | `-e MYSQL_ROOT_PASSWORD=secret` | Sets the root password. |
    | `-v myvol:/var/lib/mysql` | Named volume for persistent storage. |
    | `percona/percona-server:{{tag}}` | Image and tag for the release. |

    You must set at least one environment variable (for example `MYSQL_ROOT_PASSWORD`) or the instance refuses to initialize. For more on tags and images, see [percona/percona-server on the Docker Hub :octicons-link-external-16:](https://hub.docker.com/r/percona/percona-server). For ARM64, use the `{{arm_tag}}` tag instead of `{{tag}}`.

    ```shell
    docker run -d -p 3306:3306 --name psmysql \
    --platform linux/amd64 \
    -e MYSQL_ROOT_PASSWORD=secret \
    -v myvol:/var/lib/mysql \
    percona/percona-server:{{tag}}
    ```

    ??? example "Expected output"

        ```text
        Unable to find image 'percona/percona-server:{{tag}}' locally
        Pulling from percona/percona-server
        b902d6b6048a: Pull complete
        ...
        708ba1f9874cbc09441d18b1ca5d9c0a6f045b27e54aafe15fdd78eda8ef3ecf
        ```

## Connect to the database instance

To connect to a MySQL database on a container, use the Docker exec command with the database instance connect command. You must know the name or ID of the container that runs the database server and the database credentials.

The Docker exec command runs a specified command in a running container. The database instance connect command connects to a MySQL server with the user name and password.

For this example, we have the following options:

| Option      | Description                                                                        |
| ----------- | ---------------------------------------------------------------------------------- |
| `it`        | Interact with the container and be a pseudo-terminal                               |
| `psmysql` | Running container name                                                             |
| `mysql`   | Connects to a database instance                                                    |
| `-u`      | Specifies the user account used to connect                                         |
| `-p`      | Use this password when connecting |

You must enter the password when the server prompts you.

Run the following to connect:

```shell
docker exec -it psmysql mysql -uroot -p
```

You are prompted to enter the password, which is `secret`. If you have changed the password, use your password. You will not see any characters as you type.

```text
Enter password:
```

You should see the following result.

??? example "Expected output"

    ```text
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 10
    Server version: {{tag}} Percona Server (GPL), Release 1, Revision 238b3c02

    Copyright (c) 2009-{{year_tag}} Percona LLC and/or its affiliates
    Copyright (c) 2000, {{year_tag}}, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    ```

## Troubleshooting

* Connection Refusal: Ensure Docker is running and the container is active. Verify port 3306 is accessible on the container's IP address.

* Incorrect Credentials: Double-check the root password you set during container launch.

* Data Loss: Always back up your data regularly outside the container volume.

## Security best practices

* Strong Passwords: Utilize complex, unique passwords for the root user and any additional accounts created within the container. The alphanumeric password should contain at least 12 characters. The password should include uppercase and lowercase letters, numbers, and symbols.

* Network Restrictions: Limit network access to the container by restricting firewall rules to only authorized IP addresses.

* Periodic Updates: Regularly update the Percona Server image and Docker Engine to mitigate known vulnerabilities.

* Data Encryption: Consider encrypting the data directory within the container volume for an additional layer of security.

* Monitor Logs: Actively monitor container logs for suspicious activity or errors.

Remember, responsible container management and robust security practices are crucial for safeguarding your MySQL deployment. By following these guidelines, you can leverage the benefits of Docker and Percona Server while prioritizing the integrity and security of your data.

--8<-- "quickstart-database-script.md"

--8<-- "quickstart-cleanup.md"

## Work with a database

[Work with a database:material-arrow-right:](quickstart-database-script.md){.md-button}

## Additional resources

* [Quickstart - Overview](quickstart-overview.md)

* [Install Percona Server for MySQL on Ubuntu](quickstart-apt.md)

* [Install Percona Server for MySQL on Oracle Linux](quickstart-yum.md)

* [Clean up your installation](quickstart-cleanup.md)

* [Next steps](quickstart-next-steps.md)
