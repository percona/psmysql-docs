# Start and connect to a Docker container

The following steps create a Docker volume, start a Docker container, and connect to the Docker container.
{.power-number}

1. Create a Docker volume

    One of the benefits of using a Docker volume for persistent storage with a database is that it allows you to keep your data safe and accessible across different containers. For example, if you want to upgrade your database image to a newer version, you can stop the old container and start a new one with the same volume attached without losing any data. Another benefit is that you can quickly backup and restore your data using the docker cp command or mount the volume to another container.

    * Create a volume example

        ```{.bash data-prompt="$"}
        $ docker volume create myvol
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            myvol
            ```

2. Start a Docker container

    To use the "Docker run" command, specify the name or ID of the image you want to use and, optionally, some flags and arguments that modify the container's behavior. The command has the following options:

    | Option | Description |
    |---|---|
    | `--name` | Provides a name to the container. If you do not use this option, Docker adds a random name. |
    | `-d` | Detaches the container. The container runs in the background. |
    | `-e` | Adds an environmental variable. This example adds the  ` MYSQL_ROOT_PASSWORD `  environment variable. The instance refuses to initialize if no environmental variable is added. Choose a more secure password, if needed. |
    |  `--volume` | Lets you have persistent storage for the database. |
    | `8.0.34` | Use this tag to specify a specific version. |

    You must provide at least one environment variable to access the database, such as `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD` or the instance refuses to initialize.

    For this document, we are using the `8.0.34` tag. In Docker, a tag is a label assigned to an image. Tags are used to maintain different versions of an image. If we did not add a tag, Docker uses `latest` as the default tag and downloads the latest image from [percona/percona-server on the Docker Hub].

    ??? Information "Benefits of using Docker run"

        The "Docker run" command automatically pulls the image from a registry if that image is not available locally and starts a container. A container is an isolated environment that runs an application on the host operating system. An image is a template that contains the application code and its dependencies. You can use the "Docker run" command to run an application in a container without affecting the host system or other containers.

        The benefits of using the "Docker run" command are:

        - Allows you to run applications consistently and safely across different platforms and environments.
        - Reduces the overhead and complexity of installing and configuring applications and their dependencies on the host system.
        - Improves the security and isolation of applications by limiting their access to the host resources and other containers.
        - Enables faster development and deployment cycles by allowing you to create, update, and destroy containers easily.

    To use a Docker volume for persistent storage with a database, specify the path where the database stores its data inside the container, usually `/var/lib/mysql`.

    * Run a Docker container example

        ```{.bash data-prompt="$"}
        $ docker run -d -p 3306:3306 --name psmysql -e MYSQL_ROOT_PASSWORD=secret -v myvol:/var/lib/mysql percona/percona-server:8.0.34
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Unable to find image 'percona/percona-server:8.0.34' locally
            8.0.34: Pulling from percona/percona-server
            d6f6a69cdebb: Pull complete
            4f8794caafba: Pull complete
            d80629460c71: Pull complete
            f550e519928f: Pull complete
            fb91f65fb039: Pull complete
            e8f7e0c2fbae: Pull complete
            Digest: sha256:4944f9b365e0dc88f41b3b704ff2a02d1459fd07763d7d1a444b263db8498e1f
            Status: Downloaded newer image for percona/percona-server:8.0.34
            01d4f6d188b609ff92158605f8528d640aa28ff5720efa0286b36f51d4bec11c
            ```

3. Connect to the database instance

    To connect to a MySQL database on a container, use the Docker exec command with the database instance connect command. You must know the name or ID of the container that runs the database server and the database credentials. The Docker exec command runs a specified command in a running container. The`-it` option attaches an interactive terminal to the container, so you can run queries and see the results. The database instance connect command connects to a MySQL server with the user name and password.

    For this example, we have the following options:

    | Option      | Description                                                                        |
    | ----------- | ---------------------------------------------------------------------------------- |
    | `it`        | Interact with the container and be a pseudo-terminal                               |
    | `psmysql` | Running container name                                                             |
    | `mysql`   | Connects to a database instance                                                    |
    | `-u`      | Specifies the user account used to connect                                         |
    | `-p`      | Use this password when connecting |

    You must enter the password when the server prompts you.

    * Connect to the database instance example
  
        ```{.bash data-prompt="$"}
        $ docker exec -it psmysql mysql -uroot -p
        ```

        You are prompted to enter the password, which is `secret`.

        ```{.text .no-copy}
        Enter password:
        ```

        You should see the following result.

        ??? example "Expected output"

            ```{.text .no-copy}
            Welcome to the MySQL monitor.  Commands end with ; or \g.
            Your MySQL connection id is 8
            Server version: 8.0.34-26 Percona Server (GPL), Release 26, Revision 0fe62c85

            Copyright (c) 2009-2023 Percona LLC and/or its affiliates
            Copyright (c) 2000, 2023, Oracle and/or its affiliates.

            Oracle is a registered trademark of Oracle Corporation and/or its
            affiliates. Other names may be trademarks of their respective
            owners.

            Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

            mysql>
            ```

## Next step

[Create a database and table :material-arrow-right:](quickstart-database.md){.md-button}


[Percona Server for MySQL documentation]: https://docs.percona.com/percona-server/8.0/

[percona/percona-server on the Docker Hub]: https://hub.docker.com/r/percona/percona-server