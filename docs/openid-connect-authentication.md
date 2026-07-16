# OpenID Connect authentication

!!! tip

    To try OpenID Connect (OIDC) on one server, follow [Get started with OpenID Connect authentication](quickstart-openid-connect.md).

## What is OpenID Connect authentication?

OpenID Connect (OIDC) is an identity layer on top of the OAuth 2.0 framework. The user authenticates against an external Identity Provider (IDP) before the user connects to MySQL. Keycloak, Okta, and Microsoft Entra ID are supported providers.

The IDP issues a signed JSON Web Token (JWT). The IDP calls this token the Identity token. The client sends the token to Percona Server for MySQL during the authentication handshake. The server verifies the token and grants the connection. The server does not exchange a password.

See [Authentication methods](authentication-methods.md) for an overview of supported authentication methods. See [LDAP authentication](ldap-authentication.md), [PAM authentication](pam-plugin.md), and [FIDO authentication](fido-authentication-plugin.md) to compare OIDC with related plugins. See [SSL improvements](ssl-improvement.md) to configure the encrypted transport that OIDC requires.

## Plugin capabilities

The plugin provides the following capabilities:

* Verify signed Identity tokens from one or more configured IDPs

* Refresh signing keys from a JSON Web Key Set (JWKS) endpoint at runtime

* Apply an optional `aud` audience check for each IDP

* Map IDP group claims to MySQL roles for the session

* Proxy multiple IDP identities to one MySQL account through `GRANT PROXY`

* Accept the `RS256`, `RS384`, `RS512`, `ES256`, and `HS256` signature algorithms

Proxy support is a Percona-specific addition. The upstream MySQL OIDC plugin has no proxy support.

The server-side plugin works with the `authentication_openid_connect_client` client-side plugin in Percona Server for MySQL.

## Plugin and library file names

The library file must reside in the directory that the [`plugin_dir` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-variables.html#sysvar_plugin_dir) system variable names. The file name suffix can differ by platform.

The following table lists the plugin components:

| Plugin or file       | Name                                       |
|---|---|
| Server-side plugin   | `auth_openid_connect`                      |
| Client-side plugin   | `authentication_openid_connect_client`     |
| Server library file  | `auth_openid_connect.so`                   |
| Client library file  | `authentication_openid_connect_client.so`  |

## How does OpenID Connect authentication work?

The plugin processes a connection in the following sequence:
{.power-number}

1. The user authenticates against the IDP through an out-of-band flow. The IDP returns a JWT Identity token.

2. The user writes the token to a file. The operating system account that runs the client must be able to read the file. The token must not exceed 10 KB.

3. The client reads the token file from the `--authentication-openid-connect-client-id-token-file` option. See [Connect with a client](#connect-with-a-client) for the option syntax. The client checks that the file contains a well-formed JWT.

4. The client checks that the connection uses TLS, a Unix domain socket, or shared memory. The client rejects plaintext TCP.

5. The client sends the token to the server during the authentication handshake.

6. The server checks that the connection is secure. The server receives and decodes the token.

7. The server validates the token against the configuration for the referenced IDP.

The plugin accepts the token only when every check in the following table passes:

| Check                    | Requirement                                                                          |
|---|---|
| JWT structure            | Valid JWT                                                                            |
| Signature algorithm      | One of `RS256`, `RS384`, `RS512`, `ES256`, or `HS256`                                |
| Signature                | Matches a configured public key through the `kid` header                             |
| Expiration (`exp` claim) | Timestamp in the future                                                              |
| Issuer (`iss` claim)     | Matches the configured `issuer-name` for the IDP                                     |
| Subject (`sub` claim)    | Matches the `user` value when `IDENTIFIED ... AS` includes `user` (direct authentication only) |
| Audience (`aud` claim)   | Matches an allowed audience when `audiences` is configured                           |

The plugin selects the authentication mode from the fields present in the account's `IDENTIFIED ... AS` JSON:

| Fields in the `AS` JSON              | Mode                  | The plugin authenticates as                       |
|---|---|---|
| `identity_provider`, `user`          | Direct authentication | The handshake account (no proxying)               |
| `identity_provider`, `group`         | Named-group proxying  | The literal value of `group`                      |
| `identity_provider` only             | Anonymous proxying    | The first entry in the token's `groups` claim     |

Direct authentication verifies the `sub` claim against `user`. Proxy modes verify group membership instead.

Both proxy modes require `group-claim`. The plugin reads group membership from the token through this key.

In named-group proxying, the plugin checks that the configured `group` value appears in the claim. The session authenticates as the proxied account for that group.

In anonymous proxying, the plugin uses the first claim entry as the proxied account.

The proxying account must hold `PROXY` privilege on the proxied account. See [Proxying](#proxying) for end-to-end examples and safety notes for proxy modes.

When both `group-claim` and `group-role` are configured, the plugin reads the group claim from the token. The plugin grants the connection any matching MySQL roles for the session.

The plugin rejects the connection when any check fails. The plugin writes a diagnostic message to the server error log.

The plugin validates the token at connection time only. A connection stays open after the token expires during the session.

## Prerequisites

Before you configure OpenID Connect authentication, gather the resources in the following table:

| Resource              | Description                                                                                       |
|---|---|
| Identity Provider     | OIDC-compliant IDP that issues signed Identity tokens                                             |
| IDP issuer URL        | Issuer URL plus a JWKS endpoint or static public keys as JWKs                                     |
| Secure transport      | TLS or a Unix domain socket between client and server                                             |
| Token delivery method | Script or tool that calls the IDP token endpoint and writes tokens to a file                     |

Percona tested the plugin with Keycloak. Any IDP with a standard JWKS endpoint is compatible.

## Install the plugin

`INSTALL PLUGIN` requires the `INSERT` privilege on `mysql.plugin`. Editing `my.cnf` requires file-system access on the server host.

Choose one of the following installation methods:

=== "Load the plugin at runtime"

    Run this statement to load the plugin during a session:

    ```sql
    INSTALL PLUGIN auth_openid_connect SONAME 'auth_openid_connect.so';
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Query OK, 0 rows affected (0.01 sec)
        ```

=== "Load the plugin at server start"

    Add the following lines to the `[mysqld]` section of `my.cnf`:

    ```text
    [mysqld]
    plugin-load-add=auth_openid_connect.so
    ```

    Restart the server for the change to take effect.

### Verify the installation

Run the [`SHOW PLUGINS` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/show-plugins.html) statement. You can also query `INFORMATION_SCHEMA.PLUGINS`. Confirm that the plugin loaded successfully:

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS
FROM INFORMATION_SCHEMA.PLUGINS
WHERE PLUGIN_NAME = 'auth_openid_connect';
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+---------------+
    | PLUGIN_NAME         | PLUGIN_STATUS |
    +---------------------+---------------+
    | auth_openid_connect | ACTIVE        |
    +---------------------+---------------+
    1 row in set (0.00 sec)
    ```

When `PLUGIN_STATUS` is not `ACTIVE`, or when the query returns no rows, the plugin failed to load. Check the server error log for the cause.

### Register the update_jwks() UDF

The plugin library also provides the `update_jwks()` user-defined function (UDF). Register the function once after the plugin loads. The UDF refreshes cached JWKS public keys at runtime. See [Refresh JWKS keys](#refresh-jwks-keys) for details.

```sql
CREATE FUNCTION update_jwks RETURNS INTEGER
SONAME 'auth_openid_connect.so';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

Confirm the function is registered:

```sql
SELECT * FROM mysql.func WHERE name = 'update_jwks';
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------+-----+------------------------+----------+
    | name        | ret | dl                     | type     |
    +-------------+-----+------------------------+----------+
    | update_jwks |   2 | auth_openid_connect.so | function |
    +-------------+-----+------------------------+----------+
    1 row in set (0.00 sec)
    ```

When the query returns no rows, the function did not register. Check the server error log for the cause.

## Configure the plugin

The plugin reads trusted IDPs from one JSON document. The administrator supplies the document through the `auth_openid_connect_configuration` system variable. The variable accepts the document inline or as a path to a file.

`SET GLOBAL` requires the `SYSTEM_VARIABLES_ADMIN` privilege. `SET PERSIST_ONLY` also requires `PERSIST_RO_VARIABLES_ADMIN`.

### Configuration schema

Each top-level key in the JSON document is an IDP name. User accounts reference this name in the `IDENTIFIED ... AS` clause. Each IDP entry is a JSON object.

| Key | Required | Purpose |
|---|---|---|
| `audiences` | No | Limit accepted `aud` claim values |
| `group-claim` | No | Name of the JWT claim that lists groups |
| `group-role` | No | Map IDP groups to MySQL roles |
| `issuer-name` | Yes | Expected `iss` claim value from the IDP |
| `jwks-url` | When `keys` is absent | URL to fetch signing keys |
| `keys` | When `jwks-url` is absent | Static signing keys as JWK objects |

#### Field details

#### `audiences`

* Array of allowed `aud` claim values

* The plugin rejects tokens when the `aud` claim does not match

* When this key is absent, the plugin skips the audience check

#### `group-claim`

* Name of the JWT claim that lists group memberships, such as `groups`

* The claim value must be a string or an array of strings

#### `group-role`

* Array of single-key objects that map IDP group names to MySQL role names

* Use this key with `group-claim`

#### `issuer-name`

* Exact value of the `iss` claim that the IDP issues

* The plugin matches this value to the token `iss` claim

#### `jwks-url`

* HTTPS URL of the IDP JWKS endpoint

* The plugin fetches and caches keys from the URL

* The plugin refreshes keys at runtime through the `update_jwks()` UDF

* HTTP URLs work for testing only and emit a warning

#### `keys`

* Array of JSON Web Key (JWK) objects that verify token signatures

* Each entry must include `kty` (`RSA` or `EC`), `kid`, and algorithm-specific parameters

* RSA keys require `n` and `e`

* EC keys require `crv`, `x`, and `y`

!!! tip

    Use `jwks-url` in production. IDPs rotate signing keys on a schedule. With `jwks-url`, the plugin fetches current keys without a configuration change.

    Use `keys` only when `jwks-url` is impractical:

    * The IDP has no JWKS endpoint

    * The server cannot reach the JWKS endpoint

    For outbound traffic through a corporate forward proxy, see [Route JWKS traffic through an HTTP proxy](#route-jwks-traffic-through-an-http-proxy).

### Set the configuration variable

The system variable `auth_openid_connect_configuration` accepts a string with one of the following prefixes:

* `JSON://` followed by inline configuration JSON

* `FILE://` followed by an absolute path to a configuration file

The prefix check is case-insensitive. A value without a recognized prefix returns `ERROR 1231 (42000)`.

The same error applies when the file cannot be read or parsed. Detailed messages appear in the server error log.

#### Example configuration

The following JSON document configures two trusted IDPs. The first IDP resolves keys at runtime through a `jwks-url`. The second IDP uses static `keys` to verify token signatures.

The `n` value is truncated. Replace `ptR4...QEASRw` with the full base64url-encoded RSA modulus from the IDP signing key.

```json
{
  "my-keycloak": {
    "issuer-name": "https://keycloak.example.com/realms/master",
    "jwks-url": "https://keycloak.example.com/realms/master/protocol/openid-connect/certs",
    "audiences": [ "mysql-oidc" ],
    "group-claim": "groups",
    "group-role": [
      { "/accounting": "accounting" },
      { "/marketing": "marketing" }
    ]
  },
  "oidc-idp": {
    "issuer-name": "https://idp.example.com/realms/dummy",
    "keys": [
      {
        "kid": "rsa-key-1",
        "kty": "RSA",
        "n": "ptR4YxjdrF2RrYiY9XYH3KcXKzlS6b2foGAeHN9dViAs5y...QEASRw",
        "e": "AQAB",
        "use": "sig",
        "alg": "RS256"
      }
    ],
    "audiences": [
      "ee2811b9-10b8",
      "https://api.example.com"
    ],
    "group-claim": "groups",
    "group-role": [
      { "acc": "accounting" },
      { "eng": "engineering" }
    ]
  }
}
```

Load the document into the `auth_openid_connect_configuration` system variable in one of the following ways:

#### Configure in my.cnf

Most deployments set the variable in `my.cnf`. The configuration then applies on every server start.

Save the example as `/etc/mysql/oidc/idps.json`. Add the variable to the `[mysqld]` section with the plugin load directive:

```text
[mysqld]
plugin-load-add=auth_openid_connect.so
auth_openid_connect_configuration='FILE:///etc/mysql/oidc/idps.json'
```

The `plugin-load-add` line matches the option in [Install the plugin](#install-the-plugin).

The variable accepts the same prefixes: `FILE://` for an external file or `JSON://` for an inline document. Inline JSON in `my.cnf` requires careful quote escaping. Use the `FILE://` form for `my.cnf` deployments.

The variable also accepts a `--auth_openid_connect_configuration` command-line argument when you start `mysqld` directly. Use this form for scripted automation.

Restart the server for the change to take effect.

#### Configure from a file

To set the variable in a running server, use `SET GLOBAL` with the `FILE://` prefix:

```sql
SET GLOBAL auth_openid_connect_configuration =
  'FILE:///etc/mysql/oidc/idps.json';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

#### Configure inline

To set the variable in a running server without an external file, use `SET GLOBAL` with the `JSON://` prefix:

```sql
SET GLOBAL auth_openid_connect_configuration =
  'JSON://{"my-keycloak":{"issuer-name":"https://keycloak.example.com/realms/master","jwks-url":"https://keycloak.example.com/realms/master/protocol/openid-connect/certs","audiences":["mysql-oidc"]}}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

### Persist the configuration

!!! warning

    A `SET GLOBAL` assignment does not survive a server restart. Persist the configuration with `SET PERSIST_ONLY` or `my.cnf` to avoid an authentication outage after restart.

Skip this step when you already set the variable in [my.cnf](#configure-in-mycnf). The `my.cnf` value loads on every server start. You do not need `SET PERSIST_ONLY`.

Otherwise, persist the configuration with the following statement:

```sql
SET PERSIST_ONLY auth_openid_connect_configuration =
  'FILE:///etc/mysql/oidc/idps.json';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

## Create an individual user account

In direct authentication, one MySQL account maps to one user identity in the IDP. Encode the mapping as a JSON object in the `IDENTIFIED ... AS` clause:

```sql
CREATE USER 'mysql_oidc_user'@'%'
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak", "user": "4c28d537-a635-4b6d-957f-58e3c8860bcc"}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

The clause requires two fields:

* `identity_provider` must match a top-level key in `auth_openid_connect_configuration`.

* `user` must match the `sub` claim in the Identity tokens that the IDP issues for this user.

For Keycloak, the `sub` claim contains the user UUID. Other providers may use an email address or another stable identifier in the `sub` claim.

The server validates the JSON at connection time, not at user creation. The connection fails when either field is missing. The connection also fails when the configuration has no entry for the referenced IDP.

Grant privileges to the account with `GRANT`. Use the same process as for any other MySQL account.

When many IDP users share one MySQL account, see [Proxying](#proxying). One MySQL proxied account maps to one IDP group. IDP users in that group inherit the same privileges.

## Obtain an Identity token

The plugin requires the ID token from the IDP. The ID token is not the access token.

Production environments use the OAuth 2.0 flow that the IDP recommends. Authorization code with Proof Key for Code Exchange (PKCE) and device authorization are common choices.

The following example uses [Keycloak :octicons-link-external-16:](https://www.keycloak.org/securing-apps/oidc-layers) and the password grant. Replace placeholders with values from your IDP:

!!! warning "Password grant is for testing only"

    The password grant (`grant_type=password`) is deprecated in OAuth 2.1. Use this flow only for local automation, scripts, and internal testing.

    For production CLI clients, use the [Device Authorization Grant :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc8628) or authorization code with PKCE. These flows do not send user credentials to the client.

```bash
curl -s -X POST \
  https://keycloak.example.com/realms/master/protocol/openid-connect/token \
  -d 'grant_type=password' \
  -d 'client_id=mysql-oidc' \
  -d 'scope=openid' \
  -d 'username=alice' \
  -d 'password=<password>' \
  | jq -r .id_token > /run/user/1000/id_token.jwt

chmod 600 /run/user/1000/id_token.jwt
```

The `scope=openid` parameter is required. Without this parameter, the IDP returns an access token but no ID token. The `client_id` must reference a client registered in the IDP. The client must permit the grant type.

!!! note "Keycloak client configuration"

    For Keycloak, the ID token `aud` claim equals the `client_id`. Set `audiences` in the plugin configuration to match.

    The Keycloak token request uses `client_id=mysql-oidc`. Set `"audiences": ["mysql-oidc"]` in the configuration.

    Public clients send only the `client_id`. Confidential clients also require `client_secret`:

    ```bash
    -d 'client_secret=<CLIENT_SECRET>'
    ```

    Retrieve the secret from the Keycloak admin console under Clients > mysql-oidc > Credentials.

The file must contain only the raw compact-serialized JWT. The JWT has three base64url segments joined by dots. Do not add whitespace, a JSON wrapper, or a `Bearer ` prefix.

For other IDPs, see the vendor documentation:

* [Okta token endpoint :octicons-link-external-16:](https://developer.okta.com/docs/reference/api/oidc/#token)

* [Microsoft Entra ID OAuth 2.0 token endpoint :octicons-link-external-16:](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)

## Connect with a client

The client locates the Identity token file through the `--authentication-openid-connect-client-id-token-file` option. The client must supply the token through this option only. The client does not read an environment variable.

Pass the option on the command line:

```bash
mysql --host=mysql.example.com \
      --ssl-mode=REQUIRED \
      --user=mysql_oidc_user \
      --authentication-openid-connect-client-id-token-file=/run/user/1000/id_token.jwt
```

For persistent client configuration, set the option in the `[client]` section of `my.cnf`:

```ini
[client]
authentication-openid-connect-client-id-token-file=/run/user/1000/id_token.jwt
```

The MySQL client reads `[client]` at startup. A command-line value overrides the `my.cnf` value.

The client rejects authentication when any of the following conditions apply:

* The `--authentication-openid-connect-client-id-token-file` option is missing from both the command line and `my.cnf`.

* The token file is missing, empty, or larger than 10 KB.

* The token file does not contain a syntactically valid JWT.

* The connection between the client and server is not secured by TLS, a Unix socket, or shared memory.

## Map groups to MySQL roles

When both `group-claim` and `group-role` are configured for an IDP, the plugin reads the named claim at connection time. The plugin associates each matching MySQL role with the connection. Activate the role with [`SET ROLE` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/set-role.html).

The following configuration fragment maps two groups to two roles:

```json
"group-claim": "groups",
"group-role": [
  { "acc": "accounting" },
  { "eng": "engineering" }
]
```

When a token has the `groups` claim with the value `["acc", "hr"]`, the connection behaves as follows:

* `SET ROLE accounting` succeeds. The `acc` group maps to the `accounting` role.

* `SET ROLE engineering` fails. The token has no `eng` group.

* `SET ROLE hr` fails. The `hr` group has no role mapping.

<!-- External roles were not revoked is added based on a comment from [PS-11248](https://perconadev.atlassian.net/browse/PS-11248) -->

### Grant and revoke external roles at connection time

Percona Server maintains a container of external roles for each user account. External roles are MySQL roles that an authentication plugin grants at connection time.

At each connection, the server compares plugin roles to container roles:

* The server grants returned roles that are not yet in the container

* The server revokes external roles in the container that the plugin did not return

* The server updates the container to match session roles

The OIDC plugin reads group membership from the Identity token group claim. Configure the claim name with `group-claim`. Map groups to MySQL roles with `group-role`.

External role privileges apply at connection time only. Percona Server does not sync with the IDP between connections.

When an administrator removes a user from a group at the IDP, the user keeps external role privileges until the next connection. The next token must no longer contain the group.

Roles must already exist on the server. The plugin does not create roles.

The group claim must be a JSON array of strings or a single string. Other types fail authentication with `cannot parse groups claim in the token`.

!!! note "Keycloak claim shape"

    The plugin reads `group-claim` as a top-level token field. Nested claim paths such as `realm_access.roles` are unsupported.

    Keycloak stores realm roles in `realm_access.roles` and client roles in `resource_access.<client>.roles` by default. Add a Keycloak client scope mapper that emits a flat top-level claim:

    * For groups, add a `Group Membership` mapper with `Full group path` enabled

    * For realm roles, add a `User Realm Role` mapper with `Multivalued` enabled

    Set `Token Claim Name` to the `group-claim` value in the plugin configuration. See the Keycloak [Protocol Mappers :octicons-link-external-16:](https://www.keycloak.org/docs/latest/server_admin/#protocol) documentation for UI paths.

## Proxying

The plugin supports MySQL [proxy users :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/proxy-users.html). Multiple IDP identities can share one MySQL account. The proxy target comes from IDP group membership.

| Mode | Fields in `IDENTIFIED ... AS` | Proxy target |
|---|---|---|
| Named-group proxying | `identity_provider`, `group` | Value of `group` |
| Anonymous proxying | `identity_provider` only | First group in the token `groups` claim |

See [How does OpenID Connect authentication work?](#how-does-openid-connect-authentication-work) for how each mode is selected.

Proxying reduces administrative work when many IDP users connect to MySQL. One proxied account serves every IDP user in a group. DBAs do not maintain a MySQL account per user. This pattern matches common [LDAP authentication](ldap-authentication.md) deployments.

!!! warning

    Proxy modes do not verify the `sub` claim. The plugin accepts any token signed by a configured IDP that contains the required group. Use proxy modes only when group membership is the trust boundary.

Complete these steps before you configure proxy modes:

1. Configure the plugin and IDP. See [Configure the plugin](#configure-the-plugin).

2. Configure `group-claim` for the IDP entry. See [Map groups to MySQL roles](#map-groups-to-mysql-roles).

3. Confirm that tokens include the configured group claim.

Both proxy examples use the [`mysql_no_login` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/no-login-pluggable-authentication.html) plugin for proxy target accounts. Target accounts cannot authenticate directly.

### Named-group proxying

Use named-group proxying when one user belongs to multiple IDP groups. The user selects the group at connect time through the MySQL handshake account.

Complete these steps:

1. Create one handshake account per IDP group.

2. Create one `mysql_no_login` target account per group.

3. Grant `PROXY` from each handshake account to its target.

4. Grant privileges on the target accounts.

#### Step 1. Create handshake accounts

```sql
CREATE USER 'accounting'@'%'
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak", "group": "/accounting"}';

CREATE USER 'marketing'@'%'
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak", "group": "/marketing"}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 0 rows affected (0.01 sec)
    ```

#### Step 2 and 3. Create target accounts and grant PROXY

```sql
CREATE USER '/accounting'@'%' IDENTIFIED WITH 'mysql_no_login';
GRANT PROXY ON '/accounting'@'%' TO 'accounting'@'%';

CREATE USER '/marketing'@'%' IDENTIFIED WITH 'mysql_no_login';
GRANT PROXY ON '/marketing'@'%' TO 'marketing'@'%';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 0 rows affected (0.00 sec)
    ```

#### Step 4. Grant privileges on target accounts

Grant privileges on the target accounts with `GRANT`. Use the same process as for any other MySQL account.

#### Connect and verify

The token must include the chosen group in the `groups` claim. Select the group through the handshake account name:

```bash
mysql -u marketing \
      --authentication-openid-connect-client-id-token-file=id_token.jwt
```

Verify the proxied session:

```sql
SELECT USER(), CURRENT_USER();
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+----------------+
    | USER()              | CURRENT_USER() |
    +---------------------+----------------+
    | marketing@localhost | /marketing@%   |
    +---------------------+----------------+
    1 row in set (0.00 sec)
    ```

`USER()` returns the handshake account (`marketing`). `CURRENT_USER()` returns the proxied target (`/marketing@%`). The target account holds the session privileges.

### Anonymous proxying

Use anonymous proxying when the handshake username does not matter. The plugin selects the proxy target from the first group in the token `groups` claim.

!!! warning "Group ordering hazard"

    The plugin selects the proxy target from index 0 of the `groups` claim. The IDP controls claim order. A sort, an added group, or a policy change can shift index 0 without warning. The session then inherits a different proxy target.

    Use anonymous proxying only when one of these conditions applies:

    * Each IDP user belongs to exactly one privilege-bearing group

    * The IDP keeps the privileged group at index 0

    Otherwise, use [Named-group proxying](#named-group-proxying).

Complete these steps:

1. Create one anonymous handshake account.

2. Create one `mysql_no_login` target account per group.

3. Grant `PROXY` from the anonymous account to each target.

4. Grant privileges on the target accounts.

#### Step 1. Create the anonymous handshake account

```sql
CREATE USER ''@''
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak"}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

#### Step 2 and 3. Create target accounts and grant PROXY

```sql
CREATE USER '/accounting'@'%' IDENTIFIED WITH 'mysql_no_login';
GRANT PROXY ON '/accounting'@'%' TO ''@'';

CREATE USER '/marketing'@'%' IDENTIFIED WITH 'mysql_no_login';
GRANT PROXY ON '/marketing'@'%' TO ''@'';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 0 rows affected (0.00 sec)
    ```

#### Step 4. Grant privileges on target accounts

Grant privileges on the target accounts with `GRANT`. Use the same process as for any other MySQL account.

#### Connect and verify

Connect with any handshake username. The first group in the token selects the proxied target:

```bash
mysql -u anyname \
      --authentication-openid-connect-client-id-token-file=id_token.jwt
```

Verify the proxied session:

```sql
SELECT USER(), CURRENT_USER();
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------+----------------+
    | USER()            | CURRENT_USER() |
    +-------------------+----------------+
    | anyname@localhost | /marketing@%   |
    +-------------------+----------------+
    1 row in set (0.00 sec)
    ```

When a token has multiple groups, only the first group selects the target. Use named-group proxying to select the target explicitly.

## Refresh JWKS keys

When you configure an IDP with `jwks-url`, the plugin loads keys at startup. The plugin also reloads keys on every assignment to `auth_openid_connect_configuration`.

Keys can rotate at the IDP between configuration changes. The `update_jwks()` UDF refreshes cached keys without a configuration change. Register the UDF during plugin installation. See [Register the update_jwks() UDF](#register-the-update_jwks-udf).

The plugin does not refresh keys automatically. The plugin ignores HTTP cache headers such as `Cache-Control`, `Expires`, and `ETag`. Cached keys stay valid until a refresh trigger runs.

The plugin defines three refresh triggers:

* Server start with a configured `jwks-url`

* Assignment to `auth_openid_connect_configuration`

* A successful call to `update_jwks()`

Schedule the UDF when your IDP rotates keys on a fixed schedule. See [Schedule periodic refresh](#schedule-periodic-refresh) for an event-based example.

Call the UDF without arguments to refresh keys for every configured IDP that has a `jwks-url`:

```sql
SELECT update_jwks();
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------+
    | update_jwks() |
    +---------------+
    |             1 |
    +---------------+
    1 row in set (0.05 sec)
    ```

Call the UDF with one string argument to refresh a single IDP:

```sql
SELECT update_jwks('my-keycloak');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------+
    | update_jwks('my-keycloak')  |
    +-----------------------------+
    |                           1 |
    +-----------------------------+
    1 row in set (0.04 sec)
    ```

The following table lists the return values:

| Return value | Meaning |
|---|---|
| `>= 0` | Count of IDPs whose keys refreshed successfully |
| `-1` | Named IDP is not in the configuration |
| `-2` | Unexpected error during refresh. Details are in the server error log. |

### Schedule periodic refresh

Schedule the UDF to match the key rotation policy of the IDP. A MySQL event runs inside the server and needs no external tools. You can also use external tools such as `cron` or a Kubernetes CronJob.

The following event refreshes keys for every configured IDP once per hour:

```sql
CREATE EVENT update_oidc_keys
  ON SCHEDULE EVERY 1 HOUR
  DO SELECT update_jwks();
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

The event scheduler must run for the event to fire. Check and enable the scheduler at runtime:

```sql
SHOW VARIABLES LIKE 'event_scheduler';
SET GLOBAL event_scheduler = ON;
```

To enable the scheduler on every server start, set the variable in `my.cnf`:

```text
[mysqld]
event_scheduler=ON
```

The account that runs `CREATE EVENT` requires the `EVENT` privilege on the schema that holds the event.

Choose an interval that matches the key rotation schedule of the IDP. Hourly works for most deployments. Check the IDP documentation for the schedule.

### Route JWKS traffic through an HTTP proxy

The plugin fetches `jwks-url` content with libcurl. The plugin has no proxy options. The IDP configuration JSON has no proxy field.

Libcurl reads standard proxy environment variables from the mysqld process environment:

* `https_proxy` for HTTPS JWKS endpoints

* `http_proxy` for HTTP JWKS endpoints

* `no_proxy` for hostnames that bypass the proxy

The variables must reach mysqld, not the interactive shell that the DBA uses. On systemd systems, set the variables in the service unit:

```ini
[Service]
Environment="https_proxy=http://proxy.example.com:8080"
Environment="no_proxy=keycloak.internal,.example.lan,127.0.0.1"
```

After editing the unit, reload systemd and restart mysqld:

```bash
systemctl daemon-reload
systemctl restart mysqld
```

!!! warning "Restart required"

    The plugin reads the environment at process start. Updated proxy values apply only after you restart mysqld.

For environments that block all outbound traffic, configure each IDP with a static `keys` array instead of `jwks-url`. See [Configuration schema](#configuration-schema) for the required JWK fields. Copy the JWK set to the database host out of band.

## Uninstall the plugin

!!! warning

    Drop every UDF that depends on the plugin before you uninstall the plugin. When `UNINSTALL PLUGIN` runs while a UDF still references the library, a stale function definition remains. Drop scheduled events that call the UDF as well.

If you scheduled a refresh event, drop it first:

```sql
DROP EVENT IF EXISTS update_oidc_keys;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

Drop the UDF:

```sql
DROP FUNCTION IF EXISTS update_jwks;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

Uninstall the plugin:

```sql
UNINSTALL PLUGIN auth_openid_connect;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

## System variable reference

### auth_openid_connect_configuration

The following table summarizes the system variable. See [Percona Server system variables](percona-server-system-variables.md) for the full list.

| Variable name | Default value | Scope | Dynamic | Valid values |
|---|---|---|---|---|
| `auth_openid_connect_configuration` | `{}` | Global | Yes | A string prefixed with `JSON://` or `FILE://` |

The variable holds trusted OpenID Connect IDP configuration.

* Start the value with `JSON://` for inline JSON

* Start the value with `FILE://` for an absolute path to a JSON file

See [Configure the plugin](#configure-the-plugin) for the configuration schema.

Assign the variable with `SET GLOBAL`, `SET PERSIST_ONLY`, the `my.cnf` option file, or the `mysqld` command line. See [Set the configuration variable](#set-the-configuration-variable) for examples.

The plugin validates the variable at assignment. The server returns `ERROR 1231 (42000)` when the prefix is unknown, the JSON is malformed, or the file is unreadable.

The server accepts a configuration with an unreachable `jwks-url`. The plugin writes a warning to the server error log. Authentication against that IDP fails until the keys load. Run `update_jwks()` after the IDP becomes reachable.

## User-defined function reference

### update_jwks()

The following table summarizes the function:

| Property    | Value                       |
|---|---|
| Return type | `INTEGER`                   |
| Library     | `auth_openid_connect.so`    |
| Arguments   | Zero or one string          |

The function refreshes cached JWKS public keys for one IDP or for all configured IDPs. See [Refresh JWKS keys](#refresh-jwks-keys) for return values.

## Troubleshoot connection failures

The plugin writes one diagnostic line to the server error log for each rejected connection. The client receives a generic authentication failure. This behavior avoids leaking configuration details.

The following table lists common failures with symptoms, diagnosis, and solutions:

| Symptom | Diagnosis | Solution |
|---|---|---|
| `unsecure connection, use TLS, socket or memory` in the server log | Client connected over plaintext TCP | Reconnect with TLS, a Unix socket, or shared memory |
| `IDP not found: <name>` in the server log | `identity_provider` in `IDENTIFIED ... AS` does not match a configuration key | Align the user definition and configuration IDP names |
| `audience not authorized` in the server log | Token `aud` claim does not match `audiences` | Set `audiences` to match the token `aud` claim. For Keycloak, use the `client_id` value |
| `invalid sysvar prefix, expected FILE:// or JSON://` in the server log | `auth_openid_connect_configuration` has no valid prefix | Reset the variable with a `JSON://` or `FILE://` prefix |
| `JWKS configuration is insecure, use HTTPS` warning in the server log | `jwks-url` uses `http://` | Replace the URL with an `https://` endpoint |
| `JWKS: HTTP GET from <url> failed` in the server log | IDP is unreachable or returned a non-2xx status | Verify network reachability. See [Route JWKS traffic through an HTTP proxy](#route-jwks-traffic-through-an-http-proxy) for proxy egress. Run `update_jwks()` after recovery |
| `incorrect number of keys` in the server log | Token has no `kid` header and the IDP has multiple cached keys | Set `keys` to one entry that matches the IDP signing key |
| `user is not a member of the required group` in the server log | Named-group proxy account and token `groups` claim do not match | Verify group membership at the IDP or connect with a different handshake account |
