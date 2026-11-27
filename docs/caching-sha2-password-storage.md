# Caching SHA-2 password storage format

Introduced in Percona Server for MySQL 8.4.13-12, Percona Server for MySQL {{vers}} stores `caching_sha2_password` credentials in either of two formats.
The plugin name is `caching_sha2_password`.
The storage format controls how the server writes a new password hash to `mysql.user`.

See [Authentication methods](authentication-methods.md) for authentication plugin details.

## Storage formats

| Format          | Hash                     | Authentication string prefix | Default |
| --------------- | ------------------------ | ---------------------------- | ------- |
| `CRYPT5`        | SHA-256                  | `$A$`                        | Yes     |
| `PBKDF2_SHA512` | PBKDF2 with HMAC-SHA-512 | `$B$`                        | No      |

`CRYPT5` is the format from earlier {{vers}} releases.
Existing accounts retain that hash until the password changes.
A server restart does not rewrite stored hashes.

Characters after the prefix record the iteration count.
Three hexadecimal digits represent the value of [`caching_sha2_password_digest_rounds`](#caching_sha2_password_digest_rounds) divided by 1,000.
For example, `$A$005$` is a `CRYPT5` hash with 5,000 rounds, and `$B$00A$` is a `PBKDF2_SHA512` hash with 10,000 rounds.

List the format in use for each account with the following query:

```sql
SELECT User, Host, LEFT(authentication_string, 7) AS hash_prefix
FROM mysql.user
WHERE plugin = 'caching_sha2_password'
  AND authentication_string <> '';
```

A prefix of `$A$` indicates `CRYPT5`.
A prefix of `$B$` indicates `PBKDF2_SHA512`.

## Choose a format

`caching_sha2_password_storage_format` selects the format used by `CREATE USER`, `ALTER USER`, and `SET PASSWORD` for accounts using `caching_sha2_password`.
The variable is global.
A session `SET` fails.

Configure the global variable:

```sql
SET PERSIST caching_sha2_password_storage_format = 'PBKDF2_SHA512';
```

Configure the same setting in the option file:

```ini
[mysqld]
caching_sha2_password_storage_format = PBKDF2_SHA512
```

* `SET PERSIST` applies the value immediately and retains it across restarts.
* `SET PERSIST_ONLY` writes the value for the next restart and retains the current format on the running server.

Valid values are `CRYPT5` and `PBKDF2_SHA512`.
Any other value fails, and the current setting remains active.

After changing the format, update each account password so the server writes a new hash.
You can reuse the current password:

```sql
ALTER USER 'app'@'%' IDENTIFIED BY 'current-password';
```

`ALTER USER ... RETAIN CURRENT PASSWORD` stores the new password in the current format and retains the previous hash as the retained password.
The retained hash retains its original format.
Clients can authenticate with either password.
See [Dual passwords](#dual-passwords).

A replicated `CREATE USER` or `ALTER USER` stores the hash generated on the source.
The replica `caching_sha2_password_storage_format` does not rewrite that hash.
Configure the same format on every server that creates or rotates passwords.

## Enforce one format

`caching_sha2_password_enforce_storage_format` defaults to `OFF`.
With the default setting, an account logs in with either a `CRYPT5` hash or a `PBKDF2_SHA512` hash.

Configure the variable to `ON` after rotating passwords to the format named by `caching_sha2_password_storage_format`:

```sql
SET PERSIST caching_sha2_password_enforce_storage_format = ON;
```

When enforcement is active:

* A correct password stored in the configured format authenticates successfully and updates the authentication cache.

* A correct password stored in the alternative format expires the account password for the session.

* The client receives `ER_MUST_CHANGE_PASSWORD` until it executes `SET PASSWORD`.

* The server writes the new hash in the configured format.

To resolve an expired password:

1. Connect with a client option that permits expired passwords, such as the `mysql` client `--connect-expired-password` option.
2. Establish a connection that supports password transmission (Transport Layer Security (TLS), Unix socket, shared memory, or RSA key-pair exchange).
3. Execute the password update:

```sql
SET PASSWORD = 'current-password';
```

A successful full authentication with a hash in the configured format adds the account to the authentication cache.
Subsequent connections use the fast challenge-response exchange.
Hashes in alternative formats are excluded from the cache.
Logins using alternative formats require TLS, a Unix socket, shared memory, or RSA key-pair exchange.
Connections offering only the fast exchange fail.
`SET PASSWORD` writes a hash in the configured format and clears the cache entry.
The next full authentication repopulates the cache.

!!! warning "Rotate non-interactive accounts before enforcement"

    Application accounts, replication users, and connection pools cannot complete an interactive `SET PASSWORD` at login.
    Identify these accounts, update their passwords while enforcement is disabled, and confirm the hash prefix matches the configured format before enabling enforcement.

Enabling enforcement clears the in-memory authentication cache.
The next connection for each account uses full authentication until the account is cached again.

On a replica, enforcement uses the replica `caching_sha2_password_storage_format`, including for hashes replicated from the source.
Configure the same format on the source and every replica before enabling enforcement.

## Dual passwords

Each password (current and retained) has its own storage format.
With enforcement disabled, either password authenticates successfully.

With enforcement active, the server evaluates the presented password:

* A password in the configured format authenticates and populates the cache.
* A password in the alternative format expires the account password for that session.
* `SET PASSWORD` replaces the current hash and discards the retained password.

## Hash rounds

`caching_sha2_password_digest_rounds` defines the iteration count used when the server stores a new `caching_sha2_password` hash.
It applies to both `CRYPT5` and `PBKDF2_SHA512`.
The variable is global and dynamic.

The stored hash records `caching_sha2_password_digest_rounds / 1000` in three hexadecimal digits.
Configure a multiple of 1,000.
Values that are not a multiple of 1,000 truncate to the next lower multiple when the server writes the hash.
For example, 10,500 stores as 10,000 rounds.

Raising the iteration count increases the duration of password changes and the first full authentication after clearing the cache.
Connections hitting the authentication cache use the fast path and bypass this calculation.
Changing the variable clears the cache and retains existing stored hashes.

## System variables

### `caching_sha2_password_storage_format`

| Option       | Description                                    |
| ------------ | ---------------------------------------------- |
| Command-line | `--caching-sha2-password-storage-format=value` |
| Scope        | Global                                         |
| Dynamic      | Yes                                            |
| Data type    | Enumeration                                    |
| Default      | `CRYPT5`                                       |
| Valid values | `CRYPT5`, `PBKDF2_SHA512`                      |

Storage format for new `caching_sha2_password` hashes.
Changing the value clears the authentication cache.

### `caching_sha2_password_enforce_storage_format`

| Option       | Description                                      |
| ------------ | ------------------------------------------------ |
| Command-line | `--caching-sha2-password-enforce-storage-format` |
| Scope        | Global                                           |
| Dynamic      | Yes                                              |
| Data type    | Boolean                                          |
| Default      | `OFF`                                            |

When `ON`, a `caching_sha2_password` account presenting a password stored in a format other than [`caching_sha2_password_storage_format`](#caching_sha2_password_storage_format) must change that password at login.
Changing the value clears the authentication cache.

### `caching_sha2_password_digest_rounds`

| Option       | Description                               |
| ------------ | ----------------------------------------- |
| Command-line | `--caching-sha2-password-digest-rounds=#` |
| Scope        | Global                                    |
| Dynamic      | Yes                                       |
| Data type    | Integer                                   |
| Default      | `5000`                                    |
| Minimum      | `5000`                                    |
| Maximum      | `4095000`                                 |

Number of hash rounds used when storing a `caching_sha2_password` hash.
Changing the value clears the authentication cache.
