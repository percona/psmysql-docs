# LDAP Simple system variables

The following variables are static. These variables can only be modified by restarting the server with a new value set in the configuration file (for example, my.cnf or my.ini) or passed as a command-line option when starting the server.

| Name                                                      |
|-----------------------------------------------------------|
| [authentication_ldap_simple_bind_base_dn](#authentication_ldap_simple_bind_base_dn)        |
| [authentication_ldap_simple_bind_root_dn](#authentication_ldap_simple_bind_root_dn)        |
| [authentication_ldap_simple_bind_root_pwd](#authentication_ldap_simple_bind_root_pwd)       |
| [authentication_ldap_simple_ca_path](#authentication_ldap_simple_ca_path)             |
| [authentication_ldap_simple_fallback_server_host](#authentication_ldap_simple_fallback_server_host)|
| [authentication_ldap_simple_fallback_server_port](#authentication_ldap_simple_fallback_server_port)|
| [authentication_ldap_simple_group_role_mapping](#authentication_ldap_simple_group_role_mapping)  |
| [authentication_ldap_simple_group_search_attr](#authentication_ldap_simple_group_search_attr)   |
| [authentication_ldap_simple_group_search_filter](#authentication_ldap_simple_group_search_filter) |
| [authentication_ldap_simple_init_pool_size](#authentication_ldap_simple_init_pool_size)      |
| [authentication_ldap_simple_log_status](#authentication_ldap_simple_log_status)          |
| [authentication_ldap_simple_max_pool_size](#authentication_ldap_simple_max_pool_size)       |
| [authentication_ldap_simple_server_host](#authentication_ldap_simple_server_host)         |
| [authentication_ldap_simple_server_port](#authentication_ldap_simple_server_port)         |
| [authentication_ldap_simple_ssl](#authentication_ldap_simple_ssl)                 |
| [authentication_ldap_simple_tls](#authentication_ldap_simple_tls)                 |
| [authentication_ldap_simple_user_search_attr](#authentication_ldap_simple_user_search_attr)    |

### `authentication_ldap_simple_bind_base_dn`

| Option                | Details        |
|-----------------------|----------------|
| Command-line          | `--authentication-ldap-simple-bind-base-dn` |
| Scope                 | global         |
| Dynamic               | Yes            |
| Data Type             | String         |
| Default               | NULL              |


This variable sets the base Distinguished Name (DN) for binding to the LDAP server during simple LDAP authentication.

Setting this value correctly is crucial for security. Incorrect values can cause authentication failures or security risks.

### `authentication_ldap_simple_bind_root_dn`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-bind-root-dn=value` |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | NULL                                           |


Percona Server for MySQL uses a root Distinguished Name (DN) to connect to the LDAP server for simple LDAP authentication. This variable is used with [authentication_ldap_simple_bind_root_pwd](#authentication_ldap_simple_bind_root_pwd). This root DN, along with the root password, is used to authenticate with the LDAP server and obtain a connection.

* If the MySQL account does not specify an LDAP user DN:

    * MySQL first authenticates to the LDAP server using the provided root DN and password.
  
    * Then, it searches the LDAP directory for the user DN corresponding to the MySQL user's name.
  
    * Finally, MySQL attempts to authenticate using the found user DN and the password provided by the MySQL user.
  
If the MySQL account specifies an LDAP user DN:

  * MySQL directly authenticates to the LDAP server using the provided user DN and the password supplied by the MySQL user.
 
  * This method is faster as it avoids the initial authentication step with the root DN.
 
### `authentication_ldap_simple_bind_root_pwd`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-bind-root-pwd=value` |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | NULL                                           |

The `root` password used to authenticate against an LDAP. This variable is used with [`authentication_ldap_simple_bind_root_dn`](#authentication_ldap_simple_bind_root_dn).

### `authentication_ldap_simple_ca_path`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-ca_path=value`   |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | Null                                           |

This variable specifies the absolute path to the Certificate Authority (CA) file for LDAP Simple authentication. This variable allows the authentication plugin to verify the LDAP server certificate, enhancing security.

### `authentication_ldap_simple_fallback_server_host`

| Option | Description |
|---|---|
| Command-line | --authentication-ldap-simple-fallback-server-host |
| Scope | Global |
| Dynamic | Yes |
| Type | Sting |
| Default | NULL |

Use with [`authentication_ldap_simple_fallback_server_port`](#authentication_ldap_simple_fallback_server_port).

If the primary server is unavailable, the authentication plugin attempts to connect to the fallback server and authenticate using that server.

### `authentication_ldap_simple_fallback_server_port`

| Option | Description |
|---|---|
| Command-line | --authentication-ldap-simple-fallback-server-port |
| Scope | Global |
| Dynamic | Yes |
| Type | Integer |
| Default | NULL |

Use with [`authentication_ldap_simple_fallback_server_host`](#authentication_ldap_simple_fallback_server_host).

If the primary server is unavailable, the authentication plugin attempts to connect to the fallback server and authenticate using that server.

If the fallback server host has a value, and the fallback port is 0, users can specify multiple fallback servers.

Use this format to specify multiple fallback servers: `authentication_ldap_simple_fallback_server_host="ldap(s)://host:port,ldap(s)://host2:port2`, for example.

### `authentication_ldap_simple_group_role_mapping`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-group-role-mapping=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | Null                                       |

When an LDAP user logs in, the server checks if the LDAP user is a member of the specified group. If the user is, then the server automatically grants the database server roles to the user.

The variable has this format: `<ldap_group>=<mysql_role>,<ldap_group2>=<mysql_role2>,`.

### `authentication_ldap_simple_group_search_attr`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-group-search-attr=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | cn                                       |

The attribute name that specifies group names in the LDAP directory entries for simple LDAP authentication.  

### `authentication_ldap_simple_group_search_filter`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-group-search-filter=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | (\|(&(objectClass=posixGroup)(memberUid=%s))(&(objectClass=group)(member=%s)))                                       |

The custom group search filter for simple LDAP authentication.

### `authentication_ldap_simple_init_pool_size`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-init-pool-size=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | Integer                                     |
| Default      | 10                                       |
| Minimum value | 0 |
| Maximum value | 32767 |
| Unit | connections |

The initial size of the connection pool to the LDAP server for simple LDAP authentication.

### `authentication_ldap_simple_log_status`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-log-status=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | Integer                                     |
| Default      | 1                                       |
| Minimum value | 1 |
| Maximum value | 6 |

The logging level for messages written to the error log for simple LDAP authentication.

### `authentication_ldap_simple_max_pool_size`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-max-pool-size=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | Integer                                     |
| Default      | 1000                                       |
| Minimum value | 0 |
| Maximum value | 32767 |
| Unit | connections |

The maximum connection pool size to the LDAP server in simple LDAP authentication. The variable is used with [`authentication_ldap_simple_init_pool_size`](#authentication_ldap_simple_init_pool_size).

### `authentication_ldap_simple_server_host`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-server-host=value` |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | Null                                           |

The LDAP server host used for LDAP authentication.


### `authentication_ldap_simple_server_port`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-server-port=value` |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | Null                                           |

The LDAP server TCP/IP port number used for LDAP authentication.


### `authentication_ldap_simple_ssl`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-ssl=value`       |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | Null                                           |

If this variable is enabled, the plugin connects to the server with SSL.

### `authentication_ldap_simple_tls`

| **Option**         | **Description**                                 |
|---------------------|-------------------------------------------------|
| Command-line        | `--authentication-ldap-simple-tls=value`       |
| Scope               | Global                                         |
| Dynamic             | No                                             |
| Data type           | String                                         |
| Default             | Null                                           |

If this variable is enabled, the plugin connects to the server with TLS.

### `authentication_ldap_simple_user_search_attr`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-simple-user-search-attr=value |
| Scope        | Global                                 |
| Dynamic      | Yes                                     |
| Data type    | String                                 |
| Default      | uid                                   |

The attribute name that specifies the user names in LDAP directory entries in simple LDAP authentication.

For more details, see the [LDAP Authentication documentation](ldap-authentication.md).