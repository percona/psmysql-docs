# Authentication methods

An authentication method is a way to verify the identity of a user trying to access the database. The method defines how the server checks credentials and whether the user can connect.

## Version changes

Percona Server for MySQL {{vers}} follows MySQL 9.x authentication rules.

* The `mysql_native_password` plugin is removed in MySQL 9.x. The server does not offer `--mysql-native-password=ON`, `mysql_native_password=ON`, or any other way to load the `mysql_native_password` plugin on {{vers}}.
* The `default_authentication_plugin` system variable is not used in MySQL 9.x.
* Password-based authentication for new accounts uses `caching_sha2_password` by default.

Upgrading from 8.4 LTS: On 8.4 LTS, `mysql_native_password` was disabled by default but could still be enabled for compatibility. Before cutover to {{vers}}, inventory accounts and clients that rely on native password authentication, migrate them to `caching_sha2_password` (or another supported plugin), and verify connector support. See [Upgrade checklist for {{vers}}](upgrade-checklist-9.7.md) and [Use an APT repository to install Percona Server for MySQL](apt-repo.md) (configure authentication during package install).

## Common Authentication Methods


| Method                              | Description                                                                                                                                                                                   |
|-------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Caching SHA-2 Pluggable Authentication | Uses SHA-256 for password hashing. The server compares a hash of the supplied password to the stored hash and caches authentication data for performance. `caching_sha2_password` is the default for password authentication on {{vers}}. Older MySQL client libraries may not support `caching_sha2_password` without an upgrade. Use TLS for network connections when your policy requires encryption. |
| MySQL Native Authentication      | Not available on MySQL 9.x or on {{vers}} (plugin removed). On older MySQL and Percona Server releases only: SHA-1-based hashing, wide legacy compatibility, weak by modern standards.                                                                                                                                                |
| PAM Pluggable Authentication     | Integrates MySQL with Linux's Pluggable Authentication Modules (PAM). MySQL relies on the operating system for authentication, allowing various mechanisms. Useful where centralized OS-level authentication is required; setup can be complex.       |
| LDAP Authentication              | MySQL connects to an LDAP server to authenticate users. Suited to large, distributed setups and directory-backed identity; maintaining LDAP adds operational overhead.              |
| Kerberos Authentication          | Uses the Kerberos protocol. Strong security and single sign-on in enterprise environments; requires Kerberos infrastructure.                                                              |
| FIDO Pluggable Authentication    | Supports FIDO devices for strong authentication. Common in high-assurance environments; needs compatible hardware and client support.                                                          |
| Auth Socket Authentication       | Uses OS socket-based authentication, matching the connecting OS user to the server process user. Useful for local administration; not a substitute for remote multi-user password policies.        |