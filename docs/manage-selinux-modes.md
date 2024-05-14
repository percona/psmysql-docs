# Manage SELinux modes

SELinux, or Security-Enhanced Linux, is a security module that provides access control policies. It enhances the system's security by allowing administrators to define rules restricting how applications and users can access resources. SELinux operates in three different modes: Disabled, Permissive, and Enforcing.

## Disabled Mode

In Disabled mode, SELinux is completely turned off. The system does not enforce any SELinux policies, and there is no SELinux security checking. Applications and processes run without any restrictions imposed by SELinux. This mode is typically used for troubleshooting or when SELinux is not needed.

To set SELinux to Disabled mode, you need to edit the SELinux configuration file. Open the file `/etc/selinux/config` with a text editor and set the `SELINUX` parameter to `disabled`:

```{.bash data-prompt="$"}
$ SELINUX=disabled
```

Save the file and reboot the system for the change to take effect.

## Permissive Mode

In Permissive mode, SELinux policies are not enforced, but violations are logged. This mode is useful for troubleshooting and for understanding what SELinux would block without actually blocking anything. Applications and processes run as if SELinux is not enforcing policies, but administrators can see which actions would have been denied if SELinux were enforcing.

To set SELinux to Permissive mode, you can edit the SELinux configuration file `/etc/selinux/config` and set the `SELINUX` parameter to `permissive`:

```{.bash data-prompt="$"}
$ SELINUX=permissive
```

Save the file and reboot the system. Alternatively, you can change to Permissive mode temporarily without rebooting by running the following command as root:

```{.bash data-prompt="$"}
$ setenforce 0
```

## Enforcing Mode

In Enforcing mode, SELinux enforces all policies and denies access based on the rules defined in the policy. This mode is the default and most secure mode. SELinux actively restricts actions of applications and processes based on the policies in place. Any violation of the rules results in access being denied and logged.

To set SELinux to Enforcing mode, edit the SELinux configuration file `/etc/selinux/config` and set the `SELINUX` parameter to `enforcing`:

```{.bash data-prompt="$"}
$ SELINUX=enforcing
```

Save the file and reboot the system. To change to Enforcing mode temporarily without rebooting, you can use the following command as root:

```{.bash data-prompt="$"}
$ setenforce 1
```

## How to check the SELinux mode

 You can check which mode SELinux is currently running in by using a few terminal commands.

### Use the `sestatus` command

To check the current SELinux mode, you can use the `sestatus` command. This command shows the status of SELinux, including the mode it is operating in. Type the following command and press Enter:

```{.bash data-prompt="$"}
$ sestatus
```

??? example "Expected output"

    ```{.text .no-copy}
    
    SELinux status:                 enabled
    SELinuxfs mount:                /sys/fs/selinux
    SELinux root directory:         /etc/selinux
    Loaded policy name:             targeted
    Current mode:                   enforcing
    Mode from config file:          enforcing
    Policy MLS status:              enabled
    Policy deny_unknown status:     allowed
    Max kernel policy version:      31
    ```


| Result                 | Description                                                                                                                                                       |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Current mode**       | This line shows the mode SELinux is currently operating in. It can be "enforcing", "permissive", or "disabled".                                                     |
| **Enforcing**          | SELinux is actively enforcing its policies and blocking any actions that are not allowed.                                                                           |
| **Permissive**         | SELinux is not blocking actions, but it logs any actions that would be blocked in enforcing mode.                                                                   |
| **Disabled**           | SELinux is completely turned off, and no policies are enforced or logged.                                                                                           |
| **Mode from config file** | This line shows the mode that SELinux is configured to use at boot time, which might be different from the current mode if changes were made without rebooting. |

### Use the `getenforce` command

Another command to check the current SELinux mode is `getenforce`. Type the following command and press Enter:

```{.bash data-prompt="$"}
$ getenforce
```

??? example "Expected output"

    ```{.text .no-copy}
    Enforcing
    ```


### Check the configuration file

You can also check the SELinux configuration file to see what mode SELinux is set to use when the system boots. Open the configuration file located at `/etc/selinux/config` using a text editor. For example, you can use `cat` to view the file contents:

```{.bash data-prompt="$"}
$ cat /etc/selinux/config
```

??? example "Expected output"

    ```{.text .no-copy}
    SELINUX=enforcing
    ```

## How to switch the SELinux mode

Switching the SELinux mode changes how the Security-Enhanced Linux (SELinux) system controls access and enforces policies on your system.

### Switch SELinux mode temporarily

To switch SELinux mode temporarily, use the `setenforce` command. This change will last until the system is rebooted.


```{.bash data-prompt="$"}
$ sudo setenforce 1
```

To check if the mode has changed, run `sestatus`.

## Switch SELinux Mode permanently

To make the change permanent, you need to edit the SELinux configuration file. This file is usually located at `/etc/selinux/config`.

1. Open the configuration file with a text editor. For example, using `nano`:

    ```{.bash data-prompt="$"}
    $ sudo nano /etc/selinux/config
    ```

2. Look for the line that starts with `SELINUX=`. It will be followed by the current mode: `enforcing`, `permissive`, or `disabled`.

3. Change the value to the desired mode.

4. Save the file and exit the text editor.

To apply the permanent change, reboot the system. After the system restarts, check the SELinux mode with `sestatus` to ensure the change took effect.


## Changing SELinux mode for a service

SELinux (Security-Enhanced Linux) controls access and permissions for processes and users on a Linux system. SELinux has different modes: Enforcing, Permissive, and Disabled. When you change the SELinux mode for a specific service, you can control how strictly SELinux policies apply to that service. This can be useful when you need to test or troubleshoot services without disabling SELinux entirely.

### Step 1: Identify the Service

First, identify the service for which you want to change the SELinux mode. For example, let's say you want to change the SELinux mode for the Apache web server (`httpd`).

### Step 2: Check current SELinux context

Check the current SELinux context of the service to understand its current mode and permissions. You can use the `ps` command with `-Z` option to view the SELinux context of a running process.

```{.bash data-prompt="$"}
$ ps -eZ | grep httpd
```

This command displays the SELinux context for all `httpd` processes.

### Step 3: Create a Custom SELinux Policy Module

To change the SELinux mode for a specific service, you create a custom SELinux policy module. This module will move the service to a permissive domain while keeping the rest of the system in enforcing mode.

Create a policy file, for example, `httpd_permissive.te`:

```{.bash data-prompt="$"}
$ nano httpd_permissive.te
```

Add the following content to the file:

```text
policy_module(httpd_permissive, 1.0)

gen_permissive(httpd_t)
```

This policy module tells SELinux to make the `httpd_t` domain permissive.

### Step 4: Compile and Install the Policy Module

Compile the policy module using the `checkmodule` and `semodule_package` commands:

```{.bash data-prompt="$"}
$ checkmodule -M -m -o httpd_permissive.mod httpd_permissive.te
$ semodule_package -o httpd_permissive.pp -m httpd_permissive.mod
```

Install the compiled policy module using the `semodule` command:

```{.bash data-prompt="$"}
$ semodule -i httpd_permissive.pp
```

This installs the custom SELinux policy module, making the `httpd` service run in permissive mode.

### Step 5: Verify the Changes

Restart the service to apply the changes:

```{.bash data-prompt="$"}
$ systemctl restart httpd
```

Check the SELinux context again to ensure the `httpd` service is running in the permissive domain:

```{.bash data-prompt="$"}
$ ps -eZ | grep httpd
```

You should see the `httpd` processes with a permissive context.

### Step 6: Monitor Logs and Adjust Policies

While the service is in a permissive domain, SELinux logs any policy violations without enforcing them. Monitor the logs to identify and resolve issues. Use `audit2allow` to generate new policies if needed:

```{.bash data-prompt="$"}
$ ausearch -m avc -c httpd | audit2allow -M httpd_custom
$ semodule -i httpd_custom.pp
```

This command sequence helps you create and install new SELinux policies based on logged violations, refining your SELinux configuration.