# SELinux contexts and labels

Viewing SELinux Contexts
Example of viewing SELinux context for a process using ps command
Listing SELinux Types or Domains
Explanation of SELinux type security property
Example of listing SELinux types associated with MySQL directories and files

SELinux context is like a label that tells the system how to handle files, processes, and other resources. For example, it determines which processes can access certain files and what actions they can perform on them. Understanding SELinux context helps you know how your applications interact with the system and ensures that they have the necessary permissions to function correctly. It's like giving each item on your computer a tag that says what it is and what it's allowed to do. So when your application tries to access a file, SELinux checks its context to see if it's allowed. If the context matches what's expected, the action is allowed; if not, it's denied. So knowing the SELinux context is essential for managing security and troubleshooting issues on your system.

### Viewing SELinux context for a process using ps command

To view the SELinux context for a process using the `ps` command, you can add the `-Z` option to display the context information. Here's how you can do it:

```text
$ ps -eZ | grep <process_name>
```

Replace `<process_name>` with the process name you want to check. For example, if you want to see the SELinux context for the MySQL process, you would use:

```{.bash data-prompt="$"}
$ ps -eZ | grep mysqld
```

The output displays the SELinux context for the specified process and typically consists of four parts: user, role, type (or domain), and sensitivity level.

??? example "Expected output"

    ```{.text .no-copy}
    system_u:system_r:mysqld_t:s0    3356 ?        00:00:01 mysqld
    ```

- `system_u` represents the user context.
- `system_r` represents the role context.
- `mysqld_t` represents the type (or domain) context.
- `s0` represents the sensitivity level.

This information helps you understand how SELinux enforces security policies for the specified process.

## List SELinux Types or Domains

SELinux types or domains categorize different resources on the system, such as files, directories, and processes. Each type or domain has specific permissions and restrictions associated with it, determining how resources interact with each other. To list SELinux types or domains associated with files, you can use the `ls` command with the `-Z` option. For example:

```{.bash data-prompt="$"}
$ ls -laZ /var/lib/mysql
```

??? example "Expected output"

    ```{.text .no-copy}
    drwxr-x--x. mysql   mysql   system_u:object_r:mysqld_db_t:s0 mysql
    drwxr-x---. mysql   mysql   system_u:object_r:mysqld_db_t:s0 mysql-files
    drwxr-x---. mysql   mysql   system_u:object_r:mysqld_db_t:s0 mysql-keyring
    ```

This command lists the files and directories under `/var/lib/mysql` along with their SELinux context, which includes the type or domain associated with each resource. Understanding these types or domains helps manage SELinux policies and ensure proper access control for MySQL-related resources.