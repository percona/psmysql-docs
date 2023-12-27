# Exit the Docker container

## Stop the container

The [docker stop](https://docs.docker.com/engine/reference/commandline/stop/) container command sends a TERM signal, waits 10 seconds, and sends a KILL signal. The following example stops the `ps` container:

```{.bash data-prompt="$"}
$ docker stop ps
```

The default length of time before stopping a container is 10 seconds. A large instance cannot dump the data from memory to disk within that time. With this type of instance, add the `--time` or the `-t` option to docker stop:

```{.bash data-prompt="$"}
$ docker stop ps -t 600
```

## Exit the container

If you are in the interactive shell, use `CTRL-D` or `exit` to exit the session.

If you have a non-shell process running, interrupt the process with `CTRL-C` before using `CTRL-D` or `exit.`


## Remove the container

To remove a stopped container, use the `docker rm` command.

```{.bash data-prompt="$"}
$ docker rm ps
```