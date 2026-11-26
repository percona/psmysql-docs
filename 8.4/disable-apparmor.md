> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Disable AppArmor

## Disable AppArmor Risks

Using AppArmor might seem like an extra step, but if you disable it, your server could face security risks.

Do not disable AppArmor in production environments. This action can have the following risks:

| Risk                         | Description                                                                                                                                                                                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Increased Attack Surface     | Disabling AppArmor removes security restrictions, potentially allowing unauthorized access to Percona Server for MySQL’s files and functionalities. This creates an attractive target for attackers seeking to exploit vulnerabilities or gain control of your database. |
| Unforeseen Security Holes    | AppArmor can help mitigate even unknown vulnerabilities by restricting unexpected behaviors. Disabling it leaves your system more susceptible to these hidden security holes.                                                                                            |
| Accidental Misconfigurations | Even with good intentions, manual configuration of access controls can be error-prone. AppArmor provides a pre-defined security layer, reducing the risk of human error in managing permissions.                                                                         |

Instead, use AppArmor’s security features and configure it to fit your needs.

## Disable procedure

If AppArmor must be disabled, run the following commands:

1. Check the status.

   ```shell
   sudo apparmor_status
   ```

1. Stop and disable AppArmor.

   ```shell
   sudo systemctl stop apparmor
   sudo systemctl disable apparmor
   ```

## AppArmor links

[AppArmor](https://docs.percona.com/percona-server/8.4/apparmor.md)\
[AppArmor Profiles](https://docs.percona.com/percona-server/8.4/apparmor-profiles.md)\
[Manage AppArmor Profiles](https://docs.percona.com/percona-server/8.4/manage-apparmor-profiles.md)\
[Configure AppArmor](https://docs.percona.com/percona-server/8.4/configure-apparmor.md)\
[Troubleshoot AppArmor](https://docs.percona.com/percona-server/8.4/troubleshoot-apparmor.md)
