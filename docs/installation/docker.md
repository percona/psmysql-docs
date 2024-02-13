# Run Percona Server for MySQL 5.7 in a Docker Container

!!! note

    The following instructions run Percona Server for MySQL 5.7 in a Docker container. 
    The instructions on how to run [Percona Server for MySQL 8.0 in a Docker container are available at this location](https://docs.percona.com/percona-server/latest/installation/docker.html).

## {{post}} Docker containers

To use {{post}} in a Docker container, you must request access to the {{post}} repository from Percona Support. This request provides you with the client ID and the access token. The Docker image is stored in a binary tarball. 

Download the tar file.

```{.bash data-prompt="$"}
$ sudo docker load -i percona-server-5.7.44-49-1.docker.tar
```

Provide a password before the download begins.

After the download, check the Docker images:

```{.bash data-prompt="$"}
$ sudo docker images
```

??? example "Expected output"

    ```{.text .no-copy}
    Repository              TAG            IMAGE ID       CREATED       SIZE
    percona/percona-server  5.7           (image number) (when created) (size of file)
    percona/percona-server  5.7.44 
    percona/percona-server  5.7.44-49
    percona/percona-server  5.7.44-49.1
    ```

Run the image in a container in detached mode with the following command:

```{.bash data-prompt="$"}
sudo docker run -d --name ps57 -t percona/percona-server:5.7 bash
```

Access the detached mode container with the following command:

```{.bash data-prompt="$"}
$ sudo docker exec -it ps57 /bin/bash
```

In the container, verify the version.

```{.bash data-prompt="$"}
$ mysql -V
```

??? example "Expected output"

    ```{.text .no-copy}
    mysql Ver 14.14 Distrib 5.7.44-49, for Linux (x86_64) using 7.0
    ```

## Docker images for versions that are not {{post}}

Docker images of Percona Server are hosted publicly on Docker Hub at
[https://hub.docker.com/r/percona/percona-server/](https://hub.docker.com/r/percona/percona-server/).

For more information about using Docker, see the [Docker Docs](https://docs.docker.com/).

!!! note

    Make sure that you are using the latest version of Docker. The ones provided via `apt` and `yum` may be outdated and cause errors.

We gather [Telemetry data] in the Percona packages and Docker images.

## Using the Percona Server Images

The following procedure describes how to run and access Percona Server 5.7
using Docker.

### Starting a Percona Server Instance in a Container

!!! note 

    By default, Docker pulls the image from Docker Hub if it is not available locally.
    
To start a container named `ps`
running the latest version in the Percona Server 5.7 series,
with the root password set to `root`:

```{.bash data-prompt="$"}
$ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  percona/percona-server:5.7
```

!!! warning

    `root` is not a secure password. The word is used in the example for illustrative purposes only. Do not use this example in production.

!!! note

    The docker stop command sends a TERM signal. Docker waits 10 seconds and sends a KILL signal. A very large instance cannot dump the data from memory to disk in 10 seconds. If you plan to run a very large instance, add the following option to the docker run command.

      `–stop-timeout 600`

## Accessing the Percona Server Container

To access the shell in the container:

```{.bash data-prompt="$"}
[root@docker-host] $ docker exec -it ps /bin/bash
```

From the shell, you can view the error log:

```{.text .no-copy}
[mysql@ps] $ more /var/log/mysql/error.log
2017-08-29T04:20:22.190474Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2017-08-29T04:20:22.190520Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
...
```

You can also run the MySQL command-line client
to access the database directly:

```{.bash data-prompt="$"}
[mysql@ps] $ mysql -uroot -proot
```

The output may be similar to the following:

```{.text .no-copy}
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.19-17 Percona Server (GPL), Release '17', Revision 'e19a6b7b73f'

Copyright (c) 2009-2017 Percona LLC and/or its affiliates
Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its affiliates. Other names may be trademarks of their respective owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

## Accessing Percona Server from Application in Another Container

The image exposes the standard MySQL port 3306,
so container linking makes Percona Server instance available
from other containers.
To link a container running your application
(in this case, from image named `app/image`)
with the Percona Server container,
run it with the following command:

```{.bash data-prompt="$"}
[root@docker-host] $ docker run -d \
  --name app \
  --link ps \
  app/image:latest
```

This application container can access the Percona Server container
via port 3306.

## Environment Variables

When running a Docker container with Percona Server,
you can adjust the instance's configuration by passing one or more environment variables with the `docker run` command.

!!! note

    If you start the container with a data directory containing a database, these variables are not effective. Any pre-existing database will always remain untouched on container startup.

The variables are optional, except that you must specify at least one of the following:

* [MYSQL_ALLOW_EMPTY_PASSWORD](https://docs.percona.com/percona-server/8.0/installation/docker.html#mysql-allow-empty-password): least secure, use only for testing.

* [MYSQL_ROOT_PASSWORD](https://docs.percona.com/percona-server/8.0/installation/docker.html#mysql-root-password): more secure,
but setting the password on the command line is not recommended
for sensitive production setups.

* [MYSQL_RANDOM_ROOT_PASSWORD](https://docs.percona.com/percona-server/8.0/installation/docker.html#mysql-random-root-password): most secure,
recommended for production.

!!! note

   To further secure your instance, use the [MYSQL_ONETIME_PASSWORD](https://docs.percona.com/percona-server/8.0/installation/docker.html#mysql-onetime-password) variable if you are running version 5.6 or later.

## Storing Data

There are two ways to store data used by applications
that run in Docker containers:

* Let Docker manage the storage of your data
by writing the database files to disk on the host system
using its internal volume management.

* Create a data directory on the host system
(outside the container on high-performance storage)
and mount it to a directory visible from inside the container.
This directory places the database files in a known location on the host system and makes it easy for tools and applications on the host system
to access the files.
The user should ensure that the directory exists and that permissions and other security mechanisms on the host system
are set up correctly.

For example, if you create a data directory on a suitable volume
on your host system named `/local/datadir`,
you run the container with the following command:

```{.bash data-prompt="$"}
$ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  -v /local/datadir:/var/lib/mysql \
  percona/percona-server:5.7
```

The `-v /local/datadir:/var/lib/mysql` option
mounts the `/local/datadir` directory on the host
to `/var/lib/mysql` in the container,
which is the default data directory used by Percona Server.

!!! note

    If you have the Percona Server container instance with a data directory that already contains data (the `mysql` subdirectory where all our system tables are stored), the [MYSQL_ROOT_PASSWORD](https://docs.percona.com/percona-server/8.0/installation/docker.html#mysql-root-password) variable should be omitted from the `docker run` command.

!!! note

    If you have SELinux enabled, assign the relevant policy type to the new data directory so that the container will be allowed to access it:

    ```{.bash data-prompt="$"}
    $ sudo chcon -Rt svirt_sandbox_file_t /local/datadir
    ```

## Port Forwarding

Docker allows mapping ports on the container to ports on the host system
using the `-p` option.
If you run the container with this option,
you can connect to the database by connecting your client
to a port on the host machine.
This can significantly simplify consolidating many instances to a single host.

To map the standard MySQL port 3306 to port 6603 on the host:

```{.bash data-prompt="$"}
[root@docker-host] $ docker run -d \
 --name ps \
 -e MYSQL_ROOT_PASSWORD=root \
 -p 6603:3306 \
 percona/percona-server:5.7
```

## Passing Options to Percona Server

You can pass options to the Percona Server by appending them to the `docker run` command when running the container.
For example, to start run Percona Server with UTF-8
as the default setting for character set
and collation for all databases:

```{.bash data-prompt="$"}
$ docker run -d \
 --name ps \
 -e MYSQL_ROOT_PASSWORD=root \
 percona/percona-server:5.7 \
 --character-set-server=utf8 \
 --collation-server=utf8_general_ci
```

[Telemetry data]: ../telemetry.md
