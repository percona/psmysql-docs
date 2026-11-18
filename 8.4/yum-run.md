> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Run Percona Server for MySQL

Percona Server for MySQL stores the data files in `/var/lib/mysql/` by default. The configuration file used to manage Percona Server for MySQL is the `/etc/my.cnf`.

The following commands start, provide the server status, stop the server, and restart the server.

Note

The RHEL distributions and derivatives come with [systemd](https:/freedesktop.org/wiki/Software/systemd/) as the default system and service manager so you can invoke all of the commands with `sytemctl` instead of `service`. Currently, both options are supported.

1. Percona Server for MySQL is not started automatically on the RHEL distributions and derivatives after installation. Start the server with the following command:

   ```
   sudo service mysql start
   ```

1. Review the service status with the following command:

   ```
   sudo service mysql status
   ```

1. Stop the service with the following command:

   ```
   sudo service mysql stop
   ```

1. Restart the service with the following command:

   ```
   sudo service mysql restart
   ```

## SELinux and security considerations

For information on working with SELinux, see [Working with SELinux](https://docs.percona.com/percona-server/8.4/selinux.html).

The RHEL 8 distributions and derivatives have added [system-wide cryptographic policies component](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening). This component allows the configuration of cryptographic subsystems.
