# FIDO authentication plugin

!!! important

    --8<--- "tech.preview.md:5:5"
    
Percona Server for MySQL supports the Fast Identify Online (FIDO) authentication method that uses a plugin. The FIDO authentication provides a set of standards that reduces the reliance on passwords.

The server-side fido authentication plugin enables authentication using external devices. If this plugin is the only authentication plugin used by the account, this plugin allows authentication without a password. Multi-factor authentication can use non-FIDO MySQL authentication methods, the FIDO authentication method, or a combination of both. 

All distributions include the client-side `authentication_fido_client` plugin. This plugin allows clients to connect to accounts that use `authentication_fido` and authenticate on a server that has that plugin loaded.

## Plugin and library file names

The plugin and library file names are listed in the following table. 

| Plugin or file name | Plugin or library file name |
|---|---|
| Server-side plugin  | `authentication_fido` |
| Client-side plugin | `authentication_fido_client` |
| Library file | authentication_fido.so |

## Install the FIDO authentication plugin

The library file must be stored in the directory named by the [`plugin_dir`] variable. 

=== "At server startup"

    At server startup, use the [`--plugin_load_add`] option with the library name. The option must be added each time the server starts.

=== "Edit my.cnf and restart the server"

    ```text

    [mysqld]
    ...
    plugin-load-add=authentication_fido.so
    ...
    ```

=== "Load the plugin at runtime"

    ```{.bash data-prompt="mysql>"}
    mysql> INSTALL PLUGIN authentication_fido SONAME `authentication_fido.so`;
    ```

### Verify installation

Use the [`SHOW PLUGINS`] statement or query the `INFORMATION_SCHEMA.PLUGINS` table to verify that the plugin was loaded successfully and is active.

Check the server error log if the plugin is not loaded.

## FIDO authentication strategies

FIDO can be used with [non-FIDO authentication](#use-fido-authentication-with-non-fido-authentication). FIDO can be used to [create 1FA accounts that do not require passwords](#use-fido-authentication-as-the-only-method).

### Use FIDO authentication with non-FIDO authentication

A FIDO device is associated with the account using FIDO authentication. The FIDO device must be registered before the account can be used in a one-time process. This device must be available and the user must perform whatever FIDO device action required, such as adding a thumbprint, or the registration fails.

The registration can only be performed by the user named by the account. An error occurs if a user attempts the registration for another user. 

The device registration can be performed on the mysql client or MySQL Shell.  Use the `--fido-register-factor` option with the factor or factors for the device. For example, if you are using FIDO as a second authentication method, which is a common practice, the statement is `--fido-register-factor=2`. 

Any authentication factors that proceed the FIDO registration must succeed before the registration continues.

The server checks the user account information to determine if the FIDO device requires registration. If the device must be registered, the server switches the client session to sandbox mode. The registration must be completed before any other activity. In this mode, only `ALTER USER` statements are permitted. If the session is started with `--fido-register-factor`, the client generates the statements required to register. After the registration is complete, the session is switched out of sandbox mode and the client can proceed as normal.

After the device is registered, the server updates the `mysql.user` system table for that account with the device registration status and stores the public key and credential ID.

The user must use the same FIDO device during registration and authentication. If the device is reset or the user attempts to use a different device, the authentication fails. To use a different device, the registered device must be unregistered and you must complete the registration process again.

### Use FIDO authentication as the only method

If FIDO is used as the only method of authentication, the method does not use a password. The authentication uses a method such as a biometric scan or a security key.

The user creates an account with the `PASSWORDLESS_USER_ADMIN` privilege and the `CREATE USER` privilege. 

The first element of the `authentication_policy` value must be an asterisk(*). Do not start with the plugin name. [Configuring the `authentication policy` value] has more information.

You must include the `INITIAL AUTHENTICATION IDENTIFIED BY` clause in the `CREATE USER` statement. The server does accept the statement without the clause but the account is unusable because the user cannot connect to the server to register the device. 

The `CREATE USER` syntax is the following:

```{.bash data-prompt="mysql>"}
mysql> CREATE USER <username>@<hostname> IDENTIFIED WITH authentication_fido INITIAL AUTHENTICATION IDENTIFIED BY '<password>';
```

During registration, the user must authenticate with the password. After the device is registered, the server deletes the password and modifies the account to make FIDO the only authentication method. 

## Unregister a FIDO device

If the FIDO device is replaced or lost, the following actions occur:

| Action required | Who can perform the action |
|---|---|
| Unregister the previous device | The account owner or any user with the `CREATE USER` privilege can unregister the device |
| Register the new device | The user planning to use the device must register the new device |

Unregister a device with the following statement:

```{.bash data-prompt="mysql>"}
mysql> ALTER USER `username`@`hostname` {2|3} FACTOR UNREGISTER;
```

[`plugin_dir`]: https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-variables.html#sysvar_plugin_dir
[`--plugin_load_add`]: https://dev.mysql.com/doc/refman/{{vers}}/en/server-options.html#option_mysqld_plugin-load-add
[Configuring the `authentication policy` value]: https://dev.mysql.com/doc/refman/{{vers}}/en/multifactor-authentication.html#multifactor-authentication-policy
[`SHOW PLUGINS`]: https://dev.mysql.com/doc/refman/{{vers}}/en/show-plugins.html