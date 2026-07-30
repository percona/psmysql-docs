# Get started with OpenID Connect authentication

The following steps configure OpenID Connect (OIDC) authentication against a Keycloak realm. Allow about 20 minutes.

You install the server-side plugin, configure trust for Keycloak, create a MySQL user, obtain an ID token, and connect. See [OpenID Connect authentication](openid-connect-authentication.md) for production guidance, the configuration schema, and troubleshooting.

## Before you begin

Gather the resources in the following list:

* Percona Server for MySQL {{vers}} with the `auth_openid_connect.so` library in `plugin_dir`

* A reachable Keycloak server with a configured realm, an OIDC client, and at least one user in a group

* TLS, a Unix domain socket, or shared memory between the MySQL client and the server

* `curl` and `jq` on the workstation that obtains the ID token

* A MySQL administrator account with the `INSERT` privilege on `mysql.plugin`, the `SYSTEM_VARIABLES_ADMIN` privilege, and the `CREATE USER` privilege

## Quickstart values

Replace the following example values with values from your environment:

| Item                | Example value                            | Description                                          |
|---|---|---|
| Keycloak host       | `keycloak.example.com`                   | Hostname of the Keycloak server                      |
| Realm               | `master`                                 | Keycloak realm name                                  |
| OIDC client ID      | `mysql-oidc`                             | Client registered in the realm                       |
| IDP name in MySQL   | `my-keycloak`                            | Top-level key in the JSON configuration              |
| Keycloak username   | `alice`                                  | User in the realm                                    |
| `sub` claim value   | `4c28d537-a635-4b6d-957f-58e3c8860bcc`   | User UUID from Keycloak                              |
| Keycloak group      | `/accounting`                            | Group for the user                                   |
| MySQL role          | `accounting`                             | Role mapped to the group                             |

## Install the OIDC plugin

Load the plugin during the current server session:

```sql
INSTALL PLUGIN auth_openid_connect SONAME 'auth_openid_connect.so';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

Confirm that the plugin loaded:

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

To load the plugin at server start, see [Install the plugin](openid-connect-authentication.md#install-the-plugin).

## Configure trust for Keycloak

Set the `auth_openid_connect_configuration` system variable to a JSON document for the Keycloak realm. The plugin fetches signing keys from the realm JWKS endpoint:

```sql
SET GLOBAL auth_openid_connect_configuration = 'JSON://{
  "my-keycloak": {
    "issuer-name": "https://keycloak.example.com/realms/master",
    "jwks-url": "https://keycloak.example.com/realms/master/protocol/openid-connect/certs",
    "audiences": ["mysql-oidc"],
    "group-claim": "groups",
    "group-role": [
      { "/accounting": "accounting" }
    ]
  }
}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

`SET GLOBAL` lasts only until the next restart. To persist the configuration, run the same statement with `SET PERSIST_ONLY`. See [Persist the configuration](openid-connect-authentication.md#persist-the-configuration).

## Create demo objects and an OIDC user

Create demo objects in the following order:

1. Create a database and table for the demo.

2. Create a MySQL role and grant table access.

3. Create the OIDC-authenticated user.

Create a small database that the OIDC user reads through the role:

```sql
CREATE DATABASE oidc_demo;
CREATE TABLE oidc_demo.invoices (id INT, amount DECIMAL(10, 2));
INSERT INTO oidc_demo.invoices VALUES (1, 99.95), (2, 145.00);
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.00 sec)
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 2 rows affected (0.00 sec)
    ```

Create the MySQL role and grant access to the table:

```sql
CREATE ROLE accounting;
GRANT SELECT ON oidc_demo.* TO accounting;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 0 rows affected (0.00 sec)
    ```

Create the OIDC-authenticated user. Replace the `user` value with the `sub` claim that Keycloak issues for the account:

```sql
CREATE USER 'alice'@'%'
  IDENTIFIED WITH 'auth_openid_connect'
  AS '{"identity_provider": "my-keycloak", "user": "4c28d537-a635-4b6d-957f-58e3c8860bcc"}';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

The OIDC user does not need an explicit `GRANT` for `oidc_demo`. When the token includes the `/accounting` group, the user inherits access from the `accounting` role.

## Obtain an ID token from Keycloak

Run the following command on the workstation. The command writes the ID token to `/run/user/1000/id_token.jwt`. Replace `<password>` with the password for `alice`:

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

The password grant suits scripted demos. Production deployments use authorization code with Proof Key for Code Exchange (PKCE) or device authorization. See [Obtain an Identity token](openid-connect-authentication.md#obtain-an-identity-token) for details.

!!! note

    The plugin requires the ID token, not the access token. The Keycloak token request selects the `id_token` field from the response.

    The example assumes a public Keycloak client. Confidential clients require an additional `-d 'client_secret=<SECRET>'` parameter. See [Obtain an Identity token](openid-connect-authentication.md#obtain-an-identity-token) for details.

## Connect with the OIDC token

Connect as `alice` and pass the token file:

```bash
mysql --host=mysql.example.com \
      --ssl-mode=REQUIRED \
      --user=alice \
      --authentication-openid-connect-client-id-token-file=/run/user/1000/id_token.jwt
```

Successful authentication opens the MySQL prompt. The plugin rejects the connection when the token is missing, expired, or sent over an unsecured transport.

## Verify the role mapping

Confirm the connected identity:

```sql
SELECT CURRENT_USER();
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------+
    | CURRENT_USER() |
    +----------------+
    | alice@%        |
    +----------------+
    1 row in set (0.00 sec)
    ```

Activate the role and read from the table:

```sql
SET ROLE accounting;
SELECT * FROM oidc_demo.invoices;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)

    +------+--------+
    | id   | amount |
    +------+--------+
    |    1 |  99.95 |
    |    2 | 145.00 |
    +------+--------+
    2 rows in set (0.00 sec)
    ```

The token contains `/accounting` in the `groups` claim, so `SET ROLE accounting` succeeds. A user without the group sees `ERROR 3530 (HY000)`.

## Clean up

Remove the demo objects when you finish:

```sql
DROP USER 'alice'@'%';
DROP ROLE accounting;
DROP DATABASE oidc_demo;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 1 row affected (0.01 sec)
    ```

To remove the plugin and any UDFs, see [Uninstall the plugin](openid-connect-authentication.md#uninstall-the-plugin).

## Additional resources

* [OpenID Connect authentication](openid-connect-authentication.md): full reference, configuration schema, and troubleshooting

* [Authentication methods](authentication-methods.md): overview of supported plugins

* [SSL improvements](ssl-improvement.md): configure the encrypted transport that OIDC requires

* [Keycloak server administration guide :octicons-link-external-16:](https://www.keycloak.org/docs/latest/server_admin/): configure realms, clients, users, and groups
