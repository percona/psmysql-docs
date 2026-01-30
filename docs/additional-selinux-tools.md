# Additional SELinux tools and management

## Installing SELinux management tools

To install SELinux management tools on Red Hat Enterprise Linux 8 or later, run the following command as root:

```shell
yum -y install policycoreutils-python-utils
```

Ensure you have root privileges to execute these commands.

## Switching SELinux mode

SELinux can operate in three modes: Disabled, Permissive, and Enforcing. 

To switch SELinux mode until the next reboot, use either of the following commands as root:

```shell
setenforce Enforcing
```
or
```shell
setenforce 1
```

To view the current SELinux mode, use either of the following commands:

```shell
getenforce
```
or
```shell
sestatus | grep -i mode
```

## Managing SELinux policies

### Using the semanage command

To add a service to the permissive domain, execute the following as root:

```shell
semanage permissive -a <service_name>
```

To delete a service from the permissive domain, run:

```shell
semanage permissive -d <service_name>
```

### List the current Permissive domains

To list the current permissive domains, use the following command:

```shell
semanage permissive -l
```
