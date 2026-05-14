# Authentication methods

An authentication method is a way to verify the identity of a user trying to access the database. It defines how the server checks if the credentials provided are correct and whether the user can connect.

## Version changes

MySQL 8.4 disables the deprecated `mysql_native_password` authentication plugin by default.

Enable the `mysql_native_password` plugin explicitly. Use one of the following configuration methods:

* Add the `--mysql-native-password=ON` option when starting the MySQL server.

* Edit your MySQL configuration file. In the `[mysqld]` section, add the line `mysql_native_password=ON`.

Either option re-enables the plugin for backward compatibility. Adopt a stronger authentication method whenever possible.

## Common Authentication Methods


| Method                              | Description                                                                                                                                                                                   |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Caching SHA-2 Pluggable Authentication | Uses SHA-256 for password hashing. MySQL hashes the user's password and compares it to the stored hash. It caches authentication data for better performance. Suitable for modern setups with strong security and performance. However, it may not work with older MySQL clients. |
| MySQL Native Authentication      | An older method that uses SHA-1 for password hashing. It offers wide compatibility, making it useful for legacy systems or applications that don't support newer methods. However, it has reduced security and is best avoided unless necessary for compatibility.                |
| PAM Pluggable Authentication     | Integrates MySQL with Linux's Pluggable Authentication Modules (PAM). MySQL relies on the operating system for authentication, allowing for various authentication mechanisms. Useful in environments needing centralized authentication management, but setup can be complex.       |
| LDAP Authentication              | MySQL connects to an LDAP server to authenticate users. Ideal for managing large, distributed systems, enabling centralized user management, and integrating with existing directory services. The main drawback is the added complexity of maintaining an LDAP server.              |
| Kerberos Authentication          | Uses the Kerberos protocol for authentication. Provides strong security and single sign-on across multiple services. Common in enterprise environments but requires a complex Kerberos infrastructure.                                                              |
| FIDO Pluggable Authentication    | Supports FIDO (Fast IDentity Online) authentication devices. Used in high-security environments for robust two-factor authentication. Requires special hardware like security keys and may face user resistance.                                                          |
| OpenID Connect Authentication    | Authenticates users with signed JSON Web Tokens (JWTs) from an external Identity Provider. Supported providers include Keycloak, Okta, and Microsoft Entra ID. Suitable for organizations that already operate a central identity service and want password-less, single-sign-on access to MySQL. Requires a secure connection (TLS, socket, or shared memory). Supports group-to-role mapping and group-based proxy users. |
| Auth Socket Authentication       | Uses the operating system's socket-based authentication, matching the connecting user with the system user that owns the MySQL process. Ideal for local administrative access but limited to local machine use and not suitable for remote or multi-user environments.        |

