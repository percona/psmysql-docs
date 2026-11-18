> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Run Percona Server for MySQL 9.7 after APT repository installation

Percona Server for MySQL stores the data files in `/var/lib/mysql/` by default. You can find the configuration file that is used to manage Percona Server for MySQL in `/etc/mysql/my.cnf`.

Note

Debian and Ubuntu installation doesn’t automatically create a special `debian-sys-maint` user which can be used by the control scripts to control the Percona Server for MySQL `mysqld` and `mysqld_safe` services which was the case with previous Percona Server for MySQL versions. If you still require this user you’ll need to create it manually.

Run the following commands as root or by using the sudo command

1. Starting the service

   Percona Server for MySQL is started automatically after it gets installed unless it encounters errors during the installation process. You can also manually start it by running: `service mysql start`

1. Confirming that service is running. You can check the service status by running: `service mysql status`

1. Stopping the service

   You can stop the service by running: `service mysql stop`

1. Restarting the service. `service mysql restart`

Note

Debian 9.0 (stretch) and Ubuntu 18.04 LTS (bionic) come with [systemd](http://freedesktop.org/wiki/Software/systemd/) as the default system and service manager. You can invoke all the above commands with `systemctl` instead of `service`. Currently, both are supported.

## Working with AppArmor

For information on AppArmor, see [Working with AppArmor](https://docs.percona.com/percona-server/9.7/apparmor.html).
