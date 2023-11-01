# Security & account management changes in MySQL 8.0

The grant tables in the mysql system database are now InnoDB (transactional) tables.

A new `caching_sha2_password` authentication plugin is available. Like the `sha256_password` plugin, `caching_sha2_password` implements SHA-256 password hashing, but uses caching to address latency issues at connect time.

MySQL now supports roles, which are named collections of privileges. Roles can be created and dropped. Roles can have privileges granted to and revoked from them. Roles can be granted to and revoked from user accounts.

MySQL now incorporates the concept of user account categories, with system and regular users distinguished according to whether they have the `SYSTEM_USER` privilege.

MySQL now maintains information about password history, enabling restrictions on reuse of previous passwords.

MySQL now supports `FIPS` mode, if compiled using OpenSSL, and an OpenSSL library and FIPS Object Module are available at runtime.

MySQL now enables administrators to configure user accounts such that too many consecutive login failures due to incorrect passwords cause temporary account locking.

As of MySQL 8.0.27, MySQL supports multi-factor authentication (MFA), which makes it possible to create accounts that have up to three authentication methods.

