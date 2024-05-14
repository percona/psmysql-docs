# Secure Percona Server for MySQL with AppArmor

The operating system has a Discretionary Access Controls (DAC) system. AppArmor supplements the DAC with a Mandatory Access Control (MAC) system. AppArmor is the default security module for Ubuntu or Debian systems and uses profiles to define how programs access resources.

AppArmor is path-based and restricts processes by using profiles. Each profile contains a set of policy rules. Some applications may install their profile along with the application. If an installation does not also install a profile, that application is not part of the AppArmor subsystem. You can also create profiles since they are simple text files stored in the `/etc/apparmor.d` directory.

AppArmor enhances system security by enforcing strict access controls and protecting against unauthorized access and potential threats. It achieves this by defining profiles that specify how programs interact with system resources. These profiles act as a set of rules dictating a program's actions and the resources it can access. By confining each program to its designated profile, AppArmor limits the damage in case of a compromise and prevents unauthorized escalation of privileges. Additionally, AppArmor provides fine-grained control over program behavior, allowing administrators to tailor security policies to specific application requirements and minimize the attack surface. Overall, AppArmor is crucial in bolstering system security for MySQL developers, maintaining system integrity, and mitigating the risks associated with security breaches.

## AppArmor links:

[AppArmor Profiles](apparmor-profiles.md)<br>
[Manage AppArmor Profiles](manage-apparmor-profiles.md)<br>
[Disable AppArmor](disable-apparmor.md)<br>
[Configure AppArmor](configure-apparmor.md)<br>
[Troubleshoot AppArmor](troubleshoot-apparmor.md)