# Store data in Docker

There are two ways to store data used by applications that run in Docker containers:

* Let Docker manage the storage of your data by writing the database files to disk on the host system and us its internal volume management.

* Create a data directory on the host system on high-performance storage and mount it to a directory visible from the container.


This method places the database files in a known location on the host system and makes it easy for tools and applications on the host system
to access the files. The user should ensure that the directory exists, that the user accounts have required permissions, and that any other security mechanisms on the host system are set up correctly.

For example, if you create a data directory on a suitable volume on your host system named `/local/datadir`, you run the container with the following command:

```shell
[root@docker-host] $ docker run -d \
  --name ps \
  -e MYSQL_ROOT_PASSWORD=root \
  -v /local/datadir:/var/lib/mysql \
  percona/percona-server:{{vers}}
```

The `-v /local/datadir:/var/lib/mysql` option mounts the `/local/datadir` directory on the host to `/var/lib/mysql` in the container,
which is the default data directory used by Percona Server for MySQL.

Do not add MYSQL_ROOT_PASSWORD to the `docker run` command if the data directory contains subdirectories, files, or data.

!!! note 

    If you have SELinux enabled, assign the relevant policy type to the new data directory so that the container will be allowed to access it:

    ```
    [root@docker-host] $ chcon -Rt svirt_sandbox_file_t /local/datadir
    ```
