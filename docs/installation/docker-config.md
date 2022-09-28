## Docker environment variables

When running a Docker container with Percona Server,
you can adjust the configuration of the instance
Add one or more environment variables to the `docker run` command.

These variables will not affect you if you start the container with a data directory that already contains a database. Any pre-existing database remains untouched on the container startup.

The variables are optional, but you must specify at least one of the following:

* `MYSQL_DATABASE` - the database schema name that is created when the container starts

* `MYSQL_USER` - create a user account when the container starts

* `MYSQL_PASSWORD` - used with `MYSQL_USER` to create a password for that user account.

* `MYSQL_ALLOW_EMPTY_PASSWORD` - creates a root user with an empty password. This option is insecure and only should be used for testing or proof of concept when the database can be removed afterward. Anyone can connect as `root`.

* `MYSQL_ROOT_PASSWORD` - this password is used for the `root` user account. This option is not recommended for production.

* `MYSQL_RANDOM_ROOT_PASSWORD` - set this variable instead of `MYSQL_ROOT_PASSWORD` when you want Percona Server to generate a password for you. The generated password is available in the container's logs only during the first start of the container. Use `docker logs`. You cannot retrieve the password after the first start.

To further secure your instance, use the `MYSQL_ONETIME_PASSWORD` variable.

These variables are visible to anyone able to run `Docker inspect`. 

```shell
$ docker inspect ps
```

The output could be the following:

```text
...
 "Env": [
                "MYSQL_ROOT_PASSWORD=root",
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "PS_VERSION=8.0.29-21.1",
                "OS_VER=el8",
                "FULL_PERCONA_VERSION=8.0.29-21.1.el8"
               ]
...
```

You should use `Docker secrets` or volumes instead. 

Percona Server for MySQL also allows adding the `_FILE` suffix to a variable name. This suffix lets you add the value in a path so that the value cannot be inspected from outside the container.




