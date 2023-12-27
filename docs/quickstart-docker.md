# Run and connect to a Docker container

The following steps create a Docker volume, start a Docker container, and connect to the Docker container.
{.power-number}


1. Run a Docker container

    The "Docker run" command creates and runs a new container from an image. The command modifies the container's behavior with the following options: 

    | Option | Description |
    |---|---|
    | `-d` | Detaches the container. The container runs in the background. |
    | `-p` | Makes the port available to services outside of Docker. |
    | `--name` | Provides a name to the container. If you do not use this option, Docker assigns a random name. |
    | `-e` | Adds an environmental variable. This example adds the  ` MYSQL_ROOT_PASSWORD `  environment variable. Choose a more secure password if needed.|
    |  `-v` | Lets you have persistent storage for the database. <br> To use a Docker volume for persistent storage with a database, specify the path where the database stores its data inside the container, usually `/var/lib/mysql`. |
    | `{{vers}}` | Use this tag to specify a specific version.|

    If we did not add a tag, Docker uses `latest`, the default tag, and pulls the newest image from [percona/percona-server on the Docker Hub]. This image can be in a different series or version from what you expect since the latest image changes over time.
    
    To run the ARM64 version of Percona Server, edit the command to use the `{{release}}-aarch64` tag.

    * Run a Docker container example

        ```{.bash data-prompt="$"}
        $ docker run -d -p 3306:3306 --name psmysql -e MYSQL_ROOT_PASSWORD=secret -v myvol:/var/lib/mysql percona/percona-server:{{vers}}
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Unable to find image 'percona/percona-server:{{vers}}' locally
            {{vers}}: Pulling from percona/percona-server
            3eb6a50586d1: Pull complete
            c5d348ef1f63: Pull complete
            0ad4027da0f8: Pull complete
            2e6beb1323c1: Pull complete
            82d90fa38f30: Pull complete
            0274392ca2c3: Pull complete
            665a7e779f15: Pull complete
            492939fc0f07: Pull complete
            7bab40a5e409: Pull complete
            c33fa6eb873d: Pull complete
            Digest: sha256:febc44d776e06c170d0abfd76c17d14c72dcd068064a4b4a20a7d7f58b4e6d5c
            7d61f8f49dd8376904cc577a4f87a5d0016b156cd84785151066de6d6b7c5b97
            ```

3. Connect to the database instance

    To connect to a MySQL database on a container, use the Docker exec command with the database instance connect command. You must know the name or ID of the container that runs the database server and the database credentials. This command runs a specified command in a running container. The`-it` option attaches an interactive terminal to the container so you can run queries and see the results. The database instance connect command connects to a MySQL server with the user name and password.

    For this guide, we have the following options:

    | Option    | Description |   
    | --- | --- |
    | `-it`        | Interact with the container and be a pseudo-terminal                               |
    | `psmysql` | Running container name                                                             |
    | `mysql`   | Connects to a database instance                                                    |
    | `-u`      | Specifies the user account used to connect                                         |
    | `-p`      | Use this password when connecting |

    You must enter the password when the server prompts you.

    * Connect to the database instance example
  
        ```{.bash data-prompt="$"}
        $ docker exec -it psmysql mysql -uroot -p
        ```

        At the prompt, enter the password, which is `secret`.

        ```{.text .no-copy}
        Enter password:
        ```

        You should see the following result.

        ??? example "Expected output"

            ```{.text .no-copy}
            Welcome to the MySQL monitor.  Commands end with ; or \g.
            Your MySQL connection id is 8
            Server version: {{release}} Percona Server (GPL), Release 1, Revision 74ca9072

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
