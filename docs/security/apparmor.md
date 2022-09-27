# Working with AppArmor

The operating system has a Discretionary Access Controls (DAC) system. AppArmor supplements the DAC with a Mandatory Access Control (MAC) system. AppArmor is the default security module for Ubuntu or Debian systems and uses profiles to define how programs access resources.

AppArmor is path-based and restricts processes by using profiles. Each profile contains a set of policy rules. Some applications may install their profile along with the application. If an installation does not also install a profile, then that application is not part of the AppArmor subsystem. You can also create profiles since they are simple text files stored in the `/etc/apparmor.d` directory.

A profile is in one of the following modes:

* Enforce - the default setting, applications are prevented from taking actions restricted by the profile rules.

* Complain - applications are allowed to take restricted actions, and the actions are logged.

* Disabled - Applications are allowed to take restricted actions, and the actions are not logged.

You can mix enforce profiles and complain profiles in your server.

## Install the Utilities used to control AppArmor

Install the `apparmor-utils` package to work with profiles. Use these utilities to create, update, enforce, switch to complain mode, and disable profiles, as needed:

```shell
$ sudo apt install apparmor-utils
```

The output could be the following:

```text
Reading package lists... Done
Building dependency tree
...
The following additional packages will be installed:
    python3-apparmor python3-libapparmor
...
```

## Check the Current Status

As root or using `sudo`, you can check the AppArmor status:

```shell
$ sudo aa-status
```

The output could be the following:

```text
apparmor module is loaded.
34 profiles are loaded.
32 profiles in enforce mode.
...
    /usr/sbin/mysqld
...
2 profiles in complain mode.
...
3 profiles have profiles defined.
...
0 processes are in complain mode.
0 processes are unconfined but have a profile defined.
```

## Switch a Profile to Complain mode

Switch a profile to complain mode when the program is in your path with this command:

```text
$ sudo aa-complain <program>
```

If needed, specify the program’s path in the command:

```shell
$ sudo aa-complain /sbin/<program>
```

If the profile is not stored in `/etc/apparmor.d/`, use the following command:

```shell
$ sudo aa-complain /path/to/profiles/<program>
```

## Switch a Profile to Enforce mode

Switch a profile to the enforce mode when the program is in your path with this command:

```text
$ sudo aa-enforce <program>
```

If needed, specify the program’s path in the command:

```shell
$ sudo aa-enforce /sbin/<program>
```

If the profile is not stored in `/etc/apparmor.d/`, use the following command:

```text
$ sudo aa-enforce /path/to/profile
```

## Disable one profile

You can disable a profile but it is recommended to Switch a Profile to Complain mode.

Use either of the following methods to disable a profile:

```shell
$ sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
$ sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld
```

or

```shell
$ aa-disable /etc/apparmor.d/usr.sbin.mysqld
```

## Reload all profiles

Run either of the following commands to reload all profiles:

```shell
$ sudo service apparmor reload
```

or

```shell
$ sudo systemctl reload apparmor.service
```

## Reload one profile

To reload one profile, run the following:

```shell
$ sudo apparmor_parser -r /etc/apparmor.d/<profile>
```

For some changes to take effect, you may need to restart the program.

## Disable AppArmor

AppArmor provides security and disabling the system is not recommened. If AppArmor must be disabled, run the following commands:


1. Check the status.

    ```shell
    $ sudo apparmor_status
    ```

2. Stop and disable AppArmor.

    ```shell
    $ sudo systemctl stop apparmor
    $ sudo systemctl disable apparmor
    ```

## Add the mysqld profile

Add the mysqld profile with the following procedure:

1. Download the current version of the AppArmor:

    ```shell
    $ wget https://raw.githubusercontent.com/mysql/mysql-server/8.0/packaging/deb-in/extra/apparmor-profile
    ```

   The output could be the following:

   ```text
   ...
   Saving to 'apparamor-profile`
   ...
   ```

2. Move the file to /etc/apparmor.d/usr.sbin.mysqld

    ```shell
    $ sudo mv apparmor-profile /etc/apparmor.d/usr.sbin.mysqld
    ```

3. Create an empty file for editing:

    ```shell
    $ sudo touch /etc/apparmor.d/local/usr.sbin.mysqld
    ```

4. Load the profile:

    ```shell
    $ sudo apparmor_parser -r -T -W /etc/apparmor.d/usr.sbin.mysqld
    ```

5. Restart *Percona Server for MySQL*:

    ```shell
    $ sudo systemctl restart mysql
    ```

6. Verify the profile status:
 
    ```shell
    $ sudo aa-status
    ```

    The output could be the following:

    ```text
    ...
    processes are in enforce mode
    ...
    /usr/sbin/mysqld (100840)
    ...
    ```

## Edit the mysqld profile

Only edit `/etc/apparmor.d/local/usr.sbin.mysql`. We recommend that you Switch a Profile to Complain mode before editing the file. Edit the file in any text editor. When your work is done, Reload one profile and Switch a Profile to Enforce mode.

## Configure a custom data directory location

You can change the data directory to a non-default location, like /var/lib/mysqlcustom. You should enable audit mode, to capture all of the actions, and edit the profile to allow access for the custom location.

```shell
$ cat /etc/mysql/mysql.conf.d/mysqld.cnf
```

The output could be the following:

```text
#
# The Percona Server 8.0 configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
pid-file    = /var/run/mysqld/mysqld.pid
socket        = /var/run/mysqld/mysqld.sock
*datadir    = /var/lib/mysqlcustom*
log-error    = /var/log/mysql/error.log
```

Enable audit mode for mysqld. In this mode, the security policy is enforced and all access is logged.

```shell
$ aa-audit mysqld
```

Restart Percona Server for MySQL.

```shell
$ sudo systemctl mysql restart
```

The restart fails because AppArmor has blocked access to the custom data directory location. To diagnose the issue, check the logs for the following:

* ALLOWED - A log event when the profile is in complain mode and the action violates a policy.

* DENIED - A log event when the profile is in enforce mode and the action is blocked.

For example, the following log entries show `DENIED`:

```text
...
Dec 07 12:17:08 ubuntu-s-4vcpu-8gb-nyc1-01-aa-ps audit[16013]: AVC apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/var/lib/mysqlcustom/binlog.index" pid=16013 comm="mysqld" requested_mask="c" denied_mask="c" fsuid=111 ouid=111
Dec 07 12:17:08 ubuntu-s-4vcpu-8gb-nyc1-01-aa-ps kernel: audit: type=1400 audit(1607343428.022:36): apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/var/lib/mysqlcustom/mysqld_tmp_file_case_insensitive_test.lower-test" pid=16013 comm="mysqld" requested_mask="c" denied_mask="c" fsuid=111 ouid=111
...
```

Open `/etc/apparmor.d/local/usr.sbin.mysqld` in a text editor and edit the following entries in the `Allow data dir access` section.

```text
# Allow data dir access
/var/lib/mysqlcustom/ r,
/var/lib/mysqlcustom/** rwk,
```

In `etc/apparmor.d/local/usr.sbin.mysqld`, comment out, using the # symbol, the current entries in the Allow data dir access section. This step is optional. If you skip this step, mysqld continues to access the default data directory location.

!!! note

    Edit the local version of the file instead of the main profile. Separating the changes makes maintenance easier.

Reload the profile:

```shell
$apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

Restart mysql:

```shell
$ systemctl restart mysqld
```

## Set up a custom log location

To move your logs to a custom location, you must edit the my.cnf configuration file and then edit the local profile to allow access:

```shell
cat /etc/mysql/mysql.conf.d/mysqld.cnf
```

The output could be the following:

```text
#
# The Percona Server 8.0 configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
pid-file    = /var/run/mysqld/mysqld.pid
socket        = /var/run/mysqld/mysqld.sock
datadir    = /var/lib/mysql
log-error    = /*custom-log-dir*/mysql/error.log
```

Verify the custom directory exists.

```shell
$ ls -la /custom-log-dir/
```

The output could be the following:

```text
total 12
drwxrwxrwx  3 root root 4096 Dec  7 13:09 .
drwxr-xr-x 24 root root 4096 Dec  7 13:07 ..
drwxrwxrwx  2 root root 4096 Dec  7 13:09 mysql
```

Restart Percona Server.

```shell
$ service mysql start
```

The output could be the following:

```text
Job for mysql.service failed because the control process exited with error code.
See "systemctl status mysql.service" and "journalctl -xe" for details.

```shell
$ journalctl -xe
```

The output could be the following:

```text
...
AVC apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/custom-log-dir/mysql/error.log"
...
```

The access has been denied by AppArmor. Edit the local profile in the `Allow log file access` section to allow access to the custom log location.

```shell
$ cat /etc/apparmor.d/local/usr.sbin.mysqld
```

The output could be the following:

```text
 # Site-specific additions and overrides for usr.sbin.mysqld..
 # For more details, please see /etc/apparmor.d/local/README.

 # Allow log file access
/custom-log-dir/mysql/ r,
/custom-log-dir/mysql/** rw,
```

Reload the profile:

```shell
$apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

Restart Percona Server:

```shell
$ systemctl restart mysqld
```

## Set `secure_file_priv` directory location

By default, secure_file_priv points to the following location:

```sql
mysql> mysqlshow variables like 'secure_file_priv';
```

The output could be the following:

```text
+------------------+-----------------------+
| Variable_name    | Value                 |
+------------------+-----------------------+
| secure_file_priv | /var/lib/mysql-files/ |
+------------------+-----------------------+
```

To allow access to another location, in a text editor, open the local profile. Review the settings in the `Allow data dir access` section:

```text
 # Allow data dir access
/var/lib/mysql/ r,
/var/lib/mysql/** rwk,
```

Edit the local profile in a text editor to allow access to the custom location.

```shell
$ cat /etc/apparmor.d/local/usr.sbin.mysqld
```

The output could be the following:

```text
# Site-specific additions and overrides for usr.sbin.mysqld..
# For more details, please see /etc/apparmor.d/local/README.

# Allow data dir access
/var/lib/mysqlcustom/ r,
/var/lib/mysqlcustom/** rwk,
```

Reload the profile:

```shell
$apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

Restart Percona Server for MySQL:

```shell
$ systemctl restart mysqld
```
