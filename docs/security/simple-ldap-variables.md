# Simple LDAP Variables

The following variables are static and can only be changed at runtime.


| Name                                     | Command Line | Dynamic | Scope  |
|------------------------------------------|--------------|---------|--------|
| [authentication_ldap_simple_bind_root_dn](#authentication_ldap_simple_bind_root_dn)  | Yes          | No      | Global |
| [authentication_ldap_simple_bind_root_pwd](#authentication_ldap_simple_bind_root_pwd) | Yes          | No      | Global |
| [authentication_ldap_simple_ca_path](#authentication_ldap_simple_ca_path)       | Yes          | No      | Global |
| [authentication_ldap_simple_server_host](#authentication_ldap_simple_server_host)   | Yes          | No      | Global |
| [authentication_ldap_simple_server_port](#authentication_ldap_simple_server_port)   | Yes          | No      | Global |
| [authentication_ldap_simple_ssl](#authentication_ldap_simple_ssl)           | Yes          | No      | Global |
| [authentication_ldap_simple_tls](#authentication_ldap_simple_tls)           | Yes          | No      | Global |


## `authentication_ldap_simple_bind_root_dn`

| Option       | Description                                     |
|--------------|-------------------------------------------------|
| Command-line | --authentication-ldap-simple-bind-root-dn=value |
| Scope        | Global                                          |
| Dynamic      | No                                              |
| Data type    | String                                          |
| Default      | Null                                            |

The `root` credential used to authenticate against an LDAP. This variable is used with
`authentication_ldap_simple_bind_root_pwd`.

## `authentication_ldap_simple_bind_root_pwd`

| Option       | Description                                      |
|--------------|--------------------------------------------------|
| Command-line | --authentication-ldap-simple-bind-root-pwd=value |
| Scope        | Global                                           |
| Dynamic      | No                                               |
| Data type    | String                                           |
| Default      | Null                                             |

The `root` password used to authenticate against an LDAP. This variable is used with
`authentication_ldap_simple_bind_root_dn`.

## `authentication_ldap_simple_ca_path`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --authentication-ldap-simple-ca_path=value |
| Scope        | Global                                     |
| Dynamic      | No                                         |
| Data type    | String                                     |
| Default      | Null                                       |

The certificate authority’s absolute path used to verify the LDAP certificate.

## `authentication_ldap_simple_server_host`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --authentication-ldap-simple-server-host=value |
| Scope        | Global                                         |
| Dynamic      | No                                             |
| Data type    | String                                         |
| Default      | Null                                           |

The LDAP server host used for LDAP authentication.

## `authentication_ldap_simple_server_port`

| Option       | Description                                    |
|--------------|------------------------------------------------|
| Command-line | --authentication-ldap-simple-server-port=value |
| Scope        | Global                                         |
| Dynamic      | No                                             |
| Data type    | String                                         |
| Default      | Null                                           |

The LDAP server TCP/IP port number used for LDAP authentication.

## `authentication_ldap_simple_ssl`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-simple-ssl=value |
| Scope        | Global                                 |
| Dynamic      | No                                     |
| Data type    | String                                 |
| Default      | Null                                   |

If this variable is enabled, the plugin connects to the server with SSL.

## `authentication_ldap_simple_tls`

| Option       | Description                            |
|--------------|----------------------------------------|
| Command-line | --authentication-ldap-simple-tls=value |
| Scope        | Global                                 |
| Dynamic      | No                                     |
| Data type    | String                                 |
| Default      | Null                                   |

If this variable is enabled, the plugin connects to the server with TLS.

!!! admonition "See also"

    [Simple LDAP Authentication](https://dev.mysql.com/doc/mysql-security-excerpt/8.0/en/ldap-pluggable-authentication.html#ldap-pluggable-authentication-usage-simple)