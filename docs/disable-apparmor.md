# Disable AppArmor

## Disable AppArmor Risks

Using AppArmor might seem like an extra step, but if you disable it, your server could face security risks.

Do not disable AppArmor in production environments. Instead, use AppArmor's security features and configure it to fit your needs.

## Risks

| Risk | Description |
|---|---|
| Increased Attack Surface | Disabling AppArmor removes security restrictions, potentially allowing unauthorized access to Percona Server for MySQL's files and functionalities. This creates an attractive target for attackers seeking to exploit vulnerabilities or gain control of your database. |
| Unforeseen Security Holes | AppArmor can help mitigate even unknown vulnerabilities by restricting unexpected behaviors. Disabling it leaves your system more susceptible to these hidden security holes. |
| Accidental Misconfigurations | Even with good intentions, manual configuration of access controls can be error-prone. AppArmor provides a pre-defined security layer, reducing the risk of human error in managing permissions. |

## Disable procedure

If AppArmor must be disabled, run the following commands:
{.power-number}

1. Check the status.

    ```{.bash data-prompt="$"}
    $ sudo apparmor_status
    ```

2. Stop and disable AppArmor.

    ```{.bash data-prompt="$"}
    $ sudo systemctl stop apparmor
    $ sudo systemctl disable apparmor
    ```

## AppArmor links

[AppArmor](apparmor.md)<br>
[AppArmor Profiles](apparmor-profiles.md)<br>
[Manage AppArmor Profiles](manage-apparmor-profiles.md)<br>
[Configure AppArmor](configure-apparmor.md)<br>
[Troubleshoot AppArmor](troubleshoot-apparmor.md)