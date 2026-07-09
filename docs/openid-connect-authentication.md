# OpenID Connect authentication

!!! tip

    Want to try OIDC end-to-end on a single server? Follow the [Get started with OpenID Connect authentication](quickstart-openid-connect.md) walkthrough. The sections that follow are the full reference.

## What is OpenID Connect authentication?

OpenID Connect (OIDC) is an identity layer on top of the OAuth 2.0 framework. The user authenticates against an external Identity Provider (IDP) before connecting to MySQL. Supported providers include Keycloak, Okta, and Microsoft Entra ID.

The IDP issues a signed JSON Web Token (JWT), called the Identity token. The client transmits the token to Percona Server for MySQL during the authentication handshake. The server verifies the token and grants the connection without exchanging a password.

For an overview of the supported authentication methods, see [Authentication methods](authentication-methods.md). To compare OIDC with related plugins, see [LDAP authentication](ldap-authentication.md), [PAM authentication](pam-plugin.md), and [FIDO authentication](fido-authentication-plugin.md). To configure the encrypted transport that OIDC requires, see [SSL improvements](ssl-improvement.md).

## Plugin capabilities

The plugin provides the following capabilities:

* Verify signed Identity tokens issued by one or more configured Identity Providers.

* Refresh signing keys from a JSON Web Key Set (JWKS) endpoint at runtime.

* Enforce an optional `aud` audience check per IDP.

* Map IDP group claims to MySQL roles for the duration of the session.

* Proxy multiple IDP identities to a single MySQL account through `GRANT PROXY`.

* Support the signature algorithms listed in [Supported signature algorithms](#supported-signature-algorithms).

Proxy support is a Percona-specific addition. The upstream MySQL OIDC plugin does not include this capability.

The server-side plugin pairs with the `authentication_openid_connect_client` client-side plugin distributed with Percona Server for MySQL.

### Supported signature algorithms

The plugin supports the following signature algorithms:

| Algorithm | Description |
|---|---|
| `RS256` | RSASSA-PKCS1-v1_5 with SHA-256 |
| `RS384` | RSASSA-PKCS1-v1_5 with SHA-384 |
| `RS512` | RSASSA-PKCS1-v1_5 with SHA-512 |
| `ES256` | ECDSA with SHA-256 |
| `ES384` | ECDSA with SHA-384 |
| `ES512` | ECDSA with SHA-512 |
| `PS256` | RSASSA-PSS with SHA-256 |
| `PS384` | RSASSA-PSS with SHA-384 |
| `PS512` | RSASSA-PSS with SHA-512 |

## Plugin and library file names

The library file must reside in the directory named by the [`plugin_dir` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-variables.html#sysvar_plugin_dir) system variable. The file name suffix may differ on your platform.

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

2. The user writes the token to a file readable by the operating system account that runs the client. The token must not exceed 10 KB.

3. The client reads the token file referenced by the `--authentication-openid-connect-client-id-token-file` option. See [Connect with a client](#connect-with-a-client) for the option syntax. The client validates that the file contains a well-formed JWT.

4. The client confirms the connection uses TLS, a Unix domain socket, or shared memory. The client refuses to send the token over plaintext TCP.

5. The client transmits the token to the server during the authentication handshake.

6. The server confirms the connection is secure. The server then receives and decodes the token.

7. The server validates the token against the configuration of the referenced IDP.

The plugin accepts the token only when every check in the following table passes:

| Check                    | Requirement                                                                          |
|---|---|
| JWT structure            | Parses as a valid JWT                                                                |
| Signature algorithm      | One of the supported signature algorithms (see [Supported signature algorithms](#supported-signature-algorithms)) |
| Signature                | Verified by a configured public key, selected by the `kid` header                    |
| Expiration (`exp` claim) | Timestamp in the future                                                              |
| Issuer (`iss` claim)     | Equals the configured `issuer-name` for the IDP                                      |
| Subject (`sub` claim)    | Equals the `user` value when `IDENTIFIED ... AS` includes a `user` field (direct authentication only) |
| Audience (`aud` claim)   | Matches an allowed audience when `audiences` is configured                           |

The plugin selects the authentication mode from the fields present in the account's `IDENTIFIED ... AS` JSON:

| Fields in the `AS` JSON              | Mode                  | The plugin authenticates as                       |
|---|---|---|
| `identity_provider`, `user`          | Direct authentication | The handshake account (no proxying)               |
| `identity_provider`, `group`         | Named-group proxying  | The literal value of `group`                      |
| `identity_provider` only             | Anonymous proxying    | The first entry in the token's `groups` claim     |

The `sub` claim is verified against `user` only in direct authentication. Proxy modes verify group membership instead.

Both proxy modes require `group-claim`, so the plugin can read group membership from the token. In named-group proxying, the plugin verifies that the configured `group` appears in the claim. The session then authenticates as the proxied account named after that group. In anonymous proxying, the plugin uses the first entry in the claim as the proxied account.

The proxying account must hold `PROXY` privilege on the proxied account. For end-to-end examples and the safety considerations of proxy modes, see [Proxying](#proxying).

When `group-claim` and `group-role` are both configured, the plugin reads the group claim from the token. The plugin grants the connection any matching MySQL roles for the session.

The plugin denies the connection on any failed check. The plugin writes a diagnostic message to the server error log.

The plugin validates the token only at connection time. A connection remains active when the token expires later in the session.

## Prerequisites

Before you configure OpenID Connect authentication, gather the resources in the following table:

| Resource              | Description                                                                                       |
|---|---|
| Identity Provider     | OIDC-compliant IDP that issues signed Identity tokens                                             |
| IDP issuer URL        | URL plus either a JWKS endpoint or a static set of public keys exported as JWKs                   |
| Secure transport      | TLS or a Unix domain socket between the client and the server                                     |
| Token delivery method | Wrapper script or other tool that calls the IDP token endpoint and writes tokens to a file        |

The plugin has been tested with Keycloak. Any IDP that exposes a standard JWKS endpoint is compatible.

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

Run the [`SHOW PLUGINS` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/show-plugins.html) statement, or query `INFORMATION_SCHEMA.PLUGINS`. Confirm that the plugin loaded successfully:

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

A `PLUGIN_STATUS` value other than `ACTIVE`, or an empty result set, indicates that the plugin failed to load. Check the server error log for the cause.

### Register the update_jwks() UDF

The plugin library also provides the `update_jwks()` user-defined function (UDF). Register the function once after the plugin loads. The UDF refreshes cached JWKS public keys at runtime. For details, see [Refresh JWKS keys](#refresh-jwks-keys).

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

An empty result set indicates that the function did not register. Check the server error log for the cause.

## Configure the plugin

The plugin reads the list of trusted Identity Providers from a single JSON document. The administrator supplies the document through the `auth_openid_connect_configuration` system variable. The variable accepts the document inline or as a path to a file.

`SET GLOBAL` requires the `SYSTEM_VARIABLES_ADMIN` privilege. `SET PERSIST_ONLY` additionally requires `PERSIST_RO_VARIABLES_ADMIN`.

### Configuration schema

Each top-level key in the JSON document is the IDP name. User accounts reference this name in the `IDENTIFIED ... AS` clause. The value is an object with the following members:

| Key | Required | Description |
|---|---|---|
| `audiences`   | No                       | An array of allowed `aud` claim values. The plugin rejects the token when the `aud` claim does not match. The plugin omits the audience check when this key is absent. |
| `group-claim` | No                       | The name of the JWT claim that lists the user group memberships, such as `groups`. The claim value must be a string or an array of strings. |
| `group-role`  | No                       | An array of single-key objects that map IDP group names to MySQL role names. The mapping pairs with `group-claim`. |
| `issuer-name` | Yes                      | The exact value of the `iss` claim that the IDP issues. The plugin matches this value against the token's `iss` claim. |
| `jwks-url`    | When `keys` is absent    | The HTTPS URL of the IDP JWKS endpoint. The plugin fetches and caches keys from the URL. The plugin can refresh keys at runtime through the `update_jwks()` UDF. HTTP URLs are accepted for testing only and emit a warning. |
| `keys`        | When `jwks-url` is absent | An array of JSON Web Key (JWK) objects that verify token signatures. Each entry must include `kty` (`RSA` or `EC`), `kid`, and the algorithm-specific parameters. RSA keys require `n` and `e`. EC keys require `crv`, `x`, and `y`. |

!!! tip

    Use `jwks-url` in production. IDPs rotate signing keys on a schedule, and `jwks-url` lets the plugin fetch the current keys without a configuration change.

    Use `keys` only when `jwks-url` is impractical, for example:

    * The IDP runs without a JWKS endpoint, such as a test scenario where tokens are signed by a script.

    * The server cannot reach the JWKS endpoint, such as a deployment behind a firewall that blocks outbound HTTPS. For deployments that route egress through a corporate forward proxy, see [Route JWKS traffic through an HTTP proxy](#route-jwks-traffic-through-an-http-proxy).

### Set the configuration variable

The system variable `auth_openid_connect_configuration` accepts a string with one of the following prefixes:

* `JSON://` followed by the configuration JSON inline.

* `FILE://` followed by an absolute path to a file that contains the configuration JSON.

The prefix check is case-insensitive. Setting the variable to a value without a recognized prefix fails with `ERROR 1231 (42000)`. The same error applies when the file cannot be read or parsed. Detailed messages appear in the server error log.

#### Example configuration

The following JSON document configures two trusted IDPs. The first resolves keys at runtime through a `jwks-url`. The second uses static `keys` to verify token signatures.

The `n` value is truncated for brevity. Replace `ptR4...QEASRw` with the full base64url-encoded RSA modulus from the IDP signing key.

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

The subsections that follow show three ways to load the JSON configuration into the `auth_openid_connect_configuration` system variable.

#### Configure in my.cnf

Most deployments set the variable in `my.cnf` so the configuration applies on every server start. Save the example as `/etc/mysql/oidc/idps.json`, then add the variable to the `[mysqld]` section alongside the plugin load directive:

```text
[mysqld]
plugin-load-add=auth_openid_connect.so
auth_openid_connect_configuration='FILE:///etc/mysql/oidc/idps.json'
```

The `plugin-load-add` line matches the option shown in [Install the plugin](#install-the-plugin). The same prefixes apply to the variable: `FILE://` for an external file or `JSON://` for an inline document. Inline JSON in `my.cnf` requires careful quote escaping and is harder to maintain. Prefer the `FILE://` form for `my.cnf` deployments.

The variable also accepts a `--auth_openid_connect_configuration` command-line argument when starting `mysqld` directly. This form suits scripted automation.

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

    A `SET GLOBAL` assignment does not survive a server restart. Persist the configuration through `SET PERSIST_ONLY` or `my.cnf` to avoid an authentication outage on the next restart.

Skip this step if you already set the variable in [my.cnf](#configure-in-mycnf). The `my.cnf` value loads on every server start and does not require `SET PERSIST_ONLY`.

Otherwise, persist the configuration with the following statement:

```sql
SET PERSIST_ONLY auth_openid_connect_configuration =
  'FILE:///etc/mysql/oidc/idps.json';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    ```

## Create a user (individual account)

In direct authentication, one MySQL account maps to one user identity in the IDP. The mapping is encoded as a JSON object in the `IDENTIFIED ... AS` clause:

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

For Keycloak, the `sub` claim contains the user UUID. For other providers, the claim may contain an email address or another stable identifier.

The server validates the JSON at connection time, not at user creation. The connection fails when either field is missing. The connection also fails when the configuration does not contain the referenced IDP.

Grant privileges to the account with `GRANT`, the same as any other MySQL account.

For deployments where many IDP users share a single MySQL account, see [Proxying](#proxying). One MySQL proxied account maps to one IDP group. The IDP users in that group inherit the same privileges.

## Obtain an Identity token

The plugin requires the ID token issued by the IDP. The ID token is distinct from the access token. Production environments use the OAuth 2.0 flow that the IDP recommends. Common choices include authorization code with Proof Key for Code Exchange (PKCE) and device authorization.

The following example uses [Keycloak :octicons-link-external-16:](https://www.keycloak.org/securing-apps/oidc-layers) and the password grant. Replace placeholders with values from your IDP:

!!! warning "Password grant is for testing only"

    The password grant (`grant_type=password`) is deprecated in OAuth 2.1 and omitted from modern best-practice guidance. Use this flow only for local automation, scripts, and internal testing.

    For production CLI clients, use the [Device Authorization Grant :octicons-link-external-16:](https://datatracker.ietf.org/doc/html/rfc8628) or authorization code with PKCE. These flows do not require the client to handle user credentials directly.

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

The `scope=openid` parameter is required. Without `scope=openid`, the IDP returns an access token but no ID token. The `client_id` must reference a client registered in the IDP. The client must permit the relevant grant type.

!!! note "Keycloak client configuration"

    For Keycloak, the ID token `aud` claim equals the `client_id`. Set `audiences` in the plugin configuration to match. The preceding example uses `client_id=mysql-oidc`, so the configuration uses `"audiences": ["mysql-oidc"]`.

    Public clients (Access Type: public) send only the `client_id`. Confidential clients (Access Type: confidential) require a `client_secret` parameter:

    ```bash
    -d 'client_secret=<CLIENT_SECRET>'
    ```

    Retrieve the secret from the Keycloak admin console under Clients > mysql-oidc > Credentials.

The file must contain only the raw compact-serialized JWT. The JWT is three base64url segments joined by dots, with no surrounding whitespace, JSON wrapper, or `Bearer ` prefix.

For other IDPs, see the vendor documentation. Examples: [Okta token endpoint :octicons-link-external-16:](https://developer.okta.com/docs/reference/api/oidc/#token) and [Microsoft Entra ID OAuth 2.0 token endpoint :octicons-link-external-16:](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow).

## Connect with a client

A client locates the Identity token file through the `--authentication-openid-connect-client-id-token-file` option. The plugin reads no other source. The plugin does not consult an environment variable.

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

The MySQL client reads `[client]` at startup. A command-line value overrides the value from `my.cnf`.

The client refuses to authenticate when any of the following conditions occur:

* The `--authentication-openid-connect-client-id-token-file` option is missing from both the command line and `my.cnf`.

* The token file is missing, empty, or larger than 10 KB.

* The token file does not contain a syntactically valid JWT.

* The connection between the client and server is not secured by TLS, a Unix socket, or shared memory.

## Map groups to MySQL roles

When `group-claim` and `group-role` are both configured for an IDP, the plugin inspects the named claim at connection time. The plugin associates each matching MySQL role with the connection. The user activates the role with [`SET ROLE` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/set-role.html).

Consider the following configuration fragment:

```json
"group-claim": "groups",
"group-role": [
  { "acc": "accounting" },
  { "eng": "engineering" }
]
```

Suppose a token has the `groups` claim with the value `["acc", "hr"]`. The connection then exhibits the following behavior:

* `SET ROLE accounting` succeeds: `acc` maps to the `accounting` role.

* `SET ROLE engineering` fails: `eng` is not present in the token.

* `SET ROLE hr` fails: `hr` has no role mapping.

<!-- External roles were not revoked is added based on a comment from [PS-11248](https://perconadev.atlassian.net/browse/PS-11248) -->

### Grant and revoke external roles at connection time

Percona Server maintains a container of external roles for each user account. External roles are MySQL roles that an authentication plugin grants when a user connects.

At each connection, the server compares the roles returned by the plugin against the roles already recorded in the container:

* The server grants any returned role that is not yet in the container. Roles already in the container remain granted.

* The server revokes any external role that exists in the container but was not returned by the plugin.

* The server updates the container to match the roles actually granted to the session.

The OIDC plugin determines group membership from the group claim in the Identity token. The claim name is configured with `group-claim`. The plugin maps matching groups to MySQL roles through `group-role`.

External role privileges are applied at connection time, not continuously. Percona Server does not synchronize with the Identity Provider between connections. A user removed from a group at the IDP retains external role privileges until the next connection. The token on that connection must no longer contain the group.

The roles must already exist on the server. The plugin does not create roles automatically.

The group claim must be a JSON array of strings or a single string. Any other type causes authentication to fail with the message `cannot parse groups claim in the token`.

!!! note "Keycloak claim shape"

    The plugin reads `group-claim` as a top-level field in the token. The plugin does not traverse nested objects. A claim path such as `realm_access.roles` is not supported.

    Keycloak places realm roles inside `realm_access.roles` and client roles inside `resource_access.<client>.roles` by default. Configure a Keycloak client scope mapper that emits a flat top-level claim:

    * For Keycloak groups, add a `Group Membership` mapper with `Full group path` enabled.

    * For realm roles, add a `User Realm Role` mapper with `Multivalued` enabled.

    Set `Token Claim Name` to match the value of `group-claim` in the plugin configuration. See the Keycloak [Protocol Mappers :octicons-link-external-16:](https://www.keycloak.org/docs/latest/server_admin/#protocol) documentation for the exact UI paths.

## Proxying

The plugin supports MySQL [proxy users :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/proxy-users.html) so multiple IDP identities can share a single MySQL account. The proxy target is selected by IDP group membership. For the field combinations that select each mode, see [How does OpenID Connect authentication work?](#how-does-openid-connect-authentication-work).

Proxying reduces administrative overhead in deployments with many IDP users. One MySQL proxied account serves every IDP user in a group. DBAs do not maintain a MySQL account per user, and they do not synchronize IDP and MySQL user lists. The pattern matches how MySQL [LDAP authentication](ldap-authentication.md) is typically deployed.

!!! warning

    Proxy modes do not verify the `sub` claim. Any token signed by a configured IDP that contains the required group is accepted. Use proxy modes only when group membership is your trust boundary.

Configure the plugin and IDP before you use the proxy examples. The IDP must issue tokens with a `groups` claim. For the configuration baseline, see [Configure the plugin](#configure-the-plugin) and [Map groups to MySQL roles](#map-groups-to-mysql-roles).

The two subsections that follow show end-to-end examples for both proxy modes. Both use the [`mysql_no_login` :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/no-login-pluggable-authentication.html) plugin so proxy target accounts cannot authenticate directly.

### Named-group proxying

In named-group proxying, the connecting MySQL user names the IDP group for the session. Named-group proxying suits users who belong to multiple groups and need to choose between them per session.

Create one MySQL account per group. The `group` field in the `AS` JSON pins the account to one IDP group:

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

Create a `mysql_no_login` proxy target for each group, then grant `PROXY`:

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

The proxy target accounts hold the privileges that the proxied session inherits. Grant privileges to the targets with `GRANT`, the same as any other MySQL account.

The token holder selects a group by choosing the matching MySQL user at connect time. The token must include the chosen group in the `groups` claim:

```bash
mysql -u marketing \
      --authentication-openid-connect-client-id-token-file=id_token.jwt
```

After connecting, the session reflects the proxied target:

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

`USER()` shows the handshake account (`marketing`). `CURRENT_USER()` shows the proxied target (`/marketing@%`), which holds the privileges the session inherits.

### Anonymous proxying

In anonymous proxying, the connecting username is irrelevant. The plugin proxies to a target named after the first group in the token's `groups` claim.

!!! warning "Group ordering hazard"

    The plugin selects the proxy target from index 0 of the `groups` claim. JSON arrays preserve insertion order, but the IDP controls that order. An alphabetical sort, an added group, or an IDP policy change can shift index 0 silently. The session then inherits a different proxy target without warning.

    Anonymous proxying is safe only when one of these conditions holds:

    * Each IDP user belongs to exactly one privilege-bearing group.

    * The IDP guarantees a stable position for the privileged group at index 0.

    Otherwise, use [Named-group proxying](#named-group-proxying). The target is selected by the `IDENTIFIED ... AS` clause and is not affected by token ordering.

Create a single anonymous MySQL account that any handshake username matches:

```sql
CREATE USER ''@''
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak"}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

Create a `mysql_no_login` proxy target for each group, then grant `PROXY` to the anonymous account:

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

Connect with any handshake username. The first group in the token selects the proxied target:

```bash
mysql -u anyname \
      --authentication-openid-connect-client-id-token-file=id_token.jwt
```

After connecting, the session reflects the proxied target:

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

If a token has multiple groups, only the first group selects the target. To make the choice explicit, use named-group proxying instead.

## Refresh JWKS keys

When you configure an IDP with `jwks-url`, the plugin loads keys at startup. The plugin also reloads keys on every assignment to `auth_openid_connect_configuration`. Keys may rotate at the IDP between configuration changes. The `update_jwks()` UDF refreshes cached keys without changing the configuration. Register the UDF as part of plugin installation. See [Register the update_jwks() UDF](#register-the-update_jwks-udf).

The plugin does not refresh keys automatically. The plugin ignores HTTP cache headers such as `Cache-Control`, `Expires`, and `ETag`. Cached keys remain valid until a refresh trigger fires.

The plugin defines three refresh triggers:

* Server start with a configured `jwks-url`

* Assignment to `auth_openid_connect_configuration`

* A successful call to `update_jwks()`

Schedule the UDF when your IDP rotates keys on a fixed cadence. See [Schedule periodic refresh](#schedule-periodic-refresh) for an event-based example.

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
| `>= 0` | The number of IDPs whose keys were successfully refreshed. |
| `-1` | The named IDP is not in the configuration. |
| `-2` | An unexpected error occurred during the refresh. Details are written to the server error log. |

### Schedule periodic refresh

Schedule the UDF to align the cache with the key rotation policy of the IDP. A MySQL event is the simplest option. The event runs inside the server. External tooling such as `cron` or a Kubernetes CronJob is a valid alternative.

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

The event scheduler must be running for the event to fire. Confirm and enable the scheduler at runtime:

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

Choose an interval that matches the key rotation cadence of the IDP. Hourly suits most deployments. Consult the IDP documentation for the exact cadence.

### Route JWKS traffic through an HTTP proxy

The plugin fetches `jwks-url` content with libcurl. The plugin sets no proxy options of its own. The IDP configuration JSON exposes no proxy field.

Libcurl reads standard proxy environment variables from the mysqld process environment:

* `https_proxy` for HTTPS JWKS endpoints

* `http_proxy` for HTTP JWKS endpoints

* `no_proxy` for hostnames that bypass the proxy

The variables must reach mysqld, not the interactive shell that the DBA uses. Set them in the service unit on systems that use systemd:

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

    The plugin reads the environment at process start. The plugin applies updated proxy values only after mysqld restarts.

For environments that block all outbound traffic, configure each IDP with a static `keys` array instead of `jwks-url`. See [Configuration schema](#configuration-schema) for the required JWK fields. Distribute the JWK set to the database host out of band.

## Uninstall the plugin

!!! warning

    Drop every UDF that depends on the plugin before you uninstall the plugin. A stale function definition remains when `UNINSTALL PLUGIN` runs while a UDF still references the library. Drop scheduled events that call the UDF as well.

If you scheduled a refresh event, drop the event first:

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

The following table summarizes the system variable. For the full list of system variables, see [Percona Server system variables](percona-server-system-variables.md).

| Variable name | Default value | Scope | Dynamic | Valid values |
|---|---|---|---|---|
| `auth_openid_connect_configuration` | `{}` | Global | Yes | A string prefixed with `JSON://` or `FILE://` |

The variable holds the configuration of trusted OpenID Connect Identity Providers. The value must start with `JSON://` for an inline JSON document. The value must start with `FILE://` for an absolute path to a JSON file. The configuration schema appears in [Configure the plugin](#configure-the-plugin).

The variable accepts assignments from `SET GLOBAL`, `SET PERSIST_ONLY`, the `my.cnf` option file, and the `mysqld` command line. For examples, see [Set the configuration variable](#set-the-configuration-variable).

The plugin validates the variable at assignment. The server rejects an unknown prefix, malformed JSON, or an unreadable file with `ERROR 1231 (42000)`.

A configuration that references an unreachable `jwks-url` is accepted at assignment. The plugin writes a warning to the server error log. Authentication against that IDP fails until the keys load successfully. Run `update_jwks()` after the IDP becomes reachable.

## User-defined function reference

### update_jwks()

The following table summarizes the function:

| Property    | Value                       |
|---|---|
| Return type | `INTEGER`                   |
| Library     | `auth_openid_connect.so`    |
| Arguments   | Zero or one string          |

The function refreshes cached JWKS public keys for one IDP or for all configured IDPs. For details on return values, see [Refresh JWKS keys](#refresh-jwks-keys).

## Troubleshoot connection failures

The plugin writes a single diagnostic line to the server error log on each rejected connection. The client receives a generic authentication failure to avoid leaking configuration details.

The following table follows a Symptoms, Diagnosis, and Solution model for the most frequent failures:

| Symptom | Diagnosis | Solution |
|---|---|---|
| `unsecure connection, use TLS, socket or memory` in the server log              | The client connected over plaintext TCP.                                                                          | Reconnect with TLS, a Unix socket, or shared memory.                                |
| `IDP not found: <name>` in the server log                                       | The `identity_provider` value in the user `IDENTIFIED ... AS` clause does not match a key in the configuration.   | Update the user definition or the configuration so the IDP names align.             |
| `audience not authorized` in the server log                                     | The token `aud` claim does not match any value in the `audiences` configuration. For Keycloak, the ID token `aud` equals the `client_id`. | Set `audiences` to match the `aud` claim in the ID token. For Keycloak, use the `client_id` value (for example, `["mysql-oidc"]`). |
| `invalid sysvar prefix, expected FILE:// or JSON://` in the server log          | The `auth_openid_connect_configuration` value lacks a valid prefix.                                               | Reset the variable with the correct `JSON://` or `FILE://` prefix.                  |
| `JWKS configuration is insecure, use HTTPS` warning in the server log           | The `jwks-url` uses `http://`.                                                                                    | Replace the URL with an `https://` endpoint before production use.                  |
| `JWKS: HTTP GET from <url> failed` in the server log                            | The IDP is unreachable or returned a non-2xx status. The host may also require an outbound HTTP proxy.            | Verify network reachability. For corporate egress, see [Route JWKS traffic through an HTTP proxy](#route-jwks-traffic-through-an-http-proxy). Run `update_jwks()` after the IDP recovers. |
| `incorrect number of keys` in the server log                                    | The token has no `kid` header but the plugin loaded multiple keys for the IDP.                                    | Set `keys` to a single entry that matches the IDP signing key.                      |
| `user is not a member of the required group` in the server log                  | The account uses named-group proxying but the token's `groups` claim does not contain the configured `group`.     | Verify the user's group membership at the IDP, or have the user select a different MySQL account that maps to a group they belong to. |
