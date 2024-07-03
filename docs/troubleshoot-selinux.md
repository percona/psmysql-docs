# Troubleshoot SELinux issues

## Relabel the Entire File System

Relabeling the entire file system is updating SELinux contexts for all files and directories. This operation ensures that SELinux can enforce its policies correctly.

When relabeling the entire file system for SELinux, you should use `fixfiles` when you want to initiate the relabeling process manually. This command is useful when you need to perform the relabeling operation immediately or if you want to specify additional options, such as forcing the operation with the `-f` flag.

On the other hand, `.autorelabel` is used when you want the relabeling process to occur automatically during system boot. This method is convenient when scheduling the relabeling task without manual intervention. The `.autorelabel` in the root directory triggers the relabeling process during the boot sequence, ensuring that all files and directories are relabeled according to the SELinux policy.

### Manually relabeling

This command relabels the entire file system without requiring a system reboot.

   ```{.bash data-prompt="$"}
   $ fixfiles -f relabel
   ```
The command `fixfiles -f relabel` is a directive used within the context of SELinux, a security feature in Linux systems. This specific command instructs the system to forcefully reapply SELinux labels, also known as contexts, to files and directories.

Here's a breakdown of what each part of the command does:

| Option   | Description                                                                                                     |
|----------|-----------------------------------------------------------------------------------------------------------------|
| fixfiles | This is the name of the command being executed. It's a tool provided by SELinux specifically designed to fix file contexts. |
| -f       | This is an option passed to the `fixfiles` command. In this context, the `-f` option stands for "force". It tells the `fixfiles` command to perform the relabeling operation forcefully, regardless of the current state or any potential errors. |
| relabel  | This is an argument passed to the `fixfiles` command. It specifies the action that `fixfiles` should take: relabel the files and directories on the system. |

When you run `fixfiles -f relabel`, SELinux goes through all files and directories on the system and applies the appropriate SELinux labels to each one. These labels are crucial for SELinux to enforce its security policies effectively. They determine how processes and users can interact with the files and directories, ensuring that only authorized actions are allowed.

This command is typically used in scenarios where there may have been changes to the file system that require SELinux labels to be updated. For example, if files or directories have been moved or copied from one location to another or if SELinux policies have been modified, running `fixfiles -f relabel` ensures that the SELinux labels remain consistent with the system's current configuration.

It's important to note that running `fixfiles -f relabel` can be a resource-intensive operation and may take some time to complete, especially on systems with many files and directories. Additionally, since it forcefully relabels all files and directories, use it cautiously and preferably during maintenance windows to minimize potential disruptions to system operations.

### Automatic relabeling

Creating the `.autorelabel` file initiates a relabeling process that often requires a reboot to apply the changes effectively. During this reboot, SELinux relabels all files based on their defined policies.

   ```{.bash data-prompt="$"}
   $ touch /.autorelabel
   ```

This command creates a file named `.autorelabel` in the root directory of the Linux filesystem. The "touch" command creates a new file.

The purpose of the `.autorelabel` file is to trigger an automatic relabeling of the entire filesystem when the system boots up. Relabeling involves assigning security labels to files and directories based on SELinux policies. This process ensures that all files and directories have the correct security context, which is essential for SELinux to enforce its security policies effectively.

Creating this file tells the system to perform a relabeling operation during the next boot. This operation can be useful in situations where SELinux policies or file contexts have been modified, and we want to ensure that all files are correctly labeled according to the updated policies.

It's important to note that the `.autorelabel` file contains no data or configuration. The file acts as a trigger for the relabeling process. Once the relabeling is complete, the system automatically removes the `.autorelabel` file.

## Set Custom Data Directory

Setting a custom data directory for the server involves configuring SELinux contexts to allow the server to access the new directory properly.

It would be best to use `semanage` when you defining or modifying SELinux policy rules related to a custom data directory. This command allows you to manage SELinux policy modules, including adding, deleting, and modifying SELinux policy rules for specific file contexts or directories.

It would be best to use `restorecon` when you restore the default SELinux context for files and directories, including those in a custom data directory. `restorecon` resets the SELinux context of specified files or directories to match the default context defined in the SELinux policy. It's typically used after file or directory modifications to ensure they have the correct SELinux context.

### Use semanage

The following command configures the SELinux context for a custom data directory in the server.

   ```{.bash data-prompt="$"}
   $ semanage fcontext -a -t mysqld_db_t "/path/to/custom/data(/.*)?"
   ```

Each part of the command is as follows:

| Option              | Description                                                                                                   |
|---------------------|---------------------------------------------------------------------------------------------------------------|
| `semanage`          | Command-line tool used to manage SELinux policy settings.                                                     |
| `fcontext`          | Sub-command of `semanage` specifically used to manage file contexts, which define how SELinux labels files and directories. |
| `-a`                | Stands for "add" and indicates the intention to add a new file context configuration.                        |
| `-t mysqld_db_t`    | Specifies the type of context to assign to the specified path. In this case, `mysqld_db_t` is the SELinux type context for The server database files. |
| `"/path/to/custom/data(/.*)?"` | Path to the custom data directory in the Server setup. The `(/.*)?` part is a regular expression pattern matching any files or subdirectories within the specified directory. |

This command tells SELinux to label all files and subdirectories within the `/path/to/custom/data` directory with the SELinux type context `mysqld_db_t`. This operation ensures that SELinux treats these files and directories as part of the server's database, allowing the server to access them according to its SELinux policy.
   
### Use restorecon

```{.bash data-prompt="$"}
$ restorecon -Rv /path/to/custom/data
```

The `restorecon -Rv /path/to/custom/data` command restores the SELinux context for a specific directory and subdirectory. Here's what each part of the command does:

- `restorecon`: This is the main command used to restore the SELinux context of files and directories.
- `-R`: This option stands for "recursive" and indicates that the command should operate recursively on all files and subdirectories within the specified directory.
- `-v`: This option stands for "verbose" and instructs the command to display detailed information about the actions it performs, providing feedback on which files and directories had their SELinux context restored.

The `/path/to/custom/data` part of the command should be replaced with the actual path to the directory for which you want to restore the SELinux context.

Typically, `restorecon` does not require a system reboot. It simply restores the SELinux context for the specified directory and its contents. However, if you're experiencing issues with SELinux after running the command, a system reboot may be necessary to ensure all changes take effect.

## Setting Custom Log Location

When setting a custom log location for the server, SELinux permissions may need adjustment to allow the server to write to the new directory.

This command associates the `var_log_t` type with the custom log directory and contents.

```{.bash data-prompt="$"}
$ semanage fcontext -a -t var_log_t "/path/to/custom/logs(/.*)?"
```

This command restores SELinux contexts recursively for the custom log directory, ensuring proper permissions for the server to write logs.

```{.bash data-prompt="$"}
$ restorecon -Rv /path/to/custom/logs
```

## Setting secure_file_priv Directory

When configuring the server's `secure_file_priv` directory, you must update the SELinux tags to allow the server to access this directory.

This command associates the `mysqld_db_t` type with the `secure_file_priv` directory and its contents.

```{.bash data-prompt="$"}
$ semanage fcontext -a -t mysqld_db_t "/path/to/secure_file_priv(/.*)?"
```

This command restores SELinux contexts recursively for the `secure_file_priv` directory, ensuring proper permissions for the server file operations.

```{.bash data-prompt="$"}
$ restorecon -Rv /path/to/secure_file_priv
```

   


