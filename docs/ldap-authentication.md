# Using LDAP authentication plugins

!!! important

    --8<--- "tech.preview.md:5:5"

LDAP (Lightweight Directory Access Protocol) provides an alternative method to
access existing directory servers, which maintain information about
individuals, groups, and organizations.

Percona Server for MySQL supports the simple LDAP authentication. The Percona simple LDAP authentication plugin is a free and Open Source implementation of the MySQL Enterprise Simple LDAP authentication plugin. Percona Server for MySQL also supports an SASL-based LDAP authentication plugin. This plugin only supports the SCRAM-SHA-1 SASL mechanism. 

## Plugin names and file names

The following tables show the plugin names and the file name for simple LDAP authentication and SASL-based LDAP authentication.

=== "Simple LDAP authentication plugin names and library name"

    | Plugin or file | Plugin name or file name |
    |---|---|
    | Server-side plugin | authentication_ldap_simple |
    | client-side plugin | mysql_clear_password |
    | library file | authentication_ldap_simple.so |

=== "SASL-based LDAP authentication plugin names and library names"

    | Plugin or file | Plugin name or file name |
    |---|---|
    | Server-side plugin | authentication_ldap_sasl |
    | client-side plugin | authentication_ldap_sasl_client |
    | library files | authentication_ldap_sasl.so <br> authentication_ldap_sasl_client.so  |

## How does the authentication work

The server-side LDAP plugins work only with the specific client-side plugin:

* The `authentication_ldap_simple` plugin, on the server, performs the simple LDAP authentication. The client, using `mysql_clear_password`, connects to the server. The client plugin sends the password to the server as cleartext. For this method, use a secure connection between the client and server.

* The `authentication_ldap_sasl` plugin, on the server, performs the SASL-based LDAP authentication. The client must use the `authentication_ldap_sasl_client` plugin. The method does not send the password to the server in cleartext. The server-side and client-side plugins use Simple Authentication and Security Layer (SASL) to send secure messages within the LDAP protocol.

For either method, the database server rejects the connection if the client user name and the host name do not match a server account.

If a database server LDAP authentication is successful, the LDAP server searches for an entry. The LDAP server matches the user and authenticates using the LDAP password. If the database server account names the LDAP user distinguished name (DN), added by the `IDENTIFIED WITH <plugin-name> BY '<auth-string>'` clause, the LDAP server uses that value and the LDAP password provided by the client. This method fails if the DN and password have incorrect values

If the LDAP server finds multiple matches or no match, authentication fails.

If the password is correct, and the LDAP server finds a match, then LDAP authentication succeeds. The LDAP server returns the LDAP entry and the authentication plugin determines the authenticated user's name based on the entry. If the LDAP entry has no group attribute, the plugin returns the client user name as the authenticated name. If the LDAP entry has a group attribute, the plugin returns the group value as the authenticated name.

The database server compares the client user name to the authenticated user name. If these names are the same, the database server uses the client user name to check for privileges. If the name differs, then the database server looks for an account that matches the authenticated name.

## Prerequisites for authentication

The LDAP authentication plugins required the following:

* An available LDAP server

* The LDAP server must contain the LDAP user accounts to be authenticated

* The OpenLDAP client library must be available on the same system as the plugin

The SASL-based LDAP authentication additionally requires the following:

* Configure the LDAP server to communicate with a SASL server

* Available SASL client library on the same system as the client plugin.

* Services are configured to use the supported SCRAM-SHA-1 SASL mechanism

## Install the plugins

You can use either of the following methods to install the plugins.

### Load the plugins at server start

Use either of the following methods to load the plugin at server start.

=== "Load the simple LDAP authentication"

    Add the following statements to your `my.cnf` file to load simple LDAP authentication:

    ```text
    [mysqld]
    plugin-load-add=authentication_ldap_simple.so
    authentication_ldap_simple_server_host=127.0.0.1
    authentication_ldap_simple_bind_base_dn='dc=percona, dc=com'
    ```

    Restart the server for the changes to take effect.

=== "Load the SASL_based LDAP authentication plugin"

    Add the following statements to your `my.cnf` file to load the SASL-based LDAP authentication:

    ```text
    [mysqld]
    plugin-load-add=authentication_ldap_sasl.so
    authentication_ldap_sasl_server_host=127.0.0.1
    authentication_ldap_sasl_bind_base_dn='dc=percona, dc=com'
    ```

### Load the plugins at runtime

Install the plugin with the following statements.

=== "Load the simple LDAP authentication plugin"

    ```{.bash data-prompt="mysql>"}
    mysql> INSTALL PLUGIN authentication_ldap_simple SONAME 'authentication_ldap_simple.so';
    ```

    To set and persist values at runtime, use the following statements:

    ```{.bash data-prompt="mysql>"}
    mysql> SET PERSIST authentication_ldap_simple_server_host='127.0.0.1';
    mysql> SET PERSIST authentication_ldap_simple_bind_base_dn='dc=percona, dc=com';
    ```

=== "Load the SASL-based LDAP authentication plugin" 

    ```{.bash data-prompt="mysql>"}
    mysql> INSTALL PLUGIN authentication_ldap_sasl SONAME 'authentication_ldap_sasl.so`;
    ```

    To set and persist values at runtime, use the following statements:

    ```{.bash data-prompt="mysql>"}
    mysql> SET PERSIST authentication_ldap_sasl_server_host='127.0.0.1';
    mysql> SET PERSIST authentication_ldap_sasl_bind_base_dn='dc=percona, dc=com';
    ```

## Create a user using simple LDAP authentication

There are several methods to add or modify a user.

=== "Use authentication_ldap_simple plugin"

    In the `CREATE USER` statement or the `ALTER USER` statement, for simple LDAP authentication, you can specify the `authentication_ldap_simple` plugin in the `IDENTIFIED WITH` clause:

    ```text
    mysql> CREATE USER ... IDENTIFIED WITH authentication_ldap_simple;
    ```

    Using the `IDENTIFIED WITH` clause, the database server assigns the specified plugin.

=== "Use the authentication string in simple LDAP"

    If you provide the optional authentication string clause, ‘cn,ou,dc,dc’ in the example, the string is stored along with the password.

    ```text
    mysql> CREATE USER ... IDENTIFIED WITH authentication_ldap_simple BY 'cn=[user name],ou=[organization unit],dc=[domain component],dc=com'
    ```

    Unless the [authentication_ldap_simple_group_role_mapping](ldap-system-variables.md#authentication_ldap_simple_group_role_mapping) variable is used, creating a user with an authentication string does not use the following system variables:

    * [authentication_ldap_simple_bind_base_dn](ldap-system-variables.md#authentication_ldap_simple_bind_base_dn)
  
    * [authentication_ldap_simple_bind_root_dn](ldap-system-variables.md#authentication_ldap_simple_bind_root_dn)
  
    * [authentication_ldap_simple_bind_root_pwd](ldap-system-variables.md#authentication_ldap_simple_bind_root_pwd)
  
    * [authentication_ldap_simple_user_search_attr](ldap-system-variables.md#authentication_ldap_simple_user_search_attr)
  
    * [authentication_ldap_simple_group_search_attr](ldap-system-variables.md#authentication_ldap_simple_group_search_attr)
  
    Creating the user with `IDENTIFIED BY authentication_ldap_simple` uses the variables.
    
    Creating the user with the [authentication_ldap_simple_group_role_mapping](ldap-system-variables.md#authentication_ldap_simple_group_role_mapping) variable also adds the [authentication_ldap_simple_bind_root_dn](ldap-system-variables.md#authentication_ldap_simple_bind_root_dn) and [authentication_ldap_simple_bind_root_pwd](ldap-system-variables.md#authentication_ldap_simple_bind_root_pwd) variables.

## Create a user using SASL-based LDAP authentication

There are several methods to add or modify a user.

=== "Use authentication_ldap_sasl plugin"

    For SASL-based LDAP authentication, in the `CREATE USER` statement or the `ALTER USER` statement, you can specify the `authentication_ldap_sasl` plugin:

    ```text
    mysql> CREATE USER ... IDENTIFIED WITH authentication_ldap_sasl;
    ```

=== "Use the authentication string in SASL-based LDAP"

    If you provide the optional authentication string clause, ‘cn,ou,dc,dc’ in the example, the string is stored along with the password.

    ```text
    mysql> CREATE USER ... IDENTIFIED WITH authentication_ldap_sasl BY 'cn=[user name],ou=[organization unit],dc=[domain component],dc=com'
    ```

    Unless the [authentication_ldap_sasl_group_role_mapping](ldap-system-variables.md#authentication_ldap_sasl_group_role_mapping) variable is used, creating a user with an authentication string does not use the following system variables:

    * [authentication_ldap_sasl_bind_base_dn](ldap-system-variables.md#authentication_ldap_sasl_bind_base_dn)

    * [authentication_ldap_sasl_bind_root_dn](ldap-system-variables.md#authentication_ldap_sasl_bind_root_dn)

    * [authentication_ldap_sasl_bind_root_pwd](ldap-system-variables.md#authentication_ldap_sasl_bind_root_pwd)

    * [authentication_ldap_sasl_user_search_attr](ldap-system-variables.md#authentication_ldap_sasl_user_search_attr)

    * [authentication_ldap_sasl_group_search_attr](ldap-system-variables.md#authentication_ldap_sasl_group_search_attr)

    Creating the user with `IDENTIFIED BY authentication_ldap_sasl` uses the variables. 
    
    Creating the user with the [authentication_ldap_sasl_group_role_mapping](ldap-system-variables.md#authentication_ldap_sasl_group_role_mapping) variable also adds the[authentication_ldap_sasl_bind_root_dn](ldap-system-variables.md#authentication_ldap_sasl_bind_root_dn) and [authentication_ldap_sasl_bind_root_pwd](ldap-system-variables.md#authentication_ldap_sasl_bind_root_pwd) variables.

## Examples

The following sections are examples of using simple LDAP authentication and SASL-based LDAP authentication.

For the purposes of this example, we use the following LDAP user:

```text
uid=ldapuser,ou=testusers,dc=percona,dc=com
```

=== "Simple LDAP authentication"

    The following example configures an LDAP user and connects to the database server.

    Create a database server account for `ldapuser` with the following statement:

    ```{.bash data-prompt="mysql>"}
    mysql> CREATE USER 'ldapuser'@'localhost' IDENTIFIED WITH authentication_ldap_simple BY 'uid=ldapuser,ou=testusers,dc=percona,dc=com';
    ```

    The authentication string does not include the LDAP password. This password must be provided by the client user when they connect.

    ```{.bash data-prompt="mysql>"}
    mysql> mysql --user=ldapuser --password --enable-cleartext-plugin
    ```

    The user enters the `ldapuser` password. The client sends the password as cleartext, which is necessary when using a server-side LDAP library without SASL. The following actions may minimize the risk:

    * Require that the database server clients explicitly enable the `mysql_clear_password` plugin with `--enable-cleartext-plugin`. 
    * Require that the database server clients connect to the database server using an encrypted connection

=== "SASL-based LDAP authentication"

    The following example configures an LDAP user and connect to the database server.

    Create a database server account for `ldapuser` with the following statement:

    ```{.bash data-prompt="mysql>"}
    mysql> CREATE USER 'ldapuser'@'localhost' IDENTIFIED WITH authentication_ldap_sasl AS 'uid=ldapuser,ou=testusers,dc=percona,dc=com';
    ```

    The authentication string does not include the LDAP password. This password must be provided by the client user when they connect.

    Clients connect ot the database server by providing the database server user name and LDAP password:

    ```{.bash data-prompt="mysql>"}
    mysql> mysql --user=ldapuser --password
    ```

    The authentication is similar to the authentication method used by simple LDAP authentication, except that the client and the database server SASL LDAP plugins use SASL messages. These messages are secure within the LDAP protocol.

### Uninstall the plugins

If you installed either plugin at [server startup](#load-the-plugins-at-server-start), remove those options from the `my.cnf` file, remove any startup options that set LDAP system variables, and restart the server.

=== "Uninstall the simple LDAP authentication plugin"

    If you installed the plugins at [runtime](#load-the-simple-ldap-authentication-plugin-at-runtime), run the following statements:

    ```{.bash data-prompt="mysql>"}
    mysql> UNINSTALL PLUGIN authentication_ldap_simple;
    ```

    If you used `SET_PERSIST`, use `RESET PERSIST` to remove the settings.

=== "Uninstall the SASL-based LDAP authentication plugin"

    If you installed the plugins at [runtime](#load-the-sasl-based-ldap-authentication-plugin-at-runtime), run the following statements:

    ```{.bash data-prompt="mysql>"}
    mysql> UNINSTALL PLUGIN authentication_ldap_sasl;
    ```

    If you used `SET_PERSIST`, use `RESET PERSIST` to remove the settings.
