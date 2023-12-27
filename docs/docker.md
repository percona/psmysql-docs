# Run Percona Server for MySQL in a Docker Container

Deploying a Percona Server for MySQL container is an efficient, fast solution to setting up a database quickly without using too many resources. This type of deployment works best for small to medium applications.

You should deploy a Percona Server for MySQL database in Docker for several reasons. Here are some of them:

- Portability: Docker containers can run on any platform that supports Docker. This flexibility lets you move your database or installation steps from one platform to another.
- Isolation: Docker containers are isolated from each other and the host system. This isolation means you can run multiple instances of MySQL on the same machine without interfering with each other or affecting the host's performance. You can also isolate your database from other applications or services that might pose a security risk or consume too many resources.
- Scalability: Depending on the load and demand, you can scale docker containers up or down. You can use tools like Docker Compose or Kubernetes to orchestrate multiple containers and manage their configuration, networking, and deployment. You can also use Docker Swarm or Amazon ECS to distribute your containers across multiple nodes and achieve high availability and fault tolerance.
- Versioning: Docker images and containers contain all the dependencies and configurations needed to run your application. You can use tags to specify different versions of your images and easily switch between them. You can also use Docker Hub or other registries to store and share your images with others.
- Development: Docker containers can help you create a consistent and reproducible development environment that matches your production environment. You can use tools like Dockerfile or Docker Build to automate the creation of your images and ensure they have the same settings and packages as your production images. You can also use tools like Docker Volumes or Bind Mounts to persist and share your data between containers or the host system.

[Install Docker](https://docs.docker.com/get-docker/) on your system. Make sure you use the latest version of Docker. The `APT` or `YUM` versions may be outdated and cause errors.

We gather [Telemetry data] in the Percona packages and Docker images.

## Percona Server for MySQL versions

Percona Server for MySQL has an official Docker image hosted on [Docker Hub](https://hub.docker.com/r/percona/percona-server/). Download a specific version by adding that [Docker tag filter for the {{vers}} versions]. If you do not add a tag, Docker uses `latest`, the default tag, and pulls the newest image. This image can be in a different series or version from what you expect since the latest image changes over time.
    
To run the ARM64 version of Percona Server, edit the command to use the `{{vers}}-aarch64` tag.

## Benefits of the Docker run

The `Docker run` command automatically pulls the image from a registry if that image is not available locally and starts a Docker container. A container is an isolated environment that runs an application on the host operating system. An image is a template that contains the application code and its dependencies. You can use the "Docker run" command to run an application in a container without affecting the host system or other containers.

The benefits of using the `Docker run` command are:

- Allows you to run applications consistently and safely across different platforms and environments.

- Reduces the overhead and complexity of installing and configuring applications and their dependencies on the host system.

- Improves the security and isolation of applications by limiting their access to the host resources and other containers.

- Enables faster development and deployment cycles by allowing you to create, update, and destroy containers quickly.

## Starting a detached container

Start a container with the `--detached` or `-d` option and run the container in the background. The container exits when the root process which runs the container exits.

You must provide at least one environmental variable, such as `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD`. The database refuses to initialize if you do not add at least one variable.

The following example starts a container named `ps` with the {{vers}} version of
Percona Server for MySQL. The command creates the `root` user and uses `root`` as the password. Please note that `root` is not a secure password.

```{.bash data-prompt="$"}
$ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  percona/percona-server:{{vers}}
```

??? example "Expected output"

    ```{.text .no-copy}
    Unable to find image 'percona/percona-server:{{vers}}' locally
    {{vers}}: Pulling from percona/percona-server
    ```

By default, Docker pulls the image from Docker Hub if it is unavailable locally.

For example, the following command uses UTF-8 as the default setting for character set and collation for all databases:

```shell
[root@docker-host] $ docker run -d \
 --name ps \
 -e MYSQL_ROOT_PASSWORD=root \
 percona/percona-server:{{vers}} \
 --character-set-server=utf8 \
 --collation-server=utf8_general_ci
```

## Port forwarding

Docker allows mapping ports on the container to ports on the host system using the `-p` option.
If you run the container with this option, you can connect your client
to a port on the host machine. 

To map the standard MySQL port 3306 to port 6603 on the host:

```shell
[root@docker-host] $ docker run -d \
 --name ps \
 -e MYSQL_ROOT_PASSWORD=root \
 -p 6603:3306 \
 percona/percona-server:{{vers}}
```

## Access the container

The `docker exec` command lets you have a shell inside the container. This command uses `it` to forward your input stream as an interactive TTY. 

An example of accessing a detached container:

```shell
[root@docker-host] $ docker exec -it ps /bin/bash
```

## Access the database 

You can access the database either with `Docker exec` or using the `mysql` command in the container's shell.

An example of using `Docker exec` to access the database:

```{.bash data-prompt="$"}
$ docker exec -ti ps mysql -uroot -proot
```

??? example "Expected output"

    ```{.text .no-copy}   
    mysql: [Warning] Using a password on the command line interface can be insecure.
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 9
    ...
    ```

When you exit the database, you also close the container.

You can also run the MySQL command-line client within the container's shell to access the database:

```shell
[mysql@ps] $ mysql -uroot -proot
```

??? example "Expected output"

    ```{.text .no-copy}
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 12
    Server version: 8.1.0-1 Percona Server (GPL), Release 1, Revision 74ca9072

    Copyright (c) 2009-2023 Percona LLC and/or its affiliates
    Copyright (c) 2000, 2023, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    ```

## Access the server from an application in another container

The image exposes the standard MySQL port 3306,
so container linking makes the Percona Server instance available
from other containers.
To link a container running your application
(in this case, from an image named `app/image`)
with the Percona Server container,
run it with the following command:

```shell
[root@docker-host] $ docker run -d \
  --name app \
  --link ps \
  app/image:latest
```

This application container is able to access the Percona Server container by port 3306.




## For more information

Review the [Docker Docs](https://docs.docker.com/)

[Docker tag filter for the {{vers}} versions]: https://registry.hub.docker.com/r/percona/percona-server/tags?page=1&name={{vers}}

[Telemetry data]: telemetry.md