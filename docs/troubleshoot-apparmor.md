# Troubleshoot AppArmor profiles

Troubleshooting AppArmor profiles ensure that applications can access necessary resources without compromising system security. 

## Profile Modes

AppArmor profiles operate in different modes:

| Mode     | Description                                                                                  |
|----------|----------------------------------------------------------------------------------------------|
| Enforce  | Applications are restricted by profile rules, and any violation results in denial of access. |
| Complain | Applications are allowed to take restricted actions, but these actions are logged.           |
| Disabled | Profile restrictions are turned off, allowing applications to take any action without logging. |

### Check status

Use commands like `aa-status` to check the current status of AppArmor profiles. This check helps identify if profiles are enforcing or complaining about actions.

### Switch modes

You may need to switch profiles between `enforce` and `complain` modes when troubleshooting. Use `aa-enforce` to switch to enforce mode and `aa-complain` to switch to complain mode.

### Disable profiles

If necessary, profiles can be temporarily disabled. However, this is not recommended for security reasons. Use commands like `ln -s` or `aa-disable` to disable profiles.

### Reload profiles

After making changes to profiles or switching modes, reloading profiles for changes to take effect is essential. Use commands like `service apparmor reload` or `apparmor_parser -r` to reload profiles.

### Check Log Entries

 Monitor log entries for DENIED or ALLOWED actions. DENIED entries indicate that a profile is blocking an action, while ALLOWED entries suggest that an action is permitted.

### Edit Profiles

You may need to edit AppArmor profiles to troubleshoot access issues and allow specific actions. Edit the profile files in the `/etc/apparmor.d/` directory to adjust access permissions.

## AppArmor links

[AppArmor](apparmor.md)<br>
[AppArmor Profiles](apparmor-profiles.md)<br>
[Manage AppArmor Profiles](manage-apparmor-profiles.md)<br>
[Disable AppArmor](disable-apparmor.md)<br>
[Configure AppArmor](configure-apparmor.md)
