# Install Percona Server for MySQL 8.4 using DEB packages

Percona distributes DEB packages in tar bundles that contain multiple related packages. Two bundle types are available:

* Full bundle: Contains all Percona Server packages including server, client, test packages, debug symbols, and source files

* Minimal bundle: Contains only the essential server and client packages needed for basic operation

Choose the bundle type based on your requirements. Download the bundle to access the components you need, then extract and install the individual DEB files using your system package manager.

## When to use this installation method

Skills needed: Basic system administration, command line familiarity

Advantages:

* Provides precise version control over installed packages

* Works in offline environments without internet access

* Allows installation before packages appear in standard repositories

* Enables administrators to validate packages before deployment

Disadvantages:

* Requires manual download and extraction steps

* Does not receive automatic updates through the package manager

* Users must manually track new releases and security updates

* Takes more time than repository-based installation

Download the bundle from Percona Product Downloads. Review the Instructions for the Percona Product Download if you need assistance.

This example downloads Percona Server for MySQL {{release}} release packages for Ubuntu 22.04:

```{.bash data-prompt="$"}
$ wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-{{release}}/binary/debian/jammy/x86_64/Percona-Server-{{release}}-[revision hash]-jammy-x86_64-bundle.tar
```

Extract the bundle to access the individual packages:

```{.bash data-prompt="$"}
$ tar xvf Percona-Server-{{release}}-[revision hash]-jammy-x86_64-bundle.tar
```

??? example "Expected output for a full tar extraction"

    ```{.text .no-copy}
    percona-server-server_{{release}}-1.jammy_amd64.deb
    percona-server-client_{{release}}-1.jammy_amd64.deb
    percona-server-common_{{release}}-1.jammy_amd64.deb
    percona-server-dbg_{{release}}-1.jammy_amd64.deb
    percona-server-source_{{release}}-1.jammy_amd64.deb
    percona-server-test_{{release}}-1.jammy_amd64.deb
    ```

Install Percona Server for MySQL using the system package manager. Run this command as root or use sudo:

```{.bash data-prompt="$"}
$ sudo apt install ./*.deb
```

The package manager resolves dependencies automatically and installs all required components from the extracted files.