# Configure AppArmor

## Edit profile

Only edit `/etc/apparmor.d/local/usr.sbin.mysql`. 

You should [switch the profile] to `Complain` mode before editing the file. Edit the file in any text editor. When finished, reload the profile and switch it to `Enforce` mode.

## Configure data directory location

You can change the data directory to a non-default location, like /var/lib/mysqlcustom. You should enable audit mode to capture all actions and edit the profile to allow access to the custom location.

```{.bash data-prompt="$"}
$ cat /etc/mysql/mysql.conf.d/mysqld.cnf
```

??? example "Expected output"

    ```{.text .no-copy}
    
    The Percona Server {{vers}} configuration file.
    
    For explanations see
    https://dev.mysql.com/doc/mysql/en/server-system-variables.html

    [mysqld]
    pid-file    = /var/run/mysqld/mysqld.pid
    socket        = /var/run/mysqld/mysqld.sock
    *datadir    = /var/lib/mysqlcustom*
    log-error    = /var/log/mysql/error.log
    ```

Enable audit mode for mysqld. In this mode, the security policy is enforced and all access is logged.

```{.bash data-prompt="$"}
$ aa-audit mysqld
```

Restart Percona Server for MySQL.

```{.bash data-prompt="$"}
$ sudo systemctl mysql restart
```

The restart fails because AppArmor has blocked access to the custom data directory location. To diagnose the issue, check the logs for the following:

* ALLOWED - A log event when the profile is in complain mode and the action violates a policy.

* DENIED - A log event when the profile is in enforce mode and the action is blocked.

For example, the following log entries show `DENIED`:

??? example "Expected output"

    ```{.text .no-copy}
    ...
    Dec 07 12:17:08 ubuntu-s-4vcpu-8gb-nyc1-01-aa-ps audit[16013]: AVC apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/var/lib/mysqlcustom/binlog.index" pid=16013 comm="mysqld" requested_mask="c" denied_mask="c" fsuid=111 ouid=111
    Dec 07 12:17:08 ubuntu-s-4vcpu-8gb-nyc1-01-aa-ps kernel: audit: type=1400 audit(1607343428.022:36): apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/var/lib/mysqlcustom/mysqld_tmp_file_case_insensitive_test.lower-test" pid=16013 comm="mysqld" requested_mask="c" denied_mask="c" fsuid=111 ouid=111
    ...
    ```

Open `/etc/apparmor.d/local/usr.sbin.mysqld` in a text editor and edit the following entries in the `Allow data dir access` section.

```text
Allow data dir access
/var/lib/mysqlcustom/ r,
/var/lib/mysqlcustom/** rwk,
```

In `etc/apparmor.d/local/usr.sbin.mysqld`, comment out, using the # symbol, the current entries in the Allow data dir access section. This step is optional. If you skip this step, mysqld continues to access the default data directory location.

!!! note

    Edit the local version of the file instead of the main profile. Separating the changes makes maintenance easier.

Reload the profile:

```{.bash data-prompt="$"}
$ apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

Restart mysql:

```{.bash data-prompt="$"}
$ systemctl restart mysqld
```

## Set up a custom log location

To move your logs to a custom location, you must edit the my.cnf configuration file and then edit the local profile to allow access:

```shell
cat /etc/mysql/mysql.conf.d/mysqld.cnf
```

??? example "Expected output"

    ```{.text .no-copy}
    
    The Percona Server {{vers}} configuration file.
    
    For explanations see
    https://dev.mysql.com/doc/mysql/en/server-system-variables.html

    [mysqld]
    pid-file    = /var/run/mysqld/mysqld.pid
    socket        = /var/run/mysqld/mysqld.sock
    datadir    = /var/lib/mysql
    log-error    = /*custom-log-dir*/mysql/error.log
    ```

Verify the custom directory exists.

```{.bash data-prompt="$"}
$ ls -la /custom-log-dir/
```

??? example "Expected output"

    ```{.text .no-copy}
    total 12
    drwxrwxrwx  3 root root 4096 Dec  7 13:09 .
    drwxr-xr-x 24 root root 4096 Dec  7 13:07 ..
    drwxrwxrwx  2 root root 4096 Dec  7 13:09 mysql
    ```

Restart Percona Server.

```{.bash data-prompt="$"}
$ service mysql start
```

??? example "Expected output"

    ```{.text .no-copy}
    Job for mysql.service failed because the control process exited with error code.
    See "systemctl status mysql.service" and "journalctl -xe" for details.
    ```

```{.bash data-prompt="$"}
$ journalctl -xe
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    AVC apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/custom-log-dir/mysql/error.log"
    ...
    ```

The access has been denied by AppArmor. Edit the local profile in the `Allow log file access` section to allow access to the custom log location.

```{.bash data-prompt="$"}
$ cat /etc/apparmor.d/local/usr.sbin.mysqld
```

??? example "Expected output"

    ```{.text .no-copy}
     Site-specific additions and overrides for usr.sbin.mysqld..
     For more details, please see /etc/apparmor.d/local/README.

     Allow log file access
     /custom-log-dir/mysql/ r,
     /custom-log-dir/mysql/** rw,
    ```

Reload the profile:

```{.bash data-prompt="$"}
$ apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

Restart Percona Server:

```{.bash data-prompt="$"}
$ systemctl restart mysqld
```

## Set `secure_file_priv` directory location

By default, secure_file_priv points to the following location:

```{.bash data-prompt="mysql>"}
mysql> mysqlshow variables like 'secure_file_priv';
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------+-----------------------+
    | Variable_name    | Value                 |
    +------------------+-----------------------+
    | secure_file_priv | /var/lib/mysql-files/ |
    +------------------+-----------------------+
    ```

To allow access to another location, in a text editor, open the local profile. Review the settings in the `Allow data dir access` section:

```text
Allow data dir access
/var/lib/mysql/ r,
/var/lib/mysql/** rwk,
```

Edit the local profile in a text editor to allow access to the custom location.

```{.bash data-prompt="$"}
$ cat /etc/apparmor.d/local/usr.sbin.mysqld
```

??? example "Expected output"

    ```{.text .no-copy}
    Site-specific additions and overrides for usr.sbin.mysqld..
    For more details, please see /etc/apparmor.d/local/README.

    Allow data dir access
    /var/lib/mysqlcustom/ r,
    /var/lib/mysqlcustom/** rwk,
    ```

Reload the profile:

```{.bash data-prompt="$"}
$ apparmor_parser -r -T /etc/apparmor.d/usr.sbin.mysqld
```

Restart Percona Server for MySQL:

```{.bash data-prompt="$"}
$ systemctl restart mysqld
```

## AppArmor links:

[AppArmor](apparmor.md)<br>
[AppArmor Profiles](apparmor-profiles.md)<br>
[Manage AppArmor Profiles](manage-apparmor-profiles.md)<br>
[Disable AppArmor](disable-apparmor.md)<br>
[Troubleshoot AppArmor](troubleshoot-apparmor.md)

