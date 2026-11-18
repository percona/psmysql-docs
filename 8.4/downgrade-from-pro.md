> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Downgrade from Percona Server for MySQL Pro

If you want to downgrade from Percona Server for MySQL Pro to the same version of Percona Server for MySQL, do the following:

**On Debian and Ubuntu**

1. Set up the Percona Server for MySQL 8.4 repository

   ```
   sudo percona-release setup ps84
   ```

1. Stop the `mysql` server.

   ```
   sudo systemctl stop mysql
   ```

1. Install the server package

   ```
   sudo apt install percona-server-server
   ```

   Install other required packages. [Check files in the DEB package built for Percona Server for MySQL 8.4](https://docs.percona.com/percona-server/8.4/apt-files.html).

1. Start the `mysql` server

   ```
   sudo systemctl start mysql
   ```

Note

On Debian 12, if you want to remove the Percona Server for MySQL after the downgrade, you must stop the server manually. This behavior will be fixed in future releases.

```
sudo systemctl stop mysql
```

**On RHEL and derivatives**

1. Set up the Percona Server for MySQL 8.4 repository

   ```
   sudo percona-release setup ps84
   ```

1. Stop the `mysql` server.

   ```
   sudo systemctl stop mysql
   ```

1. Install the server package

   ```
   sudo yum --allowerasing install percona-server-server
   ```

   Install other required packages. [Check files in the RPM package built for Percona Server for MySQL 8.4](https://docs.percona.com/percona-server/8.4/yum-files.html).

1. Start the `mysql` server

   ```
   sudo systemctl start mysql
   ```
