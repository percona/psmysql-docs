# Managing AppArmor profiles

## Understanding AppArmor Risks in MySQL Development

While AppArmor profiles help secure your MySQL server, misconfiguring them can lead to unexpected behavior and potential security vulnerabilities. Here's why careful review and testing are crucial when making changes:

## Potential risks of misconfigured AppArmor profiles

| Misconfiguration | Description |
|---|---|
| **Overly restrictive profiles** |  These profiles might prevent MySQL from accessing necessary files or resources, hindering its functionality and causing errors. Imagine a profile accidentally blocking MySQL from writing to its log files, rendering them useless for troubleshooting. |
| **Underly permissive profiles** |  Profiles with insufficient restrictions could allow unauthorized access to MySQL's files or functionalities. This creates a security risk, as an attacker exploiting a vulnerability might leverage a permissive profile to gain more control over the server.  |
| **Incorrect profile assignment** |   Assigning the wrong profile to a process can lead to either of the issues mentioned above.  For instance, accidentally assigning a profile meant for a different service to MySQL could have unintended consequences. |

## Importance of careful review and testing

By carefully reviewing and testing your AppArmor profile changes, you can minimize the risks associated with misconfigurations and ensure a secure and functional MySQL environment.

* Review your changes thoroughly: Double-check your AppArmor profile modifications to ensure they grant MySQL the necessary permissions while maintaining security. 

* Test your changes in a safe environment: Before deploying changes to a production server, test them in a staging environment that mimics your production setup. This test allows you to identify and fix any issues caused by the AppArmor profile adjustments without impacting your live MySQL instance.

## Install the utilities used to control AppArmor

Install the `apparmor-utils` package to work with profiles. Use these utilities to create, update, enforce, switch to complain mode, and disable profiles, as needed:

```{.bash data-prompt="$"}
$ sudo apt install apparmor-utils
```

??? example "Expected output"

    ```{.text .no-copy}
    Reading package lists... Done
    Building dependency tree
    ...
    The following additional packages will be installed:
        python3-apparmor python3-libapparmor
    ...
    ```

## Add the mysqld profile

Add the mysqld profile with the following procedure:
{.power-number}

1. Download the current version of the AppArmor:

    ```{.bash data-prompt="$"}
    $ wget https://raw.githubusercontent.com/percona/percona-server/release-{{release}}/build-ps/debian/percona-server-server.install
    ```

    ??? example "Expected output"

    ```{.text .no-copy}
    ...
    Saving to 'apparamor-profile`
    ...
    ```

2. Move the file to /etc/apparmor.d/usr.sbin.mysqld

    ```{.bash data-prompt="$"}
    $ sudo mv apparmor-profile /etc/apparmor.d/usr.sbin.mysqld
    ```

3. Create an empty file for editing:

    ```{.bash data-prompt="$"}
    $ sudo touch /etc/apparmor.d/local/usr.sbin.mysqld
    ```

4. Load the profile:

    ```{.bash data-prompt="$"}
    $ sudo apparmor_parser -r -T -W /etc/apparmor.d/usr.sbin.mysqld
    ```

5. Restart *Percona Server for MySQL*:

    ```{.bash data-prompt="$"}
    $ sudo systemctl restart mysql
    ```

6. Verify the profile status:
 
    ```{.bash data-prompt="$"}
    $ sudo aa-status
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        ...
        processes are in enforce mode
        ...
        /usr/sbin/mysqld (100840)
        ...
        ```

## Check the current status

As root or using `sudo`, you can check the AppArmor status:

```{.bash data-prompt="$"}
$ sudo aa-status
```

??? example "Expected output"

    ```{.text .no-copy}
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

## Switch a profile to complain mode

Switch a profile to complain mode when the program is in your path with this command:

```{.bash data-prompt="$"}
$ sudo aa-complain <program>
```

If needed, specify the program’s path in the command:

```{.bash data-prompt="$"}
$ sudo aa-complain /sbin/<program>
```

If the profile is not stored in `/etc/apparmor.d/`, use the following command:

```{.bash data-prompt="$"}
$ sudo aa-complain /path/to/profiles/<program>
```

## Switch a profile to enforce mode

Switch a profile to the enforce mode when the program is in your path with this command:

```{.bash data-prompt="$"}
$ sudo aa-enforce <program>
```

If needed, specify the program’s path in the command:

```{.bash data-prompt="$"}
$ sudo aa-enforce /sbin/<program>
```

If the profile is not stored in `/etc/apparmor.d/`, use the following command:

```{.bash data-prompt="$"}
$ sudo aa-enforce /path/to/profile
```

## Disable one profile

You can disable a profile but it is recommended to Switch a Profile to Complain mode.

Use either of the following methods to disable a profile:

```{.bash data-prompt="$"}
$ sudo ln -s /etc/apparmor.d/usr.sbin.mysqld /etc/apparmor.d/disable/
$ sudo apparmor_parser -R /etc/apparmor.d/usr.sbin.mysqld
```

or

```{.bash data-prompt="$"}
$ aa-disable /etc/apparmor.d/usr.sbin.mysqld
```

## Reload all profiles

Run either of the following commands to reload all profiles:

```{.bash data-prompt="$"}
$ sudo service apparmor reload
```

or

```{.bash data-prompt="$"}
$ sudo systemctl reload apparmor.service
```

## Reload one profile

To reload one profile, run the following:
You may need to restart the program for some changes to take effect.

## Useful links:

[AppArmor](apparmor.md)<br>
[AppArmor Profiles](apparmor-profiles.md)<br>
[Disable AppArmor](disable-apparmor.md)<br>
[Configure AppArmor](configure-apparmor.md)<br>
[Troubleshoot AppArmor](troubleshoot-apparmor.md)