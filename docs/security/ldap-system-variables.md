# LDAP authentication plugin system variables

## Authentication system variables

[Percona 8.0.30-22][8.0.30-22-RN] adds LDAP_SASL variables and the `fallback` server variables for simple LDAP and SASL-based LDAP.

!!! important

    {% include './snippets/tech-preview/_tech-preview-variables.md'%}

The installation adds the following variables:

| Variable name | Description |
|---|---|
| [authentication_ldap_sasl_bind_base_dn](#authentication_ldap_sasl_bind_base_dn) | Base distinguished name |
| [authentication_ldap_sasl_bind_root_dn](#authentication_ldap_sasl_bind_root_dn) | Root distinguished name |
| [authentication_ldap_sasl_bind_root_dn_pwd](#authentication_ldap_sasl_bind_root_pwd) | Password for the root distinguished name |
| [authentication_ldap_sasl_ca_path](#authentication_ldap_sasl_ca_path) | Absolute path of the certificate authority |
| [authentication_ldap_sasl_fallback_server_host](#authentication_ldap_sasl_fallback_server_host) | If the primary server is unavailable, the authentication plugin attempts to connect to the fallback server |
| [authentication_ldap_sasl_fallback_server_port](#authentication_ldap_sasl_fallback_server_port) | The port number for the fallback server |
| [authentication_ldap_sasl_group_role_mapping](#authentication_ldap_sasl_group_role_mapping) | A list of LDAP group names - MySQL role pairs |
| [authentication_ldap_sasl_group_search_attr](#authentication_ldap_sasl_group_search_attr) | Name of the attribute that specifies the group names in the LDAP directory entries |
| [authentication_ldap_sasl_group_search_filter](#authentication_ldap_sasl_group_search_filter) | Custom group search filter |
| [authentication_ldap_sasl_init_pool_size](#authentication_ldap_sasl_init_pool_size) | Initial size of the connection pool to the LDAP server |
| [authentication_ldap_sasl_log_status](#authentication_ldap_sasl_log_status) | logging level |
| [authentication_ldap_sasl_max_pool_size](#authentication_ldap_sasl_max_pool_size) | Maximum size of the pool of connections to the LDAP server |
| [authentication_ldap_sasl_server_host](#authentication_ldap_sasl_server_host) | LDAP server host |
| [authentication_ldap_sasl_server_port](#authentication_ldap_sasl_server_port) | LDAP server TCP/IP port number |
| [authentication_ldap_sasl_ssl](#authentication_ldap_sasl_ssl) | If plugin connections to the LDAP server use the SSL protocol (ldaps://) |
| [authentication_ldap_sasl_tls](#authentication_ldap_sasl_tls) | If plugin connections to the LDAP server are secured with STARTTLS (ldap://) |
| [authentication_ldap_sasl_user_search_attr](#authentication_ldap_sasl_user_search_attr) | Name of the attribute that specifies user names in the LDAP directory entries |
| [authentication_ldap_simple_bind_base_dn](#authentication_ldap_simple_bind_base_dn) | Base distinguished name |
| [authentication_ldap_simple_bind_root_dn](#authentication_ldap_simple_bind_root_dn) | Root distinguished name |
| [authentication_ldap_simple_bind_root_dn_pwd](#authentication_ldap_simple_bind_root_pwd) | Password for the root distinguished name |
| [authentication_ldap_simple_ca_path](#authentication_ldap_simple_ca_path) | Absolute path of the certificate authority |
| [authentication_ldap_simple_fallback_server_host](#authentication_ldap_simple_fallback_server_host) | If the primary server is unavailable, the authentication plugin attempts to connect to the fallback server |
| [authentication_ldap_simple_fallback_server_port](#authentication_ldap_simple_fallback_server_port) | The port number for the fallback server |
| [authentication_ldap_simple_group_role_mapping](#authentication_ldap_simple_group_role_mapping) | A list of LDAP group names - MySQL role pairs |
| [authentication_ldap_simple_group_search_attr](#authentication_ldap_simple_group_search_attr) | Name of the attribute that specifies the group names in the LDAP directory entries |
| [authentication_ldap_simple_group_search_filter](#authentication_ldap_simple_group_search_filter) | Custom group search filter |
| [authentication_ldap_simple_init_pool_size](#authentication_ldap_simple_init_pool_size) | Initial size of the connection pool to the LDAP server |
| [authentication_ldap_simple_log_status](#authentication_ldap_simple_log_status) | logging level |
| [authentication_ldap_simple_max_pool_size](#authentication_ldap_simple_max_pool_size) | Maximum size of the pool of connections to the LDAP server |
| [authentication_ldap_simple_server_host](#authentication_ldap_simple_server_host) | LDAP server host |
| [authentication_ldap_simple_server_port](#authentication_ldap_simple_server_port) | LDAP server TCP/IP port number |
| [authentication_ldap_simple_ssl](#authentication_ldap_simple_ssl) | If plugin connections to the LDAP server use the SSL protocol (ldaps://) |
| [authentication_ldap_simple_tls](#authentication_ldap_simple_tls) | If plugin connections to the LDAP server are secured with STARTTLS (ldap://) |
| [authentication_ldap_simple_user_search_attr](#authentication_ldap_simple_user_search_attr) | Name of the attribute that specifies user names in the LDAP directory entries |

The following variables are described in detail:

### `authentication_ldap_sasl_bind_base_dn`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --authentication-ldap-sasl-bind-base-dn=value |
| Scope        | Global                                          |
| Dynamic      | Yes                                              |
| Data type    | String                                          |
| Default      | NULL                                            |

The base distinguished name (DN) for SASL-based LDAP authentication. You can limit the search scope by using the variable as the base of the search.

### `authentication_ldap_sasl_bind_root_dn`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --authentication-ldap-sasl-bind-root-dn=value |
| Scope        | Global                                          |
| Dynamic      | Yes                                              |
| Data type    | String                                          |
| Default      | NULL                                            |

The `root` distiguished name (DN) used to authenticate SASL-based LDAP. When performing a search, this variable is used with
`authentication_ldap_sasl_bind_root_pwd` as the authenticating credentials to the LDAP server.

### `authentication_ldap_sasl_bind_root_pwd`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --authentication-ldap-sasl-bind-root-pwd=value |
| Scope        | Global                                           |
| Dynamic      | Yes                                               |
| Data type    | String                                           |
| Default      | NULL                                             |

The `root` password used to authenticate against SASL-based LDAP server. This variable is used with
[`authentication_ldap_sasl_bind_root_dn`](#authentication_ldap_sasl_bind_root_dn).

### `authentication_ldap_sasl_ca_path`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-ca_path=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | NULL                                       |

The certificate authority’s absolute path used to verify the LDAP certificate.

### `authentication_ldap_sasl_fallback_server_host`

| Option | Description |
|---|---|
| Command-line | --authentication-ldap-sasl-fallback-server-host |
| Scope | Global |
| Dynamic | Yes |
| Type | Sting |
| Default | NULL |

Use with [`authentication_ldap_sasl_fallback_server_port`](#authentication_ldap_sasl_fallback_server_port).

If the primary server is unavailable, the authentication plugin attempts to connect to the fallback server and authenticate using that server.

### `authentication_ldap_sasl_fallback_server_port`

| Option | Description |
|---|---|
| Command-line | --authentication-ldap-sasl-fallback-server-port |
| Scope | Global |
| Dynamic | Yes |
| Type | Integer |
| Default | NULL |

Use with [`authentication_ldap_sasl_fallback_server_host`](#authentication_ldap_sasl_fallback_server_host).

If the primary server is unavailable, the authentication plugin attempts to connect to the fallback server and authenticate using that server.

If the fallback server host has a value, and the fallback port is 0, users can specify multiple fallback servers.

Use this format to specify multiple fallback servers: `authentication_ldap_sasl_fallback_server_host="ldap(s)://host:port,ldap(s)://host2:port2`, for example.

### `authentication_ldap_sasl_group_role_mapping`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-group-role-mapping=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | Null                                       |

When an LDAP user logs in, the server checks if the LDAP user is a member of the specified group. If the user is, then the server automatically grants the database server roles to the user.

The variable has this format: `<ldap_group>=<mysql_role>,<ldap_group2>=<mysql_role2>,`.

### `authentication_ldap_sasl_group_search_attr`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-group-search-attr=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | cn                                       |

The attribute name that specifies group names in the LDAP directory entries for SASL-based LDAP authentication.  

### `authentication_ldap_sasl_group_search_filter`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-group-search-filter=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | (\|(&(objectClass=posixGroup)(memberUid=%s))(&(objectClass=group)(member=%s)))                                       |

The custom group search filter for SASL-based LDAP authentication.

### `authentication_ldap_sasl_init_pool_size`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-init-pool-size=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | Integer                                     |
| Default      | 10                                       |
| Minimum value | 0 |
| Maximum value | 32767 |
| Unit | connections |

The initial size of the connection pool to the LDAP server for SASL-based LDAP authentication.

### `authentication_ldap_sasl_log_status`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-log-status=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | Integer                                     |
| Default      | 1                                       |
| Minimum value | 1 |
| Maximum value | 6 |

The logging level for messages written to the error log for SASL-based LDAP authentication.

### `authentication_ldap_sasl_max_pool_size`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-sasl-max-pool-size=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | Integer                                     |
| Default      | 1000                                       |
| Minimum value | 0 |
| Maximum value | 32767 |
| Unit | connections |

The maximum connection pool size to the LDAP server in SASL-based LDAP authentication. The variable is used with [`authentication_ldap_sasl_init_pool_size`](#authentication_ldap_sasl_init_pool_size).

### `authentication_ldap_sasl_server_host`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --authentication-ldap-sasl-server-host=value |
| Scope        | Global                                         |
| Dynamic      | Yes                                             |
| Data type    | String                                         |
| Default      | NULL                                           |

The LDAP server host used for SASL-based LDAP authentication.  The LDAP server host can be an IP address or a host name.

### `authentication_ldap_sasl_server_port`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --authentication-ldap-sasl-server-port=value |
| Scope        | Global                                         |
| Dynamic      | Yes                                             |
| Data type    | Integer                                         |
| Default      | 389                                           |
| Minimum value | 1 |
| Maximum value | 32376 |

The LDAP server TCP/IP port number used for SASL-based LDAP authentication.

### `authentication_ldap_sasl_ssl`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-sasl-ssl=value |
| Scope        | Global                                 |
| Dynamic      | Yes                                     |
| Data type    | Boolean                                 |
| Default      | OFF                                   |

If this variable is enabled, the plugin connects to the server with SSL.

### `authentication_ldap_sasl_tls`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-sasl-tls=value |
| Scope        | Global                                 |
| Dynamic      | Yes                                     |
| Data type    | Boolean                                 |
| Default      | OFF                                   |

If this variable is enabled, the plugin connects to the server with TLS.

### `authentication_ldap_sasl_user_search_attr`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-sasl-user-search-attr=value |
| Scope        | Global                                 |
| Dynamic      | Yes                                     |
| Data type    | String                                 |
| Default      | uid                                   |

The attribute name that specifies the user names in LDAP directory entries in SASL-based LDAP authentication.

### `authentication_ldap_simple_bind_base_dn`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --authentication-ldap-simple-bind-base-dn=value |
| Scope        | Global                                          |
| Dynamic      | Yes                                              |
| Data type    | String                                          |
| Default      | NULL                                            |

The base distinguished name (DN) for simple LDAP authentication. You can limit the search scope by using the variable as the base of the search.

### `authentication_ldap_simple_bind_root_dn`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --authentication-ldap-simple-bind-root-dn=value |
| Scope        | Global                                          |
| Dynamic      | Yes                                              |
| Data type    | String                                          |
| Default      | NULL                                            |

The `root` distinguished name (DN) used to authenticate simple LDAP. When performing a search, this variable is used with
`authentication_ldap_simple_bind_root_pwd` as the authenticating credentials to the LDAP server.

### `authentication_ldap_simple_bind_root_pwd`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --authentication-ldap-simple-bind-root-pwd=value |
| Scope        | Global                                           |
| Dynamic      | Yes                                               |
| Data type    | String                                           |
| Default      | NULL                                             |

The `root` password used to authenticate against simple LDAP server. This variable is used with
[`authentication_ldap_simple_bind_root_dn`](#authentication_ldap_simple_bind_root_dn).

### `authentication_ldap_simple_ca_path`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-ca_path=value |
| Scope        | Global                                     |
| Dynamic      | Yes                                         |
| Data type    | String                                     |
| Default      | NULL                                       |

The certificate authority’s absolute path used to verify the LDAP certificate.

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

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --authentication-ldap-simple-server-host=value |
| Scope        | Global                                         |
| Dynamic      | Yes                                             |
| Data type    | String                                         |
| Default      | NULL                                           |

The LDAP server host used for simple LDAP authentication.  The LDAP server host can be an IP address or a host name.

### `authentication_ldap_simple_server_port`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --authentication-ldap-simple-server-port=value |
| Scope        | Global                                         |
| Dynamic      | Yes                                             |
| Data type    | Integer                                         |
| Default      | 389                                           |
| Minimum value | 1 |
| Maximum value | 32376 |

The LDAP server TCP/IP port number used for simple LDAP authentication.

### `authentication_ldap_simple_ssl`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-simple-ssl=value |
| Scope        | Global                                 |
| Dynamic      | Yes                                     |
| Data type    | Boolean                                 |
| Default      | OFF                                   |

If this variable is enabled, the plugin connects to the server with SSL.

### `authentication_ldap_simple_tls`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-simple-tls=value |
| Scope        | Global                                 |
| Dynamic      | Yes                                     |
| Data type    | Boolean                                 |
| Default      | OFF                                   |

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

[8.0.30-22-RN]: ./docs/release-notes//release-notes/8.0.30-22.md
