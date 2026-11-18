> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# AppArmor profile modes

AppArmor profile modes determine how applications interact with system resources. You can mix enforce mode profiles and complain mode profiles in your server.

| Mode     | Description                                                                                                          |
| -------- | -------------------------------------------------------------------------------------------------------------------- |
| Enforce  | Restricts MySQL processes according to the rules defined in the profile. Any action violating these rules is denied. |
| Complain | Allows MySQL processes to take restricted actions, but logs these actions for review.                                |
| Disabled | Turns off profile restrictions entirely, allowing MySQL processes to take any action without logging.                |

Understanding these modes helps MySQL developers ensure that their applications can access necessary resources while maintaining system security.

## Benefits

| Benefit              | Description                                                                                                          |
| -------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Enhanced Security    | AppArmor profile modes, such as Enforce and Complain, help enforce security policies to prevent unauthorized access. |
| Easy Troubleshooting | Profile modes provide flexibility in troubleshooting access issues by allowing developers to switch between modes.   |

### Disadvantages

| Disadvantage         | Description                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Limited Flexibility  | Profile modes may restrict certain actions or access, potentially limiting the functionality of MySQL applications. |
| Complexity           | Understanding and managing different profile modes can be complex for beginner developers, leading to errors.       |
| Debugging Challenges | Troubleshooting issues related to profile modes, such as DENIED entries in logs, may require additional expertise.  |

## AppArmor links:

[AppArmor](https://docs.percona.com/percona-server/8.4/apparmor.html)\
[Manage AppArmor Profiles](https://docs.percona.com/percona-server/8.4/manage-apparmor-profiles.html)\
[Disable AppArmor](https://docs.percona.com/percona-server/8.4/disable-apparmor.html)\
[Configure AppArmor](https://docs.percona.com/percona-server/8.4/configure-apparmor.html)\
[Troubleshoot AppArmor](https://docs.percona.com/percona-server/8.4/troubleshoot-apparmor.html)
