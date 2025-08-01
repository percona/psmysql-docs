# Apt pinning the Percona Server for MySQL {{vers}} packages

Apt pinning helps you control which version of a package is installed from different repositories. This is useful when you want to stay on a specific release such as Percona Server for MySQL 8.4 and avoid automatic upgrades from other sources.

To pin the Percona Server for MySQL 8.4 packages, follow these steps:
{.power-number}

1.  Create a preferences file in `/etc/apt/preferences.d/` named `00percona.pref`:

    ```{.bash data-prompt="$"}
    $ sudo nano /etc/apt/preferences.d/00percona.pref
    ```

2.  Add the pinning configuration content to the file:

    ```ini
    Package: percona-server-server
    Pin: release o=Percona Development Team,a=stable
    Pin-Priority: 1001
    ```

    * The `Package` field specifies the exact name of the package.
    * The `Pin` field identifies the origin of the package, which is the Percona repository.
    * The `Pin-Priority` field sets the priority level. A value above 1000 ensures this version is preferred over others.

    Save and close the file.

3.  Update package lists to refresh your package sources:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    ```

4.  Install Percona Server for MySQL 8.4 using the following command:

    ```{.bash data-prompt="$"}
    $ sudo apt install percona-server-server
    ```

    Your system prioritizes the version from the Percona repository according to your pinning settings.

## Learn more

For additional details, visit the [debian wiki](https://wiki.debian.org/AptConfiguration?action=show&redirect=AptPreferences).
