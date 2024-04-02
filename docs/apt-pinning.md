# Apt pinning the Percona Server for MySQL 8.0 packages

Apt pinning is a feature in Debian and its derivatives like Ubuntu, allowing you to prioritize package versions from different repositories. When you pin the Percona Server for MySQL 8.0 packages, you tell your system's package manager to prefer this specific version over others available in different repositories. This ability is beneficial when you want to ensure that you're running a specific version of Percona Server for MySQL due to compatibility or stability reasons, despite newer versions available elsewhere.

To apt pin Percona Server for MySQL 8.0, you must first open the `/etc/apt/preferences.d/` directory and create a new file for the Percona Server package. In this file, you will specify the package name followed by a pinning priority. A higher priority ensures that the version of Percona Server you wish to install is preferred over other versions. 

You should include the version number of the Percona Server in the 'Package' field to identify the package. 

Then, assign a priority in the 'Pin-Priority' field; a common practice is to set it above 1000 to prioritize it over other packages. 
The pinning takes place in the `preference` file. To pin a package, set the `Pin-Priority` to higher numbers. 
 
Make a new file `/etc/apt/preferences.d/00percona.pref`. For example, add the following to the `preference` file:

```{.text .no-copy}
Package: 
Pin: release o=Percona Development Team
Pin-Priority: 1001
```

Save this file and update your package lists with `sudo apt update`. Finally, install Percona Server for MySQL 8.0 with `sudo apt install percona-server-server-8.0`, and apt will adhere to your pinning preferences.

For more information, see [debian wiki on AptConfiguration](https://wiki.debian.org/AptConfiguration?action=show&redirect=AptPreferences).
