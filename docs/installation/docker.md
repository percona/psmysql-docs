# Running *Percona Server for MySQL* in a Docker Container

 *Percona Server for MySQL* has an official Docker image hosted on [Docker Hub](https://hub.docker.com/r/percona/percona-server/). If you want the latest version, use the `latest` tag. You can reference a specific version using the [Docker tag filter for the 8.0 versions](https://registry.hub.docker.com/r/percona/percona-server/tags?page=1&name=8.0). 

Make sure that you are using the latest version of Docker. The `apt` and `yum` versions may be outdated and cause errors.


## Starting a detached container

You can start a background container with the `--detached` or `-d` option, which runs the container in the background. In detached mode, the container exits when the root process used to run the container exits.

The following example starts a container named `ps` with the latest version of
*Percona Server for MySQL* 8.0. This action also creates the `root` user and uses `root` as the password. Please note that `root` is not a secure password. 

```shell
$ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  percona/percona-server:8.0
```
The output should be similar to the following:

```text
Unable to find image 'percona/percona-server:8.0' locally
8.0: Pulling from percona/percona-server
```

By default, Docker pulls the image from Docker Hub if it is not
available locally.

To view the container's logs, use the following command:

```shell
docker logs ps --follow
```
The output should resemble the following:

```text
Initializing database
2022-09-07T15:20:03.158128Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld 8.0.29-21) initializing of server in progress as process 15
2022-09-07T15:20:03.167764Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2022-09-07T15:20:03.530600Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2022-09-07T15:20:04.367600Z 0 [Warning] [MY-013829] [Server] Missing data directory for ICU regular expressions: /usr/lib64/mysql/private/.
...
2022-09-07T15:20:13.706090Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/lib/mysql/mysqlx.sock
2022-09-07T15:20:13.706136Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.29-21'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  Percona Server (GPL), Release 21, Revision c59f87d2854.
```
You can access the server when you see the `ready for connections` information in the log.
 
## Passing Options


You can pass options with the `docker run` command. For example, the following command uses UTF-8 as the default setting for character set and collation for all databases:

```shell
[root@docker-host] $ docker run -d \
 --name ps \
 -e MYSQL_ROOT_PASSWORD=root \
 percona/percona-server:8.0 \
 --character-set-server=utf8 \
 --collation-server=utf8_general_ci
```

## Accessing the Percona Server Container

The `docker exec` command lets you have a shell inside the container. This command uses `it` which forwards your input stream as an interactive TTY. 

An example of accessing the detached container:

```shell
[root@docker-host] $ docker exec -it ps /bin/bash
```

If you need to troubleshoot, the error log is found in `/var/log/` or `/var/log/mysql/`. The file name may be error.log or mysqld.log. 


## Troubleshooting

You can view the error log with the following command:

```shell
[mysql@ps] $ more /var/log/mysql/error.log
```
The output could be the following:

```text
...
2017-08-29T04:20:22.190474Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
2017-08-29T04:20:22.190520Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
...
```

## Accessing the database 

You can access the database either with `Docker exec` or using the `mysql` command in the container's shell.

An example of using `Docker exec` to access the database:

```shell
$ docker exec -ti ps mysql -uroot -proot
```

The output should be similar to the following:

```text
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
...
```

Exiting Percona Server also exits the container.

You can also run the MySQL command-line client within the container's shell to access the database:

```shell
[mysql@ps] $ mysql -uroot -proot
```
The output could be the following:

```text
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.29-21 Percona Server (GPL), Release 21, Revision c59f87d2854

Copyright (c) 2009-2022 Percona LLC and/or its affiliates
Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

## Accessing the server from an application in another container

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

This application container will be able to access the Percona Server container
via port 3306.

## Storing data

There are two ways to store data used by applications that run in Docker containers:

* Let Docker manage the storage of your data
by writing the database files to disk on the host system
using its internal volume management.

* Create a data directory on the host system on high-performance storage
and mount it to a directory visible from the container.
This method places the database files in a known location on the host system,
and makes it easy for tools and applications on the host system
to access the files.
The user should ensure that the directory exists, that the user accounts have required permissions, and that any other security mechanisms on the host system are set up correctly.

For example, if you create a data directory on a suitable volume
on your host system named `/local/datadir`,
you run the container with the following command:

```shell
[root@docker-host] $ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  -v /local/datadir:/var/lib/mysql \
  percona/percona-server:8.0
```

The `-v /local/datadir:/var/lib/mysql` option
mounts the `/local/datadir` directory on the host
to `/var/lib/mysql` in the container,
which is the default data directory used by *Percona Server for MySQL*.

Do not add MYSQL_ROOT_PASSWORD to the `docker run` command if the data directory contains subdirectories, files, or data.

!!! note 

    If you have SELinux enabled, assign the relevant policy type to the new data directory so that the container will be allowed to access it:

```
[root@docker-host] $ chcon -Rt svirt_sandbox_file_t /local/datadir
```

## Port forwarding

Docker allows mapping ports on the container to ports on the host system
using the `-p` option.
If you run the container with this option,
you can connect to the database by connecting your client
to a port on the host machine.
This ability simplifies consolidating instances to a single host.

To map the standard MySQL port 3306 to port 6603 on the host:

```shell
[root@docker-host] $ docker run -d \
 --name ps \
 -e MYSQL_ROOT_PASSWORD=root \
 -p 6603:3306 \
 percona/percona-server:8.0
```


## Exiting the container

If you are in the interactive shell, use CTRL-D or exit to exit the session.

If you have a non-shell process running, interrupt the process with `CTRL-C` before using either `CTRL-D` or `exit.`


## Stopping the container

The [docker stop](https://docs.docker.com/engine/reference/commandline/stop/) container command sends a TERM signal, then waits 10 seconds and sends a KILL signal. The following example stops the `ps` container:

```shell
$ docker stop ps
```

The default length of time before stopping a container is 10 seconds. A very large instance cannot dump the data from memory to disk within that time. With this type of instance, add the `--time` or the `-t` option to docker stop:

```shell
$ docker stop ps -t 600
```

## Removing the container

To remove a stopped container, use the `docker rm` command.

```shell
$ docker rm ps
```
## For more information

Review the [Docker Docs](https://docs.docker.com/)
