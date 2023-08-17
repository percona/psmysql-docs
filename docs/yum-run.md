# Run Percona Server for MySQL

Percona Server for MySQL stores the data files in `/var/lib/mysql/` by
default. The configuration file used to manage Percona Server for MySQL is the `/etc/my.cnf`.

The following commands start, provide the server status, stop the server, and restart the server.

!!! note

    The RHEL distributions and derivatives come with [systemd](https:/freedesktop.org/wiki/Software/systemd/) as the default system and service manager so you can invoke all of the commands with `sytemctl` instead of `service`. Currently, both options are supported.

1. Percona Server for MySQL is not started automatically on the RHEL distributions and derivatives after installation. Start the server with the following command:
	
	```{.bash data-prompt="$"}
	$ sudo service mysql start
	```

2. Review the service status with the following command:

	```{.bash data-prompt="$"}
	$ sudo service mysql status
	```

3. Stop the service with the following command:
	
	```{.bash data-prompt="$"}
	$ sudo service mysql stop
	```

4. Restart the service with the following command:

	```{.bash data-prompt="$"}
	$ sudo service mysql restart
	```

## SELinux and security considerations

For information on working with SELinux, see [Working with SELinux](selinux.md).

The RHEL 8 distributions and derivatives have added [system-wide cryptographic policies component](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening). This component allows the configuration of cryptographic subsystems.
