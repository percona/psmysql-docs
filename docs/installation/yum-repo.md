# Install Percona Server for MySQL from Percona RPM repository

<!-- package name: percona-server-server-8.0.13-3.1.el7.x86_64.rpm -->
Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [download page](https://www.percona.com/downloads/Percona-Server-8.0/). The
Percona yum repository supports popular RPM-based
operating systems. The easiest way to install the Percona RPM repository is to install an RPM
that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/5869161).

!!! note

    The RPM packages for Red Hat Enterprise Linux 7 and the compatible derivatives do not support TLSv1.3, as it requires OpenSSL 1.1.1, which is currently not available on this platform.



You can install Percona yum repository by running the following commands as a `root` user or with sudo.


1. Install the Percona repository

	```{.bash data-prompt="$"}
	$ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	```
	
	??? example "Expected output"
	
	    ```text
	    percona-release-latest.noarch-rpm               36 kB/s | 19 kb 00:00
	    =====================================================================
	      Package         Architecture      Version    Repository    Size
	    =====================================================================
	    Installing:
	       percona release noarch         1.0-25     @commandline  19k
	    ...
	    ```
    
2. Enable the repository:

	```{.bash data-prompt="$"}
	$ sudo percona-release setup ps80
	```
	
	If you see the following message, enter 'y' to disable the mysql module:
	
	??? example "Expected output"

        ```{.text .no-copy}
	    On RedHat 8 systems it is needed to disable dnf mysql module to install Percona-Server
	    Do you want to disable it? [y/N] 
	    ...
	    ```


3. Install the packages:

	```{.bash data-prompt="$"}
	$ sudo yum install percona-server-server
	```

### Available storage engines

Percona Server for MySQL 8.0 comes with the TokuDB storage engine and MyRocks storage engine. Install the selected storage engine as plugins.

Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. 
We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds. 
For more information, see [TokuDB Introduction](../tokudb/tokudb_intro.md).

For information on how to install and configure TokuDB, refer to the [TokuDB Installation guide](../tokudb/tokudb_installation.md).

For information on how to install and configure MyRocks, refer to the Percona [MyRocks Installation Guide](../myrocks/install.md).
	

### Percona yum Testing repository

Percona offers pre-release builds from our testing repository. To
subscribe to the testing repository, you enable the testing
repository in `/etc/yum.repos.d/percona-release.repo`. To do so,
set both `percona-testing-$basearch` and `percona-testing-noarch`
to `enabled = 1` (Note that there are three sections in this file:
release, testing, and experimental - in this case, it is the second section that requires updating).

!!! note

    You must install the Percona repository first if the installation has not been done already.
