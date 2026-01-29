# Quickstart - Run Percona Server for MySQL container images with Docker

You are welcome to name any items to match your organization's standards or use your table structure and data. If you do, the results are different from the expected results.

## Prerequisites

* Docker Engine installed and running
* Stable internet connection
* Basic understanding of the command-line interface (CLI)

Always adapt the commands and configurations to your specific environment and security requirements.


## Start a Docker container

To use the "Docker run" command, specify the name or ID of the image you want to use and, optionally, some flags and arguments that modify the container's behavior. The command has the following options:

| Option | Description |
|---|---|
| `-d` | Runs the container in detached mode, allowing the container to operate in the background. |
| `-p 3306:3306` |Maps the container's MySQLport (3306) to the same port as your host, enabling external access.|
| `--name psmysql` | Provides a meaningful name to the container. If you do not use this option, Docker adds a random name. |
| `-e MYSQL_ROOT_PASSWORD=secret` | Adds an environmental variable and changes the password from the default password. |
|  `--v myvol:/var/lib/mysql` | Mounts a host directory (myvol) as the container's data volume, ensuring persistent storage for the database between container lifecycles. |
| `percona/percona-server:{{tag}}` | The image with the tag ({{tag}}) to specify a specific release. |

You must provide at least one environment variable to access the database, such as `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD` or the instance refuses to initialize.

If needed, you can replace the `secret` password with a [stronger password](#security-measures).

For this document, we add the `{{tag}}` tag. In Docker, a tag is a label assigned to an image and is used to maintain different versions of an image. If we did not add a tag, Docker uses `latest` as the default tag and downloads the latest image from [percona/percona-server on the Docker Hub :octicons-link-external-16:](https://hub.docker.com/r/percona/percona-server).

To run the Docker ARM64 version of Percona Server for MySQL, use the `{{arm_tag}}` tag instead of `{{tag}}`.

```{.bash data-prompt="$"}
$ docker run -d -p 3306:3306 --name psmysql \
--platform linux/amd64 \
-e MYSQL_ROOT_PASSWORD=secret \
-v myvol:/var/lib/mysql \
percona/percona-server:{{tag}}
```

??? example "Expected output"

    ```{.text .no-copy}
    Unable to find image 'percona/percona-server:{{tag}}' locally
    Pulling from percona/percona-server
    b902d6b6048a: Pull complete
    16cef723486e: Pull complete
    66df07bf7a1c: Pull complete
    b2963ee1caa4: Pull complete
    8ff166e7ebab: Pull complete
    fc0329eb813b: Pull complete
    46522d05868c: Pull complete
    8a91dcc6141f: Pull complete
    2225668f8cee: Pull complete
    Digest: sha256:ec4cdd25ec3887a90282dda1298a475a88429953fd7e2718e22fd6e205626047  
    Status: Downloaded newer image for percona/percona-server:{{tag}}
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

Connect to the database instance example

```{.bash data-prompt="$"}
$ docker exec -it psmysql mysql -uroot -p
```

You are prompted to enter the password, which is `secret`. If you have changed the password, use your password. You will not see any characters as you type.

```{.text .no-copy}
Enter password:
```

You should see the following result.

??? example "Expected output"

    ```{.text .no-copy}
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 10
    Server version: {{tag}} Percona Server (GPL), Release 1, Revision 238b3c02

    Copyright (c) 2009-{{year_tag}} Percona LLC and/or its affiliates
    Copyright (c) 2000, {{year_tag}}, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
    ```

--8<-- "quickstart-database-script.md"

--8<-- "quickstart-cleanup.md"

## Troubleshooting

* Connection Refusal: Ensure Docker is running and the container is active. Verify port 3306 is accessible on the container's IP address.

* Incorrect Credentials: Double-check the root password you set during container launch.

* Data Loss: Always back up your data regularly outside the container volume.

## Security measures

* Strong Passwords: Utilize complex, unique passwords for the root user and any additional accounts created within the container. The alphanumeric password should contain at least 12 characters. The password should include uppercase and lowercase letters, numbers, and symbols.

* Network Restrictions: Limit network access to the container by restricting firewall rules to only authorized IP addresses.

* Periodic Updates: Regularly update the Percona Server image and Docker Engine to mitigate known vulnerabilities.

* Data Encryption: Consider encrypting the data directory within the container volume for an additional layer of security.

* Monitor Logs: Actively monitor container logs for suspicious activity or errors.

Remember, responsible container management and robust security practices are crucial for safeguarding your MySQL deployment. By following these guidelines, you can leverage the benefits of Docker and Percona Server while prioritizing the integrity and security of your data.

## Other installation methods

- [Quickstart - Overview](quickstart-overview.md)
- [Install Percona Server for MySQL on Ubuntu](quickstart-apt.md)
- [Install Percona Server for MySQL on Oracle Linux](quickstart-yum.md)
- [Clean up your installation](quickstart-cleanup.md)
- [Next steps](quickstart-next-steps.md)

## Next step

[Choose your next steps:material-arrow-right:](quickstart-next-steps.md){.md-button}
