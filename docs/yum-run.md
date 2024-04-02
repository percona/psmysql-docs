# Run Percona Server for MySQL

Percona Server for MySQL stores the data files in `/var/lib/mysql/` by
default. The configuration file used to manage Percona Server for MySQL is the `/etc/my.cnf`.

## Manage the service

You would use `systemctl` to manage system services and daemons in a Linux environment. It provides a systematic and unified interface for controlling the state of services and checking their status. With `systemctl`, you can start a service to initiate its operations, stop it to terminate its operations, restart it to refresh its state, and check the status to monitor its performance and health. This command is essential for system administrators who need precise control over service management tasks.

The RHEL distributions and derivatives come with [systemd](https:/freedesktop.org/wiki/Software/systemd/) as the default system and service manager. 

`systemctl` is a command-line utility that is used to control the systemd system and service manager. It's a primary tool for managing services on Linux distributions that use systemd.

You can use either `sytemctl` or `service`. Currently, both options are supported.

Percona Server for MySQL is not started automatically on the RHEL distributions and derivatives after installation. 

The following command uses superuser privileges to start, check the status, stop, and restart the MySQL service using `systemctl`.

```{.bash data-prompt="$"}
$ sudo systemctl start mysql
$ sudo systemctl status mysql
$ sudo systemctl stop mysql
$ sudo systemctl restart mysql
```

## SELinux and security 

Security-Enhanced Linux (SELinux) is a security feature of the Linux operating system that provides a mechanism for supporting access control security policies. This ability includes mandatory access controls (MAC), which the United States National Security Agency (NSA) implemented and first introduced in CentOS and Red Hat Enterprise Linux. 

As you administer your system, SELinux gives you a framework to manage access controls, such as setting permissions and deciding which users or programs can access specific files. SELinux operates on the principle of least privilege, where every process and system user runs with only the minimum permissions necessary to function.

For information on SELinux, see [Working with SELinux](selinux.md).

The RHEL 8 distributions and derivatives have added a [system-wide cryptographic policies component]. This component lets administrators manage the cryptographic compliance of the entire system with a single command. This ability simplifies the task of meeting specific security requirements for cryptographic algorithms.


[system-wide cryptographic policies component]: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening
