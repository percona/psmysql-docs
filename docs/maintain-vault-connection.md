# Maintain the Vault connection

Installation of the [keyring vault component](use-keyring-vault-component.md) is the first step. The most common production failure of `keyring_vault` is a lost connection to Vault, not a misconfigured component. Two conditions cause the loss:

* The token used by the component expires.

* The Vault server seals.

Either condition prevents Percona Server from fetching master keys.

The `keyring_vault` component reads the `token` value from the configuration file at startup. The component then uses the stored token for the lifetime of the `mysqld` process. The component does not renew the token and does not reread the configuration file at runtime. Renewal and rotation must run outside MySQL, on the Vault side or through a helper process.

## Renew the Vault token

Every Vault token has a time-to-live (TTL). When the TTL elapses, Vault revokes the token. Any subsequent Application Programming Interface (API) call returns HTTP 403, including the master-key fetch performed by `keyring_vault`.

The following symptoms indicate an expired or revoked token:

* `mysqld` startup fails after a restart with keyring component initialization or fetch errors.

* The statement `ALTER INSTANCE ROTATE INNODB MASTER KEY` fails.

* Opening an encrypted table after a restart fails with a keyring error.

* The row in `performance_schema.keyring_component_status` shows the component as loaded but unable to reach Vault.

Because the component does not renew tokens, choose one of the following patterns to keep the configured token valid:

### Option 1 (recommended): Periodic tokens

A [periodic token :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/concepts/tokens#periodic-tokens) has no maximum TTL. The token continues to work indefinitely as long as a renewal occurs within each period. This renewal model matches the lifetime of a long-running database server.

Create a Vault role that issues periodic tokens, then mint the token referenced by `component_keyring_vault.cnf`:

```bash
vault write auth/token/roles/percona-keyring \
    allowed_policies="percona-keyring-policy" \
    period="24h" \
    renewable=true

vault token create -role=percona-keyring -format=json
```

Store the issued token in the `token` field of the `keyring_vault` configuration file. Pair the periodic token with a renewer (see Option 2) so a renewal occurs at least once per `period`.

### Option 2: Sidecar renewer

A sidecar process must call `vault token renew` before each expiry. The requirement applies whether the token is periodic or has a fixed maximum TTL. The following table compares two common implementations:

| Implementation | Description |
|---|---|
| `vault agent` | Configure `vault agent` with an `auto_auth` block. The agent authenticates, writes the issued token to a sink, and renews the token automatically. Configure `component_keyring_vault.cnf` to read a token issued by the same auth method, or generate the configuration with agent templating. |
| `systemd` timer or cron job | Schedule `vault token renew` at an interval shorter than the token TTL, for example hourly for a 24-hour token. Run the job under a dedicated service account, not as `root`, and forward renewal failures to the alerting system. |

Configure alerts on renewal failure. Without alerts, a failed renewer behaves the same as no renewer at all. The failure surfaces only at the next `mysqld` restart, when startup fails.

### Operational checklist

* Treat the `token` value as a secret equal in sensitivity to the Vault unseal keys. Restrict file permissions on `component_keyring_vault.cnf` to the `mysql` user.

* Monitor the token TTL with `vault token lookup`. Alert when the remaining TTL drops below a safe threshold.

* Rotate the token only during a maintenance window. Update the configuration file, then restart `mysqld`. The component reads the file only at startup.

* Assign one token to one server. The one-token-per-server rule complements the `secret_mount_point` warning in [Configure the keyring vault component](use-keyring-vault-component.md#configure-the-keyring-vault-component).

## Handle a sealed Vault

The `keyring_vault` component calls the Vault HTTP API at startup and during every key operation. A [sealed Vault :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/concepts/seal) returns HTTP 503 for any request to the secrets engine. The component cannot read or write keys against a sealed Vault, even with a valid token.

Vault becomes sealed in the following situations:

* A host reboot or package upgrade restarts the Vault process.

* An operator runs `vault operator seal`.

* Vault seals itself in response to a detected integrity issue.

Percona Server behavior during a sealed Vault depends on timing:

| State | Behavior |
|---|---|
| `mysqld` running, keys cached in memory | Reads and writes against the open encrypted tables continue to succeed. |
| `mysqld` running, additional key fetch required | Operations that require an additional key fetch fail. Examples include opening an encrypted table that was not already open, rotating the master key, and creating an encrypted tablespace. |
| `mysqld` restarted while Vault remains sealed | `InnoDB` cannot unwrap tablespace keys. Startup fails or encrypted tables remain inaccessible until Vault is unsealed. |

### Recommended practice

* Unseal Vault before starting or restarting Percona Server. Confirm that `vault status` reports `Sealed` as `false`.

* Automate the unseal step with [auto-unseal :octicons-link-external-16:](https://developer.hashicorp.com/vault/docs/concepts/seal#auto-unseal). Use a cloud KMS, Hardware Security Module (HSM), or Transit secret engine as the backing store. A Vault restart then completes without manual intervention. A Vault reboot outside business hours blocks every Percona Server that depends on the sealed Vault.

* Order the startup dependencies. Configure `mysqld` to depend on Vault being unsealed, not only on Vault being reachable. Apply the dependency when both processes run on the same host or under the same orchestrator.

* Monitor the `/v1/sys/health` endpoint of Vault. The endpoint reports seal status. Alert on `sealed=true` independently of database telemetry, so operators can respond before the next `mysqld` restart.

* Keep unseal keys and recovery keys offline and distributed across custodians. The custody practice belongs to the Vault domain rather than Percona. Lost unseal keys produce permanent data loss for every Percona Server that depends on the sealed Vault.

## See also

Percona Server documentation:

* [Data at Rest Encryption](data-at-rest-encryption.md) describes how Percona Server uses the keyring to protect tablespace data.

* [Keyring components overview](keyring-components-plugins-overview.md) compares the available keyring components.

* [Rotate the master encryption key](rotate-master-key.md) covers the full rotation procedure and required privileges.

* [Use the keyring vault component](use-keyring-vault-component.md) describes installation and configuration of the `keyring_vault` component.

HashiCorp documentation:

* [Installing Vault :octicons-link-external-16:](https://www.vaultproject.io/docs/install/index.html)

* [Production Hardening :octicons-link-external-16:](https://learn.hashicorp.com/vault/operations/production-hardening)
