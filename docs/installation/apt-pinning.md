# Apt pinning the Percona Server for MySQL 8.0 packages

Pinning allows you to stay on a release and get packages from a different version. In some cases, you can pin selected packages and avoid accidentally upgrading all the packages. 

The pinning takes place in the `preference` file. To pin a package, set the `Pin-Priority` to higher numbers. 
 
Make a new file `/etc/apt/preferences.d/00percona.pref`. For example, add the following to the `preference` file:

```text
Package: 
Pin: release o=Percona Development Team
Pin-Priority: 1001
```

For more information about the pinning, you can check the official [debian wiki](https://wiki.debian.org/AptConfiguration?action=show&redirect=AptPreferences).
