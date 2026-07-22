# Using LDAP authentication plugins

Lightweight Directory Access Protocol (LDAP) provides an alternative method to
access existing directory servers. These servers maintain information about
individuals, groups, and organizations.

Percona Server for MySQL supports two LDAP authentication plugins:

| Authentication method | Description |
|---|---|
| Simple LDAP authentication | The Percona plugin is a free and Open Source implementation of the MySQL Enterprise Simple LDAP authentication plugin. |
| Simple Authentication and Security Layer (SASL)-based LDAP authentication | Supports the SCRAM-SHA-1 SASL mechanism only. |

For all LDAP plugin system variables, see [LDAP authentication plugin system variables](ldap-system-variables.md).

## Choose an authentication method

Both plugins authenticate users against an LDAP server. Both plugins support LDAP group to MySQL role mapping. The main difference is how the client sends the password to the database server.

| Factor | Simple LDAP authentication | SASL-based LDAP authentication |
|---|---|---|
| Password on the wire to the database server | Cleartext | SASL-protected |
| Client plugin | `mysql_clear_password` | `authentication_ldap_sasl_client` |
| Client requirement | Enable `--enable-cleartext-plugin` | Install the SASL client plugin library on the client host |
| Connection security | Require TLS between the client and the database server | TLS recommended; password stays off the wire to the database server |
| LDAP server requirement | Standard LDAP bind | LDAP server must support SASL with the SCRAM-SHA-1 mechanism |
| Additional dependencies | OpenLDAP client library on the database server | SASL server, SASL client library on the client host, SCRAM-SHA-1 configuration |

Choose simple LDAP authentication when you can require TLS on the client connection and you want fewer dependencies.

Choose SASL-based LDAP authentication when the password must stay off the wire to the database server and your LDAP environment supports SCRAM-SHA-1.

## Plugin names and file names

The plugins require manual installation. The database server does not load them by default.

Each method uses these plugin and file names:

=== "Simple LDAP authentication plugin names and library name"

    | Plugin or file | Plugin name or file name |
    |---|---|
    | Server-side plugin | authentication_ldap_simple |
    | Client-side plugin | mysql_clear_password |
    | Library file | authentication_ldap_simple.so |

=== "SASL-based LDAP authentication plugin names and library names"

    | Plugin or file | Plugin name or file name |
    |---|---|
    | Server-side plugin | authentication_ldap_sasl |
    | Client-side plugin | authentication_ldap_sasl_client |
    | Library files | authentication_ldap_sasl.so <br> authentication_ldap_sasl_client.so |

Install `authentication_ldap_sasl_client.so` on each client host that uses SASL-based LDAP authentication. Place the library in the MySQL client plugin directory. The mysql client loads the plugin when you connect to an account that uses `authentication_ldap_sasl`.

## Prerequisites for authentication

The LDAP authentication plugins require the following:

* Run an LDAP server.

* Add user accounts to the LDAP server for authentication.

* Install the OpenLDAP client library on the same system as the plugin.

The SASL-based LDAP authentication additionally requires the following:

* Configure the LDAP server to communicate with a SASL server.

* Install the SASL client library on the same system as the client plugin.

* Configure services to use the SCRAM-SHA-1 SASL mechanism.

## Install the plugins

Install the plugins at server start or at runtime.

### Load the plugins at server start

=== "Load the simple LDAP authentication"

    Add these statements to `my.cnf` to load simple LDAP authentication:

    ```text
    [mysqld]
    plugin-load-add=authentication_ldap_simple.so
    authentication_ldap_simple_server_host=127.0.0.1
    authentication_ldap_simple_bind_base_dn='dc=percona, dc=com'
    ```

    Restart the database server for the changes to take effect.

=== "Load the SASL-based LDAP authentication plugin"

    Add these statements to `my.cnf` to load SASL-based LDAP authentication:

    ```text
    [mysqld]
    plugin-load-add=authentication_ldap_sasl.so
    authentication_ldap_sasl_server_host=127.0.0.1
    authentication_ldap_sasl_bind_base_dn='dc=percona, dc=com'
    ```

### Load the plugins at runtime

=== "Load the simple LDAP authentication plugin"

    ```sql
    INSTALL PLUGIN authentication_ldap_simple SONAME 'authentication_ldap_simple.so';
    ```

    Set and persist values at runtime:

    ```sql
    SET PERSIST authentication_ldap_simple_server_host='127.0.0.1';
    SET PERSIST authentication_ldap_simple_bind_base_dn='dc=percona, dc=com';
    ```

=== "Load the SASL-based LDAP authentication plugin"

    ```sql
    INSTALL PLUGIN authentication_ldap_sasl SONAME 'authentication_ldap_sasl.so';
    ```

    Set and persist values at runtime:

    ```sql
    SET PERSIST authentication_ldap_sasl_server_host='127.0.0.1';
    SET PERSIST authentication_ldap_sasl_bind_base_dn='dc=percona, dc=com';
    ```

## Verify the plugin

### Confirm the plugin is loaded

After you install a plugin, confirm that the database server loaded it and set the status to `ACTIVE`.

Run this statement:

```sql
SHOW PLUGINS;
```

Or query the `INFORMATION_SCHEMA.PLUGINS` table:

=== "Simple LDAP authentication"

    ```sql
    SELECT PLUGIN_NAME, PLUGIN_STATUS
    FROM INFORMATION_SCHEMA.PLUGINS
    WHERE PLUGIN_NAME = 'authentication_ldap_simple';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +----------------------------+----------------+
        | PLUGIN_NAME                | PLUGIN_STATUS  |
        +----------------------------+----------------+
        | authentication_ldap_simple | ACTIVE         |
        +----------------------------+----------------+
        ```

=== "SASL-based LDAP authentication"

    ```sql
    SELECT PLUGIN_NAME, PLUGIN_STATUS
    FROM INFORMATION_SCHEMA.PLUGINS
    WHERE PLUGIN_NAME = 'authentication_ldap_sasl';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +--------------------------+----------------+
        | PLUGIN_NAME              | PLUGIN_STATUS  |
        +--------------------------+----------------+
        | authentication_ldap_sasl | ACTIVE         |
        +--------------------------+----------------+
        ```

Check the server error log if the plugin is missing or the status is not `ACTIVE`.

### Confirm authentication works

Create an LDAP user account. Connect with the mysql client as shown in [Examples](#examples). A successful connection confirms LDAP authentication.

## Configure the LDAP connection

Configure the database server to LDAP server connection separately from the client to database server connection. TLS on the client connection does not encrypt traffic between the database server and the LDAP server.

This configuration example uses simple LDAP authentication. For SASL-based LDAP authentication, use the matching `authentication_ldap_sasl_*` variables.

```text
[mysqld]
authentication_ldap_simple_server_host=ldap.example.com
authentication_ldap_simple_server_port=636
authentication_ldap_simple_bind_base_dn='dc=example,dc=com'
authentication_ldap_simple_user_search_attr=uid
authentication_ldap_simple_bind_root_dn='cn=ldapadmin,ou=services,dc=example,dc=com'
authentication_ldap_simple_bind_root_pwd='LDAP_BIND_PASSWORD'
authentication_ldap_simple_ssl=ON
authentication_ldap_simple_ca_path=/etc/mysql/ldap-ca.pem
```

The database server uses these settings as follows:

| Variable | Purpose |
|---|---|
| `authentication_ldap_simple_server_host`, `authentication_ldap_simple_server_port` | LDAP server address. Port 636 is typical for LDAPS. |
| `authentication_ldap_simple_bind_base_dn` | Base distinguished name (DN) for LDAP searches. |
| `authentication_ldap_simple_user_search_attr` | LDAP attribute that holds the user name. Use `uid` for OpenLDAP. Use `sAMAccountName` for Active Directory. |
| `authentication_ldap_simple_bind_root_dn`, `authentication_ldap_simple_bind_root_pwd` | Credentials the plugin uses to search LDAP for users and groups. |
| `authentication_ldap_simple_ssl` | Enable LDAPS (`ldaps://`). Use [authentication_ldap_simple_tls](ldap-system-variables.md#authentication_ldap_simple_tls) for STARTTLS on port 389. |
| `authentication_ldap_simple_ca_path` | Certificate authority file for LDAPS or STARTTLS. |

For group membership and role mapping, configure [authentication_ldap_simple_group_search_attr](ldap-system-variables.md#authentication_ldap_simple_group_search_attr) and [authentication_ldap_simple_group_search_filter](ldap-system-variables.md#authentication_ldap_simple_group_search_filter) when the default `cn` attribute or filter does not match your directory layout.

To configure a fallback LDAP server, set [authentication_ldap_simple_fallback_server_host](ldap-system-variables.md#authentication_ldap_simple_fallback_server_host) and [authentication_ldap_simple_fallback_server_port](ldap-system-variables.md#authentication_ldap_simple_fallback_server_port). The plugin connects to the fallback server when the primary server is unavailable.

### Active Directory

For Active Directory, use a configuration like this:

```text
[mysqld]
authentication_ldap_simple_server_host=ad.example.com
authentication_ldap_simple_server_port=636
authentication_ldap_simple_bind_base_dn='dc=example,dc=com'
authentication_ldap_simple_user_search_attr=sAMAccountName
authentication_ldap_simple_bind_root_dn='cn=ldapbind,ou=service accounts,dc=example,dc=com'
authentication_ldap_simple_bind_root_pwd='LDAP_BIND_PASSWORD'
authentication_ldap_simple_ssl=ON
```

Match the LDAP group name in [authentication_ldap_simple_group_role_mapping](ldap-system-variables.md#authentication_ldap_simple_group_role_mapping) to the group name returned from Active Directory. Adjust [authentication_ldap_simple_group_search_attr](ldap-system-variables.md#authentication_ldap_simple_group_search_attr) when your directory stores group names in an attribute other than `cn`.

## How authentication works

Each server-side LDAP plugin requires a specific client-side plugin.

=== "Simple LDAP authentication"

    The database server uses `authentication_ldap_simple`. The client uses `mysql_clear_password`. The client sends the password to the database server as cleartext. Require a secure connection between the client and the database server.

=== "SASL-based LDAP authentication"

    The database server uses `authentication_ldap_sasl`. The client uses `authentication_ldap_sasl_client`. The client sends the password through SASL messages within the LDAP protocol. The password stays off the wire to the database server.

The database server rejects the connection when the client user name and host name do not match a server account.

The authentication flow is as follows:

1. The client connects with a user name and password.

2. The database server finds the matching MySQL account.

3. The LDAP server searches for the user entry.

4. The LDAP server validates the password.

5. The authentication plugin determines the authenticated user name from the LDAP entry.

6. The database server checks privileges for the client user name or the authenticated user name.

The LDAP server locates the user entry in one of two ways:

* The MySQL account includes an authentication string with the user DN. Add the DN with `IDENTIFIED WITH <plugin-name> BY '<auth-string>'` or `AS '<auth-string>'`. Authentication fails when the DN or password is wrong.

* The MySQL account has no authentication string. The database server uses the client user name and the configured search attribute to find the LDAP entry.

Authentication fails when the LDAP server finds no match or multiple matches.

When the LDAP entry has no group attribute, the plugin returns the client user name as the authenticated name. When the LDAP entry has a group attribute, the plugin returns the group value as the authenticated name.

When the client user name and authenticated user name match, the database server checks privileges for the client user name. When the names differ, the database server looks for an account that matches the authenticated name.

## External roles

<!-- based on [PS-11248](https://perconadev.atlassian.net/browse/PS-11248) -->

When an LDAP user logs in, the database server checks LDAP group membership.

When the user belongs to a configured group, the database server grants the mapped database roles.

Configure the LDAP group to MySQL role mapping with [authentication_ldap_simple_group_role_mapping](ldap-system-variables.md#authentication_ldap_simple_group_role_mapping) or [authentication_ldap_sasl_group_role_mapping](ldap-system-variables.md#authentication_ldap_sasl_group_role_mapping).

The mapping value is a plain comma-separated string. Use `<ldap_group>=<mysql_role>` pairs:

```text
<ldap_group>=<mysql_role>,<ldap_group2>=<mysql_role2>,
```

The LDAP group name must match the group name from LDAP. By default, the database server reads the group name from the `cn` attribute. The MySQL role must exist before login.

When the user belongs to multiple mapped groups, the database server grants each matching role.

Group membership lookup requires [authentication_ldap_simple_bind_root_dn](ldap-system-variables.md#authentication_ldap_simple_bind_root_dn) and [authentication_ldap_simple_bind_root_pwd](ldap-system-variables.md#authentication_ldap_simple_bind_root_pwd), or the SASL equivalents. See [Map LDAP groups to MySQL roles](#map-ldap-groups-to-mysql-roles).

The database server applies external roles as follows:

* Grant or revoke external role privileges on each user connection.

* Read group membership from the LDAP group attribute.

* Check LDAP group membership only at user login.

* Revoke privileges on the next connection after group removal.

### External roles and LDAP proxy mapping

Percona Server for MySQL supports two LDAP authorization models:

| Model | Configuration | Result |
|---|---|---|
| External roles | Global `authentication_ldap_*_group_role_mapping` variable | The database server grants MySQL roles to the connecting user |
| LDAP proxy mapping | Authentication string with `#group=proxied_user` syntax on a MySQL account | The connecting user acts as a different MySQL account |

External roles grant privileges through MySQL roles. LDAP proxy mapping switches the session to another MySQL user account.

Choose external roles when LDAP groups should map directly to MySQL roles. Choose LDAP proxy mapping when LDAP groups should map to existing MySQL user accounts.

## Create a user using simple LDAP authentication

Use one of these methods to add or modify a user.

=== "Use authentication_ldap_simple plugin"

    Specify the `authentication_ldap_simple` plugin in the `IDENTIFIED WITH` clause of a `CREATE USER` or `ALTER USER` statement:

    ```text
    CREATE USER ... IDENTIFIED WITH authentication_ldap_simple;
    ```

    The database server assigns the specified plugin to the account.

=== "Use the authentication string in simple LDAP"

    An optional authentication string stores the LDAP user DN. The string uses the format `cn,ou,dc,dc`:

    ```text
    CREATE USER ... IDENTIFIED WITH authentication_ldap_simple BY 'cn=[user name],ou=[organization unit],dc=[domain component],dc=com'
    ```

    When the account includes an authentication string, the database server skips these system variables unless [authentication_ldap_simple_group_role_mapping](ldap-system-variables.md#authentication_ldap_simple_group_role_mapping) is set:

    * [authentication_ldap_simple_bind_base_dn](ldap-system-variables.md#authentication_ldap_simple_bind_base_dn)

    * [authentication_ldap_simple_bind_root_dn](ldap-system-variables.md#authentication_ldap_simple_bind_root_dn)

    * [authentication_ldap_simple_bind_root_pwd](ldap-system-variables.md#authentication_ldap_simple_bind_root_pwd)

    * [authentication_ldap_simple_user_search_attr](ldap-system-variables.md#authentication_ldap_simple_user_search_attr)

    * [authentication_ldap_simple_group_search_attr](ldap-system-variables.md#authentication_ldap_simple_group_search_attr)

    When the account has no authentication string, the database server uses these system variables.

    When [authentication_ldap_simple_group_role_mapping](ldap-system-variables.md#authentication_ldap_simple_group_role_mapping) is set, the database server also requires [authentication_ldap_simple_bind_root_dn](ldap-system-variables.md#authentication_ldap_simple_bind_root_dn) and [authentication_ldap_simple_bind_root_pwd](ldap-system-variables.md#authentication_ldap_simple_bind_root_pwd).

## Create a user using SASL-based LDAP authentication

Use one of these methods to add or modify a user.

=== "Use authentication_ldap_sasl plugin"

    Specify the `authentication_ldap_sasl` plugin in the `IDENTIFIED WITH` clause of a `CREATE USER` or `ALTER USER` statement:

    ```text
    CREATE USER ... IDENTIFIED WITH authentication_ldap_sasl;
    ```

=== "Use the authentication string in SASL-based LDAP"

    An optional authentication string stores the LDAP user DN. The string uses the format `cn,ou,dc,dc`. You can use `BY` or `AS` for the authentication string:

    ```text
    CREATE USER ... IDENTIFIED WITH authentication_ldap_sasl BY 'cn=[user name],ou=[organization unit],dc=[domain component],dc=com'
    ```

    When the account includes an authentication string, the database server skips these system variables unless [authentication_ldap_sasl_group_role_mapping](ldap-system-variables.md#authentication_ldap_sasl_group_role_mapping) is set:

    * [authentication_ldap_sasl_bind_base_dn](ldap-system-variables.md#authentication_ldap_sasl_bind_base_dn)

    * [authentication_ldap_sasl_bind_root_dn](ldap-system-variables.md#authentication_ldap_sasl_bind_root_dn)

    * [authentication_ldap_sasl_bind_root_pwd](ldap-system-variables.md#authentication_ldap_sasl_bind_root_pwd)

    * [authentication_ldap_sasl_user_search_attr](ldap-system-variables.md#authentication_ldap_sasl_user_search_attr)

    * [authentication_ldap_sasl_group_search_attr](ldap-system-variables.md#authentication_ldap_sasl_group_search_attr)

    When the account has no authentication string, the database server uses these system variables.

    When [authentication_ldap_sasl_group_role_mapping](ldap-system-variables.md#authentication_ldap_sasl_group_role_mapping) is set, the database server also requires [authentication_ldap_sasl_bind_root_dn](ldap-system-variables.md#authentication_ldap_sasl_bind_root_dn) and [authentication_ldap_sasl_bind_root_pwd](ldap-system-variables.md#authentication_ldap_sasl_bind_root_pwd).

## Examples

These examples configure an LDAP user and verify authentication with a client connection.

The sample LDAP user DN is:

```text
uid=ldapuser,ou=testusers,dc=percona,dc=com
```

=== "Simple LDAP authentication"

    Create a database server account for `ldapuser`:

    ```sql
    CREATE USER 'ldapuser'@'localhost' IDENTIFIED WITH authentication_ldap_simple BY 'uid=ldapuser,ou=testusers,dc=percona,dc=com';
    ```

    The authentication string does not include the LDAP password. The client user must provide the LDAP password at connect time.

    ```sql
    mysql --user=ldapuser --password --enable-cleartext-plugin
    ```

    Enter the LDAP password for `ldapuser` when prompted. A successful connection confirms that LDAP authentication works.

    The client sends the password as cleartext. This behavior is required for a server-side LDAP library without SASL. To reduce risk:

    * Require clients to enable the `mysql_clear_password` plugin with `--enable-cleartext-plugin`.

    * Require clients to connect over an encrypted connection to the database server.

=== "SASL-based LDAP authentication"

    Create a database server account for `ldapuser`:

    ```sql
    CREATE USER 'ldapuser'@'localhost' IDENTIFIED WITH authentication_ldap_sasl AS 'uid=ldapuser,ou=testusers,dc=percona,dc=com';
    ```

    The authentication string does not include the LDAP password. The client user must provide the LDAP password at connect time.

    ```sql
    mysql --user=ldapuser --password
    ```

    Enter the LDAP password for `ldapuser` when prompted. A successful connection confirms that LDAP authentication works.

    The client and database server SASL LDAP plugins exchange SASL messages within the LDAP protocol.

### Map LDAP groups to MySQL roles

This example maps two LDAP groups to MySQL roles. The LDAP groups have a `cn` value of `mysql-admins` and `mysql-readers`. The example uses simple LDAP authentication. For SASL-based LDAP authentication, use the `authentication_ldap_sasl_*` variables with the same mapping string format.

Create the MySQL roles and grant privileges:

```sql
CREATE ROLE 'mysql_admins', 'mysql_readers';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'mysql_admins';
GRANT SELECT ON app_db.* TO 'mysql_readers';
```

Set the mapping and LDAP bind credentials at server start in `my.cnf`:

```text
[mysqld]
authentication_ldap_simple_group_role_mapping='mysql-admins=mysql_admins,mysql-readers=mysql_readers,'
authentication_ldap_simple_bind_root_dn='cn=ldapadmin,ou=services,dc=percona,dc=com'
authentication_ldap_simple_bind_root_pwd='LDAP_BIND_PASSWORD'
```

Set the values at runtime instead:

```sql
SET PERSIST authentication_ldap_simple_group_role_mapping = 'mysql-admins=mysql_admins,mysql-readers=mysql_readers,';
SET PERSIST authentication_ldap_simple_bind_root_dn = 'cn=ldapadmin,ou=services,dc=percona,dc=com';
SET PERSIST authentication_ldap_simple_bind_root_pwd = 'LDAP_BIND_PASSWORD';
```

Create an LDAP user account:

```sql
CREATE USER 'ldapuser'@'%' IDENTIFIED WITH authentication_ldap_simple;
```

Connect as `ldapuser` with the LDAP password. When `ldapuser` belongs to the `mysql-admins` LDAP group, the database server grants the `mysql_admins` role on connection. Verify the role assignment:

```sql
SHOW GRANTS;
SELECT CURRENT_ROLE();
```

When the role appears in the output but privileges are missing, activate the role:

```sql
SET ROLE 'mysql_admins';
SHOW GRANTS;
```

To activate all granted roles at login, enable [activate_all_roles_on_login :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-variables.html#sysvar_activate_all_roles_on_login).

## Troubleshoot authentication

When LDAP authentication fails, check these items:

* Confirm the plugin status is `ACTIVE`. See [Confirm the plugin is loaded](#confirm-the-plugin-is-loaded).

* Review the server error log.

* Increase the logging level with [authentication_ldap_simple_log_status](ldap-system-variables.md#authentication_ldap_simple_log_status) or [authentication_ldap_sasl_log_status](ldap-system-variables.md#authentication_ldap_sasl_log_status). Valid values range from 1 to 6. Higher values write more detail to the error log.

* Confirm the database server can reach the LDAP server on the configured host and port.

* Confirm `authentication_ldap_*_bind_root_dn` and `authentication_ldap_*_bind_root_pwd` are correct when the plugin searches LDAP for users or groups.

* Confirm `authentication_ldap_*_user_search_attr` matches your directory. OpenLDAP directories often use `uid`. Active Directory directories often use `sAMAccountName`.

* Confirm the LDAP group name in `authentication_ldap_*_group_role_mapping` matches the group name returned from LDAP.

* Confirm each mapped MySQL role exists and has the expected privileges before login.

* For simple LDAP authentication, confirm the client uses `--enable-cleartext-plugin` and connects over TLS.

* For SASL-based LDAP authentication, confirm `authentication_ldap_sasl_client.so` is installed on the client host.

## Uninstall the plugins

When you installed either plugin at [server startup](#load-the-plugins-at-server-start), remove those options from the `my.cnf` file. Remove any startup options that set LDAP system variables. Restart the database server.

=== "Uninstall the simple LDAP authentication plugin"

    When you installed the plugin at [runtime](#load-the-plugins-at-runtime), run these statements:

    ```sql
    UNINSTALL PLUGIN authentication_ldap_simple;
    ```

    When you used `SET PERSIST`, run `RESET PERSIST` to remove the settings.

=== "Uninstall the SASL-based LDAP authentication plugin"

    When you installed the plugin at [runtime](#load-the-plugins-at-runtime), run these statements:

    ```sql
    UNINSTALL PLUGIN authentication_ldap_sasl;
    ```

    When you used `SET PERSIST`, run `RESET PERSIST` to remove the settings.
