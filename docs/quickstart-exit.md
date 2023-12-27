# Clean up

The following steps do the following:

* Exits the MySQL command client shell and the Docker container

* Removes the Docker container 

* Removes the Docker image

* Removes the Docker volume

The steps are as follows:
{.power-number}

1. To exit the MySQL command client shell, we use `exit`. You can also use the `\q` or `quit` commands. The execution of the statement also closes the connection.


    ```{.bash data-prompt="mysql>"}
    mysql> exit
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Bye
        ```

2. You may want to remove the docker container if the container is no longer needed or to free up disk space. To remove a docker container, use the command `docker rm` followed by `psmysql`, the container ID or name. The example uses the `-f` option to force the removal. 


    ```{.bash data-prompt="$"}
    $ docker container rm psmysql -f
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        psmysql
        ```

3. To remove a docker image, use the command `docker rmi` followed by `percona/percona-server:{{vers}}`, the image ID or name, and the tag. If running the ARM64 version of Percona Server, edit the Docker command to use the `{{release}}-aarch64` tag.


    ```
    $ docker image rmi percona/percona-server:{{vers}}
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Untagged: percona/percona-server:{{vers}}
        Untagged: percona/percona-server@sha256:febc44d776e06c170d0abfd76c17d14c72dcd068064a4b4a20a7d7f58b4e6d5c
        Deleted: sha256:f945412b337cfb5bbe67a59c8a56a9f1b7334d35685790f3b80ed9fe52c7d4ff
        Deleted: sha256:a511ae543dfe386b78a6946e6445bb3b97f596288a2bbe97e38cfc5f763bb6ed
        Deleted: sha256:da0cef34c3c4200c54f9c5e2f657c0ff649413f70cbc331d81500b6870c94208
        Deleted: sha256:a445f7deabf75eb1cab04f8e93e2ecb329f6e7982a40aef2c37ef66c35132f4a
        Deleted: sha256:adf285ef33e55c9bc77c67ec257d813c6844edc9a5a444d875375eeb7ceed751
        Deleted: sha256:ca4bf5af3260284ed6ddf89c45d043ed57a8f5cb7fb8f2b6030e6327444ccb89
        Deleted: sha256:b0017201477d4326ec1724457bceff405d68da23b3fdbdb55a2f54df6626acca
        Deleted: sha256:ccdf20540bb107e15882b9d198cc25eb454d0ed16cddb973dd110f253eea4d87
        Deleted: sha256:a1fa655b6a1d511b4ba52d61fdb3057833c8cf41b4afe209ffd532cb767756ca
        Deleted: sha256:e39093249d950c9c7af3005d15c61b4560226bf5ef749f40a35ff89ec996e795
        Deleted: sha256:f443fe07d3f67a41cf68025ead92e9c5f9cb2431d5875e3368a33d8e3bd04eca
        ```

3. Remove the docker volume if no container uses it and you no longer need it.

  
    ```{.bash data-prompt="$"}
    $ docker volume rm myvol
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        myvol
        ```

## Next step

[Next steps :material-arrow-right:](quickstart-next-steps.md){.md-button}
