# Additional SELinux tools and management

## Installing SELinux management tools

To install SELinux management tools on RHEL 7, use the following command as root:

```{.bash data-prompt="$"}
$ yum -y install policycoreutils-python
```

On RHEL 8, utilize the following command as root:

```{.bash data-prompt="$"}
$ yum -y install policycoreutils-python-utils
```

Ensure you have root privileges to execute these commands.

## Switching SELinux mode

SELinux can operate in three modes: Disabled, Permissive, and Enforcing. 

To switch SELinux mode until the next reboot, use either of the following commands as root:

```{.bash data-prompt="$"}
$ setenforce Enforcing
```
or
```{.bash data-prompt="$"}
$ setenforce 1
```

To view the current SELinux mode, use either of the following commands:

```{.bash data-prompt="$"}
$ getenforce
```
or
```{.bash data-prompt="$"}
$ sestatus | grep -i mode
```

## Managing SELinux policies

### Using the semanage command

To add a service to the permissive domain, execute the following as root:

```{.bash data-prompt="$"}
$ semanage permissive -a <service_name>
```

To delete a service from the permissive domain, run:

```{.bash data-prompt="$"}
$ semanage permissive -d <service_name>
```

### List the current Permissive domains

To list the current permissive domains, use the following command:

```{.bash data-prompt="$"}
$ semanage permissive -l
```
