# Clean up

The following steps do the following:

* Exits the MySQL command client shell and the Docker container

* Removes the Docker container and the Docker image

* Removes the Docker volume.

The steps are as follows:
{.power-number}

1. To exit the MySQL command client shell we use `exit`. You can also use the `\q` or `quit` commands. The execution of the statement also closes the connection.

    * An example of exiting the MySQL command client shell and closing the connection.

        ```{.bash data-prompt="mysql>"}
        mysql> exit
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Bye
            ```

2. You may want to remove the docker container and the image if they are no longer needed or to free up disk space. To remove a docker container, use the command `docker rm` followed by `psmysql`, the container ID or name. To remove a docker image, use the command `docker rmi` followed by `percona/percona-server:8.0.34`, the image ID or name and the tag.

    * An example of removing a Docker container and a Docker image.

        ```{.bash data-prompt="$"}
        $ docker container rm psmysql -f
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            psmysql
            ```

        ```
        $ docker image rmi percona/percona-server:8.0.34
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Untagged: percona/percona-server:8.0.34
            Untagged: percona/percona-server@sha256:4944f9b365e0dc88f41b3b704ff2a02d1459fd07763d7d1a444b263db8498e1f
            Deleted: sha256:b2588da614b1f382468fc9f44600863e324067a9cae57c204a30a2105d61d9d9
            Deleted: sha256:1ceaa6dc89e328281b426854a3b00509b5df13826a9618a09e819a830b752ebd
            Deleted: sha256:77471692427a227eb16d06907357956c3bb43f0fdc3ecf6f8937e1acecae24fe
            Deleted: sha256:8db06cc7b0430437edc7f118b139d2195cb65e2e8025f9a4517d16778f615384
            Deleted: sha256:e5a57a2fafec4ab9482240f28927651d56545c19626e344aceb8be3704c3c397
            Deleted: sha256:f86198f39b893674d44d424c958f23183bf919d2ced20e1f519714d0972d75ed
            Deleted: sha256:db9672f7e12e374d5e9016b758a29d5444e8b0fd1246a6f1fc5c2b3c847dddcf
            ```

3. Remove the docker volume if a container does not use the volume, and you no longer need it.

    * An example of removing a Docker volume.
  
        ```{.bash data-prompt="$"}
        $ docker volume rm myvol
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            myvol
            ```

## Next step

[Next steps :material-arrow-right:](quickstart-next-steps.md){.md-button}